# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/ml\vision\_models\dlinknet\estimation_tf.py
# Compiled at: 2019-12-31 04:09:01
# Size of source mod 2**32: 8808 bytes
import os, sys, tempfile, cv2, numpy as np, rasterio, tensorflow as tf
from rasterio.plot import reshape_as_image
from rasterio.windows import Window
from tensorflow.python.platform import gfile
from iobjectspy import export_to_geojson
from iobjectspy import raster_to_vector, DatasourceConnectionInfo, Datasource, import_tif, DatasetType, EngineType
from iobjectspy.ml.toolkit._toolkit import view_bar

class DlinknetEstimationTf:

    def __init__(self):
        self.sess = None
        self.tf_inputs = None
        self.tf_outputs = None

    def augment_data(self, input_tile):
        img90 = np.array(np.rot90(input_tile))
        img1 = np.concatenate([input_tile[None], img90[None]])
        img2 = np.array(img1)[:, ::-1]
        img3 = np.concatenate([img1, img2])
        img4 = np.array(img3)[:, :, ::-1]
        img5 = img3.transpose(0, 3, 1, 2)
        img_augment1 = np.array(img5, np.float32) / 255.0 * 3.2 - 1.6
        img6 = img4.transpose(0, 3, 1, 2)
        img_augment2 = np.array(img6, np.float32) / 255.0 * 3.2 - 1.6
        return (
         img_augment1, img_augment2)

    def estimate_tile(self, tile_augment1, tile_augment2):
        maska = self.sess.run((self.tf_outputs), feed_dict={self.tf_inputs: tile_augment1})
        maskb = self.sess.run((self.tf_outputs), feed_dict={self.tf_inputs: tile_augment2})
        maska = maska.reshape(4, 1024, 1024)
        maskb = maskb.reshape(4, 1024, 1024)
        mask1 = maska + maskb[:, :, ::-1]
        mask2 = mask1[:2] + mask1[2:, ::-1]
        mask3 = mask2[0] + np.rot90(mask2[1])[::-1, ::-1]
        mask3[mask3 >= 4.5] = 255
        mask3[mask3 < 4.5] = 0
        mask3 = mask3.reshape(1, mask3.shape[0], mask3.shape[1])
        return mask3

    def estimate_img--- This code section failed: ---

 L.  58         0  LOAD_FAST                'out_format'
                2  LOAD_STR                 'vector'
                4  COMPARE_OP               ==
                6  POP_JUMP_IF_FALSE    18  'to 18'

 L.  59         8  LOAD_GLOBAL              tempfile
               10  LOAD_METHOD              mkdtemp
               12  CALL_METHOD_0         0  '0 positional arguments'
               14  STORE_FAST               'out_mask_path'
               16  JUMP_FORWARD         22  'to 22'
             18_0  COME_FROM             6  '6'

 L.  61        18  LOAD_FAST                'out_path'
               20  STORE_FAST               'out_mask_path'
             22_0  COME_FROM            16  '16'

 L.  62        22  LOAD_GLOBAL              rasterio
               24  LOAD_METHOD              open
               26  LOAD_FAST                'input_img'
               28  CALL_METHOD_1         1  '1 positional argument'
               30  STORE_FAST               'img_in'

 L.  64        32  LOAD_FAST                'config'
               34  LOAD_ATTR                ModelInput
               36  LOAD_ATTR                Width
               38  STORE_FAST               'blocksize'

 L.  65        40  LOAD_FAST                'blocksize'
               42  LOAD_FAST                'coversize'
               44  BINARY_SUBTRACT  
               46  STORE_FAST               'uncoversize'

 L.  66        48  LOAD_FAST                'img_in'
               50  LOAD_ATTR                width
               52  LOAD_FAST                'coversize'
               54  LOAD_CONST               2
               56  BINARY_FLOOR_DIVIDE
               58  BINARY_SUBTRACT  
               60  LOAD_FAST                'uncoversize'
               62  BINARY_FLOOR_DIVIDE
               64  STORE_FAST               'width_block'

 L.  67        66  LOAD_FAST                'img_in'
               68  LOAD_ATTR                height
               70  LOAD_FAST                'coversize'
               72  LOAD_CONST               2
               74  BINARY_FLOOR_DIVIDE
               76  BINARY_SUBTRACT  
               78  LOAD_FAST                'uncoversize'
               80  BINARY_FLOOR_DIVIDE
               82  STORE_FAST               'height_block'

 L.  69        84  LOAD_FAST                'img_in'
               86  LOAD_ATTR                width
               88  LOAD_FAST                'blocksize'
               90  COMPARE_OP               <
               92  POP_JUMP_IF_TRUE    104  'to 104'
               94  LOAD_FAST                'img_in'
               96  LOAD_ATTR                height
               98  LOAD_FAST                'blocksize'
              100  COMPARE_OP               <
              102  POP_JUMP_IF_FALSE   150  'to 150'
            104_0  COME_FROM            92  '92'

 L.  70       104  LOAD_GLOBAL              sys
              106  LOAD_ATTR                stderr
              108  LOAD_METHOD              write

 L.  71       110  LOAD_STR                 'Iuput data is too small, it should be larger than '
              112  LOAD_GLOBAL              str
              114  LOAD_FAST                'blocksize'
              116  CALL_FUNCTION_1       1  '1 positional argument'
              118  BINARY_ADD       
              120  LOAD_STR                 'x'
              122  BINARY_ADD       
              124  LOAD_GLOBAL              str
              126  LOAD_FAST                'blocksize'
              128  CALL_FUNCTION_1       1  '1 positional argument'
              130  BINARY_ADD       
              132  LOAD_STR                 '!'
              134  BINARY_ADD       
              136  CALL_METHOD_1         1  '1 positional argument'
              138  POP_TOP          

 L.  72       140  LOAD_GLOBAL              sys
              142  LOAD_METHOD              exit
              144  LOAD_CONST               1
              146  CALL_METHOD_1         1  '1 positional argument'
              148  POP_TOP          
            150_0  COME_FROM           102  '102'

 L.  73       150  LOAD_GLOBAL              os
              152  LOAD_ATTR                path
              154  LOAD_METHOD              join
              156  LOAD_FAST                'out_mask_path'
              158  LOAD_FAST                'out_dataset_name'
              160  LOAD_STR                 '.tif'
              162  BINARY_ADD       
              164  CALL_METHOD_2         2  '2 positional arguments'
              166  STORE_FAST               'out_file'

 L.  74       168  LOAD_GLOBAL              rasterio
              170  LOAD_ATTR                open
              172  LOAD_FAST                'out_file'
              174  LOAD_STR                 'w'
              176  LOAD_STR                 'GTiff'
              178  LOAD_FAST                'img_in'
              180  LOAD_ATTR                width

 L.  75       182  LOAD_FAST                'img_in'
              184  LOAD_ATTR                height

 L.  76       186  LOAD_CONST               1
              188  LOAD_FAST                'img_in'
              190  LOAD_ATTR                bounds
              192  LOAD_FAST                'img_in'
              194  LOAD_ATTR                crs
              196  LOAD_FAST                'img_in'
              198  LOAD_ATTR                transform

 L.  77       200  LOAD_GLOBAL              np
              202  LOAD_ATTR                uint8
              204  LOAD_STR                 'lzw'
              206  LOAD_CONST               ('driver', 'width', 'height', 'count', 'bounds', 'crs', 'transform', 'dtype', 'compress')
              208  CALL_FUNCTION_KW_11    11  '11 total positional and keyword args'
              210  STORE_FAST               'img_out'

 L.  78       212  LOAD_FAST                'coversize'
              214  LOAD_CONST               0
              216  COMPARE_OP               ==
              218  POP_JUMP_IF_FALSE   226  'to 226'

 L.  79       220  LOAD_CONST               0
              222  STORE_FAST               'plusnum'
              224  JUMP_FORWARD        230  'to 230'
            226_0  COME_FROM           218  '218'

 L.  81       226  LOAD_CONST               1
              228  STORE_FAST               'plusnum'
            230_0  COME_FROM           224  '224'

 L.  82       230  LOAD_CONST               0
              232  STORE_FAST               'p'

 L.  83       234  LOAD_FAST                'self'
              236  LOAD_METHOD              load_model
              238  LOAD_FAST                'model_path'
              240  CALL_METHOD_1         1  '1 positional argument'
              242  POP_TOP          

 L.  84   244_246  SETUP_LOOP         1522  'to 1522'
              248  LOAD_GLOBAL              range
              250  LOAD_FAST                'height_block'
              252  LOAD_FAST                'plusnum'
              254  BINARY_ADD       
              256  CALL_FUNCTION_1       1  '1 positional argument'
              258  GET_ITER         
          260_262  FOR_ITER           1520  'to 1520'
              264  STORE_FAST               'i'

 L.  85   266_268  SETUP_LOOP         1516  'to 1516'
              270  LOAD_GLOBAL              range
              272  LOAD_FAST                'width_block'
              274  LOAD_FAST                'plusnum'
              276  BINARY_ADD       
              278  CALL_FUNCTION_1       1  '1 positional argument'
              280  GET_ITER         
          282_284  FOR_ITER           1514  'to 1514'
              286  STORE_FAST               'j'

 L.  89       288  LOAD_GLOBAL              np
              290  LOAD_ATTR                zeros
              292  LOAD_FAST                'config'
              294  LOAD_ATTR                ModelInput
              296  LOAD_ATTR                Bands
              298  LOAD_FAST                'blocksize'
              300  LOAD_FAST                'blocksize'
              302  BUILD_LIST_3          3 
              304  LOAD_GLOBAL              np
              306  LOAD_ATTR                uint8
              308  LOAD_CONST               ('dtype',)
              310  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              312  STORE_FAST               'block'

 L.  90       314  LOAD_FAST                'img_in'
              316  LOAD_ATTR                read
              318  LOAD_GLOBAL              Window
              320  LOAD_FAST                'j'
              322  LOAD_FAST                'uncoversize'
              324  BINARY_MULTIPLY  
              326  LOAD_FAST                'i'
              328  LOAD_FAST                'uncoversize'
              330  BINARY_MULTIPLY  
              332  LOAD_FAST                'blocksize'
              334  LOAD_FAST                'blocksize'
              336  CALL_FUNCTION_4       4  '4 positional arguments'
              338  LOAD_CONST               ('window',)
              340  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              342  STORE_FAST               'img'

 L.  91       344  LOAD_FAST                'img'
              346  LOAD_CONST               None
              348  LOAD_FAST                'config'
              350  LOAD_ATTR                ModelInput
              352  LOAD_ATTR                Bands
              354  BUILD_SLICE_2         2 
              356  LOAD_CONST               None
              358  LOAD_CONST               None
              360  BUILD_SLICE_2         2 
              362  LOAD_CONST               None
              364  LOAD_CONST               None
              366  BUILD_SLICE_2         2 
              368  BUILD_TUPLE_3         3 
              370  BINARY_SUBSCR    
              372  LOAD_FAST                'block'
              374  LOAD_CONST               None
              376  LOAD_CONST               None
              378  BUILD_SLICE_2         2 
              380  LOAD_CONST               None
              382  LOAD_FAST                'img'
              384  LOAD_ATTR                shape
              386  LOAD_CONST               1
              388  BINARY_SUBSCR    
              390  BUILD_SLICE_2         2 
              392  LOAD_CONST               None
              394  LOAD_FAST                'img'
              396  LOAD_ATTR                shape
              398  LOAD_CONST               2
              400  BINARY_SUBSCR    
              402  BUILD_SLICE_2         2 
              404  BUILD_TUPLE_3         3 
              406  STORE_SUBSCR     

 L.  92       408  LOAD_GLOBAL              reshape_as_image
              410  LOAD_FAST                'block'
              412  CALL_FUNCTION_1       1  '1 positional argument'
              414  STORE_FAST               'block'

 L.  93       416  LOAD_GLOBAL              cv2
              418  LOAD_METHOD              cvtColor
              420  LOAD_FAST                'block'
              422  LOAD_GLOBAL              cv2
              424  LOAD_ATTR                COLOR_RGB2BGR
              426  CALL_METHOD_2         2  '2 positional arguments'
              428  STORE_FAST               'block'

 L.  96       430  LOAD_FAST                'self'
              432  LOAD_METHOD              augment_data
              434  LOAD_FAST                'block'
              436  CALL_METHOD_1         1  '1 positional argument'
              438  UNPACK_SEQUENCE_2     2 
              440  STORE_FAST               'img1'
              442  STORE_FAST               'img2'

 L.  99       444  LOAD_FAST                'self'
              446  LOAD_METHOD              estimate_tile
              448  LOAD_FAST                'img1'
              450  LOAD_FAST                'img2'
              452  CALL_METHOD_2         2  '2 positional arguments'
              454  STORE_FAST               'mask'

 L. 102       456  LOAD_FAST                'i'
              458  LOAD_CONST               0
              460  COMPARE_OP               ==
          462_464  POP_JUMP_IF_FALSE   556  'to 556'
              466  LOAD_FAST                'j'
              468  LOAD_CONST               0
              470  COMPARE_OP               ==
          472_474  POP_JUMP_IF_FALSE   556  'to 556'

 L. 103       476  LOAD_FAST                'mask'
              478  LOAD_CONST               None
              480  LOAD_CONST               None
              482  BUILD_SLICE_2         2 
              484  LOAD_CONST               None
              486  LOAD_FAST                'blocksize'
              488  LOAD_FAST                'coversize'
              490  LOAD_CONST               2
              492  BINARY_FLOOR_DIVIDE
              494  BINARY_SUBTRACT  
              496  BUILD_SLICE_2         2 
              498  LOAD_CONST               None
              500  LOAD_FAST                'blocksize'
              502  LOAD_FAST                'coversize'
              504  LOAD_CONST               2
              506  BINARY_FLOOR_DIVIDE
              508  BINARY_SUBTRACT  
              510  BUILD_SLICE_2         2 
              512  BUILD_TUPLE_3         3 
              514  BINARY_SUBSCR    
              516  STORE_FAST               'mask'

 L. 105       518  LOAD_CONST               (0, 0)
              520  UNPACK_SEQUENCE_2     2 
              522  STORE_FAST               'col_off'
              524  STORE_FAST               'row_off'

 L. 106       526  LOAD_FAST                'uncoversize'
              528  LOAD_FAST                'coversize'
              530  LOAD_CONST               2
              532  BINARY_FLOOR_DIVIDE
              534  BINARY_ADD       
              536  LOAD_FAST                'uncoversize'
              538  LOAD_FAST                'coversize'
              540  LOAD_CONST               2
              542  BINARY_FLOOR_DIVIDE
              544  BINARY_ADD       
              546  ROT_TWO          
              548  STORE_FAST               'width'
              550  STORE_FAST               'height'
          552_554  JUMP_FORWARD       1448  'to 1448'
            556_0  COME_FROM           472  '472'
            556_1  COME_FROM           462  '462'

 L. 108       556  LOAD_FAST                'i'
              558  LOAD_FAST                'height_block'
              560  COMPARE_OP               ==
          562_564  POP_JUMP_IF_FALSE   690  'to 690'
              566  LOAD_FAST                'j'
              568  LOAD_FAST                'width_block'
              570  COMPARE_OP               ==
          572_574  POP_JUMP_IF_FALSE   690  'to 690'

 L. 109       576  LOAD_FAST                'mask'
              578  LOAD_CONST               None
              580  LOAD_CONST               None
              582  BUILD_SLICE_2         2 
              584  LOAD_FAST                'coversize'
              586  LOAD_CONST               2
              588  BINARY_FLOOR_DIVIDE
              590  LOAD_FAST                'img_in'
              592  LOAD_ATTR                height
              594  LOAD_FAST                'i'
              596  LOAD_FAST                'uncoversize'
              598  BINARY_MULTIPLY  
              600  BINARY_SUBTRACT  
              602  BUILD_SLICE_2         2 

 L. 110       604  LOAD_FAST                'coversize'
              606  LOAD_CONST               2
              608  BINARY_FLOOR_DIVIDE
              610  LOAD_FAST                'img_in'
              612  LOAD_ATTR                width
              614  LOAD_FAST                'j'
              616  LOAD_FAST                'uncoversize'
              618  BINARY_MULTIPLY  
              620  BINARY_SUBTRACT  
              622  BUILD_SLICE_2         2 
              624  BUILD_TUPLE_3         3 
              626  BINARY_SUBSCR    
              628  STORE_FAST               'mask'

 L. 112       630  LOAD_FAST                'j'
              632  LOAD_FAST                'uncoversize'
              634  BINARY_MULTIPLY  
              636  LOAD_FAST                'coversize'
              638  LOAD_CONST               2
              640  BINARY_FLOOR_DIVIDE
              642  BINARY_ADD       
              644  LOAD_FAST                'i'
              646  LOAD_FAST                'uncoversize'
              648  BINARY_MULTIPLY  
              650  LOAD_FAST                'coversize'
              652  LOAD_CONST               2
              654  BINARY_FLOOR_DIVIDE
              656  BINARY_ADD       
              658  ROT_TWO          
              660  STORE_FAST               'col_off'
              662  STORE_FAST               'row_off'

 L. 113       664  LOAD_FAST                'img_in'
              666  LOAD_ATTR                width
              668  LOAD_FAST                'col_off'
              670  BINARY_SUBTRACT  
              672  LOAD_FAST                'img_in'
              674  LOAD_ATTR                height
              676  LOAD_FAST                'row_off'
              678  BINARY_SUBTRACT  
              680  ROT_TWO          
              682  STORE_FAST               'width'
              684  STORE_FAST               'height'
          686_688  JUMP_FORWARD       1448  'to 1448'
            690_0  COME_FROM           572  '572'
            690_1  COME_FROM           562  '562'

 L. 115       690  LOAD_FAST                'i'
              692  LOAD_CONST               0
              694  COMPARE_OP               ==
          696_698  POP_JUMP_IF_FALSE   910  'to 910'
              700  LOAD_FAST                'j'
              702  LOAD_CONST               0
              704  COMPARE_OP               !=
          706_708  POP_JUMP_IF_FALSE   910  'to 910'

 L. 116       710  LOAD_FAST                'j'
              712  LOAD_FAST                'width_block'
              714  COMPARE_OP               ==
          716_718  POP_JUMP_IF_FALSE   816  'to 816'

 L. 118       720  LOAD_FAST                'mask'
              722  LOAD_CONST               None
              724  LOAD_CONST               None
              726  BUILD_SLICE_2         2 
              728  LOAD_CONST               None
              730  LOAD_FAST                'blocksize'
              732  LOAD_FAST                'coversize'
              734  LOAD_CONST               2
              736  BINARY_FLOOR_DIVIDE
              738  BINARY_SUBTRACT  
              740  BUILD_SLICE_2         2 

 L. 119       742  LOAD_FAST                'coversize'
              744  LOAD_CONST               2
              746  BINARY_FLOOR_DIVIDE
              748  LOAD_FAST                'img_in'
              750  LOAD_ATTR                width
              752  LOAD_FAST                'j'
              754  LOAD_FAST                'uncoversize'
              756  BINARY_MULTIPLY  
              758  BINARY_SUBTRACT  
              760  BUILD_SLICE_2         2 
              762  BUILD_TUPLE_3         3 
              764  BINARY_SUBSCR    
              766  STORE_FAST               'mask'

 L. 121       768  LOAD_FAST                'j'
              770  LOAD_FAST                'uncoversize'
              772  BINARY_MULTIPLY  
              774  LOAD_FAST                'coversize'
              776  LOAD_CONST               2
              778  BINARY_FLOOR_DIVIDE
              780  BINARY_ADD       
              782  LOAD_CONST               0
              784  ROT_TWO          
              786  STORE_FAST               'col_off'
              788  STORE_FAST               'row_off'

 L. 122       790  LOAD_FAST                'img_in'
              792  LOAD_ATTR                width
              794  LOAD_FAST                'col_off'
              796  BINARY_SUBTRACT  
              798  LOAD_FAST                'uncoversize'
              800  LOAD_FAST                'coversize'
              802  LOAD_CONST               2
              804  BINARY_FLOOR_DIVIDE
              806  BINARY_ADD       
              808  ROT_TWO          
              810  STORE_FAST               'width'
              812  STORE_FAST               'height'
              814  JUMP_FORWARD       1448  'to 1448'
            816_0  COME_FROM           716  '716'

 L. 125       816  LOAD_FAST                'mask'
              818  LOAD_CONST               None
              820  LOAD_CONST               None
              822  BUILD_SLICE_2         2 
              824  LOAD_CONST               None
              826  LOAD_FAST                'blocksize'
              828  LOAD_FAST                'coversize'
              830  LOAD_CONST               2
              832  BINARY_FLOOR_DIVIDE
              834  BINARY_SUBTRACT  
              836  BUILD_SLICE_2         2 
              838  LOAD_FAST                'coversize'
              840  LOAD_CONST               2
              842  BINARY_FLOOR_DIVIDE
              844  LOAD_FAST                'blocksize'
              846  LOAD_FAST                'coversize'
              848  LOAD_CONST               2
              850  BINARY_FLOOR_DIVIDE
              852  BINARY_SUBTRACT  
              854  BUILD_SLICE_2         2 
              856  BUILD_TUPLE_3         3 
              858  BINARY_SUBSCR    
              860  STORE_FAST               'mask'

 L. 127       862  LOAD_FAST                'j'
              864  LOAD_FAST                'uncoversize'
              866  BINARY_MULTIPLY  
              868  LOAD_FAST                'coversize'
              870  LOAD_CONST               2
              872  BINARY_FLOOR_DIVIDE
              874  BINARY_ADD       
              876  LOAD_FAST                'i'
              878  LOAD_FAST                'uncoversize'
              880  BINARY_MULTIPLY  
              882  ROT_TWO          
              884  STORE_FAST               'col_off'
              886  STORE_FAST               'row_off'

 L. 128       888  LOAD_FAST                'uncoversize'
              890  LOAD_FAST                'uncoversize'
              892  LOAD_FAST                'coversize'
              894  LOAD_CONST               2
              896  BINARY_FLOOR_DIVIDE
              898  BINARY_ADD       
              900  ROT_TWO          
              902  STORE_FAST               'width'
              904  STORE_FAST               'height'
          906_908  JUMP_FORWARD       1448  'to 1448'
            910_0  COME_FROM           706  '706'
            910_1  COME_FROM           696  '696'

 L. 130       910  LOAD_FAST                'i'
              912  LOAD_CONST               0
              914  COMPARE_OP               !=
          916_918  POP_JUMP_IF_FALSE  1126  'to 1126'
              920  LOAD_FAST                'j'
              922  LOAD_CONST               0
              924  COMPARE_OP               ==
          926_928  POP_JUMP_IF_FALSE  1126  'to 1126'

 L. 131       930  LOAD_FAST                'i'
              932  LOAD_FAST                'height_block'
              934  COMPARE_OP               ==
          936_938  POP_JUMP_IF_FALSE  1036  'to 1036'

 L. 132       940  LOAD_FAST                'mask'
              942  LOAD_CONST               None
              944  LOAD_CONST               None
              946  BUILD_SLICE_2         2 
              948  LOAD_FAST                'coversize'
              950  LOAD_CONST               2
              952  BINARY_FLOOR_DIVIDE
              954  LOAD_FAST                'img_in'
              956  LOAD_ATTR                height
              958  LOAD_FAST                'i'
              960  LOAD_FAST                'uncoversize'
              962  BINARY_MULTIPLY  
              964  BINARY_SUBTRACT  
              966  BUILD_SLICE_2         2 
              968  LOAD_CONST               None

 L. 133       970  LOAD_FAST                'blocksize'
              972  LOAD_FAST                'coversize'
              974  LOAD_CONST               2
              976  BINARY_FLOOR_DIVIDE
              978  BINARY_SUBTRACT  
              980  BUILD_SLICE_2         2 
              982  BUILD_TUPLE_3         3 
              984  BINARY_SUBSCR    
              986  STORE_FAST               'mask'

 L. 135       988  LOAD_CONST               0
              990  LOAD_FAST                'i'
              992  LOAD_FAST                'uncoversize'
              994  BINARY_MULTIPLY  
              996  LOAD_FAST                'coversize'
              998  LOAD_CONST               2
             1000  BINARY_FLOOR_DIVIDE
             1002  BINARY_ADD       
             1004  ROT_TWO          
             1006  STORE_FAST               'col_off'
             1008  STORE_FAST               'row_off'

 L. 136      1010  LOAD_FAST                'uncoversize'
             1012  LOAD_FAST                'coversize'
             1014  LOAD_CONST               2
             1016  BINARY_FLOOR_DIVIDE
             1018  BINARY_ADD       
             1020  LOAD_FAST                'img_in'
             1022  LOAD_ATTR                height
             1024  LOAD_FAST                'row_off'
             1026  BINARY_SUBTRACT  
             1028  ROT_TWO          
             1030  STORE_FAST               'width'
             1032  STORE_FAST               'height'
             1034  JUMP_FORWARD       1448  'to 1448'
           1036_0  COME_FROM           936  '936'

 L. 139      1036  LOAD_FAST                'mask'
             1038  LOAD_CONST               None
             1040  LOAD_CONST               None
             1042  BUILD_SLICE_2         2 
             1044  LOAD_FAST                'coversize'
             1046  LOAD_CONST               2
             1048  BINARY_FLOOR_DIVIDE
             1050  LOAD_FAST                'blocksize'
             1052  LOAD_FAST                'coversize'
             1054  LOAD_CONST               2
             1056  BINARY_FLOOR_DIVIDE
             1058  BINARY_SUBTRACT  
             1060  BUILD_SLICE_2         2 
             1062  LOAD_CONST               None
             1064  LOAD_FAST                'blocksize'
             1066  LOAD_FAST                'coversize'
             1068  LOAD_CONST               2
             1070  BINARY_FLOOR_DIVIDE
             1072  BINARY_SUBTRACT  
             1074  BUILD_SLICE_2         2 
             1076  BUILD_TUPLE_3         3 
             1078  BINARY_SUBSCR    
             1080  STORE_FAST               'mask'

 L. 141      1082  LOAD_CONST               0
             1084  LOAD_FAST                'i'
             1086  LOAD_FAST                'uncoversize'
             1088  BINARY_MULTIPLY  
             1090  LOAD_FAST                'coversize'
             1092  LOAD_CONST               2
             1094  BINARY_FLOOR_DIVIDE
             1096  BINARY_ADD       
             1098  ROT_TWO          
             1100  STORE_FAST               'col_off'
             1102  STORE_FAST               'row_off'

 L. 142      1104  LOAD_FAST                'uncoversize'
             1106  LOAD_FAST                'coversize'
             1108  LOAD_CONST               2
             1110  BINARY_FLOOR_DIVIDE
             1112  BINARY_ADD       
             1114  LOAD_FAST                'uncoversize'
             1116  ROT_TWO          
             1118  STORE_FAST               'width'
             1120  STORE_FAST               'height'
         1122_1124  JUMP_FORWARD       1448  'to 1448'
           1126_0  COME_FROM           926  '926'
           1126_1  COME_FROM           916  '916'

 L. 145      1126  LOAD_FAST                'i'
             1128  LOAD_FAST                'height_block'
             1130  COMPARE_OP               ==
         1132_1134  POP_JUMP_IF_FALSE  1240  'to 1240'

 L. 146      1136  LOAD_FAST                'mask'
             1138  LOAD_CONST               None
             1140  LOAD_CONST               None
             1142  BUILD_SLICE_2         2 
             1144  LOAD_FAST                'coversize'
             1146  LOAD_CONST               2
             1148  BINARY_FLOOR_DIVIDE
             1150  LOAD_FAST                'img_in'
             1152  LOAD_ATTR                height
             1154  LOAD_FAST                'i'
             1156  LOAD_FAST                'uncoversize'
             1158  BINARY_MULTIPLY  
             1160  BINARY_SUBTRACT  
             1162  BUILD_SLICE_2         2 

 L. 147      1164  LOAD_FAST                'coversize'
             1166  LOAD_CONST               2
             1168  BINARY_FLOOR_DIVIDE
             1170  LOAD_FAST                'blocksize'
             1172  LOAD_FAST                'coversize'
             1174  LOAD_CONST               2
             1176  BINARY_FLOOR_DIVIDE
             1178  BINARY_SUBTRACT  
             1180  BUILD_SLICE_2         2 
             1182  BUILD_TUPLE_3         3 
             1184  BINARY_SUBSCR    
             1186  STORE_FAST               'mask'

 L. 149      1188  LOAD_FAST                'j'
             1190  LOAD_FAST                'uncoversize'
             1192  BINARY_MULTIPLY  
             1194  LOAD_FAST                'coversize'
             1196  LOAD_CONST               2
             1198  BINARY_FLOOR_DIVIDE
             1200  BINARY_ADD       
             1202  LOAD_FAST                'i'
             1204  LOAD_FAST                'uncoversize'
             1206  BINARY_MULTIPLY  
             1208  LOAD_FAST                'coversize'
             1210  LOAD_CONST               2
             1212  BINARY_FLOOR_DIVIDE
             1214  BINARY_ADD       
             1216  ROT_TWO          
             1218  STORE_FAST               'col_off'
             1220  STORE_FAST               'row_off'

 L. 150      1222  LOAD_FAST                'uncoversize'
             1224  LOAD_FAST                'img_in'
             1226  LOAD_ATTR                height
             1228  LOAD_FAST                'row_off'
             1230  BINARY_SUBTRACT  
             1232  ROT_TWO          
             1234  STORE_FAST               'width'
             1236  STORE_FAST               'height'
             1238  JUMP_FORWARD       1448  'to 1448'
           1240_0  COME_FROM          1132  '1132'

 L. 152      1240  LOAD_FAST                'j'
             1242  LOAD_FAST                'width_block'
             1244  COMPARE_OP               ==
         1246_1248  POP_JUMP_IF_FALSE  1354  'to 1354'

 L. 153      1250  LOAD_FAST                'mask'
             1252  LOAD_CONST               None
             1254  LOAD_CONST               None
             1256  BUILD_SLICE_2         2 
             1258  LOAD_FAST                'coversize'
             1260  LOAD_CONST               2
             1262  BINARY_FLOOR_DIVIDE
             1264  LOAD_FAST                'blocksize'
             1266  LOAD_FAST                'coversize'
             1268  LOAD_CONST               2
             1270  BINARY_FLOOR_DIVIDE
             1272  BINARY_SUBTRACT  
             1274  BUILD_SLICE_2         2 

 L. 154      1276  LOAD_FAST                'coversize'
             1278  LOAD_CONST               2
             1280  BINARY_FLOOR_DIVIDE
             1282  LOAD_FAST                'img_in'
             1284  LOAD_ATTR                width
             1286  LOAD_FAST                'j'
             1288  LOAD_FAST                'uncoversize'
             1290  BINARY_MULTIPLY  
             1292  BINARY_SUBTRACT  
             1294  BUILD_SLICE_2         2 
             1296  BUILD_TUPLE_3         3 
             1298  BINARY_SUBSCR    
             1300  STORE_FAST               'mask'

 L. 156      1302  LOAD_FAST                'j'
             1304  LOAD_FAST                'uncoversize'
             1306  BINARY_MULTIPLY  
             1308  LOAD_FAST                'coversize'
             1310  LOAD_CONST               2
             1312  BINARY_FLOOR_DIVIDE
             1314  BINARY_ADD       
             1316  LOAD_FAST                'i'
             1318  LOAD_FAST                'uncoversize'
             1320  BINARY_MULTIPLY  
             1322  LOAD_FAST                'coversize'
             1324  LOAD_CONST               2
             1326  BINARY_FLOOR_DIVIDE
             1328  BINARY_ADD       
             1330  ROT_TWO          
             1332  STORE_FAST               'col_off'
             1334  STORE_FAST               'row_off'

 L. 157      1336  LOAD_FAST                'img_in'
             1338  LOAD_ATTR                width
             1340  LOAD_FAST                'col_off'
             1342  BINARY_SUBTRACT  
             1344  LOAD_FAST                'uncoversize'
             1346  ROT_TWO          
             1348  STORE_FAST               'width'
             1350  STORE_FAST               'height'
             1352  JUMP_FORWARD       1448  'to 1448'
           1354_0  COME_FROM          1246  '1246'
           1354_1  COME_FROM           814  '814'

 L. 160      1354  LOAD_FAST                'mask'
             1356  LOAD_CONST               None
           1358_0  COME_FROM          1034  '1034'
             1358  LOAD_CONST               None
             1360  BUILD_SLICE_2         2 
             1362  LOAD_FAST                'coversize'
             1364  LOAD_CONST               2
             1366  BINARY_FLOOR_DIVIDE
             1368  LOAD_FAST                'blocksize'
             1370  LOAD_FAST                'coversize'
             1372  LOAD_CONST               2
             1374  BINARY_FLOOR_DIVIDE
             1376  BINARY_SUBTRACT  
             1378  BUILD_SLICE_2         2 

 L. 161      1380  LOAD_FAST                'coversize'
             1382  LOAD_CONST               2
             1384  BINARY_FLOOR_DIVIDE
             1386  LOAD_FAST                'blocksize'
             1388  LOAD_FAST                'coversize'
             1390  LOAD_CONST               2
             1392  BINARY_FLOOR_DIVIDE
             1394  BINARY_SUBTRACT  
             1396  BUILD_SLICE_2         2 
             1398  BUILD_TUPLE_3         3 
             1400  BINARY_SUBSCR    
             1402  STORE_FAST               'mask'

 L. 163      1404  LOAD_FAST                'j'
             1406  LOAD_FAST                'uncoversize'
             1408  BINARY_MULTIPLY  
             1410  LOAD_FAST                'coversize'
             1412  LOAD_CONST               2
             1414  BINARY_FLOOR_DIVIDE
             1416  BINARY_ADD       
             1418  LOAD_FAST                'i'
             1420  LOAD_FAST                'uncoversize'
             1422  BINARY_MULTIPLY  
             1424  LOAD_FAST                'coversize'
             1426  LOAD_CONST               2
             1428  BINARY_FLOOR_DIVIDE
             1430  BINARY_ADD       
             1432  ROT_TWO          
             1434  STORE_FAST               'col_off'
             1436  STORE_FAST               'row_off'

 L. 164      1438  LOAD_FAST                'uncoversize'
             1440  LOAD_FAST                'uncoversize'
             1442  ROT_TWO          
             1444  STORE_FAST               'width'
             1446  STORE_FAST               'height'
           1448_0  COME_FROM          1352  '1352'
           1448_1  COME_FROM          1238  '1238'
           1448_2  COME_FROM          1122  '1122'
           1448_3  COME_FROM           906  '906'
           1448_4  COME_FROM           686  '686'
           1448_5  COME_FROM           552  '552'

 L. 166      1448  LOAD_FAST                'p'
             1450  LOAD_CONST               1
             1452  INPLACE_ADD      
             1454  STORE_FAST               'p'

 L. 167      1456  LOAD_FAST                'img_out'
             1458  LOAD_ATTR                write
             1460  LOAD_FAST                'mask'
             1462  LOAD_METHOD              astype
             1464  LOAD_GLOBAL              np
             1466  LOAD_ATTR                uint8
             1468  CALL_METHOD_1         1  '1 positional argument'
             1470  LOAD_GLOBAL              Window
             1472  LOAD_FAST                'col_off'
             1474  LOAD_FAST                'row_off'
             1476  LOAD_FAST                'width'
             1478  LOAD_FAST                'height'
             1480  CALL_FUNCTION_4       4  '4 positional arguments'
             1482  LOAD_CONST               ('window',)
             1484  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1486  POP_TOP          

 L. 169      1488  LOAD_GLOBAL              view_bar
             1490  LOAD_FAST                'p'
             1492  LOAD_FAST                'height_block'
             1494  LOAD_FAST                'plusnum'
             1496  BINARY_ADD       
             1498  LOAD_FAST                'width_block'
             1500  LOAD_FAST                'plusnum'
             1502  BINARY_ADD       
             1504  BINARY_MULTIPLY  
             1506  CALL_FUNCTION_2       2  '2 positional arguments'
             1508  POP_TOP          
         1510_1512  JUMP_BACK           282  'to 282'
             1514  POP_BLOCK        
           1516_0  COME_FROM_LOOP      266  '266'
         1516_1518  JUMP_BACK           260  'to 260'
             1520  POP_BLOCK        
           1522_0  COME_FROM_LOOP      244  '244'

 L. 171      1522  LOAD_FAST                'self'
             1524  LOAD_METHOD              close_model
             1526  CALL_METHOD_0         0  '0 positional arguments'
             1528  POP_TOP          

 L. 172      1530  LOAD_FAST                'img_in'
             1532  LOAD_METHOD              close
             1534  CALL_METHOD_0         0  '0 positional arguments'
             1536  POP_TOP          

 L. 173      1538  LOAD_FAST                'img_out'
             1540  LOAD_METHOD              close
             1542  CALL_METHOD_0         0  '0 positional arguments'
             1544  POP_TOP          

 L. 175      1546  LOAD_FAST                'out_format'
             1548  LOAD_STR                 'vector'
             1550  COMPARE_OP               ==
         1552_1554  POP_JUMP_IF_FALSE  1662  'to 1662'

 L. 176      1556  LOAD_GLOBAL              DatasourceConnectionInfo
             1558  LOAD_STR                 ''
             1560  LOAD_GLOBAL              EngineType
             1562  LOAD_ATTR                MEMORY
             1564  LOAD_CONST               ('server', 'engine_type')
             1566  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1568  STORE_FAST               'tmp_dsc'

 L. 177      1570  LOAD_GLOBAL              Datasource
             1572  CALL_FUNCTION_0       0  '0 positional arguments'
             1574  LOAD_METHOD              create
             1576  LOAD_FAST                'tmp_dsc'
             1578  CALL_METHOD_1         1  '1 positional argument'
             1580  STORE_FAST               'tmp_ds'

 L. 179      1582  LOAD_GLOBAL              import_tif
             1584  LOAD_FAST                'out_file'
             1586  LOAD_FAST                'tmp_ds'
             1588  LOAD_STR                 'mask_tmp'
             1590  LOAD_CONST               True
             1592  LOAD_CONST               ('output', 'out_dataset_name', 'is_import_as_grid')
             1594  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
             1596  POP_TOP          

 L. 180      1598  LOAD_GLOBAL              os
             1600  LOAD_METHOD              remove
             1602  LOAD_FAST                'out_file'
             1604  CALL_METHOD_1         1  '1 positional argument'
             1606  POP_TOP          

 L. 182      1608  LOAD_GLOBAL              raster_to_vector
             1610  LOAD_FAST                'tmp_ds'
             1612  LOAD_STR                 'mask_tmp'
             1614  BINARY_SUBSCR    
             1616  LOAD_STR                 'class_type'
             1618  LOAD_GLOBAL              DatasetType
             1620  LOAD_ATTR                REGION
             1622  LOAD_CONST               0

 L. 183      1624  LOAD_FAST                'tmp_ds'
             1626  LOAD_FAST                'out_dataset_name'
             1628  LOAD_CONST               ('out_dataset_type', 'back_or_no_value', 'out_data', 'out_dataset_name')
             1630  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
             1632  POP_TOP          

 L. 184      1634  LOAD_GLOBAL              export_to_geojson
             1636  LOAD_FAST                'tmp_ds'
             1638  LOAD_FAST                'out_dataset_name'
             1640  BINARY_SUBSCR    
             1642  LOAD_GLOBAL              os
             1644  LOAD_ATTR                path
             1646  LOAD_METHOD              join
             1648  LOAD_FAST                'out_path'
             1650  LOAD_FAST                'out_dataset_name'
             1652  CALL_METHOD_2         2  '2 positional arguments'
             1654  LOAD_STR                 '.json'
             1656  BINARY_ADD       
             1658  CALL_FUNCTION_2       2  '2 positional arguments'
             1660  POP_TOP          
           1662_0  COME_FROM          1552  '1552'

Parse error at or near `COME_FROM' instruction at offset 1358_0

    def load_model(self, model_path):
        model_path = os.path.join(model_path, 'saved_model.pb')
        self.sess = tf.Session
        with gfile.FastGFile(model_path, 'rb') as (f):
            graph_def = tf.GraphDef
            graph_def.ParseFromString(f.read)
            self.sess.graph.as_default
            tf.import_graph_def(graph_def, name='')
        self.sess.graph.finalize
        self.tf_inputs = self.sess.graph.get_tensor_by_name('input:0')
        self.tf_outputs = self.sess.graph.get_tensor_by_name('Sigmoid:0')

    def close_model(self):
        self.sess.close
        tf.reset_default_graph