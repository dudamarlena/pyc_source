# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/ml\vision\_models\semantic_seg\change_detection.py
# Compiled at: 2019-12-31 04:09:04
# Size of source mod 2**32: 11296 bytes
"""
@author: YangRuijie
@license: 
@contact: yangruijie@supermap.com
@software: 
@file: change_detection.py
@time: 7/23/19 6:14 AM
@desc:
"""
import os, tempfile, rasterio
from rasterio.plot import reshape_as_image, reshape_as_raster
from rasterio.windows import Window
import numpy as np
from ..... import import_tif, raster_to_vector, DatasetType
from _jsuperpy.data._util import get_output_datasource, check_output_datasource
from toolkit._toolkit import stretch_n, stretch_min_max, view_bar, get_input_dataset
from .base_keras_models import Estimation

class ChangeEstimation(Estimation):

    def __init__(self, model_path, config):
        super().__init__(model_path, config)
        self.model_input = config.ModelInput[0]
        self.model_output = config.ModelOutput[0]
        if np.argmin(self.model_input.Shape) == 0:
            self.band_order = 'first'
            self.seg_size = self.model_input.Shape[1]
            self.out_width_height = [self.model_output.Shape[1], self.model_output.Shape[2]]
            self.output_msk_num = self.model_output.Shape[0]
            if self.model_input.Shape[1] != self.model_input.Shape[2]:
                raise ValueError('Model input width and height should be equal!')
        else:
            self.band_order = 'last'
            self.seg_size = self.model_input.Shape[1]
            self.out_width_height = [self.model_output.Shape[0], self.model_output.Shape[1]]
            self.output_msk_num = self.model_output.Shape[(-1)]
            if self.model_input.Shape[1] != self.model_input.Shape[0]:
                raise ValueError('Model input width and height should be equal!')
        self.is_stretch = config.IsStretch
        self.model_path = model_path

    def estimate_img(self, before_img, after_image, coversize, out_ds, out_dataset_name, **kwargs):
        self.half_oversize = coversize
        self._predict_with_rasterio(before_img, after_image, out_ds, out_dataset_name)

    def _predict_with_rasterio--- This code section failed: ---

 L.  67         0  LOAD_FAST                'self'
                2  LOAD_ATTR                half_oversize
                4  LOAD_CONST               2
                6  BINARY_MULTIPLY  
                8  STORE_FAST               'coversize'

 L.  68        10  LOAD_FAST                'self'
               12  LOAD_ATTR                seg_size
               14  STORE_FAST               'blocksize'

 L.  69        16  LOAD_FAST                'coversize'
               18  LOAD_CONST               2
               20  BINARY_MODULO    
               22  LOAD_CONST               0
               24  COMPARE_OP               !=
               26  POP_JUMP_IF_FALSE    38  'to 38'

 L.  70        28  LOAD_GLOBAL              ValueError
               30  LOAD_STR                 'coversize must be even number!'
               32  CALL_FUNCTION_1       1  '1 positional argument'
               34  RAISE_VARARGS_1       1  'exception instance'
               36  JUMP_FORWARD         74  'to 74'
             38_0  COME_FROM            26  '26'

 L.  71        38  LOAD_FAST                'coversize'
               40  LOAD_FAST                'blocksize'
               42  COMPARE_OP               ==
               44  POP_JUMP_IF_FALSE    56  'to 56'

 L.  72        46  LOAD_GLOBAL              ValueError
               48  LOAD_STR                 'coversize and blocksize is same!'
               50  CALL_FUNCTION_1       1  '1 positional argument'
               52  RAISE_VARARGS_1       1  'exception instance'
               54  JUMP_FORWARD         74  'to 74'
             56_0  COME_FROM            44  '44'

 L.  73        56  LOAD_FAST                'coversize'
               58  LOAD_FAST                'blocksize'
               60  COMPARE_OP               >
               62  POP_JUMP_IF_FALSE    74  'to 74'

 L.  74        64  LOAD_GLOBAL              ValueError
               66  LOAD_STR                 'coversize is bigger than blocksize!'
               68  CALL_FUNCTION_1       1  '1 positional argument'
               70  RAISE_VARARGS_1       1  'exception instance'
               72  JUMP_FORWARD         74  'to 74'
             74_0  COME_FROM            72  '72'
             74_1  COME_FROM            62  '62'
             74_2  COME_FROM            54  '54'
             74_3  COME_FROM            36  '36'

 L.  78        74  LOAD_FAST                'blocksize'
               76  LOAD_FAST                'coversize'
               78  BINARY_SUBTRACT  
               80  STORE_FAST               'uncoversize'

 L.  80        82  LOAD_GLOBAL              rasterio
               84  LOAD_METHOD              open
               86  LOAD_FAST                'before_img'
               88  CALL_METHOD_1         1  '1 positional argument'
            90_92  SETUP_WITH         2158  'to 2158'
               94  STORE_FAST               'b_ds'

 L.  81        96  LOAD_GLOBAL              rasterio
               98  LOAD_METHOD              open
              100  LOAD_FAST                'after_image'
              102  CALL_METHOD_1         1  '1 positional argument'
          104_106  SETUP_WITH         2148  'to 2148'
              108  STORE_FAST               'a_ds'

 L.  82       110  LOAD_FAST                'a_ds'
              112  LOAD_ATTR                width
              114  LOAD_FAST                'b_ds'
              116  LOAD_ATTR                width
              118  COMPARE_OP               ==
              120  POP_JUMP_IF_FALSE   134  'to 134'
              122  LOAD_FAST                'a_ds'
              124  LOAD_ATTR                height
              126  LOAD_FAST                'b_ds'
              128  LOAD_ATTR                height
              130  COMPARE_OP               ==
              132  POP_JUMP_IF_TRUE    142  'to 142'
            134_0  COME_FROM           120  '120'
              134  LOAD_ASSERT              AssertionError
              136  LOAD_STR                 'the width and height between before and after should be equal'
              138  CALL_FUNCTION_1       1  '1 positional argument'
              140  RAISE_VARARGS_1       1  'exception instance'
            142_0  COME_FROM           132  '132'

 L.  84       142  LOAD_FAST                'b_ds'
              144  LOAD_ATTR                width
              146  LOAD_FAST                'coversize'
              148  LOAD_CONST               2
              150  BINARY_FLOOR_DIVIDE
              152  BINARY_SUBTRACT  
              154  LOAD_FAST                'uncoversize'
              156  BINARY_FLOOR_DIVIDE
              158  STORE_FAST               'width_block'

 L.  85       160  LOAD_FAST                'b_ds'
              162  LOAD_ATTR                height
              164  LOAD_FAST                'coversize'
              166  LOAD_CONST               2
              168  BINARY_FLOOR_DIVIDE
              170  BINARY_SUBTRACT  
              172  LOAD_FAST                'uncoversize'
              174  BINARY_FLOOR_DIVIDE
              176  STORE_FAST               'height_block'

 L.  87       178  LOAD_GLOBAL              os
              180  LOAD_ATTR                path
              182  LOAD_METHOD              join
              184  LOAD_GLOBAL              tempfile
              186  LOAD_METHOD              mkdtemp
              188  CALL_METHOD_0         0  '0 positional arguments'
              190  LOAD_STR                 'tmp.tif'
              192  CALL_METHOD_2         2  '2 positional arguments'
              194  STORE_FAST               'tmp_file'

 L.  88       196  LOAD_GLOBAL              rasterio
              198  LOAD_ATTR                open
              200  LOAD_FAST                'tmp_file'
              202  LOAD_STR                 'w'
              204  LOAD_STR                 'GTiff'
              206  LOAD_FAST                'a_ds'
              208  LOAD_ATTR                width
              210  LOAD_FAST                'a_ds'
              212  LOAD_ATTR                height

 L.  89       214  LOAD_CONST               1
              216  LOAD_FAST                'a_ds'
              218  LOAD_ATTR                bounds
              220  LOAD_FAST                'a_ds'
              222  LOAD_ATTR                crs
              224  LOAD_FAST                'a_ds'
              226  LOAD_ATTR                transform
              228  LOAD_GLOBAL              np
              230  LOAD_ATTR                uint8
              232  LOAD_CONST               ('driver', 'width', 'height', 'count', 'bounds', 'crs', 'transform', 'dtype')
              234  CALL_FUNCTION_KW_10    10  '10 total positional and keyword args'
              236  STORE_FAST               'dst'

 L.  90       238  LOAD_CONST               0
              240  STORE_FAST               'p'

 L.  91   242_244  SETUP_LOOP         1894  'to 1894'
              246  LOAD_GLOBAL              range
              248  LOAD_FAST                'height_block'
              250  LOAD_CONST               1
              252  BINARY_ADD       
              254  CALL_FUNCTION_1       1  '1 positional argument'
              256  GET_ITER         
          258_260  FOR_ITER           1892  'to 1892'
              262  STORE_FAST               'i'

 L.  92   264_266  SETUP_LOOP         1888  'to 1888'
              268  LOAD_GLOBAL              range
              270  LOAD_FAST                'width_block'
              272  LOAD_CONST               1
              274  BINARY_ADD       
              276  CALL_FUNCTION_1       1  '1 positional argument'
              278  GET_ITER         
          280_282  FOR_ITER           1886  'to 1886'
              284  STORE_FAST               'j'

 L.  95       286  LOAD_GLOBAL              np
              288  LOAD_ATTR                zeros
              290  LOAD_CONST               3
              292  LOAD_FAST                'blocksize'
              294  LOAD_FAST                'blocksize'
              296  BUILD_LIST_3          3 
              298  LOAD_GLOBAL              np
              300  LOAD_ATTR                float64
              302  LOAD_CONST               ('dtype',)
              304  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              306  STORE_FAST               'b_block'

 L.  96       308  LOAD_GLOBAL              np
              310  LOAD_ATTR                zeros
              312  LOAD_CONST               3
              314  LOAD_FAST                'blocksize'
              316  LOAD_FAST                'blocksize'
              318  BUILD_LIST_3          3 
              320  LOAD_GLOBAL              np
              322  LOAD_ATTR                float64
              324  LOAD_CONST               ('dtype',)
              326  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              328  STORE_FAST               'a_block'

 L.  97       330  LOAD_FAST                'b_ds'
              332  LOAD_ATTR                read
              334  LOAD_GLOBAL              Window
              336  LOAD_FAST                'j'
              338  LOAD_FAST                'uncoversize'
              340  BINARY_MULTIPLY  
              342  LOAD_FAST                'i'
              344  LOAD_FAST                'uncoversize'
              346  BINARY_MULTIPLY  
              348  LOAD_FAST                'blocksize'
              350  LOAD_FAST                'blocksize'
              352  CALL_FUNCTION_4       4  '4 positional arguments'
              354  LOAD_CONST               ('window',)
              356  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              358  STORE_FAST               'b_img'

 L.  98       360  LOAD_FAST                'a_ds'
              362  LOAD_ATTR                read
              364  LOAD_GLOBAL              Window
              366  LOAD_FAST                'j'
              368  LOAD_FAST                'uncoversize'
              370  BINARY_MULTIPLY  
              372  LOAD_FAST                'i'
              374  LOAD_FAST                'uncoversize'
              376  BINARY_MULTIPLY  
              378  LOAD_FAST                'blocksize'
              380  LOAD_FAST                'blocksize'
              382  CALL_FUNCTION_4       4  '4 positional arguments'
              384  LOAD_CONST               ('window',)
              386  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              388  STORE_FAST               'a_img'

 L.  99       390  LOAD_FAST                'b_img'
              392  LOAD_CONST               None
              394  LOAD_CONST               None
              396  BUILD_SLICE_2         2 
              398  LOAD_CONST               None
              400  LOAD_CONST               None
              402  BUILD_SLICE_2         2 
              404  LOAD_CONST               None
              406  LOAD_CONST               None
              408  BUILD_SLICE_2         2 
              410  BUILD_TUPLE_3         3 
              412  BINARY_SUBSCR    
              414  LOAD_FAST                'b_block'
              416  LOAD_CONST               None
              418  LOAD_CONST               None
              420  BUILD_SLICE_2         2 
              422  LOAD_CONST               None
              424  LOAD_FAST                'b_img'
              426  LOAD_ATTR                shape
              428  LOAD_CONST               1
              430  BINARY_SUBSCR    
              432  BUILD_SLICE_2         2 
              434  LOAD_CONST               None
              436  LOAD_FAST                'b_img'
              438  LOAD_ATTR                shape
              440  LOAD_CONST               2
              442  BINARY_SUBSCR    
              444  BUILD_SLICE_2         2 
              446  BUILD_TUPLE_3         3 
              448  STORE_SUBSCR     

 L. 100       450  LOAD_FAST                'a_img'
              452  LOAD_CONST               None
              454  LOAD_CONST               None
              456  BUILD_SLICE_2         2 
              458  LOAD_CONST               None
              460  LOAD_CONST               None
              462  BUILD_SLICE_2         2 
              464  LOAD_CONST               None
              466  LOAD_CONST               None
              468  BUILD_SLICE_2         2 
              470  BUILD_TUPLE_3         3 
              472  BINARY_SUBSCR    
              474  LOAD_FAST                'a_block'
              476  LOAD_CONST               None
              478  LOAD_CONST               None
              480  BUILD_SLICE_2         2 
              482  LOAD_CONST               None
              484  LOAD_FAST                'a_img'
              486  LOAD_ATTR                shape
              488  LOAD_CONST               1
              490  BINARY_SUBSCR    
              492  BUILD_SLICE_2         2 
              494  LOAD_CONST               None
              496  LOAD_FAST                'a_img'
              498  LOAD_ATTR                shape
              500  LOAD_CONST               2
              502  BINARY_SUBSCR    
              504  BUILD_SLICE_2         2 
              506  BUILD_TUPLE_3         3 
              508  STORE_SUBSCR     

 L. 102       510  LOAD_FAST                'self'
              512  LOAD_ATTR                is_stretch
          514_516  POP_JUMP_IF_FALSE   558  'to 558'

 L. 103       518  LOAD_STR                 'all_max'
              520  LOAD_GLOBAL              dir
              522  CALL_FUNCTION_0       0  '0 positional arguments'
              524  COMPARE_OP               not-in
          526_528  POP_JUMP_IF_TRUE    542  'to 542'
              530  LOAD_STR                 'all_min'
              532  LOAD_GLOBAL              dir
              534  CALL_FUNCTION_0       0  '0 positional arguments'
              536  COMPARE_OP               not-in
          538_540  POP_JUMP_IF_FALSE   558  'to 558'
            542_0  COME_FROM           526  '526'

 L. 104       542  LOAD_GLOBAL              stretch_n
              544  LOAD_FAST                'b_block'
              546  CALL_FUNCTION_1       1  '1 positional argument'
              548  STORE_FAST               'b_block'

 L. 105       550  LOAD_GLOBAL              stretch_n
              552  LOAD_FAST                'a_block'
              554  CALL_FUNCTION_1       1  '1 positional argument'
              556  STORE_FAST               'a_block'
            558_0  COME_FROM           538  '538'
            558_1  COME_FROM           514  '514'

 L. 106       558  LOAD_GLOBAL              reshape_as_image
              560  LOAD_FAST                'b_block'
              562  CALL_FUNCTION_1       1  '1 positional argument'
              564  STORE_FAST               'b_block'

 L. 107       566  LOAD_GLOBAL              reshape_as_image
              568  LOAD_FAST                'a_block'
              570  CALL_FUNCTION_1       1  '1 positional argument'
              572  STORE_FAST               'a_block'

 L. 108       574  LOAD_FAST                'b_block'
              576  LOAD_GLOBAL              np
              578  LOAD_ATTR                newaxis
              580  LOAD_CONST               None
              582  LOAD_CONST               None
              584  BUILD_SLICE_2         2 
              586  LOAD_CONST               None
              588  LOAD_CONST               None
              590  BUILD_SLICE_2         2 
              592  LOAD_CONST               None
              594  LOAD_CONST               None
              596  BUILD_SLICE_2         2 
              598  BUILD_TUPLE_4         4 
              600  BINARY_SUBSCR    
              602  STORE_FAST               'b_block'

 L. 109       604  LOAD_FAST                'a_block'
              606  LOAD_GLOBAL              np
              608  LOAD_ATTR                newaxis
              610  LOAD_CONST               None
              612  LOAD_CONST               None
              614  BUILD_SLICE_2         2 
              616  LOAD_CONST               None
              618  LOAD_CONST               None
              620  BUILD_SLICE_2         2 
              622  LOAD_CONST               None
              624  LOAD_CONST               None
              626  BUILD_SLICE_2         2 
              628  BUILD_TUPLE_4         4 
              630  BINARY_SUBSCR    
              632  STORE_FAST               'a_block'

 L. 112       634  LOAD_FAST                'b_block'
              636  LOAD_ATTR                shape
              638  LOAD_CONST               0
              640  BINARY_SUBSCR    
              642  LOAD_FAST                'self'
              644  LOAD_ATTR                out_width_height
              646  LOAD_CONST               0
              648  BINARY_SUBSCR    
              650  LOAD_FAST                'self'
              652  LOAD_ATTR                out_width_height
              654  LOAD_CONST               1
              656  BINARY_SUBSCR    
              658  LOAD_FAST                'self'
              660  LOAD_ATTR                output_msk_num
              662  BUILD_TUPLE_4         4 
              664  STORE_FAST               'out_shape'

 L. 113       666  LOAD_FAST                'self'
              668  LOAD_METHOD              _predict_tile_local
              670  LOAD_FAST                'b_block'
              672  LOAD_FAST                'out_shape'
              674  CALL_METHOD_2         2  '2 positional arguments'
              676  STORE_FAST               'b_mask_block'

 L. 114       678  LOAD_FAST                'self'
              680  LOAD_METHOD              _predict_tile_local
              682  LOAD_FAST                'a_block'
              684  LOAD_FAST                'out_shape'
              686  CALL_METHOD_2         2  '2 positional arguments'
              688  STORE_FAST               'a_mask_block'

 L. 116       690  LOAD_FAST                'a_mask_block'
              692  LOAD_FAST                'single_thresold'
              694  COMPARE_OP               >
              696  LOAD_METHOD              astype
              698  LOAD_GLOBAL              np
              700  LOAD_ATTR                int8
              702  CALL_METHOD_1         1  '1 positional argument'

 L. 117       704  LOAD_FAST                'b_mask_block'
              706  LOAD_FAST                'single_thresold'
              708  COMPARE_OP               >
              710  LOAD_METHOD              astype
              712  LOAD_GLOBAL              np
              714  LOAD_ATTR                int8
              716  CALL_METHOD_1         1  '1 positional argument'
              718  BINARY_SUBTRACT  
              720  STORE_FAST               'mask_block'

 L. 118       722  LOAD_CONST               0
              724  LOAD_FAST                'mask_block'
              726  LOAD_FAST                'mask_block'
              728  LOAD_CONST               1
              730  COMPARE_OP               !=
              732  STORE_SUBSCR     

 L. 119       734  LOAD_GLOBAL              np
              736  LOAD_ATTR                squeeze
              738  LOAD_FAST                'mask_block'
              740  LOAD_CONST               0
              742  LOAD_CONST               ('axis',)
              744  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              746  STORE_FAST               'mask_block'

 L. 120       748  LOAD_FAST                'self'
              750  LOAD_ATTR                output_msk_num
              752  LOAD_CONST               1
              754  COMPARE_OP               >
          756_758  POP_JUMP_IF_FALSE   796  'to 796'

 L. 121       760  LOAD_GLOBAL              np
              762  LOAD_ATTR                argmax
              764  LOAD_FAST                'mask_block'
              766  LOAD_CONST               -1
              768  LOAD_CONST               ('axis',)
              770  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              772  LOAD_CONST               None
              774  LOAD_CONST               None
              776  BUILD_SLICE_2         2 
              778  LOAD_CONST               None
              780  LOAD_CONST               None
              782  BUILD_SLICE_2         2 
              784  LOAD_GLOBAL              np
              786  LOAD_ATTR                newaxis
              788  BUILD_TUPLE_3         3 
              790  BINARY_SUBSCR    
              792  STORE_FAST               'mask_int'
              794  JUMP_FORWARD        804  'to 804'
            796_0  COME_FROM           756  '756'

 L. 123       796  LOAD_FAST                'mask_block'
              798  LOAD_FAST                'single_thresold'
              800  COMPARE_OP               >
              802  STORE_FAST               'mask_int'
            804_0  COME_FROM           794  '794'

 L. 124       804  LOAD_FAST                'mask_int'
              806  LOAD_METHOD              astype
              808  LOAD_GLOBAL              np
              810  LOAD_ATTR                uint8
              812  CALL_METHOD_1         1  '1 positional argument'
              814  STORE_FAST               'mask_int'

 L. 127       816  LOAD_GLOBAL              reshape_as_raster
              818  LOAD_FAST                'mask_int'
              820  CALL_FUNCTION_1       1  '1 positional argument'
              822  STORE_FAST               'block'

 L. 130       824  LOAD_FAST                'i'
              826  LOAD_CONST               0
              828  COMPARE_OP               ==
          830_832  POP_JUMP_IF_FALSE   924  'to 924'
              834  LOAD_FAST                'j'
              836  LOAD_CONST               0
              838  COMPARE_OP               ==
          840_842  POP_JUMP_IF_FALSE   924  'to 924'

 L. 131       844  LOAD_FAST                'block'
              846  LOAD_CONST               None
              848  LOAD_CONST               None
              850  BUILD_SLICE_2         2 
              852  LOAD_CONST               None
              854  LOAD_FAST                'blocksize'
              856  LOAD_FAST                'coversize'
              858  LOAD_CONST               2
              860  BINARY_FLOOR_DIVIDE
              862  BINARY_SUBTRACT  
              864  BUILD_SLICE_2         2 
              866  LOAD_CONST               None
              868  LOAD_FAST                'blocksize'
              870  LOAD_FAST                'coversize'
              872  LOAD_CONST               2
              874  BINARY_FLOOR_DIVIDE
              876  BINARY_SUBTRACT  
              878  BUILD_SLICE_2         2 
              880  BUILD_TUPLE_3         3 
              882  BINARY_SUBSCR    
              884  STORE_FAST               'block'

 L. 133       886  LOAD_CONST               (0, 0)
              888  UNPACK_SEQUENCE_2     2 
              890  STORE_FAST               'col_off'
              892  STORE_FAST               'row_off'

 L. 134       894  LOAD_FAST                'uncoversize'
              896  LOAD_FAST                'coversize'
              898  LOAD_CONST               2
              900  BINARY_FLOOR_DIVIDE
              902  BINARY_ADD       
              904  LOAD_FAST                'uncoversize'
              906  LOAD_FAST                'coversize'
              908  LOAD_CONST               2
              910  BINARY_FLOOR_DIVIDE
              912  BINARY_ADD       
              914  ROT_TWO          
              916  STORE_FAST               'width'
              918  STORE_FAST               'height'
          920_922  JUMP_FORWARD       1828  'to 1828'
            924_0  COME_FROM           840  '840'
            924_1  COME_FROM           830  '830'

 L. 136       924  LOAD_FAST                'i'
              926  LOAD_FAST                'height_block'
              928  COMPARE_OP               ==
          930_932  POP_JUMP_IF_FALSE  1058  'to 1058'
              934  LOAD_FAST                'j'
              936  LOAD_FAST                'width_block'
              938  COMPARE_OP               ==
          940_942  POP_JUMP_IF_FALSE  1058  'to 1058'

 L. 137       944  LOAD_FAST                'block'
              946  LOAD_CONST               None
              948  LOAD_CONST               None
              950  BUILD_SLICE_2         2 
              952  LOAD_FAST                'coversize'
              954  LOAD_CONST               2
              956  BINARY_FLOOR_DIVIDE
              958  LOAD_FAST                'b_ds'
              960  LOAD_ATTR                height
              962  LOAD_FAST                'i'
              964  LOAD_FAST                'uncoversize'
              966  BINARY_MULTIPLY  
              968  BINARY_SUBTRACT  
              970  BUILD_SLICE_2         2 

 L. 138       972  LOAD_FAST                'coversize'
              974  LOAD_CONST               2
              976  BINARY_FLOOR_DIVIDE
              978  LOAD_FAST                'b_ds'
              980  LOAD_ATTR                width
              982  LOAD_FAST                'j'
              984  LOAD_FAST                'uncoversize'
              986  BINARY_MULTIPLY  
              988  BINARY_SUBTRACT  
              990  BUILD_SLICE_2         2 
              992  BUILD_TUPLE_3         3 
              994  BINARY_SUBSCR    
              996  STORE_FAST               'block'

 L. 140       998  LOAD_FAST                'j'
             1000  LOAD_FAST                'uncoversize'
             1002  BINARY_MULTIPLY  
             1004  LOAD_FAST                'coversize'
             1006  LOAD_CONST               2
             1008  BINARY_FLOOR_DIVIDE
             1010  BINARY_ADD       
             1012  LOAD_FAST                'i'
             1014  LOAD_FAST                'uncoversize'
             1016  BINARY_MULTIPLY  
             1018  LOAD_FAST                'coversize'
             1020  LOAD_CONST               2
             1022  BINARY_FLOOR_DIVIDE
             1024  BINARY_ADD       
             1026  ROT_TWO          
             1028  STORE_FAST               'col_off'
             1030  STORE_FAST               'row_off'

 L. 141      1032  LOAD_FAST                'b_ds'
             1034  LOAD_ATTR                width
             1036  LOAD_FAST                'col_off'
             1038  BINARY_SUBTRACT  
             1040  LOAD_FAST                'b_ds'
             1042  LOAD_ATTR                height
             1044  LOAD_FAST                'row_off'
             1046  BINARY_SUBTRACT  
             1048  ROT_TWO          
             1050  STORE_FAST               'width'
             1052  STORE_FAST               'height'
         1054_1056  JUMP_FORWARD       1828  'to 1828'
           1058_0  COME_FROM           940  '940'
           1058_1  COME_FROM           930  '930'

 L. 143      1058  LOAD_FAST                'i'
             1060  LOAD_CONST               0
             1062  COMPARE_OP               ==
         1064_1066  POP_JUMP_IF_FALSE  1278  'to 1278'
             1068  LOAD_FAST                'j'
             1070  LOAD_CONST               0
             1072  COMPARE_OP               !=
         1074_1076  POP_JUMP_IF_FALSE  1278  'to 1278'

 L. 144      1078  LOAD_FAST                'j'
             1080  LOAD_FAST                'width_block'
             1082  COMPARE_OP               ==
         1084_1086  POP_JUMP_IF_FALSE  1184  'to 1184'

 L. 146      1088  LOAD_FAST                'block'
             1090  LOAD_CONST               None
             1092  LOAD_CONST               None
             1094  BUILD_SLICE_2         2 
             1096  LOAD_CONST               None
             1098  LOAD_FAST                'blocksize'
             1100  LOAD_FAST                'coversize'
             1102  LOAD_CONST               2
             1104  BINARY_FLOOR_DIVIDE
             1106  BINARY_SUBTRACT  
             1108  BUILD_SLICE_2         2 

 L. 147      1110  LOAD_FAST                'coversize'
             1112  LOAD_CONST               2
             1114  BINARY_FLOOR_DIVIDE
             1116  LOAD_FAST                'b_ds'
             1118  LOAD_ATTR                width
             1120  LOAD_FAST                'j'
             1122  LOAD_FAST                'uncoversize'
             1124  BINARY_MULTIPLY  
             1126  BINARY_SUBTRACT  
             1128  BUILD_SLICE_2         2 
             1130  BUILD_TUPLE_3         3 
             1132  BINARY_SUBSCR    
             1134  STORE_FAST               'block'

 L. 149      1136  LOAD_FAST                'j'
             1138  LOAD_FAST                'uncoversize'
             1140  BINARY_MULTIPLY  
             1142  LOAD_FAST                'coversize'
             1144  LOAD_CONST               2
             1146  BINARY_FLOOR_DIVIDE
             1148  BINARY_ADD       
             1150  LOAD_CONST               0
             1152  ROT_TWO          
             1154  STORE_FAST               'col_off'
             1156  STORE_FAST               'row_off'

 L. 150      1158  LOAD_FAST                'b_ds'
             1160  LOAD_ATTR                width
             1162  LOAD_FAST                'col_off'
             1164  BINARY_SUBTRACT  
             1166  LOAD_FAST                'uncoversize'
             1168  LOAD_FAST                'coversize'
             1170  LOAD_CONST               2
             1172  BINARY_FLOOR_DIVIDE
             1174  BINARY_ADD       
             1176  ROT_TWO          
             1178  STORE_FAST               'width'
             1180  STORE_FAST               'height'
             1182  JUMP_FORWARD       1828  'to 1828'
           1184_0  COME_FROM          1084  '1084'

 L. 153      1184  LOAD_FAST                'block'
             1186  LOAD_CONST               None
             1188  LOAD_CONST               None
             1190  BUILD_SLICE_2         2 
             1192  LOAD_CONST               None
             1194  LOAD_FAST                'blocksize'
             1196  LOAD_FAST                'coversize'
             1198  LOAD_CONST               2
             1200  BINARY_FLOOR_DIVIDE
             1202  BINARY_SUBTRACT  
             1204  BUILD_SLICE_2         2 

 L. 154      1206  LOAD_FAST                'coversize'
             1208  LOAD_CONST               2
             1210  BINARY_FLOOR_DIVIDE
             1212  LOAD_FAST                'blocksize'
             1214  LOAD_FAST                'coversize'
             1216  LOAD_CONST               2
             1218  BINARY_FLOOR_DIVIDE
             1220  BINARY_SUBTRACT  
             1222  BUILD_SLICE_2         2 
             1224  BUILD_TUPLE_3         3 
             1226  BINARY_SUBSCR    
             1228  STORE_FAST               'block'

 L. 156      1230  LOAD_FAST                'j'
             1232  LOAD_FAST                'uncoversize'
             1234  BINARY_MULTIPLY  
             1236  LOAD_FAST                'coversize'
             1238  LOAD_CONST               2
             1240  BINARY_FLOOR_DIVIDE
             1242  BINARY_ADD       
             1244  LOAD_FAST                'i'
             1246  LOAD_FAST                'uncoversize'
             1248  BINARY_MULTIPLY  
             1250  ROT_TWO          
             1252  STORE_FAST               'col_off'
             1254  STORE_FAST               'row_off'

 L. 157      1256  LOAD_FAST                'uncoversize'
             1258  LOAD_FAST                'uncoversize'
             1260  LOAD_FAST                'coversize'
             1262  LOAD_CONST               2
             1264  BINARY_FLOOR_DIVIDE
             1266  BINARY_ADD       
             1268  ROT_TWO          
             1270  STORE_FAST               'width'
             1272  STORE_FAST               'height'
         1274_1276  JUMP_FORWARD       1828  'to 1828'
           1278_0  COME_FROM          1074  '1074'
           1278_1  COME_FROM          1064  '1064'

 L. 159      1278  LOAD_FAST                'i'
             1280  LOAD_CONST               0
             1282  COMPARE_OP               !=
         1284_1286  POP_JUMP_IF_FALSE  1506  'to 1506'
             1288  LOAD_FAST                'j'
             1290  LOAD_CONST               0
             1292  COMPARE_OP               ==
         1294_1296  POP_JUMP_IF_FALSE  1506  'to 1506'

 L. 160      1298  LOAD_FAST                'i'
             1300  LOAD_FAST                'height_block'
             1302  COMPARE_OP               ==
         1304_1306  POP_JUMP_IF_FALSE  1404  'to 1404'

 L. 161      1308  LOAD_FAST                'block'
             1310  LOAD_CONST               None
             1312  LOAD_CONST               None
             1314  BUILD_SLICE_2         2 
             1316  LOAD_FAST                'coversize'
             1318  LOAD_CONST               2
             1320  BINARY_FLOOR_DIVIDE
             1322  LOAD_FAST                'b_ds'
             1324  LOAD_ATTR                height
             1326  LOAD_FAST                'i'
             1328  LOAD_FAST                'uncoversize'
             1330  BINARY_MULTIPLY  
             1332  BINARY_SUBTRACT  
             1334  BUILD_SLICE_2         2 
             1336  LOAD_CONST               None

 L. 162      1338  LOAD_FAST                'blocksize'
             1340  LOAD_FAST                'coversize'
             1342  LOAD_CONST               2
             1344  BINARY_FLOOR_DIVIDE
             1346  BINARY_SUBTRACT  
             1348  BUILD_SLICE_2         2 
             1350  BUILD_TUPLE_3         3 
             1352  BINARY_SUBSCR    
             1354  STORE_FAST               'block'

 L. 164      1356  LOAD_CONST               0
             1358  LOAD_FAST                'i'
             1360  LOAD_FAST                'uncoversize'
             1362  BINARY_MULTIPLY  
             1364  LOAD_FAST                'coversize'
             1366  LOAD_CONST               2
             1368  BINARY_FLOOR_DIVIDE
             1370  BINARY_ADD       
             1372  ROT_TWO          
             1374  STORE_FAST               'col_off'
             1376  STORE_FAST               'row_off'

 L. 165      1378  LOAD_FAST                'uncoversize'
             1380  LOAD_FAST                'coversize'
             1382  LOAD_CONST               2
             1384  BINARY_FLOOR_DIVIDE
             1386  BINARY_ADD       
             1388  LOAD_FAST                'b_ds'
             1390  LOAD_ATTR                height
             1392  LOAD_FAST                'row_off'
             1394  BINARY_SUBTRACT  
             1396  ROT_TWO          
             1398  STORE_FAST               'width'
             1400  STORE_FAST               'height'
             1402  JUMP_FORWARD       1828  'to 1828'
           1404_0  COME_FROM          1304  '1304'

 L. 168      1404  LOAD_FAST                'block'
             1406  LOAD_CONST               None
             1408  LOAD_CONST               None
             1410  BUILD_SLICE_2         2 
             1412  LOAD_GLOBAL              int
             1414  LOAD_FAST                'coversize'
             1416  LOAD_CONST               2
             1418  BINARY_FLOOR_DIVIDE
             1420  CALL_FUNCTION_1       1  '1 positional argument'
             1422  LOAD_GLOBAL              int
             1424  LOAD_FAST                'blocksize'
             1426  LOAD_FAST                'coversize'
             1428  LOAD_CONST               2
             1430  BINARY_FLOOR_DIVIDE
             1432  BINARY_SUBTRACT  
             1434  CALL_FUNCTION_1       1  '1 positional argument'
             1436  BUILD_SLICE_2         2 
             1438  LOAD_CONST               None

 L. 169      1440  LOAD_GLOBAL              int
             1442  LOAD_FAST                'blocksize'
             1444  LOAD_FAST                'coversize'
             1446  LOAD_CONST               2
             1448  BINARY_FLOOR_DIVIDE
             1450  BINARY_SUBTRACT  
             1452  CALL_FUNCTION_1       1  '1 positional argument'
             1454  BUILD_SLICE_2         2 
             1456  BUILD_TUPLE_3         3 
             1458  BINARY_SUBSCR    
             1460  STORE_FAST               'block'

 L. 171      1462  LOAD_CONST               0
             1464  LOAD_FAST                'i'
             1466  LOAD_FAST                'uncoversize'
             1468  BINARY_MULTIPLY  
             1470  LOAD_FAST                'coversize'
             1472  LOAD_CONST               2
             1474  BINARY_FLOOR_DIVIDE
             1476  BINARY_ADD       
             1478  ROT_TWO          
             1480  STORE_FAST               'col_off'
             1482  STORE_FAST               'row_off'

 L. 172      1484  LOAD_FAST                'uncoversize'
             1486  LOAD_FAST                'coversize'
             1488  LOAD_CONST               2
             1490  BINARY_FLOOR_DIVIDE
             1492  BINARY_ADD       
             1494  LOAD_FAST                'uncoversize'
             1496  ROT_TWO          
             1498  STORE_FAST               'width'
             1500  STORE_FAST               'height'
         1502_1504  JUMP_FORWARD       1828  'to 1828'
           1506_0  COME_FROM          1294  '1294'
           1506_1  COME_FROM          1284  '1284'

 L. 175      1506  LOAD_FAST                'i'
             1508  LOAD_FAST                'height_block'
             1510  COMPARE_OP               ==
         1512_1514  POP_JUMP_IF_FALSE  1620  'to 1620'

 L. 176      1516  LOAD_FAST                'block'
             1518  LOAD_CONST               None
             1520  LOAD_CONST               None
             1522  BUILD_SLICE_2         2 
             1524  LOAD_FAST                'coversize'
             1526  LOAD_CONST               2
             1528  BINARY_FLOOR_DIVIDE
             1530  LOAD_FAST                'b_ds'
             1532  LOAD_ATTR                height
             1534  LOAD_FAST                'i'
             1536  LOAD_FAST                'uncoversize'
             1538  BINARY_MULTIPLY  
             1540  BINARY_SUBTRACT  
             1542  BUILD_SLICE_2         2 

 L. 177      1544  LOAD_FAST                'coversize'
             1546  LOAD_CONST               2
             1548  BINARY_FLOOR_DIVIDE
             1550  LOAD_FAST                'blocksize'
             1552  LOAD_FAST                'coversize'
             1554  LOAD_CONST               2
             1556  BINARY_FLOOR_DIVIDE
             1558  BINARY_SUBTRACT  
             1560  BUILD_SLICE_2         2 
             1562  BUILD_TUPLE_3         3 
             1564  BINARY_SUBSCR    
             1566  STORE_FAST               'block'

 L. 179      1568  LOAD_FAST                'j'
             1570  LOAD_FAST                'uncoversize'
             1572  BINARY_MULTIPLY  
             1574  LOAD_FAST                'coversize'
             1576  LOAD_CONST               2
             1578  BINARY_FLOOR_DIVIDE
             1580  BINARY_ADD       
             1582  LOAD_FAST                'i'
             1584  LOAD_FAST                'uncoversize'
             1586  BINARY_MULTIPLY  
             1588  LOAD_FAST                'coversize'
             1590  LOAD_CONST               2
             1592  BINARY_FLOOR_DIVIDE
             1594  BINARY_ADD       
             1596  ROT_TWO          
             1598  STORE_FAST               'col_off'
             1600  STORE_FAST               'row_off'

 L. 180      1602  LOAD_FAST                'uncoversize'
             1604  LOAD_FAST                'b_ds'
             1606  LOAD_ATTR                height
             1608  LOAD_FAST                'row_off'
             1610  BINARY_SUBTRACT  
             1612  ROT_TWO          
             1614  STORE_FAST               'width'
             1616  STORE_FAST               'height'
             1618  JUMP_FORWARD       1828  'to 1828'
           1620_0  COME_FROM          1512  '1512'

 L. 182      1620  LOAD_FAST                'j'
             1622  LOAD_FAST                'width_block'
             1624  COMPARE_OP               ==
         1626_1628  POP_JUMP_IF_FALSE  1734  'to 1734'

 L. 183      1630  LOAD_FAST                'block'
             1632  LOAD_CONST               None
             1634  LOAD_CONST               None
             1636  BUILD_SLICE_2         2 
             1638  LOAD_FAST                'coversize'
             1640  LOAD_CONST               2
             1642  BINARY_FLOOR_DIVIDE
             1644  LOAD_FAST                'blocksize'
             1646  LOAD_FAST                'coversize'
             1648  LOAD_CONST               2
             1650  BINARY_FLOOR_DIVIDE
             1652  BINARY_SUBTRACT  
             1654  BUILD_SLICE_2         2 

 L. 184      1656  LOAD_FAST                'coversize'
             1658  LOAD_CONST               2
             1660  BINARY_FLOOR_DIVIDE
             1662  LOAD_FAST                'b_ds'
             1664  LOAD_ATTR                width
             1666  LOAD_FAST                'j'
             1668  LOAD_FAST                'uncoversize'
             1670  BINARY_MULTIPLY  
             1672  BINARY_SUBTRACT  
             1674  BUILD_SLICE_2         2 
             1676  BUILD_TUPLE_3         3 
             1678  BINARY_SUBSCR    
             1680  STORE_FAST               'block'

 L. 186      1682  LOAD_FAST                'j'
             1684  LOAD_FAST                'uncoversize'
             1686  BINARY_MULTIPLY  
             1688  LOAD_FAST                'coversize'
             1690  LOAD_CONST               2
             1692  BINARY_FLOOR_DIVIDE
             1694  BINARY_ADD       
             1696  LOAD_FAST                'i'
             1698  LOAD_FAST                'uncoversize'
             1700  BINARY_MULTIPLY  
             1702  LOAD_FAST                'coversize'
             1704  LOAD_CONST               2
             1706  BINARY_FLOOR_DIVIDE
             1708  BINARY_ADD       
             1710  ROT_TWO          
             1712  STORE_FAST               'col_off'
             1714  STORE_FAST               'row_off'

 L. 187      1716  LOAD_FAST                'b_ds'
             1718  LOAD_ATTR                width
             1720  LOAD_FAST                'col_off'
             1722  BINARY_SUBTRACT  
             1724  LOAD_FAST                'uncoversize'
           1726_0  COME_FROM          1402  '1402'
             1726  ROT_TWO          
             1728  STORE_FAST               'width'
             1730  STORE_FAST               'height'
             1732  JUMP_FORWARD       1828  'to 1828'
           1734_0  COME_FROM          1626  '1626'
           1734_1  COME_FROM          1182  '1182'

 L. 190      1734  LOAD_FAST                'block'
             1736  LOAD_CONST               None
             1738  LOAD_CONST               None
             1740  BUILD_SLICE_2         2 
             1742  LOAD_FAST                'coversize'
             1744  LOAD_CONST               2
             1746  BINARY_FLOOR_DIVIDE
             1748  LOAD_FAST                'blocksize'
             1750  LOAD_FAST                'coversize'
             1752  LOAD_CONST               2
             1754  BINARY_FLOOR_DIVIDE
             1756  BINARY_SUBTRACT  
             1758  BUILD_SLICE_2         2 

 L. 191      1760  LOAD_FAST                'coversize'
             1762  LOAD_CONST               2
             1764  BINARY_FLOOR_DIVIDE
             1766  LOAD_FAST                'blocksize'
             1768  LOAD_FAST                'coversize'
             1770  LOAD_CONST               2
             1772  BINARY_FLOOR_DIVIDE
             1774  BINARY_SUBTRACT  
             1776  BUILD_SLICE_2         2 
             1778  BUILD_TUPLE_3         3 
             1780  BINARY_SUBSCR    
             1782  STORE_FAST               'block'

 L. 193      1784  LOAD_FAST                'j'
             1786  LOAD_FAST                'uncoversize'
             1788  BINARY_MULTIPLY  
             1790  LOAD_FAST                'coversize'
             1792  LOAD_CONST               2
             1794  BINARY_FLOOR_DIVIDE
             1796  BINARY_ADD       
             1798  LOAD_FAST                'i'
             1800  LOAD_FAST                'uncoversize'
             1802  BINARY_MULTIPLY  
             1804  LOAD_FAST                'coversize'
             1806  LOAD_CONST               2
             1808  BINARY_FLOOR_DIVIDE
             1810  BINARY_ADD       
             1812  ROT_TWO          
             1814  STORE_FAST               'col_off'
             1816  STORE_FAST               'row_off'

 L. 194      1818  LOAD_FAST                'uncoversize'
             1820  LOAD_FAST                'uncoversize'
             1822  ROT_TWO          
             1824  STORE_FAST               'width'
             1826  STORE_FAST               'height'
           1828_0  COME_FROM          1732  '1732'
           1828_1  COME_FROM          1618  '1618'
           1828_2  COME_FROM          1502  '1502'
           1828_3  COME_FROM          1274  '1274'
           1828_4  COME_FROM          1054  '1054'
           1828_5  COME_FROM           920  '920'

 L. 196      1828  LOAD_FAST                'p'
             1830  LOAD_CONST               1
             1832  INPLACE_ADD      
             1834  STORE_FAST               'p'

 L. 197      1836  LOAD_FAST                'dst'
             1838  LOAD_ATTR                write
             1840  LOAD_FAST                'block'
             1842  LOAD_GLOBAL              Window
             1844  LOAD_FAST                'col_off'
             1846  LOAD_FAST                'row_off'
             1848  LOAD_FAST                'width'
             1850  LOAD_FAST                'height'
             1852  CALL_FUNCTION_4       4  '4 positional arguments'
             1854  LOAD_CONST               ('window',)
             1856  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1858  POP_TOP          

 L. 198      1860  LOAD_GLOBAL              view_bar
             1862  LOAD_FAST                'p'
             1864  LOAD_FAST                'height_block'
             1866  LOAD_CONST               1
             1868  BINARY_ADD       
             1870  LOAD_FAST                'width_block'
             1872  LOAD_CONST               1
             1874  BINARY_ADD       
             1876  BINARY_MULTIPLY  
             1878  CALL_FUNCTION_2       2  '2 positional arguments'
             1880  POP_TOP          
         1882_1884  JUMP_BACK           280  'to 280'
             1886  POP_BLOCK        
           1888_0  COME_FROM_LOOP      264  '264'
         1888_1890  JUMP_BACK           258  'to 258'
             1892  POP_BLOCK        
           1894_0  COME_FROM_LOOP      242  '242'

 L. 200      1894  LOAD_FAST                'dst'
             1896  LOAD_METHOD              close
             1898  CALL_METHOD_0         0  '0 positional arguments'
             1900  POP_TOP          

 L. 201      1902  LOAD_FAST                'self'
             1904  LOAD_METHOD              close_model
             1906  CALL_METHOD_0         0  '0 positional arguments'
             1908  POP_TOP          

 L. 203      1910  LOAD_GLOBAL              get_output_datasource
             1912  LOAD_FAST                'out_ds'
             1914  CALL_FUNCTION_1       1  '1 positional argument'
             1916  STORE_FAST               'ds'

 L. 204      1918  LOAD_GLOBAL              check_output_datasource
             1920  LOAD_FAST                'ds'
             1922  CALL_FUNCTION_1       1  '1 positional argument'
             1924  POP_TOP          

 L. 205      1926  LOAD_GLOBAL              import_tif
             1928  LOAD_FAST                'tmp_file'
             1930  LOAD_FAST                'ds'
             1932  LOAD_FAST                'out_dataset_name'
             1934  LOAD_CONST               True
             1936  LOAD_CONST               ('output', 'out_dataset_name', 'is_import_as_grid')
             1938  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
             1940  STORE_FAST               'odst'

 L. 206      1942  LOAD_GLOBAL              os
             1944  LOAD_METHOD              remove
             1946  LOAD_FAST                'tmp_file'
             1948  CALL_METHOD_1         1  '1 positional argument'
             1950  POP_TOP          

 L. 208      1952  LOAD_GLOBAL              raster_to_vector
             1954  LOAD_FAST                'ds'
             1956  LOAD_FAST                'odst'
             1958  LOAD_CONST               0
             1960  BINARY_SUBSCR    
             1962  BINARY_SUBSCR    
             1964  LOAD_STR                 'class_type'
             1966  LOAD_GLOBAL              DatasetType
             1968  LOAD_ATTR                REGION

 L. 209      1970  LOAD_CONST               0

 L. 210      1972  LOAD_CONST               True
             1974  LOAD_FAST                'out_ds'

 L. 211      1976  LOAD_FAST                'out_dataset_name'
             1978  LOAD_STR                 '_region'
             1980  BINARY_ADD       
             1982  LOAD_CONST               ('out_dataset_type', 'back_or_no_value', 'is_thin_raster', 'out_data', 'out_dataset_name')
             1984  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
             1986  STORE_FAST               'result'

 L. 212      1988  LOAD_GLOBAL              get_input_dataset
             1990  LOAD_FAST                'result'
             1992  CALL_FUNCTION_1       1  '1 positional argument'
             1994  STORE_FAST               'result'

 L. 213      1996  BUILD_LIST_0          0 
             1998  STORE_FAST               'areas'

 L. 215      2000  SETUP_LOOP         2034  'to 2034'
             2002  LOAD_FAST                'result'
             2004  LOAD_METHOD              get_recordset
             2006  CALL_METHOD_0         0  '0 positional arguments'
             2008  GET_ITER         
             2010  FOR_ITER           2032  'to 2032'
             2012  STORE_FAST               'feature'

 L. 216      2014  LOAD_FAST                'areas'
             2016  LOAD_METHOD              append
             2018  LOAD_FAST                'feature'
             2020  LOAD_ATTR                geometry
             2022  LOAD_ATTR                area
             2024  CALL_METHOD_1         1  '1 positional argument'
             2026  POP_TOP          
         2028_2030  JUMP_BACK          2010  'to 2010'
             2032  POP_BLOCK        
           2034_0  COME_FROM_LOOP     2000  '2000'

 L. 217      2034  LOAD_GLOBAL              np
             2036  LOAD_METHOD              percentile
             2038  LOAD_FAST                'areas'
             2040  LOAD_CONST               93
             2042  CALL_METHOD_2         2  '2 positional arguments'
             2044  STORE_FAST               'area_thr'

 L. 218      2046  LOAD_FAST                'result'
             2048  LOAD_METHOD              get_recordset
             2050  CALL_METHOD_0         0  '0 positional arguments'
             2052  STORE_FAST               'rd'

 L. 219      2054  LOAD_FAST                'rd'
             2056  LOAD_METHOD              batch_edit
             2058  CALL_METHOD_0         0  '0 positional arguments'
             2060  POP_TOP          

 L. 220      2062  SETUP_LOOP         2128  'to 2128'
             2064  LOAD_GLOBAL              range
             2066  LOAD_FAST                'rd'
             2068  LOAD_METHOD              get_record_count
             2070  CALL_METHOD_0         0  '0 positional arguments'
             2072  LOAD_CONST               1
             2074  BINARY_SUBTRACT  
             2076  LOAD_CONST               -1
             2078  LOAD_CONST               -1
             2080  CALL_FUNCTION_3       3  '3 positional arguments'
             2082  GET_ITER         
           2084_0  COME_FROM          2110  '2110'
             2084  FOR_ITER           2126  'to 2126'
             2086  STORE_FAST               'i'

 L. 221      2088  LOAD_FAST                'rd'
             2090  LOAD_METHOD              move
             2092  LOAD_FAST                'i'
             2094  CALL_METHOD_1         1  '1 positional argument'
             2096  POP_TOP          

 L. 222      2098  LOAD_FAST                'rd'
             2100  LOAD_METHOD              get_geometry
             2102  CALL_METHOD_0         0  '0 positional arguments'
             2104  LOAD_ATTR                area
             2106  LOAD_FAST                'area_thr'
             2108  COMPARE_OP               <=
         2110_2112  POP_JUMP_IF_FALSE  2084  'to 2084'

 L. 223      2114  LOAD_FAST                'rd'
             2116  LOAD_METHOD              delete
             2118  CALL_METHOD_0         0  '0 positional arguments'
             2120  POP_TOP          
         2122_2124  JUMP_BACK          2084  'to 2084'
             2126  POP_BLOCK        
           2128_0  COME_FROM_LOOP     2062  '2062'

 L. 224      2128  LOAD_FAST                'rd'
             2130  LOAD_METHOD              batch_update
             2132  CALL_METHOD_0         0  '0 positional arguments'
             2134  POP_TOP          

 L. 225      2136  LOAD_FAST                'result'
             2138  LOAD_METHOD              close
             2140  CALL_METHOD_0         0  '0 positional arguments'
             2142  POP_TOP          
             2144  POP_BLOCK        
             2146  LOAD_CONST               None
           2148_0  COME_FROM_WITH      104  '104'
             2148  WITH_CLEANUP_START
             2150  WITH_CLEANUP_FINISH
             2152  END_FINALLY      
             2154  POP_BLOCK        
             2156  LOAD_CONST               None
           2158_0  COME_FROM_WITH       90  '90'
             2158  WITH_CLEANUP_START
             2160  WITH_CLEANUP_FINISH
             2162  END_FINALLY      

Parse error at or near `COME_FROM' instruction at offset 1726_0