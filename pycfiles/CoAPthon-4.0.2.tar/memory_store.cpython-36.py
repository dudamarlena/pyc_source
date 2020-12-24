# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/jik/.virtualenvs/coal-mine/lib/python3.6/site-packages/coal_mine/memory_store.py
# Compiled at: 2016-08-09 17:39:55
# Size of source mod 2**32: 2636 bytes
__doc__ = '\nIn-memory store for Coal Mine, primarily for use by tests\n'
from .abstract_store import AbstractStore
from copy import deepcopy
import re

class MemoryStore(AbstractStore):

    def __init__(self):
        self.canaries = {}

    def create(self, canary):
        self.canaries[canary['id']] = deepcopy(canary)

    def update(self, identifier, updates):
        canary = self.canaries[identifier]
        for key, value in ((k, v) for k, v in updates.items()):
            if value is None:
                if key in canary:
                    del canary[key]
            else:
                canary[key] = value

    def get(self, identifier):
        return deepcopy(self.canaries[identifier])

    def list(self, *, verbose=False, paused=None, late=None, search=None):
        iterator = self.canaries.values()
        if paused is not None:
            iterator = (i for i in iterator if i['paused'] == paused)
        if late is not None:
            iterator = (i for i in iterator if i['late'] == late)
        if search is not None:
            regex = re.compile(search)
            iterator = (i for i in iterator if regex.search(i['name']) or regex.search(i['slug']) or regex.search(i['id']))
        if not verbose:
            iterator = ({'id':i['id'],  'name':i['name']} for i in iterator)
        return (deepcopy(i) for i in iterator)

    def upcoming_deadlines(self):
        iterator = self.canaries.values()
        iterator = (i for i in iterator if not i['paused'])
        iterator = (i for i in iterator if not i['late'])
        return (deepcopy(i) for i in sorted(iterator, key=(lambda i: i['deadline'])))

    def delete(self, identifier):
        del self.canaries[identifier]

    def find_identifier(self, slug):
        matches = (i for i in self.canaries.values() if i['slug'] == slug)
        try:
            return next(matches)['id']
        except StopIteration:
            raise KeyError()