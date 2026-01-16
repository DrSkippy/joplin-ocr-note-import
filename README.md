# Joplin OCR Note Import Tool

A Python-based hot folder monitoring tool that automatically performs OCR (Optical Character Recognition) on images and PDFs using either Tesseract or DeepSeek OCR. The tool watches a specified directory for new image files, extracts text from them, and can create either plain text files or Joplin-compatible markdown notes with embedded images.

## Features

- **Automatic File Monitoring**: Watches a directory for new image files in real-time
- **Multiple OCR Processors**: Choose between Tesseract OCR (local, open-source) or DeepSeek OCR (AI-powered via Ollama)
- **Multiple Output Formats**:
  - Plain text files (.txt)
  - Joplin-compatible markdown notes with embedded images
- **OCR Processor Selection**: Choose between:
  - **Tesseract**: Traditional OCR engine, fast and reliable for standard documents
  - **DeepSeek**: AI-powered OCR via Ollama for complex layouts and better accuracy
- **Flexible Configuration**: Configure via YAML file or command-line arguments
- **Filename Sanitization**: Automatically removes spaces and special characters from filenames for Joplin compatibility
- **Comprehensive Logging**: Detailed logs with timestamps, module names, function names, and line numbers
- **Supported File Types**: PNG, JPG, JPEG, TIF, and PDF files
- **Image Preprocessing**: Automatic image enhancement for better OCR accuracy

## System Requirements

- Python 3.10 or higher
- Poetry (for dependency management)
- **For Tesseract OCR processor**:
  - Tesseract OCR installed on your system
- **For DeepSeek OCR processor**:
  - Ollama installed and running
  - DeepSeek OCR model pulled in Ollama (`ollama pull deepseek-ocr`)

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

### Installing Ollama (for DeepSeek OCR)

**Linux:**
```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama pull deepseek-ocr
```

**macOS/Windows:**
Visit [ollama.com](https://ollama.com) to download and install, then:
```bash
ollama pull deepseek-ocr
```

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd joplin-ocr-note-import
```

2. Install dependencies using Poetry:
```bash
poetry install
```

## Configuration

### Using config.yaml

Create or edit `config.yaml` in the project root:

```yaml
# Joplin OCR Note Import Tool Configuration

# Directory to watch for new images
watch_folder: "/path/to/watch/folder"

# Directory where OCR text output will be saved
output_path: "/path/to/output"

# Optional: Directory where Joplin-compatible markdown notes will be saved
# Set to a path to enable Joplin mode, or leave as null for text-only mode
joplin_path: null  # or "/path/to/joplin/notes"

# OCR Processor Selection
# Choose which OCR processor to use: "tesseract" or "deepseek"
ocr_processor: "tesseract"  # or "deepseek"

# DeepSeek OCR Configuration (only used if ocr_processor is "deepseek")
deepseek_ocr:
  model: "deepseek-ocr:latest"
  host: "http://localhost:11434"  # Ollama server address
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
- `--processor {tesseract,deepseek}`: OCR processor to use (optional, default from config)
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
3. The image is copied to the joplin directory with a sanitized filename
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

### Using DeepSeek OCR Processor

To use DeepSeek OCR instead of Tesseract, either set it in your config.yaml:

```yaml
ocr_processor: "deepseek"
```

Or specify it via command line:

```bash
poetry run python bin/tool.py --processor deepseek --watch-folder /path/to/watch
```

DeepSeek OCR provides better accuracy for complex layouts, handwritten text, and documents with mixed content.

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
   - **Tesseract**: Images are preprocessed (grayscale, upscaled) and text is extracted using Tesseract
   - **DeepSeek**: Images are sent to Ollama's DeepSeek OCR model for AI-powered text extraction
   - PDFs are converted to images at 300 DPI before processing
4. **Output Generation**:
   - **Text mode**: Creates a `.txt` file in the output directory
   - **Joplin mode**: Creates a `.md` file and copies the image to the joplin directory
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
joplin-ocr-note-import/
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
│   ├── tesseract_process.py    # Tesseract OCR processor
│   └── deepseekocr_process.py  # DeepSeek OCR processor
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
- **ollama**: Python client for Ollama API (required for DeepSeek OCR)
- **Pillow** (>=12.1.0): Image processing library
- **watchdog** (>=6.0.0): File system monitoring
- **pdf2image** (>=1.17.0): PDF to image conversion
- **pyyaml** (>=6.0.3): YAML configuration file parsing

## Tips for Best Results

1. **Choosing OCR Processor**:
   - **Tesseract**: Fast, reliable, best for standard printed text and simple layouts
   - **DeepSeek**: Better for complex layouts, handwritten text, tables, and mixed content (requires more resources)
2. **Image Quality**: Higher resolution images (300 DPI+) produce better OCR results
3. **File Formats**: PNG and TIFF generally work better than JPEG
4. **Text Clarity**: Clear, high-contrast text is easier to recognize
5. **Language Support**: Install additional Tesseract language packs if needed (Tesseract only)
6. **Preprocessing**: Tesseract automatically preprocesses images, but manual cleanup may improve results for poor quality images

## Troubleshooting

**"No module named 'pytesseract'"**
- Run `poetry install` to install dependencies

**"Tesseract not found"**
- Install Tesseract OCR on your system (see System Requirements)

**"Connection error" or "Ollama not found" (DeepSeek)**
- Ensure Ollama is installed and running (`ollama serve`)
- Check the `deepseek_ocr.host` setting in config.yaml matches your Ollama server address
- Verify the DeepSeek model is pulled (`ollama list` should show `deepseek-ocr`)

**Poor OCR accuracy**
- Try switching between Tesseract and DeepSeek processors (`--processor` flag)
- Check image quality and resolution
- Ensure text is clear and high-contrast
- Consider manually preprocessing images (for Tesseract)

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
