# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/apps/project.py
# Compiled at: 2010-06-15 15:31:36
"""
An apps sdk project.
"""
import json, os

class Project(object):

    def __init__(self, path):
        self.path = path
        self.read_metadata()

    def read_metadata(self):
        try:
            self.metadata = json.load(open(os.path.join(self.path, 'package.json'), 'r'))
        except IOError, err:
            self.metadata = {'name': self.path, 
               'version': '0.1', 
               'description': 'The default project.', 
               'site': 'http://apps.bittorrent.com', 
               'author': 'Default Author <default@example.com>', 
               'keywords': [
                          'example'], 
               'bt:publisher': 'Example Publisher', 
               'bt:update_url': 'http://localhost/example', 
               'bt:release_date': '00/00/0000', 
               'bt:description': 'This is the example app.', 
               'bt:libs': [
                         {'name': 'apps-sdk', 'url': 'http://staging.apps.bittorrent.com/pkgs/apps-sdk.pkg'}]}