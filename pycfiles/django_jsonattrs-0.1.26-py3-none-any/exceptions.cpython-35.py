# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Volumes/Work/dev/cadasta/django-jsonattrs/jsonattrs/exceptions.py
# Compiled at: 2017-01-30 12:18:04
# Size of source mod 2**32: 1376 bytes


class SchemaUpdateConflict:
    CONFLICT_TYPES = {'required_no_default': "Required field '{}' added without supplying a default value", 
     'incompatible_type': "Incompatible change in type of field '{}'", 
     'incompatible_choices': "Choices list for field '{}' doesn't include current field value"}

    def __init__(self, field, typ, **kwargs):
        if typ not in self.CONFLICT_TYPES:
            raise ValueError("Invalid type '{}' for SchemaUpdateConflict".format(typ))
        self.field = field
        self.typ = typ
        self.args = kwargs

    def message(self):
        return self.CONFLICT_TYPES[self.typ].format(self.field)

    def __eq__(self, other):
        return self.field == other.field and self.typ == other.typ


class SchemaUpdateException(Exception):

    def __init__(self, *args, **kwargs):
        self.conflicts = kwargs.pop('conflicts', [])
        super().__init__(*args, **kwargs)

    @property
    def messages(self):
        if not hasattr(self, '_messages'):
            self._messages = list(map(lambda c: c.message(), self.conflicts))
        return self._messages

    def __str__(self):
        return 'SchemaUpdateException: ' + str(self.messages)

    def __repr__(self):
        return str(self)