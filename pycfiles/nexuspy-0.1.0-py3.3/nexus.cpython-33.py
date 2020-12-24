# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nexuspy/nexus.py
# Compiled at: 2016-12-20 07:07:57
# Size of source mod 2**32: 1484 bytes
import os, requests

class Nexus(object):
    upload_path = 'service/local/artifact/maven/content'

    def __init__(self, url, username=None, password=None):
        self.url = url
        self.username = username
        self.password = password

    def upload_artifact(self, filePath, repository, groupId, artifactId, version, packaging=None, classifier=None):
        if not self.username or not self.password:
            raise Exception('Username or password was not set, cannot upload artifacts')
        if not packaging:
            packaging = os.path.splitext(filePath)[1][1:]
        parameters = {'r': repository, 
         'hasPom': 'false', 
         'g': groupId, 
         'a': artifactId, 
         'v': version, 
         'p': packaging, 
         'e': packaging}
        if classifier:
            parameters['c'] = classifier
        with open(filePath, 'rb') as (file):
            remotePath = '{}/content/repositories/{}/{}/{}/{}/{}-{}{}.{}'.format(self.url, repository, groupId, artifactId, version, artifactId, version, '-{}'.format(classifier) if classifier else '', packaging)
            print('Uploading file {} to {}'.format(filePath, remotePath))
            response = requests.post('{}/{}'.format(self.url, Nexus.upload_path), auth=(self.username, self.password), data=parameters, files={'file': file})
            if response.status_code != 201:
                raise Exception('Failed to upload file: {0}\n{1}'.format(response.status_code, response.text))
        print('Uploaded successfully')