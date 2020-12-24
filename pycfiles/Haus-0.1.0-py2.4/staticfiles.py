# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/haus/components/staticfiles.py
# Compiled at: 2008-11-12 23:57:47
""".. _StaticFilesComponent:

``static`` -- Static Content
============================

Uses  Static_ to serve up static content.
Provides a framework function that gets used
by selector when it is present.

.. _Static: http://lukearno.com/projects/static/

"""
from static import Cling
from haus.components.abstract import Component, update_wrapper

class StaticClingComponent(Component):
    __module__ = __name__
    provides = [
     'static_app']

    def __init__(self, wrk):
        cling = Cling(wrk.pdfilename(wrk.config['static']['root']))
        cling.not_found = wrk.functions['status404']
        cling.method_not_allowed = wrk.functions['status405']
        wrk.functions['static_app'] = cling