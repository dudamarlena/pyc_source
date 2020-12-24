# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kensuke-mi/Desktop/analysis_work/document-feature-selection/DocumentFeatureSelection/soa/soa_python3.py
# Compiled at: 2018-10-24 08:46:08
# Size of source mod 2**32: 5377 bytes
from scipy.sparse import csr_matrix
from numpy import memmap
from typing import Union
from DocumentFeatureSelection.init_logger import logger
import logging, joblib, math, numpy
__author__ = 'kensuke-mi'

def soa--- This code section failed: ---

 L.  19         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'X'
                4  LOAD_GLOBAL              memmap
                6  LOAD_GLOBAL              csr_matrix
                8  BUILD_TUPLE_2         2 
               10  CALL_FUNCTION_2       2  '2 positional arguments'
               12  POP_JUMP_IF_TRUE     18  'to 18'
               14  LOAD_ASSERT              AssertionError
               16  RAISE_VARARGS_1       1  'exception instance'
             18_0  COME_FROM            12  '12'

 L.  20        18  LOAD_GLOBAL              isinstance
               20  LOAD_FAST                'unit_distribution'
               22  LOAD_GLOBAL              numpy
               24  LOAD_ATTR                ndarray
               26  CALL_FUNCTION_2       2  '2 positional arguments'
               28  POP_JUMP_IF_TRUE     34  'to 34'
               30  LOAD_ASSERT              AssertionError
               32  RAISE_VARARGS_1       1  'exception instance'
             34_0  COME_FROM            28  '28'

 L.  21        34  LOAD_GLOBAL              isinstance
               36  LOAD_FAST                'feature_index'
               38  LOAD_GLOBAL              int
               40  CALL_FUNCTION_2       2  '2 positional arguments'
               42  POP_JUMP_IF_TRUE     48  'to 48'
               44  LOAD_ASSERT              AssertionError
               46  RAISE_VARARGS_1       1  'exception instance'
             48_0  COME_FROM            42  '42'

 L.  22        48  LOAD_GLOBAL              isinstance
               50  LOAD_DEREF               'sample_index'
               52  LOAD_GLOBAL              int
               54  CALL_FUNCTION_2       2  '2 positional arguments'
               56  POP_JUMP_IF_TRUE     62  'to 62'
               58  LOAD_ASSERT              AssertionError
               60  RAISE_VARARGS_1       1  'exception instance'
             62_0  COME_FROM            56  '56'

 L.  24        62  LOAD_FAST                'X'
               64  LOAD_ATTR                shape
               66  STORE_FAST               'matrix_size'

 L.  25        68  LOAD_CLOSURE             'sample_index'
               70  BUILD_TUPLE_1         1 
               72  LOAD_LISTCOMP            '<code_object <listcomp>>'
               74  LOAD_STR                 'soa.<locals>.<listcomp>'
               76  MAKE_FUNCTION_8          'closure'
               78  LOAD_GLOBAL              range
               80  LOAD_CONST               0
               82  LOAD_FAST                'matrix_size'
               84  LOAD_CONST               0
               86  BINARY_SUBSCR    
               88  CALL_FUNCTION_2       2  '2 positional arguments'
               90  GET_ITER         
               92  CALL_FUNCTION_1       1  '1 positional argument'
               94  STORE_FAST               'NOT_sample_indexes'

 L.  28        96  LOAD_FAST                'X'
               98  LOAD_DEREF               'sample_index'
              100  LOAD_FAST                'feature_index'
              102  BUILD_TUPLE_2         2 
              104  BINARY_SUBSCR    
              106  STORE_FAST               'freq_w_e'

 L.  30       108  LOAD_FAST                'X'
              110  LOAD_FAST                'NOT_sample_indexes'
              112  LOAD_FAST                'feature_index'
              114  BUILD_TUPLE_2         2 
              116  BINARY_SUBSCR    
              118  LOAD_METHOD              sum
              120  CALL_METHOD_0         0  '0 positional arguments'
              122  STORE_FAST               'freq_w_not_e'

 L.  32       124  LOAD_FAST                'unit_distribution'
              126  LOAD_DEREF               'sample_index'
              128  BINARY_SUBSCR    
              130  STORE_FAST               'freq_e'

 L.  34       132  LOAD_FAST                'n_total_docs'
              134  LOAD_FAST                'freq_e'
              136  BINARY_SUBTRACT  
              138  STORE_FAST               'freq_not_e'

 L.  36       140  LOAD_FAST                'verbose'
              142  POP_JUMP_IF_FALSE   184  'to 184'

 L.  37       144  LOAD_GLOBAL              logging
              146  LOAD_METHOD              debug
              148  LOAD_STR                 'For feature_index:{} sample_index:{}'
              150  LOAD_METHOD              format
              152  LOAD_FAST                'feature_index'
              154  LOAD_DEREF               'sample_index'
              156  CALL_METHOD_2         2  '2 positional arguments'
              158  CALL_METHOD_1         1  '1 positional argument'
              160  POP_TOP          

 L.  38       162  LOAD_GLOBAL              logging
              164  LOAD_METHOD              debug
              166  LOAD_STR                 'freq_w_e:{} freq_w_not_e:{} freq_e:{} freq_not_e:{}'
              168  LOAD_METHOD              format

 L.  39       170  LOAD_FAST                'freq_w_e'

 L.  40       172  LOAD_FAST                'freq_w_not_e'

 L.  41       174  LOAD_FAST                'freq_e'

 L.  42       176  LOAD_FAST                'freq_not_e'
              178  CALL_METHOD_4         4  '4 positional arguments'
              180  CALL_METHOD_1         1  '1 positional argument'
              182  POP_TOP          
            184_0  COME_FROM           142  '142'

 L.  45       184  LOAD_FAST                'freq_w_e'
              186  LOAD_CONST               0
              188  COMPARE_OP               ==
              190  POP_JUMP_IF_TRUE    216  'to 216'
              192  LOAD_FAST                'freq_w_not_e'
              194  LOAD_CONST               0
              196  COMPARE_OP               ==
              198  POP_JUMP_IF_TRUE    216  'to 216'
              200  LOAD_FAST                'freq_e'
              202  LOAD_CONST               0
              204  COMPARE_OP               ==
              206  POP_JUMP_IF_TRUE    216  'to 216'
              208  LOAD_FAST                'freq_not_e'
              210  LOAD_CONST               0
              212  COMPARE_OP               ==
              214  POP_JUMP_IF_FALSE   220  'to 220'
            216_0  COME_FROM           206  '206'
            216_1  COME_FROM           198  '198'
            216_2  COME_FROM           190  '190'

 L.  46       216  LOAD_CONST               0
              218  RETURN_VALUE     
            220_0  COME_FROM           214  '214'

 L.  48       220  LOAD_GLOBAL              float
              222  LOAD_FAST                'freq_w_e'
              224  CALL_FUNCTION_1       1  '1 positional argument'
              226  LOAD_FAST                'freq_not_e'
              228  BINARY_MULTIPLY  
              230  STORE_FAST               'nominator'

 L.  49       232  LOAD_GLOBAL              float
              234  LOAD_FAST                'freq_e'
              236  CALL_FUNCTION_1       1  '1 positional argument'
              238  LOAD_FAST                'freq_w_not_e'
              240  BINARY_MULTIPLY  
              242  STORE_FAST               'denominator'

 L.  50       244  LOAD_FAST                'nominator'
              246  LOAD_FAST                'denominator'
              248  BINARY_TRUE_DIVIDE
              250  STORE_FAST               'ans'

 L.  51       252  LOAD_GLOBAL              isinstance
              254  LOAD_FAST                'ans'
              256  LOAD_GLOBAL              float
              258  CALL_FUNCTION_2       2  '2 positional arguments'
          260_262  POP_JUMP_IF_TRUE    268  'to 268'
              264  LOAD_ASSERT              AssertionError
              266  RAISE_VARARGS_1       1  'exception instance'
            268_0  COME_FROM           260  '260'

 L.  52       268  LOAD_GLOBAL              math
              270  LOAD_METHOD              log
              272  LOAD_FAST                'ans'
              274  LOAD_CONST               2
              276  CALL_METHOD_2         2  '2 positional arguments'
              278  STORE_FAST               'soa_val'

 L.  53       280  LOAD_FAST                'soa_val'
              282  RETURN_VALUE     

Parse error at or near `LOAD_FAST' instruction at offset 280


class SOA(object):

    def __init__(self):
        pass

    def fit_transform(self, X: Union[(memmap, csr_matrix)], unit_distribution: numpy.ndarray, n_jobs: int=1, verbose=False, joblib_backend: str='multiprocessing', use_cython: bool=False):
        """* What you can do
        - Get SOA weighted-score matrix.
        - You can get fast-speed with Cython
        """
        if not isinstanceX(memmap, csr_matrix):
            raise AssertionError
        else:
            assert isinstanceunit_distributionnumpy.ndarray
            matrix_size = X.shape
            sample_range = list(range0matrix_size[0])
            feature_range = list(range0matrix_size[1])
            n_total_document = sum(unit_distribution)
            logger.debug(msg='Start calculating SOA')
            logger.debug(msg=('size(input_matrix)={} * {}'.formatX.shape[0]X.shape[1]))
            if use_cython:
                import pyximport
                pyximport.install
                from DocumentFeatureSelection.soa.soa_cython import main
                logger.warning(msg='n_jobs parameter is invalid when use_cython=True')
                soa_score_csr_source = main(X=X, n_docs_distribution=unit_distribution,
                  n_total_doc=n_total_document,
                  sample_range=sample_range,
                  feature_range=feature_range,
                  verbose=False)
            else:
                self.soa = soa
            soa_score_csr_source = joblib.Parallel(n_jobs=n_jobs, backend=joblib_backend)((joblib.delayedself.docId_word_soa(X=X, unit_distribution=unit_distribution, feature_index=feature_index, sample_index=sample_index, n_total_doc=n_total_document, verbose=verbose) for sample_index in sample_range for feature_index in feature_range))
        row_list = [t[0] for t in soa_score_csr_source]
        col_list = [t[1] for t in soa_score_csr_source]
        data_list = [t[2] for t in soa_score_csr_source]
        soa_featured_csr_matrix = csr_matrix((data_list, (row_list, col_list)), shape=(
         X.shape[0],
         X.shape[1]))
        logging.debug(msg='End calculating SOA')
        return soa_featured_csr_matrix

    def docId_word_soa(self, X: Union[(memmap, csr_matrix)], unit_distribution: numpy.ndarray, n_total_doc: int, feature_index: int, sample_index: int, verbose=False):
        """
        """
        assert isinstanceX(memmap, csr_matrix)
        assert isinstanceunit_distributionnumpy.ndarray
        assert isinstancefeature_indexint
        assert isinstancesample_indexint
        soa_score = self.soa(X=X,
          unit_distribution=unit_distribution,
          feature_index=feature_index,
          sample_index=sample_index,
          n_total_docs=n_total_doc,
          verbose=verbose)
        return (
         sample_index, feature_index, soa_score)