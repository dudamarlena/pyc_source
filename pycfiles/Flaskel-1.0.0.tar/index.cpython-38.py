# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\Project\CLOUD\flaskel\skeleton\blueprints\web\index.py
# Compiled at: 2020-04-15 15:30:16
# Size of source mod 2**32: 172 bytes
from flask import render_template
from . import web

@web.route('/', methods=['GET'], strict_slashes=False)
def index():
    return render_template('index.html')