# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/alessio/Envs/remote-wps/lib/python2.7/site-packages/wpsremote/busIndipendentMessages.py
# Compiled at: 2018-09-24 09:03:41
__author__ = 'Alessio Fabiani'
__copyright__ = 'Copyright 2016 Open Source Geospatial Foundation - all rights reserved'
__license__ = 'GPL'
import pickle

class BusInipendentMessage(object):
    pass


class PresenceMessage(BusInipendentMessage):
    pass


class InviteMessage(BusInipendentMessage):

    def __init__(self, payload, originator):
        self._originator = originator
        self._payload = payload

    def originator(self):
        return self._originator


class RegisterMessage(BusInipendentMessage):

    def __init__(self, originator, service, namespace, descritpion, par, output):
        self._originator = originator
        self.service = service
        self.namespace = namespace
        self.description = descritpion
        self._input_parameter = par
        self.output = output

    def input_parameters(self):
        return self._input_parameter

    def originator(self):
        return self._originator


class ExecuteMessage(BusInipendentMessage):

    @staticmethod
    def deserialize(filepath):
        fp = open(filepath)
        exe_msg = pickle.load(fp)
        fp.close()
        return exe_msg

    def __init__(self, originator, uniqueExeId, baseURL, variables):
        self._uniqueExeId = uniqueExeId
        self._baseURL = baseURL
        self._originator = originator
        self._variables = variables

    def variables(self):
        return self._variables

    def originator(self):
        return self._originator

    def UniqueId(self):
        return self._uniqueExeId

    def BaseURL(self):
        return self._baseURL

    def serialize(self, fileptr):
        pickle.dump(self, fileptr)


class ProgressMessage(BusInipendentMessage):

    def __init__(self, originator, progress):
        self.originator = originator
        self.progress = progress


class LogMessage(BusInipendentMessage):

    def __init__(self, originator, level, msg):
        self.level = level
        self.originator = originator
        self.msg = msg


class CompletedMessage(BusInipendentMessage):

    def __init__(self, originator, base_url, outputs):
        self.originator = originator
        self.base_url = base_url
        self._outputs = outputs

    def outputs(self):
        return self._outputs


class FinishMessage(BusInipendentMessage):

    def __init__(self, payload, originator):
        self.originator = originator
        self.payload = payload


class ErrorMessage(BusInipendentMessage):

    def __init__(self, originator, msg, id=None):
        self.originator = originator
        self.msg = msg
        self.id = id


class AbortMessage(BusInipendentMessage):

    def __init__(self, payload, originator):
        self.originator = originator
        self.payload = payload


class GetLoadAverageMessage(BusInipendentMessage):

    def __init__(self, payload, originator):
        self._originator = originator
        self._payload = payload

    def originator(self):
        return self._originator


class LoadAverageMessage(BusInipendentMessage):

    def __init__(self, originator, outputs):
        self.originator = originator
        self._outputs = outputs

    def outputs(self):
        return self._outputs