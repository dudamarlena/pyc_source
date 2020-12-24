# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/foxylib/tools/flask/flask_tool.py
# Compiled at: 2020-02-07 17:24:39
# Size of source mod 2**32: 4269 bytes
import logging
from flask import url_for
from foxylib.tools.collections.collections_tool import l_singleton2obj, merge_dicts, DictTool, vwrite_no_duplicate_key
from foxylib.tools.function.function_tool import FunctionTool
from foxylib.tools.json.json_tool import jpath_v2j, jdown
from foxylib.tools.log.foxylib_logger import FoxylibLogger

class FlaskToolSessionType:

    class Value:
        FILESYSTEM = 'filesystem'

    V = Value


class FlaskTool:

    @classmethod
    def func2endpoint(cls, func):
        return FunctionTool.func2fullpath(func)

    @classmethod
    def add_url2app(cls, app, url, view_func, methods, endpoint=None):
        logger = FoxylibLogger.func_level2logger(cls.add_url2app, logging.DEBUG)
        if endpoint is None:
            endpoint = cls.func2endpoint(view_func)
        logger.debug({'url':url,  'endpoint':endpoint})
        app.add_url_rule(url, endpoint=endpoint,
          view_func=view_func,
          methods=methods)

    @classmethod
    def func2url(cls, f, values=None):
        if values is None:
            values = {}
        return url_for((cls.func2endpoint(f)), **values)

    @classmethod
    def user2username_authenticated(cls, user):
        if not user:
            return
        else:
            return cls.user2is_authenticated(user) or None
        return str(user.username)

    @classmethod
    def user2email_authenticated(cls, user):
        if not user:
            return
        else:
            return cls.user2is_authenticated(user) or None
        return str(user.email)

    @classmethod
    def user2is_authenticated(cls, user):
        return user and user.is_authenticated

    @classmethod
    def request2params(cls, request):
        if not request:
            return
        return request.args

    @classmethod
    def request_key2param(cls, request, key):
        url_params = cls.request2params(request)
        if not url_params:
            return
        return url_params.get(key)


class FormResult:

    class Field:
        IN = 'in'
        DATA = 'data'
        ERROR = 'error'

    F = Field

    @classmethod
    def j_form2is_valid(cls, j_form):
        j_error = j_form.get(cls.F.ERROR)
        return not j_error

    @classmethod
    def j_form2j_data(cls, j_form):
        return j_form.get(cls.F.DATA)

    @classmethod
    def j_form2h_jinja2(cls, j_form):
        if not j_form:
            return
        h_jinja2 = {k:{'value': v} for k, v in j_form.items() if v if v}
        return h_jinja2


rq2params = FlaskTool.request2params
rq_key2param = FlaskTool.request_key2param