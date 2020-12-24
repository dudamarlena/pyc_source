# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/app/app.py
# Compiled at: 2015-12-07 10:28:20
from sling import create_app
from sling.ext import example
from modules import localmodule
app = create_app(modules=[
 example,
 localmodule])