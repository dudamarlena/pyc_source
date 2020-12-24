# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /zerodb/catalog/indexes/common.py
# Compiled at: 2016-04-22 11:29:50
import six
from zerodbext.catalog.indexes.common import *
_marker = ()

class CallableDiscriminatorMixin(object):
    """
    Compatibility function which makes index pickleable
    """

    def _init_discriminator(self, discriminator):
        if isinstance(discriminator, tuple):
            self.discriminator, = discriminator
            self.discriminator_callable = True
        else:
            if not isinstance(discriminator, six.string_types):
                raise ValueError('discriminator value must be callable or a string')
            self.discriminator = discriminator
            self.discriminator_callable = False

    def index_doc(self, docid, obj):
        if self.discriminator_callable:
            virtuals = getattr(obj.__class__, '_z_virtual_fields', {})
            value = virtuals.get(self.discriminator, _marker)
            if value != _marker:
                try:
                    value = value(obj)
                except:
                    value = _marker

        else:
            value = getattr(obj, self.discriminator, _marker)
        if value is _marker:
            super(CatalogIndex, self).unindex_doc(docid)
            self._not_indexed.add(docid)
            return None
        else:
            if isinstance(value, Persistent):
                raise ValueError('Catalog cannot index persistent object %s' % value)
            if isinstance(value, Broken):
                raise ValueError('Catalog cannot index broken object %s' % value)
            if docid in self._not_indexed:
                self._not_indexed.remove(docid)
            return super(CatalogIndex, self).index_doc(docid, value)