# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\xl_tensorflow\utils\fintune.py
# Compiled at: 2020-04-07 03:43:18
# Size of source mod 2**32: 14165 bytes
import os, shutil, re
from .pretrained_model import ImageFineModel, my_call_backs
from xl_tool.xl_io import read_json
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.optimizers import Adam, RMSprop, SGD, Nadam, Adadelta, Adamax, Adagrad, Ftrl
import numpy as np
import matplotlib.pyplot as plt
import logging
from preprocessing.tfdata import image_from_tfrecord
logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', level=(logging.INFO),
  handlers=[
 logging.FileHandler('./training_log'), logging.StreamHandler()])
plt.rcParams['font.sans-serif'] = [
 'SimHei']
plt.rcParams['axes.unicode_minus'] = False
eff_input_dict = {'efficientnetb0':224,  'efficientnetb1':240,  'efficientnetb2':260, 
 'efficientnetb3':300, 
 'efficientnetb4':380}
optimizer_dict = {'RMSprop':RMSprop, 
 'Adam':Adam, 
 'Ftrl':Ftrl, 
 'SGD':SGD, 
 'Nadam':Nadam, 
 'Adamax':Adamax, 
 'Adadelta':Adadelta, 
 'Adagrad':Adagrad}

def file_scanning(path, file_format='.txt$', full_path=True, sub_scan=False):
    """
        scanning directory and return file paths with specified format
        :param path: directory to scan
        :param file_format:  file format to return ,regular patterns
        :param full_path: whether to return the full path
        :param sub_scan: whether to sanning the subfolder
        :return:file paths
        """
    if os.path.exists(path):
        file_paths = []
        for root, dirs, files in os.walk(path, topdown=True):
            paths = [file for file in files if re.search(file_format, file)]
            if full_path:
                paths = [os.path.join(root, file) for file in paths]
            file_paths.extend(paths)
            if not sub_scan:
                break

        file_paths or print('File with specified format not find')
        return
    else:
        print('Invalid path!')
        return
    return file_paths


def data_gen_from_one(target_size=(224, 224), batch_size=10):
    train_path = 'E:\\foodDetection_5_classes_first_20191227_train'
    datagen = ImageDataGenerator(rescale=0.00392156862745098, rotation_range=20, width_shift_range=0.1, height_shift_range=0.1,
      zoom_range=0.1,
      validation_split=0.2)
    train_gen = datagen.flow_from_directory(train_path, target_size=target_size, batch_size=batch_size, subset='training')
    val_gen = datagen.flow_from_directory(train_path, target_size=target_size, batch_size=batch_size, subset='validation')
    return (train_gen, val_gen)


def train_data_from_directory(train_path, val_path, target_size=(224, 224), batch_size=16, rescale=0.00392156862745098, rotation_range=20, width_shift_range=0.2, height_shift_range=0.2, zoom_range=0.3, vertical_flip=True, horizontal_flip=True, brightness_range=(0.7, 1.2), classes=None):
    """从指定数据集生成数据，如果没有验证集请将val_path设置为空"""
    train_datagen = ImageDataGenerator(rescale=rescale, rotation_range=rotation_range, width_shift_range=width_shift_range,
      height_shift_range=height_shift_range,
      brightness_range=brightness_range,
      zoom_range=zoom_range,
      vertical_flip=vertical_flip,
      horizontal_flip=horizontal_flip)
    val_datagen = ImageDataGenerator(rescale=rescale)
    train_gen = train_datagen.flow_from_directory(train_path, classes=classes, target_size=target_size, batch_size=batch_size)
    if val_path:
        val_gen = val_datagen.flow_from_directory(val_path, target_size=target_size, classes=classes, batch_size=batch_size)
        if train_gen.class_indices == val_gen.class_indices:
            return (
             train_gen, val_gen)
        logging.info('训练集与验证集类别定义不一致！')
        return False
    else:
        return train_gen


def finetune_model--- This code section failed: ---

 L. 108         0  LOAD_FAST                'tf_record'
              2_4  POP_JUMP_IF_FALSE   262  'to 262'

 L. 109         6  LOAD_FAST                'prefetch'
                8  POP_JUMP_IF_FALSE    90  'to 90'

 L. 110        10  LOAD_GLOBAL              image_from_tfrecord
               12  LOAD_FAST                'train_path'
               14  LOAD_FAST                'class_num'
               16  LOAD_FAST                'batch_size'

 L. 111        18  LOAD_FAST                'target_size'
               20  LOAD_CONST               0.15

 L. 112        22  LOAD_CONST               (0.8, 1.3)
               24  LOAD_CONST               0.3
               26  LOAD_CONST               0.15
               28  LOAD_CONST               0.04

 L. 113        30  LOAD_CONST               0.85
               32  LOAD_CONST               True
               34  LOAD_CONST               False

 L. 114        36  LOAD_CONST               True
               38  LOAD_FAST                'train_buffer_size'
               40  LOAD_CONST               ('target_size', 'random_brightness', 'random_contrast', 'rotate', 'zoom_range', 'noise', 'random_crop', 'random_flip_left_right', 'random_flip_up_down', 'random_aspect', 'buffer_size')
               42  CALL_FUNCTION_KW_14    14  '14 total positional and keyword args'
               44  LOAD_METHOD              prefetch

 L. 115        46  LOAD_GLOBAL              tf
               48  LOAD_ATTR                data
               50  LOAD_ATTR                experimental
               52  LOAD_ATTR                AUTOTUNE
               54  CALL_METHOD_1         1  '1 positional argument'
               56  STORE_FAST               'train_gen'

 L. 116        58  LOAD_GLOBAL              image_from_tfrecord
               60  LOAD_FAST                'val_path'
               62  LOAD_FAST                'class_num'
               64  LOAD_FAST                'batch_size'

 L. 117        66  LOAD_FAST                'target_size'
               68  LOAD_FAST                'val_buffer_size'
               70  LOAD_CONST               ('target_size', 'buffer_size')
               72  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
               74  LOAD_METHOD              prefetch

 L. 118        76  LOAD_GLOBAL              tf
               78  LOAD_ATTR                data
               80  LOAD_ATTR                experimental
               82  LOAD_ATTR                AUTOTUNE
               84  CALL_METHOD_1         1  '1 positional argument'
               86  STORE_FAST               'val_gen'
               88  JUMP_FORWARD        144  'to 144'
             90_0  COME_FROM             8  '8'

 L. 120        90  LOAD_GLOBAL              image_from_tfrecord
               92  LOAD_FAST                'train_path'
               94  LOAD_FAST                'class_num'
               96  LOAD_FAST                'batch_size'

 L. 121        98  LOAD_FAST                'target_size'
              100  LOAD_CONST               0.15

 L. 122       102  LOAD_CONST               (0.8, 1.3)
              104  LOAD_CONST               0.3
              106  LOAD_CONST               0.15
              108  LOAD_CONST               0.04

 L. 123       110  LOAD_CONST               0.85
              112  LOAD_CONST               True
              114  LOAD_CONST               False

 L. 124       116  LOAD_CONST               True
              118  LOAD_FAST                'train_buffer_size'
              120  LOAD_CONST               ('target_size', 'random_brightness', 'random_contrast', 'rotate', 'zoom_range', 'noise', 'random_crop', 'random_flip_left_right', 'random_flip_up_down', 'random_aspect', 'buffer_size')
              122  CALL_FUNCTION_KW_14    14  '14 total positional and keyword args'
              124  STORE_FAST               'train_gen'

 L. 125       126  LOAD_GLOBAL              image_from_tfrecord
              128  LOAD_FAST                'val_path'
              130  LOAD_FAST                'class_num'
              132  LOAD_FAST                'batch_size'

 L. 126       134  LOAD_FAST                'target_size'
              136  LOAD_FAST                'val_buffer_size'
              138  LOAD_CONST               ('target_size', 'buffer_size')
              140  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              142  STORE_FAST               'val_gen'
            144_0  COME_FROM            88  '88'

 L. 127       144  LOAD_GLOBAL              read_json
              146  LOAD_FAST                'tf_record_label2id'
              148  CALL_FUNCTION_1       1  '1 positional argument'
              150  STORE_FAST               'cat_id'

 L. 128       152  LOAD_GLOBAL              print
              154  LOAD_FAST                'cat_id'
              156  CALL_FUNCTION_1       1  '1 positional argument'
              158  POP_TOP          

 L. 129       160  LOAD_LISTCOMP            '<code_object <listcomp>>'
              162  LOAD_STR                 'finetune_model.<locals>.<listcomp>'
              164  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              166  LOAD_GLOBAL              sorted
              168  LOAD_LISTCOMP            '<code_object <listcomp>>'
              170  LOAD_STR                 'finetune_model.<locals>.<listcomp>'
              172  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              174  LOAD_FAST                'cat_id'
              176  LOAD_METHOD              items
              178  CALL_METHOD_0         0  '0 positional arguments'
              180  GET_ITER         
              182  CALL_FUNCTION_1       1  '1 positional argument'
              184  LOAD_LAMBDA              '<code_object <lambda>>'
              186  LOAD_STR                 'finetune_model.<locals>.<lambda>'
              188  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              190  LOAD_CONST               ('key',)
              192  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              194  GET_ITER         
              196  CALL_FUNCTION_1       1  '1 positional argument'
              198  STORE_FAST               'labels'

 L. 130       200  LOAD_GLOBAL              open
              202  LOAD_STR                 './model/labels/'
              204  LOAD_FAST                'prefix'
              206  LOAD_FAST                'name'
              208  BINARY_ADD       
              210  LOAD_STR                 '_'
              212  LOAD_FAST                'class_num'
              214  FORMAT_VALUE          0  ''
              216  LOAD_STR                 '_labels.txt'
              218  BUILD_STRING_3        3 
              220  BINARY_ADD       
              222  FORMAT_VALUE          0  ''
              224  BUILD_STRING_2        2 
              226  LOAD_STR                 'w'
              228  CALL_FUNCTION_2       2  '2 positional arguments'
              230  SETUP_WITH          254  'to 254'
              232  STORE_FAST               'f'

 L. 131       234  LOAD_FAST                'f'
              236  LOAD_METHOD              write
              238  LOAD_STR                 '\n'
              240  LOAD_METHOD              join
              242  LOAD_FAST                'labels'
              244  CALL_METHOD_1         1  '1 positional argument'
              246  CALL_METHOD_1         1  '1 positional argument'
              248  POP_TOP          
              250  POP_BLOCK        
              252  LOAD_CONST               None
            254_0  COME_FROM_WITH      230  '230'
              254  WITH_CLEANUP_START
              256  WITH_CLEANUP_FINISH
              258  END_FINALLY      
              260  JUMP_FORWARD        478  'to 478'
            262_0  COME_FROM             2  '2'

 L. 133       262  LOAD_GLOBAL              type
              264  LOAD_FAST                'classes'
              266  CALL_FUNCTION_1       1  '1 positional argument'
              268  LOAD_GLOBAL              str
              270  COMPARE_OP               ==
          272_274  POP_JUMP_IF_FALSE   322  'to 322'

 L. 134       276  LOAD_GLOBAL              print
              278  LOAD_FAST                'classes'
              280  CALL_FUNCTION_1       1  '1 positional argument'
              282  POP_TOP          

 L. 135       284  LOAD_GLOBAL              read_json
              286  LOAD_FAST                'classes'
              288  CALL_FUNCTION_1       1  '1 positional argument'
              290  STORE_FAST               'classes'

 L. 136       292  LOAD_LISTCOMP            '<code_object <listcomp>>'
              294  LOAD_STR                 'finetune_model.<locals>.<listcomp>'
              296  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              298  LOAD_GLOBAL              sorted
              300  LOAD_FAST                'classes'
              302  LOAD_METHOD              items
              304  CALL_METHOD_0         0  '0 positional arguments'
              306  LOAD_LAMBDA              '<code_object <lambda>>'
              308  LOAD_STR                 'finetune_model.<locals>.<lambda>'
              310  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              312  LOAD_CONST               ('key',)
              314  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              316  GET_ITER         
              318  CALL_FUNCTION_1       1  '1 positional argument'
              320  STORE_FAST               'classes'
            322_0  COME_FROM           272  '272'

 L. 137       322  LOAD_GLOBAL              train_data_from_directory
              324  LOAD_FAST                'train_path'
              326  LOAD_FAST                'val_path'
              328  LOAD_FAST                'classes'
              330  LOAD_FAST                'batch_size'

 L. 138       332  LOAD_CONST               0.00392156862745098
              334  LOAD_CONST               20
              336  LOAD_CONST               0.2

 L. 139       338  LOAD_CONST               0.2
              340  LOAD_CONST               0.3
              342  LOAD_CONST               True

 L. 140       344  LOAD_CONST               True
              346  LOAD_CONST               (0.7, 1.2)
              348  LOAD_CONST               ('classes', 'batch_size', 'rescale', 'rotation_range', 'width_shift_range', 'height_shift_range', 'zoom_range', 'vertical_flip', 'horizontal_flip', 'brightness_range')
              350  CALL_FUNCTION_KW_12    12  '12 total positional and keyword args'
              352  UNPACK_SEQUENCE_2     2 
              354  STORE_FAST               'train_gen'
              356  STORE_FAST               'val_gen'

 L. 141       358  LOAD_GLOBAL              dict
              360  CALL_FUNCTION_0       0  '0 positional arguments'
              362  STORE_FAST               'cat_id'

 L. 142       364  LOAD_FAST                'train_gen'
              366  LOAD_ATTR                class_indices
              368  LOAD_FAST                'cat_id'
              370  LOAD_STR                 'cat2id'
              372  STORE_SUBSCR     

 L. 143       374  LOAD_GLOBAL              print
              376  LOAD_FAST                'cat_id'
              378  LOAD_STR                 'cat2id'
              380  BINARY_SUBSCR    
              382  CALL_FUNCTION_1       1  '1 positional argument'
              384  POP_TOP          

 L. 144       386  LOAD_LISTCOMP            '<code_object <listcomp>>'
              388  LOAD_STR                 'finetune_model.<locals>.<listcomp>'
              390  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              392  LOAD_GLOBAL              sorted
              394  LOAD_FAST                'train_gen'
              396  LOAD_ATTR                class_indices
              398  LOAD_METHOD              items
              400  CALL_METHOD_0         0  '0 positional arguments'
              402  LOAD_LAMBDA              '<code_object <lambda>>'
              404  LOAD_STR                 'finetune_model.<locals>.<lambda>'
              406  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              408  LOAD_CONST               ('key',)
              410  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              412  GET_ITER         
              414  CALL_FUNCTION_1       1  '1 positional argument'
              416  STORE_FAST               'labels'

 L. 145       418  LOAD_GLOBAL              open
              420  LOAD_STR                 './model/labels/'
              422  LOAD_FAST                'prefix'
              424  LOAD_FAST                'name'
              426  BINARY_ADD       
              428  LOAD_STR                 '_'
              430  LOAD_FAST                'class_num'
              432  FORMAT_VALUE          0  ''
              434  LOAD_STR                 '_labels.txt'
              436  BUILD_STRING_3        3 
              438  BINARY_ADD       
              440  FORMAT_VALUE          0  ''
              442  BUILD_STRING_2        2 
              444  LOAD_STR                 'w'
              446  CALL_FUNCTION_2       2  '2 positional arguments'
              448  SETUP_WITH          472  'to 472'
              450  STORE_FAST               'f'

 L. 146       452  LOAD_FAST                'f'
              454  LOAD_METHOD              write
              456  LOAD_STR                 '\n'
              458  LOAD_METHOD              join
              460  LOAD_FAST                'labels'
              462  CALL_METHOD_1         1  '1 positional argument'
              464  CALL_METHOD_1         1  '1 positional argument'
              466  POP_TOP          
              468  POP_BLOCK        
              470  LOAD_CONST               None
            472_0  COME_FROM_WITH      448  '448'
              472  WITH_CLEANUP_START
              474  WITH_CLEANUP_FINISH
              476  END_FINALLY      
            478_0  COME_FROM           260  '260'

 L. 147       478  LOAD_GLOBAL              tf
              480  LOAD_ATTR                config
              482  LOAD_ATTR                experimental
              484  LOAD_METHOD              list_physical_devices
              486  LOAD_STR                 'GPU'
              488  CALL_METHOD_1         1  '1 positional argument'
              490  STORE_FAST               'gpus'

 L. 148       492  LOAD_FAST                'gpus'
          494_496  POP_JUMP_IF_FALSE   580  'to 580'

 L. 149       498  SETUP_EXCEPT        536  'to 536'

 L. 151       500  SETUP_LOOP          532  'to 532'
              502  LOAD_FAST                'gpus'
              504  GET_ITER         
              506  FOR_ITER            530  'to 530'
              508  STORE_FAST               'gpu'

 L. 152       510  LOAD_GLOBAL              tf
              512  LOAD_ATTR                config
              514  LOAD_ATTR                experimental
              516  LOAD_METHOD              set_memory_growth
              518  LOAD_FAST                'gpu'
              520  LOAD_CONST               True
              522  CALL_METHOD_2         2  '2 positional arguments'
              524  POP_TOP          
          526_528  JUMP_BACK           506  'to 506'
              530  POP_BLOCK        
            532_0  COME_FROM_LOOP      500  '500'
              532  POP_BLOCK        
              534  JUMP_FORWARD        580  'to 580'
            536_0  COME_FROM_EXCEPT    498  '498'

 L. 153       536  DUP_TOP          
              538  LOAD_GLOBAL              RuntimeError
              540  COMPARE_OP               exception-match
          542_544  POP_JUMP_IF_FALSE   578  'to 578'
              546  POP_TOP          
              548  STORE_FAST               'e'
              550  POP_TOP          
              552  SETUP_FINALLY       566  'to 566'

 L. 154       554  LOAD_GLOBAL              print
              556  LOAD_FAST                'e'
              558  CALL_FUNCTION_1       1  '1 positional argument'
              560  POP_TOP          
              562  POP_BLOCK        
              564  LOAD_CONST               None
            566_0  COME_FROM_FINALLY   552  '552'
              566  LOAD_CONST               None
              568  STORE_FAST               'e'
              570  DELETE_FAST              'e'
              572  END_FINALLY      
              574  POP_EXCEPT       
              576  JUMP_FORWARD        580  'to 580'
            578_0  COME_FROM           542  '542'
              578  END_FINALLY      
            580_0  COME_FROM           576  '576'
            580_1  COME_FROM           534  '534'
            580_2  COME_FROM           494  '494'

 L. 156       580  LOAD_FAST                'train_from_scratch'
          582_584  POP_JUMP_IF_TRUE    886  'to 886'

 L. 157       586  LOAD_GLOBAL              tf
              588  LOAD_ATTR                distribute
              590  LOAD_METHOD              MirroredStrategy
              592  CALL_METHOD_0         0  '0 positional arguments'
              594  STORE_FAST               'strategy'

 L. 158       596  LOAD_GLOBAL              logging
              598  LOAD_METHOD              info
              600  LOAD_STR                 'Number of devices: %d'
              602  LOAD_FAST                'strategy'
              604  LOAD_ATTR                num_replicas_in_sync
              606  BINARY_MODULO    
              608  CALL_METHOD_1         1  '1 positional argument'
              610  POP_TOP          

 L. 159       612  LOAD_FAST                'strategy'
              614  LOAD_METHOD              scope
              616  CALL_METHOD_0         0  '0 positional arguments'
              618  SETUP_WITH          678  'to 678'
              620  POP_TOP          

 L. 160       622  LOAD_GLOBAL              ImageFineModel
              624  LOAD_ATTR                create_fine_model
              626  LOAD_FAST                'name'
              628  LOAD_FAST                'class_num'
              630  LOAD_FAST                'weights'
              632  LOAD_FAST                'prefix'

 L. 161       634  LOAD_STR                 '_'
              636  LOAD_FAST                'class_num'
              638  FORMAT_VALUE          0  ''
              640  BUILD_STRING_2        2 
              642  LOAD_FAST                'dropout'

 L. 162       644  LOAD_CONST               True
              646  LOAD_FAST                'target_size'
              648  LOAD_CONST               (3,)
              650  BUILD_TUPLE_UNPACK_2     2 
              652  LOAD_CONST               ('weights', 'prefix', 'suffix', 'dropout', 'non_flatten_trainable', 'input_shape')
              654  CALL_FUNCTION_KW_8     8  '8 total positional and keyword args'
              656  STORE_FAST               'model'

 L. 163       658  LOAD_GLOBAL              my_call_backs
              660  LOAD_FAST                'model'
              662  LOAD_ATTR                name
              664  LOAD_FAST                'patience'
              666  LOAD_FAST                'reducelr'
              668  LOAD_CONST               ('patience', 'reducelr')
              670  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              672  STORE_FAST               'call_back'
              674  POP_BLOCK        
              676  LOAD_CONST               None
            678_0  COME_FROM_WITH      618  '618'
              678  WITH_CLEANUP_START
              680  WITH_CLEANUP_FINISH
              682  END_FINALLY      

 L. 164       684  LOAD_FAST                'test'
          686_688  POP_JUMP_IF_FALSE   718  'to 718'

 L. 165       690  LOAD_FAST                'model'
              692  LOAD_ATTR                fit
              694  LOAD_FAST                'train_gen'
              696  LOAD_FAST                'val_gen'
              698  LOAD_CONST               2
              700  LOAD_FAST                'call_back'
              702  LOAD_CONST               2

 L. 166       704  LOAD_CONST               2
              706  LOAD_CONST               True
              708  LOAD_CONST               5
              710  LOAD_CONST               ('validation_data', 'epochs', 'callbacks', 'steps_per_epoch', 'validation_steps', 'use_multiprocessing', 'workers')
              712  CALL_FUNCTION_KW_8     8  '8 total positional and keyword args'
              714  POP_TOP          
              716  JUMP_FORWARD       1172  'to 1172'
            718_0  COME_FROM           686  '686'

 L. 168       718  LOAD_FAST                'strategy'
              720  LOAD_METHOD              scope
              722  CALL_METHOD_0         0  '0 positional arguments'
              724  SETUP_WITH          766  'to 766'
              726  POP_TOP          

 L. 169       728  LOAD_FAST                'model'
              730  LOAD_ATTR                compile
              732  LOAD_GLOBAL              optimizer_dict
              734  LOAD_FAST                'optimizer'
              736  BINARY_SUBSCR    
              738  LOAD_FAST                'lrs'
              740  LOAD_CONST               0
              742  BINARY_SUBSCR    
              744  CALL_FUNCTION_1       1  '1 positional argument'
              746  LOAD_STR                 'categorical_crossentropy'

 L. 170       748  LOAD_GLOBAL              list
              750  LOAD_STR                 'accuracy'
              752  BUILD_LIST_1          1 
              754  CALL_FUNCTION_1       1  '1 positional argument'
              756  LOAD_CONST               ('loss', 'metrics')
              758  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              760  POP_TOP          
              762  POP_BLOCK        
              764  LOAD_CONST               None
            766_0  COME_FROM_WITH      724  '724'
              766  WITH_CLEANUP_START
              768  WITH_CLEANUP_FINISH
              770  END_FINALLY      

 L. 171       772  LOAD_FAST                'model'
              774  LOAD_ATTR                fit
              776  LOAD_FAST                'train_gen'
              778  LOAD_FAST                'val_gen'
              780  LOAD_FAST                'epochs'
              782  LOAD_CONST               0
              784  BINARY_SUBSCR    
              786  LOAD_FAST                'call_back'

 L. 172       788  LOAD_CONST               0
              790  LOAD_CONST               False
              792  LOAD_CONST               ('validation_data', 'epochs', 'callbacks', 'initial_epoch', 'use_multiprocessing')
              794  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
              796  POP_TOP          

 L. 173       798  LOAD_FAST                'strategy'
              800  LOAD_METHOD              scope
              802  CALL_METHOD_0         0  '0 positional arguments'
              804  SETUP_WITH          846  'to 846'
              806  POP_TOP          

 L. 174       808  LOAD_FAST                'model'
              810  LOAD_ATTR                compile
              812  LOAD_GLOBAL              optimizer_dict
              814  LOAD_FAST                'optimizer'
              816  BINARY_SUBSCR    
              818  LOAD_FAST                'lrs'
              820  LOAD_CONST               1
              822  BINARY_SUBSCR    
              824  CALL_FUNCTION_1       1  '1 positional argument'
              826  LOAD_STR                 'categorical_crossentropy'

 L. 175       828  LOAD_GLOBAL              list
              830  LOAD_STR                 'accuracy'
              832  BUILD_LIST_1          1 
              834  CALL_FUNCTION_1       1  '1 positional argument'
              836  LOAD_CONST               ('loss', 'metrics')
              838  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              840  POP_TOP          
              842  POP_BLOCK        
              844  LOAD_CONST               None
            846_0  COME_FROM_WITH      804  '804'
              846  WITH_CLEANUP_START
              848  WITH_CLEANUP_FINISH
              850  END_FINALLY      

 L. 176       852  LOAD_FAST                'model'
              854  LOAD_ATTR                fit_generator
              856  LOAD_FAST                'train_gen'
              858  LOAD_FAST                'val_gen'
              860  LOAD_FAST                'epochs'
              862  LOAD_CONST               1
              864  BINARY_SUBSCR    
              866  LOAD_FAST                'call_back'

 L. 177       868  LOAD_FAST                'epochs'
              870  LOAD_CONST               0
              872  BINARY_SUBSCR    
              874  LOAD_CONST               False
              876  LOAD_CONST               ('validation_data', 'epochs', 'callbacks', 'initial_epoch', 'use_multiprocessing')
              878  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
              880  POP_TOP          
          882_884  JUMP_FORWARD       1172  'to 1172'
            886_0  COME_FROM           582  '582'

 L. 179       886  LOAD_GLOBAL              print
              888  LOAD_STR                 '从头开始训练模型！！！'
              890  CALL_FUNCTION_1       1  '1 positional argument'
              892  POP_TOP          

 L. 180       894  LOAD_GLOBAL              tf
              896  LOAD_ATTR                distribute
              898  LOAD_METHOD              MirroredStrategy
              900  CALL_METHOD_0         0  '0 positional arguments'
              902  STORE_FAST               'strategy'

 L. 181       904  LOAD_FAST                'strategy'
              906  LOAD_METHOD              scope
              908  CALL_METHOD_0         0  '0 positional arguments'
              910  SETUP_WITH          968  'to 968'
              912  POP_TOP          

 L. 182       914  LOAD_GLOBAL              ImageFineModel
              916  LOAD_ATTR                create_fine_model
              918  LOAD_FAST                'name'
              920  LOAD_FAST                'class_num'

 L. 183       922  LOAD_FAST                'weights'
              924  LOAD_STR                 'imagenet'
              926  COMPARE_OP               ==
          928_930  POP_JUMP_IF_FALSE   936  'to 936'
              932  LOAD_FAST                'weights'
              934  JUMP_FORWARD        938  'to 938'
            936_0  COME_FROM           928  '928'
              936  LOAD_CONST               None
            938_0  COME_FROM           934  '934'
              938  LOAD_FAST                'prefix'

 L. 184       940  LOAD_STR                 '_'
              942  LOAD_FAST                'class_num'
              944  FORMAT_VALUE          0  ''
              946  BUILD_STRING_2        2 
              948  LOAD_FAST                'dropout'

 L. 185       950  LOAD_CONST               True
              952  LOAD_FAST                'target_size'
              954  LOAD_CONST               (3,)
              956  BUILD_TUPLE_UNPACK_2     2 
              958  LOAD_CONST               ('weights', 'prefix', 'suffix', 'dropout', 'non_flatten_trainable', 'input_shape')
              960  CALL_FUNCTION_KW_8     8  '8 total positional and keyword args'
              962  STORE_FAST               'model'
              964  POP_BLOCK        
              966  LOAD_CONST               None
            968_0  COME_FROM_WITH      910  '910'
              968  WITH_CLEANUP_START
              970  WITH_CLEANUP_FINISH
              972  END_FINALLY      

 L. 186       974  LOAD_FAST                'weights'
          976_978  POP_JUMP_IF_FALSE  1000  'to 1000'
              980  LOAD_FAST                'weights'
              982  LOAD_STR                 'imagenet'
              984  COMPARE_OP               !=
          986_988  POP_JUMP_IF_FALSE  1000  'to 1000'

 L. 187       990  LOAD_FAST                'model'
              992  LOAD_METHOD              load_weights
              994  LOAD_FAST                'weights'
              996  CALL_METHOD_1         1  '1 positional argument'
              998  POP_TOP          
           1000_0  COME_FROM           986  '986'
           1000_1  COME_FROM           976  '976'

 L. 188      1000  LOAD_GLOBAL              my_call_backs
             1002  LOAD_FAST                'model'
           1004_0  COME_FROM           716  '716'
             1004  LOAD_ATTR                name
             1006  LOAD_FAST                'patience'
             1008  LOAD_FAST                'reducelr'
             1010  LOAD_CONST               ('patience', 'reducelr')
             1012  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
             1014  STORE_FAST               'call_back'

 L. 189      1016  LOAD_FAST                'test'
         1018_1020  POP_JUMP_IF_FALSE  1050  'to 1050'

 L. 190      1022  LOAD_FAST                'model'
             1024  LOAD_ATTR                fit_generator
             1026  LOAD_FAST                'train_gen'
             1028  LOAD_FAST                'val_gen'
             1030  LOAD_CONST               2
             1032  LOAD_FAST                'call_back'
             1034  LOAD_CONST               2

 L. 191      1036  LOAD_CONST               2
             1038  LOAD_CONST               True
             1040  LOAD_CONST               5
             1042  LOAD_CONST               ('validation_data', 'epochs', 'callbacks', 'steps_per_epoch', 'validation_steps', 'use_multiprocessing', 'workers')
             1044  CALL_FUNCTION_KW_8     8  '8 total positional and keyword args'
             1046  POP_TOP          
             1048  JUMP_FORWARD       1172  'to 1172'
           1050_0  COME_FROM          1018  '1018'

 L. 193      1050  SETUP_LOOP         1172  'to 1172'
             1052  LOAD_GLOBAL              enumerate
             1054  LOAD_FAST                'epochs'
             1056  CALL_FUNCTION_1       1  '1 positional argument'
             1058  GET_ITER         
             1060  FOR_ITER           1170  'to 1170'
             1062  UNPACK_SEQUENCE_2     2 
             1064  STORE_FAST               'i'
             1066  STORE_FAST               'epoch'

 L. 194      1068  LOAD_FAST                'initial_epoch'
             1070  LOAD_FAST                'epoch'
             1072  COMPARE_OP               >=
         1074_1076  POP_JUMP_IF_FALSE  1082  'to 1082'

 L. 195  1078_1080  CONTINUE           1060  'to 1060'
           1082_0  COME_FROM          1074  '1074'

 L. 196      1082  LOAD_FAST                'strategy'
             1084  LOAD_METHOD              scope
             1086  CALL_METHOD_0         0  '0 positional arguments'
             1088  SETUP_WITH         1130  'to 1130'
             1090  POP_TOP          

 L. 197      1092  LOAD_FAST                'model'
             1094  LOAD_ATTR                compile
             1096  LOAD_GLOBAL              optimizer_dict
             1098  LOAD_FAST                'optimizer'
             1100  BINARY_SUBSCR    
             1102  LOAD_FAST                'lrs'
             1104  LOAD_FAST                'i'
             1106  BINARY_SUBSCR    
             1108  CALL_FUNCTION_1       1  '1 positional argument'
             1110  LOAD_STR                 'categorical_crossentropy'

 L. 198      1112  LOAD_GLOBAL              list
             1114  LOAD_STR                 'accuracy'
             1116  BUILD_LIST_1          1 
             1118  CALL_FUNCTION_1       1  '1 positional argument'
             1120  LOAD_CONST               ('loss', 'metrics')
             1122  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
             1124  POP_TOP          
             1126  POP_BLOCK        
             1128  LOAD_CONST               None
           1130_0  COME_FROM_WITH     1088  '1088'
             1130  WITH_CLEANUP_START
             1132  WITH_CLEANUP_FINISH
             1134  END_FINALLY      

 L. 199      1136  LOAD_FAST                'model'
             1138  LOAD_ATTR                fit
             1140  LOAD_FAST                'train_gen'
             1142  LOAD_FAST                'val_gen'
             1144  LOAD_FAST                'epoch'

 L. 200      1146  LOAD_FAST                'call_back'

 L. 201      1148  LOAD_FAST                'initial_epoch'
             1150  LOAD_CONST               False
             1152  LOAD_CONST               ('validation_data', 'epochs', 'callbacks', 'initial_epoch', 'use_multiprocessing')
             1154  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
             1156  POP_TOP          

 L. 202      1158  LOAD_FAST                'epochs'
             1160  LOAD_FAST                'i'
             1162  BINARY_SUBSCR    
             1164  STORE_FAST               'initial_epoch'
         1166_1168  JUMP_BACK          1060  'to 1060'
             1170  POP_BLOCK        
           1172_0  COME_FROM_LOOP     1050  '1050'
           1172_1  COME_FROM          1048  '1048'
           1172_2  COME_FROM           882  '882'

Parse error at or near `COME_FROM' instruction at offset 1004_0


def visual_misclassified_images(base_model, cat_num, weights, dataset, save_path, target_size=(224, 224), batch_size=32, test=False, classes=None):
    root_dir = os.path.split(os.path.abspath(dataset))[1]
    model = ImageFineModel.create_fine_model(base_model, cat_num=cat_num, weights=None)
    model.load_weights(weights)
    os.makedirs(save_path, exist_ok=True)
    target_size = target_size if base_model not in eff_input_dict.keys() else (
     eff_input_dict[base_model], eff_input_dict[base_model])
    if type(classes) == str:
        classes = read_json(classes)
        classes = [i[0] for i in sorted((classes.items()), key=(lambda x: x[1]))]
    gen = ImageDataGenerator(rescale=0.00392156862745098).flow_from_directory(dataset,
      shuffle=False, target_size=target_size, batch_size=batch_size, classes=classes)
    filenames = gen.filenames
    classes = gen.classes
    cat2id = gen.class_indices
    id2cat = dict([(i[1], i[0]) for i in cat2id.items()])
    predict_p = model.predict_generator(gen)
    predict_classes = predict_p.argmax(-1)
    count = 1
    for i in range(len(filenames)):
        if classes[i] == predict_classes[i]:
            continue
        else:
            if test:
                print'发现误分类样本：'filenames[i]
            true_label = id2cat[classes[i]]
            false_label = id2cat[predict_classes[i]]
            mis_filename = f"{true_label}__{false_label}__{root_dir}_{count}.jpg"
            shutil.copy(f"{dataset}/{filenames[i]}", f"{save_path}/{mis_filename}")
            count += 1

    cat_acc1, cat_acc2, top1, top2 = mul_classify_acc(predict_p, classes, cat_num)
    s = f">>>top1类别准确率：{top1}\n" + f">>>top2类别准确率：{top2}\n" + ('>>>单类别类准确率：\ntop1\t\ttop2\n' + '\n'.join([id2cat[i].rjust(10, ' ') + ':\t' + str(cat_acc1[i])[:4] + '\t' + str(cat_acc2[i])[:4] for i in range(cat_num)]))
    print(s)
    with open(f"{save_path}/mis_classify_result.txt", 'w', encoding='utf-8') as (f):
        f.write(s)


def mul_classify_acc(predict_p, real, cat_num):
    unique = list(range(cat_num))
    arg_sort = predict_p.argsort(axis=(-1))
    pred = arg_sort[:, -1]
    print(sum(predict_p.argmax(axis=(-1)) == pred))
    count = len(pred)
    pred = np.array(pred)
    real = np.array(real)
    all_eval = pred == real
    all_eval_2 = arg_sort[:, -2] == real
    cat_acc1 = [sum((real == i) & all_eval) / sum(real == i) for i in unique]
    cat_acc2 = [sum((real == i) & (all_eval_2 | all_eval)) / sum(real == i) for i in unique]
    top1 = sum(all_eval) / count
    top2 = sum(all_eval_2) / count + top1
    return (cat_acc1, cat_acc2, top1, top2)