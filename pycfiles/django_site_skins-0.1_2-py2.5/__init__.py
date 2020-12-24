# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/skins/__init__.py
# Compiled at: 2010-03-19 19:00:41
"""__init__ module for Skin app.

:Authors:
    - Bruce Kroeze
"""
__docformat__ = 'restructuredtext'
VERSION = (0, 1, 2)
if len(VERSION) > 2 and VERSION[2] is not None:
    str_version = '%d.%d_%s' % VERSION[:3]
else:
    str_version = '%d.%d' % VERSION[:2]
__version__ = str_version