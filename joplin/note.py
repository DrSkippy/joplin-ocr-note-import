import os
import shutil
from datetime import datetime
from pathlib import Path

from common.logging_config import get_logger

logger = get_logger(__name__)


class JoplinNote:
    """Creates a Joplin-compatible markdown note from an image and extracted text."""

    def __init__(self, image_file_path, extracted_text):
        """
        Initialize a JoplinNote.

        Args:
            image_file_path: Path to the source image file
            extracted_text: Text extracted from the image via OCR
        """
        self.image_file_path = Path(image_file_path)
        self.extracted_text = extracted_text
        self.original_filename = self.image_file_path.name
        self.image_filename = self._sanitize_filename(self.original_filename)
        self.note_title = self._sanitize_filename(self.image_file_path.stem)  # filename without extension

    def _sanitize_filename(self, filename):
        """
        Sanitize filename by replacing spaces and problematic characters.

        Args:
            filename: Original filename

        Returns:
            Sanitized filename safe for Joplin import
        """
        # Replace spaces with underscores
        sanitized = filename.replace(' ', '_')
        # Replace other problematic characters
        sanitized = sanitized.replace('(', '').replace(')', '')
        sanitized = sanitized.replace('[', '').replace(']', '')
        sanitized = sanitized.replace('{', '').replace('}', '')
        # Remove multiple consecutive underscores
        while '__' in sanitized:
            sanitized = sanitized.replace('__', '_')
        logger.debug(f"Sanitized filename: '{filename}' -> '{sanitized}'")
        return sanitized

    def _clean_text(self, text):
        """Remove consecutive blank lines, keeping at most one blank line between paragraphs."""
        lines = text.split('\n')
        cleaned_lines = []
        prev_blank = False

        for line in lines:
            is_blank = line.strip() == ''
            if is_blank:
                if not prev_blank:
                    cleaned_lines.append(line)
                prev_blank = True
            else:
                cleaned_lines.append(line)
                prev_blank = False

        return '\n'.join(cleaned_lines)

    def _generate_markdown(self, image_link):
        """Generate the markdown content for the note."""
        date_str = datetime.now().strftime('%Y-%m-%d')
        title = f"# {date_str} {self.note_title}"

        cleaned_text = self._clean_text(self.extracted_text)

        markdown_content = f"{title}\n\n{cleaned_text}\n\n![{self.image_filename}]({image_link})\n"

        return markdown_content

    def save(self, output_path):
        """
        Save the note as a markdown file and move the image to the output directory.
        Filenames are sanitized to remove spaces and problematic characters for Joplin import.

        Args:
            output_path: Directory where the markdown file and image should be saved

        Returns:
            Path to the created markdown file
        """
        logger.debug(f"Saving Joplin note for image: {self.original_filename}")
        output_dir = Path(output_path)
        output_dir.mkdir(parents=True, exist_ok=True)

        # Move image to output directory with sanitized filename
        image_dest = output_dir / self.image_filename
        logger.debug(f"Copying image from {self.image_file_path} to {image_dest}")
        shutil.copy(str(self.image_file_path), str(image_dest))

        # Create markdown file
        markdown_filename = f"{self.note_title}.md"
        markdown_path = output_dir / markdown_filename

        # Generate markdown content with relative image link
        markdown_content = self._generate_markdown(self.image_filename)

        # Write markdown file
        with open(markdown_path, 'w', encoding='utf-8') as f:
            f.write(markdown_content)

        logger.info(f"Joplin note created: {markdown_path}")
        return markdown_path
