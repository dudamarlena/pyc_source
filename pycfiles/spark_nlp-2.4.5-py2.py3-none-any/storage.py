# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/maziyar/Desktop/Work/JohnSnowLabs/spark-nlp/python/build/lib/sparknlp/storage.py
# Compiled at: 2020-01-01 12:06:29
import sparknlp.internal as _internal
from pyspark.ml.param import Params
from pyspark import keyword_only
import sys, threading, time, sparknlp.pretrained as _pretrained
from sparknlp.annotator import WordEmbeddingsModel

class RocksDBConnection:

    def __init__(self, connection):
        self.jconnection = connection


class StorageHelper:

    @classmethod
    def load(cls, path, spark_session, database):
        print 'Loading started this may take some time'
        stop_threads = False
        t1 = threading.Thread(target=_pretrained.printProgress, args=(lambda : stop_threads,))
        t1.start()
        jembeddings = _internal._StorageHelper(path, spark_session, database).apply()
        stop_threads = True
        t1.join()
        print 'Loading done'
        return RocksDBConnection(jembeddings)