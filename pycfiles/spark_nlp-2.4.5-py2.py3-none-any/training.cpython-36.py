# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/maziyar/Desktop/Work/JohnSnowLabs/spark-nlp/python/build/lib/sparknlp/training.py
# Compiled at: 2020-02-08 11:36:13
# Size of source mod 2**32: 1844 bytes
from sparknlp.internal import ExtendedJavaWrapper
from sparknlp.common import ExternalResource, ReadAs
from pyspark.sql import SparkSession, DataFrame

class CoNLL(ExtendedJavaWrapper):

    def __init__(self, documentCol='document', sentenceCol='sentence', tokenCol='token', posCol='pos', conllLabelIndex=3, conllPosIndex=1, textCol='text', labelCol='label', explodeSentences=True):
        super(CoNLL, self).__init__('com.johnsnowlabs.nlp.training.CoNLL', documentCol, sentenceCol, tokenCol, posCol, conllLabelIndex, conllPosIndex, textCol, labelCol, explodeSentences)

    def readDataset(self, spark, path, read_as=ReadAs.TEXT):
        jSession = spark._jsparkSession
        jdf = self._java_obj.readDataset(jSession, path, read_as)
        return DataFrame(jdf, spark._wrapped)


class POS(ExtendedJavaWrapper):

    def __init__(self):
        super(POS, self).__init__('com.johnsnowlabs.nlp.training.POS')

    def readDataset(self, spark, path, delimiter='|', outputPosCol='tags', outputDocumentCol='document', outputTextCol='text'):
        jSession = spark._jsparkSession
        jdf = self._java_obj.readDataset(jSession, path, delimiter, outputPosCol, outputDocumentCol, outputTextCol)
        return DataFrame(jdf, spark._wrapped)