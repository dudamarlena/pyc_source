# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/ml\vision\_models\semantic_seg\unet.py
# Compiled at: 2019-12-31 04:09:04
# Size of source mod 2**32: 61784 bytes
"""
@author: YangRuijie
@license: 
@contact: yangruijie@supermap.com
@software: 
@file: unet.py.py
@time: 4/4/19 3:33 AM
@desc:
"""
import os
from iobjectspy._jsuperpy.data._util import get_output_datasource, get_input_dataset
from toolkit._keras_loss import IOUScore
from ....._logger import log_error, log_warning, log_info
os.environ['KERAS_BACKEND'] = 'tensorflow'
import shutil, tempfile
from iobjectspy import Dataset, raster_to_vector, DatasourceConnectionInfo, Datasource, import_tif, DatasetType, datasetraster_to_numpy_array, numpy_array_to_datasetraster, EngineType
from toolkit._toolkit import view_bar, stretch_n, get_percentclip_min_max, stretch_min_max, get_image_from_csv, split_train_val_withdirs, get_config_from_yaml
from toolkit._keras_model_utils import bce_dice_loss, dice_coef, find_last
from .base_keras_models import Trainer
from _seg_models.model_builder import build_model
from _seg_models.backbones.cls_models.cls_models.utils import get_weights_default_path
from _seg_models.backbones.cls_models.cls_models.weights import weights_collection
import numpy as np, rasterio, tensorflow as tf
from rasterio.plot import reshape_as_image, reshape_as_raster
from rasterio.windows import Window
from keras import Input, Model
from keras import backend as K
K.set_image_data_format('channels_last')
from keras.layers import Conv2D, MaxPooling2D, concatenate, Lambda, Conv2DTranspose, Dropout
from keras.losses import binary_crossentropy, categorical_crossentropy
from keras.optimizers import Adam
from keras.regularizers import l2

class UnetEstimation:

    def __init__(self, model_path, config):
        if not isinstance(model_path, str):
            raise TypeError('model_path data type inappropriate ，should be str ')
        if not os.path.exists(model_path):
            raise Exception('model_path  path not exists')
        self.model_input = config.model_input[0]
        self.model_output = config.model_output[0]
        if np.argmin(self.model_input.shape) == 0:
            self.band_order = 'first'
            self.seg_size = self.model_input.shape[1]
            self.input_bands = self.model_input.shape[0]
            self.out_width_height = [self.model_output.shape[1], self.model_output.shape[2]]
            self.output_msk_num = self.model_output.shape[0]
            if self.model_input.shape[1] != self.model_input.shape[2]:
                raise ValueError('Model input width and height should be equal!')
        else:
            self.band_order = 'last'
            self.seg_size = self.model_input.shape[1]
            self.input_bands = self.model_input.shape[(-1)]
            self.out_width_height = [self.model_output.shape[0], self.model_output.shape[1]]
            self.output_msk_num = self.model_output.shape[(-1)]
            if self.model_input.shape[1] != self.model_input.shape[0]:
                raise ValueError('Model input width and height should be equal!')
            self.class_type = config.class_type
            self.color_map = {c.class_value:tuple(c.class_color) for c in self.class_type}
            self.is_stretch = config.is_stretch
            self.model_path = model_path
            self.sess = None
            self.tf_inputs = None
            self.tf_outputs = None
            self.load_model(model_path)

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

    def estimate_img(self, input_img, coversize, out_path, out_dataset_name, result_type, **kwargs):
        """

        :param input_img:
        :param coversize:
        :param out_path:
        :param out_dataset_name:
        :param result_type: region or grid
        :param kwargs:
        :return:
        """
        self.half_oversize = coversize
        dsm_dataset = kwargs.get('dsm_dataset')
        if not result_type in ('grid', 'region'):
            raise AssertionError('result_type should be grid or region')
        else:
            if self.output_msk_num > 1:
                self.back_or_no_value = -9999
            else:
                self.back_or_no_value = 0
            dom_is_udb = False
            try:
                rasterio.open(input_img)
            except Exception as e:
                try:
                    dom_is_udb = True
                finally:
                    e = None
                    del e

            if dom_is_udb:
                if isinstance(input_img, str):
                    input_img = get_input_dataset(input_img)
                else:
                    if not isinstance(input_img, Dataset):
                        raise TypeError('image_dataset data type inappropriate ，should be  str or Dataset')
                    else:
                        dom_bounds = input_img.bounds
                        x_pixel_res = (dom_bounds.right - dom_bounds.left) / input_img.width
                        y_pixel_res = (dom_bounds.top - dom_bounds.bottom) / input_img.height
                        coord_array = [
                         x_pixel_res,
                         0,
                         0,
                         y_pixel_res,
                         dom_bounds.left,
                         dom_bounds.bottom]
                        if not dsm_dataset is None:
                            input_martix = dsm_dataset or datasetraster_to_numpy_array(input_img)
                        else:
                            pass
                        dom = datasetraster_to_numpy_array(input_img)
                        dsm = datasetraster_to_numpy_array(dsm_dataset)
                        input_martix = np.concatenate((dom, dsm[np.newaxis, :, :]))
                    result_int, result_dataset = self._predict_with_matix(input_martix,
                      out_path, out_dataset_name, coord_array=coord_array, band_order='first', result_type=result_type)
            else:
                result_dataset = self.predict_with_rasterio(input_img, dsm_dataset, out_path, out_dataset_name,
                  result_type=result_type)
        return result_dataset

    def estimate_numpy(self, input_img, coversize, **kwargs):
        self.half_oversize = coversize
        result_numpy = self._predict_with_numpy(input_img, self.band_order)
        return result_numpy

    def estimate_tile(self, input_img, single_thresold=0.5):
        if self.band_order == 'first':
            assert input_img.shape[0] == self.model_input.shape[0], 'channel first channel顺序不对或channel数量不对'
            assert input_img.shape[1] <= self.seg_size, '输入图像长宽应小于等于{}'.format(self.seg_size)
            assert input_img.shape[2] <= self.seg_size, '输入图像长宽应小于等于{}'.format(self.seg_size)
            input_width_height = [input_img.shape[1], input_img.shape[2]]
            process_img = np.pad(input_img, (
             (0, 0), (0, self.seg_size - input_img.shape[1]), (0, self.seg_size - input_img.shape[2])), 'constant')
        else:
            assert input_img.shape[2] == self.model_input.shape[2], 'channel last channel顺序不对或channel数量不对'
            assert input_img.shape[0] <= self.seg_size, '输入图像长宽应小于等于{}'.format(self.seg_size)
            assert input_img.shape[1] <= self.seg_size, '输入图像长宽应小于等于{}'.format(self.seg_size)
            input_width_height = [input_img.shape[0], input_img.shape[1]]
            process_img = np.pad(input_img, (
             (
              0, self.seg_size - input_img.shape[0]), (0, self.seg_size - input_img.shape[1]), (0, 0)), 'constant')
        output_img_shape = (
         self.out_width_height[0], self.out_width_height[1], self.output_msk_num)
        result_tile = self._predict_tile_local(process_img[(np.newaxis, ...)], output_img_shape)
        if self.output_msk_num > 1:
            result_tile = np.argmax(result_tile, 0 if self.band_order == 'first' else -1).astype(input_img.dtype)
        else:
            predict_msk = result_tile[0, :, :] if self.band_order == 'first' else result_tile[:, :, 0]
            result_tile = (predict_msk > single_thresold).astype(input_img.dtype)
        return result_tile[:input_width_height[0], :input_width_height[1]]

    def _predict_with_numpy(self, image_matix, band_order='last', single_thresold=0.5):
        if self.band_order is not band_order:
            if band_order is 'first':
                image_matix = np.transpose(image_matix, (1, 2, 0))
            else:
                if band_order is 'last':
                    image_matix = np.transpose(image_matix, (2, 0, 1))
                else:
                    raise Exception('band_order参数错误')
        else:
            predict_msk = self._UnetEstimation__predict_with_preload(image_matix)
            if self.output_msk_num > 1:
                predict_int = np.argmax(predict_msk, 0 if self.band_order == 'first' else -1)
            else:
                predict_msk = predict_msk[0, :, :] if self.band_order == 'first' else predict_msk[:, :, 0]
            predict_int = predict_msk > single_thresold
        return predict_int

    def _predict_with_matix(self, image_matix, out_ds, dst_name, band_order='last', coord_array=[1, 0, 0, 1, 0, 0], single_thresold=0.5, result_type='grid'):
        """
        基于输入的图像矩阵，得到的预测结果二值图和矢量数据

        :param image_matix: ndarray输入的原始图像矩阵
        :param out_ds: 输出矢量数据要存储的数据源
        :param dst_name: 输出矢量数据集的名字
        :param band_order: 输入数据集的band所在维度 'last' or 'first'
        :param coord_array: array 数组，依次为 0——X方向上的象素分辨素， 1——X方向的旋转系数，2——Y方向的旋转系数，
            3——Y方向上的象素分辨率，4——栅格地图左下角象素中心X坐标，5——栅格地图左下角象素中心Y坐标
        :param single_thresold:  概率阈值，概率超过该值的像素则会输出为矢量
        :param result_type: grid or region
        :type result_type: str
        :return: （predict_int,result） predict_int——ndarray 二值或多值二维矩阵,result——矢量数据集
        """
        if self.band_order is not band_order:
            if band_order is 'first':
                image_matix = np.transpose(image_matix, (1, 2, 0))
            else:
                if band_order is 'last':
                    image_matix = np.transpose(image_matix, (2, 0, 1))
                else:
                    raise Exception('band_order参数错误')
        else:
            predict_msk = self._UnetEstimation__predict(image_matix)
            if self.output_msk_num > 1:
                predict_int = np.argmax(predict_msk, 0 if self.band_order == 'first' else -1)
            else:
                predict_msk = predict_msk[0, :, :] if self.band_order == 'first' else predict_msk[:, :, 0]
                predict_int = predict_msk > single_thresold
            predict_int = predict_int.astype(np.int)
            tmp_dsc = DatasourceConnectionInfo(server=':memory:', engine_type=(EngineType.MEMORY))
            tmp_ds = Datasource().create(tmp_dsc)
            result_dst = numpy_array_to_datasetraster(predict_int, (coord_array[0]), (coord_array[3]), tmp_ds, (coord_array[4]),
              (coord_array[5]), 'tmp', as_grid=True)
            if result_type.strip() == 'grid':
                out_ds = get_output_datasource(out_ds)
                result = out_ds.copy_dataset(result_dst, dst_name)
            else:
                if result_type.strip() == 'region':
                    result = raster_to_vector(result_dst, 'class_type', out_dataset_type=(DatasetType.REGION), back_or_no_value=(self.back_or_no_value),
                      is_thin_raster=True,
                      out_data=out_ds,
                      out_dataset_name=dst_name)
                else:
                    raise Exception('result_type error ,result_type should be region or grid')
        tmp_ds.delete_all()
        tmp_ds.close()
        return (
         predict_int, result)

    def predict_with_rasterio--- This code section failed: ---

 L. 266         0  LOAD_FAST                'self'
                2  LOAD_ATTR                half_oversize
                4  LOAD_CONST               2
                6  BINARY_MULTIPLY  
                8  STORE_FAST               'coversize'

 L. 267        10  LOAD_FAST                'self'
               12  LOAD_ATTR                seg_size
               14  STORE_FAST               'blocksize'

 L. 268        16  LOAD_FAST                'coversize'
               18  LOAD_CONST               2
               20  BINARY_MODULO    
               22  LOAD_CONST               0
               24  COMPARE_OP               !=
               26  POP_JUMP_IF_FALSE    38  'to 38'

 L. 269        28  LOAD_GLOBAL              ValueError
               30  LOAD_STR                 'coversize must be even number!'
               32  CALL_FUNCTION_1       1  '1 positional argument'
               34  RAISE_VARARGS_1       1  'exception instance'
               36  JUMP_FORWARD         74  'to 74'
             38_0  COME_FROM            26  '26'

 L. 270        38  LOAD_FAST                'coversize'
               40  LOAD_FAST                'blocksize'
               42  COMPARE_OP               ==
               44  POP_JUMP_IF_FALSE    56  'to 56'

 L. 271        46  LOAD_GLOBAL              ValueError
               48  LOAD_STR                 'coversize and blocksize is same!'
               50  CALL_FUNCTION_1       1  '1 positional argument'
               52  RAISE_VARARGS_1       1  'exception instance'
               54  JUMP_FORWARD         74  'to 74'
             56_0  COME_FROM            44  '44'

 L. 272        56  LOAD_FAST                'coversize'
               58  LOAD_FAST                'blocksize'
               60  COMPARE_OP               >
               62  POP_JUMP_IF_FALSE    74  'to 74'

 L. 273        64  LOAD_GLOBAL              ValueError
               66  LOAD_STR                 'coversize is bigger than blocksize!'
               68  CALL_FUNCTION_1       1  '1 positional argument'
               70  RAISE_VARARGS_1       1  'exception instance'
               72  JUMP_FORWARD         74  'to 74'
             74_0  COME_FROM            72  '72'
             74_1  COME_FROM            62  '62'
             74_2  COME_FROM            54  '54'
             74_3  COME_FROM            36  '36'

 L. 277        74  LOAD_FAST                'blocksize'
               76  LOAD_FAST                'coversize'
               78  BINARY_SUBTRACT  
               80  STORE_FAST               'uncoversize'

 L. 279        82  LOAD_GLOBAL              rasterio
               84  LOAD_METHOD              open
               86  LOAD_FAST                'dom_path'
               88  CALL_METHOD_1         1  '1 positional argument'
            90_92  SETUP_WITH         2358  'to 2358'
               94  STORE_FAST               'ds'

 L. 280        96  LOAD_CONST               None
               98  STORE_FAST               'dsm_ds'

 L. 281       100  SETUP_EXCEPT        230  'to 230'

 L. 282       102  LOAD_GLOBAL              rasterio
              104  LOAD_METHOD              open
              106  LOAD_FAST                'dsm_path'
              108  CALL_METHOD_1         1  '1 positional argument'
              110  STORE_FAST               'dsm_ds'

 L. 283       112  SETUP_EXCEPT        184  'to 184'

 L. 284       114  LOAD_GLOBAL              get_percentclip_min_max
              116  LOAD_FAST                'dom_path'
              118  CALL_FUNCTION_1       1  '1 positional argument'
              120  UNPACK_SEQUENCE_2     2 
              122  STORE_FAST               'all_min'
              124  STORE_FAST               'all_max'

 L. 285       126  LOAD_GLOBAL              get_percentclip_min_max
              128  LOAD_FAST                'dsm_path'
              130  CALL_FUNCTION_1       1  '1 positional argument'
              132  UNPACK_SEQUENCE_2     2 
              134  STORE_FAST               'dsm_min'
              136  STORE_FAST               'dsm_max'

 L. 286       138  LOAD_FAST                'all_min'
              140  LOAD_METHOD              extend
              142  LOAD_FAST                'dsm_min'
              144  CALL_METHOD_1         1  '1 positional argument'
              146  POP_TOP          

 L. 287       148  LOAD_FAST                'all_max'
              150  LOAD_METHOD              extend
              152  LOAD_FAST                'dsm_max'
              154  CALL_METHOD_1         1  '1 positional argument'
              156  POP_TOP          

 L. 288       158  LOAD_GLOBAL              np
              160  LOAD_METHOD              array
              162  LOAD_FAST                'all_max'
              164  CALL_METHOD_1         1  '1 positional argument'
              166  LOAD_GLOBAL              np
              168  LOAD_METHOD              array
              170  LOAD_FAST                'all_min'
              172  CALL_METHOD_1         1  '1 positional argument'
              174  ROT_TWO          
              176  STORE_FAST               'all_max'
              178  STORE_FAST               'all_min'
              180  POP_BLOCK        
              182  JUMP_FORWARD        226  'to 226'
            184_0  COME_FROM_EXCEPT    112  '112'

 L. 289       184  DUP_TOP          
              186  LOAD_GLOBAL              Exception
              188  COMPARE_OP               exception-match
              190  POP_JUMP_IF_FALSE   224  'to 224'
              192  POP_TOP          
              194  STORE_FAST               'e1'
              196  POP_TOP          
              198  SETUP_FINALLY       212  'to 212'

 L. 290       200  LOAD_GLOBAL              Exception
              202  LOAD_STR                 'get_percentclip_min_max, 此功能需要安装gdal python版'
              204  CALL_FUNCTION_1       1  '1 positional argument'
              206  RAISE_VARARGS_1       1  'exception instance'
              208  POP_BLOCK        
              210  LOAD_CONST               None
            212_0  COME_FROM_FINALLY   198  '198'
              212  LOAD_CONST               None
              214  STORE_FAST               'e1'
              216  DELETE_FAST              'e1'
              218  END_FINALLY      
              220  POP_EXCEPT       
              222  JUMP_FORWARD        226  'to 226'
            224_0  COME_FROM           190  '190'
              224  END_FINALLY      
            226_0  COME_FROM           222  '222'
            226_1  COME_FROM           182  '182'
              226  POP_BLOCK        
              228  JUMP_FORWARD        298  'to 298'
            230_0  COME_FROM_EXCEPT    100  '100'

 L. 291       230  DUP_TOP          
              232  LOAD_GLOBAL              Exception
              234  COMPARE_OP               exception-match
          236_238  POP_JUMP_IF_FALSE   296  'to 296'
              240  POP_TOP          
              242  STORE_FAST               'e'
              244  POP_TOP          
              246  SETUP_FINALLY       284  'to 284'

 L. 292       248  LOAD_STR                 'get_percentclip_min_max'
              250  LOAD_FAST                'e'
              252  LOAD_ATTR                args
              254  LOAD_CONST               0
              256  BINARY_SUBSCR    
              258  COMPARE_OP               in
          260_262  POP_JUMP_IF_FALSE   272  'to 272'

 L. 293       264  LOAD_GLOBAL              Exception
              266  LOAD_STR                 'get_percentclip_min_max, 此功能需要安装gdal python版'
              268  CALL_FUNCTION_1       1  '1 positional argument'
              270  RAISE_VARARGS_1       1  'exception instance'
            272_0  COME_FROM           260  '260'

 L. 294       272  LOAD_GLOBAL              log_warning
              274  LOAD_STR                 'No DSM Data，Only Predict With DOM'
              276  CALL_FUNCTION_1       1  '1 positional argument'
              278  POP_TOP          
              280  POP_BLOCK        
              282  LOAD_CONST               None
            284_0  COME_FROM_FINALLY   246  '246'
              284  LOAD_CONST               None
              286  STORE_FAST               'e'
              288  DELETE_FAST              'e'
              290  END_FINALLY      
              292  POP_EXCEPT       
              294  JUMP_FORWARD        298  'to 298'
            296_0  COME_FROM           236  '236'
              296  END_FINALLY      
            298_0  COME_FROM           294  '294'
            298_1  COME_FROM           228  '228'

 L. 296       298  LOAD_FAST                'ds'
              300  LOAD_ATTR                width
              302  LOAD_FAST                'coversize'
              304  LOAD_CONST               2
              306  BINARY_FLOOR_DIVIDE
              308  BINARY_SUBTRACT  
              310  LOAD_FAST                'uncoversize'
              312  BINARY_FLOOR_DIVIDE
              314  STORE_FAST               'width_block'

 L. 297       316  LOAD_FAST                'ds'
              318  LOAD_ATTR                height
              320  LOAD_FAST                'coversize'
              322  LOAD_CONST               2
              324  BINARY_FLOOR_DIVIDE
              326  BINARY_SUBTRACT  
              328  LOAD_FAST                'uncoversize'
              330  BINARY_FLOOR_DIVIDE
              332  STORE_FAST               'height_block'

 L. 299       334  LOAD_GLOBAL              os
              336  LOAD_ATTR                path
              338  LOAD_METHOD              join
              340  LOAD_GLOBAL              tempfile
              342  LOAD_METHOD              mkdtemp
              344  CALL_METHOD_0         0  '0 positional arguments'
              346  LOAD_STR                 'tmp.tif'
              348  CALL_METHOD_2         2  '2 positional arguments'
              350  STORE_FAST               'tmp_file'

 L. 300       352  LOAD_GLOBAL              rasterio
              354  LOAD_ATTR                open
              356  LOAD_FAST                'tmp_file'
              358  LOAD_STR                 'w'
              360  LOAD_STR                 'GTiff'
              362  LOAD_FAST                'ds'
              364  LOAD_ATTR                width
              366  LOAD_FAST                'ds'
              368  LOAD_ATTR                height

 L. 301       370  LOAD_CONST               1
              372  LOAD_FAST                'ds'
              374  LOAD_ATTR                bounds
              376  LOAD_FAST                'ds'
              378  LOAD_ATTR                crs
              380  LOAD_FAST                'ds'
              382  LOAD_ATTR                transform
              384  LOAD_GLOBAL              np
              386  LOAD_ATTR                uint8
              388  LOAD_CONST               ('driver', 'width', 'height', 'count', 'bounds', 'crs', 'transform', 'dtype')
              390  CALL_FUNCTION_KW_10    10  '10 total positional and keyword args'
              392  STORE_FAST               'dst'

 L. 302       394  LOAD_FAST                'dst'
              396  LOAD_METHOD              write_colormap
              398  LOAD_CONST               1
              400  LOAD_FAST                'self'
              402  LOAD_ATTR                color_map
              404  CALL_METHOD_2         2  '2 positional arguments'
              406  POP_TOP          

 L. 303       408  LOAD_CONST               0
              410  STORE_FAST               'p'

 L. 304   412_414  SETUP_LOOP         2026  'to 2026'
              416  LOAD_GLOBAL              range
              418  LOAD_FAST                'height_block'
              420  LOAD_CONST               1
              422  BINARY_ADD       
              424  CALL_FUNCTION_1       1  '1 positional argument'
              426  GET_ITER         
          428_430  FOR_ITER           2024  'to 2024'
              432  STORE_FAST               'i'

 L. 305   434_436  SETUP_LOOP         2020  'to 2020'
              438  LOAD_GLOBAL              range
              440  LOAD_FAST                'width_block'
              442  LOAD_CONST               1
              444  BINARY_ADD       
              446  CALL_FUNCTION_1       1  '1 positional argument'
              448  GET_ITER         
          450_452  FOR_ITER           2018  'to 2018'
              454  STORE_FAST               'j'

 L. 308       456  LOAD_GLOBAL              np
              458  LOAD_ATTR                zeros
              460  LOAD_FAST                'self'
              462  LOAD_ATTR                input_bands
              464  LOAD_FAST                'blocksize'
              466  LOAD_FAST                'blocksize'
              468  BUILD_LIST_3          3 
              470  LOAD_GLOBAL              np
              472  LOAD_ATTR                float64
              474  LOAD_CONST               ('dtype',)
              476  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              478  STORE_FAST               'block'

 L. 309       480  LOAD_GLOBAL              np
              482  LOAD_ATTR                zeros
              484  LOAD_CONST               1
              486  LOAD_FAST                'blocksize'
              488  LOAD_FAST                'blocksize'
              490  BUILD_LIST_3          3 
              492  LOAD_GLOBAL              np
              494  LOAD_ATTR                float64
              496  LOAD_CONST               ('dtype',)
              498  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              500  STORE_FAST               'dsm_block'

 L. 310       502  LOAD_FAST                'ds'
              504  LOAD_ATTR                read
              506  LOAD_GLOBAL              Window
              508  LOAD_FAST                'j'
              510  LOAD_FAST                'uncoversize'
              512  BINARY_MULTIPLY  
              514  LOAD_FAST                'i'
              516  LOAD_FAST                'uncoversize'
              518  BINARY_MULTIPLY  
              520  LOAD_FAST                'blocksize'
              522  LOAD_FAST                'blocksize'
              524  CALL_FUNCTION_4       4  '4 positional arguments'
              526  LOAD_CONST               ('window',)
              528  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              530  STORE_FAST               'img'

 L. 311       532  LOAD_FAST                'img'
              534  LOAD_CONST               None
              536  LOAD_FAST                'self'
              538  LOAD_ATTR                input_bands
              540  BUILD_SLICE_2         2 
              542  LOAD_CONST               None
              544  LOAD_CONST               None
              546  BUILD_SLICE_2         2 
              548  LOAD_CONST               None
              550  LOAD_CONST               None
              552  BUILD_SLICE_2         2 
              554  BUILD_TUPLE_3         3 
              556  BINARY_SUBSCR    
              558  LOAD_FAST                'block'
              560  LOAD_CONST               None
              562  LOAD_CONST               None
              564  BUILD_SLICE_2         2 
              566  LOAD_CONST               None
              568  LOAD_FAST                'img'
              570  LOAD_ATTR                shape
              572  LOAD_CONST               1
              574  BINARY_SUBSCR    
              576  BUILD_SLICE_2         2 
              578  LOAD_CONST               None
              580  LOAD_FAST                'img'
              582  LOAD_ATTR                shape
              584  LOAD_CONST               2
              586  BINARY_SUBSCR    
              588  BUILD_SLICE_2         2 
              590  BUILD_TUPLE_3         3 
              592  STORE_SUBSCR     

 L. 313       594  LOAD_GLOBAL              reshape_as_image
              596  LOAD_FAST                'block'
              598  CALL_FUNCTION_1       1  '1 positional argument'
              600  STORE_FAST               'all_block'

 L. 314       602  LOAD_FAST                'dsm_ds'
          604_606  POP_JUMP_IF_FALSE   724  'to 724'

 L. 315       608  LOAD_FAST                'dsm_ds'
              610  LOAD_ATTR                read
              612  LOAD_GLOBAL              Window
              614  LOAD_FAST                'j'
              616  LOAD_FAST                'uncoversize'
              618  BINARY_MULTIPLY  
              620  LOAD_FAST                'i'
              622  LOAD_FAST                'uncoversize'
              624  BINARY_MULTIPLY  
              626  LOAD_FAST                'blocksize'
              628  LOAD_FAST                'blocksize'
              630  CALL_FUNCTION_4       4  '4 positional arguments'
              632  LOAD_CONST               ('window',)
              634  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              636  STORE_FAST               'dsm_img'

 L. 316       638  LOAD_FAST                'dsm_img'
              640  LOAD_CONST               None
              642  LOAD_CONST               None
              644  BUILD_SLICE_2         2 
              646  LOAD_CONST               None
              648  LOAD_CONST               None
              650  BUILD_SLICE_2         2 
              652  LOAD_CONST               None
              654  LOAD_CONST               None
              656  BUILD_SLICE_2         2 
              658  BUILD_TUPLE_3         3 
              660  BINARY_SUBSCR    
              662  LOAD_FAST                'dsm_block'
              664  LOAD_CONST               None
              666  LOAD_CONST               None
              668  BUILD_SLICE_2         2 
              670  LOAD_CONST               None
              672  LOAD_FAST                'dsm_img'
              674  LOAD_ATTR                shape
              676  LOAD_CONST               1
              678  BINARY_SUBSCR    
              680  BUILD_SLICE_2         2 
              682  LOAD_CONST               None
              684  LOAD_FAST                'dsm_img'
              686  LOAD_ATTR                shape
              688  LOAD_CONST               2
              690  BINARY_SUBSCR    
              692  BUILD_SLICE_2         2 
              694  BUILD_TUPLE_3         3 
              696  STORE_SUBSCR     

 L. 317       698  LOAD_GLOBAL              reshape_as_image
              700  LOAD_FAST                'dsm_block'
              702  CALL_FUNCTION_1       1  '1 positional argument'
              704  STORE_FAST               'dsm_block'

 L. 318       706  LOAD_GLOBAL              np
              708  LOAD_ATTR                concatenate
              710  LOAD_FAST                'all_block'
              712  LOAD_FAST                'dsm_block'
              714  BUILD_TUPLE_2         2 
              716  LOAD_CONST               2
              718  LOAD_CONST               ('axis',)
              720  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              722  STORE_FAST               'all_block'
            724_0  COME_FROM           604  '604'

 L. 319       724  LOAD_FAST                'self'
              726  LOAD_ATTR                is_stretch
          728_730  POP_JUMP_IF_FALSE   778  'to 778'

 L. 320       732  LOAD_STR                 'all_max'
              734  LOAD_GLOBAL              dir
              736  CALL_FUNCTION_0       0  '0 positional arguments'
              738  COMPARE_OP               not-in
          740_742  POP_JUMP_IF_TRUE    756  'to 756'
              744  LOAD_STR                 'all_min'
              746  LOAD_GLOBAL              dir
              748  CALL_FUNCTION_0       0  '0 positional arguments'
              750  COMPARE_OP               not-in
          752_754  POP_JUMP_IF_FALSE   766  'to 766'
            756_0  COME_FROM           740  '740'

 L. 321       756  LOAD_GLOBAL              stretch_n
              758  LOAD_FAST                'all_block'
              760  CALL_FUNCTION_1       1  '1 positional argument'
              762  STORE_FAST               'all_block'
              764  JUMP_FORWARD        778  'to 778'
            766_0  COME_FROM           752  '752'

 L. 323       766  LOAD_GLOBAL              stretch_min_max
              768  LOAD_FAST                'all_block'
              770  LOAD_FAST                'all_min'
              772  LOAD_FAST                'all_max'
              774  CALL_FUNCTION_3       3  '3 positional arguments'
              776  STORE_FAST               'all_block'
            778_0  COME_FROM           764  '764'
            778_1  COME_FROM           728  '728'

 L. 324       778  LOAD_FAST                'all_block'
              780  LOAD_GLOBAL              np
              782  LOAD_ATTR                newaxis
              784  LOAD_CONST               None
              786  LOAD_CONST               None
              788  BUILD_SLICE_2         2 
              790  LOAD_CONST               None
              792  LOAD_CONST               None
              794  BUILD_SLICE_2         2 
              796  LOAD_CONST               None
              798  LOAD_CONST               None
              800  BUILD_SLICE_2         2 
              802  BUILD_TUPLE_4         4 
              804  BINARY_SUBSCR    
              806  STORE_FAST               'all_block'

 L. 327       808  LOAD_FAST                'all_block'
              810  LOAD_ATTR                shape
              812  LOAD_CONST               0
              814  BINARY_SUBSCR    
              816  LOAD_FAST                'self'
              818  LOAD_ATTR                out_width_height
              820  LOAD_CONST               0
              822  BINARY_SUBSCR    
              824  LOAD_FAST                'self'
              826  LOAD_ATTR                out_width_height
              828  LOAD_CONST               1
              830  BINARY_SUBSCR    
              832  LOAD_FAST                'self'
              834  LOAD_ATTR                output_msk_num
              836  BUILD_TUPLE_4         4 
              838  STORE_FAST               'out_shape'

 L. 328       840  LOAD_FAST                'self'
              842  LOAD_METHOD              _predict_tile_local
              844  LOAD_FAST                'all_block'
              846  LOAD_FAST                'out_shape'
              848  CALL_METHOD_2         2  '2 positional arguments'
              850  STORE_FAST               'mask_block'

 L. 329       852  LOAD_FAST                'mask_block'
              854  LOAD_CONST               0
              856  LOAD_CONST               None
              858  LOAD_CONST               None
              860  BUILD_SLICE_2         2 
              862  LOAD_CONST               None
              864  LOAD_CONST               None
              866  BUILD_SLICE_2         2 
              868  LOAD_CONST               None
              870  LOAD_CONST               None
              872  BUILD_SLICE_2         2 
              874  BUILD_TUPLE_4         4 
              876  BINARY_SUBSCR    
              878  STORE_FAST               'mask_block'

 L. 330       880  LOAD_FAST                'self'
              882  LOAD_ATTR                output_msk_num
              884  LOAD_CONST               1
              886  COMPARE_OP               >
          888_890  POP_JUMP_IF_FALSE   928  'to 928'

 L. 331       892  LOAD_GLOBAL              np
              894  LOAD_ATTR                argmax
              896  LOAD_FAST                'mask_block'
              898  LOAD_CONST               -1
              900  LOAD_CONST               ('axis',)
              902  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              904  LOAD_CONST               None
              906  LOAD_CONST               None
              908  BUILD_SLICE_2         2 
              910  LOAD_CONST               None
              912  LOAD_CONST               None
              914  BUILD_SLICE_2         2 
              916  LOAD_GLOBAL              np
              918  LOAD_ATTR                newaxis
              920  BUILD_TUPLE_3         3 
              922  BINARY_SUBSCR    
              924  STORE_FAST               'mask_int'
              926  JUMP_FORWARD        936  'to 936'
            928_0  COME_FROM           888  '888'

 L. 333       928  LOAD_FAST                'mask_block'
              930  LOAD_FAST                'single_thresold'
              932  COMPARE_OP               >
              934  STORE_FAST               'mask_int'
            936_0  COME_FROM           926  '926'

 L. 334       936  LOAD_FAST                'mask_int'
              938  LOAD_METHOD              astype
              940  LOAD_GLOBAL              np
              942  LOAD_ATTR                uint8
              944  CALL_METHOD_1         1  '1 positional argument'
              946  STORE_FAST               'mask_int'

 L. 337       948  LOAD_GLOBAL              reshape_as_raster
              950  LOAD_FAST                'mask_int'
              952  CALL_FUNCTION_1       1  '1 positional argument'
              954  STORE_FAST               'block'

 L. 340       956  LOAD_FAST                'i'
              958  LOAD_CONST               0
              960  COMPARE_OP               ==
          962_964  POP_JUMP_IF_FALSE  1056  'to 1056'
              966  LOAD_FAST                'j'
              968  LOAD_CONST               0
              970  COMPARE_OP               ==
          972_974  POP_JUMP_IF_FALSE  1056  'to 1056'

 L. 341       976  LOAD_FAST                'block'
              978  LOAD_CONST               None
              980  LOAD_CONST               None
              982  BUILD_SLICE_2         2 
              984  LOAD_CONST               None
              986  LOAD_FAST                'blocksize'
              988  LOAD_FAST                'coversize'
              990  LOAD_CONST               2
              992  BINARY_FLOOR_DIVIDE
              994  BINARY_SUBTRACT  
              996  BUILD_SLICE_2         2 
              998  LOAD_CONST               None
             1000  LOAD_FAST                'blocksize'
             1002  LOAD_FAST                'coversize'
             1004  LOAD_CONST               2
             1006  BINARY_FLOOR_DIVIDE
             1008  BINARY_SUBTRACT  
             1010  BUILD_SLICE_2         2 
             1012  BUILD_TUPLE_3         3 
             1014  BINARY_SUBSCR    
             1016  STORE_FAST               'block'

 L. 343      1018  LOAD_CONST               (0, 0)
             1020  UNPACK_SEQUENCE_2     2 
             1022  STORE_FAST               'col_off'
             1024  STORE_FAST               'row_off'

 L. 344      1026  LOAD_FAST                'uncoversize'
             1028  LOAD_FAST                'coversize'
             1030  LOAD_CONST               2
             1032  BINARY_FLOOR_DIVIDE
             1034  BINARY_ADD       
             1036  LOAD_FAST                'uncoversize'
             1038  LOAD_FAST                'coversize'
             1040  LOAD_CONST               2
             1042  BINARY_FLOOR_DIVIDE
             1044  BINARY_ADD       
             1046  ROT_TWO          
             1048  STORE_FAST               'width'
             1050  STORE_FAST               'height'
         1052_1054  JUMP_FORWARD       1960  'to 1960'
           1056_0  COME_FROM           972  '972'
           1056_1  COME_FROM           962  '962'

 L. 346      1056  LOAD_FAST                'i'
             1058  LOAD_FAST                'height_block'
             1060  COMPARE_OP               ==
         1062_1064  POP_JUMP_IF_FALSE  1190  'to 1190'
             1066  LOAD_FAST                'j'
             1068  LOAD_FAST                'width_block'
             1070  COMPARE_OP               ==
         1072_1074  POP_JUMP_IF_FALSE  1190  'to 1190'

 L. 347      1076  LOAD_FAST                'block'
             1078  LOAD_CONST               None
             1080  LOAD_CONST               None
             1082  BUILD_SLICE_2         2 
             1084  LOAD_FAST                'coversize'
             1086  LOAD_CONST               2
             1088  BINARY_FLOOR_DIVIDE
             1090  LOAD_FAST                'ds'
             1092  LOAD_ATTR                height
             1094  LOAD_FAST                'i'
             1096  LOAD_FAST                'uncoversize'
             1098  BINARY_MULTIPLY  
             1100  BINARY_SUBTRACT  
             1102  BUILD_SLICE_2         2 

 L. 348      1104  LOAD_FAST                'coversize'
             1106  LOAD_CONST               2
             1108  BINARY_FLOOR_DIVIDE
             1110  LOAD_FAST                'ds'
             1112  LOAD_ATTR                width
             1114  LOAD_FAST                'j'
             1116  LOAD_FAST                'uncoversize'
             1118  BINARY_MULTIPLY  
             1120  BINARY_SUBTRACT  
             1122  BUILD_SLICE_2         2 
             1124  BUILD_TUPLE_3         3 
             1126  BINARY_SUBSCR    
             1128  STORE_FAST               'block'

 L. 350      1130  LOAD_FAST                'j'
             1132  LOAD_FAST                'uncoversize'
             1134  BINARY_MULTIPLY  
             1136  LOAD_FAST                'coversize'
             1138  LOAD_CONST               2
             1140  BINARY_FLOOR_DIVIDE
             1142  BINARY_ADD       
             1144  LOAD_FAST                'i'
             1146  LOAD_FAST                'uncoversize'
             1148  BINARY_MULTIPLY  
             1150  LOAD_FAST                'coversize'
             1152  LOAD_CONST               2
             1154  BINARY_FLOOR_DIVIDE
             1156  BINARY_ADD       
             1158  ROT_TWO          
             1160  STORE_FAST               'col_off'
             1162  STORE_FAST               'row_off'

 L. 351      1164  LOAD_FAST                'ds'
             1166  LOAD_ATTR                width
             1168  LOAD_FAST                'col_off'
             1170  BINARY_SUBTRACT  
             1172  LOAD_FAST                'ds'
             1174  LOAD_ATTR                height
             1176  LOAD_FAST                'row_off'
             1178  BINARY_SUBTRACT  
             1180  ROT_TWO          
             1182  STORE_FAST               'width'
             1184  STORE_FAST               'height'
         1186_1188  JUMP_FORWARD       1960  'to 1960'
           1190_0  COME_FROM          1072  '1072'
           1190_1  COME_FROM          1062  '1062'

 L. 353      1190  LOAD_FAST                'i'
             1192  LOAD_CONST               0
             1194  COMPARE_OP               ==
         1196_1198  POP_JUMP_IF_FALSE  1410  'to 1410'
             1200  LOAD_FAST                'j'
             1202  LOAD_CONST               0
             1204  COMPARE_OP               !=
         1206_1208  POP_JUMP_IF_FALSE  1410  'to 1410'

 L. 354      1210  LOAD_FAST                'j'
             1212  LOAD_FAST                'width_block'
             1214  COMPARE_OP               ==
         1216_1218  POP_JUMP_IF_FALSE  1316  'to 1316'

 L. 356      1220  LOAD_FAST                'block'
             1222  LOAD_CONST               None
             1224  LOAD_CONST               None
             1226  BUILD_SLICE_2         2 
             1228  LOAD_CONST               None
             1230  LOAD_FAST                'blocksize'
             1232  LOAD_FAST                'coversize'
             1234  LOAD_CONST               2
             1236  BINARY_FLOOR_DIVIDE
             1238  BINARY_SUBTRACT  
             1240  BUILD_SLICE_2         2 

 L. 357      1242  LOAD_FAST                'coversize'
             1244  LOAD_CONST               2
             1246  BINARY_FLOOR_DIVIDE
             1248  LOAD_FAST                'ds'
             1250  LOAD_ATTR                width
             1252  LOAD_FAST                'j'
             1254  LOAD_FAST                'uncoversize'
             1256  BINARY_MULTIPLY  
             1258  BINARY_SUBTRACT  
             1260  BUILD_SLICE_2         2 
             1262  BUILD_TUPLE_3         3 
             1264  BINARY_SUBSCR    
             1266  STORE_FAST               'block'

 L. 359      1268  LOAD_FAST                'j'
             1270  LOAD_FAST                'uncoversize'
             1272  BINARY_MULTIPLY  
             1274  LOAD_FAST                'coversize'
             1276  LOAD_CONST               2
             1278  BINARY_FLOOR_DIVIDE
             1280  BINARY_ADD       
             1282  LOAD_CONST               0
             1284  ROT_TWO          
             1286  STORE_FAST               'col_off'
             1288  STORE_FAST               'row_off'

 L. 360      1290  LOAD_FAST                'ds'
             1292  LOAD_ATTR                width
             1294  LOAD_FAST                'col_off'
             1296  BINARY_SUBTRACT  
             1298  LOAD_FAST                'uncoversize'
             1300  LOAD_FAST                'coversize'
             1302  LOAD_CONST               2
             1304  BINARY_FLOOR_DIVIDE
             1306  BINARY_ADD       
             1308  ROT_TWO          
             1310  STORE_FAST               'width'
             1312  STORE_FAST               'height'
             1314  JUMP_FORWARD       1960  'to 1960'
           1316_0  COME_FROM          1216  '1216'

 L. 363      1316  LOAD_FAST                'block'
             1318  LOAD_CONST               None
             1320  LOAD_CONST               None
             1322  BUILD_SLICE_2         2 
             1324  LOAD_CONST               None
             1326  LOAD_FAST                'blocksize'
             1328  LOAD_FAST                'coversize'
             1330  LOAD_CONST               2
             1332  BINARY_FLOOR_DIVIDE
             1334  BINARY_SUBTRACT  
             1336  BUILD_SLICE_2         2 

 L. 364      1338  LOAD_FAST                'coversize'
             1340  LOAD_CONST               2
             1342  BINARY_FLOOR_DIVIDE
             1344  LOAD_FAST                'blocksize'
             1346  LOAD_FAST                'coversize'
             1348  LOAD_CONST               2
             1350  BINARY_FLOOR_DIVIDE
             1352  BINARY_SUBTRACT  
             1354  BUILD_SLICE_2         2 
             1356  BUILD_TUPLE_3         3 
             1358  BINARY_SUBSCR    
             1360  STORE_FAST               'block'

 L. 366      1362  LOAD_FAST                'j'
             1364  LOAD_FAST                'uncoversize'
             1366  BINARY_MULTIPLY  
             1368  LOAD_FAST                'coversize'
             1370  LOAD_CONST               2
             1372  BINARY_FLOOR_DIVIDE
             1374  BINARY_ADD       
             1376  LOAD_FAST                'i'
             1378  LOAD_FAST                'uncoversize'
             1380  BINARY_MULTIPLY  
             1382  ROT_TWO          
             1384  STORE_FAST               'col_off'
             1386  STORE_FAST               'row_off'

 L. 367      1388  LOAD_FAST                'uncoversize'
             1390  LOAD_FAST                'uncoversize'
             1392  LOAD_FAST                'coversize'
             1394  LOAD_CONST               2
             1396  BINARY_FLOOR_DIVIDE
             1398  BINARY_ADD       
             1400  ROT_TWO          
             1402  STORE_FAST               'width'
             1404  STORE_FAST               'height'
         1406_1408  JUMP_FORWARD       1960  'to 1960'
           1410_0  COME_FROM          1206  '1206'
           1410_1  COME_FROM          1196  '1196'

 L. 369      1410  LOAD_FAST                'i'
             1412  LOAD_CONST               0
             1414  COMPARE_OP               !=
         1416_1418  POP_JUMP_IF_FALSE  1638  'to 1638'
             1420  LOAD_FAST                'j'
             1422  LOAD_CONST               0
             1424  COMPARE_OP               ==
         1426_1428  POP_JUMP_IF_FALSE  1638  'to 1638'

 L. 370      1430  LOAD_FAST                'i'
             1432  LOAD_FAST                'height_block'
             1434  COMPARE_OP               ==
         1436_1438  POP_JUMP_IF_FALSE  1536  'to 1536'

 L. 371      1440  LOAD_FAST                'block'
             1442  LOAD_CONST               None
             1444  LOAD_CONST               None
             1446  BUILD_SLICE_2         2 
             1448  LOAD_FAST                'coversize'
             1450  LOAD_CONST               2
             1452  BINARY_FLOOR_DIVIDE
             1454  LOAD_FAST                'ds'
             1456  LOAD_ATTR                height
             1458  LOAD_FAST                'i'
             1460  LOAD_FAST                'uncoversize'
             1462  BINARY_MULTIPLY  
             1464  BINARY_SUBTRACT  
             1466  BUILD_SLICE_2         2 
             1468  LOAD_CONST               None

 L. 372      1470  LOAD_FAST                'blocksize'
             1472  LOAD_FAST                'coversize'
             1474  LOAD_CONST               2
             1476  BINARY_FLOOR_DIVIDE
             1478  BINARY_SUBTRACT  
             1480  BUILD_SLICE_2         2 
             1482  BUILD_TUPLE_3         3 
             1484  BINARY_SUBSCR    
             1486  STORE_FAST               'block'

 L. 374      1488  LOAD_CONST               0
             1490  LOAD_FAST                'i'
             1492  LOAD_FAST                'uncoversize'
             1494  BINARY_MULTIPLY  
             1496  LOAD_FAST                'coversize'
             1498  LOAD_CONST               2
             1500  BINARY_FLOOR_DIVIDE
             1502  BINARY_ADD       
             1504  ROT_TWO          
             1506  STORE_FAST               'col_off'
             1508  STORE_FAST               'row_off'

 L. 375      1510  LOAD_FAST                'uncoversize'
             1512  LOAD_FAST                'coversize'
             1514  LOAD_CONST               2
             1516  BINARY_FLOOR_DIVIDE
             1518  BINARY_ADD       
             1520  LOAD_FAST                'ds'
             1522  LOAD_ATTR                height
             1524  LOAD_FAST                'row_off'
             1526  BINARY_SUBTRACT  
             1528  ROT_TWO          
             1530  STORE_FAST               'width'
             1532  STORE_FAST               'height'
             1534  JUMP_FORWARD       1960  'to 1960'
           1536_0  COME_FROM          1436  '1436'

 L. 378      1536  LOAD_FAST                'block'
             1538  LOAD_CONST               None
             1540  LOAD_CONST               None
             1542  BUILD_SLICE_2         2 
             1544  LOAD_GLOBAL              int
             1546  LOAD_FAST                'coversize'
             1548  LOAD_CONST               2
             1550  BINARY_FLOOR_DIVIDE
             1552  CALL_FUNCTION_1       1  '1 positional argument'
             1554  LOAD_GLOBAL              int
             1556  LOAD_FAST                'blocksize'
             1558  LOAD_FAST                'coversize'
             1560  LOAD_CONST               2
             1562  BINARY_FLOOR_DIVIDE
             1564  BINARY_SUBTRACT  
             1566  CALL_FUNCTION_1       1  '1 positional argument'
             1568  BUILD_SLICE_2         2 
             1570  LOAD_CONST               None

 L. 379      1572  LOAD_GLOBAL              int
             1574  LOAD_FAST                'blocksize'
             1576  LOAD_FAST                'coversize'
             1578  LOAD_CONST               2
             1580  BINARY_FLOOR_DIVIDE
             1582  BINARY_SUBTRACT  
             1584  CALL_FUNCTION_1       1  '1 positional argument'
             1586  BUILD_SLICE_2         2 
             1588  BUILD_TUPLE_3         3 
             1590  BINARY_SUBSCR    
             1592  STORE_FAST               'block'

 L. 381      1594  LOAD_CONST               0
             1596  LOAD_FAST                'i'
             1598  LOAD_FAST                'uncoversize'
             1600  BINARY_MULTIPLY  
             1602  LOAD_FAST                'coversize'
             1604  LOAD_CONST               2
             1606  BINARY_FLOOR_DIVIDE
             1608  BINARY_ADD       
             1610  ROT_TWO          
             1612  STORE_FAST               'col_off'
             1614  STORE_FAST               'row_off'

 L. 382      1616  LOAD_FAST                'uncoversize'
             1618  LOAD_FAST                'coversize'
             1620  LOAD_CONST               2
             1622  BINARY_FLOOR_DIVIDE
             1624  BINARY_ADD       
             1626  LOAD_FAST                'uncoversize'
             1628  ROT_TWO          
             1630  STORE_FAST               'width'
             1632  STORE_FAST               'height'
         1634_1636  JUMP_FORWARD       1960  'to 1960'
           1638_0  COME_FROM          1426  '1426'
           1638_1  COME_FROM          1416  '1416'

 L. 385      1638  LOAD_FAST                'i'
             1640  LOAD_FAST                'height_block'
             1642  COMPARE_OP               ==
         1644_1646  POP_JUMP_IF_FALSE  1752  'to 1752'

 L. 386      1648  LOAD_FAST                'block'
             1650  LOAD_CONST               None
             1652  LOAD_CONST               None
             1654  BUILD_SLICE_2         2 
             1656  LOAD_FAST                'coversize'
             1658  LOAD_CONST               2
             1660  BINARY_FLOOR_DIVIDE
             1662  LOAD_FAST                'ds'
             1664  LOAD_ATTR                height
             1666  LOAD_FAST                'i'
             1668  LOAD_FAST                'uncoversize'
             1670  BINARY_MULTIPLY  
             1672  BINARY_SUBTRACT  
             1674  BUILD_SLICE_2         2 

 L. 387      1676  LOAD_FAST                'coversize'
             1678  LOAD_CONST               2
             1680  BINARY_FLOOR_DIVIDE
             1682  LOAD_FAST                'blocksize'
             1684  LOAD_FAST                'coversize'
             1686  LOAD_CONST               2
             1688  BINARY_FLOOR_DIVIDE
             1690  BINARY_SUBTRACT  
             1692  BUILD_SLICE_2         2 
             1694  BUILD_TUPLE_3         3 
             1696  BINARY_SUBSCR    
             1698  STORE_FAST               'block'

 L. 389      1700  LOAD_FAST                'j'
             1702  LOAD_FAST                'uncoversize'
             1704  BINARY_MULTIPLY  
             1706  LOAD_FAST                'coversize'
             1708  LOAD_CONST               2
             1710  BINARY_FLOOR_DIVIDE
             1712  BINARY_ADD       
             1714  LOAD_FAST                'i'
             1716  LOAD_FAST                'uncoversize'
             1718  BINARY_MULTIPLY  
             1720  LOAD_FAST                'coversize'
             1722  LOAD_CONST               2
             1724  BINARY_FLOOR_DIVIDE
             1726  BINARY_ADD       
             1728  ROT_TWO          
             1730  STORE_FAST               'col_off'
             1732  STORE_FAST               'row_off'

 L. 390      1734  LOAD_FAST                'uncoversize'
             1736  LOAD_FAST                'ds'
             1738  LOAD_ATTR                height
             1740  LOAD_FAST                'row_off'
             1742  BINARY_SUBTRACT  
             1744  ROT_TWO          
             1746  STORE_FAST               'width'
             1748  STORE_FAST               'height'
             1750  JUMP_FORWARD       1960  'to 1960'
           1752_0  COME_FROM          1644  '1644'

 L. 392      1752  LOAD_FAST                'j'
             1754  LOAD_FAST                'width_block'
             1756  COMPARE_OP               ==
         1758_1760  POP_JUMP_IF_FALSE  1866  'to 1866'

 L. 393      1762  LOAD_FAST                'block'
             1764  LOAD_CONST               None
             1766  LOAD_CONST               None
             1768  BUILD_SLICE_2         2 
             1770  LOAD_FAST                'coversize'
             1772  LOAD_CONST               2
             1774  BINARY_FLOOR_DIVIDE
             1776  LOAD_FAST                'blocksize'
             1778  LOAD_FAST                'coversize'
             1780  LOAD_CONST               2
             1782  BINARY_FLOOR_DIVIDE
             1784  BINARY_SUBTRACT  
             1786  BUILD_SLICE_2         2 

 L. 394      1788  LOAD_FAST                'coversize'
             1790  LOAD_CONST               2
             1792  BINARY_FLOOR_DIVIDE
             1794  LOAD_FAST                'ds'
             1796  LOAD_ATTR                width
             1798  LOAD_FAST                'j'
             1800  LOAD_FAST                'uncoversize'
             1802  BINARY_MULTIPLY  
             1804  BINARY_SUBTRACT  
             1806  BUILD_SLICE_2         2 
             1808  BUILD_TUPLE_3         3 
             1810  BINARY_SUBSCR    
             1812  STORE_FAST               'block'

 L. 396      1814  LOAD_FAST                'j'
             1816  LOAD_FAST                'uncoversize'
             1818  BINARY_MULTIPLY  
             1820  LOAD_FAST                'coversize'
             1822  LOAD_CONST               2
             1824  BINARY_FLOOR_DIVIDE
             1826  BINARY_ADD       
             1828  LOAD_FAST                'i'
             1830  LOAD_FAST                'uncoversize'
             1832  BINARY_MULTIPLY  
             1834  LOAD_FAST                'coversize'
             1836  LOAD_CONST               2
             1838  BINARY_FLOOR_DIVIDE
             1840  BINARY_ADD       
             1842  ROT_TWO          
             1844  STORE_FAST               'col_off'
             1846  STORE_FAST               'row_off'

 L. 397      1848  LOAD_FAST                'ds'
             1850  LOAD_ATTR                width
             1852  LOAD_FAST                'col_off'
             1854  BINARY_SUBTRACT  
             1856  LOAD_FAST                'uncoversize'
           1858_0  COME_FROM          1534  '1534'
             1858  ROT_TWO          
             1860  STORE_FAST               'width'
             1862  STORE_FAST               'height'
             1864  JUMP_FORWARD       1960  'to 1960'
           1866_0  COME_FROM          1758  '1758'
           1866_1  COME_FROM          1314  '1314'

 L. 400      1866  LOAD_FAST                'block'
             1868  LOAD_CONST               None
             1870  LOAD_CONST               None
             1872  BUILD_SLICE_2         2 
             1874  LOAD_FAST                'coversize'
             1876  LOAD_CONST               2
             1878  BINARY_FLOOR_DIVIDE
             1880  LOAD_FAST                'blocksize'
             1882  LOAD_FAST                'coversize'
             1884  LOAD_CONST               2
             1886  BINARY_FLOOR_DIVIDE
             1888  BINARY_SUBTRACT  
             1890  BUILD_SLICE_2         2 

 L. 401      1892  LOAD_FAST                'coversize'
             1894  LOAD_CONST               2
             1896  BINARY_FLOOR_DIVIDE
             1898  LOAD_FAST                'blocksize'
             1900  LOAD_FAST                'coversize'
             1902  LOAD_CONST               2
             1904  BINARY_FLOOR_DIVIDE
             1906  BINARY_SUBTRACT  
             1908  BUILD_SLICE_2         2 
             1910  BUILD_TUPLE_3         3 
             1912  BINARY_SUBSCR    
             1914  STORE_FAST               'block'

 L. 403      1916  LOAD_FAST                'j'
             1918  LOAD_FAST                'uncoversize'
             1920  BINARY_MULTIPLY  
             1922  LOAD_FAST                'coversize'
             1924  LOAD_CONST               2
             1926  BINARY_FLOOR_DIVIDE
             1928  BINARY_ADD       
             1930  LOAD_FAST                'i'
             1932  LOAD_FAST                'uncoversize'
             1934  BINARY_MULTIPLY  
             1936  LOAD_FAST                'coversize'
             1938  LOAD_CONST               2
             1940  BINARY_FLOOR_DIVIDE
             1942  BINARY_ADD       
             1944  ROT_TWO          
             1946  STORE_FAST               'col_off'
             1948  STORE_FAST               'row_off'

 L. 404      1950  LOAD_FAST                'uncoversize'
             1952  LOAD_FAST                'uncoversize'
             1954  ROT_TWO          
             1956  STORE_FAST               'width'
             1958  STORE_FAST               'height'
           1960_0  COME_FROM          1864  '1864'
           1960_1  COME_FROM          1750  '1750'
           1960_2  COME_FROM          1634  '1634'
           1960_3  COME_FROM          1406  '1406'
           1960_4  COME_FROM          1186  '1186'
           1960_5  COME_FROM          1052  '1052'

 L. 406      1960  LOAD_FAST                'p'
             1962  LOAD_CONST               1
             1964  INPLACE_ADD      
             1966  STORE_FAST               'p'

 L. 407      1968  LOAD_FAST                'dst'
             1970  LOAD_ATTR                write
             1972  LOAD_FAST                'block'
             1974  LOAD_GLOBAL              Window
             1976  LOAD_FAST                'col_off'
             1978  LOAD_FAST                'row_off'
             1980  LOAD_FAST                'width'
             1982  LOAD_FAST                'height'
             1984  CALL_FUNCTION_4       4  '4 positional arguments'
             1986  LOAD_CONST               ('window',)
             1988  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1990  POP_TOP          

 L. 408      1992  LOAD_GLOBAL              view_bar
             1994  LOAD_FAST                'p'
             1996  LOAD_FAST                'height_block'
             1998  LOAD_CONST               1
             2000  BINARY_ADD       
             2002  LOAD_FAST                'width_block'
             2004  LOAD_CONST               1
             2006  BINARY_ADD       
             2008  BINARY_MULTIPLY  
             2010  CALL_FUNCTION_2       2  '2 positional arguments'
             2012  POP_TOP          
         2014_2016  JUMP_BACK           450  'to 450'
             2018  POP_BLOCK        
           2020_0  COME_FROM_LOOP      434  '434'
         2020_2022  JUMP_BACK           428  'to 428'
             2024  POP_BLOCK        
           2026_0  COME_FROM_LOOP      412  '412'

 L. 410      2026  LOAD_FAST                'dst'
             2028  LOAD_METHOD              close
             2030  CALL_METHOD_0         0  '0 positional arguments'
             2032  POP_TOP          

 L. 411      2034  LOAD_FAST                'self'
             2036  LOAD_METHOD              close_model
             2038  CALL_METHOD_0         0  '0 positional arguments'
             2040  POP_TOP          

 L. 412      2042  LOAD_FAST                'result_type'
             2044  LOAD_METHOD              strip
             2046  CALL_METHOD_0         0  '0 positional arguments'
             2048  LOAD_STR                 'grid'
             2050  COMPARE_OP               ==
         2052_2054  POP_JUMP_IF_FALSE  2176  'to 2176'

 L. 413      2056  LOAD_GLOBAL              get_output_datasource
             2058  LOAD_FAST                'out_ds'
             2060  CALL_FUNCTION_1       1  '1 positional argument'
             2062  STORE_FAST               'out_ds'

 L. 414      2064  LOAD_GLOBAL              import_tif
             2066  LOAD_FAST                'tmp_file'
             2068  LOAD_FAST                'out_ds'
             2070  LOAD_FAST                'dst_name'
             2072  LOAD_CONST               True
             2074  LOAD_CONST               ('output', 'out_dataset_name', 'is_import_as_grid')
             2076  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
             2078  STORE_FAST               'result'

 L. 415      2080  LOAD_GLOBAL              shutil
             2082  LOAD_METHOD              copyfile
             2084  LOAD_FAST                'tmp_file'

 L. 416      2086  LOAD_GLOBAL              os
             2088  LOAD_ATTR                path
             2090  LOAD_METHOD              join
             2092  LOAD_GLOBAL              os
             2094  LOAD_ATTR                path
             2096  LOAD_METHOD              dirname
             2098  LOAD_FAST                'out_ds'
             2100  LOAD_ATTR                connection_info
             2102  LOAD_ATTR                server
             2104  CALL_METHOD_1         1  '1 positional argument'
             2106  LOAD_FAST                'dst_name'
             2108  LOAD_STR                 '.tif'
             2110  BINARY_ADD       
             2112  CALL_METHOD_2         2  '2 positional arguments'
             2114  CALL_METHOD_2         2  '2 positional arguments'
             2116  POP_TOP          

 L. 417      2118  LOAD_GLOBAL              isinstance
             2120  LOAD_FAST                'result'
             2122  LOAD_GLOBAL              list
             2124  CALL_FUNCTION_2       2  '2 positional arguments'
         2126_2128  POP_JUMP_IF_FALSE  2152  'to 2152'
             2130  LOAD_GLOBAL              len
             2132  LOAD_FAST                'result'
             2134  CALL_FUNCTION_1       1  '1 positional argument'
             2136  LOAD_CONST               0
             2138  COMPARE_OP               >
         2140_2142  POP_JUMP_IF_FALSE  2152  'to 2152'
             2144  LOAD_FAST                'result'
             2146  LOAD_CONST               0
             2148  BINARY_SUBSCR    
             2150  JUMP_FORWARD       2154  'to 2154'
           2152_0  COME_FROM          2140  '2140'
           2152_1  COME_FROM          2126  '2126'
             2152  LOAD_FAST                'result'
           2154_0  COME_FROM          2150  '2150'
             2154  STORE_FAST               'result'

 L. 418      2156  LOAD_GLOBAL              os
             2158  LOAD_METHOD              remove
             2160  LOAD_FAST                'tmp_file'
             2162  CALL_METHOD_1         1  '1 positional argument'
             2164  POP_TOP          

 L. 419      2166  LOAD_FAST                'out_ds'
             2168  LOAD_METHOD              close
             2170  CALL_METHOD_0         0  '0 positional arguments'
             2172  POP_TOP          
             2174  JUMP_FORWARD       2354  'to 2354'
           2176_0  COME_FROM          2052  '2052'

 L. 420      2176  LOAD_FAST                'result_type'
             2178  LOAD_METHOD              strip
             2180  CALL_METHOD_0         0  '0 positional arguments'
             2182  LOAD_STR                 'region'
             2184  COMPARE_OP               ==
         2186_2188  POP_JUMP_IF_FALSE  2346  'to 2346'

 L. 421      2190  LOAD_GLOBAL              os
             2192  LOAD_ATTR                path
             2194  LOAD_METHOD              join
             2196  LOAD_GLOBAL              tempfile
             2198  LOAD_METHOD              mkdtemp
             2200  CALL_METHOD_0         0  '0 positional arguments'
             2202  LOAD_STR                 'tmp.udb'
             2204  CALL_METHOD_2         2  '2 positional arguments'
             2206  STORE_FAST               'tmp_udb_file'

 L. 422      2208  LOAD_GLOBAL              DatasourceConnectionInfo
             2210  LOAD_FAST                'tmp_udb_file'
             2212  LOAD_GLOBAL              EngineType
             2214  LOAD_ATTR                UDB
             2216  LOAD_CONST               ('server', 'engine_type')
             2218  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             2220  STORE_FAST               'tmp_dsc'

 L. 423      2222  LOAD_GLOBAL              Datasource
             2224  CALL_FUNCTION_0       0  '0 positional arguments'
             2226  LOAD_METHOD              create
             2228  LOAD_FAST                'tmp_dsc'
             2230  CALL_METHOD_1         1  '1 positional argument'
             2232  STORE_FAST               'tmp_ds'

 L. 424      2234  LOAD_GLOBAL              import_tif
             2236  LOAD_FAST                'tmp_file'
             2238  LOAD_FAST                'tmp_ds'
             2240  LOAD_STR                 'mask_tmp'
             2242  LOAD_CONST               True
             2244  LOAD_CONST               ('output', 'out_dataset_name', 'is_import_as_grid')
             2246  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
             2248  POP_TOP          

 L. 425      2250  LOAD_GLOBAL              os
             2252  LOAD_METHOD              remove
             2254  LOAD_FAST                'tmp_file'
             2256  CALL_METHOD_1         1  '1 positional argument'
             2258  POP_TOP          

 L. 427      2260  LOAD_GLOBAL              raster_to_vector
             2262  LOAD_FAST                'tmp_ds'
             2264  LOAD_STR                 'mask_tmp'
             2266  BINARY_SUBSCR    
             2268  LOAD_STR                 'class_type'
             2270  LOAD_GLOBAL              DatasetType
             2272  LOAD_ATTR                REGION

 L. 428      2274  LOAD_FAST                'self'
             2276  LOAD_ATTR                back_or_no_value

 L. 429      2278  LOAD_CONST               True
             2280  LOAD_FAST                'out_ds'
             2282  LOAD_FAST                'dst_name'
             2284  LOAD_CONST               ('out_dataset_type', 'back_or_no_value', 'is_thin_raster', 'out_data', 'out_dataset_name')
             2286  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
             2288  STORE_FAST               'result'

 L. 430      2290  LOAD_GLOBAL              isinstance
             2292  LOAD_FAST                'result'
             2294  LOAD_GLOBAL              list
             2296  CALL_FUNCTION_2       2  '2 positional arguments'
         2298_2300  POP_JUMP_IF_FALSE  2324  'to 2324'
             2302  LOAD_GLOBAL              len
             2304  LOAD_FAST                'result'
             2306  CALL_FUNCTION_1       1  '1 positional argument'
             2308  LOAD_CONST               0
             2310  COMPARE_OP               >
         2312_2314  POP_JUMP_IF_FALSE  2324  'to 2324'
             2316  LOAD_FAST                'result'
             2318  LOAD_CONST               0
             2320  BINARY_SUBSCR    
             2322  JUMP_FORWARD       2326  'to 2326'
           2324_0  COME_FROM          2312  '2312'
           2324_1  COME_FROM          2298  '2298'
             2324  LOAD_FAST                'result'
           2326_0  COME_FROM          2322  '2322'
             2326  STORE_FAST               'result'

 L. 431      2328  LOAD_FAST                'tmp_ds'
             2330  LOAD_METHOD              delete_all
             2332  CALL_METHOD_0         0  '0 positional arguments'
             2334  POP_TOP          

 L. 432      2336  LOAD_FAST                'tmp_ds'
             2338  LOAD_METHOD              close
             2340  CALL_METHOD_0         0  '0 positional arguments'
             2342  POP_TOP          
             2344  JUMP_FORWARD       2354  'to 2354'
           2346_0  COME_FROM          2186  '2186'

 L. 434      2346  LOAD_GLOBAL              Exception
             2348  LOAD_STR                 'result_type error'
             2350  CALL_FUNCTION_1       1  '1 positional argument'
             2352  RAISE_VARARGS_1       1  'exception instance'
           2354_0  COME_FROM          2344  '2344'
           2354_1  COME_FROM          2174  '2174'

 L. 436      2354  LOAD_FAST                'result'
             2356  RETURN_VALUE     
           2358_0  COME_FROM_WITH       90  '90'
             2358  WITH_CLEANUP_START
             2360  WITH_CLEANUP_FINISH
             2362  END_FINALLY      

Parse error at or near `COME_FROM' instruction at offset 1858_0

    def __predict(self, input_image):
        """
        输入numpy的影像数据，进行预测

        :param input_image: numpy输入影像
        :type input_image: ndarray
        :return:
        """
        if self.is_stretch:
            input_image = stretch_n(input_image)
        else:
            predict_merge = np.zeros((input_image.shape[0], input_image.shape[1], self.output_msk_num), dtype=(np.float))
            seg_size = self.seg_size
            half_oversize = self.half_oversize
            if self.band_order == 'last':
                predict_tile = self._UnetEstimation__make_predict_tile(input_image, seg_size=seg_size, half_oversize=half_oversize, band_order='last')
                out_shape = (predict_tile.shape[0], self.out_width_height[0], self.out_width_height[1], self.output_msk_num)
                predict_y = self._predict_tile_local(predict_tile, out_shape)
                self.close_model()
                predict_merge = self._UnetEstimation__make_predict_merage(predict_y, predict_merge, seg_size=seg_size, half_oversize=half_oversize,
                  band_order='last')
            else:
                predict_tile = self._UnetEstimation__make_predict_tile(input_image, seg_size=seg_size, half_oversize=half_oversize, band_order='first')
                out_shape = (predict_tile.shape[0], self.output_msk_num, self.out_width_height[0], self.out_width_height[1])
                predict_y = self._predict_tile_local(predict_tile, out_shape)
                self.close_model()
            predict_merge = self._UnetEstimation__make_predict_merage(predict_y, predict_merge, seg_size=seg_size, half_oversize=half_oversize,
              band_order='first')
        return predict_merge

    def __predict_with_preload(self, input_image):
        """
        输入numpy的影像数据，进行预测

        :param input_image: numpy输入影像
        :type input_image: ndarray
        :return:
        """
        if self.is_stretch:
            input_image = stretch_n(input_image)
        else:
            predict_merge = np.zeros((input_image.shape[0], input_image.shape[1], self.output_msk_num), dtype=(np.float))
            seg_size = self.seg_size
            half_oversize = self.half_oversize
            if self.band_order == 'last':
                predict_tile = self._UnetEstimation__make_predict_tile(input_image, seg_size=seg_size, half_oversize=half_oversize, band_order='last')
                out_shape = (predict_tile.shape[0], self.out_width_height[0], self.out_width_height[1], self.output_msk_num)
                predict_y = self._predict_tile_local(predict_tile, out_shape)
                predict_merge = self._UnetEstimation__make_predict_merage(predict_y, predict_merge, seg_size=seg_size, half_oversize=half_oversize,
                  band_order='last')
            else:
                predict_tile = self._UnetEstimation__make_predict_tile(input_image, seg_size=seg_size, half_oversize=half_oversize, band_order='first')
            out_shape = (
             predict_tile.shape[0], self.output_msk_num, self.out_width_height[0], self.out_width_height[1])
            predict_y = self._predict_tile_local(predict_tile, out_shape)
            predict_merge = self._UnetEstimation__make_predict_merage(predict_y, predict_merge, seg_size=seg_size, half_oversize=half_oversize,
              band_order='first')
        return predict_merge

    def __make_predict_tile(self, image, seg_size, half_oversize, band_order='last'):
        """
        to divided the image to be predicted a specified size

        :param image:   input predicted image
        :param seg_size: specified divide size
        :param oversize: each patch overlapping size
        :return: divided image list
        """
        if band_order == 'first':
            image = np.transpose(image, (1, 2, 0))
        x = []
        oversize = 2 * half_oversize
        count_x = int((image.shape[0] - oversize) / (seg_size - oversize)) + 1
        count_y = int((image.shape[1] - oversize) / (seg_size - oversize)) + 1
        realsize = seg_size - oversize
        if count_x == 1 and count_y == 1:
            im = np.zeros((seg_size, seg_size, image.shape[2]), dtype=(np.float))
            im[0:image.shape[0], 0:image.shape[1], :] = image
            x.append(im)
        else:
            if count_x == 1 and count_y is not 1:
                im = np.zeros((seg_size, seg_size, image.shape[2]), dtype=(np.float))
                for i in range(0, count_y):
                    if i == 0:
                        im[0:image.shape[0], :] = image[:, 0:seg_size, :]
                        x.append(im)
                    elif i == count_y - 1:
                        im[0:image.shape[0], 0:image.shape[1] - realsize * (count_y - 1)] = image[:,
                         realsize * i:image.shape[1], :]
                        x.append(im)
                    else:
                        im[0:image.shape[0], :] = image[:, realsize * i:realsize * i + seg_size, :]
                        x.append(im)

            else:
                if count_y == 1 and count_x is not 1:
                    im = np.zeros((seg_size, seg_size, image.shape[2]), dtype=(np.float))
                    for i in range(0, count_x):
                        if i == 0:
                            im[:, 0:image.shape[1]] = image[0:seg_size, :, :]
                            x.append(im)
                        elif i == count_x - 1:
                            im[0:image.shape[0] - realsize * (count_x - 1), 0:image.shape[1]] = image[
                             realsize * i:image.shape[0], :, :]
                            x.append(im)
                        else:
                            im[:, 0:image.shape[1]] = image[realsize * i:realsize * i + seg_size, :, :]
                            x.append(im)

                else:
                    for i in range(0, count_x):
                        for j in range(0, count_y):
                            im = np.zeros((seg_size, seg_size, image.shape[2]), dtype=(np.float))
                            if i == 0:
                                if j == 0:
                                    im = image[0:seg_size, 0:seg_size]
                                    x.append(im)
                            if i == 0:
                                if j is not 0:
                                    if j == count_y - 1:
                                        im[:, 0:image.shape[1] - realsize * (count_y - 1)] = image[0:seg_size,
                                         realsize * j:image.shape[1], :]
                                        x.append(im)
                                    else:
                                        im = image[0:seg_size, realsize * j:realsize * j + seg_size, :]
                                        x.append(im)
                            if j == 0:
                                if i is not 0:
                                    if i == count_x - 1:
                                        im[0:image.shape[0] - realsize * (count_x - 1), :] = image[realsize * i:image.shape[0],
                                         0:seg_size, :]
                                        x.append(im)
                                    else:
                                        im = image[realsize * i:realsize * i + seg_size, 0:seg_size, :]
                                        x.append(im)
                            if i == count_x - 1:
                                if j == count_y - 1:
                                    im[0:image.shape[0] - realsize * (count_x - 1), 0:image.shape[1] - realsize * (count_y - 1)] = image[realsize * i:image.shape[0],
                                     realsize * j:image.shape[1], :]
                                    x.append(im)
                            if i == count_x - 1 and j is not count_y - 1:
                                im[0:image.shape[0] - realsize * (count_x - 1), :] = image[realsize * i:image.shape[0],
                                 realsize * j:realsize * j + seg_size, :]
                                x.append(im)
                            elif i is not count_x - 1 and j == count_y - 1:
                                im[:, 0:image.shape[1] - realsize * (count_y - 1)] = image[
                                 realsize * i:realsize * i + seg_size,
                                 realsize * j:image.shape[1], :]
                                x.append(im)
                            else:
                                im = image[realsize * i:realsize * i + seg_size, realsize * j:realsize * j + seg_size, :]
                                x.append(im)

        if band_order == 'first':
            x = np.transpose(x, (0, 3, 1, 2))
        return np.array(x)

    def __make_predict_merage(self, predict_y, predict_merge, seg_size, half_oversize, band_order='last'):
        """
        merage the predicted tiles, only channels last
        maybe have a bug ,the axis x maybe have a data lose,but the reason isn't found

        :param predict_y: predict tiles
        :param predict_merge: merage
        :param seg_size: divided size
        :param half_oversize: half overlap size
        :return: meraged image
        """
        if band_order == 'first':
            predict_y = np.transpose(predict_y, (0, 2, 3, 1))
        oversize = 2 * half_oversize
        count_x = int((predict_merge.shape[0] - oversize) / (seg_size - oversize)) + 1
        count_y = int((predict_merge.shape[1] - oversize) / (seg_size - oversize)) + 1
        realsize = seg_size - oversize
        if count_x == 1 and count_y == 1:
            predict_merge = predict_y[0][0:predict_merge.shape[0], 0:predict_merge.shape[1]]
        else:
            if count_x == 1 and count_y is not 1:
                for i in range(0, count_y):
                    if i == 0:
                        predict_merge[:, 0:seg_size - half_oversize, :] = predict_y[i][0:predict_merge.shape[0],
                         0:seg_size - half_oversize]
                    elif i == count_y - 1:
                        predict_merge[:, realsize * i + half_oversize:, :] = predict_y[i][0:predict_merge.shape[0],
                         half_oversize:predict_merge.shape[1] - realsize * (count_y - 1)]
                    else:
                        predict_merge[:, realsize * i + half_oversize:realsize * i + seg_size - half_oversize, :] = predict_y[i][0:predict_merge.shape[0], half_oversize:seg_size - half_oversize]

            else:
                if count_y == 1 and count_x is not 1:
                    for i in range(0, count_x):
                        if i == 0:
                            predict_merge[0:seg_size - half_oversize, :, :] = predict_y[i][0:seg_size - half_oversize,
                             0:predict_merge.shape[1]]
                        elif i == count_x - 1:
                            predict_merge[realsize * i + half_oversize:, :, :] = predict_y[i][
                             half_oversize:predict_merge.shape[0] - realsize * (count_y - 1),
                             0:predict_merge.shape[1]]
                        else:
                            predict_merge[realsize * i + half_oversize:realsize * i + seg_size - half_oversize, :, :] = predict_y[i][half_oversize:seg_size - half_oversize, 0:predict_merge.shape[1]]

                else:
                    for i in range(0, count_x):
                        for j in range(0, count_y):
                            if i == 0 and j == 0:
                                predict_merge[0:seg_size - half_oversize, 0:seg_size - half_oversize] = predict_y[(i * count_y + j)][
                                 0:seg_size - half_oversize,
                                 0:seg_size - half_oversize]
                            elif i == 0:
                                if j is not 0:
                                    if j == count_y - 1:
                                        predict_merge[0:seg_size - half_oversize, realsize * j + half_oversize:, :] = predict_y[(i * count_y + j)][
                                         0:seg_size - half_oversize,
                                         half_oversize:predict_merge.shape[1] - realsize * (count_y - 1)]
                                else:
                                    predict_merge[0:seg_size - half_oversize, realsize * j + half_oversize:realsize * j + seg_size - half_oversize, :] = predict_y[(i * count_y + j)][
                                     0:seg_size - half_oversize,
                                     half_oversize:seg_size - half_oversize]
                            elif j == 0:
                                if i is not 0:
                                    if i == count_x - 1:
                                        predict_merge[realsize * i + half_oversize:, 0:seg_size - half_oversize, :] = predict_y[(i * count_y + j)][
                                         half_oversize:predict_merge.shape[0] - realsize * (count_x - 1),
                                         0:seg_size - half_oversize]
                                else:
                                    predict_merge[realsize * i + half_oversize:realsize * i + seg_size - half_oversize, 0:seg_size - half_oversize, :] = predict_y[(i * count_y + j)][
                                     half_oversize:seg_size - half_oversize,
                                     0:seg_size - half_oversize, :]
                            elif i == count_x - 1 and j == count_y - 1:
                                predict_merge[realsize * i + half_oversize:, realsize * j + half_oversize:, :] = predict_y[(i * count_y + j)][
                                 half_oversize:predict_merge.shape[0] - realsize * i,
                                 half_oversize:predict_merge.shape[1] - realsize * j]
                            elif i == count_x - 1 and j is not count_y - 1:
                                predict_merge[realsize * i + half_oversize:, realsize * j + half_oversize:realsize * j + seg_size - half_oversize, :] = predict_y[(i * count_y + j)][
                                 half_oversize:predict_merge.shape[0] - realsize * i,
                                 half_oversize:seg_size - half_oversize, :]
                            elif i is not count_x - 1 and j == count_y - 1:
                                predict_merge[realsize * i + half_oversize:realsize * i + seg_size - half_oversize, realsize * j + half_oversize:, :] = predict_y[(i * count_y + j)][
                                 half_oversize:seg_size - half_oversize,
                                 half_oversize:predict_merge.shape[1] - realsize * j, :]
                            else:
                                predict_merge[realsize * i + half_oversize:realsize * i + seg_size - half_oversize, realsize * j + half_oversize:realsize * j + seg_size - half_oversize, :] = predict_y[(i * count_y + j)][
                                 half_oversize:seg_size - half_oversize,
                                 half_oversize:seg_size - half_oversize, :]

        if band_order == 'first':
            predict_merge = np.transpose(predict_merge, (1, 2, 0))
        return predict_merge

    def _predict_tile_local(self, predict_tile, out_shape):
        """
        利用给定的模型使用tensorflow推断得到模型预测结果
        :param predict_tile:  ndarray 需要预测的数组片 形状为 （tile_nums,:） 即第一列为图片的数量
        :param out_shape: tuple 输出结果的形状  如（100,320,320,1）
        :return:  ndarray 返回预测的结果
        """
        x_tensor_name = self.signature['predict'].inputs['images'].name
        y_tensor_name = self.signature['predict'].outputs['scores'].name
        x = self.sess.graph.get_tensor_by_name(x_tensor_name)
        y = self.sess.graph.get_tensor_by_name(y_tensor_name)
        self.sess.graph.finalize()
        batch_size = 1
        total_batch = int(predict_tile.shape[0] / batch_size)
        for i in range(total_batch):
            out = self.sess.run(y, feed_dict={x: predict_tile[i * batch_size:(i + 1) * batch_size, :]})
            if i == 0:
                y_all = out
            else:
                y_all = np.concatenate((y_all, out), 0)

        y_out = np.expand_dims(y_all, axis=0)
        y_out.resize(out_shape)
        return y_out

    def load_model(self, model_path):
        self.model_path = model_path
        self.sess = tf.Session()
        self.meta_graph_def = tf.saved_model.loader.load(self.sess, ['serve'], model_path)
        self.signature = self.meta_graph_def.signature_def
        self.sess.graph.finalize()

    def close_model(self):
        """
        关闭模型
        :return:
        """
        self.sess.close()
        tf.reset_default_graph()


class VggUnetPlusModel:

    def __init__(self, config, width, height, depth, classes):
        self.build_model(width, height, depth, classes)
        self.config = config

    def build_model(self, width, height, depth, classes):
        self.dropout_rate = 0.5
        self.act = 'relu'
        self.model = self.get_unet_with_inputbn(width, height, depth, classes)

    def keras_bn(self, x, bn_axis):
        if bn_axis == 3:
            axis = [
             -3, -2]
        else:
            if bn_axis == 1:
                axis = [
                 -2, -1]
        x_max = tf.contrib.distributions.percentile(x, 98, axis=axis, keep_dims=True)
        x_min = tf.contrib.distributions.percentile(x, 2, axis=axis, keep_dims=True)
        return tf.divide(tf.subtract(x, x_min), tf.add(tf.subtract(x_max, x_min), 1e-10))

    def get_unet_with_inputbn(self, img_rows, img_cols, num_channels, num_mask_channels, bn_axis=3, deep_supervision=False):
        if bn_axis == 3:
            K.set_image_data_format('channels_last')
            inputs = Input((img_rows, img_cols, num_channels))
        else:
            if bn_axis == 1:
                K.set_image_data_format('channels_first')
                inputs = Input((num_channels, img_rows, img_cols))
            else:
                bn1 = Lambda((self.keras_bn), arguments={'bn_axis': bn_axis})(inputs)
                nb_filter = [32, 64, 128, 256, 512]
                conv1_1 = self._standard_unit(bn1, stage='11', nb_filter=(nb_filter[0]))
                pool1 = MaxPooling2D((2, 2), strides=(2, 2), name='pool1')(conv1_1)
                conv2_1 = self._standard_unit(pool1, stage='21', nb_filter=(nb_filter[1]))
                pool2 = MaxPooling2D((2, 2), strides=(2, 2), name='pool2')(conv2_1)
                up1_2 = Conv2DTranspose((nb_filter[0]), (2, 2), strides=(2, 2), name='up12', padding='same')(conv2_1)
                conv1_2 = concatenate([up1_2, conv1_1], name='merge12', axis=bn_axis)
                conv1_2 = self._standard_unit(conv1_2, stage='12', nb_filter=(nb_filter[0]))
                conv3_1 = self._standard_unit(pool2, stage='31', nb_filter=(nb_filter[2]))
                pool3 = MaxPooling2D((2, 2), strides=(2, 2), name='pool3')(conv3_1)
                up2_2 = Conv2DTranspose((nb_filter[1]), (2, 2), strides=(2, 2), name='up22', padding='same')(conv3_1)
                conv2_2 = concatenate([up2_2, conv2_1], name='merge22', axis=bn_axis)
                conv2_2 = self._standard_unit(conv2_2, stage='22', nb_filter=(nb_filter[1]))
                up1_3 = Conv2DTranspose((nb_filter[0]), (2, 2), strides=(2, 2), name='up13', padding='same')(conv2_2)
                conv1_3 = concatenate([up1_3, conv1_1, conv1_2], name='merge13', axis=bn_axis)
                conv1_3 = self._standard_unit(conv1_3, stage='13', nb_filter=(nb_filter[0]))
                conv4_1 = self._standard_unit(pool3, stage='41', nb_filter=(nb_filter[3]))
                pool4 = MaxPooling2D((2, 2), strides=(2, 2), name='pool4')(conv4_1)
                up3_2 = Conv2DTranspose((nb_filter[2]), (2, 2), strides=(2, 2), name='up32', padding='same')(conv4_1)
                conv3_2 = concatenate([up3_2, conv3_1], name='merge32', axis=bn_axis)
                conv3_2 = self._standard_unit(conv3_2, stage='32', nb_filter=(nb_filter[2]))
                up2_3 = Conv2DTranspose((nb_filter[1]), (2, 2), strides=(2, 2), name='up23', padding='same')(conv3_2)
                conv2_3 = concatenate([up2_3, conv2_1, conv2_2], name='merge23', axis=bn_axis)
                conv2_3 = self._standard_unit(conv2_3, stage='23', nb_filter=(nb_filter[1]))
                up1_4 = Conv2DTranspose((nb_filter[0]), (2, 2), strides=(2, 2), name='up14', padding='same')(conv2_3)
                conv1_4 = concatenate([up1_4, conv1_1, conv1_2, conv1_3], name='merge14', axis=bn_axis)
                conv1_4 = self._standard_unit(conv1_4, stage='14', nb_filter=(nb_filter[0]))
                conv5_1 = self._standard_unit(pool4, stage='51', nb_filter=(nb_filter[4]))
                up4_2 = Conv2DTranspose((nb_filter[3]), (2, 2), strides=(2, 2), name='up42', padding='same')(conv5_1)
                conv4_2 = concatenate([up4_2, conv4_1], name='merge42', axis=bn_axis)
                conv4_2 = self._standard_unit(conv4_2, stage='42', nb_filter=(nb_filter[3]))
                up3_3 = Conv2DTranspose((nb_filter[2]), (2, 2), strides=(2, 2), name='up33', padding='same')(conv4_2)
                conv3_3 = concatenate([up3_3, conv3_1, conv3_2], name='merge33', axis=bn_axis)
                conv3_3 = self._standard_unit(conv3_3, stage='33', nb_filter=(nb_filter[2]))
                up2_4 = Conv2DTranspose((nb_filter[1]), (2, 2), strides=(2, 2), name='up24', padding='same')(conv3_3)
                conv2_4 = concatenate([up2_4, conv2_1, conv2_2, conv2_3], name='merge24', axis=bn_axis)
                conv2_4 = self._standard_unit(conv2_4, stage='24', nb_filter=(nb_filter[1]))
                up1_5 = Conv2DTranspose((nb_filter[0]), (2, 2), strides=(2, 2), name='up15', padding='same')(conv2_4)
                conv1_5 = concatenate([up1_5, conv1_1, conv1_2, conv1_3, conv1_4], name='merge15', axis=bn_axis)
                conv1_5 = self._standard_unit(conv1_5, stage='15', nb_filter=(nb_filter[0]))
                nestnet_output_1 = Conv2D(num_mask_channels, (1, 1), activation='sigmoid', name='output_1', kernel_initializer='he_normal',
                  padding='same',
                  kernel_regularizer=(l2(0.0001)))(conv1_2)
                nestnet_output_2 = Conv2D(num_mask_channels, (1, 1), activation='sigmoid', name='output_2', kernel_initializer='he_normal',
                  padding='same',
                  kernel_regularizer=(l2(0.0001)))(conv1_3)
                nestnet_output_3 = Conv2D(num_mask_channels, (1, 1), activation='sigmoid', name='output_3', kernel_initializer='he_normal',
                  padding='same',
                  kernel_regularizer=(l2(0.0001)))(conv1_4)
                nestnet_output_4 = Conv2D(num_mask_channels, (1, 1), activation='sigmoid', name='output_4', kernel_initializer='he_normal',
                  padding='same',
                  kernel_regularizer=(l2(0.0001)))(conv1_5)
                if deep_supervision:
                    model = Model(inputs=inputs, outputs=[nestnet_output_1,
                     nestnet_output_2,
                     nestnet_output_3,
                     nestnet_output_4])
                else:
                    model = Model(inputs=inputs, outputs=nestnet_output_4)
            return model

    def _standard_unit(self, input_tensor, stage, nb_filter, kernel_size=3):
        x = Conv2D(nb_filter, (kernel_size, kernel_size), activation=(self.act), name=('conv' + stage + '_1'), kernel_initializer='he_normal',
          padding='same',
          kernel_regularizer=(l2(0.0001)))(input_tensor)
        x = Dropout((self.dropout_rate), name=('dp' + stage + '_1'))(x)
        x = Conv2D(nb_filter, (kernel_size, kernel_size), activation=(self.act), name=('conv' + stage + '_2'), kernel_initializer='he_normal',
          padding='same',
          kernel_regularizer=(l2(0.0001)))(x)
        x = Dropout((self.dropout_rate), name=('dp' + stage + '_2'))(x)
        return x

    @staticmethod
    def mean_iou(y_true, y_pred):
        prec = []
        for t in np.arange(0.5, 1.0, 0.05):
            y_pred_ = tf.to_int32(y_pred > t)
            score, up_opt = tf.metrics.mean_iou(y_true, y_pred_, 2)
            K.get_session().run(tf.local_variables_initializer())
            with tf.control_dependencies([up_opt]):
                score = tf.identity(score)
            prec.append(score)

        return K.mean((K.stack(prec)), axis=0)

    @staticmethod
    def dice_coef(y_true, y_pred):
        smooth = 1e-10
        y_true_f = K.flatten(y_true)
        y_pred_f = K.flatten(y_pred)
        intersection = K.sum(y_true_f * y_pred_f)
        return (2.0 * intersection + smooth) / (K.sum(y_true_f) + K.sum(y_pred_f) + smooth)

    @staticmethod
    def bce_dice_loss(y_true, y_pred):
        return 0.5 * binary_crossentropy(y_true, y_pred) + 0.5 * (1.0 - VggUnetPlusModel.dice_coef(y_true, y_pred))


class UnetTrainer(Trainer):

    def __init__(self):
        super().__init__()
        self.callbacks = []
        self.loss = []
        self.acc = []
        self.val_loss = []
        self.val_acc = []
        self.model_architecture = 'unet'

    def train(self, train_data_path, config, epoch=1, batch_size=1, lr=0.001, output_model_path='./', output_model_name='unet', log_path=None, backbone_name='resnext50', backbone_weight_path=None, reload_model=False, pretrained_model_path=None):
        K.clear_session()
        self.config = config
        self.train_data_path = train_data_path
        self.data_config = get_config_from_yaml(os.path.join(self.train_data_path, os.path.basename(self.train_data_path) + '.sda'))
        self.data_type = self.data_config.dataset.data_type
        if not self.data_type in ('multi_classification', 'binary_classifition'):
            raise AssertionError('data_type should be multi_classification or binary_classifition ')
        else:
            self.class_type = self.data_config.dataset.class_type
            self.tile_size = self.data_config.dataset.tile_size
            pixel_counts = np.array([c.pixel_count for c in self.class_type])
            self.class_weight = list(pixel_counts.sum(dtype=(np.float64)) / pixel_counts.shape[0] / (pixel_counts + 1.0))
            if self.data_type.strip() == 'multi_classification':
                self.output_bands = len(self.class_type)
            else:
                if self.data_type.strip() == 'binary_classifition':
                    self.output_bands = 1
                else:
                    log_error('data_type should be multi_classification or binary_classifition')
                    raise Exception('data_type should be multi_classification or binary_classifition')
        self.model_type = self.data_type
        self.input_bands = self.data_config.dataset.x_bandnum
        assert self.input_bands >= 1, '输入波段数应大于等于1'
        assert self.output_bands >= 1, '输出波段数应大于等于1'
        self.backbone_name = backbone_name
        if self.backbone_name is None or self.backbone_name.strip() == '':
            self.backbone_name = self.config.model.backbone_name
            log_warning('backbone_name 为空,将使用默认 backbone_name : {}'.format(self.backbone_name))
        self.config = config
        self.epoch = epoch
        self.batch_size = batch_size
        self.lr = lr
        self.output_model_path = output_model_path
        self.output_model_name = output_model_name
        self.backbone_weight_path = backbone_weight_path
        self.pretrained_model_path = pretrained_model_path
        self.log_path = log_path
        self.reload_model = reload_model
        self.init_callbacks(log_path)
        self.config.trainer.num_epochs = epoch
        self.config.trainer.batch_size = batch_size
        self.config.trainer.learning_rate = lr
        if self.pretrained_model_path is not None:
            self.model = build_model((self.tile_size), (self.tile_size), (self.input_bands), (self.output_bands), backbone_name=(self.backbone_name),
              encoder_weights=None,
              net_type='unet')
            checkpoint = find_last(self.pretrained_model_path, self.config.application.name)
            if checkpoint and os.path.exists(checkpoint):
                log_info('从 {} 下加载预训练模型'.format(checkpoint))
                self.model.load_weights(checkpoint)
            else:
                log_error('{} 中没有预训练模型'.format(self.pretrained_model_path))
        else:
            if self.backbone_weight_path is not None:
                if os.path.isfile(self.backbone_weight_path) and os.path.exists(self.backbone_weight_path):
                    self.model = build_model((self.tile_size), (self.tile_size), (self.input_bands), (self.output_bands), backbone_name=(self.backbone_name),
                      encoder_weights=None,
                      net_type='unet')
                    log_info('从 {} 下加载backbone模型'.format(self.backbone_weight_path))
                    self.model.load_weights((self.backbone_weight_path), by_name=True, skip_mismatch=True)
                else:
                    self.model = build_model((self.tile_size), (self.tile_size), (self.input_bands), (self.output_bands), backbone_name=(self.backbone_name),
                      encoder_weights='imagenet',
                      net_type='unet')
            elif self.output_bands == 1:
                self.model.compile(loss=bce_dice_loss, optimizer=Adam(lr=(self.lr)),
                  metrics=[
                 'acc', dice_coef])
            else:
                self.class_index = [i for i in range(len(self.class_type))]
                loss = categorical_crossentropy
                self.model.compile(loss=loss, optimizer=Adam(lr=(self.lr)),
                  metrics=[
                 'acc', IOUScore(threshold=0.5, class_indexes=(self.class_index))])
            if self.config.trainer.num_epochs > 0:
                try:
                    import psutil
                    free_memory = psutil.virtual_memory().total
                except Exception as e:
                    try:
                        free_memory = 4294967296
                    finally:
                        e = None
                        del e

                train_num, val_num, train_val_num = self._init_data()
                train_path = os.path.join(self.train_data_path, 'csv_path', 'train.csv')
                val_path = os.path.join(self.train_data_path, 'csv_path', 'val.csv')
                image_memory = train_val_num * (self.input_bands + self.output_bands) * self.tile_size ** 2
                if image_memory * 2.0 < free_memory:
                    x, y = self._get_data_from_csv(train_path, False, image_size=(self.tile_size))
                    history = self.model.fit(x=x,
                      y=y,
                      validation_data=self._get_data_from_csv(val_path, False, image_size=(self.tile_size)),
                      epochs=(self.config.trainer.num_epochs),
                      verbose=(self.config.trainer.verbose_training),
                      batch_size=(self.config.trainer.batch_size),
                      callbacks=(self.callbacks))
                else:
                    history = self.model.fit_generator((self._get_data_from_csv(train_path, False, image_size=(self.tile_size), generate=True, batch_size=(self.config.trainer.batch_size))()),
                      steps_per_epoch=(int(train_val_num / self.config.trainer.batch_size)),
                      epochs=(self.config.trainer.num_epochs),
                      validation_data=(self._get_data_from_csv(val_path, False, image_size=(self.tile_size), generate=True, batch_size=(self.config.trainer.batch_size))()),
                      validation_steps=(int(val_num / self.config.trainer.batch_size)),
                      verbose=(self.config.trainer.verbose_training),
                      callbacks=(self.callbacks))
                self.loss.extend(history.history['loss'])
                self.acc.extend(history.history['acc'])
                self.val_loss.extend(history.history['val_loss'])
                self.val_acc.extend(history.history['val_acc'])
                checkpoint = find_last(self.log_path, self.config.application.name)
            else:
                checkpoint = find_last((self.pretrained_model_path), (self.config.application.name), best=False)
            K.clear_session()
            K.set_learning_phase(0)
            export_model = build_model((self.tile_size), (self.tile_size), (self.input_bands), (self.output_bands), backbone_name=(self.backbone_name),
              encoder_weights=None,
              net_type='unet')
            export_model.load_weights(checkpoint)
            log_info('export model load from {}'.format(checkpoint))
            self._save_tfserving_model(export_model, os.path.join(output_model_path, output_model_name))

    def _init_data(self):
        return split_train_val_withdirs([os.path.join(self.train_data_path, 'Images')], [
         os.path.join(self.train_data_path, 'Masks')],
          (os.path.join(self.train_data_path, 'csv_path')),
          x_ext=(self.data_config.dataset.x_ext),
          y_ext=(self.data_config.dataset.y_ext),
          val_scale=(self.config.trainer.validation_split))

    def _get_data_from_csv(self, data_path, is_aug=False, image_size=None, generate=False, batch_size=None):
        if self.output_bands > 1:
            if data_path.endswith('.csv'):
                if generate:
                    return get_image_from_csv(data_path, is_aug,
                      input_bands=(self.input_bands),
                      output_bands=(self.output_bands),
                      image_size=image_size,
                      generate=generate,
                      batch_size=batch_size)
                return get_image_from_csv(data_path, is_aug,
                  input_bands=(self.input_bands),
                  output_bands=(self.output_bands),
                  image_size=image_size)
            else:
                raise Exception('Data load error,You should input a *.csv file')
        elif data_path.endswith('.csv'):
            if generate:
                return get_image_from_csv(data_path, is_aug,
                  input_bands=(self.input_bands),
                  output_bands=(self.output_bands),
                  image_size=image_size,
                  generate=generate,
                  batch_size=batch_size)
            return get_image_from_csv(data_path, is_aug,
              input_bands=(self.input_bands),
              output_bands=(self.output_bands),
              image_size=image_size)
        else:
            raise Exception('Data load error,You should input a *.csv file')