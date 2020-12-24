# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/marpel/Scrivania/github/Evaluation-Framework/evaluation_framework/hdf5_dataManager.py
# Compiled at: 2020-01-21 09:44:15
import pandas as pd, json, codecs, numpy as np, base64, h5py
from evaluation_framework.abstract_dataManager import AbstractDataManager

class DataManager(AbstractDataManager):
    """
    It initializes the DataManager for each provided task.
    
    debugging_mode: {TRUE,FALSE}.
    """

    def __init__(self, debugging_mode):
        self.debugging_mode = debugging_mode
        self.taskDataManager = dict()
        self.taskDataManager['classification'] = ClassificationDataManager
        self.taskDataManager['clustering'] = ClusteringDataManager
        self.taskDataManager['regression'] = RegressionDataManager
        self.taskDataManager['document_similarity'] = DocumentSimilarityDataManager
        self.taskDataManager['entity_relatedness'] = EntityRelatednessDataManager
        self.taskDataManager['semantic_analogies'] = SemanticAnalogiesDataManager
        if self.debugging_mode:
            print 'HDF5 data manager initialized'

    def initialize_vectors(self, vector_filename, vector_size):
        return

    def read_vector_file(self, vector_filename, vec_size):
        pass

    def create_header(self, vec_size):
        headers = [
         'name']
        for i in range(0, vec_size):
            headers.append(i)

        return headers

    def read_file(self, filename, columns):
        pass

    def intersect_vectors_goldStandard(self, vectors, vector_filename, vector_size, goldStandard_filename, goldStandard_data, column_key, column_score):
        pass

    def get_data_manager(self, task):
        if task in self.taskDataManager:
            return self.taskDataManager[task]
        else:
            return self

    def add_task_dataManager(self, taskName, dataManager):
        self.dict[taskName] = dataManager


class ClassificationDataManager(DataManager):
    """
    It initializes the DataManager for the classification data manager.
    """

    def __init__(self, debugging_mode):
        self.debugging_mode = debugging_mode
        if self.debugging_mode:
            print 'Classification data manager initialized'

    def read_file(self, filename, columns):
        return pd.read_csv(filename, '\t', usecols=columns, encoding='utf-8')

    def intersect_vectors_goldStandard(self, vectors, vector_filename, vector_size, goldStandard_filename, goldStandard_data=None, column_key='DBpedia_URI15_Base32', column_score='label'):
        vector_file = h5py.File(vector_filename, 'r')
        vector_group = vector_file['Vectors']
        fields = [
         'DBpedia_URI15', column_key, column_score]
        gold = self.read_file(goldStandard_filename, fields)
        gold.rename(columns={column_key: 'name'}, inplace=True)
        gold.rename(columns={column_score: 'label'}, inplace=True)
        merged = pd.DataFrame(columns=self.create_header(vector_size))
        ignored = list()
        for row in gold.itertuples():
            try:
                values = vector_group[row.name][0]
                new_row = dict(zip(np.arange(vector_size), values))
                new_row['name'] = row.name
                new_row['label'] = row.label
                merged = merged.append(new_row, ignore_index=True)
            except KeyError:
                ignored.append(row.DBpedia_URI15)

        ignored_df = pd.DataFrame(ignored, columns=['name'])
        return (merged, ignored_df)

    def create_header(self, vec_size):
        headers = [
         'name', 'label']
        for i in range(0, vec_size):
            headers.append(i)

        return headers


class ClusteringDataManager(DataManager):
    """
    It initializes the DataManager for the clustering data manager.
    """

    def __init__(self, debugging_mode):
        self.debugging_mode = debugging_mode
        if self.debugging_mode:
            print 'Clustering data manager initialized'

    def read_file(self, filename, columns):
        return pd.read_csv(filename, delim_whitespace=True, usecols=columns, index_col=False, skipinitialspace=True, skip_blank_lines=True, encoding='utf-8')

    def intersect_vectors_goldStandard(self, vectors, vector_filename, vector_size, goldStandard_filename, goldStandard_data=None, column_key='DBpedia_URI_Base32', column_score='cluster'):
        vector_file = h5py.File(vector_filename, 'r')
        vector_group = vector_file['Vectors']
        fields = [
         'DBpedia_URI', column_key, column_score]
        gold = self.read_file(goldStandard_filename, fields)
        gold.rename(columns={column_key: 'name'}, inplace=True)
        gold.rename(columns={column_score: 'cluster'}, inplace=True)
        merged = pd.DataFrame(columns=self.create_header(vector_size))
        ignored = pd.DataFrame(columns=['name', 'cluster'])
        for row in gold.itertuples():
            try:
                values = vector_group[row.name][0]
                new_row = dict(zip(np.arange(vector_size), values))
                new_row['name'] = row.name
                new_row['cluster'] = row.cluster
                merged = merged.append(new_row, ignore_index=True)
            except KeyError:
                ignored = ignored.append({'name': row.DBpedia_URI, 'cluster': row.cluster}, ignore_index=True)

        return (
         merged, ignored)

    def create_header(self, vec_size):
        headers = [
         'name', 'cluster']
        for i in range(0, vec_size):
            headers.append(i)

        return headers


class DocumentSimilarityDataManager(DataManager):
    """
    DataManager attached to the DocumentSimilarity task
    """

    def __init__(self, debugging_mode):
        self.debugging_mode = debugging_mode
        if self.debugging_mode:
            print 'Document similarity data manager initialized'

    def read_file(self, filename, columns):
        return pd.read_csv(filename, ',', usecols=columns, index_col=False, skipinitialspace=True, skip_blank_lines=True)

    def intersect_vectors_goldStandard(self, vectors, vector_filename, vector_size, goldStandard_filename, goldStandard_data=None, column_key=None, column_score=None):
        vector_file = h5py.File(vector_filename, 'r')
        vector_group = vector_file['Vectors']
        merged = pd.DataFrame(columns=self.create_header(vector_size))
        ignored = list()
        entities = self.get_entities(goldStandard_filename)
        for row in entities.itertuples():
            try:
                values = vector_group[row.name][0]
                new_row = dict(zip(np.arange(vector_size), values))
                new_row['doc'] = row.doc
                new_row['name'] = row.name
                new_row['weight'] = row.weight
                merged = merged.append(new_row, ignore_index=True)
            except KeyError:
                ignored.append(base64.b32decode(row.name))

        ignored_df = pd.DataFrame(ignored, columns=['name'])
        return (
         merged, ignored_df)

    def get_entities(self, filename):
        with open(filename) as (f):
            data = json.load(f)
        dict_entities = {}
        doc_list = list()
        entities_list = list()
        weight_list = list()
        i = 0
        for doc_obj in data:
            i += 1
            for annotation in doc_obj['annotations']:
                doc_list.append(i)
                key = annotation['entity']
                entities_list.append(base64.b32encode(bytes(key)))
                weight_list.append(float(annotation['weight']))

        dict_entities['doc'] = doc_list
        dict_entities['name'] = entities_list
        dict_entities['weight'] = weight_list
        return pd.DataFrame.from_dict(dict_entities)

    def create_header(self, vec_size):
        headers = [
         'doc', 'name', 'weight']
        for i in range(0, vec_size):
            headers.append(i)

        return headers


class EntityRelatednessDataManager(DataManager):
    """
    It initializes the DataManager for the entity relatedness data manager.
    """

    def __init__(self, debugging_mode):
        self.debugging_mode = debugging_mode
        if self.debugging_mode:
            print 'Entity relatedness data manager initialized'

    def read_file(self, filename, columns=None):
        entities_groups = {}
        related_entities = []
        f = codecs.open(filename, 'r', 'utf-8')
        for i, line in enumerate(f):
            key = line.strip().encode('utf-8')
            encodedKey = base64.b32encode(key)
            if i % 21 == 0:
                main_entitiy = encodedKey
                related_entities = []
            else:
                related_entities.append(encodedKey)
            if i % 21 == 20:
                entities_groups[main_entitiy] = related_entities

        return entities_groups

    def intersect_vectors_goldStandard(self, vectors, vector_filename, vector_size, goldStandard_filename, goldStandard_data=None, column_key=None, column_score=None):
        vector_file = h5py.File(vector_filename, 'r')
        vector_group = vector_file['Vectors']
        merged = pd.DataFrame(columns=self.create_header(vector_size))
        ignored = list()
        if goldStandard_data is None:
            entities = self.read_file(goldStandard_filename)
            goldStandard_data = pd.DataFrame({'name': entities.keys()})
        for row in goldStandard_data.itertuples():
            try:
                encoded_name = row.name
                values = vector_group[encoded_name][0]
                new_row = dict(zip(np.arange(vector_size), values))
                new_row['name'] = encoded_name
                merged = merged.append(new_row, ignore_index=True)
            except KeyError:
                ignored.append(base64.b32decode(encoded_name).decode('utf-8'))

        ignored_df = pd.DataFrame(ignored, columns=['name'])
        return (
         merged, ignored_df)

    def create_header(self, vec_size):
        headers = [
         'name']
        for i in range(0, vec_size):
            headers.append(i)

        return headers


class RegressionDataManager(DataManager):
    """
    It initializes the DataManager for the regression data manager.
    """

    def __init__(self, debugging_mode):
        self.debugging_mode = debugging_mode
        if self.debugging_mode:
            print 'Regression data manager initialized'

    def read_file(self, filename, columns):
        return pd.read_csv(filename, '\t', usecols=columns, encoding='utf-8')

    def intersect_vectors_goldStandard(self, vectors, vector_filename, vector_size, goldStandard_filename, goldStandard_data=None, column_key='DBpedia_URI15_Base32', column_score='rating'):
        vector_file = h5py.File(vector_filename, 'r')
        vector_group = vector_file['Vectors']
        fields = [
         'DBpedia_URI15', column_key, column_score]
        gold = self.read_file(goldStandard_filename, fields)
        gold.rename(columns={column_key: 'name'}, inplace=True)
        gold.rename(columns={column_score: 'label'}, inplace=True)
        merged = pd.DataFrame(columns=self.create_header(vector_size))
        ignored = list()
        for row in gold.itertuples():
            try:
                values = vector_group[row.name][0]
                new_row = dict(zip(np.arange(vector_size), values))
                new_row['name'] = row.name
                new_row['label'] = row.label
                merged = merged.append(new_row, ignore_index=True)
            except KeyError:
                ignored.append(row.DBpedia_URI15)

        ignored_df = pd.DataFrame(ignored, columns=['name'])
        return (merged, ignored_df)

    def create_header(self, vec_size):
        headers = [
         'name', 'label']
        for i in range(0, vec_size):
            headers.append(i)

        return headers


class SemanticAnalogiesDataManager(DataManager):
    """
    It initializes the DataManager for the semantic analogies data manager.
    """

    def __init__(self, debugging_mode):
        self.debugging_mode = debugging_mode
        if self.debugging_mode:
            print 'Semantic analogies data manager initialized'

    def read_file(self, filename, columns):
        pass

    def intersect_vectors_goldStandard(self, vectors, vector_filename, vector_size, goldStandard_filename, goldStandard_data=None, column_key=None, column_score=None):
        vector_file = h5py.File(vector_filename, 'r')
        vector_group = vector_file['Vectors']
        data = list()
        ignored = list()
        with open(goldStandard_filename, 'r') as (f):
            for line in f:
                quadruplet = line.rstrip().split()
                try:
                    key_0 = base64.b32encode(quadruplet[0])
                    key_1 = base64.b32encode(quadruplet[1])
                    key_2 = base64.b32encode(quadruplet[2])
                    key_3 = base64.b32encode(quadruplet[3])
                    vector_group[key_0][0]
                    vector_group[key_1][0]
                    vector_group[key_2][0]
                    vector_group[key_3][0]
                    data.append([key_0, key_1, key_2, key_3])
                except KeyError:
                    ignored.append(quadruplet)

        return (
         data, ignored)

    def create_vocab(self, vectors, vector_filename, vector_size):
        vector_file = h5py.File(vector_filename, 'r')
        vector_group = vector_file['Vectors']
        words = [ key for key in vector_group.keys() ]
        vocab = {w:idx for idx, w in enumerate(words)}
        return vocab

    def normalize_vectors(self, vectors, vector_filename, vec_size, vocab):
        vector_file = h5py.File(vector_filename, 'r')
        vector_group = vector_file['Vectors']
        words = [ key for key in vector_group.keys() ]
        vocab = {w:idx for idx, w in enumerate(words)}
        W = np.zeros((len(words), vec_size))
        for key in words:
            W[vocab[key], :] = vector_group[key][0]

        W_norm = np.zeros(W.shape)
        d = np.sum(W ** 2, 1) ** 0.5
        W_norm = (W.T / d).T
        return W_norm