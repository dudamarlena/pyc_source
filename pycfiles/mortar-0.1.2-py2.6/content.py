# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/mortar/content.py
# Compiled at: 2008-12-19 12:41:15
from field import Field
from interfaces import IContent, IField, IFieldType, empty
from types import reference
from zope.interface import implements

class Content:
    implements(IContent, reference)
    id = None

    def __init__(self):
        self.data = {}

    def __getitem__(self, name):
        return Field(self, name)

    def __setitem__(self, name, value):
        if IField.providedBy(value):
            value = value.get()
        elif value is empty:
            value = None
        else:
            value = IFieldType(value)
            if value is empty:
                value = None
        self.data[name] = value
        return

    def __delitem__(self, name):
        del self.data[name]

    @property
    def names(self):
        return sorted(self.data.keys())

    @property
    def type(self):
        return

    def view(self, name=None):
        raise NotImplementedError

    def dimension(self, name, id=None):
        raise NotImplementedError