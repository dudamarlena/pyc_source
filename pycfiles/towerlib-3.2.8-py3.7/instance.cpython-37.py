# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ctyfoxylos/SBP/python/towerlib/towerlib/entities/instance.py
# Compiled at: 2019-10-18 06:12:55
# Size of source mod 2**32: 5798 bytes
"""
Main code for instances.

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""
import logging
from .core import Entity, EntityManager
__author__ = 'Costas Tyfoxylos <ctyfoxylos@schubergphilis.com>'
__docformat__ = 'google'
__date__ = '2018-01-03'
__copyright__ = 'Copyright 2018, Costas Tyfoxylos'
__credits__ = ['Costas Tyfoxylos']
__license__ = 'MIT'
__maintainer__ = 'Costas Tyfoxylos'
__email__ = '<ctyfoxylos@schubergphilis.com>'
__status__ = 'Development'
LOGGER_BASENAME = 'instances'
LOGGER = logging.getLogger(LOGGER_BASENAME)
LOGGER.addHandler(logging.NullHandler())

class Instance(Entity):
    __doc__ = 'Models the instance entity of ansible tower.'

    def __init__(self, tower_instance, data):
        Entity.__init__(self, tower_instance, data)

    @property
    def uuid(self):
        """The uuid of the instance.

        Returns:
            string: The uuid of the instance.

        """
        return self._data.get('uuid')

    @property
    def hostname(self):
        """The hostname of the instance.

        Returns:
            string: The hostname of the instance.

        """
        return self._data.get('hostname')

    @property
    def version(self):
        """The version of the instance.

        Returns:
            string: The version of the instance.

        """
        return self._data.get('version')

    @property
    def capacity(self):
        """Not really sure what this is.

        Returns:
            integer:

        """
        return self._data.get('capacity')

    @property
    def consumed_capacity(self):
        """Not really sure what this is.

        Returns:
            integer:

        """
        return self._data.get('consumed_capacity')

    @property
    def percent_capacity_remaining(self):
        """Not really sure what this is.

        Returns:
            integer:

        """
        return self._data.get('percent_capacity_remaining')

    @property
    def jobs_running_count(self):
        """The number of running jobs.

        Returns:
            integer: The number of running jobs.

        """
        return self._data.get('jobs_running')

    @property
    def jobs(self):
        """The jobs of the instance.

        Returns:
            EntityManager: EntityManager of the jobs of the instance.

        """
        url = self._data.get('related', {}).get('jobs')
        return EntityManager((self._tower), entity_object='Job',
          primary_match_field='name',
          url=url)


class InstanceGroup(Entity):
    __doc__ = 'Models the instance_group entity of ansible tower.'

    def __init__(self, tower_instance, data):
        Entity.__init__(self, tower_instance, data)

    @property
    def name(self):
        """The name of the instance group.

        Returns:
            string: The name of the instance group.

        """
        return self._data.get('name')

    @property
    def capacity(self):
        """Not really sure what this is.

        Returns:
            integer:

        """
        return self._data.get('capacity')

    @property
    def consumed_capacity(self):
        """Not really sure what this is.

        Returns:
            integer:

        """
        return self._data.get('consumed_capacity')

    @property
    def percent_capacity_remaining(self):
        """Not really sure what this is.

        Returns:
            integer:

        """
        return self._data.get('percent_capacity_remaining')

    @property
    def jobs_running_count(self):
        """The number of running jobs.

        Returns:
            integer: The number of running jobs.

        """
        return self._data.get('jobs_running')

    @property
    def instances_count(self):
        """The number of instances.

        Returns:
            integer: The number of instances.

        """
        return self._data.get('instances')

    @property
    def instances(self):
        """The instances of the instance group.

        Returns:
            list of Instances: The instances of the instance group.

        """
        url = self._data.get('related', {}).get('instances')
        return self._tower._get_object_by_url('Instance', url)

    @property
    def controller(self):
        """Not really sure what this is.

        Returns:
            None.

        """
        return self._data.get('controller')