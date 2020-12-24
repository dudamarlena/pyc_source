# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: F:\GitCode\trangevi-azurecli\azure\cli\command_modules\ml\_mma\operations\mms_ops.py
# Compiled at: 2017-09-20 13:50:34
from msrest.pipeline import ClientRawResponse
import uuid
from .. import models

class ModelManagementAccountsOperations(object):
    """ModelManagementAccountsOperations operations.

    :param client: Client for service requests.
    :param config: Configuration of service client.
    :param serializer: An object model serializer.
    :param deserializer: An objec model deserializer.
    :ivar api_version: The version of the Microsoft.MachineLearning resource provider API to use. Constant value: "2017-09-01-preview".
    """

    def __init__(self, client, config, serializer, deserializer):
        self._client = client
        self._serialize = serializer
        self._deserialize = deserializer
        self.api_version = '2017-09-01-preview'
        self.config = config

    def create_or_update(self, resource_group_name, model_management_account_name, parameters, custom_headers=None, raw=False, **operation_config):
        """Create or update a Model Management Account. This call will overwrite
        an existing Model Management Account. Note that there is no warning or
        confirmation. This is a nonrecoverable operation. If your intent is to
        create a new Model Management Account, call the Get operation first to
        verify that it does not exist.

        :param resource_group_name: Name of the resource group in which the
         Model Management Account is located.
        :type resource_group_name: str
        :param model_management_account_name: The name of the Model Management
         Account.
        :type model_management_account_name: str
        :param parameters: The payload that is used to create or update the
         Model Management Account.
        :type parameters: :class:`ModelManagementAccount
         <modelmanagementaccounts.models.ModelManagementAccount>`
        :param dict custom_headers: headers that will be added to the request
        :param bool raw: returns the direct response alongside the
         deserialized response
        :param operation_config: :ref:`Operation configuration
         overrides<msrest:optionsforoperations>`.
        :rtype: :class:`ModelManagementAccount
         <modelmanagementaccounts.models.ModelManagementAccount>`
        :rtype: :class:`ClientRawResponse<msrest.pipeline.ClientRawResponse>`
         if raw=true
        :raises:
         :class:`ErrorResponseException<modelmanagementaccounts.models.ErrorResponseException>`
        """
        url = '/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.MachineLearningModelManagement/accounts/{modelManagementAccountName}'
        path_format_arguments = {'resourceGroupName': self._serialize.url('resource_group_name', resource_group_name, 'str'), 
           'modelManagementAccountName': self._serialize.url('model_management_account_name', model_management_account_name, 'str'), 
           'subscriptionId': self._serialize.url('self.config.subscription_id', self.config.subscription_id, 'str')}
        url = self._client.format_url(url, **path_format_arguments)
        query_parameters = {}
        query_parameters['api-version'] = self._serialize.query('self.api_version', self.api_version, 'str')
        header_parameters = {}
        header_parameters['Content-Type'] = 'application/json; charset=utf-8'
        if self.config.generate_client_request_id:
            header_parameters['x-ms-client-request-id'] = str(uuid.uuid1())
        if custom_headers:
            header_parameters.update(custom_headers)
        if self.config.accept_language is not None:
            header_parameters['accept-language'] = self._serialize.header('self.config.accept_language', self.config.accept_language, 'str')
        body_content = self._serialize.body(parameters, 'ModelManagementAccount')
        request = self._client.put(url, query_parameters)
        response = self._client.send(request, header_parameters, body_content, **operation_config)
        if response.status_code not in (200, 201):
            raise models.ErrorResponseException(self._deserialize, response)
        deserialized = None
        if response.status_code == 200:
            deserialized = self._deserialize('ModelManagementAccount', response)
        if response.status_code == 201:
            deserialized = self._deserialize('ModelManagementAccount', response)
        if raw:
            client_raw_response = ClientRawResponse(deserialized, response)
            return client_raw_response
        else:
            return deserialized

    def get(self, resource_group_name, model_management_account_name, custom_headers=None, raw=False, **operation_config):
        """Gets the Model Management Account Definiton as specified by a
        subscription, resource group, and name.

        :param resource_group_name: Name of the resource group in which the
         Model Management Account is located.
        :type resource_group_name: str
        :param model_management_account_name: The name of the Model Management
         Account.
        :type model_management_account_name: str
        :param dict custom_headers: headers that will be added to the request
        :param bool raw: returns the direct response alongside the
         deserialized response
        :param operation_config: :ref:`Operation configuration
         overrides<msrest:optionsforoperations>`.
        :rtype: :class:`ModelManagementAccount
         <modelmanagementaccounts.models.ModelManagementAccount>`
        :rtype: :class:`ClientRawResponse<msrest.pipeline.ClientRawResponse>`
         if raw=true
        :raises:
         :class:`ErrorResponseException<modelmanagementaccounts.models.ErrorResponseException>`
        """
        url = '/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.MachineLearningModelManagement/accounts/{modelManagementAccountName}'
        path_format_arguments = {'resourceGroupName': self._serialize.url('resource_group_name', resource_group_name, 'str'), 
           'modelManagementAccountName': self._serialize.url('model_management_account_name', model_management_account_name, 'str'), 
           'subscriptionId': self._serialize.url('self.config.subscription_id', self.config.subscription_id, 'str')}
        url = self._client.format_url(url, **path_format_arguments)
        query_parameters = {}
        query_parameters['api-version'] = self._serialize.query('self.api_version', self.api_version, 'str')
        header_parameters = {}
        header_parameters['Content-Type'] = 'application/json; charset=utf-8'
        if self.config.generate_client_request_id:
            header_parameters['x-ms-client-request-id'] = str(uuid.uuid1())
        if custom_headers:
            header_parameters.update(custom_headers)
        if self.config.accept_language is not None:
            header_parameters['accept-language'] = self._serialize.header('self.config.accept_language', self.config.accept_language, 'str')
        request = self._client.get(url, query_parameters)
        response = self._client.send(request, header_parameters, **operation_config)
        if response.status_code not in (200, ):
            raise models.ErrorResponseException(self._deserialize, response)
        deserialized = None
        if response.status_code == 200:
            deserialized = self._deserialize('ModelManagementAccount', response)
        if raw:
            client_raw_response = ClientRawResponse(deserialized, response)
            return client_raw_response
        else:
            return deserialized

    def update(self, resource_group_name, model_management_account_name, payload, custom_headers=None, raw=False, **operation_config):
        """Modifies an existing Model Management Account resource.

        :param resource_group_name: Name of the resource group in which the
         Model Management Account is located.
        :type resource_group_name: str
        :param model_management_account_name: The name of the Model Management
         Account.
        :type model_management_account_name: str
        :param payload: The payload to use to patch the Model Management
         Account.
        :type payload: :class:`ModelManagementAccountUpdateProperties
         <modelmanagementaccounts.models.ModelManagementAccountUpdateProperties>`
        :param dict custom_headers: headers that will be added to the request
        :param bool raw: returns the direct response alongside the
         deserialized response
        :param operation_config: :ref:`Operation configuration
         overrides<msrest:optionsforoperations>`.
        :rtype: :class:`ModelManagementAccount
         <modelmanagementaccounts.models.ModelManagementAccount>`
        :rtype: :class:`ClientRawResponse<msrest.pipeline.ClientRawResponse>`
         if raw=true
        :raises:
         :class:`ErrorResponseException<modelmanagementaccounts.models.ErrorResponseException>`
        """
        url = '/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.MachineLearningModelManagement/accounts/{modelManagementAccountName}'
        path_format_arguments = {'resourceGroupName': self._serialize.url('resource_group_name', resource_group_name, 'str'), 
           'modelManagementAccountName': self._serialize.url('model_management_account_name', model_management_account_name, 'str'), 
           'subscriptionId': self._serialize.url('self.config.subscription_id', self.config.subscription_id, 'str')}
        url = self._client.format_url(url, **path_format_arguments)
        query_parameters = {}
        query_parameters['api-version'] = self._serialize.query('self.api_version', self.api_version, 'str')
        header_parameters = {}
        header_parameters['Content-Type'] = 'application/json; charset=utf-8'
        if self.config.generate_client_request_id:
            header_parameters['x-ms-client-request-id'] = str(uuid.uuid1())
        if custom_headers:
            header_parameters.update(custom_headers)
        if self.config.accept_language is not None:
            header_parameters['accept-language'] = self._serialize.header('self.config.accept_language', self.config.accept_language, 'str')
        body_content = self._serialize.body(payload, 'ModelManagementAccountUpdateProperties')
        request = self._client.patch(url, query_parameters)
        response = self._client.send(request, header_parameters, body_content, **operation_config)
        if response.status_code not in (200, ):
            raise models.ErrorResponseException(self._deserialize, response)
        deserialized = None
        if response.status_code == 200:
            deserialized = self._deserialize('ModelManagementAccount', response)
        if raw:
            client_raw_response = ClientRawResponse(deserialized, response)
            return client_raw_response
        else:
            return deserialized

    def delete(self, resource_group_name, model_management_account_name, custom_headers=None, raw=False, **operation_config):
        """Deletes the specified Model Management Account.

        :param resource_group_name: Name of the resource group in which the
         Model Management Account is located.
        :type resource_group_name: str
        :param model_management_account_name: The name of the Model Management
         Account.
        :type model_management_account_name: str
        :param dict custom_headers: headers that will be added to the request
        :param bool raw: returns the direct response alongside the
         deserialized response
        :param operation_config: :ref:`Operation configuration
         overrides<msrest:optionsforoperations>`.
        :rtype: None
        :rtype: :class:`ClientRawResponse<msrest.pipeline.ClientRawResponse>`
         if raw=true
        :raises:
         :class:`ErrorResponseException<modelmanagementaccounts.models.ErrorResponseException>`
        """
        url = '/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.MachineLearningModelManagement/accounts/{modelManagementAccountName}'
        path_format_arguments = {'resourceGroupName': self._serialize.url('resource_group_name', resource_group_name, 'str'), 
           'modelManagementAccountName': self._serialize.url('model_management_account_name', model_management_account_name, 'str'), 
           'subscriptionId': self._serialize.url('self.config.subscription_id', self.config.subscription_id, 'str')}
        url = self._client.format_url(url, **path_format_arguments)
        query_parameters = {}
        query_parameters['api-version'] = self._serialize.query('self.api_version', self.api_version, 'str')
        header_parameters = {}
        header_parameters['Content-Type'] = 'application/json; charset=utf-8'
        if self.config.generate_client_request_id:
            header_parameters['x-ms-client-request-id'] = str(uuid.uuid1())
        if custom_headers:
            header_parameters.update(custom_headers)
        if self.config.accept_language is not None:
            header_parameters['accept-language'] = self._serialize.header('self.config.accept_language', self.config.accept_language, 'str')
        request = self._client.delete(url, query_parameters)
        response = self._client.send(request, header_parameters, **operation_config)
        if response.status_code not in (200, 204):
            raise models.ErrorResponseException(self._deserialize, response)
        if raw:
            client_raw_response = ClientRawResponse(None, response)
            return client_raw_response
        else:
            return

    def list_by_resource_group(self, resource_group_name, skiptoken=None, custom_headers=None, raw=False, **operation_config):
        """Gets the Model Management Accounts in the specified resource group.

        :param resource_group_name: Name of the resource group in which the
         Model Management Account is located.
        :type resource_group_name: str
        :param skiptoken: Continuation token for pagination.
        :type skiptoken: str
        :param dict custom_headers: headers that will be added to the request
        :param bool raw: returns the direct response alongside the
         deserialized response
        :param operation_config: :ref:`Operation configuration
         overrides<msrest:optionsforoperations>`.
        :rtype: :class:`ModelManagementAccountPaged
         <modelmanagementaccounts.models.ModelManagementAccountPaged>`
        :raises:
         :class:`ErrorResponseException<modelmanagementaccounts.models.ErrorResponseException>`
        """

        def internal_paging(next_link=None, raw=False):
            if not next_link:
                url = '/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.MachineLearningModelManagement/accounts'
                path_format_arguments = {'resourceGroupName': self._serialize.url('resource_group_name', resource_group_name, 'str'), 
                   'subscriptionId': self._serialize.url('self.config.subscription_id', self.config.subscription_id, 'str')}
                url = self._client.format_url(url, **path_format_arguments)
                query_parameters = {}
                if skiptoken is not None:
                    query_parameters['$skiptoken'] = self._serialize.query('skiptoken', skiptoken, 'str')
                query_parameters['api-version'] = self._serialize.query('self.api_version', self.api_version, 'str')
            else:
                url = next_link
                query_parameters = {}
            header_parameters = {}
            header_parameters['Content-Type'] = 'application/json; charset=utf-8'
            if self.config.generate_client_request_id:
                header_parameters['x-ms-client-request-id'] = str(uuid.uuid1())
            if custom_headers:
                header_parameters.update(custom_headers)
            if self.config.accept_language is not None:
                header_parameters['accept-language'] = self._serialize.header('self.config.accept_language', self.config.accept_language, 'str')
            request = self._client.get(url, query_parameters)
            response = self._client.send(request, header_parameters, **operation_config)
            if response.status_code not in (200, ):
                raise models.ErrorResponseException(self._deserialize, response)
            return response

        deserialized = models.ModelManagementAccountPaged(internal_paging, self._deserialize.dependencies)
        if raw:
            header_dict = {}
            client_raw_response = models.ModelManagementAccountPaged(internal_paging, self._deserialize.dependencies, header_dict)
            return client_raw_response
        else:
            return deserialized

    def list_by_subscription_id(self, skiptoken=None, custom_headers=None, raw=False, **operation_config):
        """Gets the Model Management Accounts in the specified subscription.

        :param skiptoken: Continuation token for pagination.
        :type skiptoken: str
        :param dict custom_headers: headers that will be added to the request
        :param bool raw: returns the direct response alongside the
         deserialized response
        :param operation_config: :ref:`Operation configuration
         overrides<msrest:optionsforoperations>`.
        :rtype: :class:`ModelManagementAccountPaged
         <modelmanagementaccounts.models.ModelManagementAccountPaged>`
        :raises:
         :class:`ErrorResponseException<modelmanagementaccounts.models.ErrorResponseException>`
        """

        def internal_paging(next_link=None, raw=False):
            if not next_link:
                url = '/subscriptions/{subscriptionId}/providers/Microsoft.MachineLearningModelManagement/accounts'
                path_format_arguments = {'subscriptionId': self._serialize.url('self.config.subscription_id', self.config.subscription_id, 'str')}
                url = self._client.format_url(url, **path_format_arguments)
                query_parameters = {}
                if skiptoken is not None:
                    query_parameters['$skiptoken'] = self._serialize.query('skiptoken', skiptoken, 'str')
                query_parameters['api-version'] = self._serialize.query('self.api_version', self.api_version, 'str')
            else:
                url = next_link
                query_parameters = {}
            header_parameters = {}
            header_parameters['Content-Type'] = 'application/json; charset=utf-8'
            if self.config.generate_client_request_id:
                header_parameters['x-ms-client-request-id'] = str(uuid.uuid1())
            if custom_headers:
                header_parameters.update(custom_headers)
            if self.config.accept_language is not None:
                header_parameters['accept-language'] = self._serialize.header('self.config.accept_language', self.config.accept_language, 'str')
            request = self._client.get(url, query_parameters)
            response = self._client.send(request, header_parameters, **operation_config)
            if response.status_code not in (200, ):
                raise models.ErrorResponseException(self._deserialize, response)
            return response

        deserialized = models.ModelManagementAccountPaged(internal_paging, self._deserialize.dependencies)
        if raw:
            header_dict = {}
            client_raw_response = models.ModelManagementAccountPaged(internal_paging, self._deserialize.dependencies, header_dict)
            return client_raw_response
        else:
            return deserialized

    def list_available_operations(self, custom_headers=None, raw=False, **operation_config):
        """Gets all available operations.

        :param dict custom_headers: headers that will be added to the request
        :param bool raw: returns the direct response alongside the
         deserialized response
        :param operation_config: :ref:`Operation configuration
         overrides<msrest:optionsforoperations>`.
        :rtype: :class:`AvailableOperations
         <modelmanagementaccounts.models.AvailableOperations>`
        :rtype: :class:`ClientRawResponse<msrest.pipeline.ClientRawResponse>`
         if raw=true
        :raises:
         :class:`ErrorResponseException<modelmanagementaccounts.models.ErrorResponseException>`
        """
        url = '/providers/Microsoft.MachineLearningModelManagement/operations'
        query_parameters = {}
        query_parameters['api-version'] = self._serialize.query('self.api_version', self.api_version, 'str')
        header_parameters = {}
        header_parameters['Content-Type'] = 'application/json; charset=utf-8'
        if self.config.generate_client_request_id:
            header_parameters['x-ms-client-request-id'] = str(uuid.uuid1())
        if custom_headers:
            header_parameters.update(custom_headers)
        if self.config.accept_language is not None:
            header_parameters['accept-language'] = self._serialize.header('self.config.accept_language', self.config.accept_language, 'str')
        request = self._client.get(url, query_parameters)
        response = self._client.send(request, header_parameters, **operation_config)
        if response.status_code not in (200, ):
            raise models.ErrorResponseException(self._deserialize, response)
        deserialized = None
        if response.status_code == 200:
            deserialized = self._deserialize('AvailableOperations', response)
        if raw:
            client_raw_response = ClientRawResponse(deserialized, response)
            return client_raw_response
        else:
            return deserialized