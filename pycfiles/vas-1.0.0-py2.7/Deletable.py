# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-x86_64/egg/vas/shared/Deletable.py
# Compiled at: 2012-11-01 11:35:36


class Deletable(object):
    """The :class:`vas.shared.Deletable.Deletable` mixin provides classes with support for deletion. The class must
    provide to instance variables: client and location.
    """
    __collection = None

    @property
    def _collection(self):
        return self.__collection

    @_collection.setter
    def _collection(self, collection):
        self.__collection = collection

    def delete(self):
        """Performs a delete. If a collection is available it is reloaded."""
        self._client.delete(self._location)
        if self.__collection:
            self.__collection.reload()