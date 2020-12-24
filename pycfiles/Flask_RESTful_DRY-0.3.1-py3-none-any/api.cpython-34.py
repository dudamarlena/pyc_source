# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/bruce/GoTonight/restful_poc/Flask-RESTful-DRY/build/lib/flask_dry/api/api.py
# Compiled at: 2015-04-14 08:11:28
# Size of source mod 2**32: 1603 bytes
from datetime import datetime, date, time
from flask.ext.restful import Api
from flask.ext.restful.representations import json
from ..model.utils import names_from_module
_datetime_formats = {datetime: '%Y-%m-%dT%H:%M:%S', 
 date: '%Y-%m-%d', 
 time: '%H:%M:%S'}

def to_json(o):
    format = _datetime_formats.get(type(o))
    if format:
        return o.strftime(format)
    raise TypeError


json.settings.update(sort_keys=True, ensure_ascii=False, check_circular=False, default=to_json)

class DRY_Api(Api):

    def __init__(self, app=None, *args, **kwargs):
        if app is not None:
            if app.debug:
                json.settings.setdefault('indent', 4)
        kwargs.setdefault('catch_all_404s', True)
        super().__init__(app, *args, **kwargs)

    def load_apis_from_module(self, all_apis):
        return self.load_apis(*names_from_module(all_apis))

    def load_apis(self, *apis):
        apis = {}
        for each_api in apis:
            if hasattr(each_api, 'resource_init'):
                each_api.resource_init(self)
            apis[each_api.__name__] = each_api

        return apis

    def unauthorized(self, response):
        if 'WWW-Authenticate' not in response.headers:
            response.headers['WWW-Authenticate'] = 'login realm="{}"'.format(self.app.config['DRY_WWW_AUTHENTICATE_LOGIN_REALM'])
        return response