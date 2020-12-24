# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/namegen/namegen.py
# Compiled at: 2012-01-11 09:49:54
from .names import names as default_names
import random

class NameGenerator(object):

    def __init__(self, names=default_names):
        self._names = {i:name.strip() for i, name in enumerate(names)}
        self._total_names = len(self._names)
        self._used_indices = set()

    def __call__(self):
        index = random.randrange(self._total_names)
        name = self._names[index]
        if index not in self._used_indices:
            self._used_indices.add(index)
            return name

    def __iter__(self):
        while True:
            yield self()