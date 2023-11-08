import logging
import os

def my_logger(dirname='log', 
              logger_name=None, 
              debug_level='DEBUG', 
              mode='w',
              stream_logs = True,
              encoding='UTF-8'
              ):
    
    level_mapping = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR,
        'EXCEPTION': logging.ERROR,  # Exception is not a level in Python logging; it's usually logged as an ERROR
    }

    if debug_level.upper() not in level_mapping:
        raise ValueError(f"Invalid debug_level: {debug_level}. Must be one of: {', '.join(level_mapping.keys())}")

    logger = logging.getLogger(logger_name if logger_name else __name__)
    
    # Clear existing handlers
    for handler in logger.handlers[:]:
        handler.close()
        logger.removeHandler(handler)

    logger.setLevel(level_mapping[debug_level.upper()])

    formatter = logging.Formatter('%(asctime)s - %(module)s - %(levelname)s - Name: %(funcName)s - Line: %(lineno)d - %(message)s')

    # Check if the directory exists, and create it if it doesn't
    if not os.path.exists(dirname):
        os.makedirs(dirname)

    file_handler = logging.FileHandler(os.path.join(dirname, f'{logger_name if logger_name else "log"}.log'), mode=mode, encoding=encoding)
    file_handler.setLevel(level_mapping[debug_level.upper()])
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    if stream_logs == True:
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(level_mapping[debug_level.upper()])
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)
    
    return logger 