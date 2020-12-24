# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/finvoicelib/mapping.py
# Compiled at: 2010-03-24 05:43:08


class Mapping(object):
    cls = None
    tag = None

    def __init__(self, tag, cls):
        self.tag = tag
        self.cls = cls


class Map(object):
    tag = None
    cls = None
    collection = None

    def __init__(self, cls):
        self.collection = []
        self.tag = cls.tag
        self.cls = cls

    def __repr__(self):
        return '<Mapping: %s>' % self.tag

    def __len__(self):
        return len(self.collection)

    def __getitem__(self, i):
        return self.collection[i]

    def first(self):
        if len(self.collection) > 0:
            return self.collection[0]
        else:
            return

    def as_string(self, delim='\n'):
        value = delim.join([ unicode(obj.text) for obj in self.collection ])
        if len(value) < 1:
            return ''
        return value

    def add(self, node):
        self.collection.append(node)