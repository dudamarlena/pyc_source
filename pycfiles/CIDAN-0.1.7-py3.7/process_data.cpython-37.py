# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/CIDAN/LSSC/process_data.py
# Compiled at: 2020-04-27 03:58:33
# Size of source mod 2**32: 13873 bytes
from CIDAN.LSSC.functions.data_manipulation import load_filter_tif_stack, filter_stack, reshape_to_2d_over_time
from CIDAN.LSSC.functions.roi_extraction import roi_extract_image, merge_rois
from CIDAN.LSSC.functions.embeddings import calc_affinity_matrix
from CIDAN.LSSC.functions.pickle_funcs import pickle_save, pickle_load, pickle_clear, pickle_set_dir, pickle_exist
from CIDAN.LSSC.functions.temporal_correlation import *
from CIDAN.LSSC.functions.eigen import gen_eigen_vectors, save_eigen_vectors, load_eigen_vectors, save_embeding_norm_image, create_embeding_norm_multiple
from dask import delayed
from functools import reduce
import numpy as np
from typing import Union, Any, List, Optional, cast, Tuple, Dict
import CIDAN.LSSC.SpatialBox as SpatialBox
from CIDAN.LSSC.functions.save_test_images import save_eigen_images, save_volume_images, save_roi_images
from dask.distributed import performance_report
import logging
logger1 = logging.getLogger('CIDAN.LSSC.process_data')

def process_data--- This code section failed: ---

 L.  41         0  LOAD_GLOBAL              logger1
                2  LOAD_METHOD              debug

 L.  59         4  LOAD_STR                 'Inputs: num_threads {0},test_images {1}, test_output_dir {2},\n                 save_dir {3}, save_intermediate_steps {4},\n                 load_data {5}, data_path {6},\n                 image_data {7},\n                 eigen_vectors_already_generated {8},\n                 save_embedding_images {9},\n                 total_num_time_steps {10}, total_num_spatial_boxes {11},\n                 spatial_overlap {12}, filter {13}, median_filter {14},\n                 median_filter_size {15},\n                 z_score {16}, slice_stack {17},\n                 slice_every {18}, slice_start {19}, metric {20}, knn {21},\n                 accuracy {22}, connections {23}, normalize_w_k {24}, num_eig {25},\n                 merge {26},\n                 num_rois {27}, refinement {28}, num_eigen_vector_select {29},\n                 max_iter {30}, roi_size_min {31}, fill_holes {32},\n                 elbow_threshold_method {33}, elbow_threshold_value {34},\n                 eigen_threshold_method {35},\n                 eigen_threshold_value {36}, merge_temporal_coef {37},\n                 roi_size_max {38}'
                6  LOAD_METHOD              format
                8  LOAD_FAST                'num_threads'
               10  LOAD_FAST                'test_images'
               12  LOAD_FAST                'test_output_dir'

 L.  60        14  LOAD_FAST                'save_dir'
               16  LOAD_FAST                'save_intermediate_steps'

 L.  61        18  LOAD_FAST                'load_data'
               20  LOAD_FAST                'data_path'

 L.  62        22  LOAD_FAST                'image_data'

 L.  63        24  LOAD_FAST                'eigen_vectors_already_generated'

 L.  64        26  LOAD_FAST                'save_embedding_images'

 L.  65        28  LOAD_DEREF               'total_num_time_steps'
               30  LOAD_DEREF               'total_num_spatial_boxes'

 L.  66        32  LOAD_DEREF               'spatial_overlap'
               34  LOAD_FAST                'filter'
               36  LOAD_FAST                'median_filter'

 L.  67        38  LOAD_FAST                'median_filter_size'

 L.  68        40  LOAD_FAST                'z_score'
               42  LOAD_FAST                'slice_stack'

 L.  69        44  LOAD_FAST                'slice_every'
               46  LOAD_FAST                'slice_start'
               48  LOAD_FAST                'metric'
               50  LOAD_FAST                'knn'

 L.  70        52  LOAD_FAST                'accuracy'
               54  LOAD_FAST                'connections'
               56  LOAD_FAST                'normalize_w_k'
               58  LOAD_FAST                'num_eig'

 L.  71        60  LOAD_FAST                'merge'

 L.  72        62  LOAD_FAST                'num_rois'
               64  LOAD_FAST                'refinement'
               66  LOAD_FAST                'num_eigen_vector_select'

 L.  73        68  LOAD_FAST                'max_iter'
               70  LOAD_FAST                'roi_size_min'
               72  LOAD_FAST                'fill_holes'

 L.  74        74  LOAD_FAST                'elbow_threshold_method'
               76  LOAD_FAST                'elbow_threshold_value'

 L.  75        78  LOAD_FAST                'eigen_threshold_method'

 L.  76        80  LOAD_FAST                'eigen_threshold_value'
               82  LOAD_FAST                'merge_temporal_coef'

 L.  77        84  LOAD_FAST                'roi_size_max'
               86  CALL_METHOD_39       39  '39 positional arguments'
               88  CALL_METHOD_1         1  '1 positional argument'
               90  POP_TOP          

 L.  83        92  LOAD_FAST                'load_data'
               94  LOAD_CONST               True
               96  COMPARE_OP               ==
               98  POP_JUMP_IF_FALSE   126  'to 126'

 L.  84       100  LOAD_GLOBAL              load_filter_tif_stack
              102  LOAD_FAST                'data_path'
              104  LOAD_FAST                'filter'

 L.  85       106  LOAD_FAST                'median_filter'

 L.  86       108  LOAD_FAST                'median_filter_size'

 L.  87       110  LOAD_FAST                'z_score'
              112  LOAD_FAST                'slice_stack'

 L.  88       114  LOAD_FAST                'slice_start'

 L.  89       116  LOAD_FAST                'slice_every'
              118  LOAD_CONST               ('path', 'filter', 'median_filter', 'median_filter_size', 'z_score', 'slice_stack', 'slice_start', 'slice_every')
              120  CALL_FUNCTION_KW_8     8  '8 total positional and keyword args'
              122  STORE_FAST               'image'
              124  JUMP_FORWARD        130  'to 130'
            126_0  COME_FROM            98  '98'

 L.  91       126  LOAD_FAST                'image_data'
              128  STORE_FAST               'image'
            130_0  COME_FROM           124  '124'

 L.  92       130  LOAD_FAST                'test_images'
              132  POP_JUMP_IF_FALSE   146  'to 146'

 L.  93       134  LOAD_GLOBAL              save_volume_images
              136  LOAD_FAST                'image'
              138  LOAD_FAST                'test_output_dir'
              140  LOAD_CONST               ('volume', 'output_dir')
              142  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              144  POP_TOP          
            146_0  COME_FROM           132  '132'

 L.  94       146  LOAD_FAST                'image'
              148  LOAD_ATTR                shape
              150  STORE_DEREF              'shape'

 L.  95       152  LOAD_GLOBAL              logger1
              154  LOAD_METHOD              debug
              156  LOAD_STR                 'image shape {0}'
              158  LOAD_METHOD              format
              160  LOAD_DEREF               'shape'
              162  CALL_METHOD_1         1  '1 positional argument'
              164  CALL_METHOD_1         1  '1 positional argument'
              166  POP_TOP          

 L.  96       168  LOAD_GLOBAL              print
              170  LOAD_STR                 'Creating {} spatial boxes'
              172  LOAD_METHOD              format
              174  LOAD_DEREF               'total_num_spatial_boxes'
              176  CALL_METHOD_1         1  '1 positional argument'
              178  CALL_FUNCTION_1       1  '1 positional argument'
              180  POP_TOP          

 L.  97       182  LOAD_CLOSURE             'shape'
              184  LOAD_CLOSURE             'spatial_overlap'
              186  LOAD_CLOSURE             'total_num_spatial_boxes'
              188  BUILD_TUPLE_3         3 
              190  LOAD_LISTCOMP            '<code_object <listcomp>>'
              192  LOAD_STR                 'process_data.<locals>.<listcomp>'
              194  MAKE_FUNCTION_8          'closure'

 L.  99       196  LOAD_GLOBAL              range
              198  LOAD_DEREF               'total_num_spatial_boxes'
              200  CALL_FUNCTION_1       1  '1 positional argument'
              202  GET_ITER         
              204  CALL_FUNCTION_1       1  '1 positional argument'
              206  STORE_FAST               'spatial_boxes'

 L. 100       208  BUILD_LIST_0          0 
              210  STORE_FAST               'all_rois'

 L. 101       212  BUILD_LIST_0          0 
              214  STORE_FAST               'all_boxes_eigen_vectors'

 L. 102   216_218  SETUP_LOOP          628  'to 628'
              220  LOAD_FAST                'spatial_boxes'
              222  GET_ITER         
          224_226  FOR_ITER            626  'to 626'
              228  STORE_FAST               'spatial_box'

 L. 103       230  LOAD_FAST                'spatial_box'
              232  LOAD_METHOD              extract_box
              234  LOAD_FAST                'image'
              236  CALL_METHOD_1         1  '1 positional argument'
              238  STORE_FAST               'spatial_box_data'

 L. 104       240  LOAD_CLOSURE             'shape'
              242  LOAD_CLOSURE             'total_num_time_steps'
              244  BUILD_TUPLE_2         2 
              246  LOAD_LISTCOMP            '<code_object <listcomp>>'
              248  LOAD_STR                 'process_data.<locals>.<listcomp>'
              250  MAKE_FUNCTION_8          'closure'

 L. 106       252  LOAD_GLOBAL              range
              254  LOAD_DEREF               'total_num_time_steps'
              256  CALL_FUNCTION_1       1  '1 positional argument'
              258  GET_ITER         
              260  CALL_FUNCTION_1       1  '1 positional argument'
              262  STORE_FAST               'time_boxes'

 L. 107       264  BUILD_LIST_0          0 
              266  STORE_FAST               'all_eigen_vectors_list'

 L. 108       268  LOAD_FAST                'eigen_vectors_already_generated'
          270_272  POP_JUMP_IF_TRUE    460  'to 460'

 L. 109       274  SETUP_LOOP          502  'to 502'
              276  LOAD_GLOBAL              enumerate
              278  LOAD_FAST                'time_boxes'
              280  CALL_FUNCTION_1       1  '1 positional argument'
              282  GET_ITER         
            284_0  COME_FROM           448  '448'
              284  FOR_ITER            456  'to 456'
              286  UNPACK_SEQUENCE_2     2 
              288  STORE_FAST               'temporal_box_num'
              290  STORE_FAST               'start_end'

 L. 110       292  LOAD_FAST                'start_end'
              294  UNPACK_SEQUENCE_2     2 
              296  STORE_FAST               'start'
              298  STORE_FAST               'end'

 L. 112       300  LOAD_FAST                'spatial_box_data'
              302  LOAD_FAST                'start'
              304  LOAD_FAST                'end'
              306  BUILD_SLICE_2         2 
              308  LOAD_CONST               None
              310  LOAD_CONST               None
              312  BUILD_SLICE_2         2 
              314  LOAD_CONST               None
              316  LOAD_CONST               None
              318  BUILD_SLICE_2         2 
              320  BUILD_TUPLE_3         3 
              322  BINARY_SUBSCR    
              324  STORE_FAST               'time_box_data'

 L. 113       326  LOAD_GLOBAL              reshape_to_2d_over_time
              328  LOAD_FAST                'time_box_data'
              330  CALL_FUNCTION_1       1  '1 positional argument'
              332  STORE_FAST               'time_box_data_2d'

 L. 114       334  LOAD_GLOBAL              logger1
              336  LOAD_METHOD              debug
              338  LOAD_STR                 'Time box {0}, start {1}, end {2}, time_box shape {3}, 2d shape {4}'
              340  LOAD_METHOD              format
              342  LOAD_FAST                'temporal_box_num'
              344  LOAD_FAST                'start'
              346  LOAD_FAST                'end'
              348  LOAD_FAST                'time_box_data'
              350  LOAD_ATTR                shape
              352  LOAD_FAST                'time_box_data_2d'
              354  LOAD_ATTR                shape
              356  CALL_METHOD_5         5  '5 positional arguments'
              358  CALL_METHOD_1         1  '1 positional argument'
              360  POP_TOP          

 L. 115       362  LOAD_GLOBAL              calc_affinity_matrix
              364  LOAD_FAST                'time_box_data_2d'
              366  LOAD_FAST                'metric'

 L. 116       368  LOAD_FAST                'knn'
              370  LOAD_FAST                'accuracy'

 L. 117       372  LOAD_FAST                'connections'

 L. 118       374  LOAD_FAST                'normalize_w_k'

 L. 119       376  LOAD_FAST                'num_threads'
              378  LOAD_FAST                'spatial_box'
              380  LOAD_ATTR                box_num
              382  LOAD_FAST                'temporal_box_num'
              384  LOAD_CONST               ('pixel_list', 'metric', 'knn', 'accuracy', 'connections', 'normalize_w_k', 'num_threads', 'spatial_box_num', 'temporal_box_num')
              386  CALL_FUNCTION_KW_9     9  '9 total positional and keyword args'
              388  STORE_FAST               'k'

 L. 120       390  LOAD_GLOBAL              gen_eigen_vectors
              392  LOAD_FAST                'k'

 L. 121       394  LOAD_FAST                'num_eig'

 L. 122       396  LOAD_DEREF               'total_num_time_steps'
              398  BINARY_FLOOR_DIVIDE
              400  LOAD_FAST                'spatial_box'
              402  LOAD_ATTR                box_num
              404  LOAD_FAST                'temporal_box_num'
              406  LOAD_CONST               ('K', 'num_eig', 'spatial_box_num', 'temporal_box_num')
              408  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              410  STORE_FAST               'eigen_vectors'

 L. 123       412  LOAD_FAST                'save_intermediate_steps'
          414_416  POP_JUMP_IF_FALSE   436  'to 436'

 L. 124       418  LOAD_GLOBAL              save_eigen_vectors
              420  LOAD_FAST                'eigen_vectors'

 L. 125       422  LOAD_FAST                'spatial_box'
              424  LOAD_ATTR                box_num

 L. 126       426  LOAD_FAST                'temporal_box_num'
              428  LOAD_FAST                'save_dir'
              430  LOAD_CONST               ('e_vectors', 'spatial_box_num', 'time_box_num', 'save_dir')
              432  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              434  STORE_FAST               'eigen_vectors'
            436_0  COME_FROM           414  '414'

 L. 128       436  LOAD_FAST                'all_eigen_vectors_list'
              438  LOAD_METHOD              append
              440  LOAD_FAST                'eigen_vectors'
              442  CALL_METHOD_1         1  '1 positional argument'
              444  POP_TOP          

 L. 129       446  LOAD_FAST                'test_images'
          448_450  POP_JUMP_IF_FALSE   284  'to 284'

 L. 130   452_454  JUMP_BACK           284  'to 284'
              456  POP_BLOCK        
              458  JUMP_FORWARD        502  'to 502'
            460_0  COME_FROM           270  '270'

 L. 137       460  SETUP_LOOP          502  'to 502'
              462  LOAD_GLOBAL              range
              464  LOAD_DEREF               'total_num_time_steps'
              466  CALL_FUNCTION_1       1  '1 positional argument'
              468  GET_ITER         
              470  FOR_ITER            500  'to 500'
              472  STORE_FAST               'temporal_box_num'

 L. 138       474  LOAD_FAST                'all_eigen_vectors_list'
              476  LOAD_METHOD              append
              478  LOAD_GLOBAL              load_eigen_vectors
              480  LOAD_FAST                'spatial_box'
              482  LOAD_ATTR                box_num

 L. 139       484  LOAD_FAST                'temporal_box_num'

 L. 140       486  LOAD_FAST                'save_dir'
              488  LOAD_CONST               ('spatial_box_num', 'time_box_num', 'save_dir')
              490  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              492  CALL_METHOD_1         1  '1 positional argument'
              494  POP_TOP          
          496_498  JUMP_BACK           470  'to 470'
              500  POP_BLOCK        
            502_0  COME_FROM_LOOP      460  '460'
            502_1  COME_FROM           458  '458'
            502_2  COME_FROM_LOOP      274  '274'

 L. 142       502  LOAD_GLOBAL              delayed
              504  LOAD_GLOBAL              np
              506  LOAD_ATTR                hstack
              508  CALL_FUNCTION_1       1  '1 positional argument'
              510  LOAD_FAST                'all_eigen_vectors_list'
              512  CALL_FUNCTION_1       1  '1 positional argument'
              514  STORE_FAST               'all_eigen_vectors'

 L. 143       516  LOAD_FAST                'all_boxes_eigen_vectors'
              518  LOAD_METHOD              append
              520  LOAD_FAST                'all_eigen_vectors'
              522  CALL_METHOD_1         1  '1 positional argument'
              524  POP_TOP          

 L. 144       526  LOAD_FAST                'save_embedding_images'
          528_530  POP_JUMP_IF_FALSE   552  'to 552'

 L. 145       532  LOAD_GLOBAL              save_embeding_norm_image
              534  LOAD_FAST                'all_eigen_vectors'

 L. 146       536  LOAD_FAST                'spatial_box'
              538  LOAD_ATTR                shape

 L. 147       540  LOAD_FAST                'save_dir'

 L. 148       542  LOAD_FAST                'spatial_box'
              544  LOAD_ATTR                box_num
              546  LOAD_CONST               ('e_vectors', 'image_shape', 'save_dir', 'spatial_box_num')
              548  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              550  STORE_FAST               'all_eigen_vectors'
            552_0  COME_FROM           528  '528'

 L. 150       552  LOAD_GLOBAL              roi_extract_image
              554  LOAD_FAST                'all_eigen_vectors'

 L. 151       556  LOAD_FAST                'spatial_box_data'
              558  LOAD_ATTR                shape

 L. 152       560  LOAD_GLOBAL              reshape_to_2d_over_time

 L. 153       562  LOAD_FAST                'spatial_box_data'
              564  CALL_FUNCTION_1       1  '1 positional argument'

 L. 154       566  LOAD_FAST                'merge'

 L. 155       568  LOAD_FAST                'num_rois'
              570  LOAD_FAST                'refinement'

 L. 156       572  LOAD_FAST                'num_eigen_vector_select'

 L. 157       574  LOAD_FAST                'max_iter'

 L. 158       576  LOAD_FAST                'roi_size_min'

 L. 159       578  LOAD_FAST                'fill_holes'

 L. 160       580  LOAD_FAST                'elbow_threshold_method'

 L. 161       582  LOAD_FAST                'elbow_threshold_value'

 L. 162       584  LOAD_FAST                'eigen_threshold_method'

 L. 163       586  LOAD_FAST                'eigen_threshold_value'

 L. 164       588  LOAD_FAST                'merge_temporal_coef'

 L. 165       590  LOAD_FAST                'roi_size_max'
              592  LOAD_FAST                'spatial_box'
              594  LOAD_ATTR                box_num
              596  LOAD_CONST               ('e_vectors', 'original_shape', 'original_2d_vol', 'merge', 'num_rois', 'refinement', 'num_eigen_vector_select', 'max_iter', 'roi_size_min', 'fill_holes', 'elbow_threshold_method', 'elbow_threshold_value', 'eigen_threshold_method', 'eigen_threshold_value', 'merge_temporal_coef', 'roi_size_limit', 'box_num')
              598  CALL_FUNCTION_KW_17    17  '17 total positional and keyword args'
              600  STORE_FAST               'rois'

 L. 166       602  LOAD_FAST                'test_images'
          604_606  POP_JUMP_IF_FALSE   608  'to 608'
            608_0  COME_FROM           604  '604'

 L. 173       608  LOAD_FAST                'all_rois'
              610  LOAD_METHOD              append
              612  LOAD_FAST                'spatial_box'
              614  LOAD_METHOD              redefine_spatial_cord_1d
              616  LOAD_FAST                'rois'
              618  CALL_METHOD_1         1  '1 positional argument'
              620  CALL_METHOD_1         1  '1 positional argument'
              622  POP_TOP          
              624  JUMP_BACK           224  'to 224'
              626  POP_BLOCK        
            628_0  COME_FROM_LOOP      216  '216'

 L. 174       628  LOAD_GLOBAL              delayed
              630  LOAD_GLOBAL              reduce
              632  CALL_FUNCTION_1       1  '1 positional argument'
              634  LOAD_LAMBDA              '<code_object <lambda>>'
              636  LOAD_STR                 'process_data.<locals>.<lambda>'
              638  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              640  LOAD_FAST                'all_rois'
              642  CALL_FUNCTION_2       2  '2 positional arguments'
              644  STORE_FAST               'all_rois'

 L. 175       646  LOAD_FAST                'all_rois'
              648  LOAD_METHOD              compute
              650  CALL_METHOD_0         0  '0 positional arguments'
              652  STORE_FAST               'all_rois'

 L. 176       654  LOAD_GLOBAL              delayed
              656  LOAD_GLOBAL              merge_rois
              658  CALL_FUNCTION_1       1  '1 positional argument'
              660  LOAD_FAST                'all_rois'

 L. 177       662  LOAD_FAST                'merge_temporal_coef'

 L. 178       664  LOAD_GLOBAL              reshape_to_2d_over_time

 L. 179       666  LOAD_FAST                'image'
              668  CALL_FUNCTION_1       1  '1 positional argument'
              670  LOAD_CONST               ('roi_list', 'temporal_coefficient', 'original_2d_vol')
              672  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              674  LOAD_METHOD              compute
              676  CALL_METHOD_0         0  '0 positional arguments'
              678  STORE_FAST               'all_rois_merged'

 L. 181       680  LOAD_FAST                'test_images'
          682_684  POP_JUMP_IF_FALSE   710  'to 710'

 L. 182       686  LOAD_GLOBAL              delayed
              688  LOAD_GLOBAL              save_roi_images
              690  CALL_FUNCTION_1       1  '1 positional argument'
              692  LOAD_FAST                'all_rois_merged'

 L. 183       694  LOAD_FAST                'test_output_dir'

 L. 184       696  LOAD_DEREF               'shape'
              698  LOAD_STR                 'all'
              700  LOAD_CONST               ('roi_list', 'output_dir', 'image_shape', 'box_num')
              702  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              704  LOAD_METHOD              compute
              706  CALL_METHOD_0         0  '0 positional arguments'
              708  POP_TOP          
            710_0  COME_FROM           682  '682'

 L. 185       710  LOAD_FAST                'save_embedding_images'
          712_714  POP_JUMP_IF_FALSE   736  'to 736'
              716  LOAD_FAST                'save_intermediate_steps'
          718_720  POP_JUMP_IF_FALSE   736  'to 736'

 L. 186       722  LOAD_GLOBAL              create_embeding_norm_multiple
              724  LOAD_FAST                'spatial_boxes'
              726  LOAD_FAST                'save_dir'
              728  LOAD_DEREF               'total_num_time_steps'
              730  LOAD_CONST               ('spatial_box_list', 'save_dir', 'num_time_steps')
              732  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              734  POP_TOP          
            736_0  COME_FROM           718  '718'
            736_1  COME_FROM           712  '712'

 L. 189       736  LOAD_FAST                'all_rois_merged'
              738  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_BLOCK' instruction at offset 456


if __name__ == '__main__':
    process_data(num_threads=1, load_data=True, data_path='/Users/sschickler/Code Devel/LSSC-python/input_images/small_dataset.tif',
      test_images=True,
      save_dir='/Users/sschickler/Code Devel/LSSC-python/output_images/15',
      save_intermediate_steps=False,
      eigen_vectors_already_generated=False,
      save_embedding_images=False,
      test_output_dir='/Users/sschickler/Code Devel/LSSC-python/output_images/15',
      image_data=None,
      total_num_time_steps=4,
      total_num_spatial_boxes=4,
      spatial_overlap=10,
      filter=True,
      median_filter_size=(1, 3, 3),
      median_filter=True,
      z_score=False,
      slice_stack=False,
      slice_every=10,
      slice_start=0,
      metric='l2',
      knn=50,
      accuracy=59,
      connections=60,
      num_eig=50,
      normalize_w_k=2,
      merge=True,
      num_rois=25,
      refinement=True,
      num_eigen_vector_select=5,
      max_iter=400,
      roi_size_min=30,
      fill_holes=True,
      elbow_threshold_method=True,
      elbow_threshold_value=1,
      eigen_threshold_method=True,
      eigen_threshold_value=0.5,
      merge_temporal_coef=0.01,
      roi_size_max=600)