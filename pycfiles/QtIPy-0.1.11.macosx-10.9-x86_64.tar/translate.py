# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/qtipy/translate.py
# Compiled at: 2014-05-12 19:21:02
from __future__ import unicode_literals
from .qt import QCoreApplication

def tr(s, *args, **kwargs):
    try:
        return QCoreApplication.translate(b'@default', s, *args, **kwargs)
    except:
        return s