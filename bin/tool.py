import time
import os
import argparse
import yaml
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from watcher.directory_watcher import ImageHandler
from common.logging_config import setup_logging, get_logger

logger = get_logger(__name__)

def load_config(config_path="config.yaml"):
    """Load configuration from YAML file."""
    config_file = Path(config_path)
    if config_file.exists():
        with open(config_file, 'r') as f:
            return yaml.safe_load(f)
    return {}

if __name__ == "__main__":
    # Set up logging
    setup_logging()

    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Tesseract Hot Folder Tool - Monitor a folder and OCR images')
    parser.add_argument('--watch-folder', type=str, help='Directory to watch for new images')
    parser.add_argument('--output-path', type=str, help='Directory where OCR text output will be saved')
    parser.add_argument('--joplin-path', type=str, help='Directory where Joplin markdown notes will be saved')
    parser.add_argument('--config', type=str, default='config.yaml', help='Path to config file (default: config.yaml)')
    args = parser.parse_args()

    # Load config from YAML
    config = load_config(args.config)

    # Command line arguments override config file
    watch_folder = args.watch_folder or config.get('watch_folder', '/home/scott/ownCloud/tesseract-hot-folder')
    output_path = args.output_path or config.get('output_path', '/home/scott/Downloads')
    joplin_path = args.joplin_path or config.get('joplin_path')

    # Ensure directories exist
    os.makedirs(watch_folder, exist_ok=True)
    os.makedirs(output_path, exist_ok=True)
    if joplin_path:
        os.makedirs(joplin_path, exist_ok=True)

    # Set up observer
    event_handler = ImageHandler(output_path, joplin_path)
    observer = Observer()
    observer.schedule(event_handler, watch_folder, recursive=False)
    observer.start()
    logger.info(f"Monitoring hot folder: {watch_folder}")
    logger.info(f"Output directory: {output_path}")
    if joplin_path:
        logger.info(f"Joplin notes directory: {joplin_path}")
    logger.info("Press Ctrl+C to stop")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

