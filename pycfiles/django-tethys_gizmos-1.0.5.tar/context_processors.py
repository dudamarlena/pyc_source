# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/swainn/projects/tethysdev/django-tethys_gizmos/tethys_gizmos/context_processors.py
# Compiled at: 2015-02-05 15:08:36


def tethys_gizmos_context(request):
    """
    Add the gizmos_rendered context to the global context.
    """
    context = {'gizmos_rendered': []}
    return context