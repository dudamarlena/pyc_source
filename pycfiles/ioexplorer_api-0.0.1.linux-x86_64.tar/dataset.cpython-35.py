# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.5/dist-packages/ioexplorer_api/dataset.py
# Compiled at: 2018-02-28 17:10:47
# Size of source mod 2**32: 649 bytes
import requests
from ioexplorer_api import API_URL
import os
from datetime import datetime

class Dataset(object):

    def __init__(self, name, keywords, description):
        self.name = name
        self.keywords = keywords
        self.description = description

    def create(self):
        endpoint = os.path.join(API_URL, 'datasets', 'dataset')
        data = {'name': self.name, 
         'keywords': self.keywords, 
         'description': self.description}
        r = requests.post(endpoint, json=data)
        if r.status_code == 201:
            return r.text
        raise Exception(r.text)