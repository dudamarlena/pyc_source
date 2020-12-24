# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/joekavalieri/git/conversionman/conversionman/lib/python2.7/site-packages/redisengine/proxy/tree.py
# Compiled at: 2016-03-26 08:08:35
from redisengine.exceptions import InvalidTreeError, LookUpError
from redisengine.core.common import _tree_registry
from redisengine.proxy.base.tree import BaseProxyTree
from redisengine.proxy.base.metaclasses import TreeMetaclass
__all__ = ['ProxyTree']

class ProxyTree(BaseProxyTree):
    __metaclass__ = TreeMetaclass
    __slots__ = ('__objects', )

    def values(self, *keys, **kwargs):
        flat = kwargs.get('flat', False)
        if not self._created:
            keys = list(keys or self._fields_ordered)
            try:
                keys.remove('id')
                keys.remove('pk')
            except ValueError:
                pass

            if flat:
                return [ getattr(self, key) for key in keys ]
            return {key:getattr(self, key) for key in keys}

    def save(self, validate=True, clean=True, use=None, ttl=None, **kwargs):
        """
        :param validate: validates the document; set to ``False`` to skip.
        :param clean: call the document clean method, requires `validate` to be True.
        :param use: optionally write to a different, pre-registered Redis db
        :param ttl: Time to live for the field as a value in seconds to use for the EXPIRY command.
        return an id of a created/updated record

        """
        try:
            ttl = int(ttl or self._ttl)
        except:
            ttl = None

        if validate:
            self.validate(clean=clean)
        if self._created:
            id = self.perform_create(ttl, **kwargs)
        else:
            id = self.perform_update()
        self._clear_changed_fields()
        return id

    def delete(self):
        if self._delete():
            self._setValues(values=dict.fromkeys(self._fields))
            self._created = True
            del self._changed_fields
            del self._deleted_fields