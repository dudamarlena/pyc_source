# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/hachoir_core/field/field_set.py
# Compiled at: 2009-09-07 17:44:28
from hachoir_core.field import BasicFieldSet, GenericFieldSet

class FieldSet(GenericFieldSet):
    __module__ = __name__

    def __init__(self, parent, name, *args, **kw):
        assert issubclass(parent.__class__, BasicFieldSet)
        GenericFieldSet.__init__(self, parent, name, parent.stream, *args, **kw)