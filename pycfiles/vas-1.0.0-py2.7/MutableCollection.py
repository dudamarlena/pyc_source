# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-x86_64/egg/vas/shared/MutableCollection.py
# Compiled at: 2012-11-01 11:36:39
from vas.shared.Collection import Collection

class MutableCollection(Collection):
    """A collection that allows items to be created

    :ivar `vas.shared.Security.Security`    security:   The resource's security
    """

    def _create(self, payload, rel=None):
        created = self._create_entry(self._client.post(self._location, payload, rel))
        self.reload()
        return created

    def _create_multipart(self, path, payload=None):
        created = self._create_entry(self._client.post_multipart(self._location, path, payload))
        self.reload()
        return created