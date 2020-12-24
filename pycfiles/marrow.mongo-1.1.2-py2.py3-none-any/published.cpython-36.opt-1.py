# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /marrow/mongo/core/trait/published.py
# Compiled at: 2017-09-13 15:15:35
# Size of source mod 2**32: 1245 bytes
"""Data model trait mix-in for tracking record publication and retraction."""
from datetime import timedelta
from ... import Document, Index, utcnow
from ...field import Date
from ...util import utcnow

class Published(Document):
    created = Date(default=utcnow, assign=True, write=False, positional=False)
    modified = Date(default=None, write=False, positional=False)
    published = Date(default=None, positional=False)
    retracted = Date(default=None, positional=False)
    _availability = Index('published', 'retracted')

    @classmethod
    def only_published(cls, at=None):
        """Produce a query fragment suitable for selecting documents public.
                
                Now (no arguments), at a specific time (datetime argument), or relative to now (timedelta).
                """
        if isinstance(at, timedelta):
            at = utcnow() + at
        else:
            at = at or utcnow()
        pub, ret = cls.published, cls.retracted
        publication = -pub | (pub == None) | (pub <= at)
        retraction = -ret | (ret == None) | (ret > at)
        return publication & retraction

    @property
    def is_published(self):
        now = utcnow()
        if self.published:
            if self.published > now:
                return False
        if self.retracted:
            if self.retracted < now:
                return False
        return True