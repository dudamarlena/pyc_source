# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/troposphere_mate-project/troposphere_mate/core/code.py
# Compiled at: 2020-02-19 10:42:41
# Size of source mod 2**32: 3788 bytes
try:
    import typing
except:
    pass

import json
from collections import OrderedDict
from troposphere import kinesisanalyticsv2, glue, AWSObject, AWSProperty

def get_schema(resource):
    _schema = OrderedDict()
    for prop_name, (prop_type, required) in resource.props.items():
        try:
            issubclass(prop_type, AWSProperty)
            _schema[prop_name] = get_schema(prop_type)
        except:
            if isinstance(prop_type, list):
                try:
                    issubclass(prop_type[0], AWSProperty)
                    _schema[prop_name] = get_schema(prop_type[0])
                except:
                    _schema[prop_name] = None

            else:
                _schema[prop_name] = None

    return _schema


glue_table_json = '\n{\n    "Table": {\n        "Name": "sign_up_counts",\n        "DatabaseName": "test",\n        "CreateTime": 1581648637.0,\n        "UpdateTime": 1581648637.0,\n        "Retention": 0,\n        "StorageDescriptor": {\n            "Columns": [\n                {\n                    "Name": "event_time",\n                    "Type": "timestamp"\n                },\n                {\n                    "Name": "sign_up_event_counts",\n                    "Type": "smallint"\n                }\n            ],\n            "Location": "s3://eq-sanhe-for-everything/data/kinesis-analytics/login-gov-metrics-dev",\n            "Compressed": false,\n            "NumberOfBuckets": 0,\n            "SerdeInfo": {\n                "SerializationLibrary": "org.openx.data.jsonserde.JsonSerDe",\n                "Parameters": {\n                    "serialization.format": "1"\n                }\n            },\n            "SortColumns": [],\n            "StoredAsSubDirectories": false\n        },\n        "PartitionKeys": [\n            {\n                "Name": "year",\n                "Type": "smallint"\n            },\n            {\n                "Name": "month",\n                "Type": "smallint"\n            },\n            {\n                "Name": "day",\n                "Type": "smallint"\n            },\n            {\n                "Name": "hour",\n                "Type": "smallint"\n            },\n            {\n                "Name": "minute",\n                "Type": "smallint"\n            }\n        ],\n        "TableType": "EXTERNAL_TABLE",\n        "CreatedBy": "arn:aws:iam::110330507156:user/sanhe",\n        "IsRegisteredWithLakeFormation": false\n    }\n}\n'.strip()

def jprint(dct):
    print(json.dumps(dct, indent=4, sort_keys=True))


SEP = '.'

def flatten_dct(dct, _items=None, _parent=None):
    """
    Convert a dict with nested dict or list into flattened key, value pairs.
    Key is in form of json path.

    :type dct: dict
    :rtype: typing.List[typing.Tuple[str, typing.Any]]
    """
    if _items is None:
        _items = list()
    if _parent is None:
        _parent = ''
    for key, value in dct.items():
        key = _parent + key
        if isinstance(value, dict):
            _items.extend(flatten_dct(value, _parent=(key + SEP)))
        else:
            if isinstance(value, list):
                for ind, item in enumerate(value):
                    _items.extend(flatten_dct({'[{}]'.format(ind): item}, _parent=(key + SEP)))

            else:
                _items.append([key, value])

    return _items


def convert_data(dct, resource_type):
    schema = get_schema(resource_type)
    schema_flattened = flatten_dct(schema)
    jprint(schema_flattened)


if __name__ == '__main__':
    schema = get_schema(glue.Table)
    jprint(schema)