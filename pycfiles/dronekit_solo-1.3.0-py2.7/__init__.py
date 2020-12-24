# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/dronekit_solo/__init__.py
# Compiled at: 2016-02-26 14:57:35
from __future__ import print_function
from dronekit import Vehicle

class SoloVehicle(Vehicle):

    def __init__(self, *args):
        super(SoloVehicle, self).__init__(*args)
        self.__msg_gopro_status = None
        self.__msg_gopro_get_response = None
        self.__msg_gopro_set_response = None
        self.add_message_listener('GOPRO_HEARTBEAT', self.__on_gopro_status)
        self.add_message_listener('GOPRO_GET_RESPONSE', self.__on_gopro_get_response)
        self.add_message_listener('GOPRO_SET_RESPONSE', self.__on_gopro_set_response)
        return

    def __on_gopro_status(self, vehicle, name, m):
        self.__msg_gopro_status = m
        self.notify_attribute_listeners('gopro_status', self.gopro_status)

    @property
    def gopro_status(self):
        return self.__msg_gopro_status

    def __on_gopro_get_response(self, vehicle, name, m):
        self.__msg_gopro_get_response = (
         m.cmd_id, m.status, m.value)
        self.notify_attribute_listeners('gopro_get_response', self.gopro_get_response)

    @property
    def gopro_get_response(self):
        return self.__msg_gopro_get_response

    def __on_gopro_set_response(self, vehicle, name, m):
        self.__msg_gopro_set_response = (
         m.cmd_id, m.status)
        self.notify_attribute_listeners('gopro_set_response', self.gopro_set_response)

    @property
    def gopro_set_response(self):
        return self.__msg_gopro_set_response