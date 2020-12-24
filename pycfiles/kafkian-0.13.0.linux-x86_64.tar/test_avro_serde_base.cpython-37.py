# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sbeilin/.pyenv/versions/3.7.0/lib/python3.7/site-packages/tests/unit/test_avro_serde_base.py
# Compiled at: 2018-12-06 16:02:36
# Size of source mod 2**32: 1461 bytes
from confluent_kafka import avro
from kafkian.serde.avroserdebase import HasSchemaMixin, _wrap
RECORD_SCHEMA = avro.loads('\n{\n    "name": "SomethingHappened",\n    "type": "record",\n    "doc": "basic schema for tests",\n    "namespace": "python.test.basic",\n    "fields": [\n        {\n            "name": "number",\n            "doc": "age",\n            "type": [\n                "long",\n                "null"\n            ]\n        },\n        {\n            "name": "name",\n            "doc": "a name",\n            "type": [\n                "string"\n            ]\n        }\n    ]\n}\n')
KEY_SCHEMA = avro.loads('{"type": "string"}')

def test_schema_mixin_wrapper_record_schema():
    for base_class in (int, float, dict, list):
        val = base_class()
        wrapped = _wrap(val, RECORD_SCHEMA)
        assert val == wrapped
        assert isinstance(wrapped, base_class)
        assert isinstance(wrapped, HasSchemaMixin)
        assert wrapped.schema is RECORD_SCHEMA
        assert wrapped.__class__.__name__ == 'python.test.basic.SomethingHappened'


def test_schema_mixin_wrapper_key_schema():
    for base_class in (int, float, dict, list):
        val = base_class()
        wrapped = _wrap(val, KEY_SCHEMA)
        assert val == wrapped
        assert isinstance(wrapped, base_class)
        assert isinstance(wrapped, HasSchemaMixin)
        assert wrapped.schema is KEY_SCHEMA
        assert wrapped.__class__.__name__ == KEY_SCHEMA.type