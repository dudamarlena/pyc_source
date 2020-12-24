# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/hugo/.virtualenvs/gitinspector/lib/python2.7/site-packages/gitinspector/interval.py
# Compiled at: 2015-08-05 12:31:15
from __future__ import unicode_literals
__since__ = b''
__until__ = b''
__ref__ = b'HEAD'

def has_interval():
    global __since__
    global __until__
    return __since__ + __until__ != b''


def get_since():
    return __since__


def set_since(since):
    global __since__
    __since__ = b'--since="' + since + b'" '


def get_until():
    return __until__


def set_until(until):
    global __until__
    __until__ = b'--until="' + until + b'" '


def get_ref():
    global __ref__
    return __ref__


def set_ref(ref):
    global __ref__
    __ref__ = ref