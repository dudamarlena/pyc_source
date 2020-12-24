# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/softwarefabrica/django/utils/templatetags/basename.py
# Compiled at: 2010-02-19 11:52:06
"""
'basename' template filter.

Return the filename component of a full path.

Copyright (C) 2010 Marco Pantaleoni. All rights reserved.
"""
import os
from django import template
register = template.Library()

def basename(pathname):
    return os.path.basename(pathname)


register.filter(basename)