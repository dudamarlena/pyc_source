# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ctyfoxylos/SBP/python/towerlib/towerlib/entities/host.py
# Compiled at: 2018-09-27 06:07:59
"""
Main code for host

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""
import logging, json
from towerlib.towerlibexceptions import InvalidGroup
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
LOGGER_BASENAME = 'host'
LOGGER = logging.getLogger(LOGGER_BASENAME)
LOGGER.addHandler(logging.NullHandler())

class Host(Entity):
    """Models the host entity of ansible tower"""

    def __init__(self, tower_instance, data):
        Entity.__init__(self, tower_instance, data)
        self._payload = ['name',
         'description',
         'enabled',
         'instance_id',
         'variables']

    @property
    def name(self):
        """The name of the host

        Returns:
            string: The name of the host

        """
        return self._data.get('name')

    @name.setter
    def name(self, value):
        """Update the name on the host"

        Returns:
            None:

        """
        self._update_values('name', value)

    @property
    def description(self):
        """The description of the host

        Returns:
            string: The description of the host

        """
        return self._data.get('description')

    @description.setter
    def description(self, value):
        """Update the description on the host"

        Returns:
            None:

        """
        self._update_values('description', value)

    @property
    def inventory(self):
        """The inventory that the host is part of

        Returns:
            Inventory: The inventory that the host is part of

        """
        return self._tower.get_inventory_by_id(self._data.get('inventory'))

    @property
    def enabled(self):
        """Flag about whether the host is enabled in tower

        Returns:
            bool: True if the host is enabled, False otherwise

        """
        return self._data.get('enabled')

    @enabled.setter
    def enabled(self, value):
        """Update the enabled status of the host"

        Returns:
            None:

        """
        self._update_values('enabled', value)

    @property
    def instance_id(self):
        """Not sure what this is

        Returns:
            string:

        """
        return self._data.get('instance_id')

    @property
    def variables(self):
        """The variables set on the host

        Returns:
            string: A string of the variables set on the host usually in yaml format.

        """
        return self._data.get('variables')

    @variables.setter
    def variables(self, value):
        """Update the variables on the host"

        Returns:
            None:

        """
        self._update_values('variables', value)

    def _update_values(self, attribute, value):
        url = ('{api}/hosts/{id}/').format(api=self._tower.api, id=self.id)
        payload = {attribute:self._data.get(attribute) for attribute in self._payload}
        payload[attribute] = json.dumps(value)
        response = self._tower.session.put(url, data=json.dumps(payload))
        if response.ok:
            self._data.update(response.json())
        else:
            self._logger.error('Error updating variables, response was: %s', response.text)

    @property
    def has_active_failures(self):
        """Flag about whether the host has active failures

        Returns:
            bool: True if the host has active failures, False otherwise

        """
        return self._data.get('has_active_failures')

    @property
    def has_inventory_sources(self):
        """Flag about whether the host has inventory sources

        Returns:
            bool: True if the host has inventory sources, False otherwise

        """
        return self._data.get('has_inventory_sources')

    @property
    def last_job(self):
        """The id of the last job

        Returns:
            integer: The id of the last job

        """
        return self._data.get('last_job')

    @property
    def last_job_host_summary(self):
        """The id of the last job summary

        Returns:
            integer: The id of the last job summary

        """
        return self._data.get('last_job_host_summary')

    @property
    def insights_system_id(self):
        """Not sure what this is

        Returns:
            None

        """
        return self._data.get('insights_system_id')

    @property
    def created_by(self):
        """The user that created the host

        Returns:
            User: The user that created the host

        """
        url = self._data.get('related', {}).get('created_by')
        return self._tower._get_object_by_url('User', url)

    @property
    def modified_by(self):
        """The person that modified the host last

        Returns:
            User: The user that modified the host in tower last

        """
        url = self._data.get('related', {}).get('modified_by')
        return self._tower._get_object_by_url('User', url)

    @property
    def groups(self):
        """The groups that the host is part of

        Returns:
            EntityManager: EntityManager of the groups of the host

        """
        url = self._data.get('related', {}).get('groups')
        return EntityManager(self._tower, entity_object='Group', primary_match_field='name', url=url)

    @property
    def recent_jobs(self):
        """The most recent jobs run on the host

        Returns:
            list if dict: The most recent jobs run on the host

        """
        return self._data.get('summary_fields', {}).get('recent_jobs')

    def associate_with_groups(self, groups):
        """Associate the host with the provided groups

        Args:
            groups: The groups to associate the host with.
            Accepts a single group string or a list or tuple of groups

        Returns:
            bool: True on complete success, False otherwise

        Raises:
            InvalidGroup: The group provided as argument does not exist.

        """
        if not isinstance(groups, (list, tuple)):
            groups = [
             groups]
        inventory_groups = [ group_ for group_ in self.inventory.groups ]
        inventory_group_names = [ group.name for group in inventory_groups ]
        for group_name in groups:
            if group_name not in inventory_group_names:
                raise InvalidGroup(group_name)

        final_groups = [ group for group in inventory_groups if group.name.lower() in groups
                       ]
        return all([ group._add_host_by_id(self.id) for group in final_groups
                   ])

    def disassociate_with_groups(self, groups):
        """Disassociate the host from the provided groups

        Args:
            groups: The group name(s) to disassociate the host from.
            Accepts a single group string or a list or tuple of groups

        Returns:
            bool: True on complete success, False otherwise

        Raises:
            InvalidGroup: The group provided as argument does not exist.

        """
        if not isinstance(groups, (list, tuple)):
            groups = [
             groups]
        groups = [ group.lower() for group in groups ]
        host_group_names = [ group.name.lower() for group in self.groups ]
        for group_name in groups:
            if group_name.lower() not in host_group_names:
                raise InvalidGroup(group_name)

        inventory_groups = [ group for group in self.inventory.groups if group.name.lower() in groups
                           ]
        return all([ group._remove_host_by_id(self.id) for group in inventory_groups
                   ])