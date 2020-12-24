# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kensuke-mi/Desktop/analysis_work/document-feature-selection/DocumentFeatureSelection/interface.py
# Compiled at: 2016-11-29 04:37:36
# Size of source mod 2**32: 7817 bytes
from DocumentFeatureSelection.models import DataCsrMatrix, ScoredResultObject, AvailableInputTypes
from DocumentFeatureSelection.common import data_converter
from DocumentFeatureSelection.soa.soa_python3 import SOA
from DocumentFeatureSelection.pmi.PMI_python3 import PMI
from DocumentFeatureSelection.tf_idf.tf_idf import TFIDF
from DocumentFeatureSelection.bns.bns_python3 import BNS
from DocumentFeatureSelection import init_logger
from sqlitedict import SqliteDict
from typing import Dict
from scipy.sparse.csr import csr_matrix
import logging
logger = init_logger.init_logger(logging.getLogger(init_logger.LOGGER_NAME))
METHOD_NAMES = ['soa', 'pmi', 'tf_idf', 'bns']
N_FEATURE_SWITCH_STRATEGY = 1000000

def decide_joblib_strategy(feature2id_dict: Dict[(str, int)]) -> str:
    if len(feature2id_dict) > N_FEATURE_SWITCH_STRATEGY:
        return 'threading'
    else:
        return 'multiprocessing'


def run_feature_selection(input_dict: AvailableInputTypes, method: str, use_cython: bool=False,
                          is_use_cache: bool=False,
                          is_use_memmap: bool=False,
                          path_working_dir: str=None,
                          matrix_form=None,
                          joblib_backend='auto',
                          n_jobs: int=1,
                          ngram: int=1) -> ScoredResultObject:
    """A interface function of DocumentFeatureSelection package.

    * Parameters
    - input_dict: Dict-object which has category-name as key and list of features as value.
        You can put dict or sqlitedict.SqliteDict, or DocumentFeatureSelection.models.PersistentDict
    - method: A method name of feature selection metric
    - use_cython: boolean flag to use cython code for computation. It's much faster to use cython than native-python code
    - is_use_cache: boolean flag to use disk-drive for keeping objects which tends to be huge.
    - is_use_memmap: boolean flag to use memmap for keeping matrix object.
    - path_working_dir: str object.
        The file path to directory where you save cache file or memmap matrix object. If you leave it None, it finds some directory and save files in it.
    """
    if method not in METHOD_NAMES:
        raise Exception('method name must be either of {}. Yours: {}'.format(METHOD_NAMES, method))
    if method == 'tf_idf':
        matrix_data_object = data_converter.DataConverter().labeledMultiDocs2TermFreqMatrix(labeled_documents=input_dict, ngram=ngram, n_jobs=n_jobs, joblib_backend=joblib_backend, is_use_cache=is_use_cache, is_use_memmap=is_use_memmap, path_working_dir=path_working_dir)
        assert isinstance(matrix_data_object, DataCsrMatrix)
        scored_sparse_matrix = TFIDF().fit_transform(X=matrix_data_object.csr_matrix_)
        if not isinstance(scored_sparse_matrix, csr_matrix):
            raise AssertionError
    else:
        if method in ('soa', 'pmi') and matrix_form is None:
            matrix_data_object = data_converter.DataConverter().labeledMultiDocs2DocFreqMatrix(labeled_documents=input_dict, ngram=ngram, n_jobs=n_jobs, joblib_backend=joblib_backend, is_use_cache=is_use_cache, is_use_memmap=is_use_memmap, path_working_dir=path_working_dir)
            assert isinstance(matrix_data_object, DataCsrMatrix)
            if method == 'pmi':
                backend_strategy = decide_joblib_strategy(matrix_data_object.vocabulary)
                scored_sparse_matrix = PMI().fit_transform(X=matrix_data_object.csr_matrix_, n_docs_distribution=matrix_data_object.n_docs_distribution, n_jobs=n_jobs, joblib_backend=backend_strategy, use_cython=use_cython)
                if not isinstance(scored_sparse_matrix, csr_matrix):
                    raise AssertionError
            else:
                if method == 'soa':
                    backend_strategy = decide_joblib_strategy(matrix_data_object.vocabulary)
                    scored_sparse_matrix = SOA().fit_transform(X=matrix_data_object.csr_matrix_, unit_distribution=matrix_data_object.n_docs_distribution, n_jobs=n_jobs, joblib_backend=backend_strategy, use_cython=use_cython)
                    if not isinstance(scored_sparse_matrix, csr_matrix):
                        raise AssertionError
                else:
                    raise Exception()
        else:
            if method == 'soa' and matrix_form == 'term_freq':
                matrix_data_object = data_converter.DataConverter().labeledMultiDocs2TermFreqMatrix(labeled_documents=input_dict, ngram=ngram, n_jobs=n_jobs, joblib_backend=joblib_backend, is_use_cache=is_use_cache, is_use_memmap=is_use_memmap, path_working_dir=path_working_dir)
                assert isinstance(matrix_data_object, DataCsrMatrix)
                backend_strategy = decide_joblib_strategy(matrix_data_object.vocabulary)
                scored_sparse_matrix = SOA().fit_transform(X=matrix_data_object.csr_matrix_, unit_distribution=matrix_data_object.n_docs_distribution, n_jobs=n_jobs, joblib_backend=backend_strategy)
                if not isinstance(scored_sparse_matrix, csr_matrix):
                    raise AssertionError
            else:
                if method == 'bns':
                    if 'positive' not in input_dict:
                        raise KeyError('input_dict must have "positive" key')
                    if 'negative' not in input_dict:
                        raise KeyError('input_dict must have "negative" key')
                    if len(input_dict.keys()) >= 3:
                        raise KeyError('input_dict must not have more than 3 keys if you would like to use BNS.')
                    matrix_data_object = data_converter.DataConverter().labeledMultiDocs2TermFreqMatrix(labeled_documents=input_dict, ngram=ngram, n_jobs=n_jobs, joblib_backend=joblib_backend, is_use_cache=is_use_cache, is_use_memmap=is_use_memmap, path_working_dir=path_working_dir)
                    assert isinstance(matrix_data_object, DataCsrMatrix)
                    true_class_index = matrix_data_object.label2id_dict['positive']
                    backend_strategy = decide_joblib_strategy(matrix_data_object.vocabulary)
                    scored_sparse_matrix = BNS().fit_transform(X=matrix_data_object.csr_matrix_, unit_distribution=matrix_data_object.n_term_freq_distribution, n_jobs=n_jobs, true_index=true_class_index, joblib_backend=backend_strategy)
                    if not isinstance(scored_sparse_matrix, csr_matrix):
                        raise AssertionError
                else:
                    raise Exception()
    return ScoredResultObject(scored_matrix=scored_sparse_matrix, label2id_dict=matrix_data_object.label2id_dict, feature2id_dict=matrix_data_object.vocabulary, method=method, matrix_form=matrix_form)