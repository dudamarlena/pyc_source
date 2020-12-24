# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-intel/egg/flask_boot/project/application/core/response.py
# Compiled at: 2018-09-06 04:56:45
from werkzeug.wrappers import Response
from flask import jsonify

class JSONResponse(Response):
    _header_dict = {'Content-Type': 'application/json'}

    @classmethod
    def force_type(cls, response, environ=None):
        if isinstance(response, dict):
            response = jsonify(response)
        return super(JSONResponse, cls).force_type(response, environ)