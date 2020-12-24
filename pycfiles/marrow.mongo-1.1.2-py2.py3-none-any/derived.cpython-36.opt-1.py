# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /marrow/mongo/core/trait/derived.py
# Compiled at: 2017-09-13 15:15:35
# Size of source mod 2**32: 693 bytes
from ... import Document, Index
from ...field import PluginReference

class Derived(Document):
    __doc__ = 'Access and store the class reference to a particular Document subclass.\n\t\n\tThis allows for easy access to the magical `_cls` key as the `cls` attribute.\n\t'
    __type_store__ = '_cls'
    cls = PluginReference('marrow.mongo.document', '_cls', explicit=True, repr=False, positional=False)
    _cls = Index('cls')

    def __init__(self, *args, **kw):
        (super(Derived, self).__init__)(*args, **kw)
        self.cls = self.__class__