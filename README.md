# Tesseract Hot Folder Tool

A Python-based hot folder monitoring tool that automatically performs OCR (Optical Character Recognition) on images and PDFs using Tesseract. The tool watches a specified directory for new image files, extracts text from them, and can create either plain text files or Joplin-compatible markdown notes with embedded images.

## Features

- **Automatic File Monitoring**: Watches a directory for new image files in real-time
- **OCR Processing**: Extracts text from images and PDFs using Tesseract OCR
- **Multiple Output Formats**:
  - Plain text files (.txt)
  - Joplin-compatible markdown notes with embedded images
- **Flexible Configuration**: Configure via YAML file or command-line arguments
- **Filename Sanitization**: Automatically removes spaces and special characters from filenames for Joplin compatibility
- **Comprehensive Logging**: Detailed logs with timestamps, module names, function names, and line numbers
- **Supported File Types**: PNG, JPG, JPEG, TIF, and PDF files
- **Image Preprocessing**: Automatic image enhancement for better OCR accuracy

## System Requirements

- Python 3.10 or higher
- Tesseract OCR installed on your system
- Poetry (for dependency management)

### Installing Tesseract

**Ubuntu/Debian:**
```bash
sudo apt-get install tesseract-ocr
```

**macOS:**
```bash
brew install tesseract
```

**Other systems:** Visit the [Tesseract documentation](https://github.com/tesseract-ocr/tesseract)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd tesseract-hot-folder-tool
```

2. Install dependencies using Poetry:
```bash
poetry install
```

## Configuration

### Using config.yaml

Create or edit `config.yaml` in the project root:

```yaml
# Tesseract Hot Folder Tool Configuration

# Directory to watch for new images
watch_folder: "/path/to/watch/folder"

# Directory where OCR text output will be saved
output_path: "/path/to/output"

# Optional: Directory where Joplin-compatible markdown notes will be saved
# Set to a path to enable Joplin mode, or leave as null for text-only mode
joplin_path: null  # or "/path/to/joplin/notes"
```

### Command-Line Arguments

Command-line arguments override configuration file settings:

```bash
poetry run python bin/tool.py [OPTIONS]
```

**Options:**
- `--watch-folder PATH`: Directory to watch for new images
- `--output-path PATH`: Directory where OCR text output will be saved
- `--joplin-path PATH`: Directory where Joplin markdown notes will be saved (optional)
- `--config PATH`: Path to config file (default: config.yaml)

## Usage

### Basic Usage (Text-Only Mode)

Monitor a folder and create text files from OCR:

```bash
poetry run python bin/tool.py --watch-folder /path/to/watch --output-path /path/to/output
```

When an image is added to the watch folder:
1. OCR extracts text from the image
2. A `.txt` file is created in the output directory
3. The image remains in the watch folder

### Joplin Mode

Create Joplin-compatible markdown notes with embedded images:

```bash
poetry run python bin/tool.py --watch-folder /path/to/watch --joplin-path /path/to/joplin
```

When an image is added to the watch folder:
1. OCR extracts text from the image
2. A `.md` markdown file is created in the joplin directory
3. The image is moved to the joplin directory with a sanitized filename
4. The markdown note includes the extracted text and an embedded image link

### Using Config File

```bash
poetry run python bin/tool.py
```

This uses settings from `config.yaml` in the project directory.

### Using Custom Config File

```bash
poetry run python bin/tool.py --config /path/to/custom-config.yaml
```

## Output Formats

### Text-Only Mode

Creates a plain text file with extracted text:

```
Invoice #12345
Date: 2026-01-13

Item: Coffee Beans
Quantity: 2

Price: $25.99
Total: $51.98

Thank you for your business!
```

### Joplin Mode

Creates a markdown note with this format:

```markdown
# 2026-01-13 filename

[Extracted text content]

![filename.png](filename.png)
```

**Features:**
- Title includes current date and filename
- Consecutive blank lines reduced to maximum of 1
- Embedded image with relative link
- Filenames sanitized (spaces → underscores, special characters removed)

## How It Works

1. **File Monitoring**: The tool uses `watchdog` to monitor the specified directory for new files
2. **File Detection**: When a new image or PDF is created in the watch folder, it triggers processing
3. **OCR Processing**:
   - Images are preprocessed (converted to grayscale, upscaled) for better accuracy
   - PDFs are converted to images at 300 DPI
   - Tesseract extracts text from each page/image
4. **Output Generation**:
   - **Text mode**: Creates a `.txt` file in the output directory
   - **Joplin mode**: Creates a `.md` file and moves the image to the joplin directory
5. **Filename Sanitization**: Spaces and special characters are removed from filenames in Joplin mode

## Logging

The tool provides comprehensive logging with the following format:

```
YYYY-MM-DD HH:MM:SS - module.name - function:line - LEVEL - message
```

**Example logs:**
```
2026-01-13 14:11:43 - __main__ - <module>:53 - INFO - Monitoring hot folder: /path/to/watch
2026-01-13 14:11:55 - ocr.process - process_image_path:27 - INFO - Detected new image: invoice.png
2026-01-13 14:11:55 - joplin.note - save:110 - INFO - Joplin note created: invoice.md
```

## Project Structure

```
tesseract-hot-folder-tool/
├── bin/
│   └── tool.py                 # Main entry point
├── common/
│   ├── __init__.py
│   └── logging_config.py       # Centralized logging configuration
├── joplin/
│   ├── __init__.py
│   └── note.py                 # JoplinNote class for markdown generation
├── ocr/
│   ├── __init__.py
│   └── process.py              # OCR processing functions
├── watcher/
│   ├── __init__.py
│   └── directory_watcher.py    # File system monitoring
├── test/                       # Test scripts and sample files
├── config.yaml                 # Configuration file
├── pyproject.toml             # Project dependencies
└── README.md                  # This file
```

## Development and Testing

### Running Tests

Test the OCR processing with a sample image:

```bash
poetry run python test/create_test_image.py
poetry run python test/test_process.py
```

Test filename sanitization:

```bash
poetry run python test/test_sanitize.py
```

### Creating Test Images

The project includes a test image generator:

```bash
poetry run python test/create_test_image.py
```

This creates a sample invoice image with text for testing OCR accuracy.

## Dependencies

- **pytesseract** (>=0.3.13): Python wrapper for Tesseract OCR
- **Pillow** (>=12.1.0): Image processing library
- **watchdog** (>=6.0.0): File system monitoring
- **pdf2image** (>=1.17.0): PDF to image conversion
- **pyyaml** (>=6.0.3): YAML configuration file parsing

## Tips for Best Results

1. **Image Quality**: Higher resolution images (300 DPI+) produce better OCR results
2. **File Formats**: PNG and TIFF generally work better than JPEG
3. **Text Clarity**: Clear, high-contrast text is easier to recognize
4. **Language Support**: Install additional Tesseract language packs if needed
5. **Preprocessing**: The tool automatically preprocesses images, but manual cleanup may improve results for poor quality images

## Troubleshooting

**"No module named 'pytesseract'"**
- Run `poetry install` to install dependencies

**"Tesseract not found"**
- Install Tesseract OCR on your system (see System Requirements)

**Poor OCR accuracy**
- Check image quality and resolution
- Ensure text is clear and high-contrast
- Consider manually preprocessing images

**Files not being detected**
- Ensure the watch folder path is correct
- Check file permissions
- Verify file extensions are supported

## Author

Scott Hendrickson (scott@drskippy.net)

## Version

0.1.0

## License

See project license file for details.
