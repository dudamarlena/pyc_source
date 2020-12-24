# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: skytap/framework/Suspendable.py
# Compiled at: 2016-12-16 14:55:45
"""Add the Suspendable class to classes that can be run/suspended/etc."""
from skytap.framework.ApiClient import ApiClient
from skytap.framework.Config import Config
import time

class Suspendable(object):
    """Add the change_state() functionality to the class.

    This includes supporting functions, like run() and suspend().
    """
    valid_states = [
     'running', 'suspended', 'reset', 'stopped', 'halted']

    def suspend(self, wait=False):
        """Suspend the object (environment/vm)."""
        self.change_state('suspended', wait)

    def run(self, wait=False):
        """Run the object (environment/vm)."""
        self.change_state('running', wait)

    def halt(self, wait=False):
        """Halt the object (environment/vm)."""
        self.change_state('halted', wait)

    def reset(self, wait=False):
        """Reset the object (environment/vm)."""
        self.change_state('reset', wait)

    def stop(self, wait=False):
        """Stop the object (environment/vm)."""
        self.change_state('stopped', wait)

    def change_state(self, state, wait=False):
        """Change the state of the object (environment/vm)."""
        if state not in Suspendable.valid_states:
            raise ValueError(str(state) + ' not a valid state.')
        self.refresh()
        if self.runstate == state:
            return True
        if Config.add_note_on_state_change:
            self.notes.add("Changing state via API to '" + state + "'")
        api = ApiClient()
        url = self.url + '.json'
        data = {'runstate': state}
        api.rest(url, {}, 'PUT', data)
        if not wait:
            return True
        if state == 'reset':
            state = 'running'
        if state == 'halted':
            state = 'stopped'
        self.refresh()
        counter = 0
        while not self.runstate == state and counter < 12:
            time.sleep(10)
            self.refresh()

        if self.runstate == state:
            return True
        return False