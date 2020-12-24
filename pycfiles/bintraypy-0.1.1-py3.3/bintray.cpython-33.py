# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bintraypy/bintray.py
# Compiled at: 2016-09-28 11:40:23
# Size of source mod 2**32: 1970 bytes
import os, requests

class Bintray(object):
    default_url = 'https://bintray.com/api/v1'

    def __init__(self, username=None, key=None, url=default_url):
        self.username = username
        self.key = key
        self.url = url

    def upload_generic(self, org, repo, package, version, local_file_path, remote_file_path=None, publish=False, override=False):
        if not remote_file_path:
            remote_file_path = os.path.basename(local_file_path)
        path = 'content/{}/{}/{}/{}/{}'.format(org, repo, package, version, remote_file_path)
        parameters = {}
        if publish:
            parameters['publish'] = '1'
        if override:
            parameters['override'] = '1'
        with open(local_file_path, 'rb') as (file):
            print('Uploading file {} to {}'.format(local_file_path, path))
            response = self._Bintray__create_request('put', path, params=parameters, data=file)
            if response.status_code != 201:
                raise Exception('Failed to upload file: {0}\n{1}'.format(response.status_code, response.text))
        print('Uploaded successfully')

    def create_package(self, org, repo, name, licenses, vcs_url, description=None):
        path = 'packages/{}/{}'.format(org, repo)
        parameters = {'name': name, 
         'licenses': licenses, 
         'vcs_url': vcs_url}
        if description:
            parameters['description'] = description
        print('Creating package {} in {}'.format(name, path))
        response = self._Bintray__create_request('post', path, params=parameters)
        if response.status_code != 201:
            raise Exception('Failed to create package: {0}\n{1}'.format(response.status_code, response.text))
        print('Created package successfully')

    def __create_request(self, method, path, **kwargs):
        url = '{}/{}'.format(self.url, path)
        if self.username and self.key:
            return requests.request(method, url, auth=(self.username, self.key), **kwargs)
        else:
            return requests.request(method, url, **kwargs)


def _bool_to_int(b):
    if b:
        return 1
    return 0