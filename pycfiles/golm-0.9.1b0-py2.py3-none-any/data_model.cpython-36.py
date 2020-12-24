# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/prihodad/Documents/projects/visitor/golm/golm/core/nlp/data_model.py
# Compiled at: 2018-04-15 14:00:29
# Size of source mod 2**32: 1345 bytes
import json, os
from django.db import models
strategies = [
 'trait', 'keywords']
languages = ['en', 'cz']

class Entity:
    name = models.CharField(max_length=100)
    strategy = models.CharField(max_length=100, choices=strategies)
    stemming = models.BooleanField(default=False)
    language = models.CharField(max_length=10, choices=languages, default='en')
    threshold = models.FloatField(default=0.7)

    @staticmethod
    def fromFile(path):
        with open(path) as (f):
            data = json.load(f)
        filename = os.path.split(path)[(-1)]
        name, ext = os.path.splitext(filename)
        e = Entity()
        e.name = name
        e.strategy = data['strategy']
        e.stemming = data.get('stemming', False)
        e.language = data.get('language', 'en')
        e.threshold = data.get('threshold', 0.7)
        values = data.get('data', [])
        e.values = []
        for value in values:
            v = EntityValue()
            v.name = value.get('label', value.get('value'))
            e.values.append(v)

        return e

    def get_values(self):
        if hasattr(self, 'values'):
            return self.values
        else:
            return []

    def __str__(self):
        return self.name


class EntityValue:
    name = models.CharField(max_length=100)