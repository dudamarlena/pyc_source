# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ghawker/code/python/oktalib/oktalib/entities/core.py
# Compiled at: 2020-01-10 08:33:33
# Size of source mod 2**32: 3989 bytes
"""
Main code for core.

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""
import logging
from dateutil.parser import parse
__author__ = 'Costas Tyfoxylos <ctyfoxylos@schubergphilis.com>'
__docformat__ = 'google'
__date__ = '2018-01-08'
__copyright__ = 'Copyright 2018, Costas Tyfoxylos'
__credits__ = ['Costas Tyfoxylos']
__license__ = 'MIT'
__maintainer__ = 'Costas Tyfoxylos'
__email__ = '<ctyfoxylos@schubergphilis.com>'
__status__ = 'Development'
LOGGER_BASENAME = 'core'
LOGGER = logging.getLogger(LOGGER_BASENAME)
LOGGER.addHandler(logging.NullHandler())

class Entity:
    __doc__ = 'The core object of okta.'

    def __init__(self, okta_instance, data):
        logger_name = '{base}.{suffix}'.format(base=LOGGER_BASENAME, suffix=(self.__class__.__name__))
        self._logger = logging.getLogger(logger_name)
        self._okta = okta_instance
        self._data = self._parse_data(data)

    def _parse_data(self, data):
        if not isinstance(data, dict):
            self._logger.error('Invalid data received :{}'.format(data))
            data = {}
        return data

    @property
    def url(self):
        """The url of the entity.

        Returns:
             None in the core entity.

        All objects inheriting from this would either expose this from their data or construct
        and overwrite this.

        """
        pass

    @property
    def id(self):
        """The id of the entity.

        Returns:
            basestring: The internal id of the entity

        """
        return self._data.get('id')

    @property
    def created_at(self):
        """The date and time of the group's creation.

        Returns:
            datetime: The datetime object of when the group was created

        """
        return self._get_date_from_key('created')

    @property
    def last_updated_at(self):
        """The date and time of the entity's last update.

        Returns:
            datetime: The datetime object of when the entity was last updated

        """
        return self._get_date_from_key('lastUpdated')

    def _get_date_from_key(self, name):
        try:
            date_ = parse(self._data.get(name))
        except (ValueError, TypeError):
            date_ = None

        return date_

    def _update(self):
        response = self._okta.session.get(self.url)
        if not response.ok:
            self._logger.error('Error getting entities data. Response :{}'.format(response.text))
            return False
        self._data = response.json()
        return True