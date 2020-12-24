# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/appd/model/set_controller_url.py
# Compiled at: 2020-03-11 17:47:43
# Size of source mod 2**32: 589 bytes
"""
Model classes for AppDynamics REST API

.. moduleauthor:: Kyle Furlong <kyle.furlong@appdynamics.com>
"""
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