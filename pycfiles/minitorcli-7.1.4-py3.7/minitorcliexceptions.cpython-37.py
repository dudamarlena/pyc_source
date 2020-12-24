# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/vincent/Projects/PythonMinitor/minitorcli/minitorcli/minitorcliexceptions.py
# Compiled at: 2020-01-13 10:17:17
# Size of source mod 2**32: 2503 bytes
"""
Custom exception code for minitorcli.

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""
from minitorcorelib import TransferAgent, BootstrapAgent, Tunnel, Machine
__author__ = 'Vincent Schouten <inquiry@intoreflection.co>'
__docformat__ = 'google'
__date__ = '06-04-2019'
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
            self.message = f"could not copy minitoragent module to {obj.ip_address_i}"
        if isinstance(obj, BootstrapAgent):
            self.message = 'could not execute minitoragent module'
        if isinstance(obj, Tunnel):
            self.message = f"could not connect to tunnel {obj.ip_address_i}"
        if isinstance(obj, Machine):
            self.message = f"could not set up machine {obj.hostname}"
        super().__init__(self.message)