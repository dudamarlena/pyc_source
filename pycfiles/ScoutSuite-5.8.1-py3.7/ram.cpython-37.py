# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ScoutSuite/providers/aliyun/facade/ram.py
# Compiled at: 2020-04-02 05:37:10
# Size of source mod 2**32: 7572 bytes
from ScoutSuite.providers.aliyun.authentication_strategy import AliyunCredentials
from ScoutSuite.providers.aliyun.facade.utils import get_response
from ScoutSuite.providers.aliyun.utils import get_client
from ScoutSuite.core.console import print_exception
from aliyunsdkram.request.v20150501 import ListUsersRequest, GetUserRequest, GetUserMFAInfoRequest, ListAccessKeysRequest, GetAccessKeyLastUsedRequest, GetPasswordPolicyRequest, GetSecurityPreferenceRequest, ListGroupsRequest, ListUsersForGroupRequest, ListRolesRequest, ListPoliciesRequest, GetPolicyVersionRequest, ListEntitiesForPolicyRequest

class RAMFacade:

    def __init__(self, credentials: AliyunCredentials):
        self._credentials = credentials
        self._client = get_client(credentials=(self._credentials))

    async def get_users(self):
        """
        Get all users

        :return: a list of all users
        """
        response = await get_response(client=(self._client), request=(ListUsersRequest.ListUsersRequest()))
        if response:
            return response['Users']['User']
        return []

    async def get_user_details(self, username):
        """
        Get additional details for a user

        :param username: The username of the user
        :return: a dict with the user's details
        """
        request = GetUserRequest.GetUserRequest()
        request.set_UserName(username)
        response = await get_response(client=(self._client), request=request)
        if response:
            return response['User']
        return []

    async def get_user_api_keys(self, username):
        """
        Get API keys for a user

        :param username: The username of the user
        :return: the list of API keys for that user
        """
        request = ListAccessKeysRequest.ListAccessKeysRequest()
        request.set_UserName(username)
        response = await get_response(client=(self._client), request=request)
        if response:
            return response['AccessKeys']['AccessKey']
        return []

    async def get_user_api_key_last_usage(self, username, key_id):
        """
        Get last usage date for an API key

        :param username: The username of the user
        :param key_id: The API key id
        :return: the list of API keys for that user
        """
        request = GetAccessKeyLastUsedRequest.GetAccessKeyLastUsedRequest()
        request.set_UserName(username)
        request.set_UserAccessKeyId(key_id)
        response = await get_response(client=(self._client), request=request)
        if response:
            return response['AccessKeyLastUsed']['LastUsedDate']
        return []

    async def get_user_mfa_status(self, username):
        """
        Check if user has MFA configured

        :param username: The username of the user
        :return: status and MFA serial number
        """
        request = GetUserMFAInfoRequest.GetUserMFAInfoRequest()
        request.set_UserName(username)
        try:
            response = await get_response(client=(self._client), request=request)
        except Exception as e:
            try:
                if e.error_code == 'EntityNotExist.User.MFADevice':
                    return (False, None)
                print_exception('Unable to get MFA status for user {}: {}'.format(username, e))
                return (False, None)
            finally:
                e = None
                del e

        else:
            return (
             True, response['MFADevice']['SerialNumber'])

    async def get_password_policy(self):
        """
        Get the account's password policy

        :return: the password policy
        """
        request = GetPasswordPolicyRequest.GetPasswordPolicyRequest()
        response = await get_response(client=(self._client), request=request)
        if response:
            return response['PasswordPolicy']
        return []

    async def get_security_policy(self):
        """
        Get the account's security policy

        :return: the security policy
        """
        request = GetSecurityPreferenceRequest.GetSecurityPreferenceRequest()
        response = await get_response(client=(self._client), request=request)
        if response:
            return response['SecurityPreference']
        return []

    async def get_groups(self):
        """
        Get all groups

        :return: a list of all groups
        """
        response = await get_response(client=(self._client), request=(ListGroupsRequest.ListGroupsRequest()))
        if response:
            return response['Groups']['Group']
        return []

    async def get_group_users(self, group_name):
        """
        Get all users in a group

        :return: a list of users in groups
        """
        request = ListUsersForGroupRequest.ListUsersForGroupRequest()
        request.set_GroupName(group_name)
        response = await get_response(client=(self._client), request=request)
        if response:
            return response['Users']['User']
        return []

    async def get_roles(self):
        """
        Get all roles

        :return: a list of all roles
        """
        response = await get_response(client=(self._client), request=(ListRolesRequest.ListRolesRequest()))
        if response:
            return response['Roles']['Role']
        return []

    async def get_policies(self):
        """
        Get all custom policies

        :return: a list of all custom policies
        """
        response = await get_response(client=(self._client), request=(ListPoliciesRequest.ListPoliciesRequest()))
        if response:
            return response['Policies']['Policy']
        return []

    async def get_policy_version(self, name, type, version):
        """
        Get all policies

        :return: a list of all policies
        """
        request = GetPolicyVersionRequest.GetPolicyVersionRequest()
        request.set_PolicyName(name)
        request.set_PolicyType(type)
        request.set_VersionId(version)
        response = await get_response(client=(self._client), request=request)
        if response:
            return response['PolicyVersion']
        return []

    async def get_policy_entities(self, name, type):
        """
        Get all entities for a policy

        :return: a dict of all policy entities
        """
        request = ListEntitiesForPolicyRequest.ListEntitiesForPolicyRequest()
        request.set_PolicyName(name)
        request.set_PolicyType(type)
        response = await get_response(client=(self._client), request=request)
        if response:
            response.pop('RequestId')
            return response
        return []