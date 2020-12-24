# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/gamerocket/attribute_getter.py
# Compiled at: 2013-08-06 11:47:48


class AttributeGetter(object):

    def __init__(self, attributes={}):
        self._setattrs = []
        for key, val in attributes.iteritems():
            setattr(self, key, val)
            self._setattrs.append(key)

    def __repr__(self, detail_list=None):
        if detail_list is None:
            detail_list = self._setattrs
        details = (', ').join('%s: %r' % (attr, getattr(self, attr)) for attr in detail_list if hasattr(self, attr))
        return '<%s {%s} at %d>' % (self.__class__.__name__, details, id(self))