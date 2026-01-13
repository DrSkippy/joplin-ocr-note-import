#!/usr/bin/env python3
"""Test script to verify filename sanitization for Joplin import."""
import sys
sys.path.insert(0, '/home/scott/Working/tesseract-hot-folder-tool')

from common.logging_config import setup_logging
from ocr.process import process_image_path
from joplin.note import JoplinNote

# Set up logging
setup_logging()

# Process the image with spaces in filename
image_path = "test/watch/Invoice (Jan 2026) Receipt.png"
print(f"Processing image: {image_path}")
print()

extracted_text = process_image_path(image_path)

print("=== Extracted Text ===")
print(extracted_text)
print("======================\n")

# Create a Joplin note
print("Creating Joplin note with sanitized filename...")
note = JoplinNote(image_path, extracted_text)

print(f"Original filename: '{note.original_filename}'")
print(f"Sanitized filename: '{note.image_filename}'")
print(f"Sanitized note title: '{note.note_title}'")
print()

markdown_path = note.save("test/joplin")
print(f"\nJoplin note saved to: {markdown_path}")
print("\n=== Verifying files in joplin directory ===")
