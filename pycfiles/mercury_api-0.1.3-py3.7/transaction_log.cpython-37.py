# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mercury_api/transaction_log.py
# Compiled at: 2018-06-20 15:42:58
# Size of source mod 2**32: 2647 bytes
import logging, datetime
from flask import request
from mercury_api.configuration import get_api_configuration

class TransactionFilter(logging.Filter):
    __doc__ = '\n    Filter log records to include request data in the transactional log.\n    '

    def filter(self, record):
        now = datetime.datetime.utcnow()
        record.utcnow = now.strftime('%Y-%m-%d %H:%M:%S,%f %Z')
        record.url = request.path
        record.method = request.method
        record.client = request.environ.get('X-Forwarded-For', request.remote_addr)
        return True


formatter = logging.Formatter('%(utcnow)s : %(levelname)s client=%(client)s [%(method)s] url=%(url)s : %(message)s')

def setup_logging(app):
    """
    Sets the log level set in the api configuration and attaches the 
    required log handlers to the default app logger.
    
    :param app: Flask app instance 
    :return: The Flask app default logger.
    """
    log_configuration = get_api_configuration().api.logging
    for handler in app.logger.handlers:
        app.logger.removeHandler(handler)

    logging.basicConfig(level=(log_configuration.level))
    if log_configuration.console_out:
        werkzeug = logging.getLogger('werkzeug')
        werkzeug.setLevel(logging.ERROR)
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.DEBUG)
        stream_handler.addFilter(TransactionFilter())
        stream_handler.setFormatter(formatter)
        app.logger.addHandler(stream_handler)
    file_handler = logging.FileHandler(log_configuration.log_file)
    file_handler.setLevel(log_configuration.level)
    file_handler.addFilter(TransactionFilter())
    file_handler.setFormatter(formatter)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(log_configuration.level)
    app.logger.addFilter(TransactionFilter())
    return app.logger