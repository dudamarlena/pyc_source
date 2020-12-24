# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/idm/Work/flask-diamond/flask_diamond/facets/logs.py
# Compiled at: 2016-11-18 16:26:45
import logging

def init_logs(self):
    """
    Initialize a log file to collect messages.

    :returns: None

    This file may be written to using

    >>> flask.current_app.logger.info("message")
    """
    handler = logging.FileHandler(self.app.config['LOG'])
    handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s'))
    self.app.logger.addHandler(handler)
    if self.app.config.get('LOG_LEVEL') == 'DEBUG':
        self.app.logger.setLevel(logging.DEBUG)
    elif self.app.config.get('LOG_LEVEL') == 'WARN':
        self.app.logger.setLevel(logging.WARN)
    else:
        self.app.logger.setLevel(logging.INFO)
    self.app.logger.info('Startup with log: %s' % self.app.config['LOG'])