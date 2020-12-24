# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/hooks/azure_container_instance_hook.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 7000 bytes
import os
from airflow.hooks.base_hook import BaseHook
from airflow.exceptions import AirflowException
from azure.common.client_factory import get_client_from_auth_file
from azure.common.credentials import ServicePrincipalCredentials
from azure.mgmt.containerinstance import ContainerInstanceManagementClient
from zope.deprecation import deprecation

class AzureContainerInstanceHook(BaseHook):
    __doc__ = "\n    A hook to communicate with Azure Container Instances.\n\n    This hook requires a service principal in order to work.\n    After creating this service principal\n    (Azure Active Directory/App Registrations), you need to fill in the\n    client_id (Application ID) as login, the generated password as password,\n    and tenantId and subscriptionId in the extra's field as a json.\n\n    :param conn_id: connection id of a service principal which will be used\n        to start the container instance\n    :type conn_id: str\n    "

    def __init__(self, conn_id='azure_default'):
        self.conn_id = conn_id
        self.connection = self.get_conn()

    def get_conn(self):
        conn = self.get_connection(self.conn_id)
        key_path = conn.extra_dejson.get('key_path', False)
        if key_path:
            if key_path.endswith('.json'):
                self.log.info('Getting connection using a JSON key file.')
                return get_client_from_auth_file(ContainerInstanceManagementClient, key_path)
            raise AirflowException('Unrecognised extension for key file.')
        if os.environ.get('AZURE_AUTH_LOCATION'):
            key_path = os.environ.get('AZURE_AUTH_LOCATION')
            if key_path.endswith('.json'):
                self.log.info('Getting connection using a JSON key file.')
                return get_client_from_auth_file(ContainerInstanceManagementClient, key_path)
            raise AirflowException('Unrecognised extension for key file.')
        credentials = ServicePrincipalCredentials(client_id=(conn.login),
          secret=(conn.password),
          tenant=(conn.extra_dejson['tenantId']))
        subscription_id = conn.extra_dejson['subscriptionId']
        return ContainerInstanceManagementClient(credentials, str(subscription_id))

    def create_or_update(self, resource_group, name, container_group):
        """
        Create a new container group

        :param resource_group: the name of the resource group
        :type resource_group: str
        :param name: the name of the container group
        :type name: str
        :param container_group: the properties of the container group
        :type container_group: azure.mgmt.containerinstance.models.ContainerGroup
        """
        self.connection.container_groups.create_or_update(resource_group, name, container_group)

    @deprecation.deprecate('get_state_exitcode_details() is deprecated. Related method is get_state()')
    def get_state_exitcode_details(self, resource_group, name):
        """
        Get the state and exitcode of a container group

        :param resource_group: the name of the resource group
        :type resource_group: str
        :param name: the name of the container group
        :type name: str
        :return: A tuple with the state, exitcode, and details.
            If the exitcode is unknown 0 is returned.
        :rtype: tuple(state,exitcode,details)
        """
        cg_state = self.get_state(resource_group, name)
        c_state = cg_state.containers[0].instance_view.current_state
        return (c_state.state, c_state.exit_code, c_state.detail_status)

    @deprecation.deprecate('get_messages() is deprecated. Related method is get_state()')
    def get_messages(self, resource_group, name):
        """
        Get the messages of a container group

        :param resource_group: the name of the resource group
        :type resource_group: str
        :param name: the name of the container group
        :type name: str
        :return: A list of the event messages
        :rtype: list[str]
        """
        cg_state = self.get_state(resource_group, name)
        instance_view = cg_state.containers[0].instance_view
        return [event.message for event in instance_view.events]

    def get_state(self, resource_group, name):
        """
        Get the state of a container group

        :param resource_group: the name of the resource group
        :type resource_group: str
        :param name: the name of the container group
        :type name: str
        :return: ContainerGroup
        :rtype: ~azure.mgmt.containerinstance.models.ContainerGroup
        """
        return self.connection.container_groups.get(resource_group, name,
          raw=False)

    def get_logs(self, resource_group, name, tail=1000):
        """
        Get the tail from logs of a container group

        :param resource_group: the name of the resource group
        :type resource_group: str
        :param name: the name of the container group
        :type name: str
        :param tail: the size of the tail
        :type tail: int
        :return: A list of log messages
        :rtype: list[str]
        """
        logs = self.connection.container.list_logs(resource_group, name, name, tail=tail)
        return logs.content.splitlines(True)

    def delete(self, resource_group, name):
        """
        Delete a container group

        :param resource_group: the name of the resource group
        :type resource_group: str
        :param name: the name of the container group
        :type name: str
        """
        self.connection.container_groups.delete(resource_group, name)

    def exists(self, resource_group, name):
        """
        Test if a container group exists

        :param resource_group: the name of the resource group
        :type resource_group: str
        :param name: the name of the container group
        :type name: str
        """
        for container in self.connection.container_groups.list_by_resource_group(resource_group):
            if container.name == name:
                return True

        return False