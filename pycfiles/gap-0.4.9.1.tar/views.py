# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/robin/projects/gap/.venv/lib/python2.7/site-packages/gap/templates/module/views.py
# Compiled at: 2013-10-11 03:16:02
from gap.utils.decorators import as_view

@as_view
def module_welcome_screen(request, response):
    return 'Welcome to example module'