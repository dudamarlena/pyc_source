# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\paps\changeInterface.py
# Compiled at: 2016-03-31 03:40:20
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

class ChangeInterface(object):
    """ Interface supports person changed """
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
        super(ChangeInterface, self).__init__()
        return

    @abstractmethod
    def on_person_new(self, people):
        """
        New people joined the audience

        :param people: People that just joined the audience
        :type people: list[paps.person.Person]
        :rtype: None
        """
        raise NotImplementedError(b'Please implement')

    @abstractmethod
    def on_person_update(self, people):
        """
        People have changed (e.g. a sensor value)

        :param people: People whos state changed (may include unchanged)
        :type people: list[paps.person.Person]
        :rtype: None
        """
        raise NotImplementedError(b'Please implement')

    @abstractmethod
    def on_person_leave(self, people):
        """
        People left the audience

        :param people: People that left
        :type people: list[paps.person.Person]
        :rtype: None
        """
        raise NotImplementedError(b'Please implement')