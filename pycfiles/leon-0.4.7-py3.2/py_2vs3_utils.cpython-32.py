# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/leon/py_2vs3_utils.py
# Compiled at: 2013-05-07 11:00:08
from __future__ import unicode_literals
import sys
string_au_ou_ou = 'äöü'
if sys.version_info >= (3, 2):
    import html
    escape = html.escape
else:
    import cgi
    escape = cgi.escape