# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\paps\si\sensorServerClientAdapter.py
# Compiled at: 2016-03-31 05:48:12
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
__author__ = b'd01'
__email__ = b'jungflor@gmail.com'
__copyright__ = b'Copyright (C) 2015-16, Florian JUNG'
__license__ = b'MIT'
__version__ = b'0.1.1'
__date__ = b'2016-03-31'
from flotils.runable import StartStopable
from flotils.logable import Logable
from .sensorInterface import SensorClientInterface
from paps.changeInterface import ChangeInterface

class SensorServerClientAdapter(Logable, ChangeInterface, StartStopable):
    """ Class to connect a plugin directly to a sensor """

    def __init__(self, settings=None):
        """
        Intialize object

        :param settings: Settings for object (default: None)
        :type settings: dict | None
        :rtype: None
        """
        if settings is None:
            settings = {}
        super(SensorServerClientAdapter, self).__init__(settings)
        self.sensor_client = settings[b'sensor_client']
        if not isinstance(self.sensor_client, SensorClientInterface):
            raise TypeError(b"'sensor_client' needs to be of class SensorClientInterface")
        self._on_config = settings.get(b'on_config', None)
        self._original_on_config = self.sensor_client.on_config
        return

    def on_person_new(self, people):
        """
        Add new people

        All people supported need to be added simultaneously,
        since on every call a unjoin() followed by a join() is issued

        :param people: People to add
        :type people: list[paps.people.People]
        :rtype: None
        :raises Exception: On error (for now just an exception)
        """
        try:
            self.on_person_leave([])
        except:
            pass

        try:
            self.sensor_client.join(people)
        except:
            self.exception(b'Failed to join audience')
            raise Exception(b'Joining audience failed')

    def on_person_leave(self, people):
        """
        Remove people from audience

        Does not check which people should leave, but leaves the audience
        all together

        :param people: People to leave - not checked
        :type people: list[paps.people.People]
        :rtype: None
        :raises Exception: On error (for now just an exception)
        """
        try:
            self.sensor_client.unjoin()
        except:
            self.exception(b'Failed to leave audience')
            raise Exception(b'Leaving audience failed')

    def on_person_update(self, people):
        """
        People have changed

        Should always include all people
        (all that were added via on_person_new)

        :param people: People to update
        :type people: list[paps.people.People]
        :rtype: None
        :raises Exception: On error (for now just an exception)
        """
        try:
            self.sensor_client.person_update(people)
        except:
            self.exception(b'Failed to update people')
            raise Exception(b'Updating people failed')

    def on_config(self, settings):
        if callable(self._original_on_config):
            try:
                self._original_on_config(settings)
            except:
                self.exception(b'Failed to update remote config on original')
                raise Exception(b'Original config failed')

        if callable(self._on_config):
            try:
                self._on_config(settings)
            except:
                self.exception(b'Failed to update remote config on local')
                raise Exception(b'Local config failed')

    def start(self, blocking=False):
        self.debug(b'()')
        super(SensorServerClientAdapter, self).start(blocking=False)
        self.sensor_client.start(blocking)

    def stop(self):
        self.debug(b'()')
        self.sensor_client.stop()
        super(SensorServerClientAdapter, self).stop()