# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /work/ansible/ansible-extras/filter_plugins/debug.py
# Compiled at: 2018-10-03 10:45:55
from ansible import errors
import sys

def debug_obj(obj):
    sys.stderr.write(str(obj) + '\n')
    return ''


class FilterModule(object):

    def filters(self):
        return {'debug_obj': debug_obj}