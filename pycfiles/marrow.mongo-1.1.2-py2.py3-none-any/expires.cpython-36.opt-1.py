# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /marrow/mongo/core/trait/expires.py
# Compiled at: 2017-09-13 15:15:35
# Size of source mod 2**32: 1283 bytes
from ... import Document, Index, utcnow
from ...field import TTL

class Expires(Document):
    __doc__ = 'Record auto-expiry field with supporting TTL index and properties.'
    expires = TTL(default=None, write=False, positional=False)
    _expires = Index('expires', expire=0, sparse=True)

    @property
    def is_expired(self):
        """Determine if this document has already expired.
                
                We need this because MongoDB TTL indexes are culled once per minute on an as-able basis, meaning records might
                be available for up to 60 seconds after their expiry time normally and that if there are many records to cull,
                may be present even longer.
                """
        if not self.expires:
            return
        else:
            return self.expires <= utcnow()

    @classmethod
    def from_mongo(cls, data, expired=False, **kw):
        """In the event a value that has technically already expired is loaded, swap it for None."""
        value = (super(Expires, cls).from_mongo)(data, **kw)
        if not expired:
            if value.is_expired:
                return
        return value