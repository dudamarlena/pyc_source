# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\pydrizzle\traits102\trait_errors.py
# Compiled at: 2014-04-16 13:17:36
from __future__ import division
import exceptions
from trait_base import class_of

class TraitError(exceptions.Exception):

    def __init__(self, args=None, name=None, info=None, value=None):
        if name is None:
            self.args = args
        else:
            self.name = name
            self.info = info
            self.value = value
            self.desc = None
            self.prefix = 'The'
            self.set_desc(None, args)
        return

    def set_desc(self, desc, object=None):
        if hasattr(self, 'desc'):
            if desc is not None:
                self.desc = desc
            if object is not None:
                self.object = object
            self.set_args()
        return

    def set_prefix(self, prefix):
        if hasattr(self, 'prefix'):
            self.prefix = prefix
            self.set_args()

    def set_args(self):
        if self.desc is None:
            extra = ''
        else:
            extra = ' specifies %s and' % self.desc
        self.args = "%s '%s' trait of %s instance%s must be %s, but a value of %s was specified." % (
         self.prefix, self.name, class_of(self.object), extra,
         self.info, self.value)
        return


class DelegationError(TraitError):

    def __init__(self, args):
        self.args = args