# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/ml\vision\_models\semantic_seg\change_unet.py
# Compiled at: 2019-12-31 04:09:04
# Size of source mod 2**32: 20616 bytes
"""
@author: YangRuijie
@license: 
@contact: yangruijie@supermap.com
@software: 
@file: change_unet.py
@time: 7/26/19 8:25 AM
@desc: 基于特征相减的变化检测unet网络
"""
import os, shutil, tempfile, numpy as np, rasterio
from keras import backend as K
from keras.losses import categorical_crossentropy
from keras.optimizers import Adam
from rasterio.plot import reshape_as_image, reshape_as_raster
from rasterio.windows import Window
from ..... import import_tif, raster_to_vector, DatasetType
from _jsuperpy.data._util import get_output_datasource, check_output_datasource, get_input_dataset
from ....._logger import log_warning, log_info, log_error
from toolkit._keras_model_utils import find_last, bce_dice_loss, dice_coef
from toolkit._toolkit import stretch_n, view_bar, split_train_val_withdirs, split_train_val_change_det, get_image_from_csv, get_changedet_image_from_csv
from _seg_models.backbones.cls_models.cls_models.utils import get_weights_default_path
from _seg_models.backbones.cls_models.cls_models.weights import weights_collection
from _seg_models.model_builder import build_model
from .base_keras_models import Estimation, Trainer

class ChangUNetEstimation(Estimation):

    def __init__(self, model_path, config):
        super().__init__(model_path, config)
        self.model_input1 = config.ModelInput[0]
        self.model_input2 = config.ModelInput[1]
        self.model_output = config.ModelOutput[0]
        if np.argmin(self.model_input1.Shape) == 0:
            self.band_order = 'first'
            self.seg_size = self.model_input1.Shape[1]
            self.out_width_height = [self.model_output.Shape[1], self.model_output.Shape[2]]
            self.output_msk_num = self.model_output.Shape[0]
            if self.model_input1.Shape[1] != self.model_input1.Shape[2]:
                raise ValueError('Model input width and height should be equal!')
        else:
            self.band_order = 'last'
            self.seg_size = self.model_input1.Shape[1]
            self.out_width_height = [self.model_output.Shape[0], self.model_output.Shape[1]]
            self.output_msk_num = self.model_output.Shape[(-1)]
            if self.model_input1.Shape[1] != self.model_input1.Shape[0]:
                raise ValueError('Model input width and height should be equal!')
        self.is_stretch = config.IsStretch
        self.model_path = model_path

    def estimate_img(self, before_img, after_image, coversize, out_ds, out_dataset_name, **kwargs):
        self.half_oversize = coversize
        self._predict_with_rasterio(before_img, after_image, out_ds, out_dataset_name)

    def _predict_with_rasterio--- This code section failed: ---

 L.  80         0  LOAD_FAST                'self'
                2  LOAD_ATTR                half_oversize
                4  LOAD_CONST               2
                6  BINARY_MULTIPLY  
                8  STORE_FAST               'coversize'

 L.  81        10  LOAD_FAST                'self'
               12  LOAD_ATTR                seg_size
               14  STORE_FAST               'blocksize'

 L.  82        16  LOAD_FAST                'coversize'
               18  LOAD_CONST               2
               20  BINARY_MODULO    
               22  LOAD_CONST               0
               24  COMPARE_OP               !=
               26  POP_JUMP_IF_FALSE    38  'to 38'

 L.  83        28  LOAD_GLOBAL              ValueError
               30  LOAD_STR                 'coversize must be even number!'
               32  CALL_FUNCTION_1       1  '1 positional argument'
               34  RAISE_VARARGS_1       1  'exception instance'
               36  JUMP_FORWARD         74  'to 74'
             38_0  COME_FROM            26  '26'

 L.  84        38  LOAD_FAST                'coversize'
               40  LOAD_FAST                'blocksize'
               42  COMPARE_OP               ==
               44  POP_JUMP_IF_FALSE    56  'to 56'

 L.  85        46  LOAD_GLOBAL              ValueError
               48  LOAD_STR                 'coversize and blocksize is same!'
               50  CALL_FUNCTION_1       1  '1 positional argument'
               52  RAISE_VARARGS_1       1  'exception instance'
               54  JUMP_FORWARD         74  'to 74'
             56_0  COME_FROM            44  '44'

 L.  86        56  LOAD_FAST                'coversize'
               58  LOAD_FAST                'blocksize'
               60  COMPARE_OP               >
               62  POP_JUMP_IF_FALSE    74  'to 74'

 L.  87        64  LOAD_GLOBAL              ValueError
               66  LOAD_STR                 'coversize is bigger than blocksize!'
               68  CALL_FUNCTION_1       1  '1 positional argument'
               70  RAISE_VARARGS_1       1  'exception instance'
               72  JUMP_FORWARD         74  'to 74'
             74_0  COME_FROM            72  '72'
             74_1  COME_FROM            62  '62'
             74_2  COME_FROM            54  '54'
             74_3  COME_FROM            36  '36'

 L.  91        74  LOAD_FAST                'blocksize'
               76  LOAD_FAST                'coversize'
               78  BINARY_SUBTRACT  
               80  STORE_FAST               'uncoversize'

 L.  93        82  LOAD_GLOBAL              rasterio
               84  LOAD_METHOD              open
               86  LOAD_FAST                'before_img'
               88  CALL_METHOD_1         1  '1 positional argument'
            90_92  SETUP_WITH         1948  'to 1948'
               94  STORE_FAST               'b_ds'

 L.  94        96  LOAD_GLOBAL              rasterio
               98  LOAD_METHOD              open
              100  LOAD_FAST                'after_image'
              102  CALL_METHOD_1         1  '1 positional argument'
          104_106  SETUP_WITH         1938  'to 1938'
              108  STORE_FAST               'a_ds'

 L.  95       110  LOAD_FAST                'a_ds'
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

 L.  97       142  LOAD_FAST                'b_ds'
              144  LOAD_ATTR                width
              146  LOAD_FAST                'coversize'
              148  LOAD_CONST               2
              150  BINARY_FLOOR_DIVIDE
              152  BINARY_SUBTRACT  
              154  LOAD_FAST                'uncoversize'
              156  BINARY_FLOOR_DIVIDE
              158  STORE_FAST               'width_block'

 L.  98       160  LOAD_FAST                'b_ds'
              162  LOAD_ATTR                height
              164  LOAD_FAST                'coversize'
              166  LOAD_CONST               2
              168  BINARY_FLOOR_DIVIDE
              170  BINARY_SUBTRACT  
              172  LOAD_FAST                'uncoversize'
              174  BINARY_FLOOR_DIVIDE
              176  STORE_FAST               'height_block'

 L. 100       178  LOAD_GLOBAL              os
              180  LOAD_ATTR                path
              182  LOAD_METHOD              join
              184  LOAD_GLOBAL              tempfile
              186  LOAD_METHOD              mkdtemp
              188  CALL_METHOD_0         0  '0 positional arguments'
              190  LOAD_STR                 'tmp.tif'
              192  CALL_METHOD_2         2  '2 positional arguments'
              194  STORE_FAST               'tmp_file'

 L. 101       196  LOAD_GLOBAL              rasterio
              198  LOAD_ATTR                open
              200  LOAD_FAST                'tmp_file'
              202  LOAD_STR                 'w'
              204  LOAD_STR                 'GTiff'
              206  LOAD_FAST                'a_ds'
              208  LOAD_ATTR                width
              210  LOAD_FAST                'a_ds'
              212  LOAD_ATTR                height

 L. 102       214  LOAD_CONST               1
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

 L. 103       238  LOAD_CONST               0
              240  STORE_FAST               'p'

 L. 104   242_244  SETUP_LOOP         1840  'to 1840'
              246  LOAD_GLOBAL              range
              248  LOAD_FAST                'height_block'
              250  LOAD_CONST               1
              252  BINARY_ADD       
              254  CALL_FUNCTION_1       1  '1 positional argument'
              256  GET_ITER         
          258_260  FOR_ITER           1838  'to 1838'
              262  STORE_FAST               'i'

 L. 105   264_266  SETUP_LOOP         1834  'to 1834'
              268  LOAD_GLOBAL              range
              270  LOAD_FAST                'width_block'
              272  LOAD_CONST               1
              274  BINARY_ADD       
              276  CALL_FUNCTION_1       1  '1 positional argument'
              278  GET_ITER         
          280_282  FOR_ITER           1832  'to 1832'
              284  STORE_FAST               'j'

 L. 108       286  LOAD_GLOBAL              np
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

 L. 109       308  LOAD_GLOBAL              np
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

 L. 110       330  LOAD_FAST                'b_ds'
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

 L. 111       360  LOAD_FAST                'a_ds'
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

 L. 112       390  LOAD_FAST                'b_img'
              392  LOAD_CONST               None
              394  LOAD_CONST               3
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

 L. 113       450  LOAD_FAST                'a_img'
              452  LOAD_CONST               None
              454  LOAD_CONST               3
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

 L. 115       510  LOAD_FAST                'self'
              512  LOAD_ATTR                is_stretch
          514_516  POP_JUMP_IF_FALSE   558  'to 558'

 L. 116       518  LOAD_STR                 'all_max'
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

 L. 117       542  LOAD_GLOBAL              stretch_n
              544  LOAD_FAST                'b_block'
              546  CALL_FUNCTION_1       1  '1 positional argument'
              548  STORE_FAST               'b_block'

 L. 118       550  LOAD_GLOBAL              stretch_n
              552  LOAD_FAST                'a_block'
              554  CALL_FUNCTION_1       1  '1 positional argument'
              556  STORE_FAST               'a_block'
            558_0  COME_FROM           538  '538'
            558_1  COME_FROM           514  '514'

 L. 119       558  LOAD_GLOBAL              reshape_as_image
              560  LOAD_FAST                'b_block'
              562  CALL_FUNCTION_1       1  '1 positional argument'
              564  STORE_FAST               'b_block'

 L. 120       566  LOAD_GLOBAL              reshape_as_image
              568  LOAD_FAST                'a_block'
              570  CALL_FUNCTION_1       1  '1 positional argument'
              572  STORE_FAST               'a_block'

 L. 121       574  LOAD_FAST                'b_block'
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

 L. 122       604  LOAD_FAST                'a_block'
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

 L. 125       634  LOAD_FAST                'b_block'
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

 L. 126       666  LOAD_FAST                'self'
              668  LOAD_METHOD              _predict_tile_local
              670  LOAD_FAST                'b_block'
              672  LOAD_FAST                'a_block'
              674  LOAD_FAST                'out_shape'
              676  CALL_METHOD_3         3  '3 positional arguments'
              678  STORE_FAST               'mask_block'

 L. 127       680  LOAD_GLOBAL              np
              682  LOAD_ATTR                squeeze
              684  LOAD_FAST                'mask_block'
              686  LOAD_CONST               0
              688  LOAD_CONST               ('axis',)
              690  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              692  STORE_FAST               'mask_block'

 L. 128       694  LOAD_FAST                'self'
              696  LOAD_ATTR                output_msk_num
              698  LOAD_CONST               1
              700  COMPARE_OP               >
          702_704  POP_JUMP_IF_FALSE   742  'to 742'

 L. 129       706  LOAD_GLOBAL              np
              708  LOAD_ATTR                argmax
              710  LOAD_FAST                'mask_block'
              712  LOAD_CONST               -1
              714  LOAD_CONST               ('axis',)
              716  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              718  LOAD_CONST               None
              720  LOAD_CONST               None
              722  BUILD_SLICE_2         2 
              724  LOAD_CONST               None
              726  LOAD_CONST               None
              728  BUILD_SLICE_2         2 
              730  LOAD_GLOBAL              np
              732  LOAD_ATTR                newaxis
              734  BUILD_TUPLE_3         3 
              736  BINARY_SUBSCR    
              738  STORE_FAST               'mask_int'
              740  JUMP_FORWARD        750  'to 750'
            742_0  COME_FROM           702  '702'

 L. 131       742  LOAD_FAST                'mask_block'
              744  LOAD_FAST                'single_thresold'
              746  COMPARE_OP               >
              748  STORE_FAST               'mask_int'
            750_0  COME_FROM           740  '740'

 L. 132       750  LOAD_FAST                'mask_int'
              752  LOAD_METHOD              astype
              754  LOAD_GLOBAL              np
              756  LOAD_ATTR                uint8
              758  CALL_METHOD_1         1  '1 positional argument'
              760  STORE_FAST               'mask_int'

 L. 135       762  LOAD_GLOBAL              reshape_as_raster
              764  LOAD_FAST                'mask_int'
              766  CALL_FUNCTION_1       1  '1 positional argument'
              768  STORE_FAST               'block'

 L. 138       770  LOAD_FAST                'i'
              772  LOAD_CONST               0
              774  COMPARE_OP               ==
          776_778  POP_JUMP_IF_FALSE   870  'to 870'
              780  LOAD_FAST                'j'
              782  LOAD_CONST               0
              784  COMPARE_OP               ==
          786_788  POP_JUMP_IF_FALSE   870  'to 870'

 L. 139       790  LOAD_FAST                'block'
              792  LOAD_CONST               None
              794  LOAD_CONST               None
              796  BUILD_SLICE_2         2 
              798  LOAD_CONST               None
              800  LOAD_FAST                'blocksize'
              802  LOAD_FAST                'coversize'
              804  LOAD_CONST               2
              806  BINARY_FLOOR_DIVIDE
              808  BINARY_SUBTRACT  
              810  BUILD_SLICE_2         2 
              812  LOAD_CONST               None
              814  LOAD_FAST                'blocksize'
              816  LOAD_FAST                'coversize'
              818  LOAD_CONST               2
              820  BINARY_FLOOR_DIVIDE
              822  BINARY_SUBTRACT  
              824  BUILD_SLICE_2         2 
              826  BUILD_TUPLE_3         3 
              828  BINARY_SUBSCR    
              830  STORE_FAST               'block'

 L. 141       832  LOAD_CONST               (0, 0)
              834  UNPACK_SEQUENCE_2     2 
              836  STORE_FAST               'col_off'
              838  STORE_FAST               'row_off'

 L. 142       840  LOAD_FAST                'uncoversize'
              842  LOAD_FAST                'coversize'
              844  LOAD_CONST               2
              846  BINARY_FLOOR_DIVIDE
              848  BINARY_ADD       
              850  LOAD_FAST                'uncoversize'
              852  LOAD_FAST                'coversize'
              854  LOAD_CONST               2
              856  BINARY_FLOOR_DIVIDE
              858  BINARY_ADD       
              860  ROT_TWO          
              862  STORE_FAST               'width'
              864  STORE_FAST               'height'
          866_868  JUMP_FORWARD       1774  'to 1774'
            870_0  COME_FROM           786  '786'
            870_1  COME_FROM           776  '776'

 L. 144       870  LOAD_FAST                'i'
              872  LOAD_FAST                'height_block'
              874  COMPARE_OP               ==
          876_878  POP_JUMP_IF_FALSE  1004  'to 1004'
              880  LOAD_FAST                'j'
              882  LOAD_FAST                'width_block'
              884  COMPARE_OP               ==
          886_888  POP_JUMP_IF_FALSE  1004  'to 1004'

 L. 145       890  LOAD_FAST                'block'
              892  LOAD_CONST               None
              894  LOAD_CONST               None
              896  BUILD_SLICE_2         2 
              898  LOAD_FAST                'coversize'
              900  LOAD_CONST               2
              902  BINARY_FLOOR_DIVIDE
              904  LOAD_FAST                'b_ds'
              906  LOAD_ATTR                height
              908  LOAD_FAST                'i'
              910  LOAD_FAST                'uncoversize'
              912  BINARY_MULTIPLY  
              914  BINARY_SUBTRACT  
              916  BUILD_SLICE_2         2 

 L. 146       918  LOAD_FAST                'coversize'
              920  LOAD_CONST               2
              922  BINARY_FLOOR_DIVIDE
              924  LOAD_FAST                'b_ds'
              926  LOAD_ATTR                width
              928  LOAD_FAST                'j'
              930  LOAD_FAST                'uncoversize'
              932  BINARY_MULTIPLY  
              934  BINARY_SUBTRACT  
              936  BUILD_SLICE_2         2 
              938  BUILD_TUPLE_3         3 
              940  BINARY_SUBSCR    
              942  STORE_FAST               'block'

 L. 148       944  LOAD_FAST                'j'
              946  LOAD_FAST                'uncoversize'
              948  BINARY_MULTIPLY  
              950  LOAD_FAST                'coversize'
              952  LOAD_CONST               2
              954  BINARY_FLOOR_DIVIDE
              956  BINARY_ADD       
              958  LOAD_FAST                'i'
              960  LOAD_FAST                'uncoversize'
              962  BINARY_MULTIPLY  
              964  LOAD_FAST                'coversize'
              966  LOAD_CONST               2
              968  BINARY_FLOOR_DIVIDE
              970  BINARY_ADD       
              972  ROT_TWO          
              974  STORE_FAST               'col_off'
              976  STORE_FAST               'row_off'

 L. 149       978  LOAD_FAST                'b_ds'
              980  LOAD_ATTR                width
              982  LOAD_FAST                'col_off'
              984  BINARY_SUBTRACT  
              986  LOAD_FAST                'b_ds'
              988  LOAD_ATTR                height
              990  LOAD_FAST                'row_off'
              992  BINARY_SUBTRACT  
              994  ROT_TWO          
              996  STORE_FAST               'width'
              998  STORE_FAST               'height'
         1000_1002  JUMP_FORWARD       1774  'to 1774'
           1004_0  COME_FROM           886  '886'
           1004_1  COME_FROM           876  '876'

 L. 151      1004  LOAD_FAST                'i'
             1006  LOAD_CONST               0
             1008  COMPARE_OP               ==
         1010_1012  POP_JUMP_IF_FALSE  1224  'to 1224'
             1014  LOAD_FAST                'j'
             1016  LOAD_CONST               0
             1018  COMPARE_OP               !=
         1020_1022  POP_JUMP_IF_FALSE  1224  'to 1224'

 L. 152      1024  LOAD_FAST                'j'
             1026  LOAD_FAST                'width_block'
             1028  COMPARE_OP               ==
         1030_1032  POP_JUMP_IF_FALSE  1130  'to 1130'

 L. 154      1034  LOAD_FAST                'block'
             1036  LOAD_CONST               None
             1038  LOAD_CONST               None
             1040  BUILD_SLICE_2         2 
             1042  LOAD_CONST               None
             1044  LOAD_FAST                'blocksize'
             1046  LOAD_FAST                'coversize'
             1048  LOAD_CONST               2
             1050  BINARY_FLOOR_DIVIDE
             1052  BINARY_SUBTRACT  
             1054  BUILD_SLICE_2         2 

 L. 155      1056  LOAD_FAST                'coversize'
             1058  LOAD_CONST               2
             1060  BINARY_FLOOR_DIVIDE
             1062  LOAD_FAST                'b_ds'
             1064  LOAD_ATTR                width
             1066  LOAD_FAST                'j'
             1068  LOAD_FAST                'uncoversize'
             1070  BINARY_MULTIPLY  
             1072  BINARY_SUBTRACT  
             1074  BUILD_SLICE_2         2 
             1076  BUILD_TUPLE_3         3 
             1078  BINARY_SUBSCR    
             1080  STORE_FAST               'block'

 L. 157      1082  LOAD_FAST                'j'
             1084  LOAD_FAST                'uncoversize'
             1086  BINARY_MULTIPLY  
             1088  LOAD_FAST                'coversize'
             1090  LOAD_CONST               2
             1092  BINARY_FLOOR_DIVIDE
             1094  BINARY_ADD       
             1096  LOAD_CONST               0
             1098  ROT_TWO          
             1100  STORE_FAST               'col_off'
             1102  STORE_FAST               'row_off'

 L. 158      1104  LOAD_FAST                'b_ds'
             1106  LOAD_ATTR                width
             1108  LOAD_FAST                'col_off'
             1110  BINARY_SUBTRACT  
             1112  LOAD_FAST                'uncoversize'
             1114  LOAD_FAST                'coversize'
             1116  LOAD_CONST               2
             1118  BINARY_FLOOR_DIVIDE
             1120  BINARY_ADD       
             1122  ROT_TWO          
             1124  STORE_FAST               'width'
             1126  STORE_FAST               'height'
             1128  JUMP_FORWARD       1774  'to 1774'
           1130_0  COME_FROM          1030  '1030'

 L. 161      1130  LOAD_FAST                'block'
             1132  LOAD_CONST               None
             1134  LOAD_CONST               None
             1136  BUILD_SLICE_2         2 
             1138  LOAD_CONST               None
             1140  LOAD_FAST                'blocksize'
             1142  LOAD_FAST                'coversize'
             1144  LOAD_CONST               2
             1146  BINARY_FLOOR_DIVIDE
             1148  BINARY_SUBTRACT  
             1150  BUILD_SLICE_2         2 

 L. 162      1152  LOAD_FAST                'coversize'
             1154  LOAD_CONST               2
             1156  BINARY_FLOOR_DIVIDE
             1158  LOAD_FAST                'blocksize'
             1160  LOAD_FAST                'coversize'
             1162  LOAD_CONST               2
             1164  BINARY_FLOOR_DIVIDE
             1166  BINARY_SUBTRACT  
             1168  BUILD_SLICE_2         2 
             1170  BUILD_TUPLE_3         3 
             1172  BINARY_SUBSCR    
             1174  STORE_FAST               'block'

 L. 164      1176  LOAD_FAST                'j'
             1178  LOAD_FAST                'uncoversize'
             1180  BINARY_MULTIPLY  
             1182  LOAD_FAST                'coversize'
             1184  LOAD_CONST               2
             1186  BINARY_FLOOR_DIVIDE
             1188  BINARY_ADD       
             1190  LOAD_FAST                'i'
             1192  LOAD_FAST                'uncoversize'
             1194  BINARY_MULTIPLY  
             1196  ROT_TWO          
             1198  STORE_FAST               'col_off'
             1200  STORE_FAST               'row_off'

 L. 165      1202  LOAD_FAST                'uncoversize'
             1204  LOAD_FAST                'uncoversize'
             1206  LOAD_FAST                'coversize'
             1208  LOAD_CONST               2
             1210  BINARY_FLOOR_DIVIDE
             1212  BINARY_ADD       
             1214  ROT_TWO          
             1216  STORE_FAST               'width'
             1218  STORE_FAST               'height'
         1220_1222  JUMP_FORWARD       1774  'to 1774'
           1224_0  COME_FROM          1020  '1020'
           1224_1  COME_FROM          1010  '1010'

 L. 167      1224  LOAD_FAST                'i'
             1226  LOAD_CONST               0
             1228  COMPARE_OP               !=
         1230_1232  POP_JUMP_IF_FALSE  1452  'to 1452'
             1234  LOAD_FAST                'j'
             1236  LOAD_CONST               0
             1238  COMPARE_OP               ==
         1240_1242  POP_JUMP_IF_FALSE  1452  'to 1452'

 L. 168      1244  LOAD_FAST                'i'
             1246  LOAD_FAST                'height_block'
             1248  COMPARE_OP               ==
         1250_1252  POP_JUMP_IF_FALSE  1350  'to 1350'

 L. 169      1254  LOAD_FAST                'block'
             1256  LOAD_CONST               None
             1258  LOAD_CONST               None
             1260  BUILD_SLICE_2         2 
             1262  LOAD_FAST                'coversize'
             1264  LOAD_CONST               2
             1266  BINARY_FLOOR_DIVIDE
             1268  LOAD_FAST                'b_ds'
             1270  LOAD_ATTR                height
             1272  LOAD_FAST                'i'
             1274  LOAD_FAST                'uncoversize'
             1276  BINARY_MULTIPLY  
             1278  BINARY_SUBTRACT  
             1280  BUILD_SLICE_2         2 
             1282  LOAD_CONST               None

 L. 170      1284  LOAD_FAST                'blocksize'
             1286  LOAD_FAST                'coversize'
             1288  LOAD_CONST               2
             1290  BINARY_FLOOR_DIVIDE
             1292  BINARY_SUBTRACT  
             1294  BUILD_SLICE_2         2 
             1296  BUILD_TUPLE_3         3 
             1298  BINARY_SUBSCR    
             1300  STORE_FAST               'block'

 L. 172      1302  LOAD_CONST               0
             1304  LOAD_FAST                'i'
             1306  LOAD_FAST                'uncoversize'
             1308  BINARY_MULTIPLY  
             1310  LOAD_FAST                'coversize'
             1312  LOAD_CONST               2
             1314  BINARY_FLOOR_DIVIDE
             1316  BINARY_ADD       
             1318  ROT_TWO          
             1320  STORE_FAST               'col_off'
             1322  STORE_FAST               'row_off'

 L. 173      1324  LOAD_FAST                'uncoversize'
             1326  LOAD_FAST                'coversize'
             1328  LOAD_CONST               2
             1330  BINARY_FLOOR_DIVIDE
             1332  BINARY_ADD       
             1334  LOAD_FAST                'b_ds'
             1336  LOAD_ATTR                height
             1338  LOAD_FAST                'row_off'
             1340  BINARY_SUBTRACT  
             1342  ROT_TWO          
             1344  STORE_FAST               'width'
             1346  STORE_FAST               'height'
             1348  JUMP_FORWARD       1774  'to 1774'
           1350_0  COME_FROM          1250  '1250'

 L. 176      1350  LOAD_FAST                'block'
             1352  LOAD_CONST               None
             1354  LOAD_CONST               None
             1356  BUILD_SLICE_2         2 
             1358  LOAD_GLOBAL              int
             1360  LOAD_FAST                'coversize'
             1362  LOAD_CONST               2
             1364  BINARY_FLOOR_DIVIDE
             1366  CALL_FUNCTION_1       1  '1 positional argument'
             1368  LOAD_GLOBAL              int
             1370  LOAD_FAST                'blocksize'
             1372  LOAD_FAST                'coversize'
             1374  LOAD_CONST               2
             1376  BINARY_FLOOR_DIVIDE
             1378  BINARY_SUBTRACT  
             1380  CALL_FUNCTION_1       1  '1 positional argument'
             1382  BUILD_SLICE_2         2 
             1384  LOAD_CONST               None

 L. 177      1386  LOAD_GLOBAL              int
             1388  LOAD_FAST                'blocksize'
             1390  LOAD_FAST                'coversize'
             1392  LOAD_CONST               2
             1394  BINARY_FLOOR_DIVIDE
             1396  BINARY_SUBTRACT  
             1398  CALL_FUNCTION_1       1  '1 positional argument'
             1400  BUILD_SLICE_2         2 
             1402  BUILD_TUPLE_3         3 
             1404  BINARY_SUBSCR    
             1406  STORE_FAST               'block'

 L. 179      1408  LOAD_CONST               0
             1410  LOAD_FAST                'i'
             1412  LOAD_FAST                'uncoversize'
             1414  BINARY_MULTIPLY  
             1416  LOAD_FAST                'coversize'
             1418  LOAD_CONST               2
             1420  BINARY_FLOOR_DIVIDE
             1422  BINARY_ADD       
             1424  ROT_TWO          
             1426  STORE_FAST               'col_off'
             1428  STORE_FAST               'row_off'

 L. 180      1430  LOAD_FAST                'uncoversize'
             1432  LOAD_FAST                'coversize'
             1434  LOAD_CONST               2
             1436  BINARY_FLOOR_DIVIDE
             1438  BINARY_ADD       
             1440  LOAD_FAST                'uncoversize'
             1442  ROT_TWO          
             1444  STORE_FAST               'width'
             1446  STORE_FAST               'height'
         1448_1450  JUMP_FORWARD       1774  'to 1774'
           1452_0  COME_FROM          1240  '1240'
           1452_1  COME_FROM          1230  '1230'

 L. 183      1452  LOAD_FAST                'i'
             1454  LOAD_FAST                'height_block'
             1456  COMPARE_OP               ==
         1458_1460  POP_JUMP_IF_FALSE  1566  'to 1566'

 L. 184      1462  LOAD_FAST                'block'
             1464  LOAD_CONST               None
             1466  LOAD_CONST               None
             1468  BUILD_SLICE_2         2 
             1470  LOAD_FAST                'coversize'
             1472  LOAD_CONST               2
             1474  BINARY_FLOOR_DIVIDE
             1476  LOAD_FAST                'b_ds'
             1478  LOAD_ATTR                height
             1480  LOAD_FAST                'i'
             1482  LOAD_FAST                'uncoversize'
             1484  BINARY_MULTIPLY  
             1486  BINARY_SUBTRACT  
             1488  BUILD_SLICE_2         2 

 L. 185      1490  LOAD_FAST                'coversize'
             1492  LOAD_CONST               2
             1494  BINARY_FLOOR_DIVIDE
             1496  LOAD_FAST                'blocksize'
             1498  LOAD_FAST                'coversize'
             1500  LOAD_CONST               2
             1502  BINARY_FLOOR_DIVIDE
             1504  BINARY_SUBTRACT  
             1506  BUILD_SLICE_2         2 
             1508  BUILD_TUPLE_3         3 
             1510  BINARY_SUBSCR    
             1512  STORE_FAST               'block'

 L. 187      1514  LOAD_FAST                'j'
             1516  LOAD_FAST                'uncoversize'
             1518  BINARY_MULTIPLY  
             1520  LOAD_FAST                'coversize'
             1522  LOAD_CONST               2
             1524  BINARY_FLOOR_DIVIDE
             1526  BINARY_ADD       
             1528  LOAD_FAST                'i'
             1530  LOAD_FAST                'uncoversize'
             1532  BINARY_MULTIPLY  
             1534  LOAD_FAST                'coversize'
             1536  LOAD_CONST               2
             1538  BINARY_FLOOR_DIVIDE
             1540  BINARY_ADD       
             1542  ROT_TWO          
             1544  STORE_FAST               'col_off'
             1546  STORE_FAST               'row_off'

 L. 188      1548  LOAD_FAST                'uncoversize'
             1550  LOAD_FAST                'b_ds'
             1552  LOAD_ATTR                height
             1554  LOAD_FAST                'row_off'
             1556  BINARY_SUBTRACT  
             1558  ROT_TWO          
             1560  STORE_FAST               'width'
             1562  STORE_FAST               'height'
             1564  JUMP_FORWARD       1774  'to 1774'
           1566_0  COME_FROM          1458  '1458'

 L. 190      1566  LOAD_FAST                'j'
             1568  LOAD_FAST                'width_block'
             1570  COMPARE_OP               ==
         1572_1574  POP_JUMP_IF_FALSE  1680  'to 1680'

 L. 191      1576  LOAD_FAST                'block'
             1578  LOAD_CONST               None
             1580  LOAD_CONST               None
             1582  BUILD_SLICE_2         2 
             1584  LOAD_FAST                'coversize'
             1586  LOAD_CONST               2
             1588  BINARY_FLOOR_DIVIDE
             1590  LOAD_FAST                'blocksize'
             1592  LOAD_FAST                'coversize'
             1594  LOAD_CONST               2
             1596  BINARY_FLOOR_DIVIDE
             1598  BINARY_SUBTRACT  
             1600  BUILD_SLICE_2         2 

 L. 192      1602  LOAD_FAST                'coversize'
             1604  LOAD_CONST               2
             1606  BINARY_FLOOR_DIVIDE
             1608  LOAD_FAST                'b_ds'
             1610  LOAD_ATTR                width
             1612  LOAD_FAST                'j'
             1614  LOAD_FAST                'uncoversize'
             1616  BINARY_MULTIPLY  
             1618  BINARY_SUBTRACT  
             1620  BUILD_SLICE_2         2 
             1622  BUILD_TUPLE_3         3 
             1624  BINARY_SUBSCR    
             1626  STORE_FAST               'block'

 L. 194      1628  LOAD_FAST                'j'
             1630  LOAD_FAST                'uncoversize'
             1632  BINARY_MULTIPLY  
             1634  LOAD_FAST                'coversize'
             1636  LOAD_CONST               2
             1638  BINARY_FLOOR_DIVIDE
             1640  BINARY_ADD       
             1642  LOAD_FAST                'i'
             1644  LOAD_FAST                'uncoversize'
             1646  BINARY_MULTIPLY  
             1648  LOAD_FAST                'coversize'
             1650  LOAD_CONST               2
             1652  BINARY_FLOOR_DIVIDE
             1654  BINARY_ADD       
             1656  ROT_TWO          
             1658  STORE_FAST               'col_off'
             1660  STORE_FAST               'row_off'

 L. 195      1662  LOAD_FAST                'b_ds'
             1664  LOAD_ATTR                width
             1666  LOAD_FAST                'col_off'
             1668  BINARY_SUBTRACT  
             1670  LOAD_FAST                'uncoversize'
           1672_0  COME_FROM          1348  '1348'
             1672  ROT_TWO          
             1674  STORE_FAST               'width'
             1676  STORE_FAST               'height'
             1678  JUMP_FORWARD       1774  'to 1774'
           1680_0  COME_FROM          1572  '1572'
           1680_1  COME_FROM          1128  '1128'

 L. 198      1680  LOAD_FAST                'block'
             1682  LOAD_CONST               None
             1684  LOAD_CONST               None
             1686  BUILD_SLICE_2         2 
             1688  LOAD_FAST                'coversize'
             1690  LOAD_CONST               2
             1692  BINARY_FLOOR_DIVIDE
             1694  LOAD_FAST                'blocksize'
             1696  LOAD_FAST                'coversize'
             1698  LOAD_CONST               2
             1700  BINARY_FLOOR_DIVIDE
             1702  BINARY_SUBTRACT  
             1704  BUILD_SLICE_2         2 

 L. 199      1706  LOAD_FAST                'coversize'
             1708  LOAD_CONST               2
             1710  BINARY_FLOOR_DIVIDE
             1712  LOAD_FAST                'blocksize'
             1714  LOAD_FAST                'coversize'
             1716  LOAD_CONST               2
             1718  BINARY_FLOOR_DIVIDE
             1720  BINARY_SUBTRACT  
             1722  BUILD_SLICE_2         2 
             1724  BUILD_TUPLE_3         3 
             1726  BINARY_SUBSCR    
             1728  STORE_FAST               'block'

 L. 201      1730  LOAD_FAST                'j'
             1732  LOAD_FAST                'uncoversize'
             1734  BINARY_MULTIPLY  
             1736  LOAD_FAST                'coversize'
             1738  LOAD_CONST               2
             1740  BINARY_FLOOR_DIVIDE
             1742  BINARY_ADD       
             1744  LOAD_FAST                'i'
             1746  LOAD_FAST                'uncoversize'
             1748  BINARY_MULTIPLY  
             1750  LOAD_FAST                'coversize'
             1752  LOAD_CONST               2
             1754  BINARY_FLOOR_DIVIDE
             1756  BINARY_ADD       
             1758  ROT_TWO          
             1760  STORE_FAST               'col_off'
             1762  STORE_FAST               'row_off'

 L. 202      1764  LOAD_FAST                'uncoversize'
             1766  LOAD_FAST                'uncoversize'
             1768  ROT_TWO          
             1770  STORE_FAST               'width'
             1772  STORE_FAST               'height'
           1774_0  COME_FROM          1678  '1678'
           1774_1  COME_FROM          1564  '1564'
           1774_2  COME_FROM          1448  '1448'
           1774_3  COME_FROM          1220  '1220'
           1774_4  COME_FROM          1000  '1000'
           1774_5  COME_FROM           866  '866'

 L. 204      1774  LOAD_FAST                'p'
             1776  LOAD_CONST               1
             1778  INPLACE_ADD      
             1780  STORE_FAST               'p'

 L. 205      1782  LOAD_FAST                'dst'
             1784  LOAD_ATTR                write
             1786  LOAD_FAST                'block'
             1788  LOAD_GLOBAL              Window
             1790  LOAD_FAST                'col_off'
             1792  LOAD_FAST                'row_off'
             1794  LOAD_FAST                'width'
             1796  LOAD_FAST                'height'
             1798  CALL_FUNCTION_4       4  '4 positional arguments'
             1800  LOAD_CONST               ('window',)
             1802  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1804  POP_TOP          

 L. 206      1806  LOAD_GLOBAL              view_bar
             1808  LOAD_FAST                'p'
             1810  LOAD_FAST                'height_block'
             1812  LOAD_CONST               1
             1814  BINARY_ADD       
             1816  LOAD_FAST                'width_block'
             1818  LOAD_CONST               1
             1820  BINARY_ADD       
             1822  BINARY_MULTIPLY  
             1824  CALL_FUNCTION_2       2  '2 positional arguments'
             1826  POP_TOP          
         1828_1830  JUMP_BACK           280  'to 280'
             1832  POP_BLOCK        
           1834_0  COME_FROM_LOOP      264  '264'
         1834_1836  JUMP_BACK           258  'to 258'
             1838  POP_BLOCK        
           1840_0  COME_FROM_LOOP      242  '242'

 L. 208      1840  LOAD_FAST                'dst'
             1842  LOAD_METHOD              close
             1844  CALL_METHOD_0         0  '0 positional arguments'
             1846  POP_TOP          

 L. 209      1848  LOAD_FAST                'self'
             1850  LOAD_METHOD              close_model
             1852  CALL_METHOD_0         0  '0 positional arguments'
             1854  POP_TOP          

 L. 211      1856  LOAD_GLOBAL              get_output_datasource
             1858  LOAD_FAST                'out_ds'
             1860  CALL_FUNCTION_1       1  '1 positional argument'
             1862  STORE_FAST               'ds'

 L. 212      1864  LOAD_GLOBAL              check_output_datasource
             1866  LOAD_FAST                'ds'
             1868  CALL_FUNCTION_1       1  '1 positional argument'
             1870  POP_TOP          

 L. 213      1872  LOAD_GLOBAL              import_tif
             1874  LOAD_FAST                'tmp_file'
             1876  LOAD_FAST                'ds'
             1878  LOAD_FAST                'out_dataset_name'
             1880  LOAD_CONST               True
             1882  LOAD_CONST               ('output', 'out_dataset_name', 'is_import_as_grid')
             1884  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
             1886  STORE_FAST               'odst'

 L. 214      1888  LOAD_GLOBAL              os
             1890  LOAD_METHOD              remove
             1892  LOAD_FAST                'tmp_file'
             1894  CALL_METHOD_1         1  '1 positional argument'
             1896  POP_TOP          

 L. 216      1898  LOAD_GLOBAL              raster_to_vector
             1900  LOAD_FAST                'ds'
             1902  LOAD_FAST                'odst'
             1904  LOAD_CONST               0
             1906  BINARY_SUBSCR    
             1908  BINARY_SUBSCR    
             1910  LOAD_STR                 'class_type'
             1912  LOAD_GLOBAL              DatasetType
             1914  LOAD_ATTR                REGION

 L. 217      1916  LOAD_CONST               0

 L. 218      1918  LOAD_CONST               True
             1920  LOAD_FAST                'out_ds'

 L. 219      1922  LOAD_FAST                'out_dataset_name'
             1924  LOAD_STR                 '_region'
             1926  BINARY_ADD       
             1928  LOAD_CONST               ('out_dataset_type', 'back_or_no_value', 'is_thin_raster', 'out_data', 'out_dataset_name')
             1930  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
             1932  STORE_FAST               'result'
             1934  POP_BLOCK        
             1936  LOAD_CONST               None
           1938_0  COME_FROM_WITH      104  '104'
             1938  WITH_CLEANUP_START
             1940  WITH_CLEANUP_FINISH
             1942  END_FINALLY      
             1944  POP_BLOCK        
             1946  LOAD_CONST               None
           1948_0  COME_FROM_WITH       90  '90'
             1948  WITH_CLEANUP_START
             1950  WITH_CLEANUP_FINISH
             1952  END_FINALLY      

Parse error at or near `COME_FROM' instruction at offset 1672_0

    def _predict_tile_local(self, pre_tile, next_tile, out_shape):
        """
        利用给定的模型使用tensorflow推断得到模型预测结果
        :param predict_tile:  ndarray 需要预测的数组片 形状为 （tile_nums,:） 即第一列为图片的数量
        :param out_shape: tuple 输出结果的形状  如（100,320,320,1）
        :return:  ndarray 返回预测的结果
        """
        x1_tensor_name = self.signature['predict'].inputs['images0'].name
        x2_tensor_name = self.signature['predict'].inputs['images1'].name
        y_tensor_name = self.signature['predict'].outputs['scores'].name
        x1 = self.sess.graph.get_tensor_by_name(x1_tensor_name)
        x2 = self.sess.graph.get_tensor_by_name(x2_tensor_name)
        y = self.sess.graph.get_tensor_by_name(y_tensor_name)
        self.sess.graph.finalize
        batch_size = 1
        assert pre_tile.shape[0] == next_tile.shape[0], 'before after image shape should be same'
        total_batch = int(pre_tile.shape[0] / batch_size)
        for i in range(total_batch):
            out = self.sess.run(y, feed_dict={x1: pre_tile[i * batch_size:(i + 1) * batch_size, :], 
             x2: pre_tile[i * batch_size:(i + 1) * batch_size, :]})
            if i == 0:
                y_all = out
            else:
                y_all = np.concatenate((y_all, out), 0)

        y_out = np.expand_dims(y_all, axis=0)
        y_out.resize(out_shape)
        return y_out


class ChangeUNetTrainer(Trainer):

    def __init__(self):
        super().__init__
        self.model_type = 'change'
        self.model_architecture = 'change_unet'

    def train(self, train_data_path, config, epoch=1, batch_size=1, lr=0.001, output_model_path='./', output_model_name='change_unet', log_path=None, backbone_name='resnext50', backbone_weight_path=None, reload_model=False, pretrained_model_path=None):
        K.clear_session
        self.train_data_path = train_data_path
        self.config = config
        self.epoch = epoch
        self.batch_size = batch_size
        self.lr = lr
        self.output_model_path = output_model_path
        self.output_model_name = output_model_name
        self.backbone_name = backbone_name
        if self.backbone_name is None or self.backbone_name.strip == '':
            log_warning('backbone_name 为空,将使用默认 backbone_name')
            self.backbone_name = 'resnext50'
        else:
            if self.backbone_name != 'resnext50':
                log_warning('backbone_name 不支持 {} ,将使用默认 backbone_name'.format(backbone_name))
                self.backbone_name = 'resnext50'
        self.backbone_weight_path = backbone_weight_path
        self.pretrained_model_path = pretrained_model_path
        self.log_path = log_path
        self.reload_model = reload_model
        self.init_callbacks(log_path)
        self.config.trainer.num_epochs = epoch
        self.config.trainer.batch_size = batch_size
        self.config.model.learning_rate = lr
        self.input_bands = self.config.model.input_bands
        if len(self.input_bands) > 0:
            tmp_num = self.input_bands[0]
            for i in self.input_bands:
                assert i >= 1, '输入波段数应大于等于1'
                assert tmp_num == i, '各个输入波段数应相等'

        self.output_bands = self.config.model.output_bands
        assert self.output_bands >= 1, '输出波段数应大于等于1'
        self.split_size = self.config.data.split_size
        self.class_type = self.config.model.ClassType
        if self.pretrained_model_path is not None:
            self.model = build_model((self.split_size), (self.split_size), (self.input_bands[0]), (self.output_bands), backbone_name=(self.backbone_name),
              encoder_weights=None,
              net_type='change_unet')
            checkpoint = find_lastself.pretrained_model_pathself.config.exp.name
            if checkpoint and os.path.exists(checkpoint):
                log_info('从 {} 下加载预训练模型'.format(checkpoint))
                self.model.load_weights(checkpoint, by_name=True)
            else:
                log_error('{} 中没有预训练模型'.format(self.pretrained_model_path))
        else:
            if self.backbone_weight_path is not None and os.path.isfile(self.backbone_weight_path):
                if os.path.exists(self.backbone_weight_path):
                    keras_cache_file, cache_file = get_weights_default_pathweights_collectionself.backbone_name'imagenet'False
                    if os.path.exists(cache_file) is not True:
                        log_info('从 {} 下加载主干网络模型'.format(self.backbone_weight_path))
                        if os.path.exists(os.path.dirname(keras_cache_file)) is not True:
                            os.makedirs(os.path.dirname(keras_cache_file))
                        shutil.copy2(self.backbone_weight_path, keras_cache_file)
                    else:
                        log_info('缓存模型已存在')
                self.model = build_model((self.split_size), (self.split_size), (self.input_bands[0]), (self.output_bands), backbone_name=(self.backbone_name),
                  encoder_weights='imagenet',
                  net_type='change_unet')
            elif self.output_bands == 1:
                self.model.compile(loss=bce_dice_loss, optimizer=Adam(lr=(self.lr)),
                  metrics=[
                 'acc', dice_coef])
            else:
                self.model.compile(loss=categorical_crossentropy, optimizer=Adam(lr=(self.lr)),
                  metrics={
                 'acc', categorical_crossentropy, dice_coef})
            self._init_data
            train_path = os.path.joinself.train_data_path'csv_path''train.csv'
            val_path = os.path.joinself.train_data_path'csv_path''val.csv'
            x, y = self._get_data_from_csv(train_path, False, image_size=(self.split_size))
            history = self.model.fit(x=x,
              y=y,
              validation_data=self._get_data_from_csv(val_path, False, image_size=(self.split_size)),
              epochs=(self.config.trainer.num_epochs),
              verbose=(self.config.trainer.verbose_training),
              batch_size=(self.config.trainer.batch_size),
              callbacks=(self.callbacks))
            self.loss.extend(history.history['loss'])
            self.acc.extend(history.history['acc'])
            self.val_loss.extend(history.history['val_loss'])
            self.val_acc.extend(history.history['val_acc'])
            checkpoint = os.path.join(tempfile.gettempdir, 'checkpoint')
            self.model.save_weights(checkpoint)
            K.clear_session
            K.set_learning_phase(0)
            export_model = build_model((self.config.data.split_size), (self.config.data.split_size), (self.input_bands[0]), (self.output_bands),
              backbone_name=(self.backbone_name),
              encoder_weights=None,
              net_type='change_unet')
            export_model.load_weights(checkpoint)
            self._save_tfserving_model(export_model, os.path.join(output_model_path, output_model_name))
            K.clear_session

    def _init_data(self):
        split_train_val_change_det([os.path.join(self.train_data_path, 'PreImages')], [
         os.path.join(self.train_data_path, 'NextImages')],
          [
         os.path.join(self.train_data_path, 'Masks')],
          (os.path.join(self.train_data_path, 'csv_path')),
          x_ext=(self.config.data.x_ext),
          y_ext=(self.config.data.y_ext),
          val_scale=(self.config.data.val_scale))

    def _get_data_from_csv(self, data_path, is_aug=False, image_size=None):
        if self.output_bands > 1:
            if data_path.endswith('.csv'):
                x1, x2, y = get_changedet_image_from_csv(data_path, is_aug, band_num=(self.output_bands), image_size=image_size)
            else:
                raise Exception('You should input a *.csv file')
        else:
            return (
             [
              x1, x2], y)
            if data_path.endswith('.csv'):
                x1, x2, y = get_changedet_image_from_csv(data_path, is_aug, image_size=image_size)
            else:
                raise Exception('You should input a *.csv file')
        return (
         [
          x1, x2], y)