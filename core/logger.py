"""
Logging configuration for the trading bot
"""
import logging
import sys
from pathlib import Path
from config.settings import LOGGING_CONFIG

def setup_logger(name):
    """
    Setup logger for the application
    
    Args:
        name: Logger name (usually __name__)
    
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, LOGGING_CONFIG['level']))
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, LOGGING_CONFIG['level']))
    
    # File handler
    log_file = LOGGING_CONFIG['log_dir'] / f"{Path(name).stem}.log"
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(getattr(logging, LOGGING_CONFIG['level']))
    
    # Formatter
    formatter = logging.Formatter(LOGGING_CONFIG['format'])
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)
    
    # Add handlers
    if not logger.handlers:
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)
    
    return logger
