# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python3.5/dist-packages/clean/updates/versions/version.py
# Compiled at: 2018-03-25 09:00:51
# Size of source mod 2**32: 364 bytes
__doc__ = 'Version management class.'
from abc import ABCMeta
from abc import abstractmethod

class Version(metaclass=ABCMeta):
    """Version"""

    @abstractmethod
    def up(self, config: dict):
        """Upgrade config file."""
        pass

    @abstractmethod
    def down(self, config: dict):
        """Downgrade config file."""
        pass