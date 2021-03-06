# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/disk1/anaconda3/lib/python3.7/site-packages/topic_modeling/model_corpus_ibm_debate_claim_sentence_search.py
# Compiled at: 2020-02-19 10:59:04
# Size of source mod 2**32: 2534 bytes
import sys
sys.path.insert(0, '/home/yamenajjour/git/topic-ontologies/')
from argument_esa_model.esa import ESA
from pyspark.sql import SparkSession
from pyspark.sql.types import StructField, StructType, StringType, LongType
import pandas as pd, numpy as np
spark = SparkSession.builder.appName('topic-ontologies').config('master', 'yarn').getOrCreate()
args_me = spark.read.format('csv').option('header', 'true').option('delimiter', ',')

def dict_to_list(dictionary):
    vector = []
    for key in sorted(dictionary):
        vector.append(dictionary[key])

    return np.array(vector).tostring()


def project_arguments():
    esa_model_debatepedia = ESA('/mnt/ceph/storage/data-in-progress/args-topic-modeling/topic-models/esa/debatepedia.mat')

    def project_argument(argument):
        dict_vect = esa_model_debatepedia.process(argument, False)
        return dict_to_list(dict_vect)

    args_me_arguments_df = spark.read.format('csv').option('header', 'true').option('delimiter', '|').option('quote', '"').load('/user/befi8957/topic-ontologies/ibm-debater-claim-sentence-search/ibm-debater-claim-sentence-search-preprocessed-documents.csv').na.drop()
    arguments = args_me_arguments_df.select('document').rdd.map(lambda r: r[0]).repartition(800)
    ids = args_me_arguments_df.select('document-id').rdd.map(lambda r: r[0]).repartition(800)
    vectors = arguments.map(lambda argument: project_argument(argument))
    ids_with_vectors = vectors.zip(ids)
    ids_with_vectors.saveAsTextFile('/user/befi8957/ibm-debater-claim-sentence-search-preprocessed-documents-esa-topic-vectors.csv')


project_arguments()