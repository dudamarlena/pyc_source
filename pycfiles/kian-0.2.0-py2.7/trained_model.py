# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/kian/trained_model.py
# Compiled at: 2015-09-03 14:20:58
import json, os, codecs
from kian.parser import ModelWithData

class TrainedModel(ModelWithData):
    """docstring for TrainedModel"""

    def __init__(self, *args, **kwargs):
        super(TrainedModel, self).__init__(*args, **kwargs)
        file_path = os.path.join(self.data_directory, 'categories.json')
        if not os.path.isfile(file_path):
            raise ValueError('You should train the model first')
        file_path = os.path.join(self.data_directory, 'theta.dat')
        if not os.path.isfile(file_path):
            raise ValueError('You should train the model first')

    def load_categories(self):
        file_path = os.path.join(self.data_directory, 'categories.json')
        with codecs.open(file_path, 'r', 'utf-8') as (f):
            self.categories = json.loads(f.read())

    def load_theta(self):
        file_path = os.path.join(self.data_directory, 'theta.dat')
        with codecs.open(file_path, 'r', 'utf-8') as (f):
            self.theta = eval(f.read())

    def load(self):
        self.load_categories()
        self.load_theta()