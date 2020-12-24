# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/avisosms/base.py
# Compiled at: 2014-01-27 08:45:40
from __future__ import unicode_literals

class MountPoint(type):

    def __new__(meta, classname, bases, classdict):
        if b'plugins' in classdict.keys():
            bases = classdict[b'plugins'] + bases
        return type.__new__(meta, classname, bases, classdict)