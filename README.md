# YouTube Shorts Generator

Transform any YouTube video into engaging short-form content automatically with this web-based tool.

## 🚀 Quick Start

### Option 1: Simple Mode (Recommended)
```bash
python main.py
```

### Option 2: Full Features (Requires Ollama)
```bash
python scripts/start_web.py
```

### Option 3: Command Line Interface
```bash
python scripts/master.py
```

## 📁 Project Structure

```
YoutubeShortsGen/
├── main.py                 # Main entry point
├── requirements.txt        # Python dependencies
├── README.md              # This file
│
├── src/                   # Source code
│   ├── core/             # Core processing modules
│   │   ├── caption_extractor.py    # YouTube caption extraction
│   │   ├── trend_analyzer.py       # Keyword trend analysis
│   │   ├── timestamp.py            # Video clip creation
│   │   ├── captions.py             # Caption overlay
│   │   ├── title_generation.py     # Metadata generation
│   │   └── adjust_aspect.py        # Aspect ratio conversion
│   │
│   ├── web/              # Web interface
│   │   ├── app.py        # Flask web application
│   │   ├── templates/    # HTML templates
│   │   └── static/       # Static files (CSS, JS, images)
│   │
│   └── utils/            # Utility functions
│
├── scripts/              # Startup and utility scripts
│   ├── start_simple.py   # Simple startup (no Ollama required)
│   ├── start_web.py      # Full startup with Ollama
│   └── master.py         # Command-line interface
│
├── config/               # Configuration files
│   └── custom_stop_words.txt
│
├── uploads/              # Temporary file storage
├── .output/              # Generated clips and metadata
└── __pycache__/          # Python cache (auto-generated)
```

## 🎬 Features

- **Automatic Video Processing**: Extract captions, analyze trends, and create clips
- **Keyword Analysis**: Identify trending topics and important moments
- **Smart Clipping**: Create video segments around key moments
- **Aspect Ratio Conversion**: Automatically reframe videos to 9:16 for YouTube Shorts
- **Caption Overlay**: Add animated captions to video clips
- **SEO Optimization**: Generate titles, descriptions, and tags for each clip
- **Batch Download**: Download all generated clips as a ZIP file
- **Beautiful Web Interface**: Modern, responsive design with real-time progress

## 📋 Prerequisites

### Required
- **Python 3.8+**
- **FFmpeg** (for video processing)
- **spaCy English model**: `python -m spacy download en_core_web_sm`

### Optional (for advanced features)
- **Ollama** with Qwen2.5:3B model (for AI-powered metadata generation)

## 🛠️ Installation

1. **Clone or download the project**

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Install spaCy language model**:
   ```bash
   python -m spacy download en_core_web_sm
   ```

4. **Install FFmpeg**:
   - **Windows**: Download from https://ffmpeg.org/download.html
   - **macOS**: `brew install ffmpeg`
   - **Linux**: `sudo apt install ffmpeg`

5. **Optional: Install Ollama for advanced features**:
   ```bash
   # Install Ollama from https://ollama.ai
   ollama pull qwen2.5:3b
   ollama serve
   ```

## 🌐 Usage

### Web Interface (Recommended)

1. **Start the application**:
   ```bash
   python main.py
   ```

2. **Open your browser** to `http://localhost:5000`

3. **Enter a YouTube URL** and configure settings:
   - **Top Keywords**: Number of trending keywords (3-10)
   - **Time Range**: Duration of clips around keywords (10-30 seconds)

4. **Click "Generate Shorts"** and monitor real-time progress

5. **View and download results** when processing is complete

### Command Line Interface

```bash
python scripts/master.py
```

Follow the interactive prompts to process videos.

## 🔧 Configuration

### Custom Stop Words
Edit `config/custom_stop_words.txt` to customize keyword filtering.

### Environment Variables
- `FLASK_ENV`: Set to 'development' for debug mode
- `PORT`: Custom port number (default: 5000)
- `HOST`: Custom host address (default: 0.0.0.0)

## 📊 Processing Steps

The tool automatically performs these steps:

1. **Caption Extraction**: Downloads and processes video captions
2. **Trend Analysis**: Analyzes keywords and their trending popularity
3. **Video Processing**: Downloads the YouTube video
4. **Clip Creation**: Creates video segments around key moments
5. **Aspect Ratio Conversion**: Reframes clips to 9:16 ratio
6. **Caption Overlay**: Adds animated captions to clips
7. **Metadata Generation**: Creates SEO-optimized titles and descriptions

## 🎯 Results

After processing, you can:

- **View clips** directly in the web interface
- **Download individual clips** or all clips as a ZIP file
- **View generated metadata** including titles, descriptions, and tags
- **Use the metadata** for uploading to YouTube or other platforms

## 🚨 Troubleshooting

### Common Issues

1. **FFmpeg not found**:
   - Install FFmpeg and ensure it's in your system PATH

2. **Ollama connection error**:
   - Ensure Ollama is running: `ollama serve`
   - Check if the model is installed: `ollama list`
   - Install the model: `ollama pull qwen2.5:3b`

3. **spaCy model not found**:
   - Install the English model: `python -m spacy download en_core_web_sm`

4. **Video download fails**:
   - Check your internet connection
   - Ensure the YouTube URL is valid and accessible

5. **Processing takes too long**:
   - Reduce the number of keywords processed
   - Use shorter time ranges
   - Check your system resources

### Performance Tips

- **Faster processing**: Use fewer keywords and shorter time ranges
- **Better quality**: Use longer time ranges for more context
- **Storage**: Ensure sufficient disk space for video processing
- **Memory**: Close other applications during processing

## 🔄 API Endpoints

- `GET /` - Main interface
- `POST /process` - Start video processing
- `GET /status` - Get processing status
- `GET /results` - View generated results
- `GET /download` - Download all clips as ZIP
- `GET /clip/<filename>` - Download specific clip
- `GET /metadata/<filename>` - Get metadata for clip

## 🤝 Contributing

Feel free to contribute by:

1. Reporting bugs
2. Suggesting new features
3. Improving the UI/UX
4. Optimizing performance
5. Adding new video processing capabilities

## 📄 License

This project is open source and available under the MIT License.

## 🆘 Support

For support and questions:

1. Check the troubleshooting section above
2. Review the code comments for implementation details
3. Open an issue on the project repository

---

**Happy YouTube Shorts Generation! 🎬✨** 