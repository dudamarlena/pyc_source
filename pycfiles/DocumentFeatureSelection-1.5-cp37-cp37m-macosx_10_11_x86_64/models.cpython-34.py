# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kensuke-mi/Desktop/analysis_work/document-feature-selection/DocumentFeatureSelection/models.py
# Compiled at: 2016-11-29 04:37:36
# Size of source mod 2**32: 8484 bytes
from typing import Dict, List, Tuple, Union, Any, TypeVar
from scipy.sparse.csr import csr_matrix
from DocumentFeatureSelection.common import utils
from numpy.core.multiarray import array, ndarray
from numpy import memmap
from sqlitedict import SqliteDict
from tempfile import mkdtemp
import pickle, json, csv, os, shutil

class PersistentDict(dict):
    __doc__ = " Persistent dictionary with an API compatible with shelve and anydbm.\n\n    The dict is kept in memory, so the dictionary operations run as fast as\n    a regular dictionary.\n\n    Write to disk is delayed until close or sync (similar to gdbm's fast mode).\n\n    Input file format is automatically discovered.\n    Output file format is selectable between pickle, json, and csv.\n    All three serialization formats are backed by fast C implementations.\n\n    "

    def __init__(self, filename, flag='c', mode=None, format='pickle', *args, **kwds):
        self.flag = flag
        self.mode = mode
        self.format = format
        self.filename = filename
        if flag != 'n':
            if os.access(filename, os.R_OK):
                fileobj = open(filename, 'rb' if format == 'pickle' else 'r')
                with fileobj:
                    self.load(fileobj)
        dict.__init__(self, *args, **kwds)

    def sync(self):
        """Write dict to disk"""
        if self.flag == 'r':
            return
        filename = self.filename
        tempname = filename + '.tmp'
        fileobj = open(tempname, 'wb' if self.format == 'pickle' else 'w')
        try:
            try:
                self.dump(fileobj)
            except Exception:
                os.remove(tempname)
                raise

        finally:
            fileobj.close()

        shutil.move(tempname, self.filename)
        if self.mode is not None:
            os.chmod(self.filename, self.mode)

    def close(self):
        self.sync()

    def __enter__(self):
        return self

    def __exit__(self, *exc_info):
        self.close()

    def dump(self, fileobj):
        if self.format == 'csv':
            csv.writer(fileobj).writerows(self.items())
        else:
            if self.format == 'json':
                json.dump(self, fileobj, separators=(',', ':'))
            else:
                if self.format == 'pickle':
                    pickle.dump(dict(self), fileobj, 2)
                else:
                    raise NotImplementedError('Unknown format: ' + repr(self.format))

    def load(self, fileobj):
        for loader in (pickle.load, json.load, csv.reader):
            fileobj.seek(0)
            try:
                return self.update(loader(fileobj))
            except Exception:
                pass

        raise ValueError('File not in a supported format')


class SetDocumentInformation(object):
    __slots__ = [
     'matrix_object', 'label2id', 'feature2id']

    def __init__(self, matrix_object: Union[(csr_matrix, ndarray)], label2id: Dict[(str, int)], feature2id: Dict[(str, int)]):
        self.matrix_object = matrix_object
        self.label2id = label2id
        self.feature2id = feature2id


class DataCsrMatrix(object):
    __doc__ = "\n    vocaburary is, dict object with token: feature_id\n    >>> {'I_aa_hero': 4, 'xx_xx_cc': 1, 'I_aa_aa': 2, 'bb_aa_aa': 3, 'cc_cc_bb': 8}\n\n    label_group_dict is, dict object with label_name: label_id\n    >>> {'label_b': 0, 'label_c': 1, 'label_a': 2}\n\n    csr_matrix is, sparse matrix from scipy.sparse\n    "
    __slots__ = [
     'csr_matrix_', 'label2id_dict', 'vocabulary', 'n_docs_distribution', 'n_term_freq_distribution', 'path_working_dir']

    def __init__(self, csr_matrix_: csr_matrix, label2id_dict: Dict[(str, int)], vocabulary: Dict[(str, int)], n_docs_distribution: ndarray, n_term_freq_distribution: ndarray, is_use_cache: bool=False,
                 is_use_memmap: bool=False,
                 path_working_dir: str=None):
        self.n_docs_distribution = n_docs_distribution
        self.n_term_freq_distribution = n_term_freq_distribution
        if path_working_dir is None:
            self.path_working_dir = mkdtemp()
        else:
            self.path_working_dir = path_working_dir
        if is_use_cache:
            path_vocabulary_cache_obj = os.path.join(self.path_working_dir, 'vocabulary.cache')
            path_label_2_dict_cache_obj = os.path.join(self.path_working_dir, 'label_2_dict.cache')
            self.vocabulary = self.initialize_cache_dict_object(path_vocabulary_cache_obj)
            self.vocabulary = vocabulary
            self.label2id_dict = self.initialize_cache_dict_object(path_label_2_dict_cache_obj)
            self.label2id_dict = label2id_dict
        else:
            self.label2id_dict = label2id_dict
            self.vocabulary = vocabulary
        if is_use_memmap:
            path_memmap_obj = os.path.join(self.path_working_dir, 'matrix.memmap')
            self.csr_matrix_ = self.initialize_memmap_object(csr_matrix_, path_memmap_object=path_memmap_obj)
        else:
            self.csr_matrix_ = csr_matrix_

    def initialize_cache_dict_object(self, path_cache_file):
        return PersistentDict(path_cache_file, flag='c', format='json')

    def initialize_memmap_object(self, matrix_object: csr_matrix, path_memmap_object: str) -> memmap:
        fp = memmap(path_memmap_object, dtype='float64', mode='w+', shape=matrix_object.shape)
        fp[:] = matrix_object.todense()[:]
        return fp

    def __str__(self):
        return 'matrix-type={}, matrix-size={}, path_working_dir={}'.format(type(self.csr_matrix_), self.csr_matrix_.shape, self.path_working_dir)


class ScoredResultObject(object):

    def __init__(self, scored_matrix: csr_matrix, label2id_dict: ndarray, feature2id_dict=ndarray,
                 method: str=None,
                 matrix_form: str=None):
        self.scored_matrix = scored_matrix
        self.label2id_dict = label2id_dict
        self.feature2id_dict = feature2id_dict
        self.method = method
        self.matrix_form = matrix_form

    def __conv_into_dict_format(self, word_score_items):
        out_format_structure = {}
        for item in word_score_items:
            if item['label'] not in out_format_structure:
                out_format_structure[item['label']] = [{'word': item['word'],  'score': item['score']}]
            else:
                out_format_structure[item['label']].append({'word': item['word'],  'score': item['score']})

        return out_format_structure

    def ScoreMatrix2ScoreDictionary(self, outformat: str='items',
                                    sort_desc: bool=True,
                                    n_jobs: int=1):
        """Get dictionary structure of PMI featured scores.

        You can choose 'dict' or 'items' for ```outformat``` parameter.

        If outformat='dict', you get

        >>> {label_name:
                {
                    feature: score
                }
            }

        Else if outformat='items', you get

        >>> [
            {
                feature: score
            }
            ]

        """
        scored_objects = utils.get_feature_dictionary(weighted_matrix=self.scored_matrix, vocabulary=self.feature2id_dict, label_group_dict=self.label2id_dict, n_jobs=n_jobs)
        if sort_desc:
            scored_objects = sorted(scored_objects, key=lambda x: x['score'], reverse=True)
        if outformat == 'dict':
            out_format_structure = self._ScoredResultObject__conv_into_dict_format(scored_objects)
        else:
            if outformat == 'items':
                out_format_structure = scored_objects
            else:
                raise ValueError('outformat must be either of {dict, items}')
        return out_format_structure


FeatureType = TypeVar('T', str, Tuple[Any])
AvailableInputTypes = TypeVar('T', PersistentDict, SqliteDict, Dict[(str, List[List[Union[(str, Tuple[Any])]]])])