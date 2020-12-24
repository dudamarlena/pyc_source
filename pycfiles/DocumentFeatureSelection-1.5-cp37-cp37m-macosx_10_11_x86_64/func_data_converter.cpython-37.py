# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kensuke-mi/Desktop/analysis_work/document-feature-selection/DocumentFeatureSelection/common/func_data_converter.py
# Compiled at: 2018-10-24 07:45:41
# Size of source mod 2**32: 4528 bytes
from collections import Counter
from DocumentFeatureSelection.models import SetDocumentInformation, AvailableInputTypes
from DocumentFeatureSelection.common.utils import init_cache_object
from sklearn.feature_extraction import DictVectorizer
from typing import Dict, List, Tuple, Any, Union
from sqlitedict import SqliteDict
import joblib, itertools, tempfile
N_FEATURE_SWITCH_STRATEGY = 1000000

def generate_document_dict(document_key: str, documents: List[Union[(List[str], Tuple[Any])]]) -> Tuple[(str, Counter)]:
    """This function gets Document-frequency count in given list of documents
    """
    assert isinstance(documents, list)
    feature_frequencies = [Counter(document) for document in documents]
    document_frequencies = Counter()
    for feat_freq in feature_frequencies:
        document_frequencies.update(feat_freq.keys())

    return (document_key, document_frequencies)


def make_multi_docs2term_freq_info(labeled_documents: AvailableInputTypes, is_use_cache: bool=True, path_work_dir: str=tempfile.mkdtemp()):
    """* What u can do
    - This function generates information to construct term-frequency matrix
    """
    if not isinstance(labeled_documents, (SqliteDict, dict)):
        raise AssertionError
    else:
        counted_frequency = [(label, Counter(list(itertools.chain.from_iterable(documents)))) for label, documents in labeled_documents.items()]
        feature_documents = [dict(label_freqCounter_tuple[1]) for label_freqCounter_tuple in counted_frequency]
        if is_use_cache:
            dict_matrix_index = init_cache_object('matrix_element_objects', path_work_dir=path_work_dir)
        else:
            dict_matrix_index = {}
    vec = DictVectorizer()
    dict_matrix_index['matrix_object'] = vec.fit_transform(feature_documents).tocsr()
    dict_matrix_index['feature2id'] = {feat:feat_id for feat_id, feat in enumerate(vec.get_feature_names())}
    dict_matrix_index['label2id'] = {label_freqCounter_tuple[0]:label_id for label_id, label_freqCounter_tuple in enumerate(counted_frequency)}
    return SetDocumentInformation(dict_matrix_index)


def make_multi_docs2doc_freq_info(labeled_documents: AvailableInputTypes, n_jobs: int=-1, path_working_dir: str=tempfile.mkdtemp(), is_use_cache: bool=True) -> SetDocumentInformation:
    """* What u can do
    - This function generates information for constructing document-frequency matrix.
    """
    if not isinstance(labeled_documents, (SqliteDict, dict)):
        raise AssertionError
    else:
        counted_frequency = joblib.Parallel(n_jobs=n_jobs)((joblib.delayed(generate_document_dict)(key, docs) for key, docs in sorted((labeled_documents.items()), key=(lambda key_value_tuple: key_value_tuple[0]))))
        seq_feature_documents = (dict(label_freqCounter_tuple[1]) for label_freqCounter_tuple in counted_frequency)
        if is_use_cache:
            dict_matrix_index = init_cache_object('matrix_element_object', path_working_dir)
        else:
            dict_matrix_index = {}
    vec = DictVectorizer()
    dict_matrix_index['matrix_object'] = vec.fit_transform(seq_feature_documents).tocsr()
    dict_matrix_index['feature2id'] = {feat:feat_id for feat_id, feat in enumerate(vec.get_feature_names())}
    dict_matrix_index['label2id'] = {label_freqCounter_tuple[0]:label_id for label_id, label_freqCounter_tuple in enumerate(counted_frequency)}
    return SetDocumentInformation(dict_matrix_index)


multiDocs2TermFreqInfo = make_multi_docs2term_freq_info
multiDocs2DocFreqInfo = make_multi_docs2doc_freq_info