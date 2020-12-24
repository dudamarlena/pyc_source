# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/Kodi/__init__.py
# Compiled at: 2016-01-08 04:43:20
from __future__ import unicode_literals
import sys
from .missing_tvshows import TVShows

def main():
    """Entry point for the application script"""
    sms = TVShows()
    sms.getArguments(sys.argv[1:])