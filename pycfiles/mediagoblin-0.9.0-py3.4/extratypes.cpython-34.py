# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mediagoblin/db/extratypes.py
# Compiled at: 2014-01-05 20:10:09
# Size of source mod 2**32: 2931 bytes
from sqlalchemy.ext.mutable import Mutable
from sqlalchemy.types import TypeDecorator, Unicode, TEXT
import json

class PathTupleWithSlashes(TypeDecorator):
    __doc__ = 'Represents a Tuple of strings as a slash separated string.'
    impl = Unicode

    def process_bind_param(self, value, dialect):
        if value is not None:
            if len(value) == 0:
                value = None
            else:
                value = '/'.join(value)
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            value = tuple(value.split('/'))
        return value


class JSONEncoded(TypeDecorator):
    __doc__ = 'Represents an immutable structure as a json-encoded string.'
    impl = TEXT

    def process_bind_param(self, value, dialect):
        if value is not None:
            value = json.dumps(value)
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            value = json.loads(value)
        return value


class MutationDict(Mutable, dict):

    @classmethod
    def coerce(cls, key, value):
        """Convert plain dictionaries to MutationDict."""
        if not isinstance(value, MutationDict):
            if isinstance(value, dict):
                return MutationDict(value)
            return Mutable.coerce(key, value)
        else:
            return value

    def __setitem__(self, key, value):
        """Detect dictionary set events and emit change events."""
        dict.__setitem__(self, key, value)
        self.changed()

    def __delitem__(self, key):
        """Detect dictionary del events and emit change events."""
        dict.__delitem__(self, key)
        self.changed()