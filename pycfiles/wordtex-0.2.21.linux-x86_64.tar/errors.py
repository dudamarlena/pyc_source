# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/wordtex/cloudtb/errors.py
# Compiled at: 2013-11-12 16:48:22
import sys, os, traceback

class NeedModule(ImportError):

    def __init__(self, value):
        self.value = value

    def __str__(self, value):
        return 'Module Dependency not met: ' + repr(self.value)


class ModuleError(Exception):
    """An error to give for module-level failures."""
    pass


class RequestError(Exception):
    pass


def get_prev_exception_str(*args, **kwargs):
    """Only prints out the actual exception if you pass in E. Otherwise just
    gives you the line information"""
    exc_info = sys.exc_info()
    E = exc_info[0]
    Estr = exc_info[1].message
    tb = sys.exc_info()[2]
    return ('').join(traceback.format_exception(E, Estr, tb))


def print_prev_exception(*args, **kwargs):
    print get_prev_exception_str(*args, **kwargs)