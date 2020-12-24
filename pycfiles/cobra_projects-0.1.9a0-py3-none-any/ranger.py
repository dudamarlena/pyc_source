# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/policytool/ranger.py
# Compiled at: 2019-05-23 11:08:11
import requests

class Client:

    def __init__(self, url_prefix, auth=None):
        """
        :param url_prefix: Prefix of the URL to the Ranger API. Example: 'http://ranger.my.org:6080'
        :param auth: If authentication is used. For Kerberos HTTPKerberosAuth(principal="user@MY.REALM")
        """
        self.url_prefix = url_prefix
        self.auth = auth

    def get_service_by_name(self, service_name):
        return requests.get(('{}/service/public/v2/api/service/name/{}').format(self.url_prefix, service_name), auth=self.auth)

    def get_policy_by_name(self, service_name, policy_name):
        response = requests.get(('{}/service/public/v2/api/service/{}/policy/{}').format(self.url_prefix, service_name, policy_name), auth=self.auth)
        return response

    def delete_policy_by_name(self, service_name, policy_name):
        response = requests.delete(('{}/service/public/v2/api/policy').format(self.url_prefix), params={'servicename': service_name, 'policyname': policy_name}, auth=self.auth)
        if response.status_code != 204:
            raise RangerError(("Couldn't delete policy {}.{}: {}").format(service_name, policy_name, response.text), response.status_code)
        return response

    def get_policies_by_name_part(self, service_name, policy_name_part, page_size=50):
        response = requests.get(('{}/service/public/v2/api/policy').format(self.url_prefix), params={'serviceName': service_name, 'policyNamePartial': policy_name_part, 'pageSize': page_size}, auth=self.auth)
        if response.status_code != 200:
            raise RangerError(response.text, response.status_code)
        return response.json()

    def create_policy(self, policy):
        return requests.post(('{}/service/plugins/policies').format(self.url_prefix), json=policy, auth=self.auth)

    def update_policy(self, policy_id, policy):
        url = ('{}/service/plugins/policies/{}').format(self.url_prefix, policy_id)
        return requests.put(url, json=policy, auth=self.auth)

    def apply_policy(self, policy, verbose=0, dryrun=False):
        service_name = policy['service']
        policy_name = policy['name']
        response = self.get_policy_by_name(service_name, policy_name)
        if response.status_code == 200:
            old_policy = response.json()
            policy_id = old_policy['id']
            old_policy.update(policy)
            if not dryrun:
                response = self.update_policy(policy_id, old_policy)
                if response.status_code != 200:
                    raise RangerError(("Couldn't update policy {}.{}: {}").format(service_name, policy_name, response.text), response.status_code)
            else:
                response = {}
            return response
        if response.status_code == 404:
            if not dryrun:
                response = self.create_policy(policy)
                if response.status_code != 200:
                    raise RangerError(("Couldn't create policy {}.{}: {}").format(service_name, policy_name, response.text), response.status_code)
            else:
                response = {}
            return response
        raise RangerError(response.text, response.status_code)


class RangerError(Exception):

    def __init__(self, message, http_code=None):
        self.message = message
        self.http_code = http_code

    def __str__(self):
        return 'HTTP code: ' + repr(self.http_code) + ' Message: ' + repr(self.message)