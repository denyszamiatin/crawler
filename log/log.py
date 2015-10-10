import logging

# create logger
logger = logging.getLogger('crawler')
logger.setLevel(logging.DEBUG)

# create file handler which logs even debug messages
fh = logging.FileHandler('debug.log')
fh.setLevel(logging.DEBUG)
logger.addHandler(fh)

def log_error(message):
    logger.error(message)
    return message