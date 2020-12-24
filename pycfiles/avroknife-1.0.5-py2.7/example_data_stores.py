# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mafju/current/icm/removing_madis_from_code/avroknife/avroknife/test/example_data_stores.py
# Compiled at: 2015-09-04 08:27:04
import os.path, avro.schema
from avro.datafile import DataFileWriter
from avro.io import DatumWriter

def create(standard_out_path, nested_out_path, binary_out_path):
    """Create example Avro data stores"""
    __create_standard(standard_out_path)
    __create_nested(nested_out_path)
    __create_binary(binary_out_path)


def __create_standard(out_path):
    os.makedirs(out_path)
    schema_path = os.path.join(os.path.dirname(__file__), 'data/user.avsc')
    schema = avro.schema.parse(open(schema_path).read())
    with DataFileWriter(open(os.path.join(out_path, 'part-m-00000.avro'), 'w'), DatumWriter(), schema) as (writer):
        writer.append({'position': 0, 'name': 'Alyssa', 'favorite_number': 256})
        writer.append({'position': 1, 'name': 'Ben', 'favorite_number': 4, 'favorite_color': 'red'})
    with DataFileWriter(open(os.path.join(out_path, 'part-m-00001.avro'), 'w'), DatumWriter(), schema) as (writer):
        writer.append({'position': 2, 'name': 'Alyssa2', 'favorite_number': 512})
        writer.append({'position': 3, 'name': 'Ben2', 'favorite_number': 8, 'favorite_color': 'blue', 'secret': '0987654321'})
        writer.append({'position': 4, 'name': 'Ben3', 'favorite_number': 2, 'favorite_color': 'green', 'secret': '12345abcd'})
    with DataFileWriter(open(os.path.join(out_path, 'part-m-00002.avro'), 'w'), DatumWriter(), schema) as (writer):
        pass
    with DataFileWriter(open(os.path.join(out_path, 'part-m-00003.avro'), 'w'), DatumWriter(), schema) as (writer):
        writer.append({'position': 5, 'name': 'Alyssa3', 'favorite_number': 16})
        writer.append({'position': 6, 'name': 'Mallet', 'favorite_color': 'blue', 'secret': 'asdfgf'})
        writer.append({'position': 7, 'name': 'Mikel', 'favorite_color': ''})


def __create_nested(out_path):
    os.makedirs(out_path)
    schema_path = os.path.join(os.path.dirname(__file__), 'data/nested.avsc')
    schema = avro.schema.parse(open(schema_path).read())
    with DataFileWriter(open(os.path.join(out_path, 'part-m-00004.avro'), 'w'), DatumWriter(), schema) as (writer):
        writer.append({'sup': 1, 'sub': {'level2': 2}})
        writer.append({'sup': 2, 'sub': {'level2': 1}})


def __create_binary(out_path):
    os.makedirs(out_path)
    schema_path = os.path.join(os.path.dirname(__file__), 'data/binary.avsc')
    schema = avro.schema.parse(open(schema_path).read())
    with DataFileWriter(open(os.path.join(out_path, 'content.avro'), 'w'), DatumWriter(), schema) as (writer):
        various_stuff_data = open(os.path.join(os.path.dirname(__file__), 'data/binary_stuff/various_stuff.tar.gz')).read()
        writer.append({'description': 'various stuff', 'packed_files': various_stuff_data})
        greetings_data = open(os.path.join(os.path.dirname(__file__), 'data/binary_stuff/greetings.tar.gz')).read()
        writer.append({'description': 'greetings', 'packed_files': greetings_data})