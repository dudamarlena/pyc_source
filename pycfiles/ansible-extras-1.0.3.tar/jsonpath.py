# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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