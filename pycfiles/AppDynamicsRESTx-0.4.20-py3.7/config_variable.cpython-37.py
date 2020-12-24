# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/appd/model/config_variable.py
# Compiled at: 2020-03-11 17:54:36
# Size of source mod 2**32: 2002 bytes
"""
Model classes for AppDynamics REST API

.. moduleauthor:: Todd Radel <tradel@appdynamics.com>
"""
from . import JsonObject, JsonList

class ConfigVariable(JsonObject):
    __doc__ = "\n    Represents a controller configuration variable. The following attributes are defined:\n\n    .. data:: name\n\n       Variable name.\n\n    .. data:: value\n\n      Current value.\n\n    .. data:: description\n\n      Optional description of the variable.\n\n    .. data:: updateable\n\n      If :const:`True`, value can be changed.\n\n    .. data:: scope\n\n      Scope of the variable. The scope can be ``'cluster'`` or ``'local'``. Variables with cluster scope are\n      replicated across HA controllers; local variables are not.\n    "
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
    __doc__ = '\n    Represents a collection of :class:`ConfigVariable` objects. Extends :class:`UserList`, so it supports the\n    standard array index and :keyword:`for` semantics.\n    '

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