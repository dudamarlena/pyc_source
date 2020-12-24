# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/alex/projects/vk-board/src/jsonify/api.py
# Compiled at: 2015-06-20 17:56:52
from collections import defaultdict

def has_frontdata(request):
    return hasattr(request, '_frontdata')


def get_frontdata(request):
    if not has_frontdata(request):
        request._frontdata = defaultdict(dict)
    return request._frontdata


def frontdata(request, key=None):
    return get_frontdata(request)[(key or 'initial')]