# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/alessio/Envs/remote-wps/lib/python2.7/site-packages/wpsremote/bus.py
# Compiled at: 2016-02-23 09:10:28
__author__ = 'Alessio Fabiani'
__copyright__ = 'Copyright 2016 Open Source Geospatial Foundation - all rights reserved'
__license__ = 'GPL'

class Bus(object):

    def __init__(self, id):
        self.callbacks = {}
        self.id = id

    def Listen(self):
        pass

    def CheckServerIdentity(self, serverId):
        pass

    def SendMessage(self, Message):
        pass

    def Stop(self, Message):
        pass

    def RegisterMessageCallback(self, message_type, callback):
        self.callbacks[message_type] = callback