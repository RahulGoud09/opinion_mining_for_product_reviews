import logging
import sys
from datetime import datetime
import os

def setup_logger():
    """
    Set up and configure the logger for the application.
    
    Returns:
        logging.Logger: Configured logger instance
    """
    # Create logger
    logger = logging.getLogger('opinion_mining')
    
    # Only add handlers if they haven't been added already
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        
        # Create logs directory if it doesn't exist
        if not os.path.exists('logs'):
            os.makedirs('logs')
        
        # Create handlers
        console_handler = logging.StreamHandler(sys.stdout)
        file_handler = logging.FileHandler(f'logs/opinion_mining_{datetime.now().strftime("%Y%m%d")}.log')
        
        # Create formatters and add it to handlers
        log_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(log_format)
        file_handler.setFormatter(log_format)
        
        # Add handlers to the logger
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)
    
    return logger 