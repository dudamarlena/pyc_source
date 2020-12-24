# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/orlo/error_handlers.py
# Compiled at: 2017-04-04 09:14:06
from __future__ import print_function
from flask import jsonify, request
from orlo.app import app
from orlo.exceptions import InvalidUsage, OrloError
__author__ = 'alforbes'

@app.errorhandler(404)
def page_not_found(error):
    d = {'message': '404 Not Found', 'url': request.url}
    return (jsonify(d), 404)


@app.errorhandler(OrloError)
@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.errorhandler(400)
def handle_400(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response