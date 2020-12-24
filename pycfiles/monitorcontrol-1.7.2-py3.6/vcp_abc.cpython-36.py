# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/monitorcontrol/vcp/vcp_abc.py
# Compiled at: 2019-11-29 22:48:56
# Size of source mod 2**32: 2481 bytes
import abc
from typing import Tuple

class VCPError(IOError):
    __doc__ = ' Raised upon an error reading or writing the VCP. '


class VCP(abc.ABC):

    @abc.abstractmethod
    def open(self):
        """
        Opens the connection to the monitor.

        Raises:
            VCPError: unable to open monitor
        """
        pass

    @abc.abstractmethod
    def close(self):
        """
        Closes the connection to the monitor.

        Raises:
            VCPError: unable to open monitor
        """
        pass

    @abc.abstractmethod
    def set_vcp_feature(self, code: int, value: int):
        """
        Sets the value of a feature on the virtual control panel.

        Args:
            code: feature code
            value: feature value

        Raises:
            VCPError: failed to set VCP feature
        """
        pass

    @abc.abstractmethod
    def get_vcp_feature(self, code: int) -> Tuple[(int, int)]:
        """
        Gets the value of a feature from the virtual control panel.

        Args:
            code: feature code

        Returns:
            current feature value, maximum feature value

        Raises:
            VCPError: failed to get VCP feature
        """
        pass