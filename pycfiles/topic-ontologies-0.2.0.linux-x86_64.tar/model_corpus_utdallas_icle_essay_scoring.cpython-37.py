# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/disk1/anaconda3/lib/python3.7/site-packages/topic_modeling/model_corpus_utdallas_icle_essay_scoring.py
# Compiled at: 2020-01-20 08:35:36
# Size of source mod 2**32: 1105 bytes
import pandas as pd, json
from conf.configuration import *
import tqdm, csv
from topic_modeling import *

def load_documents():
    dataset_preprocessed_path = get_path_preprocessed_documents('utdallas-icle-essay-scoring')
    documents = pd.read_csv(dataset_preprocessed_path, quotechar='"', sep='|', quoting=(csv.QUOTE_ALL), encoding='utf-8')
    ids = list(documents['document-id'])
    texts = list(documents['document'])
    return (
     texts, ids)


def model_arguments(documents, topic_ontology, topic_model):
    argument_vectors = model(topic_ontology, topic_model, documents)
    return argument_vectors


def save_document_vectors(document_ids, document_vectors, path):
    columns = {}
    columns['document-id'] = document_ids
    columns['document-vector'] = document_vectors
    document_vectors = pd.DataFrame(columns)
    document_vectors.to_pickle(path)


texts, ids = load_documents()
document_vectors = model_arguments(texts, 'strategic-intlligence', 'esa')
path = get_path_document_vectors('utdallas-icle-essay-scoring', 'strategic-intelligence', 'esa')
save_document_vectors(ids, document_vectors, path)