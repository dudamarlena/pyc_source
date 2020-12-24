# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kensuke-mi/Desktop/analysis_work/document-feature-selection/DocumentFeatureSelection/pmi/PMI_python3.py
# Compiled at: 2018-10-24 10:27:19
# Size of source mod 2**32: 5812 bytes
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from scipy.sparse import csr_matrix
from numpy import memmap
from typing import Union
from DocumentFeatureSelection.init_logger import logger
import logging, joblib, math, numpy
__author__ = 'kensuke-mi'

def pmi--- This code section failed: ---

 L.  36         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'X'
                4  LOAD_GLOBAL              memmap
                6  LOAD_GLOBAL              csr_matrix
                8  BUILD_TUPLE_2         2 
               10  CALL_FUNCTION_2       2  '2 positional arguments'
               12  POP_JUMP_IF_TRUE     18  'to 18'
               14  LOAD_ASSERT              AssertionError
               16  RAISE_VARARGS_1       1  'exception instance'
             18_0  COME_FROM            12  '12'

 L.  37        18  LOAD_GLOBAL              isinstance
               20  LOAD_FAST                'n_docs_distribution'
               22  LOAD_GLOBAL              numpy
               24  LOAD_ATTR                ndarray
               26  CALL_FUNCTION_2       2  '2 positional arguments'
               28  POP_JUMP_IF_TRUE     34  'to 34'
               30  LOAD_ASSERT              AssertionError
               32  RAISE_VARARGS_1       1  'exception instance'
             34_0  COME_FROM            28  '28'

 L.  38        34  LOAD_GLOBAL              isinstance
               36  LOAD_FAST                'feature_index'
               38  LOAD_GLOBAL              int
               40  CALL_FUNCTION_2       2  '2 positional arguments'
               42  POP_JUMP_IF_TRUE     48  'to 48'
               44  LOAD_ASSERT              AssertionError
               46  RAISE_VARARGS_1       1  'exception instance'
             48_0  COME_FROM            42  '42'

 L.  39        48  LOAD_GLOBAL              isinstance
               50  LOAD_DEREF               'sample_index'
               52  LOAD_GLOBAL              int
               54  CALL_FUNCTION_2       2  '2 positional arguments'
               56  POP_JUMP_IF_TRUE     62  'to 62'
               58  LOAD_ASSERT              AssertionError
               60  RAISE_VARARGS_1       1  'exception instance'
             62_0  COME_FROM            56  '56'

 L.  41        62  LOAD_FAST                'X'
               64  LOAD_ATTR                shape
               66  STORE_FAST               'matrix_size'

 L.  42        68  LOAD_CLOSURE             'sample_index'
               70  BUILD_TUPLE_1         1 
               72  LOAD_LISTCOMP            '<code_object <listcomp>>'
               74  LOAD_STR                 'pmi.<locals>.<listcomp>'
               76  MAKE_FUNCTION_8          'closure'
               78  LOAD_GLOBAL              range
               80  LOAD_CONST               0
               82  LOAD_FAST                'matrix_size'
               84  LOAD_CONST               0
               86  BINARY_SUBSCR    
               88  CALL_FUNCTION_2       2  '2 positional arguments'
               90  GET_ITER         
               92  CALL_FUNCTION_1       1  '1 positional argument'
               94  STORE_FAST               'sample_indexes'

 L.  45        96  LOAD_FAST                'X'
               98  LOAD_DEREF               'sample_index'
              100  LOAD_FAST                'feature_index'
              102  BUILD_TUPLE_2         2 
              104  BINARY_SUBSCR    
              106  STORE_FAST               'n_11'

 L.  47       108  LOAD_FAST                'n_docs_distribution'
              110  LOAD_DEREF               'sample_index'
              112  BINARY_SUBSCR    
              114  LOAD_FAST                'n_11'
              116  BINARY_SUBTRACT  
              118  STORE_FAST               'n_01'

 L.  49       120  LOAD_FAST                'X'
              122  LOAD_FAST                'sample_indexes'
              124  LOAD_FAST                'feature_index'
              126  BUILD_TUPLE_2         2 
              128  BINARY_SUBSCR    
              130  LOAD_METHOD              sum
              132  CALL_METHOD_0         0  '0 positional arguments'
              134  STORE_FAST               'n_10'

 L.  51       136  LOAD_FAST                'n_total_doc'
              138  LOAD_FAST                'n_10'
              140  LOAD_FAST                'n_docs_distribution'
              142  LOAD_DEREF               'sample_index'
              144  BINARY_SUBSCR    
              146  BINARY_ADD       
              148  BINARY_SUBTRACT  
              150  STORE_FAST               'n_00'

 L.  53       152  LOAD_FAST                'verbose'
              154  POP_JUMP_IF_FALSE   196  'to 196'

 L.  54       156  LOAD_GLOBAL              logging
              158  LOAD_METHOD              debug
              160  LOAD_STR                 'For feature_index:{} sample_index:{}'
              162  LOAD_METHOD              format
              164  LOAD_FAST                'feature_index'
              166  LOAD_DEREF               'sample_index'
              168  CALL_METHOD_2         2  '2 positional arguments'
              170  CALL_METHOD_1         1  '1 positional argument'
              172  POP_TOP          

 L.  55       174  LOAD_GLOBAL              logging
              176  LOAD_METHOD              debug
              178  LOAD_STR                 'n_11:{} n_01:{} n_10:{} n_00:{}'
              180  LOAD_METHOD              format

 L.  56       182  LOAD_FAST                'n_11'

 L.  57       184  LOAD_FAST                'n_01'

 L.  58       186  LOAD_FAST                'n_10'

 L.  59       188  LOAD_FAST                'n_00'
              190  CALL_METHOD_4         4  '4 positional arguments'
              192  CALL_METHOD_1         1  '1 positional argument'
              194  POP_TOP          
            196_0  COME_FROM           154  '154'

 L.  62       196  LOAD_FAST                'n_11'
              198  LOAD_CONST               0.0
              200  COMPARE_OP               ==
              202  POP_JUMP_IF_TRUE    228  'to 228'
              204  LOAD_FAST                'n_10'
              206  LOAD_CONST               0.0
              208  COMPARE_OP               ==
              210  POP_JUMP_IF_TRUE    228  'to 228'
              212  LOAD_FAST                'n_01'
              214  LOAD_CONST               0.0
              216  COMPARE_OP               ==
              218  POP_JUMP_IF_TRUE    228  'to 228'
              220  LOAD_FAST                'n_00'
              222  LOAD_CONST               0.0
              224  COMPARE_OP               ==
              226  POP_JUMP_IF_FALSE   232  'to 232'
            228_0  COME_FROM           218  '218'
            228_1  COME_FROM           210  '210'
            228_2  COME_FROM           202  '202'

 L.  63       228  LOAD_CONST               0
              230  RETURN_VALUE     
            232_0  COME_FROM           226  '226'

 L.  65       232  LOAD_FAST                'n_11'
              234  LOAD_FAST                'n_total_doc'
              236  BINARY_TRUE_DIVIDE
              238  LOAD_GLOBAL              math
              240  LOAD_METHOD              log
              242  LOAD_FAST                'n_total_doc'
              244  LOAD_FAST                'n_11'
              246  BINARY_MULTIPLY  
              248  LOAD_FAST                'n_10'
              250  LOAD_FAST                'n_11'
              252  BINARY_ADD       
              254  LOAD_FAST                'n_01'
              256  LOAD_FAST                'n_11'
              258  BINARY_ADD       
              260  BINARY_MULTIPLY  
              262  BINARY_TRUE_DIVIDE
              264  LOAD_CONST               2
              266  CALL_METHOD_2         2  '2 positional arguments'
              268  BINARY_MULTIPLY  
              270  STORE_FAST               'temp1'

 L.  66       272  LOAD_FAST                'n_01'
              274  LOAD_FAST                'n_total_doc'
              276  BINARY_TRUE_DIVIDE
              278  LOAD_GLOBAL              math
              280  LOAD_METHOD              log
              282  LOAD_FAST                'n_total_doc'
              284  LOAD_FAST                'n_01'
              286  BINARY_MULTIPLY  
              288  LOAD_FAST                'n_00'
              290  LOAD_FAST                'n_01'
              292  BINARY_ADD       
              294  LOAD_FAST                'n_01'
              296  LOAD_FAST                'n_11'
              298  BINARY_ADD       
              300  BINARY_MULTIPLY  
              302  BINARY_TRUE_DIVIDE
              304  LOAD_CONST               2
              306  CALL_METHOD_2         2  '2 positional arguments'
              308  BINARY_MULTIPLY  
              310  STORE_FAST               'temp2'

 L.  67       312  LOAD_FAST                'n_10'
              314  LOAD_FAST                'n_total_doc'
              316  BINARY_TRUE_DIVIDE
              318  LOAD_GLOBAL              math
              320  LOAD_METHOD              log
              322  LOAD_FAST                'n_total_doc'
              324  LOAD_FAST                'n_10'
              326  BINARY_MULTIPLY  
              328  LOAD_FAST                'n_10'
              330  LOAD_FAST                'n_11'
              332  BINARY_ADD       
              334  LOAD_FAST                'n_00'
              336  LOAD_FAST                'n_10'
              338  BINARY_ADD       
              340  BINARY_MULTIPLY  
              342  BINARY_TRUE_DIVIDE
              344  LOAD_CONST               2
              346  CALL_METHOD_2         2  '2 positional arguments'
              348  BINARY_MULTIPLY  
              350  STORE_FAST               'temp3'

 L.  68       352  LOAD_FAST                'n_00'
              354  LOAD_FAST                'n_total_doc'
              356  BINARY_TRUE_DIVIDE
              358  LOAD_GLOBAL              math
              360  LOAD_METHOD              log
              362  LOAD_FAST                'n_total_doc'
              364  LOAD_FAST                'n_00'
              366  BINARY_MULTIPLY  
              368  LOAD_FAST                'n_00'
              370  LOAD_FAST                'n_01'
              372  BINARY_ADD       
              374  LOAD_FAST                'n_00'
              376  LOAD_FAST                'n_10'
              378  BINARY_ADD       
              380  BINARY_MULTIPLY  
              382  BINARY_TRUE_DIVIDE
              384  LOAD_CONST               2
              386  CALL_METHOD_2         2  '2 positional arguments'
              388  BINARY_MULTIPLY  
              390  STORE_FAST               'temp4'

 L.  69       392  LOAD_FAST                'temp1'
              394  LOAD_FAST                'temp2'
              396  BINARY_ADD       
              398  LOAD_FAST                'temp3'
              400  BINARY_ADD       
              402  LOAD_FAST                'temp4'
              404  BINARY_ADD       
              406  STORE_FAST               'score'

 L.  71       408  LOAD_FAST                'score'
              410  RETURN_VALUE     

Parse error at or near `LOAD_FAST' instruction at offset 408


class PMI(object):

    def __init__(self):
        pass

    def fit_transform(self, X: Union[(csr_matrix, memmap)], n_docs_distribution, n_jobs=1, verbose=False, joblib_backend='multiprocessing', use_cython: bool=False):
        """Main method of PMI class.
        """
        if not isinstanceX(memmap, csr_matrix):
            raise AssertionError
        else:
            assert isinstancen_docs_distributionnumpy.ndarray
            matrix_size = X.shape
            sample_range = list(range0matrix_size[0])
            feature_range = list(range0matrix_size[1])
            n_total_document = sum(n_docs_distribution)
            logger.debug(msg='Start calculating PMI')
            logger.debug(msg=('size(input_matrix)={} * {}'.formatX.shape[0]X.shape[1]))
            if use_cython:
                import pyximport
                pyximport.install
                from DocumentFeatureSelection.pmi.pmi_cython import main
                logger.warning(msg='n_jobs parameter is invalid when use_cython=True')
                pmi_score_csr_source = main(X=X, n_docs_distribution=n_docs_distribution,
                  sample_range=sample_range,
                  feature_range=feature_range,
                  n_total_doc=n_total_document,
                  verbose=False)
            else:
                self.pmi = pmi
            pmi_score_csr_source = joblib.Parallel(n_jobs=n_jobs, backend=joblib_backend)((joblib.delayedself.docId_word_PMI(X=X, n_docs_distribution=n_docs_distribution, feature_index=feature_index, sample_index=sample_index, n_total_doc=n_total_document, verbose=verbose) for sample_index in sample_range for feature_index in feature_range))
        row_list = [t[0] for t in pmi_score_csr_source]
        col_list = [t[1] for t in pmi_score_csr_source]
        data_list = [t[2] for t in pmi_score_csr_source]
        pmi_featured_csr_matrix = csr_matrix((data_list, (row_list, col_list)), shape=(
         X.shape[0],
         X.shape[1]))
        logging.debug(msg='End calculating PMI')
        return pmi_featured_csr_matrix

    def docId_word_PMI(self, X: Union[(csr_matrix, memmap)], n_docs_distribution: numpy.ndarray, n_total_doc: int, feature_index: int, sample_index: int, verbose=False, use_cython: bool=False):
        """Calculate PMI score for fit_format()

        :param X:
        :param vocabulary:
        :param label_id:
        :param word:
        :param label:
        :return:
        """
        pmi_score = self.pmi(X=X,
          n_docs_distribution=n_docs_distribution,
          feature_index=feature_index,
          sample_index=sample_index,
          n_total_doc=n_total_doc,
          verbose=verbose)
        return (
         sample_index, feature_index, pmi_score)