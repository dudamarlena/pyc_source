# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\paps\si\sensorInterface.py
# Compiled at: 2016-03-31 04:41:30
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
__author__ = b'd01'
__email__ = b'jungflor@gmail.com'
__copyright__ = b'Copyright (C) 2015-16, Florian JUNG'
__license__ = b'MIT'
__version__ = b'0.1.0'
__date__ = b'2016-03-29'
from abc import ABCMeta, abstractmethod
from flotils.logable import Logable
from flotils.runable import StartStopable, StartException
from ..changeInterface import ChangeInterface
from ..papsException import PapsException

class SensorException(PapsException):
    """ Base class for all exceptions of a sensor interface class """
    pass


class SensorStartException(SensorException, StartException):
    """ Failed to start """
    pass


class SensorJoinException(SensorException):
    """ Failed to join audience """
    pass


class SensorUpdateException(SensorException):
    """ Failed to update """
    pass


class SensorServerInterface(Logable, StartStopable):
    """ Interface for sensor servers """
    __metaclass__ = ABCMeta

    def __init__(self, settings=None):
        """
        Initialize object

        :param settings: Settings for object (default: None)
        :type settings: dict | None
        :rtype: None
        """
        if settings is None:
            settings = {}
        super(SensorServerInterface, self).__init__(settings)
        self.changer = settings[b'changer']
        if not isinstance(self.changer, ChangeInterface):
            raise TypeError(b'Expected changer to be of ChangeInterface')
        return


class SensorClientInterface(Logable, StartStopable):
    """ Interface for sensor clients """
    __metaclass__ = ABCMeta

    def __init__(self, settings=None):
        """
        Initialize object

        :param settings: Settings for object (default: None)
        :type settings: dict | None
        :rtype: None
        """
        if settings is None:
            settings = {}
        super(SensorClientInterface, self).__init__(settings)
        self.on_config = settings.get(b'on_config', None)
        return

    @abstractmethod
    def join(self, people):
        """
        Join the local audience
        (a config message should be received on success)
        Validates that there are people to join and that each of them
        has a valid unique id

        :param people: Which people does this sensor have
        :type people: list[paps.person.Person]
        :rtype: None
        :raises SensorJoinException: Failed to join
        """
        raise NotImplementedError(b'Please implement')

    @abstractmethod
    def unjoin(self):
        """
        Leave the local audience

        :rtype: None
        :raises SensorJoinException: Failed to leave
        """
        raise NotImplementedError(b'Please implement')

    @abstractmethod
    def person_update(self, people):
        """
        Update the status of people

        :param people: All people of this sensor
        :type people: list[paps.person.Person]
        :rtype: None
        :raises SensorUpdateException: Failed to update
        """
        raise NotImplementedError(b'Please implement')

    @abstractmethod
    def config(self, settings):
        """
        Configuration has changed - config this module and lower layers
        (calls on_config - if set)

        :param settings: New configuration
        :type settings: dict
        :rtype: None
        :raises SensorUpdateException: Failed to update
        """
        raise NotImplementedError(b'Please implement')