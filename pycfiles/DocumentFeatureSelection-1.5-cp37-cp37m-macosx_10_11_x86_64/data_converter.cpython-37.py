# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kensuke-mi/Desktop/analysis_work/document-feature-selection/DocumentFeatureSelection/common/data_converter.py
# Compiled at: 2018-10-24 08:46:08
# Size of source mod 2**32: 9749 bytes
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from DocumentFeatureSelection.common import utils, func_data_converter
from DocumentFeatureSelection.models import DataCsrMatrix, AvailableInputTypes, PersistentDict
from DocumentFeatureSelection.init_logger import logger
from sqlitedict import SqliteDict
import sys, numpy, tempfile, json
from typing import Dict, List, Tuple, Any, Union
python_version = sys.version_info
__author__ = 'kensuke-mi'

class DataConverter(object):
    __doc__ = 'This class is for converting data type from dict-object into DataCsrMatrix-object which saves information of matrix.\n    '

    def __init__(self):
        self.labeledMultiDocs2TermFreqMatrix = self.convert_multi_docs2term_frequency_matrix
        self.labeledMultiDocs2DocFreqMatrix = self.convert_multi_docs2document_frequency_matrix

    def count_term_frequency_distribution(self, labeled_documents: AvailableInputTypes, label2id: Dict[(str, int)]):
        """Count term-distribution per label.
        """
        assert isinstance(labeled_documents, (SqliteDict, dict))
        assert isinstance(label2id, dict)
        term_frequency_distribution = {label:len(list(utils.flatten(document_lists))) for label, document_lists in labeled_documents.items()}
        term_frequency_distribution_list = [
         0] * len(labeled_documents)
        for label_string, n_doc in term_frequency_distribution.items():
            term_index = label2id[label_string]
            term_frequency_distribution_list[term_index] = n_doc

        return numpy.array(term_frequency_distribution_list, dtype='i8')

    def count_document_distribution(self, labeled_documents: AvailableInputTypes, label2id: Dict[(str, int)]) -> numpy.ndarray:
        """This method count n(docs) per label.
        """
        assert isinstance(labeled_documents, (SqliteDict, dict))
        assert isinstance(label2id, dict)
        n_doc_distribution = {label:len(document_lists) for label, document_lists in labeled_documents.items()}
        n_doc_distribution_list = [
         0] * len(labeled_documents)
        for label_string, n_doc in n_doc_distribution.items():
            docs_index = label2id[label_string]
            n_doc_distribution_list[docs_index] = n_doc

        return numpy.array(n_doc_distribution_list, dtype='i8')

    def __make_feature_object2json_string(self, seq_feature_in_doc: List[Union[(str, List[str], Tuple[(str, ...)])]]) -> List[str]:
        """Sub-method of make_feature_object2json_string()"""
        replaced_seq_feature_in_doc = [
         None] * len(seq_feature_in_doc)
        for i, feature_object in enumerate(seq_feature_in_doc):
            if isinstance(feature_object, str):
                replaced_seq_feature_in_doc[i] = json.dumps((tuple([feature_object])), ensure_ascii=False)
            elif isinstance(feature_object, (tuple, list)):
                replaced_seq_feature_in_doc[i] = json.dumps(feature_object, ensure_ascii=False)
            else:
                raise Exception('feature type must be either of str,list,tuple. Detected={}'.format(type(feature_object)))
        else:
            return replaced_seq_feature_in_doc

    def make_feature_object2json_string(self, labeled_document: AvailableInputTypes) -> Dict[(str, AvailableInputTypes)]:
        """* What u can do
        - This function converts feature-object in sequence object into json string.
        - This function make every object into json string.
            - string object -> json array which has one string. Ex. "feature" -> '["feature"]'
            - list object -> json array. Ex. ["feature", "feature"] -> '["feature", "feature"]'
            - tuple object -> json array. Ex. ("feature", "feature") -> '["feature", "feature"]'
        * Parameters
        - labeled_document: dict object which has key of 'label-name', and value is 2-dim list of features.

        """
        assert isinstance(labeled_document, (dict, PersistentDict, SqliteDict))
        replaced_labeled_document = {key:[] for key in labeled_document}
        for key, docs_in_label in labeled_document.items():
            assert isinstance(docs_in_label, list)
            replaced_docs_in_label = [None] * len(docs_in_label)
            for i, doc_label in enumerate(docs_in_label):
                replaced_docs_in_label[i] = self._DataConverter__make_feature_object2json_string(doc_label)
            else:
                replaced_labeled_document[key] = replaced_docs_in_label

        else:
            return replaced_labeled_document

    def convert_multi_docs2term_frequency_matrix(self, labeled_documents: AvailableInputTypes, is_use_cache: bool=False, is_use_memmap: bool=False, path_working_dir: str=tempfile.mkdtemp(), cache_backend: str='PersistentDict', n_jobs: int=1):
        """* What you can do
        - This function makes TERM-frequency matrix for TF-IDF calculation.
        - TERM-frequency matrix is scipy.csr_matrix.

        * Params
        - labeled_documents: Dict object which has category-name as key, and list of features as value
        - is_use_cache: boolean flag to use disk-drive for keeping objects which tends to be huge.
        - path_working_dir: path to directory for saving cache files
        """
        labeled_documents = self.make_feature_object2json_string(labeled_documents)
        logger.debug(msg='Now pre-processing before CSR matrix')
        set_document_information = func_data_converter.make_multi_docs2term_freq_info(labeled_documents)
        n_docs_distribution = self.count_document_distribution(labeled_documents=labeled_documents,
          label2id=(set_document_information.label2id))
        term_frequency_distribution = self.count_term_frequency_distribution(labeled_documents=labeled_documents,
          label2id=(set_document_information.label2id))
        return DataCsrMatrix(csr_matrix_=(set_document_information.matrix_object),
          label2id_dict=(set_document_information.label2id),
          vocabulary=(set_document_information.feature2id),
          n_docs_distribution=n_docs_distribution,
          n_term_freq_distribution=term_frequency_distribution,
          is_use_cache=is_use_cache,
          is_use_memmap=is_use_memmap,
          path_working_dir=path_working_dir,
          cache_backend=cache_backend)

    def convert_multi_docs2document_frequency_matrix(self, labeled_documents: AvailableInputTypes, is_use_cache: bool=False, is_use_memmap: bool=False, path_working_dir: str=None, n_jobs: int=1) -> DataCsrMatrix:
        """This function makes document-frequency matrix. Document-frequency matrix is scipy.csr_matrix.

        * Input object
        - "labeled_structure" is either of Dict object or shelve.DbfilenameShelf. The example format is below
            >>> {"label_a": [["I", "aa", "aa", "aa", "aa", "aa"],["bb", "aa", "aa", "aa", "aa", "aa"],["I", "aa", "hero", "some", "ok", "aa"]],
            >>> "label_b": [["bb", "bb", "bb"],["bb", "bb", "bb"],["hero", "ok", "bb"],["hero", "cc", "bb"],],
            >>> "label_c": [["cc", "cc", "cc"],["cc", "cc", "bb"],["xx", "xx", "cc"],["aa", "xx", "cc"],]}

        * Output
        - DataCsrMatrix object.
        """
        labeled_documents = self.make_feature_object2json_string(labeled_documents)
        logger.debug(msg='Now pre-processing before CSR matrix')
        set_document_information = func_data_converter.make_multi_docs2doc_freq_info(labeled_documents, n_jobs=n_jobs)
        assert isinstance(set_document_information, func_data_converter.SetDocumentInformation)
        n_docs_distribution = self.count_document_distribution(labeled_documents=labeled_documents,
          label2id=(set_document_information.label2id))
        term_frequency_distribution = self.count_term_frequency_distribution(labeled_documents=labeled_documents,
          label2id=(set_document_information.label2id))
        return DataCsrMatrix(csr_matrix_=(set_document_information.matrix_object),
          label2id_dict=(set_document_information.label2id),
          vocabulary=(set_document_information.feature2id),
          n_docs_distribution=n_docs_distribution,
          n_term_freq_distribution=term_frequency_distribution,
          is_use_cache=is_use_cache,
          is_use_memmap=is_use_memmap,
          path_working_dir=path_working_dir)