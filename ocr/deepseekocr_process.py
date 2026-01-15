import os
import yaml
from pathlib import Path
from PIL import Image
from pdf2image import convert_from_path
from ollama import Client
import sys
import base64
from io import BytesIO

from common.logging_config import get_logger

logger = get_logger(__name__)

def load_config(config_path="config.yaml"):
    """Load configuration from YAML file."""
    config_file = Path(config_path)
    if config_file.exists():
        with open(config_file, 'r') as f:
            return yaml.safe_load(f)
    return {}

# Load configuration
config = load_config()
deepseek_config = config.get('deepseek_ocr', {})

# Define the model to use
MODEL = deepseek_config.get('model', 'deepseek-ocr:latest')
HOST = deepseek_config.get('host', 'http://localhost:11434')
PROMPT = "Extract all text from this image and convert the document to markdown."

def process_image_path(src_path):
    logger.debug(f"Processing image: {src_path}")
    client = Client(host=HOST)
    extracted_text = ""
    if src_path.lower().endswith(('.pdf')):
        try:
            # Convert PDF pages to a list of images
            pages = convert_from_path(src_path, 300)  # 300 DPI is often a good resolution for OCR
            # Iterate through each image and perform OCR
            for page_num, img in enumerate(pages):
                logger.info(f"Processing page {page_num + 1}...")
                # Run OCR on the image
                im_file = BytesIO()
                img.save(im_file, format='JPEG')
                im_bytes = im_file.getvalue()
                encoded_image = base64.b64encode(im_bytes).decode('utf-8')
                # Send request to Ollama API
                response = client.chat(
                    model=MODEL,
                    messages=[
                        {
                            'role': 'user',
                            'content': PROMPT,
                            'images': [encoded_image]  # Pass the encoded image here
                        }
                    ]
                )
                text = response['message']['content']
                extracted_text += text + "\n"
        except Exception as e:
            logger.error(f"Error processing image {src_path}: {e}")
    elif src_path.lower().endswith(('.png', '.jpg', '.jpeg', '.tif')):
        logger.info(f"Detected new image: {src_path}")
        try:
            # Open and encode the image to base64
            with open(src_path, "rb") as f:
                encoded_image = base64.b64encode(f.read()).decode('utf-8')
            # Send request to Ollama API
            response = client.chat(
                model=MODEL,
                messages=[
                    {
                        'role': 'user',
                        'content': PROMPT,
                        'images': [encoded_image]  # Pass the encoded image here
                    }
                ]
            )
            extracted_text = response['message']['content']
        except FileNotFoundError:
            logger.error(f"Error: Image file not found at {src_path}")
        except Exception as e:
            logger.error(f"An error occurred: {e}")
    return extracted_text