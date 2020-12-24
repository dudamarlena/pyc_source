# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.4/dist-packages/fuzzyworkbench/entitybrowser.py
# Compiled at: 2015-10-01 12:54:48
# Size of source mod 2**32: 403 bytes


class EntityBrowser:

    def __init__(self, editor):
        self._editor = editor
        self._entities = []

    def add(self, entity):
        self._entities.append(entity)

    def remove(self, entity):
        self._entities.remove(entity)

    def select(self, entity):
        pass

    def getSelected(self):
        pass