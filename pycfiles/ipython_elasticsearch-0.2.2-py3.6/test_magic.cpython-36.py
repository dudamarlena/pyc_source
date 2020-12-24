# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/tests/test_magic.py
# Compiled at: 2017-12-19 17:02:27
# Size of source mod 2**32: 2059 bytes
import responses
from elasticsearch.magic import ElasticsearchMagics
ip = get_ipython()

def test_load_ext():
    elasticsearchmagic = ElasticsearchMagics(shell=ip)
    ip.register_magics(elasticsearchmagic)


def test_run_line_magic():
    ip.run_line_magic('elasticsearch', None)
    ip.run_line_magic('elasticsearch', 'http://foo')


def test_cell_magic_json_response():
    with responses.RequestsMock() as (rsps):
        rsps.add((responses.GET), 'http://magic.mock:1234/',
          body='{\n                     "name" : "Slither",\n                     "cluster_name" : "elasticsearch",\n                     "version" : {\n                         "number" : "2.0.0",\n                         "build_hash" : "de54438d6af8f9340d50c5c786151783ce7d6be5",\n                         "build_timestamp" : "2015-10-22T08:09:48Z",\n                         "build_snapshot" : false,\n                         "lucene_version" : "5.2.1"\n                     },\n                     "tagline" : "You Know, for Search"\n                 }',
          content_type='application/json; charset=UTF-8',
          status=200)
        ip.run_cell_magic('elasticsearch', 'http://magic.mock:1234/', 'GET /')


def test_cell_magic_text_response():
    with responses.RequestsMock() as (rsps):
        rsps.add((responses.GET), 'http://magic.mock:1234/_cat',
          body='=^.^=\n                     /_cat/allocation\n                     /_cat/shards\n                     /_cat/shards/{index}\n                     /_cat/master\n                     /_cat/nodes\n                     /_cat/indices\n                     /_cat/indices/{index}\n                     /_cat/segments\n                     /_cat/segments/{index}\n                     /_cat/health\n                  ',
          content_type='text/plain; charset=UTF-8',
          status=200)
        ip.run_cell_magic('elasticsearch', 'http://magic.mock:1234/', 'GET /_cat')