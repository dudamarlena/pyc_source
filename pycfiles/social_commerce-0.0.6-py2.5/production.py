# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/socialcommerce/production.py
# Compiled at: 2009-10-31 23:19:40
import os
DEBUG = False
DEBUG_TOOLBAR = False
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
execfile(PROJECT_ROOT + '/settings.py')