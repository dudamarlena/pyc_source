# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/haus/components/locations.py
# Compiled at: 2008-11-12 23:57:47
""".. _LocationsComponent:

``locations`` -- Application Locations
======================================

Find common locations in the application.

"""
from haus.components.abstract import Component

class LocationsComponent(Component):
    __module__ = __name__
    provides = [
     'get_locations']

    def __init__(self, wrk):
        """Set up locations, relative paths considered from prefix."""
        locations = wrk.config.get('locations', {})
        for (name, path) in locations.items():
            if not path.startswith('/'):
                locations[name] = wrk.config['app']['prefix'] + '/' + path

        self.locations = locations
        wrk.functions['get_locations'] = self.get_locations

    def get_locations(self, environ):
        return self.locations