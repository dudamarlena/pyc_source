# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyowm/abstractions/owm.py
# Compiled at: 2018-12-21 14:52:45
# Size of source mod 2**32: 1555 bytes
__doc__ = '\nModule containing the abstract PyOWM library main entry point interface\n'
from abc import ABCMeta, abstractmethod

class OWM(object):
    """OWM"""
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_API_key(self):
        """
        Returns the OWM API key

        :returns: the OWM API key string

        """
        raise NotImplementedError

    @abstractmethod
    def set_API_key(self, API_key):
        """
        Updates the OWM API key

        :param API_key: the new value for the OWM API key
        :type API_key: str

        """
        raise NotImplementedError

    @abstractmethod
    def get_API_version(self):
        """
        Returns the currently supported OWM Weather API version

        :returns: the OWM Weather API version string

        """
        raise NotImplementedError

    @abstractmethod
    def get_version(self):
        """
        Returns the current version of the PyOWM library

        :returns: the current PyOWM library version string

        """
        raise NotImplementedError

    @abstractmethod
    def is_API_online(self):
        """
        Returns ``True`` if the OWM Weather API is currently online. A short
        timeout is used to determine API service availability.

        :returns: bool

        """
        raise NotImplementedError