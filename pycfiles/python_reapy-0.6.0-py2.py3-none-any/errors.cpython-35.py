# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /media/despres/MAIN/Users/despres/Desktop/reaper/scripts/reapy/reapy/errors.py
# Compiled at: 2019-02-26 09:05:58
# Size of source mod 2**32: 2602 bytes
"""Define custom errors."""

class DisabledDistAPIError(Exception):

    def __init__(self):
        message = "Can't reach distant API. Please start REAPER, or call reapy.config.enable_dist_api() from inside REAPER to enable distant API."
        super(DisabledDistAPIError, self).__init__(message)


class DisabledDistAPIWarning(Warning):

    def __init__(self):
        message = "Can't reach distant API. Please start REAPER, or call reapy.config.enable_dist_api() from inside REAPER to enable distant API."
        super(DisabledDistAPIWarning, self).__init__(message)


class DisconnectedClientError(Exception):

    def __init__(self):
        message = 'Client disconnected. Call self.connect to reconnect.'
        super(DisconnectedClientError, self).__init__(message)


class DistError(Exception):

    def __init__(self, tb_string):
        message = '\n\nAn error occurred while running a Program in REAPER. Traceback was :\n\n{}'.format(tb_string)
        super(DistError, self).__init__(message)


class OutsideREAPERError(Exception):

    def __init__(self):
        message = 'reapy can not be enabled or disabled from outside REAPER'
        super(OutsideREAPERError, self).__init__(message)


class RedoError(Exception):

    def __init__(self):
        message = "Can't redo."
        super(RedoError, self).__init__(message)


class UndefinedEnvelopeError(Exception):

    def __init__(self, index, name, chunk_name):
        if index is not None:
            message = 'No envelope with index {}'.format(index)
        else:
            if name is not None:
                message = 'No envelope with name {}'.format(name)
            else:
                message = 'No envelope with chunk name {}'.format(chunk_name)
        super(UndefinedEnvelopeError, self).__init__(message)


class UndefinedExtStateError(Exception):

    def __init__(self, key):
        message = 'Undefined extended state for key {}.'.format(key)
        super(UndefinedExtStateError, self).__init__(message, key)


class UndefinedFXParamError(Exception):

    def __init__(self, fx_name, name):
        message = 'No param named "{}" for FX "{}"'.format(name, fx_name)
        super(UndefinedFXParamError, self).__init__(message)


class UndoError(Exception):

    def __init__(self):
        message = "Can't undo."
        super(UndoError, self).__init__(message)