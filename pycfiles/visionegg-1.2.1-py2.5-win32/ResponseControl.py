# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\VisionEgg\ResponseControl.py
# Compiled at: 2009-07-07 11:29:42
"""
Response control during a presentation is running.

"""
import logging, logging.handlers, VisionEgg, VisionEgg.Core, VisionEgg.FlowControl, VisionEgg.DaqKeyboard, VisionEgg.ParameterTypes as ve_types, pygame
__version__ = VisionEgg.release_name

class ResponseController(VisionEgg.FlowControl.Controller):
    """This abstract base class defines the interface to any ResponseController.

    This module provides an interface to collect responses during a
    presentation is running. To interface with real data acquisition devices,
    use a module that subclasses the classes defined here.

    """

    def _reset(self):
        self.responses = []
        self.responses_since_go = []
        self.time_responses_since_go = []
        self.first_responses_since_go = []
        self.time_first_responses_since_go = None
        self.status_first_responses_since_go = False
        self.last_responses_since_go = []
        self.time_last_responses_since_go = None
        return

    def __init__(self, **kw):
        self._reset()

    def get_responses(self):
        """Returns the responses in the current frame."""
        return self.responses

    get_data = get_responses

    def get_responses_since_go(self):
        """Returns all responses since the main 'go' loop has been
        started."""
        return self.responses_since_go

    def get_time_responses_since_go(self):
        """Returns the time stamps for all responses since the main 'go'
        loop has been started."""
        return self.time_responses_since_go

    def get_first_response_since_go(self, index=0):
        """Returns the first response since the main 'go' loop has been
        started."""
        if self.first_responses_since_go == []:
            return []
        else:
            return self.first_responses_since_go[index]

    def get_first_responses_since_go(self):
        """Returns the first responses since the main 'go' loop has been
        started."""
        return self.first_responses_since_go

    def get_time_first_response_since_go(self):
        """Returns the time stamp for first responses since the main 'go'
        loop has been started."""
        return self.time_first_responses_since_go

    get_time_first_responses_since_go = get_time_first_response_since_go

    def get_last_response_since_go(self, index=0):
        """Returns the last response since the main 'go' loop has been
        started."""
        if self.last_responses_since_go == []:
            return []
        else:
            return self.last_responses_since_go[index]

    def get_last_responses_since_go(self):
        """Returns the last responses since the main 'go' loop has been
        started."""
        return self.last_responses_since_go

    def get_time_last_response_since_go(self):
        """Returns the time stamp for last response since the main 'go'
        loop has been started."""
        return self.time_last_responses_since_go

    get_time_last_responses_since_go = get_time_last_response_since_go

    def between_go_eval(self):
        """Evaluate between runs of the main 'go' loop.

        Override this method in subclasses."""
        raise RuntimeError('%s: Definition of between_go_eval() in abstract base class ResponseController must be overriden.' % (str(self),))

    def during_go_eval(self):
        """Evaluate during the main 'go' loop.

        Override this method in subclasses."""
        raise RuntimeError('%s: Definition of during_go_eval() in abstract base class ResponseController must be overriden.' % (str(self),))


class KeyboardResponseController(ResponseController):
    """Use the keyboard to collect responses during a presentation is running."""

    def __init__(self):
        VisionEgg.FlowControl.Controller.__init__(self, return_type=ve_types.get_type(None), eval_frequency=VisionEgg.FlowControl.Controller.EVERY_FRAME, temporal_variables=VisionEgg.FlowControl.Controller.TIME_SEC_SINCE_GO)
        self.input = VisionEgg.DaqKeyboard.KeyboardInput()
        return

    def between_go_eval(self):
        return

    def during_go_eval(self):
        if self.time_sec_since_go <= 0.01:
            self._reset()
        self.responses = self.input.get_string_data()
        if len(self.responses) > 0:
            self.responses_since_go.append(self.responses)
            self.time_responses_since_go.append(self.time_sec_since_go)
            if self.status_first_responses_since_go == False:
                self.time_first_responses_since_go = self.time_sec_since_go
                self.first_responses_since_go = self.responses
                self.status_first_responses_since_go = True
            self.time_last_responses_since_go = self.time_sec_since_go
            self.last_responses_since_go = self.responses
        return