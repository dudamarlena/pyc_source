# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/dbsprockets/view.py
# Compiled at: 2008-06-30 11:43:48
"""
View Module

Classes:
Name                               Description
View

Exceptions:
None

Functions:
None

Copywrite (c) 2007 Christopher Perkins
Original Version by Christopher Perkins 2007
Released under MIT license.
"""

class View:

    def __init__(self, widget, viewConfig):
        self.widget = widget
        self.viewConfig = viewConfig