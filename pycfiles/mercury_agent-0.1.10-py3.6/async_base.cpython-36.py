# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mercury_agent/inspector/inspectors/async_inspectors/async_base.py
# Compiled at: 2018-01-10 00:48:14
# Size of source mod 2**32: 343 bytes


class AsyncInspector(object):

    def __init__(self, device_info, agent_configuration):
        self.device_info = device_info
        self.configuration = agent_configuration

    def inspect(self):
        """Cannot block"""
        raise NotImplemented

    def cleanup(self):
        """Called on agent exit"""
        raise NotImplemented