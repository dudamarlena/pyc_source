# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\cloud_training\abstract_command.py
# Compiled at: 2017-10-29 22:00:18
# Size of source mod 2**32: 935 bytes
from abc import ABC, abstractmethod
from argparse import Namespace
from cloud_training import configure

class AbstractCommand(ABC):
    __doc__ = 'Abstract class for implementing a command'

    def __init__(self, args: Namespace):
        """Command's constructor

        Args:
            args: arguments provided by argparse.

        Raises:
            ValueError: If command's arguments can't be processed.

        """
        self._args = args
        self._settings = configure.get_all_settings(self._args.profile)

    @abstractmethod
    def run(self) -> bool:
        """Performs a command

        Returns:
            bool: True for success, False otherwise.

        Raises:
            ValueError: If command's arguments can't be processed.
        """
        return True

    def _print(self, message):
        """Print results to the console."""
        print(message, flush=True)