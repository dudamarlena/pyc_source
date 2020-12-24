# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/vincent/Projects/PythonPowerMole/powermolecli/powermolecli/powermolecliexceptions.py
# Compiled at: 2020-05-11 18:23:31
# Size of source mod 2**32: 2499 bytes
"""
Custom exception code for minitorcli.

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""
from powermolelib import TransferAgent, BootstrapAgent, Tunnel, Assistant
__author__ = 'Vincent Schouten <inquiry@intoreflection.co>'
__docformat__ = 'google'
__date__ = '12-05-2020'
__copyright__ = 'Copyright 2019, Vincent Schouten'
__credits__ = ['Vincent Schouten']
__license__ = 'MIT'
__maintainer__ = 'Vincent Schouten'
__email__ = '<inquiry@intoreflection.co>'
__status__ = 'Development'

class SetupFailed(Exception):
    __doc__ = 'The setup has failed.'

    def __init__(self, obj):
        self.message = 'Unknown object provided'
        if isinstance(obj, TransferAgent):
            self.message = 'could not copy agent module to last host'
        if isinstance(obj, BootstrapAgent):
            self.message = 'could not execute agent module'
        if isinstance(obj, Tunnel):
            self.message = 'could setting up tunneling'
        if isinstance(obj, Assistant):
            self.message = 'could not set up assistant to interact with agent on target destination host'
        super().__init__(self.message)