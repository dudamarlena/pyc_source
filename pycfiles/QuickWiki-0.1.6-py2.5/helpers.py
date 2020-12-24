# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/quickwiki/lib/helpers.py
# Compiled at: 2009-02-23 12:50:50
"""Helper functions

Consists of functions to typically be used within templates, but also
available to Controllers. This module is available to templates as 'h'.
"""
from webhelpers.html import literal
from webhelpers.html.tags import *
from webhelpers.html.secure_form import secure_form
from webhelpers.pylonslib import Flash as _Flash
flash = _Flash()