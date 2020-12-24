# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/fraoustin/Workspace/ablog_api/ablog_api/util.py
# Compiled at: 2016-08-24 12:22:33
# Size of source mod 2**32: 3756 bytes
"""
    Module ablog_api.util
"""
import logging, time, os, sys, traceback, flask.config
from flask import abort
from werkzeug.exceptions import HTTPException
LEVEL = {'DEBUG': logging.DEBUG, 
 'INFO': logging.INFO, 
 'WARNING': logging.WARNING, 
 'ERROR': logging.ERROR, 
 'CRITICAL': logging.CRITICAL}
from functools import wraps
from flask import g, request, redirect, url_for

class Trace:

    def __init__(self, app):
        self._app = app

    def trace(self, f):

        @wraps(f)
        def decorated_function(*args, **kwargs):
            start_time = time.time()
            try:
                ERROR = False
                res = f(*args, **kwargs)
            except HTTPException as e:
                res = e
            except Exception as e:
                self._app.logger.error(e.__class__.__name__)
                ERROR = True
                exc_type, exc_value, exc_traceback = sys.exc_info()
                for line in traceback.format_exc().splitlines():
                    self._app.logger.error(line)

            interval = time.time() - start_time
            self._app.logger.debug('call %s: time: %s' % (f.__name__, interval))
            if ERROR:
                abort(500)
            return res

        return decorated_function


class Config(flask.config.Config):

    def __init__(self, config):
        flask.config.Config.__init__(self, config.root_path)
        for key in config.keys():
            self[key] = config[key]

    def from_env(self, namespace):
        for key in os.environ:
            if key.startswith(namespace) and key.isupper():
                try:
                    self[key] = int(os.environ.get(key))
                except:
                    self[key] = os.environ.get(key)

                continue


class ConfigAblog(Config):

    def complete(self):
        if not os.path.exists(os.path.join(self['ABLOG_CONF_DIR'], 'conf.py')):
            raise importException('conf.py not found in %s' % ['ABLOG_CONF_DIR'])
        sys.path.insert(0, self['ABLOG_CONF_DIR'])
        conf = __import__('conf')
        sys.path.pop(0)
        self['ABLOG_CWD'] = os.path.abspath(os.getcwd())
        self['ABLOG_WEBSITE'] = getattr(self, 'ABLOG_WEBSITE', os.path.join(self['ABLOG_CONF_DIR'], getattr(conf, 'ablog_builddir', '_website')))
        self['ABLOG_DOCTREES'] = getattr(self, 'ABLOG_DOCTREES', os.path.join(self['ABLOG_CONF_DIR'], getattr(conf, 'ablog_doctrees', '.doctrees')))
        self['ABLOG_BUILDER'] = getattr(self, 'ABLOG_BUILDER', getattr(conf, 'ablog_builder', 'dirhtml'))
        self['ABLOG_SRC_DIR'] = getattr(self, 'ABLOG_SRC_DIR', self['ABLOG_CONF_DIR'])
        conf.source_encoding = getattr(conf, 'source_encoding', 'utf-8-sig')
        conf.post_format_date = getattr(conf, 'post_format_date', '%b %d, %Y')
        self['ABLOG_CONF'] = conf
        self['SECRET_KEY'] = getattr(self, 'SECRET_KEY', 'secret_key')
        self['USERS'] = getattr(self, 'USERS', [])
        for key in [key for key in self.keys() if key.startswith('ABLOG_USER_')]:
            self['USERS'].append({'id': len(self['USERS']),  'username': self[key].split(':')[0],  'password': self[key].split(':')[1]})

        if not len(self['USERS']):
            self['USERS'] = [{'id': 0,  'username': 'guest',  'password': 'guest'}]
        self['ABLOG_ALLOWED_EXTENSIONS'] = getattr(self, 'ABLOG_ALLOWED_EXTENSIONS', ['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

    def allowed_file(self, filename):
        return '.' in filename and filename.rsplit('.', 1)[1] in self['ABLOG_ALLOWED_EXTENSIONS']