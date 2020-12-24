# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/orlo/app.py
# Compiled at: 2017-04-28 10:59:55
from __future__ import print_function
import os, logging, gunicorn.app.base
from gunicorn.six import iteritems
from logging import Formatter
from logging.handlers import RotatingFileHandler
from flask import Flask
from flask_alembic import Alembic
from orlo.config import config
from orlo.exceptions import OrloStartupError
__author__ = 'alforbes'
app = Flask(__name__)
alembic = Alembic()
alembic.init_app(app)
app.config['SQLALCHEMY_DATABASE_URI'] = config.get('db', 'uri')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
if not app.config['SQLALCHEMY_DATABASE_URI'].startswith('sqlite'):
    app.config['SQLALCHEMY_POOL_SIZE'] = config.getint('db', 'pool_size')
    app.config['SQLALCHEMY_POOL_RECYCLE'] = 2
    app.config['SQLALCHEMY_MAX_OVERFLOW'] = 10
if config.getboolean('flask', 'propagate_exceptions'):
    app.config['PROPAGATE_EXCEPTIONS'] = True
if config.getboolean('db', 'echo_queries'):
    app.config['SQLALCHEMY_ECHO'] = True
if not config.getboolean('flask', 'strict_slashes'):
    app.url_map.strict_slashes = False
if config.getboolean('flask', 'debug'):
    app.debug = True
if not app.debug:
    try:
        _level = config.get('logging', 'level')
        log_level = getattr(logging, _level.upper())
    except AttributeError:
        app.logger.error(('Failed to set log level to {}, see https://docs.python.org/3.6/library/logging.html#logging-levels for valid levels.').format(_level))
        log_level = logging.INFO

    app.logger.setLevel(log_level)
    log_format = config.get('logging', 'format')
    formatter = Formatter(log_format)
    for h in app.logger.handlers:
        h.setFormatter(formatter)

    log_dir = config.get('logging', 'directory')
    logfile = os.path.join(log_dir, 'orlo.log')
    if log_dir != 'disabled':
        file_handler = RotatingFileHandler(logfile, maxBytes=1048576, backupCount=1)
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.DEBUG)
        app.logger.addHandler(file_handler)

class OrloApplication(gunicorn.app.base.BaseApplication):
    """ Gunicorn application """

    def __init__(self, application, options=None):
        self.options = options or {}
        self.application = application
        super(OrloApplication, self).__init__()

    def load_config(self):
        _config = dict([ (key, value) for key, value in iteritems(self.options) if key in self.cfg.settings and value is not None
                       ])
        for key, value in iteritems(_config):
            self.cfg.set(key.lower(), value)

        return

    def load(self):
        return self.application


if config.getboolean('security', 'enabled') and config.get('security', 'secret_key') == 'change_me':
    raise OrloStartupError('Security is enabled, please configure security:secret_key in orlo.ini')
app.logger.debug(('Log level: {}').format(config.get('logging', 'level')))
import orlo.error_handlers, orlo.routes, orlo.user_auth