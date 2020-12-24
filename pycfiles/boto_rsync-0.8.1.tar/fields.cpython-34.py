# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/boto/dynamodb2/fields.py
# Compiled at: 2015-11-24 05:02:18
# Size of source mod 2**32: 8292 bytes
from boto.dynamodb2.types import STRING

class BaseSchemaField(object):
    """BaseSchemaField"""
    attr_type = None

    def __init__(self, name, data_type=STRING):
        """
        Creates a Python schema field, to represent the data to pass to
        DynamoDB.

        Requires a ``name`` parameter, which should be a string name of the
        field.

        Optionally accepts a ``data_type`` parameter, which should be a
        constant from ``boto.dynamodb2.types``. (Default: ``STRING``)
        """
        self.name = name
        self.data_type = data_type

    def definition(self):
        """
        Returns the attribute definition structure DynamoDB expects.

        Example::

            >>> field.definition()
            {
                'AttributeName': 'username',
                'AttributeType': 'S',
            }

        """
        return {'AttributeName': self.name, 
         'AttributeType': self.data_type}

    def schema(self):
        """
        Returns the schema structure DynamoDB expects.

        Example::

            >>> field.schema()
            {
                'AttributeName': 'username',
                'KeyType': 'HASH',
            }

        """
        return {'AttributeName': self.name, 
         'KeyType': self.attr_type}


class HashKey(BaseSchemaField):
    """HashKey"""
    attr_type = 'HASH'


class RangeKey(BaseSchemaField):
    """RangeKey"""
    attr_type = 'RANGE'


class BaseIndexField(object):
    """BaseIndexField"""

    def __init__(self, name, parts):
        self.name = name
        self.parts = parts

    def definition(self):
        """
        Returns the attribute definition structure DynamoDB expects.

        Example::

            >>> index.definition()
            {
                'AttributeName': 'username',
                'AttributeType': 'S',
            }

        """
        definition = []
        for part in self.parts:
            definition.append({'AttributeName': part.name, 
             'AttributeType': part.data_type})

        return definition

    def schema(self):
        """
        Returns the schema structure DynamoDB expects.

        Example::

            >>> index.schema()
            {
                'IndexName': 'LastNameIndex',
                'KeySchema': [
                    {
                        'AttributeName': 'username',
                        'KeyType': 'HASH',
                    },
                ],
                'Projection': {
                    'ProjectionType': 'KEYS_ONLY',
                }
            }

        """
        key_schema = []
        for part in self.parts:
            key_schema.append(part.schema())

        return {'IndexName': self.name, 
         'KeySchema': key_schema, 
         'Projection': {'ProjectionType': self.projection_type}}


class AllIndex(BaseIndexField):
    """AllIndex"""
    projection_type = 'ALL'


class KeysOnlyIndex(BaseIndexField):
    """KeysOnlyIndex"""
    projection_type = 'KEYS_ONLY'


class IncludeIndex(BaseIndexField):
    """IncludeIndex"""
    projection_type = 'INCLUDE'

    def __init__(self, *args, **kwargs):
        self.includes_fields = kwargs.pop('includes', [])
        super(IncludeIndex, self).__init__(*args, **kwargs)

    def schema(self):
        schema_data = super(IncludeIndex, self).schema()
        schema_data['Projection']['NonKeyAttributes'] = self.includes_fields
        return schema_data


class GlobalBaseIndexField(BaseIndexField):
    """GlobalBaseIndexField"""
    throughput = {'read': 5, 
     'write': 5}

    def __init__(self, *args, **kwargs):
        throughput = kwargs.pop('throughput', None)
        if throughput is not None:
            self.throughput = throughput
        super(GlobalBaseIndexField, self).__init__(*args, **kwargs)

    def schema(self):
        """
        Returns the schema structure DynamoDB expects.

        Example::

            >>> index.schema()
            {
                'IndexName': 'LastNameIndex',
                'KeySchema': [
                    {
                        'AttributeName': 'username',
                        'KeyType': 'HASH',
                    },
                ],
                'Projection': {
                    'ProjectionType': 'KEYS_ONLY',
                },
                'ProvisionedThroughput': {
                    'ReadCapacityUnits': 5,
                    'WriteCapacityUnits': 5
                }
            }

        """
        schema_data = super(GlobalBaseIndexField, self).schema()
        schema_data['ProvisionedThroughput'] = {'ReadCapacityUnits': int(self.throughput['read']), 
         'WriteCapacityUnits': int(self.throughput['write'])}
        return schema_data


class GlobalAllIndex(GlobalBaseIndexField):
    """GlobalAllIndex"""
    projection_type = 'ALL'


class GlobalKeysOnlyIndex(GlobalBaseIndexField):
    """GlobalKeysOnlyIndex"""
    projection_type = 'KEYS_ONLY'


class GlobalIncludeIndex(GlobalBaseIndexField, IncludeIndex):
    """GlobalIncludeIndex"""
    projection_type = 'INCLUDE'

    def __init__(self, *args, **kwargs):
        throughput = kwargs.pop('throughput', None)
        IncludeIndex.__init__(self, *args, **kwargs)
        if throughput:
            kwargs['throughput'] = throughput
        GlobalBaseIndexField.__init__(self, *args, **kwargs)

    def schema(self):
        schema_data = IncludeIndex.schema(self)
        schema_data.update(GlobalBaseIndexField.schema(self))
        return schema_data