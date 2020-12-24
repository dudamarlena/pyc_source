# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/notifications/notifications.py
# Compiled at: 2019-02-21 19:34:58
# Size of source mod 2**32: 288 bytes
"""
Context Processor

To include the notifications varialbe in all templates.
"""

def notifications(request):
    """Make notifications available in all templates."""
    if not request.user.is_authenticated:
        return {}
    return {'notifications': request.user.notifications}