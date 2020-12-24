# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/kgb/pycompat.py
# Compiled at: 2020-04-10 23:22:42
"""Python compatibility functions and types."""
from __future__ import unicode_literals
import sys
pyver = sys.version_info[:2]
if pyver[0] == 2:
    text_type = unicode

    def iterkeys(d):
        return d.iterkeys()


    def iteritems(d):
        return d.iteritems()


else:
    text_type = str

    def iterkeys(d):
        return iter(d.keys())


    def iteritems(d):
        return iter(d.items())