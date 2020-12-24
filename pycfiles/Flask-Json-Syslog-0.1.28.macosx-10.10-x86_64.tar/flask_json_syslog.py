# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/nabetama/.pyenv/versions/2.7.8/lib/python2.7/site-packages/flask_json_syslog/flask_json_syslog.py
# Compiled at: 2015-05-18 04:24:35
import syslog
json_available = True
json = None
try:
    import simplejson as json
except ImportError:
    try:
        import json
    except ImportError:
        json_available = False

def jsonify(dict_data, *args, **kwargs):
    if not json_available:
        raise RuntimeError('simplejson not installed')
    return json.dumps(dict(dict_data, *args, **kwargs), indent=None)


class JsonSysLog(object):

    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)
        return

    def init_app(self, app):
        if not app.config.get('JSON_SYSLOG_LEVEL'):
            app.config.setdefault('JSON_SYSLOG_LEVEL', 'info')
        if not app.config.get('JSON_SYSLOG_NUMBER'):
            app.config.setdefault('JSON_SYSLOG_NUMBER', syslog.LOG_LOCAL5)
        if not app.config.get('JSON_SYSLOG_FACILITY'):
            app.config.setdefault('JSON_SYSLOG_FACILITY', syslog.LOG_INFO)
        self.log_level = app.config['JSON_SYSLOG_LEVEL']
        self.log_number = app.config['JSON_SYSLOG_NUMBER']
        self.facility = app.config['JSON_SYSLOG_FACILITY']

    def put(self, dict_data, **kwargs):
        assert isinstance(dict_data, dict), 'dict_data is must be dict!'
        self.dict_data = dict_data.copy()
        self.dict_data.update(kwargs)
        self.syslog_output()

    def syslog_output(self):
        syslog.openlog(self.log_level, syslog.LOG_PID, self.log_number)
        syslog.syslog(self.facility, jsonify(self.dict_data))