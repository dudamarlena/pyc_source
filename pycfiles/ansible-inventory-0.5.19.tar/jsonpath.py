# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /work/ansible/ansible-extras/filter_plugins/jsonpath.py
# Compiled at: 2018-10-03 10:45:55
from ansible import errors
import re

def jsonpath(obj, expr):
    try:
        from jsonpath_rw import jsonpath, parse
    except:
        raise ModuleNotFoundError('Install jsonpath_rw using pip install jsonpath_rw first')

    return parse(expr).find(obj)


class FilterModule(object):
    """ A filter to transform data structures using jsonpath"""

    def filters(self):
        return {'jsonpath': jsonpath}