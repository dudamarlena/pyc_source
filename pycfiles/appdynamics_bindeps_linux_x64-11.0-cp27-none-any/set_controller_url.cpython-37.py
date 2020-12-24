# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/appd/model/set_controller_url.py
# Compiled at: 2020-03-11 17:47:43
# Size of source mod 2**32: 589 bytes
__doc__ = '\nModel classes for AppDynamics REST API\n\n.. moduleauthor:: Kyle Furlong <kyle.furlong@appdynamics.com>\n'
from . import JsonObject, JsonList

class SetControllerUrl(JsonObject):
    FIELDS = {'controllerURL': ''}

    def __init__(self, controllerURL=''):
        self.controllerURL = controllerURL


class SetControllerUrlResponse(JsonList):

    def __init__(self, initial_list=None):
        super(SetControllerUrlResponse, self).__init__(SetControllerUrl, initial_list)

    def __getitem__(self, i):
        """
        :rtype: Node
        """
        return self.data[i]