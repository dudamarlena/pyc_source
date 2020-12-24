# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\webbridge\__init__.py
# Compiled at: 2016-09-02 12:59:33
"""
I wanted to import a couple of things by default
for ease of use.

Instead of doing:
    from webbridge.bridge import Bridge, blow
Importing them here allows you to:
    from webbridge import Bridge, blow
"""
from bridge import Bridge, blow