"""
Common logging configuration for the Tesseract Hot Folder Tool.
"""
import logging
import sys


def setup_logging(level=logging.INFO):
    """
    Configure logging with a consistent format across all modules.

    Format includes: date, module, function/method, line number, and message.

    Args:
        level: The logging level (default: logging.INFO)
    """
    log_format = '%(asctime)s - %(name)s - %(funcName)s:%(lineno)d - %(levelname)s - %(message)s'
    date_format = '%Y-%m-%d %H:%M:%S'

    logging.basicConfig(
        level=level,
        format=log_format,
        datefmt=date_format,
        stream=sys.stdout,
        force=True  # Override any existing configuration
    )


def get_logger(name):
    """
    Get a logger instance for a module.

    Args:
        name: The name of the module (typically __name__)

    Returns:
        A configured logger instance
    """
    return logging.getLogger(name)
