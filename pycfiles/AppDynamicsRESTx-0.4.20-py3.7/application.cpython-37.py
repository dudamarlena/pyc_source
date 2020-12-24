# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/appd/model/application.py
# Compiled at: 2020-03-11 17:47:43
# Size of source mod 2**32: 1419 bytes
"""
Model classes for AppDynamics REST API

.. moduleauthor:: Todd Radel <tradel@appdynamics.com>
"""
from . import JsonObject, JsonList

class Application(JsonObject):
    __doc__ = '\n    Represents a business application. The following attributes are defined:\n\n    .. data:: id\n\n        Numeric ID of the application.\n\n    .. data:: name\n\n        Application name.\n\n    .. data:: description\n\n        Optional description of the application.\n    '
    FIELDS = {'id':'', 
     'name':'',  'description':''}

    def __init__(self, app_id=0, name=None, description=None):
        self.id, self.name, self.description = app_id, name, description


class Applications(JsonList):
    __doc__ = '\n    Represents a collection of :class:`Application` objects. Extends :class:`UserList`, so it supports the\n    standard array index and :keyword:`for` semantics.\n    '

    def __init__(self, initial_list=None):
        super(Applications, self).__init__(Application, initial_list)

    def __getitem__(self, i):
        """
        :rtype: Application
        """
        return self.data[i]

    def by_name(self, name):
        """
        Finds an application by name.

        :returns: First application with the correct name
        :rtype: :class:`Application`
        """
        found = [x for x in self.data if x.name == name]
        try:
            return found[0]
        except IndexError:
            raise KeyError(name)