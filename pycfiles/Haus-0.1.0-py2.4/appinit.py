# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/haus/components/appinit.py
# Compiled at: 2008-11-12 23:57:47
""".. _AppInitComponent:

``appinit`` -- Application Initialization
=========================================

If your package has an ``init()`` function, this will
try to call it with the :class:`haus.core.Haus` instance.
By default, his is the very last builtin component run.

"""
from haus.components.abstract import Component
from resolver import resolve

class AppInitComponent(Component):
    __module__ = __name__

    def __init__(self, wrk):
        try:
            init = resolve(wrk.package_name + ':init')
            init(wrk)
        except (ImportError, AttributeError), err:
            pass