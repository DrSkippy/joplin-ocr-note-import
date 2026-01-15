import os
import pytesseract
from PIL import Image
from pdf2image import convert_from_path

from common.logging_config import get_logger

logger = get_logger(__name__)


def process_image_path(src_path):
    logger.debug(f"Processing image: {src_path}")
    extracted_text = ""
    if src_path.lower().endswith(('.pdf')):
        try:
            # Convert PDF pages to a list of images
            pages = convert_from_path(src_path, 300)  # 300 DPI is often a good resolution for OCR
            # Iterate through each image and perform OCR
            for page_num, img in enumerate(pages):
                logger.info(f"Processing page {page_num + 1}...")
                # Run OCR on the image
                text = pytesseract.image_to_string(img)
                extracted_text += text + "\n"
        except Exception as e:
            logger.error(f"Error processing image {src_path}: {e}")
    elif src_path.lower().endswith(('.png', '.jpg', '.jpeg', '.tif')):
        logger.info(f"Detected new image: {src_path}")
        try:
            # Open and preprocess the image (optional but improves accuracy)
            image = Image.open(src_path).convert('L')
            image = image.resize([3 * _ for _ in image.size], Image.Resampling.BICUBIC)
            # Extract text
            extracted_text = pytesseract.image_to_string(image)
        except Exception as e:
            logger.error(f"Error processing image {src_path}: {e}")
    return extracted_text
