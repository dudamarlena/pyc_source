# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/disk1/anaconda3/lib/python3.7/site-packages/topic_modeling/model_corpora.py
# Compiled at: 2020-02-25 11:48:42
# Size of source mod 2**32: 2436 bytes
import pandas as pd
from conf.configuration import *
import tqdm, csv
from topic_modeling import *

def model_documents(documents, topic_ontology, topic_model):
    if topic_model == 'esa':
        document_vectors = esa_model(topic_ontology, documents)
    return document_vectors


def save_argument_vectors(argument_ids, argument_vectors, path):
    columns = {}
    columns['argument-id'] = argument_ids
    columns['argument-vector'] = argument_vectors
    document_vectors = pd.DataFrame(columns)
    document_vectors.to_pickle(path)


def save_document_vectors(document_ids, document_vectors, path):
    columns = {}
    columns['document-id'] = document_ids
    columns['document-vector'] = document_vectors
    document_vectors = pd.DataFrame(columns)
    print(path)
    document_vectors.to_pickle(path)


def load_dataset(dataset, level='document'):
    if level == 'argument':
        path = get_path_preprocessed_arguments(dataset)
        df_arguments = pd.read_csv(path, quotechar='"', sep='|', quoting=(csv.QUOTE_ALL), encoding='utf-8')
        return df_arguments
    path = get_path_preprocessed_documents(dataset)
    df_documents = pd.read_csv(path, quotechar='"', sep='|', quoting=(csv.QUOTE_ALL), encoding='utf-8')
    return df_documents


def model_corpora(topic_ontology, topic_model):
    argument_corpora = [
     'args-me', 'ibm-debater-evidence-sentences', 'ukp-ukpconvarg-v1', 'ukp-ukpconvarg-v2', 'ibm-debater-evidence-quality']
    corpora = load_corpora_list()
    for corpus in corpora:
        if corpus not in argument_corpora:
            print(corpus)
            path = get_path_document_vectors(corpus, topic_ontology, topic_model)
            dataset = load_dataset(corpus)
            document_ids = list(dataset['document-id'])
            documents = list(dataset['document'])
            document_vectors = model_documents(documents, topic_ontology, topic_model)
            save_document_vectors(document_ids, document_vectors, path)
        else:
            path = get_path_argument_vectors(corpus, topic_ontology, topic_model)
            dataset = load_dataset(corpus, 'argument')
            argument_ids = list(dataset['argument-id'])
            arguments = list(dataset['argument'])
            argument_vectors = model_documents(arguments, topic_ontology, topic_model)
            save_argument_vectors(argument_ids, argument_vectors, path)


model_corpora('wikipedia', 'esa')