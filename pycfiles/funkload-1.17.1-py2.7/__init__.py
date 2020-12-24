# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/funkload/__init__.py
# Compiled at: 2015-05-06 05:03:08
"""Funkload package init.

$Id: __init__.py 24649 2005-08-29 14:20:19Z bdelbosc $
"""
try:
    from gevent.monkey import patch_all
    patch_all()
except ImportError:
    pass