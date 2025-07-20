from flask import Flask, render_template, request, jsonify, send_file, send_from_directory, abort
from flask_cors import CORS
import os
import subprocess
import sys
import json
import pandas as pd
import glob
import zipfile
import shutil
from datetime import datetime
import threading
import time

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)

# Configuration
# Get the project root directory (2 levels up from src/web/)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
UPLOAD_FOLDER = os.path.join(PROJECT_ROOT, 'uploads')
OUTPUT_FOLDER = os.path.join(PROJECT_ROOT, '.output')
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv'}

# Ensure directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Global variable to track processing status
processing_status = {
    'is_processing': False,
    'current_step': '',
    'progress': 0,
    'message': '',
    'error': None
}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def clean_output_directory():
    """Clean the output directory before processing"""
    if os.path.exists(OUTPUT_FOLDER):
        shutil.rmtree(OUTPUT_FOLDER)
    os.makedirs(OUTPUT_FOLDER)

def check_ollama_available():
    """Check if Ollama is available for title generation"""
    try:
        result = subprocess.run(['curl', '-s', 'http://localhost:11434/api/tags'], 
                              capture_output=True, text=True, timeout=3)
        return result.returncode == 0 and 'qwen2.5:3b' in result.stdout
    except:
        return False

def process_youtube_shorts(youtube_url, top_n, time_range):
    """Main processing function that runs the YouTube shorts generation workflow"""
    global processing_status
    
    try:
        processing_status['is_processing'] = True
        processing_status['error'] = None
        processing_status['progress'] = 0
        
        # Step 1: Extract captions
        processing_status['current_step'] = 'Extracting captions...'
        processing_status['progress'] = 10
        caption_output = os.path.join(OUTPUT_FOLDER, "captions.txt")
        
        result = subprocess.run([
            sys.executable, "src/core/caption_extractor.py", 
            youtube_url, caption_output
        ], capture_output=True, text=True)
        
        if result.returncode != 0:
            raise Exception(f"Caption extraction failed: {result.stderr}")
        
        # Step 2: Create custom stop words if not exists
        processing_status['current_step'] = 'Setting up analysis...'
        processing_status['progress'] = 20
        custom_stop_words_path = os.path.join(PROJECT_ROOT, "config", "custom_stop_words.txt")
        if not os.path.exists(custom_stop_words_path):
            with open(custom_stop_words_path, 'w') as f:
                default_stop_words = [
                    "the", "and", "a", "to", "of", "in", "is", "it", "that", "you", 
                    "for", "on", "with", "as", "are", "be", "this", "was", "have", "by",
                    "um", "uh", "ah", "oh", "mm", "hmm", "gonna", "wanna", "like", "just"
                ]
                f.write("\n".join(default_stop_words))
        
        # Step 3: Analyze trends
        processing_status['current_step'] = 'Analyzing keyword trends...'
        processing_status['progress'] = 30
        json_path = os.path.join(OUTPUT_FOLDER, "captions.txt.json")
        output_csv = os.path.join(OUTPUT_FOLDER, "keywords.csv")
        
        result = subprocess.run([
            sys.executable, "src/core/trend_analyzer.py",
            json_path, custom_stop_words_path, output_csv
        ], capture_output=True, text=True)
        
        if result.returncode != 0:
            raise Exception(f"Trend analysis failed: {result.stderr}")
        
        # Step 4: Process video segments
        processing_status['current_step'] = 'Processing video segments...'
        processing_status['progress'] = 50
        clips_dir = os.path.join(OUTPUT_FOLDER, "clips")
        
        result = subprocess.run([
            sys.executable, "src/core/timestamp.py",
            youtube_url, str(time_range), clips_dir,
            output_csv, json_path, str(top_n)
        ], capture_output=True, text=True)
        
        if result.returncode != 0:
            raise Exception(f"Video processing failed: {result.stderr}")
        
        # Step 5: Reframe clips to meme-style
        processing_status['current_step'] = 'Reframing video clips...'
        processing_status['progress'] = 70
        process_all_clips(clips_dir)
        
        # Step 6: Add captions to clips
        processing_status['current_step'] = 'Adding captions to clips...'
        processing_status['progress'] = 80
        result = subprocess.run([sys.executable, "src/core/captions.py"], 
                              capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"Captioning failed: {result.stderr}")
        
        # Step 7: Generate titles and metadata (only if Ollama is available)
        if check_ollama_available():
            processing_status['current_step'] = 'Generating titles and metadata...'
            processing_status['progress'] = 90
            adjusted_timestamps_csv = os.path.join(OUTPUT_FOLDER, "adjusted_timestamps.csv")
            metadata_dir = os.path.join(OUTPUT_FOLDER, "metadata")
            
            result = subprocess.run([
                sys.executable, "src/core/title_generation.py",
                adjusted_timestamps_csv, json_path, output_csv, metadata_dir
            ], capture_output=True, text=True)
            
            if result.returncode != 0:
                print(f"Title generation failed: {result.stderr}")
        else:
            processing_status['current_step'] = 'Skipping metadata generation (Ollama not available)...'
            processing_status['progress'] = 90
            # Create a simple metadata directory with basic info
            metadata_dir = os.path.join(OUTPUT_FOLDER, "metadata")
            os.makedirs(metadata_dir, exist_ok=True)
            
            # Create basic metadata files for clips
            clips_dir = os.path.join(OUTPUT_FOLDER, "clips")
            if os.path.exists(clips_dir):
                for clip_file in os.listdir(clips_dir):
                    if clip_file.endswith('.mp4'):
                        clip_name = clip_file.replace('.mp4', '')
                        metadata = {
                            "title": f"YouTube Short - {clip_name.replace('_', ' ').title()}",
                            "description": f"Generated YouTube Short from {clip_name}",
                            "tags": ["youtube shorts", "generated", clip_name.lower()]
                        }
                        
                        metadata_file = os.path.join(metadata_dir, f"{clip_name}_metadata.json")
                        with open(metadata_file, 'w') as f:
                            json.dump(metadata, f, indent=2)
        
        processing_status['current_step'] = 'Processing complete!'
        processing_status['progress'] = 100
        processing_status['message'] = 'YouTube shorts generation completed successfully!'
        
    except Exception as e:
        processing_status['error'] = str(e)
        processing_status['message'] = f'Error: {str(e)}'
    finally:
        processing_status['is_processing'] = False

def process_all_clips(folder):
    """Process all mp4 files in the given folder by applying scaling and padding filter"""
    vf_filter = (
        "scale='if(gt(a,4/3),ih*4/3,iw)':'if(lt(a,4/3),iw*3/4,ih)',"
        "pad=w=iw:h=iw*16/9:x=0:y=(oh-ih)/2:color=black"
    )
    
    mp4_files = glob.glob(os.path.join(folder, "*.mp4"))
    if not mp4_files:
        print("No mp4 files found in the folder to process for reframing.")
        return
    
    for file_path in mp4_files:
        directory, filename = os.path.split(file_path)
        name, ext = os.path.splitext(filename)
        temp_output = os.path.join(directory, f"{name}_temp{ext}")
        
        cmd = [
            "ffmpeg",
            "-i", file_path,
            "-vf", vf_filter,
            "-c:a", "copy",
            temp_output
        ]
        
        try:
            subprocess.run(cmd, capture_output=True, text=True, check=True)
            os.replace(temp_output, file_path)
        except subprocess.CalledProcessError as e:
            print(f"Error during reframing {file_path}: {e}")
        except Exception as e:
            print(f"Error replacing file {file_path}: {str(e)}")

@app.route('/')
def index():
    ollama_available = check_ollama_available()
    return render_template('index.html', ollama_available=ollama_available)

@app.route('/process', methods=['POST'])
def process_video():
    """Handle video processing request"""
    global processing_status
    
    if processing_status['is_processing']:
        return jsonify({'error': 'Already processing a video. Please wait.'}), 400
    
    data = request.get_json()
    youtube_url = data.get('youtube_url', '').strip()
    top_n = int(data.get('top_n', 5))
    time_range = int(data.get('time_range', 15))
    
    if not youtube_url:
        return jsonify({'error': 'YouTube URL is required'}), 400
    
    # Clean output directory
    clean_output_directory()
    
    # Start processing in a separate thread
    thread = threading.Thread(
        target=process_youtube_shorts,
        args=(youtube_url, top_n, time_range)
    )
    thread.daemon = True
    thread.start()
    
    return jsonify({'message': 'Processing started successfully'})

@app.route('/status')
def get_status():
    """Get current processing status"""
    return jsonify(processing_status)

@app.route('/download')
def download_results():
    """Download the generated clips as a ZIP file"""
    clips_dir = os.path.join(OUTPUT_FOLDER, "clips")
    
    if not os.path.exists(clips_dir):
        return jsonify({'error': 'No clips found. Please process a video first.'}), 404
    
    # Create a temporary ZIP file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_filename = f"youtube_shorts_{timestamp}.zip"
    zip_path = os.path.join(UPLOAD_FOLDER, zip_filename)
    
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for root, dirs, files in os.walk(clips_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, clips_dir)
                zipf.write(file_path, arcname)
    
    return send_file(zip_path, as_attachment=True, download_name=zip_filename)

@app.route('/results')
def view_results():
    """View the generated results"""
    clips_dir = os.path.join(OUTPUT_FOLDER, "clips")
    metadata_dir = os.path.join(OUTPUT_FOLDER, "metadata")
    
    clips = []
    if os.path.exists(clips_dir):
        for file in os.listdir(clips_dir):
            if file.endswith('.mp4'):
                clips.append({
                    'filename': file,
                    'path': os.path.join(clips_dir, file)
                })
    
    metadata_files = []
    if os.path.exists(metadata_dir):
        for file in os.listdir(metadata_dir):
            if file.endswith('.json'):
                metadata_files.append({
                    'filename': file,
                    'path': os.path.join(metadata_dir, file)
                })
    
    return render_template('results.html', clips=clips, metadata_files=metadata_files)

@app.route('/clip/<filename>')
def serve_clip(filename):
    """Serve a specific clip file from the output directory with HTTP Range support."""
    clips_dir = os.path.join(OUTPUT_FOLDER, 'clips')
    file_path = os.path.join(clips_dir, filename)
    if not os.path.isfile(file_path):
        abort(404)
    # Use send_from_directory to serve and support Range requests
    return send_from_directory(
        clips_dir,
        filename,
        mimetype='video/mp4',
        conditional=True
    )

@app.route('/metadata/<filename>')
def serve_metadata(filename):
    metadata_dir = os.path.join(OUTPUT_FOLDER, 'metadata')
    file_path = os.path.join(metadata_dir, filename)
    if not os.path.isfile(file_path):
        abort(404)
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return jsonify(data)

@app.route('/demo')
def demo():
    """Demo page showing the interface without requiring Ollama"""
    return render_template('demo.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 