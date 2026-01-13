#!/usr/bin/env python3
"""Test script to process an image in text-only mode."""
import sys
sys.path.insert(0, '/home/scott/Working/tesseract-hot-folder-tool')

from common.logging_config import setup_logging
from ocr.process import process_image_path
from watcher.directory_watcher import ImageHandler
from unittest.mock import Mock

# Set up logging
setup_logging()

# Create a mock event
event = Mock()
event.is_directory = False
event.src_path = "test/watch/sample_invoice2.png"

# Create handler without joplin_path
print("Testing text-only mode (no Joplin)...")
handler = ImageHandler(output_folder="test/output", joplin_path=None)
handler.process(event)
print("\nDone! Check test/output/ for the text file.")
