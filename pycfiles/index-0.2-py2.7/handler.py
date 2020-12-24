# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\index\proceed_default2\handler.py
# Compiled at: 2013-09-18 01:05:14
from __future__ import division, absolute_import, print_function, unicode_literals
import os, xlrd
from ..reg import reg_object1
from .models import Handler

def reg_handler(options, session, ROOT):
    handler = options.get(b'handler', b'proceed_default')
    rev = options.get(b'rev', 0)
    unique_keys = options.get(b'__all__', [])
    unique_options = dict((key, options[key]) for key in unique_keys if key in options)
    handler_dict = dict(name=handler, rev=rev, extras=unique_options)
    HANDLER = reg_object1(session, Handler, handler_dict, ROOT)
    return HANDLER