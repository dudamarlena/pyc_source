# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dj/workspace/dyson-py/lib/dyson/utils/dataloader.py
# Compiled at: 2016-11-15 01:16:27
# Size of source mod 2**32: 931 bytes
import json, yaml
from six import string_types
from dyson.vars.parsing import parse_jinja

class DataLoader:

    def __init__(self):
        self._basedir = '.'

    def load(self, data):
        """
        Creates a python data structure from the data which can be
        JSON or YAML
        :param data:
        :return:
        """
        try:
            the_data = json.loads(data)
        except:
            the_data = yaml.load(data)

        return the_data

    def load_file(self, data_file):
        """
        Loads a JSON/YAML file
        :param data_file: the file to load
        :return: DataLoader
        """
        datum = None
        try:
            with open(data_file, 'r') as (stream):
                the_data = json.loads(stream)
        except:
            with open(data_file, 'r') as (stream):
                the_data = yaml.load(stream)

        return the_data