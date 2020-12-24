# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jovyan/libpysal/examples/locals.py
# Compiled at: 2019-12-06 15:21:49
# Size of source mod 2**32: 1844 bytes
"""
Handle local datasets
"""
import os
from bs4 import BeautifulSoup
import requests
from .base import PYSALDATA, Example, get_list_of_files, get_data_home
datasets = {}
dirs = [
 '10740', 'arcgis', 'baltim', 'berlin', 'book', 'burkitt', 'calemp',
 'chicago', 'clearwater', 'columbus', 'desmith', 'geodanet', 'georgia',
 'juvenile', 'Line', 'mexico', 'networks', 'newHaven', 'Point', 'Polygon',
 'Polygon_Holes', 'sids2', 'snow_maps', 'stl', 'street_net_pts', 'tests',
 'tokyo', 'us_income', 'virginia', 'wmat']

class LocalExample:
    __doc__ = '\n    Builtin pysal example\n    '

    def __init__(self, name, dirname):
        self.name = name
        self.dirname = dirname
        self.installed = True

    def get_description(self):
        pass

    def get_file_list(self):
        return get_list_of_files(self.dirname)

    def get_path(self, file_name):
        """
        get path for local file
        """
        file_list = self.get_file_list()
        for file_path in file_list:
            base_name = os.path.basename(file_path)
            if file_name == base_name:
                return file_path

        print('{} is not a file in this example'.format(file_name))

    def explain(self):
        """
        Provide a description of the example
        """
        description = [f for f in self.get_file_list() if 'README.md' in f][0]
        with open(description, 'r') as (f):
            print(f.read())


builtin_root = os.path.dirname(__file__)
paths = [os.path.join(builtin_root, local) for local in dirs]
paths = zip(dirs, paths)
datasets = {}
for name, pth in paths:
    files = get_list_of_files(pth)
    file_names = [os.path.basename(file) for file in files]
    if 'README.md' in file_names:
        example = LocalExample(name, pth)
        datasets[name] = example