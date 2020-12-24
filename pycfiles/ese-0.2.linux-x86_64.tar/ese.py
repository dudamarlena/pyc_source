# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/hgfs/rubik/.virtualenvs/ese/lib/python2.7/site-packages/ese/ese.py
# Compiled at: 2015-05-19 13:27:01
from __future__ import unicode_literals
import argparse
from multiprocessing import Process, Queue, Value
from uuid import uuid4
from time import sleep
import traceback
from datetime import datetime
from elasticsearch import Elasticsearch, RequestsHttpConnection
from elasticsearch.client import IndicesClient
from elasticsearch.helpers import bulk, scan
import logging
logging.basicConfig(format=b'%(asctime)s %(message)s', level=logging.INFO)
log = logging.getLogger(__name__)
__author__ = b'kheechin'

def get_elasticsearch(hostname, port):
    return Elasticsearch(hosts=[b'http://%s:%s/' % (hostname, port)], max_retries=10, timeout=60, retry_on_timeout=True, connection_class=RequestsHttpConnection)


def src_worker(args, dest_queue, MAGIC_STRING):
    src_es_instance = get_elasticsearch(args.src_host, args.src_port)
    if args.query is None or len(args.query) == 0:
        use_query = {b'query': {b'match_all': {}}}
    else:
        use_query = args.query
    try:
        try:
            scroll = scan(src_es_instance, query=use_query, index=args.src_index, scroll=b'60m', size=args.src_batch_size)
            for i, res in enumerate(scroll):
                if i % 10000 == 0:
                    log.info(b'[src_worker] Processed %s' % i)
                dest_queue.put(res)

            log.info(b'[src_worker] Total processed %s' % i)
        except:
            log.error(traceback.format_exc())

    finally:
        for i in xrange(args.dest_concurrency):
            dest_queue.put(MAGIC_STRING)

    return


def dest_worker(args, dest_queue, MAGIC_STRING, DEST_COUNTER):
    dest_es_instance = get_elasticsearch(args.dest_host, args.dest_port)
    BATCH_LIST = []
    for datum in iter(dest_queue.get, MAGIC_STRING):
        datum[b'_index'] = args.dest_index
        BATCH_LIST.append(datum)
        if len(BATCH_LIST) % args.dest_batch_size == 0:
            bulk(dest_es_instance, BATCH_LIST, chunk_size=args.dest_batch_size, refresh=False, stats_only=True)
            BATCH_LIST = []
        with DEST_COUNTER.get_lock():
            if DEST_COUNTER.value % 10000 == 0:
                log.info(b'[dest_worker] Processed %s' % (DEST_COUNTER.value,))
            DEST_COUNTER.value += 1

    if len(BATCH_LIST) > 0:
        bulk(dest_es_instance, BATCH_LIST, chunk_size=args.dest_batch_size, refresh=False, stats_only=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(b'--src-host', action=b'store', default=b'127.0.0.1', type=unicode, help=b'Source host [default: %(default)s]')
    parser.add_argument(b'--src-port', action=b'store', default=9200, help=b'Source port [default: %(default)s]')
    parser.add_argument(b'--src-index', action=b'store', default=b'', type=unicode, help=b'Source index')
    parser.add_argument(b'--src-batch-size', action=b'store', type=int, default=5000, help=b'Source query batchsize [default: %(default)s]')
    parser.add_argument(b'--dest-host', action=b'store', default=b'127.0.0.1', type=unicode, help=b'Destination host [default: %(default)s]')
    parser.add_argument(b'--dest-port', action=b'store', default=9200, help=b'Destination port [default: %(default)s]')
    parser.add_argument(b'--dest-index', action=b'store', default=b'', type=unicode, help=b'Destination index')
    parser.add_argument(b'--dest-batch-size', action=b'store', type=int, default=5000, help=b'Destination batchsize [default: %(default)s]')
    parser.add_argument(b'--dest-alias', action=b'store', help=b'Destination index alias (to be set after we have finished populating)')
    parser.add_argument(b'--dest-concurrency', action=b'store', type=int, default=4, help=b'Destination batchsize [default: %(default)s]')
    parser.add_argument(b'--dest-delete-index', action=b'store_true', help=b'Delete destination index at before starting')
    parser.add_argument(b'--query', action=b'store', type=unicode, default=b'', help=b'Query to use [if None is specified, a match_all will be used]')
    args = parser.parse_args()
    if args.src_index is None or len(args.src_index) == 0:
        raise Exception(b'--src-index must be specified!')
    if args.dest_index is None or len(args.dest_index) == 0:
        raise Exception(b'--dest-index must be specified!')
    dt_start = datetime.now()
    src_es_instance = get_elasticsearch(args.src_host, args.src_port)
    dest_es_instance = get_elasticsearch(args.dest_host, args.dest_port)
    src_es_ic = IndicesClient(src_es_instance)
    if not src_es_ic.exists(args.src_index):
        raise Exception(b'--src-index %s does not exist!' % args.src_index)
    dest_es_ic = IndicesClient(dest_es_instance)
    if dest_es_ic.exists(args.dest_index):
        if args.dest_delete_index:
            dest_es_ic.delete(index=args.dest_index)
        else:
            raise Exception(b'--dest-index %s already exists! Use --dest-delete-index if you want to drop it' % args.dest_index)
    log.info(b'Copying mapping...')
    src_index_information = src_es_ic.get(index=args.src_index)
    dest_es_ic.create(index=args.dest_index, body=src_index_information.get(args.src_index, {}))
    dest_es_ic.put_settings(index=args.dest_index, body={b'settings': {b'index': {b'number_of_replicas': 0}}})
    log.info(b'Copying data...')
    MAGIC_STRING = b'%s:%s' % (str(uuid4()), str(uuid4()))
    DEST_QUEUE = Queue()
    DEST_COUNTER = Value(b'i', 0)
    src_process = Process(target=src_worker, args=(args, DEST_QUEUE, MAGIC_STRING))
    src_process.start()
    dest_processes = [ Process(target=dest_worker, args=(args, DEST_QUEUE, MAGIC_STRING, DEST_COUNTER)) for i in xrange(args.dest_concurrency) ]
    for i in dest_processes:
        i.start()

    src_process.join()
    for i in dest_processes:
        i.join()

    log.info(b'[dest_worker] Total processed %s' % DEST_COUNTER.value)
    if args.dest_alias is not None and len(args.dest_alias) > 0:
        for idx_name, aliases_mapping in dest_es_ic.get_aliases().iteritems():
            if args.dest_alias in aliases_mapping.get(b'aliases', {}):
                dest_es_ic.delete_alias(index=idx_name, name=args.dest_alias)

        dest_es_ic.put_alias(index=args.dest_index, name=args.dest_alias)
    dest_es_ic.refresh(args.dest_index)
    dt_end = datetime.now()
    log.info(b'Time elapsed: %s' % (dt_end - dt_start,))
    return


if __name__ == b'__main__':
    main()