import os, logging
import os, sys, logging, traceback
from logging import handlers

def get_logger(logdir, LOG_NAME, LOG_FILE_ERROR = 'file.err', logsize=500*1024, logbackup_count=4):
    if not os.path.exists(logdir):
        os.makedirs(logdir)
    LOG_FILE_INFO = '%s/%s.log' % (logdir, LOG_NAME)
    LOG_LEVEL = logging.INFO

    LOG_FORMAT = '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
    log = logging.getLogger(LOG_NAME)
    log_formatter = logging.Formatter(LOG_FORMAT)
    log.setLevel(LOG_LEVEL)

    if log.handlers is not None and len(log.handlers) >= 0:
        for handler in log.handlers:
            log.removeHandler(handler)
        log.handlers = []
    loghandler = logging.handlers.RotatingFileHandler(LOG_FILE_INFO, maxBytes=logsize, backupCount=logbackup_count)
    ##
    loghandler.setFormatter(log_formatter)
    log.addHandler(loghandler)
    # comment this to suppress console output
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(log_formatter)
    log.addHandler(stream_handler)

    loghandler2 = logging.StreamHandler(sys.stdout)
    loghandler2.setFormatter(log_formatter)
    log.addHandler(loghandler2)

    file_handler_info = logging.FileHandler(LOG_FILE_INFO, mode='w')
    file_handler_info.setFormatter(log_formatter)
    file_handler_info.setLevel(logging.INFO)
    log.addHandler(file_handler_info)

    file_handler_error = logging.FileHandler(LOG_FILE_ERROR, mode='w')
    file_handler_error.setFormatter(log_formatter)
    file_handler_error.setLevel(logging.ERROR)
    log.addHandler(file_handler_error)
    log.setLevel(logging.INFO)
    return log