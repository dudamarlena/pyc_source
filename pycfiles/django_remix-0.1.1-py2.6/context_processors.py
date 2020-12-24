# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\remix\context_processors.py
# Compiled at: 2009-07-31 17:09:23
from remix import get_remixes

def remix(request):
    """Adds any defined remixes to the context based on matching request.path."""
    return get_remixes(request)