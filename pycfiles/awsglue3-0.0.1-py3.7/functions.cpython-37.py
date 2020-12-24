# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/awsglue/functions.py
# Compiled at: 2019-08-21 04:11:21
# Size of source mod 2**32: 1347 bytes
from pyspark import SparkContext
from pyspark.sql.column import Column, _to_java_column, _to_seq

def replaceArrayElement(srcCol, replaceCol, idx):
    sc = SparkContext._active_spark_context
    jsrcCol, jreplaceCol = _to_java_column(srcCol), _to_java_column(replaceCol)
    return Column(sc._jvm.gluefunctions.replaceArrayElement(jsrcCol, jreplaceCol, idx))


def namedStruct(*cols):
    sc = SparkContext._active_spark_context
    if len(cols) == 1:
        if isinstance(cols[0], (list, set)):
            cols = cols[0]
    jc = sc._jvm.gluefunctions.namedStruct(_to_seq(sc, cols, _to_java_column))
    return Column(jc)


def explodeWithIndex(col):
    sc = SparkContext._active_spark_context
    jc = sc._jvm.gluefunctions.explodeWithIndex(_to_java_column(col))
    return Column(jc).alias('index', 'val')