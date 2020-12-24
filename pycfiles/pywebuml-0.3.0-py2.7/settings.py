# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\pywebuml\settings.py
# Compiled at: 2011-03-03 19:51:46
"""
Has the different settings.
"""
import os
CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))
DEBUG = True
DEBUG_DATABASE = False
DATABASE_URL = 'sqlite:///%s/database.db' % CURRENT_DIR