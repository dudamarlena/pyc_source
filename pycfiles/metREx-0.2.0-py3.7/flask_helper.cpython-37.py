# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/app/main/util/flask_helper.py
# Compiled at: 2020-04-16 16:30:09
# Size of source mod 2**32: 183 bytes
from flask import make_response

def format_response(data, content_type):
    response = make_response(data)
    response.headers['content-type'] = content_type
    return response