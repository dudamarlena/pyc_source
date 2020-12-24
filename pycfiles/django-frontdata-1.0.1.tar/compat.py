# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/alex/projects/vk-board/src/jsonify/compat.py
# Compiled at: 2015-06-20 11:59:55
from json import dumps
try:
    from rest_framework.utils.encoders import JSONEncoder
except ImportError:
    JSONEncoder = None

def serialize_data(data):
    return dumps(data, cls=JSONEncoder)