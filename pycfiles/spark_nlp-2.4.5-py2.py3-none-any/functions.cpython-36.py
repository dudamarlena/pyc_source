# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/maziyar/Desktop/Work/JohnSnowLabs/spark-nlp/python/build/lib/sparknlp/functions.py
# Compiled at: 2020-01-01 12:06:29
# Size of source mod 2**32: 946 bytes
from pyspark.sql.functions import udf
from pyspark.sql.types import *
from pyspark.sql import DataFrame
from sparknlp.annotation import Annotation

def map_annotations(f, output_type: DataType):
    return udf(lambda content: f(content), output_type)


def map_annotations_strict(f):
    return udf(lambda content: f(content), ArrayType(Annotation.dataType()))


def map_annotations_col(dataframe: DataFrame, f, column, output_column, output_type):
    dataframe.withColumn(output_column, map_annotations(f, output_type)(column))


def filter_by_annotations_col(dataframe, f, column):
    this_udf = udf(lambda content: f(content), BooleanType())
    return dataframe.filter(this_udf(column))


def explode_annotations_col(dataframe: DataFrame, column, output_column):
    from pyspark.sql.functions import explode
    return dataframe.withColumn(output_column, explode(column))