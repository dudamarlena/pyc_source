# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/d/Sandbox/huru-server/.venv/lib/python2.7/site-packages/data_importer/core/descriptor.py
# Compiled at: 2020-04-17 10:46:24
from __future__ import unicode_literals
import os
from data_importer.core.exceptions import InvalidModel, InvalidDescriptor
try:
    import json
except ImportError:
    import simplejson as json

class ReadDescriptor(object):

    def __init__(self, file_name=None, model_name=None):
        self.file_name = file_name
        self.model_name = model_name
        self.source = None
        self.read_file()
        return

    def read_file(self):
        """Read json file"""
        if not os.path.exists(self.file_name):
            raise InvalidDescriptor(b'Invalid JSON File Source')
        read_file = open(self.file_name, b'r')
        self.source = json.loads(read_file.read())

    def get_model(self):
        """Read model from JSON descriptor"""
        valid_model = [ i for i in self.source if self.model_name in i.get(b'model') ]
        if not valid_model:
            raise InvalidModel(b'Model Name does not exist in descriptor')
        return valid_model[0]

    def get_fields(self):
        """Get content"""
        model = self.get_model()
        fields = model.get(b'fields')
        if isinstance(fields, dict):
            fields = fields.keys()
        return fields