# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/kyle/fcms/flask-cms/flask_cms/ext.py
# Compiled at: 2016-01-26 17:48:16
"""
    ext.py
    ~~~
    :license: BSD, see LICENSE for more details
"""
from flask.ext.debugtoolbar import DebugToolbarExtension
from flask.ext.wtf import Form
from flask.ext.codemirror import CodeMirror
from flask.ext.pagedown import PageDown
from flask.ext.alembic import Alembic
pagedown = PageDown()
codemirror = CodeMirror()
alembic = Alembic()
ext = ''
toolbar = lambda app: DebugToolbarExtension(app)