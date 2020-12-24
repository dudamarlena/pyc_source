# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sbeilin/.pyenv/versions/3.7.0/lib/python3.7/site-packages/tests/unit/test_subject_name_strategy.py
# Compiled at: 2019-04-23 05:48:32
# Size of source mod 2**32: 1101 bytes
import pytest
from confluent_kafka import avro
from kafkian.serde.serialization import SubjectNameStrategy, AvroSerializer
value_schema_str = '\n{\n   "namespace": "my.test",\n   "name": "Value",\n   "type": "record",\n   "fields" : [\n     {\n       "name" : "name",\n       "type" : "string"\n     }\n   ]\n}\n'
schema = avro.loads(value_schema_str)

@pytest.mark.parametrize('strategy,is_key,subject', (
 (
  SubjectNameStrategy.TopicNameStrategy, False, 'topic-value'),
 (
  SubjectNameStrategy.TopicNameStrategy, True, 'topic-key'),
 (
  SubjectNameStrategy.RecordNameStrategy, False, 'my.test.Value'),
 (
  SubjectNameStrategy.RecordNameStrategy, True, 'my.test.Value'),
 (
  SubjectNameStrategy.TopicRecordNameStrategy, False, 'topic-my.test.Value'),
 (
  SubjectNameStrategy.TopicRecordNameStrategy, True, 'topic-my.test.Value')))
def test_subject_name_strategy(strategy, is_key, subject):
    ser = AvroSerializer('http://nxhost:2181', subject_name_strategy=strategy)
    assert ser._get_subject('topic', schema, is_key) == subject