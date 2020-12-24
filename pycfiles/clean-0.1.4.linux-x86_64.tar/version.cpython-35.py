# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.5/dist-packages/clean/updates/versions/version.py
# Compiled at: 2018-03-25 09:00:51
# Size of source mod 2**32: 364 bytes
"""Version management class."""
from abc import ABCMeta
from abc import abstractmethod

class Version(metaclass=ABCMeta):
    __doc__ = 'Version migrating class.'

    @abstractmethod
    def up(self, config: dict):
        """Upgrade config file."""
        pass

    @abstractmethod
    def down(self, config: dict):
        """Downgrade config file."""
        pass