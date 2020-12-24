# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-intel/egg/pydap/handlers/sqlite/freeze.py
# Compiled at: 2011-10-04 15:18:38
"""
Dump a SQL dataset into a sqlite db file.

"""
import sys, os, urlparse, sqlite3, numpy
from simplejson import dumps
from pydap.model import *
from pydap.lib import walk
from pydap.client import open_url
sqlite3.register_adapter(numpy.float32, float)
sqlite3.register_adapter(numpy.float32, float)
sqlite3.register_adapter(numpy.int32, int)
type_name = {Float64: 'NUMBER', 
   Float32: 'NUMBER', 
   Int32: 'NUMBER', 
   Int16: 'NUMBER', 
   Byte: 'NUMBER', 
   UInt32: 'NUMBER', 
   UInt16: 'NUMBER', 
   String: 'TEXT', 
   Url: 'TEXT'}

def freeze():
    url = sys.argv[1]
    basename = urlparse.urlsplit(url).path.rsplit('/', 1)[1].rsplit('.', 1)[0]
    dataset = open_url(url)
    connection = sqlite3.connect('%s.db' % basename, detect_types=sqlite3.PARSE_DECLTYPES)
    connection.executescript('\n        CREATE TABLE attributes (\n            id VARCHAR(255),\n            value TEXT);\n        CREATE INDEX id ON attributes (id);\n    ')
    connection.commit()
    dataset.attributes['__name__'] = dataset.name
    connection.execute('INSERT INTO attributes (id, value) VALUES (?, ?);', (
     'DATASET', dumps(dataset.attributes)))
    n = 0
    for sequence in walk(dataset, SequenceType):
        n += 1

    if n != 1:
        raise Exception('Exactly one sequence must be present in the dataset.')
    sequence.attributes['__name__'] = sequence.name
    connection.execute('INSERT INTO attributes (id, value) VALUES (?, ?);', (
     'SEQUENCE', dumps(sequence.attributes)))
    for i, child in enumerate(sequence.values()):
        if i == 0:
            connection.executescript('CREATE TABLE data (%s %s);' % (child.name, type_name[child.type]))
        else:
            connection.executescript('ALTER TABLE data ADD COLUMN %s %s;' % (child.name, type_name[child.type]))
        child.attributes['__type__'] = child.type.descriptor
        connection.execute('INSERT INTO attributes (id, value) VALUES (?, ?);', (
         child.name, dumps(child.attributes)))

    connection.commit()
    for value in sequence:
        markers = (', ').join([ '?' for var in value.keys() ])
        query = 'INSERT INTO data (%s) VALUES (%s)' % ((', ').join(value.keys()), markers)
        connection.execute(query, value.data)

    connection.commit()