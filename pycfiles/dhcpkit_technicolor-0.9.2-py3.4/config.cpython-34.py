# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/dhcpkit_technicolor/server_extension/config.py
# Compiled at: 2016-07-07 05:19:26
# Size of source mod 2**32: 1000 bytes
"""
Configuration elements for the SOL_MAX_RT option handlers
"""
from dhcpkit.ipv6.server.handlers import HandlerFactory
from dhcpkit_technicolor.server_extension import SolMaxRTTechnicolorOptionHandler

def max_rt(value: str) -> int:
    """
    Convert the name of the section to the number of seconds, and validate the range

    :param value: Config section name
    :return: Number of seconds
    """
    seconds = int(value)
    if not 60 <= seconds <= 86400:
        raise ValueError('MAX_RT must be between 60 and 86400 seconds')
    return seconds


class SolMaxRTTechnicolorOptionHandlerFactory(HandlerFactory):
    __doc__ = '\n    Create the handler for the SolMaxRTTechnicolorOption.\n    '

    def create(self) -> SolMaxRTTechnicolorOptionHandler:
        """
        Create a handler of this class based on the configuration in the config section.

        :return: A handler object
        """
        return SolMaxRTTechnicolorOptionHandler(self.limit, always_send=self.always_send)