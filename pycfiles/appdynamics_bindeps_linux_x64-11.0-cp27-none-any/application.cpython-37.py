# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/appd/model/application.py
# Compiled at: 2020-03-11 17:47:43
# Size of source mod 2**32: 1419 bytes
__doc__ = '\nModel classes for AppDynamics REST API\n\n.. moduleauthor:: Todd Radel <tradel@appdynamics.com>\n'
from . import JsonObject, JsonList

class Application(JsonObject):
    """Application"""
    FIELDS = {'id':'', 
     'name':'',  'description':''}

    def __init__(self, app_id=0, name=None, description=None):
        self.id, self.name, self.description = app_id, name, description


class Applications(JsonList):
    """Applications"""

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