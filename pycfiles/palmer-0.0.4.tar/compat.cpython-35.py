# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/loup/Workspace/Projects/personal/palmer/palmer/compat.py
# Compiled at: 2016-11-16 03:38:27
# Size of source mod 2**32: 231 bytes
from __future__ import unicode_literals, absolute_import
from flask import __version__ as flask_version

def is_flask_legacy():
    v = flask_version.split('.')
    return int(v[0]) == 0 and int(v[1]) < 11