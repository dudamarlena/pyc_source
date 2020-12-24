# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\paps\crowd\controller.py
# Compiled at: 2016-03-31 05:22:49
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
import threading
from .pluginInterface import Plugin, PluginStartException
from paps.person import Person

class CrowdController(Plugin):
    """
    Manages the audience state and the plugins
    """

    def __init__(self, settings=None):
        """
        Initialize object

        :param settings: Settings to be passed to init (default: None)
        :type settings: dict | None
        :rtype: None
        :raises ValueError: No plugins given
        """
        if settings is None:
            settings = {}
        super(CrowdController, self).__init__(settings)
        self.plugins = settings.get(b'plugins')
        if not self.plugins:
            raise ValueError(b'No plugins registered')
        self._people = {}
        self._people_lock = threading.Lock()
        return

    def on_person_new(self, people):
        """
        New people joined the audience

        :param people: People that just joined the audience
        :type people: list[paps.person.Person]
        :rtype: None
        """
        self.debug(b'()')
        changed = []
        with self._people_lock:
            for p in people:
                person = Person.from_person(p)
                if person.id in self._people:
                    self.warning((b'{} already in audience').format(person.id))
                self._people[person.id] = person
                changed.append(person)

        for plugin in self.plugins:
            try:
                plugin.on_person_new(changed)
            except:
                self.exception((b'Failed to send new people to {}').format(plugin.name))

    def on_person_leave(self, people):
        """
        People left the audience

        :param people: People that left
        :type people: list[paps.person.Person]
        :rtype: None
        """
        self.debug(b'()')
        changed = []
        with self._people_lock:
            for p in people:
                person = Person.from_person(p)
                if person.id not in self._people:
                    self.warning((b'{} not in audience').format(person.id))
                else:
                    del self._people[person.id]
                changed.append(person)

        for plugin in self.plugins:
            try:
                plugin.on_person_leave(changed)
            except:
                self.exception((b'Failed to send leaving people to {}').format(plugin.name))

    def on_person_update(self, people):
        """
        People have changed (e.g. a sensor value)

        :param people: People whos state changed (may include unchanged)
        :type people: list[paps.person.Person]
        :rtype: None
        """
        self.debug(b'()')
        changed = []
        with self._people_lock:
            for p in people:
                person = Person.from_person(p)
                if person.id not in self._people:
                    self.warning((b'{} not in audience').format(person.id))
                self._people[person.id] = person
                changed.append(person)

        for plugin in self.plugins:
            try:
                plugin.on_person_update(changed)
            except:
                self.exception((b'Failed to send updated people to {}').format(plugin.name))

    @property
    def people(self):
        """
        Get people of current audience

        :return: Current people
        :rtype: list[paps.people.People]
        """
        with self._people_lock:
            return self._people.values()

    def start(self, blocking=False):
        """
        Start the interface

        :param blocking: Should the call block until stop() is called
            (default: False)
        :type blocking: bool
        :rtype: None
        """
        self.debug(b'()')
        for plugin in self.plugins:
            try:
                plugin.controller = self
                plugin.start(blocking=False)
            except:
                self.exception((b'Failed to start plugin {}').format(plugin.name))
                raise PluginStartException(b'Starting one or more plugins failed')

        super(CrowdController, self).start(blocking=blocking)

    def stop(self):
        """
        Stop the interface

        :rtype: None
        """
        self.debug(b'()')
        for plugin in self.plugins:
            try:
                plugin.stop()
            except:
                self.exception((b'Failed to stop plugin {}').format(plugin.name))

        super(CrowdController, self).stop()