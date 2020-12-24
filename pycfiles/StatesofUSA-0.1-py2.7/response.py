# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/statesofusa/response.py
# Compiled at: 2016-03-09 11:22:16
__author__ = 'Isham'
from flask import jsonify
from app import app

class RestResponse(object):

    @classmethod
    def get(cls, status, _type, message, result=None, **kwargs):
        data = {'type': _type, 'status': status, 'message': message}
        if kwargs:
            data['additional_data'] = kwargs
        if result is not None:
            data['data'] = result
        content = jsonify(data)
        return app.make_response(content)