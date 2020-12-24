# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/ore/yuiwidget/interfaces.py
# Compiled at: 2008-09-11 20:30:06
from zope.app.form.interfaces import ConversionError

class IllegalHTML(ConversionError):
    """
    illegal html, possible cross site scripting attempt
    """
    pass