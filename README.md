# YouTube Shorts Generator

This repository provides a web-based tool for transforming YouTube videos into short-form content suitable for platforms such as YouTube Shorts. The application automates caption extraction, keyword analysis, video clipping, aspect ratio conversion, caption overlay, and metadata generation.

## Quick Start

### Simple Mode
Run the following command to start the application in simple mode:

    python main.py

### Full Feature Mode (Requires Ollama)
To enable advanced metadata generation, use:

    python scripts/start_web.py

### Command Line Interface
For command-line processing, use:

    python scripts/master.py

## Project Structure

    YoutubeShortsGen/
    ├── main.py                 Main entry point
    ├── requirements.txt        Python dependencies
    ├── README.md               Project documentation
    ├── src/                    Source code
    │   ├── core/               Core processing modules
    │   ├── web/                Web interface (Flask)
    │   └── utils/              Utility functions
    ├── scripts/                Startup and utility scripts
    ├── config/                 Configuration files
    ├── uploads/                Temporary file storage
    ├── .output/                Generated clips and metadata
    └── __pycache__/            Python cache

## Features

- Automatic extraction of captions and keyword trends
- Creation of video segments around key moments
- Aspect ratio conversion to 9:16 for short-form platforms
- Caption overlay on generated clips
- Metadata generation for SEO optimization (titles, descriptions, tags)
- Batch download of generated clips
- Web interface with real-time progress display

## Prerequisites

- Python 3.8 or higher
- FFmpeg (for video processing)
- spaCy English model: `python -m spacy download en_core_web_sm`
- (Optional) Ollama with Qwen2.5:3B model for advanced metadata features

## Installation

1. Clone the repository.
2. Install Python dependencies:

       pip install -r requirements.txt

3. Install the spaCy language model:

       python -m spacy download en_core_web_sm

4. Install FFmpeg:
   - Windows: Download from https://ffmpeg.org/download.html
   - macOS: `brew install ffmpeg`
   - Linux: `sudo apt install ffmpeg`

5. (Optional) Install Ollama and the Qwen2.5:3B model for advanced features.

## Usage

### Web Interface

1. Start the application:

       python main.py

2. Open a browser and navigate to `http://localhost:5000`.
3. Enter a YouTube URL and configure the number of keywords and clip duration.
4. Click "Generate Shorts" and monitor progress.
5. View and download results upon completion.

### Command Line Interface

Run:

    python scripts/master.py

Follow the prompts to process videos.

## Configuration

- Edit `config/custom_stop_words.txt` to customize keyword filtering.
- Environment variables:
  - `FLASK_ENV`: Set to 'development' for debug mode
  - `PORT`: Custom port number (default: 5000)
  - `HOST`: Custom host address (default: 0.0.0.0)

## Processing Steps

1. Caption extraction
2. Keyword trend analysis
3. Video download and processing
4. Clip creation
5. Aspect ratio conversion
6. Caption overlay
7. Metadata generation

## Results

- View generated clips in the web interface
- Download individual clips or all clips as a ZIP archive
- View and use generated metadata for uploading to video platforms

## Troubleshooting

- Ensure FFmpeg is installed and available in the system PATH
- For Ollama errors, verify the service is running and the model is installed
- If the spaCy model is missing, run `python -m spacy download en_core_web_sm`
- For video download issues, check the validity and accessibility of the YouTube URL
- If processing is slow, reduce the number of keywords or use shorter time ranges

## API Endpoints

- `GET /` : Main interface
- `POST /process` : Start video processing
- `GET /status` : Get processing status
- `GET /results` : View generated results
- `GET /download` : Download all clips as a ZIP archive
- `GET /clip/<filename>` : Download a specific clip
- `GET /metadata/<filename>` : Retrieve metadata for a clip

## Contributing

Contributions are welcome. You may report bugs, suggest features, improve the user interface, optimize performance, or add new processing capabilities.

## License

This project is licensed under the MIT License.

## Support

For support, consult the troubleshooting section, review code comments, or open an issue in the repository.