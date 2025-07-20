#!/usr/bin/env python3
"""
YouTube Shorts Generator - Main Entry Point
This is the main entry point for the YouTube Shorts Generator application.
"""

import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from web.app import app

if __name__ == '__main__':
    print("🚀 Starting YouTube Shorts Generator...")
    print("📱 Open your browser to: http://localhost:5000")
    print("⏹️  Press Ctrl+C to stop the server")
    print("=" * 50)
    
    app.run(debug=True, host='0.0.0.0', port=5000) 