import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from ocr.process import process_image_path
from joplin.note import JoplinNote
from common.logging_config import get_logger

logger = get_logger(__name__)

class ImageHandler(FileSystemEventHandler):
    def __init__(self, output_folder, joplin_path=None):
        """
        Initialize the handler with the output folder path.

        Args:
            output_folder: Directory where text files will be saved
            joplin_path: Optional directory where Joplin markdown notes will be saved
        """
        super().__init__()
        self.output_folder = output_folder
        self.joplin_path = joplin_path

    def process(self, event):
        """Processes newly created image files."""
        if event.is_directory:
            return
        source_path = str(event.src_path)
        extracted_text = process_image_path(source_path)

        if self.joplin_path:
            # Create Joplin markdown note
            logger.debug(f"Creating Joplin note for: {source_path}")
            note = JoplinNote(source_path, extracted_text)
            markdown_path = note.save(self.joplin_path)
            logger.info(f"Joplin note saved to {markdown_path}")
        if self.output_folder:
            # Save the extracted text to a .txt file in the output folder
            image_name = os.path.basename(event.src_path)
            text_filename = os.path.splitext(image_name)[0] + ".txt"
            output_path = os.path.join(self.output_folder, text_filename)

            with open(output_path, "w") as f:
                f.write(extracted_text)
            logger.info(f"Extracted text saved to {output_path}")

    def on_created(self, event):
        self.process(event)

if __name__ == "__main__":
    # Default paths for standalone execution
    HOT_FOLDER = "/home/scott/ownCloud/tesseract-hot-folder"
    OUTPUT_FOLDER = "/home/scott/Downloads"

    os.makedirs(HOT_FOLDER, exist_ok=True)
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    event_handler = ImageHandler(OUTPUT_FOLDER)
    observer = Observer()
    observer.schedule(event_handler, HOT_FOLDER, recursive=False)
    observer.start()
    logger.info(f"Monitoring hot folder: {HOT_FOLDER} (Press Ctrl+C to stop)")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

