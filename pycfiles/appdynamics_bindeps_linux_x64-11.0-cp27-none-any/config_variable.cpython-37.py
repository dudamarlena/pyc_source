# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/appd/model/config_variable.py
# Compiled at: 2020-03-11 17:54:36
# Size of source mod 2**32: 2002 bytes
__doc__ = '\nModel classes for AppDynamics REST API\n\n.. moduleauthor:: Todd Radel <tradel@appdynamics.com>\n'
from . import JsonObject, JsonList

class ConfigVariable(JsonObject):
    """ConfigVariable"""
    FIELDS = {'name':'', 
     'description':'', 
     'scope':'', 
     'updateable':'', 
     'value':''}

    def __init__(self, name='', description='', scope='cluster', updateable=True, value=None):
        self.name, self.description, self.scope, self.updateable, self.value = (
         name, description, scope,
         updateable, value)


class ConfigVariables(JsonList):
    """ConfigVariables"""

    def __init__(self, initial_list=None):
        super(ConfigVariables, self).__init__(ConfigVariable, initial_list)

    def __getitem__(self, i):
        """
        :rtype: ConfigVariable
        """
        return self.data[i]

    def by_name(self, name):
        """
        Finds a config variable with the matching name.

        :param str name: Variable name to find.
        :return: The matching config variable.
        :rtype: appd.model.ConfigVariable
        """
        found = [x for x in self.data if x.name == name]
        try:
            return found[0]
        except IndexError:
            raise KeyError(name)