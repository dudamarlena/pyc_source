# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ctyfoxylos/SBP/python/towerlib/towerlib/entities/core.py
# Compiled at: 2019-10-18 06:12:55
# Size of source mod 2**32: 13700 bytes
"""
Main code for miscellaneous.

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""
import logging, re, json
from collections import namedtuple
from dateutil.parser import parse
from cachetools import TTLCache, cached
__author__ = 'Costas Tyfoxylos <ctyfoxylos@schubergphilis.com>'
__docformat__ = 'google'
__date__ = '2018-01-03'
__copyright__ = 'Copyright 2018, Costas Tyfoxylos'
__credits__ = ['Costas Tyfoxylos']
__license__ = 'MIT'
__maintainer__ = 'Costas Tyfoxylos'
__email__ = '<ctyfoxylos@schubergphilis.com>'
__status__ = 'Development'
LOGGER_BASENAME = 'core'
LOGGER = logging.getLogger(LOGGER_BASENAME)
LOGGER.addHandler(logging.NullHandler())
USER_LEVELS = ('standard', 'system_auditor', 'system_administrator')
VALID_CREDENTIAL_TYPES = ('net', 'cloud')
JOB_TYPES = ('run', 'check')
VERBOSITY_LEVELS = (0, 1, 2, 3, 4)
Config = namedtuple('Config', ['eula',
 'license_info',
 'analytics_status',
 'version',
 'project_base_dir',
 'time_zone',
 'ansible_version',
 'project_local_paths'])
LicenseInfo = namedtuple('LicenseInfo', ['subscription_name',
 'valid_key',
 'features',
 'date_expired',
 'available_instances',
 'hostname',
 'free_instances',
 'instance_count',
 'time_remaining',
 'compliant',
 'grace_period_remaining',
 'trial',
 'company_name',
 'date_warning',
 'license_type',
 'license_key',
 'license_date',
 'deployment_id',
 'current_instances'])
LicenseFeatures = namedtuple('LicenseFeatures', ['surveys',
 'multiple_organizations',
 'workflows',
 'system_tracking',
 'enterprise_auth',
 'rebranding',
 'activity_streams',
 'ldap',
 'ha'])
Cluster = namedtuple('InstanceGroups', ['instances',
 'capacity',
 'name',
 'ha_enabled',
 'version',
 'active_node'])
INSTANCE_STATE_CACHING_SECONDS = 60
INSTANCE_STATE_CACHE = TTLCache(maxsize=1, ttl=INSTANCE_STATE_CACHING_SECONDS)

def validate_max_length(value, max_length):
    """Validates the maximum length of a value."""
    return len(value) <= max_length


def validate_characters(value, alpha=True, numbers=True, extra_chars=None):
    """Validates the string groups of a value."""
    alphas = 'a-zA-Z' if alpha else ''
    nums = '0-9' if numbers else ''
    extra_characters = re.escape(extra_chars) if extra_chars else ''
    valid_characters = '^[{alphas}{nums}{extra_characters}]+$'.format(alphas=alphas, nums=nums,
      extra_characters=extra_characters)
    if re.search(valid_characters, value):
        return True
    return False


def validate_range(value, start, stop):
    """Validates that a value is within a range."""
    return start <= value <= stop


def validate_json(value):
    """Validates that the provided value is a valid json."""
    try:
        json.loads(value)
        return True
    except ValueError:
        return False


class DateParserMixin:
    __doc__ = 'Implements a string to datetime parsing to be inherited by all needed objects.'

    @staticmethod
    def _to_datetime(field):
        try:
            date_ = parse(field)
        except (ValueError, TypeError):
            date_ = None

        return date_


class ClusterInstance(DateParserMixin):
    __doc__ = 'Models the instance of a node as part of the cluster.'

    def __init__(self, tower_instance, name, hearbeat):
        self._tower = tower_instance
        self.name = name
        self._heartbeat = hearbeat
        self._instance_data = self._get_instance_data()

    @cached(INSTANCE_STATE_CACHE)
    def _get_instance_data(self):
        url = '{api}/instances/'.format(api=(self._tower.api))
        results = self._tower.session.get(url)
        result_json = results.json()
        return next((instance for instance in result_json.get('results', []) if instance.get('hostname') == self.name), {})

    @property
    def heartbeat(self):
        """Datetime object of when the last heartbeat was recorded."""
        try:
            date_ = parse(self._heartbeat)
        except (ValueError, TypeError):
            date_ = None

        return date_

    @property
    def id(self):
        """The id of the node."""
        return self._instance_data.get('id')

    @property
    def uuid(self):
        """The uuid of the node."""
        return self._instance_data.get('uuid')

    @property
    def hostname(self):
        """The hostname of the node."""
        return self._instance_data.get('hostname')

    @property
    def version(self):
        """The version of tower on the node."""
        return self._instance_data.get('version')

    @property
    def capacity(self):
        """The capacity of the node."""
        return self._instance_data.get('capacity')

    @property
    def consumed_capacity(self):
        """The consumed capacity."""
        return self._instance_data.get('consumed_capacity')

    @property
    def percent_capacity_remaining(self):
        """The percentage of remaining capacity."""
        return self._instance_data.get('percent_capacity_remaining')

    @property
    def jobs_running(self):
        """The number of running jobs."""
        return self._instance_data.get('jobs_running')

    @property
    def created_at(self):
        """The date and time the entity was created in tower.

        Returns:
            datetime: The datetime object of the date and time of the creation of the object.
            None: If there is no entry for the creation.

        """
        self._to_datetime(self._instance_data.get('created'))

    @property
    def modified_at(self):
        """The date and time the entity was modified in tower.

        Returns:
            datetime: The datetime object of the date and time of the modification of the object.
            None: If there is no entry for the modification.

        """
        self._to_datetime(self._instance_data.get('modified'))


class Entity(DateParserMixin):
    __doc__ = 'The basic object that holds common responses across all entities.'

    def __init__(self, tower_instance, data):
        logger_name = '{base}.{suffix}'.format(base=LOGGER_BASENAME, suffix=(self.__class__.__name__))
        self._logger = logging.getLogger(logger_name)
        self._tower = tower_instance
        self._data = data

    @property
    def id(self):
        """The id of the object.

        Returns:
            int: The number of the internal id of the object in tower.

        """
        return self._data.get('id')

    @property
    def type(self):
        """The type of the object.

        Returns:
            string: The name of the type of the object in tower.

        """
        return self._data.get('type')

    @property
    def url(self):
        """The url of the object.

        Returns:
            string: The full url of the representation of the object in tower.

        """
        return self._tower.host + self._data.get('url')

    @property
    def api_url(self):
        """The api url of the object.

        Returns:
            string: The relative url of the representation of the object in tower.

        """
        return self._data.get('url')

    @property
    def created_at(self):
        """The date and time the entity was created in tower.

        Returns:
            datetime: The datetime object of the date and time of the creation of the object.
            None: If there is no entry for the creation.

        """
        return self._to_datetime(self._data.get('created'))

    @property
    def modified_at(self):
        """The date and time the entity was modified in tower.

        Returns:
            datetime: The datetime object of the date and time of the modification of the object.
            None: If there is no entry for the modification.

        """
        return self._to_datetime(self._data.get('modified'))

    def delete(self):
        """Deletes the entity from tower.

        Returns:
            bool: True on success, False otherwise.

        """
        response = self._tower.session.delete(self.url)
        if not response.ok:
            self._logger.error('Error deleting, response was: "%s"', response.text)
        return response.ok

    def _update_values(self, attribute, value, parent_attribute=None):
        payload = {parent_attribute: {attribute: value}} if parent_attribute else {attribute: value}
        response = self._tower.session.patch((self.url), json=payload)
        if response.ok:
            self._data.update(response.json())
        else:
            self._logger.error('Error updating variables, response was: %s', response.text)

    def _refresh_state(self):
        response = self._tower.session.get(self.url)
        if response.ok:
            self._data.update(response.json())
        else:
            self._logger.error('Error getting updated state, response was: %s', response.text)


class EntityManager:
    __doc__ = 'Manages entities by making them act like iterables but also implements contains and other useful stuff.'

    def __init__(self, tower_instance, entity_object, primary_match_field, entity_name=None, url=None):
        if not any([entity_name, url]):
            raise ValueError('Either entity_name or url needs to be provided, received none.')
        else:
            self._tower = tower_instance
            self._object_type = entity_object
            self._primary_match_field = primary_match_field
            self._name = entity_name
            self._next_state = None
            if entity_name:
                self._url = '{api}/{entity_name}'.format(api=(self._tower.api), entity_name=entity_name)
            else:
                self._url = '{host}{url}'.format(host=(self._tower.host), url=url)

    @property
    def _objects(self):
        return self._get_entity_objects()

    def _get_entity_objects(self, params=None):
        module = __import__('towerlib.entities')
        entity_object = getattr(module, self._object_type)
        for data in self._tower._get_paginated_response((self._url), params=params):
            yield entity_object(self._tower, data)

    def __iter__(self):
        return self._objects

    def __contains__(self, value):
        return next(self.filter({self._primary_match_field: value}), False)

    def filter(self, params):
        """Implements filtering based on the filtering capabilities of tower.

        Args:
            params: Dictionary of filters to be passed to the api.

        Returns:
              Generator of the objects retrieved based on the filtering.
        https://docs.ansible.com/ansible-tower/latest/html/towerapi/filtering.html.

        """
        return self._get_entity_objects(params)