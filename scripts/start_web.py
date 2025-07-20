#!/usr/bin/env python3
"""
YouTube Shorts Generator Web Interface Startup Script
This script checks dependencies and starts the Flask web application.
"""

import os
import sys
import subprocess
import importlib.util

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Error: Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True

def check_dependencies():
    """Check if required Python packages are installed"""
    required_packages = [
        'flask', 'flask_cors', 'moviepy', 'numpy', 'opencv_python',
        'pandas', 'PIL', 'pymongo', 'pytrends', 'spacy',
        'youtube_transcript_api', 'yt_dlp'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'PIL':
                import PIL
            elif package == 'opencv_python':
                import cv2
            else:
                importlib.import_module(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - Missing")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n❌ Missing packages: {', '.join(missing_packages)}")
        print("Please install missing packages with: pip install -r requirements.txt")
        return False
    
    return True

def check_spacy_model():
    """Check if spaCy English model is installed"""
    try:
        import spacy
        nlp = spacy.load("en_core_web_sm")
        print("✅ spaCy English model")
        return True
    except OSError:
        print("❌ spaCy English model not found")
        print("Please install with: python -m spacy download en_core_web_sm")
        return False

def check_ffmpeg():
    """Check if FFmpeg is available"""
    try:
        result = subprocess.run(['ffmpeg', '-version'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ FFmpeg")
            return True
        else:
            print("❌ FFmpeg not found")
            return False
    except FileNotFoundError:
        print("❌ FFmpeg not found in PATH")
        print("Please install FFmpeg:")
        print("  Windows: Download from https://ffmpeg.org/download.html")
        print("  macOS: brew install ffmpeg")
        print("  Linux: sudo apt install ffmpeg")
        return False

def check_ollama():
    """Check if Ollama is running and has the required model"""
    try:
        # Check if Ollama service is running
        result = subprocess.run(['curl', '-s', 'http://localhost:11434/api/tags'], 
                              capture_output=True, text=True, timeout=5)
        
        if result.returncode == 0:
            print("✅ Ollama service is running")
            
            # Check if qwen2.5:3b model is available
            if 'qwen2.5:3b' in result.stdout:
                print("✅ Qwen2.5:3B model available")
                return True
            else:
                print("⚠️  Qwen2.5:3B model not found")
                print("Please install with: ollama pull qwen2.5:3b")
                return False
        else:
            print("❌ Ollama service not running")
            print("Please start Ollama with: ollama serve")
            return False
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print("❌ Ollama service not running")
        print("Please start Ollama with: ollama serve")
        return False

def create_directories():
    """Create necessary directories"""
    directories = ['uploads', '.output', 'templates']
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"✅ Created directory: {directory}")
        else:
            print(f"✅ Directory exists: {directory}")

def main():
    """Main startup function"""
    print("🚀 YouTube Shorts Generator Web Interface")
    print("=" * 50)
    
    # Check all requirements
    checks = [
        ("Python Version", check_python_version),
        ("Python Dependencies", check_dependencies),
        ("spaCy Model", check_spacy_model),
        ("FFmpeg", check_ffmpeg),
        ("Ollama", check_ollama),
    ]
    
    all_passed = True
    for name, check_func in checks:
        print(f"\n🔍 Checking {name}...")
        if not check_func():
            all_passed = False
    
    print(f"\n📁 Creating directories...")
    create_directories()
    
    if not all_passed:
        print("\n❌ Some requirements are not met. Please fix the issues above.")
        print("\n💡 Quick fixes:")
        print("1. Install missing packages: pip install -r requirements.txt")
        print("2. Install spaCy model: python -m spacy download en_core_web_sm")
        print("3. Install FFmpeg (see instructions above)")
        print("4. Install Ollama: https://ollama.ai")
        print("5. Start Ollama: ollama serve")
        print("6. Install model: ollama pull qwen2.5:3b")
        return False
    
    print("\n✅ All requirements met!")
    print("\n🌐 Starting web interface...")
    print("📱 Open your browser to: http://localhost:5000")
    print("⏹️  Press Ctrl+C to stop the server")
    print("=" * 50)
    
    # Start the Flask application
    try:
        from app import app
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 