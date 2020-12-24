# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/appd/model/action_suppressions.py
# Compiled at: 2020-03-11 17:47:43
# Size of source mod 2**32: 1200 bytes
__doc__ = '\nModel classes for AppDynamics REST API\n\n.. moduleauthor:: Kyle Furlong <kyle.furlong@appdynamics.com>\n'
from . import JsonObject, JsonList

class ActionSuppression(JsonObject):
    FIELDS = {'id':'', 
     'timeRange':'', 
     'name':'', 
     'affects':''}

    def __init__(self, id=0, timeRange=None, name='', affects=None):
        self.id, self.timeRange, self.name, self.affects = (
         id, timeRange, name, affects)


class ActionSuppressions(JsonList):

    def __init__(self, initial_list=None):
        super(ActionSuppressions, self).__init__(ActionSuppression, initial_list)

    def __getitem__(self, i):
        """
        :rtype: ActionSuppression
        """
        return self.data[i]


class ActionSuppressionsResponse(JsonObject):
    FIELDS = {}

    def __init__(self):
        self.actionSuppressions = ActionSuppressions()

    @classmethod
    def from_json(cls, json_dict):
        print(json_dict)
        obj = super(ActionSuppressionsResponse, cls).from_json(json_dict)
        if 'actionSuppressions' in json_dict:
            obj.actionSuppressions = ActionSuppressions.from_json(json_dict['actionSuppressions'])
        return obj