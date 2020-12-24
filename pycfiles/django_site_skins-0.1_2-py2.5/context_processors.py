# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/skins/context_processors.py
# Compiled at: 2010-03-19 19:00:41
"""Provices formatting and text manipulation tags.

:Authors:
    - Bruce Kroeze
"""
__docformat__ = 'restructuredtext'
import skin

def active_skin(request):
    """Put the active skin into the request."""
    return {'skin': skin.active_skin()}