# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ctyfoxylos/SBP/python/towerlib/towerlib/entities/credential.py
# Compiled at: 2019-10-18 06:12:55
# Size of source mod 2**32: 15252 bytes
"""
Main code for credentials.

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""
import importlib, logging
from towerlib.towerlibexceptions import InvalidOrganization, InvalidValue, InvalidCredentialType
from .core import Entity, EntityManager, validate_max_length
__author__ = 'Costas Tyfoxylos <ctyfoxylos@schubergphilis.com>'
__docformat__ = 'google'
__date__ = '2018-01-03'
__copyright__ = 'Copyright 2018, Costas Tyfoxylos'
__credits__ = ['Costas Tyfoxylos']
__license__ = 'MIT'
__maintainer__ = 'Costas Tyfoxylos'
__email__ = '<ctyfoxylos@schubergphilis.com>'
__status__ = 'Development'
LOGGER_BASENAME = 'credentials'
LOGGER = logging.getLogger(LOGGER_BASENAME)
LOGGER.addHandler(logging.NullHandler())

class CredentialType(Entity):
    __doc__ = 'Models the credential_type entity of ansible tower.'

    def __init__(self, tower_instance, data):
        Entity.__init__(self, tower_instance, data)

    @property
    def name(self):
        """The name of the credential type.

        Returns:
            string: The name of the credential type.

        """
        return self._data.get('name')

    @name.setter
    def name(self, value):
        """Update the name of the credential type.

        Returns:
            None:

        """
        max_characters = 512
        conditions = [validate_max_length(value, max_characters)]
        if all(conditions):
            self._update_values('name', value)
        else:
            raise InvalidValue('{value} is invalid. Condition max_characters must be less or equal {max_characters}'.format(value=value,
              max_characters=max_characters))

    @property
    def description(self):
        """The description of the credential type.

        Returns:
            string: The description of the credential type.

        """
        return self._data.get('description')

    @description.setter
    def description(self, value):
        """Set the description of the credential type.

        Returns:
            None.

        """
        self._update_values('description', value)

    @property
    def kind(self):
        """The kind of the credential type.

        Accepted values are : (u'scm', u'ssh', u'vault', u'net', u'cloud', u'insights').

        Returns:
            string: The kind of the credential type.

        """
        return self._data.get('kind')

    @property
    def managed_by_tower(self):
        """Flag indicating whether the credential is internal to tower.

        Returns:
            bool: True if credential is internal to tower, False if it is user created.

        """
        return self._data.get('managed_by_tower')

    @property
    def inputs(self):
        """The inputs of the credential type.

        Returns:
            dictionary: A structure of the credential type supported inputs.

        """
        return self._data.get('inputs')

    @inputs.setter
    def inputs(self, value):
        """Update the inputs of the credential type.

        Returns:
            None:

        """
        if isinstance(value, dict):
            self._update_values('inputs', value)
        else:
            raise InvalidValue('Value is not valid dictionary received: {value}'.format(value=value))

    @property
    def injectors(self):
        """The injectors of the credential type.

        Returns:
            dictionary: A structure of the credential type supported injectors.

        """
        return self._data.get('injectors')

    @injectors.setter
    def injectors(self, value):
        """Update the injectors of the credential type.

        Returns:
            None:

        """
        if isinstance(value, dict):
            self._update_values('injectors', value)
        else:
            raise InvalidValue('Value is not valid dictionary received: {value}'.format(value=value))


class Credential:
    __doc__ = 'Credential factory to handle the different credential types returned.'

    def __new__(cls, tower_instance, data):
        try:
            credential_type_name = tower_instance.get_credential_type_by_id(data.get('credential_type')).name
            credential_type_name = ''.join(credential_type_name.split())
            credential_type = '{credential_type}Credential'.format(credential_type=credential_type_name)
            CredentialType_ = getattr(importlib.import_module('towerlib.entities.credential'), credential_type)
            credential = CredentialType_(tower_instance, data)
        except Exception:
            LOGGER.warning('Could not dynamically load credential with type : "%s", trying a generic one.', credential_type)
            credential = GenericCredential(tower_instance, data)

        return credential


class GenericCredential(Entity):
    __doc__ = 'Models the credential entity of ansible tower.'

    def __init__(self, tower_instance, data):
        Entity.__init__(self, tower_instance, data)
        self._object_roles = None

    @property
    def host(self):
        """The host of the credential.

        Returns:
            dictionary: The host structure of the credential.

        """
        return self._data.get('summary_fields', {}).get('host')

    @property
    def project(self):
        """The project of the credential.

        Returns:
            dictionary: The project structure of the credential.

        """
        return self._data.get('summary_fields', {}).get('project')

    @property
    def created_by(self):
        """The user that created the credential.

        Returns:
            User: The user that created the credential.

        """
        url = self._data.get('related', {}).get('created_by')
        return self._tower._get_object_by_url('User', url)

    @property
    def modified_by(self):
        """The person that modified the credential last.

        Returns:
            User: The user that modified the credential in tower last.

        """
        url = self._data.get('related', {}).get('modified_by')
        return self._tower._get_object_by_url('User', url)

    @property
    def object_roles(self):
        """The object roles.

        Returns:
            EntityManager: EntityManager of the object roles supported.

        """
        if not self._object_roles:
            url = self._data.get('related', {}).get('object_roles')
            self._object_roles = EntityManager((self._tower), entity_object='ObjectRole',
              primary_match_field='name',
              url=url)
        return self._object_roles

    @property
    def owner_users(self):
        """The owners of the credential.

        Returns:
            EntityManager: EntityManager of the users that are owners.

        """
        url = self._data.get('related', {}).get('owner_users')
        return EntityManager((self._tower), entity_object='User',
          primary_match_field='username',
          url=url)

    @property
    def owner_teams(self):
        """The owner teams of the credential.

        Returns:
            EntityManager: EntityManager of the teams that are owners.

        """
        url = self._data.get('related', {}).get('owner_teams')
        return EntityManager((self._tower), entity_object='Team',
          primary_match_field='name',
          url=url)

    @property
    def name(self):
        """The name of the credential.

        Returns:
            string: The name of the credential.

        """
        return self._data.get('name')

    @name.setter
    def name(self, value):
        """Update the name of the credential.

        Returns:
            None:

        """
        max_characters = 512
        conditions = [validate_max_length(value, max_characters)]
        if all(conditions):
            self._update_values('name', value)
        else:
            raise InvalidValue('{value} is invalid. Condition max_characters must be less or equal to {max_characters}'.format(value=value,
              max_characters=max_characters))

    @property
    def description(self):
        """The description of the credential.

        Returns:
            string: The description of the credential.

        """
        return self._data.get('description')

    @description.setter
    def description(self, value):
        """Set the description of the credential.

        Returns:
            None.

        """
        self._update_values('description', value)

    @property
    def organization(self):
        """The organization the credential is part of.

        Returns:
            Organization: The organization the credential is part of.

        """
        return self._tower.get_organization_by_id(self._data.get('organization'))

    @organization.setter
    def organization(self, value):
        """Set the organization of the credential.

        Returns:
            None.

        """
        organization = self._tower.get_organization_by_name(value)
        if not organization:
            raise InvalidOrganization(value)
        self._update_values('organization', organization.id)

    @property
    def credential_type(self):
        """The type of the credential.

        Returns:
            CredentialType: The type of the credential.

        """
        return self._tower.get_credential_type_by_id(self._data.get('credential_type'))

    @credential_type.setter
    def credential_type(self, value):
        """Set the credential_type of the credential.

        Returns:
            None.

        """
        credential_type = self._tower.get_credential_type_by_name(value)
        if not credential_type:
            raise InvalidCredentialType(value)
        self._update_values('credential_type', credential_type.id)

    @property
    def inputs(self):
        """The inputs of the credential.

        Returns:
            dictionary: A structure of the credential supported inputs.

        """
        return self._data.get('inputs')

    @inputs.setter
    def inputs(self, value):
        """Update the inputs of the credential.

        Returns:
            None:

        """
        if isinstance(value, dict):
            self._update_values('inputs', value)
        else:
            raise InvalidValue('Value is not valid json received: {value}'.format(value=value))


class MachineCredential(GenericCredential):
    __doc__ = 'Models the machine credential.'

    def __init__(self, tower_instance, data):
        GenericCredential.__init__(self, tower_instance, data)

    @property
    def username(self):
        """The username that is set in the credential.

        Returns:
            basestring: The username that is set in the credential.

        """
        return self._data.get('inputs', {}).get('username')

    @username.setter
    def username(self, value):
        """Set the username of the credential.

        Returns:
            None.

        """
        self._update_values('username', value, parent_attribute='inputs')

    @property
    def password(self):
        """The password that is set in the credential.

        Returns:
            basestring: The password that is set in the credential.

        """
        return self._data.get('inputs', {}).get('password')

    @password.setter
    def password(self, value):
        """Set the password of the credential.

        Returns:
            None.

        """
        self._update_values('password', value, parent_attribute='inputs')


class HashicorpVaultCredential(GenericCredential):
    __doc__ = 'Models the hashicorp vault credential.'

    def __init__(self, tower_instance, data):
        GenericCredential.__init__(self, tower_instance, data)

    @property
    def token(self):
        """The token that is set in the credential.

        Returns:
            basestring: The token that is set in the credential.

        """
        return self._data.get('inputs', {}).get('hashi_vault_token')

    @token.setter
    def token(self, value):
        """Set the token of the credential.

        Returns:
            None.

        """
        self._update_values('hashi_vault_token', value, parent_attribute='inputs')

    @property
    def vault_address(self):
        """The vault address that is set in the credential.

        Returns:
            basestring: The vault address that is set in the credential.

        """
        return self._data.get('inputs', {}).get('hashi_vault_addr')

    @vault_address.setter
    def vault_address(self, value):
        """Set the password of the credential.

        Returns:
            None.

        """
        self._update_values('hashi_vault_addr', value, parent_attribute='inputs')

    @property
    def ca_host_verify(self):
        """The ca host verify setting that is set in the credential.

        Returns:
            basestring: The vault address that is set in the credential.

        """
        return self._data.get('inputs', {}).get('hashi_vault_pre_python_279_cahostverify')

    @ca_host_verify.setter
    def ca_host_verify(self, value):
        """Set the ca host verify of the credential.

        Returns:
            None.

        """
        if value.lower() not in ('no', 'yes'):
            raise ValueError('Value should be either no/yes')
        self._update_values('hashi_vault_pre_python_279_cahostverify', value, parent_attribute='inputs')