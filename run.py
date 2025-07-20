#!/usr/bin/env python3
"""
YouTube Shorts Generator - Simple Runner
This script starts the web interface with the new organized structure.
"""

import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from web.app import app
    
    print("🚀 YouTube Shorts Generator")
    print("=" * 40)
    print("📱 Open your browser to: http://localhost:5000")
    print("⏹️  Press Ctrl+C to stop the server")
    print("=" * 40)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
    
except ImportError as e:
    print(f"❌ Error importing modules: {e}")
    print("💡 Make sure all dependencies are installed:")
    print("   pip install -r requirements.txt")
    print("   python -m spacy download en_core_web_sm")
except Exception as e:
    print(f"❌ Error starting server: {e}")
    print("💡 Check that all files are in the correct locations") 