#!/usr/bin/env python3
"""Test script to process a sample image."""
import sys
sys.path.insert(0, '/home/scott/Working/tesseract-hot-folder-tool')

from common.logging_config import setup_logging
from ocr.tesseract_process import process_image_path
from joplin.note import JoplinNote

# Set up logging
setup_logging()

# Process the image
print("Processing test/watch/sample_invoice.png...")
extracted_text = process_image_path("test/watch/sample_invoice.png")

print("\n=== Extracted Text ===")
print(extracted_text)
print("======================\n")

# Create a Joplin note
print("Creating Joplin note...")
note = JoplinNote("test/watch/sample_invoice.png", extracted_text)
markdown_path = note.save("test/joplin")
print(f"Joplin note saved to: {markdown_path}")
