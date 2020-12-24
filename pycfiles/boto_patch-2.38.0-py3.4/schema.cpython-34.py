# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/boto/dynamodb/schema.py
# Compiled at: 2015-11-24 05:02:18
# Size of source mod 2**32: 3978 bytes


class Schema(object):
    __doc__ = '\n    Represents a DynamoDB schema.\n\n    :ivar hash_key_name: The name of the hash key of the schema.\n    :ivar hash_key_type: The DynamoDB type specification for the\n        hash key of the schema.\n    :ivar range_key_name: The name of the range key of the schema\n        or None if no range key is defined.\n    :ivar range_key_type: The DynamoDB type specification for the\n        range key of the schema or None if no range key is defined.\n    :ivar dict: The underlying Python dictionary that needs to be\n        passed to Layer1 methods.\n    '

    def __init__(self, schema_dict):
        self._dict = schema_dict

    def __repr__(self):
        if self.range_key_name:
            s = 'Schema(%s:%s)' % (self.hash_key_name, self.range_key_name)
        else:
            s = 'Schema(%s)' % self.hash_key_name
        return s

    @classmethod
    def create(cls, hash_key, range_key=None):
        """Convenience method to create a schema object.

        Example usage::

            schema = Schema.create(hash_key=('foo', 'N'))
            schema2 = Schema.create(hash_key=('foo', 'N'),
                                    range_key=('bar', 'S'))

        :type hash_key: tuple
        :param hash_key: A tuple of (hash_key_name, hash_key_type)

        :type range_key: tuple
        :param hash_key: A tuple of (range_key_name, range_key_type)

        """
        reconstructed = {'HashKeyElement': {'AttributeName': hash_key[0], 
                            'AttributeType': hash_key[1]}}
        if range_key is not None:
            reconstructed['RangeKeyElement'] = {'AttributeName': range_key[0],  'AttributeType': range_key[1]}
        instance = cls(None)
        instance._dict = reconstructed
        return instance

    @property
    def dict(self):
        return self._dict

    @property
    def hash_key_name(self):
        return self._dict['HashKeyElement']['AttributeName']

    @property
    def hash_key_type(self):
        return self._dict['HashKeyElement']['AttributeType']

    @property
    def range_key_name(self):
        name = None
        if 'RangeKeyElement' in self._dict:
            name = self._dict['RangeKeyElement']['AttributeName']
        return name

    @property
    def range_key_type(self):
        type = None
        if 'RangeKeyElement' in self._dict:
            type = self._dict['RangeKeyElement']['AttributeType']
        return type

    def __eq__(self, other):
        return self.hash_key_name == other.hash_key_name and self.hash_key_type == other.hash_key_type and self.range_key_name == other.range_key_name and self.range_key_type == other.range_key_type