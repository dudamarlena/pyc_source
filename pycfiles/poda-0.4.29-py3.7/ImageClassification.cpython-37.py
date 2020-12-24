# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\poda\application\ImageClassification.py
# Compiled at: 2019-09-29 12:40:38
# Size of source mod 2**32: 15843 bytes
import os, tensorflow as tf
from poda.layers.dense import *
from poda.layers.metrics import *
from poda.layers.optimizer import *
from poda.layers.activation import *
from poda.layers.convolutional import *
from poda.utils.visualize_training import *
from poda.transfer_learning.Vgg16_slim import *
from poda.transfer_learning.Vgg16 import VGG16
from poda.transfer_learning.InceptionV4_slim import *
import poda.transfer_learning.InceptionV4 as InceptionV4
import poda.preprocessing.GeneratorImage as generator

class ImageClassification(object):

    def __init__(self, classes, directory_dataset, batch_sizes=4, color_modes='rgb', image_sizes=(512, 512, 3), base_model='vgg_16', custom_architecture=False, dict_var_architecture={}):
        """[summary]
        
        Arguments:
            object {[type]} -- [description]
            classes {[type]} -- [description]
            directory_dataset {[type]} -- [description]
        
        Keyword Arguments:
            image_sizes {tuple} -- [description] (default: {(512,512,3)})
            base_model {str} -- [description] (default: {'vgg_16'})
            custom_architecture {bool} -- [description] (default: {False})
            dict_var_architecture {dict} -- [description] (default: {{}})
        """
        self.classes = classes
        self.dataset_folder_path = directory_dataset
        self.batch_size = batch_sizes
        self.color_mode = color_modes
        self.input_height = image_sizes[0]
        self.input_width = image_sizes[1]
        self.input_channel = image_sizes[2]
        self.image_size = image_sizes
        self.type_architecture = base_model
        self.custom_architecture = custom_architecture
        self.dict_var_architecture = dict_var_architecture
        self.input_tensor = tf.compat.v1.placeholder((tf.float32), shape=(self.batch_size, self.input_height, self.input_width, self.input_channel), name='input_tensor')
        self.output_tensor = tf.compat.v1.placeholder((tf.float32), (self.batch_size, self.classes), name='output_tensor')

    def create_model--- This code section failed: ---

 L.  46         0  LOAD_FAST                'self'
                2  LOAD_ATTR                type_architecture
                4  LOAD_STR                 'vgg_16_slim'
                6  COMPARE_OP               in
                8  POP_JUMP_IF_FALSE   234  'to 234'

 L.  47        10  LOAD_GLOBAL              len
               12  LOAD_FAST                'dict_architecture'
               14  CALL_FUNCTION_1       1  '1 positional argument'
               16  LOAD_CONST               0
               18  COMPARE_OP               >
               20  POP_JUMP_IF_FALSE    96  'to 96'

 L.  48        22  LOAD_FAST                'dict_architecture'
               24  LOAD_STR                 'num_blocks'
               26  BINARY_SUBSCR    
               28  STORE_FAST               'num_block'

 L.  49        30  LOAD_FAST                'dict_architecture'
               32  LOAD_STR                 'batch_normalizations'
               34  BINARY_SUBSCR    
               36  STORE_FAST               'batch_normalization'

 L.  50        38  LOAD_FAST                'dict_architecture'
               40  LOAD_STR                 'num_depthwise_layers'
               42  BINARY_SUBSCR    
               44  STORE_FAST               'num_depthwise_layer'

 L.  51        46  LOAD_FAST                'dict_architecture'
               48  LOAD_STR                 'num_dense_layers'
               50  BINARY_SUBSCR    
               52  STORE_FAST               'num_dense_layer'

 L.  52        54  LOAD_FAST                'dict_architecture'
               56  LOAD_STR                 'num_hidden_units'
               58  BINARY_SUBSCR    
               60  STORE_FAST               'num_hidden_unit'

 L.  53        62  LOAD_FAST                'dict_architecture'
               64  LOAD_STR                 'activation_denses'
               66  BINARY_SUBSCR    
               68  STORE_FAST               'activation_dense'

 L.  54        70  LOAD_FAST                'dict_architecture'
               72  LOAD_STR                 'dropout_rates'
               74  BINARY_SUBSCR    
               76  STORE_FAST               'dropout_rate'

 L.  55        78  LOAD_FAST                'dict_architecture'
               80  LOAD_STR                 'regularizers'
               82  BINARY_SUBSCR    
               84  STORE_FAST               'regularizer'

 L.  56        86  LOAD_FAST                'dict_architecture'
               88  LOAD_STR                 'scopes'
               90  BINARY_SUBSCR    
               92  STORE_FAST               'scope'
               94  JUMP_FORWARD        132  'to 132'
             96_0  COME_FROM            20  '20'

 L.  58        96  LOAD_CONST               4
               98  STORE_FAST               'num_block'

 L.  59       100  LOAD_CONST               True
              102  STORE_FAST               'batch_normalization'

 L.  60       104  LOAD_CONST               0
              106  STORE_FAST               'num_depthwise_layer'

 L.  61       108  LOAD_CONST               1
              110  STORE_FAST               'num_dense_layer'

 L.  62       112  LOAD_CONST               512
              114  STORE_FAST               'num_hidden_unit'

 L.  63       116  LOAD_STR                 'relu'
              118  STORE_FAST               'activation_dense'

 L.  64       120  LOAD_CONST               None
              122  STORE_FAST               'dropout_rate'

 L.  65       124  LOAD_CONST               None
              126  STORE_FAST               'regularizer'

 L.  66       128  LOAD_CONST               None
              130  STORE_FAST               'scope'
            132_0  COME_FROM            94  '94'

 L.  68       132  LOAD_FAST                'self'
              134  LOAD_ATTR                type_architecture
              136  LOAD_STR                 'vgg_16'
              138  COMPARE_OP               ==
              140  POP_JUMP_IF_FALSE   194  'to 194'

 L.  69       142  LOAD_GLOBAL              VGG16
              144  LOAD_FAST                'self'
              146  LOAD_ATTR                input_tensor
              148  LOAD_FAST                'num_block'
              150  LOAD_FAST                'self'
              152  LOAD_ATTR                classes
              154  LOAD_FAST                'batch_normalization'
              156  LOAD_FAST                'num_depthwise_layer'

 L.  70       158  LOAD_FAST                'num_dense_layer'
              160  LOAD_FAST                'num_hidden_unit'
              162  LOAD_FAST                'activation_dense'
              164  LOAD_FAST                'dropout_rate'
              166  LOAD_FAST                'regularizer'
              168  LOAD_FAST                'scope'
              170  LOAD_CONST               ('input_tensor', 'num_blocks', 'classes', 'batch_normalizations', 'num_depthwise_layers', 'num_dense_layers', 'num_hidden_units', 'activation_denses', 'dropout_rates', 'regularizers', 'scopes')
              172  CALL_FUNCTION_KW_11    11  '11 total positional and keyword args'
              174  STORE_FAST               'model'

 L.  71       176  LOAD_FAST                'model'
              178  LOAD_METHOD              create_model
              180  CALL_METHOD_0         0  '0 positional arguments'
              182  UNPACK_SEQUENCE_4     4 
              184  STORE_FAST               'non_logit'
              186  STORE_FAST               'output'
              188  STORE_FAST               'base_var_list'
              190  STORE_FAST               'full_var_list'
              192  JUMP_FORWARD        626  'to 626'
            194_0  COME_FROM           140  '140'

 L.  73       194  LOAD_GLOBAL              vgg16
              196  LOAD_FAST                'self'
              198  LOAD_ATTR                input_tensor
              200  LOAD_FAST                'self'
              202  LOAD_ATTR                classes
              204  LOAD_FAST                'num_block'
              206  LOAD_FAST                'num_depthwise_layer'

 L.  74       208  LOAD_FAST                'num_dense_layer'
              210  LOAD_FAST                'num_hidden_unit'
              212  LOAD_FAST                'activation_dense'
              214  LOAD_FAST                'regularizer'
              216  LOAD_CONST               ('input_tensor', 'num_classes', 'num_blocks', 'num_depthwise_layer', 'num_fully_connected_layer', 'num_hidden_unit', 'activation_fully_connected', 'regularizers')
              218  CALL_FUNCTION_KW_8     8  '8 total positional and keyword args'
              220  UNPACK_SEQUENCE_4     4 
              222  STORE_FAST               'non_logit'
              224  STORE_FAST               'output'
              226  STORE_FAST               'base_var_list'
              228  STORE_FAST               'full_var_list'
          230_232  JUMP_FORWARD        626  'to 626'
            234_0  COME_FROM             8  '8'

 L.  76       234  LOAD_FAST                'self'
              236  LOAD_ATTR                type_architecture
              238  LOAD_STR                 'inception_v4_slim'
              240  COMPARE_OP               in
          242_244  POP_JUMP_IF_FALSE   442  'to 442'

 L.  77       246  LOAD_GLOBAL              len
              248  LOAD_FAST                'dict_architecture'
              250  CALL_FUNCTION_1       1  '1 positional argument'
              252  LOAD_CONST               0
              254  COMPARE_OP               >
          256_258  POP_JUMP_IF_FALSE   318  'to 318'

 L.  78       260  LOAD_FAST                'dict_architecture'
              262  LOAD_STR                 'n_inception_a'
              264  BINARY_SUBSCR    
              266  STORE_FAST               'inception_a'

 L.  79       268  LOAD_FAST                'dict_architecture'
              270  LOAD_STR                 'n_inception_b'
              272  BINARY_SUBSCR    
              274  STORE_FAST               'inception_b'

 L.  80       276  LOAD_FAST                'dict_architecture'
              278  LOAD_STR                 'n_inception_c'
              280  BINARY_SUBSCR    
              282  STORE_FAST               'inception_c'

 L.  81       284  LOAD_FAST                'dict_architecture'
              286  LOAD_STR                 'batch_normalizations'
              288  BINARY_SUBSCR    
              290  STORE_FAST               'batch_normalization'

 L.  82       292  LOAD_FAST                'dict_architecture'
              294  LOAD_STR                 'dropout_rates'
              296  BINARY_SUBSCR    
              298  STORE_FAST               'dropout_rate'

 L.  83       300  LOAD_FAST                'dict_architecture'
              302  LOAD_STR                 'regularizers'
              304  BINARY_SUBSCR    
              306  STORE_FAST               'regularizer'

 L.  84       308  LOAD_FAST                'dict_architecture'
              310  LOAD_STR                 'scopes'
              312  BINARY_SUBSCR    
              314  STORE_FAST               'scope'
              316  JUMP_FORWARD        346  'to 346'
            318_0  COME_FROM           256  '256'

 L.  86       318  LOAD_CONST               4
              320  STORE_FAST               'inception_a'

 L.  87       322  LOAD_CONST               7
              324  STORE_FAST               'inception_b'

 L.  88       326  LOAD_CONST               3
              328  STORE_FAST               'inception_c'

 L.  89       330  LOAD_CONST               True
              332  STORE_FAST               'batch_normalization'

 L.  90       334  LOAD_CONST               None
              336  STORE_FAST               'dropout_rate'

 L.  91       338  LOAD_CONST               None
              340  STORE_FAST               'regularizer'

 L.  92       342  LOAD_CONST               None
              344  STORE_FAST               'scope'
            346_0  COME_FROM           316  '316'

 L.  94       346  LOAD_FAST                'self'
              348  LOAD_ATTR                type_architecture
              350  LOAD_STR                 'inception_v4'
              352  COMPARE_OP               ==
          354_356  POP_JUMP_IF_FALSE   406  'to 406'

 L.  95       358  LOAD_GLOBAL              InceptionV4
              360  LOAD_FAST                'self'
              362  LOAD_ATTR                input_tensor
              364  LOAD_FAST                'inception_a'
              366  LOAD_FAST                'inception_b'
              368  LOAD_FAST                'inception_c'
              370  LOAD_FAST                'self'
              372  LOAD_ATTR                classes
              374  LOAD_FAST                'batch_normalization'

 L.  96       376  LOAD_FAST                'dropout_rate'
              378  LOAD_FAST                'regularizer'
              380  LOAD_FAST                'scope'
              382  LOAD_CONST               ('input_tensor', 'n_inception_a', 'n_inception_b', 'n_inception_c', 'classes', 'batch_normalizations', 'dropout_rates', 'regularizers', 'scopes')
              384  CALL_FUNCTION_KW_9     9  '9 total positional and keyword args'
              386  STORE_FAST               'model'

 L.  97       388  LOAD_FAST                'model'
              390  LOAD_METHOD              create_model
              392  CALL_METHOD_0         0  '0 positional arguments'
              394  UNPACK_SEQUENCE_4     4 
              396  STORE_FAST               'non_logit'
              398  STORE_FAST               'output'
              400  STORE_FAST               'base_var_list'
              402  STORE_FAST               'full_var_list'
              404  JUMP_FORWARD        440  'to 440'
            406_0  COME_FROM           354  '354'

 L.  99       406  LOAD_GLOBAL              inception_v4
              408  LOAD_FAST                'self'
              410  LOAD_ATTR                input_tensor
              412  LOAD_FAST                'self'
              414  LOAD_ATTR                classes
              416  LOAD_STR                 'Mixed_7d'
              418  LOAD_FAST                'batch_normalization'
              420  LOAD_FAST                'dropout_rate'

 L. 100       422  LOAD_CONST               None
              424  LOAD_FAST                'regularizer'
              426  LOAD_CONST               ('inputs', 'num_classes', 'final_endpoint', 'is_training', 'dropout_keep_prob', 'num_depthwise_layer', 'regularizers')
              428  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
              430  UNPACK_SEQUENCE_4     4 
              432  STORE_FAST               'non_logit'
              434  STORE_FAST               'output'
              436  STORE_FAST               'base_var_list'
              438  STORE_FAST               'full_var_list'
            440_0  COME_FROM           404  '404'
              440  JUMP_FORWARD        626  'to 626'
            442_0  COME_FROM           242  '242'

 L. 101       442  LOAD_FAST                'self'
              444  LOAD_ATTR                type_architecture
              446  LOAD_STR                 'inception_resnet_v2_slim'
              448  COMPARE_OP               ==
          450_452  POP_JUMP_IF_FALSE   626  'to 626'

 L. 102       454  LOAD_GLOBAL              len
              456  LOAD_FAST                'dict_architecture'
              458  CALL_FUNCTION_1       1  '1 positional argument'
              460  LOAD_CONST               0
              462  COMPARE_OP               >
          464_466  POP_JUMP_IF_FALSE   526  'to 526'

 L. 103       468  LOAD_FAST                'dict_architecture'
              470  LOAD_STR                 'n_inception_a'
              472  BINARY_SUBSCR    
              474  STORE_FAST               'inception_a'

 L. 104       476  LOAD_FAST                'dict_architecture'
              478  LOAD_STR                 'n_inception_b'
              480  BINARY_SUBSCR    
              482  STORE_FAST               'inception_b'

 L. 105       484  LOAD_FAST                'dict_architecture'
              486  LOAD_STR                 'n_inception_c'
              488  BINARY_SUBSCR    
              490  STORE_FAST               'inception_c'

 L. 106       492  LOAD_FAST                'dict_architecture'
              494  LOAD_STR                 'batch_normalizations'
              496  BINARY_SUBSCR    
              498  STORE_FAST               'batch_normalization'

 L. 107       500  LOAD_FAST                'dict_architecture'
              502  LOAD_STR                 'dropout_rates'
              504  BINARY_SUBSCR    
              506  STORE_FAST               'dropout_rate'

 L. 108       508  LOAD_FAST                'dict_architecture'
              510  LOAD_STR                 'regularizers'
              512  BINARY_SUBSCR    
              514  STORE_FAST               'regularizer'

 L. 109       516  LOAD_FAST                'dict_architecture'
              518  LOAD_STR                 'scopes'
              520  BINARY_SUBSCR    
              522  STORE_FAST               'scope'
              524  JUMP_FORWARD        554  'to 554'
            526_0  COME_FROM           464  '464'

 L. 111       526  LOAD_CONST               5
              528  STORE_FAST               'inception_a'

 L. 112       530  LOAD_CONST               10
              532  STORE_FAST               'inception_b'

 L. 113       534  LOAD_CONST               5
              536  STORE_FAST               'inception_c'

 L. 114       538  LOAD_CONST               True
              540  STORE_FAST               'batch_normalization'

 L. 115       542  LOAD_CONST               None
              544  STORE_FAST               'dropout_rate'

 L. 116       546  LOAD_CONST               None
              548  STORE_FAST               'regularizer'

 L. 117       550  LOAD_CONST               None
              552  STORE_FAST               'scope'
            554_0  COME_FROM           524  '524'

 L. 119       554  LOAD_FAST                'self'
              556  LOAD_ATTR                type_architecture
              558  LOAD_STR                 'inception_resnet_v2'
              560  COMPARE_OP               ==
          562_564  POP_JUMP_IF_FALSE   614  'to 614'

 L. 120       566  LOAD_GLOBAL              InceptionResnetV2
              568  LOAD_FAST                'self'
              570  LOAD_ATTR                input_tensor
              572  LOAD_FAST                'inception_a'
              574  LOAD_FAST                'inception_b'
              576  LOAD_FAST                'inception_c'
              578  LOAD_FAST                'self'
              580  LOAD_ATTR                classes
              582  LOAD_FAST                'batch_normalization'

 L. 121       584  LOAD_CONST               None
            586_0  COME_FROM           192  '192'
              586  LOAD_CONST               None
              588  LOAD_CONST               None
              590  LOAD_CONST               ('input_tensor', 'n_inception_a', 'n_inception_b', 'n_inception_c', 'classes', 'batch_normalizations', 'dropout_rates', 'regularizers', 'scopes')
              592  CALL_FUNCTION_KW_9     9  '9 total positional and keyword args'
              594  STORE_FAST               'model'

 L. 122       596  LOAD_FAST                'model'
              598  LOAD_METHOD              create_model
              600  CALL_METHOD_0         0  '0 positional arguments'
              602  UNPACK_SEQUENCE_4     4 
              604  STORE_FAST               'non_logit'
              606  STORE_FAST               'output'
              608  STORE_FAST               'base_var_list'
              610  STORE_FAST               'full_var_list'
              612  JUMP_FORWARD        626  'to 626'
            614_0  COME_FROM           562  '562'

 L. 124       614  LOAD_CONST               (None, None, None, None)
              616  UNPACK_SEQUENCE_4     4 
              618  STORE_FAST               'non_logit'
              620  STORE_FAST               'output'
              622  STORE_FAST               'base_var_list'
              624  STORE_FAST               'full_var_list'
            626_0  COME_FROM           612  '612'
            626_1  COME_FROM           450  '450'
            626_2  COME_FROM           440  '440'
            626_3  COME_FROM           230  '230'

 L. 127       626  LOAD_FAST                'non_logit'
              628  LOAD_FAST                'output'
              630  LOAD_FAST                'base_var_list'
              632  LOAD_FAST                'full_var_list'
              634  BUILD_TUPLE_4         4 
              636  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM' instruction at offset 586_0

    def train(self, epoch, output_model_path, dict_augmented_image={}, is_last_checkpoint=False, manual_split_dataset=False, use_pretrain=False, path_pretrained='', threshold_best_model=0.5, optimizers_name='adam', lr=0.0001):
        train_accuracy = []
        train_losess = []
        val_accuracy = []
        val_losess = []
        if self.custom_architecture:
            non_logit, output, base_var_list, full_var_list = self.create_model(dict_architecture=(self.dict_var_architecture))
        else:
            non_logit, output, base_var_list, full_var_list = self.create_model(dict_architecture={})
        accuracy = calculate_accuracy_classification(output, self.output_tensor)
        cost = calculate_loss(input_tensor=non_logit, label=(self.output_tensor), type_loss_function='softmax_crossentropy_mean')
        update_ops = tf.compat.v1.get_collection(tf.compat.v1.GraphKeys.UPDATE_OPS)
        with tf.control_dependencies(update_ops):
            optimizer = optimizers(optimizers_names=optimizers_name, learning_rates=lr).minimize(cost)
        init = tf.compat.v1.global_variables_initializer
        if len(dict_augmented_image) > 0:
            rotation_degree = dict_augmented_image['rotation_degree']
            flip_horizontal = dict_augmented_image['flip_horizontal']
            flip_vertical = dict_augmented_image['flip_vertical']
            zoom_scale = dict_augmented_image['zoom_scale']
        else:
            rotation_degree = None
            flip_horizontal = False
            flip_vertical = False
            zoom_scale = None
        if manual_split_dataset:
            if len(dict_augmented_image) > 0:
                gen_train = generator(batch_sizes=(self.batch_size), color_modes=(self.color_mode), image_sizes=(self.image_size), rotation_degrees=rotation_degree, flip_image_horizontal_status=flip_horizontal, flip_image_vertical_status=flip_vertical,
                  zoom_scales=zoom_scale)
                gen_val = generator(batch_sizes=(self.batch_size), color_modes=(self.color_mode), image_sizes=(self.image_size), rotation_degrees=rotation_degree, flip_image_horizontal_status=flip_horizontal, flip_image_vertical_status=flip_vertical,
                  zoom_scales=zoom_scale)
            else:
                gen_train = generator(batch_sizes=(self.batch_size), color_modes=(self.color_mode), image_sizes=(self.image_size))
                gen_val = generator(batch_sizes=(self.batch_size), color_modes=(self.color_mode), image_sizes=(self.image_size))
            path_dataset_train = os.path.join(self.dataset_folder_path, 'train')
            path_dataset_val = os.path.join(self.dataset_folder_path, 'val')
            generator_train, num_train_data = gen_train.generate_from_directory_manual(directory=path_dataset_train)
            generator_val, num_val_data = gen_val.generate_from_directory_manual(directory=path_dataset_val)
        else:
            if len(dict_augmented_image) > 0:
                image_generator = generator(batch_sizes=(self.batch_size), color_modes=(self.color_mode), image_sizes=(self.image_size), rotation_degrees=rotation_degree, flip_image_horizontal_status=flip_horizontal, flip_image_vertical_status=flip_vertical,
                  zoom_scales=zoom_scale)
            else:
                image_generator = generator(batch_sizes=(self.batch_size), color_modes=(self.color_mode), image_sizes=(self.image_size))
            generator_train, generator_val, num_train_data, num_val_data = image_generator.generate_from_directory_auto(directory=(self.dataset_folder_path), val_ratio=0.2)
        main_graph_saver = tf.compat.v1.train.Saver(base_var_list)
        output_saver = tf.compat.v1.train.Saver
        output_saver_path = os.path.join(os.getcwd, output_model_path, 'full_model')
        if not os.path.exists(output_saver_path):
            os.makedirs(output_saver_path)
        main_graph_saver_path = os.path.join(os.getcwd, output_model_path, 'base_model')
        if not os.path.exists(main_graph_saver_path):
            os.makedirs(main_graph_saver_path)
        base_model_path = os.path.join(main_graph_saver_path, 'base_' + str(self.type_architecture))
        full_model_path = os.path.join(output_saver_path, str(self.type_architecture))
        msg = 'Epoch: {0:>6} loss: {1:>6.3} - acc: {2:>6.3} - val_loss: {3:>6.3} - val_acc: {4:>6.3} - {5}'
        train_iteration = int(num_train_data / self.batch_size)
        validation_iteration = int(num_val_data / self.batch_size)
        counter_model = 1
        with tf.compat.v1.Session as (sess):
            sess.run(init)
            if is_last_checkpoint:
                loader_output = tf.compat.v1.train.import_meta_graph(full_model_path + '.meta')
                loader_output.restore(sess, full_model_path)
            if use_pretrain:
                loader_main_graph = tf.compat.v1.train.import_meta_graph(base_model_path + '.meta')
                loader_main_graph.restore(sess, base_model_path)
            best_val_accuracy = threshold_best_model
            for i in range(epoch):
                print('Epoch ' + str(i + 1) + '/' + str(epoch))
                tmp_train_loss = []
                tmp_train_acc = []
                print('Step Train')
                for j in range(0, train_iteration):
                    sign = '--------------'
                    x_batch_train, y_batch_train = next(generator_train)
                    feed_dict_train = {self.input_tensor: x_batch_train, self.output_tensor: y_batch_train}
                    sess.run(optimizer, feed_dict=feed_dict_train)
                    y_prediction, train_loss = sess.run([output, cost], feed_dict=feed_dict_train)
                    train_acc = sess.run(accuracy, feed_dict=feed_dict_train)
                    print_progress_training(number_iteration=train_iteration, index_iteration=j, metrics_acc=train_acc, metrics_loss=train_loss, type_progress='train')
                    tmp_train_loss.append(train_loss)
                    tmp_train_acc.append(train_acc)

                avg_train_loss = sum(tmp_train_loss) / (len(tmp_train_loss) + 0.0001)
                avg_train_acc = sum(tmp_train_acc) / (len(tmp_train_acc) + 0.0001)
                tmp_val_loss = []
                tmp_val_acc = []
                print('Step Validation')
                for k in range(0, validation_iteration):
                    x_batch_valid, y_batch_valid = next(generator_val)
                    feed_dict_valid = {self.input_tensor: x_batch_valid, self.output_tensor: y_batch_valid}
                    y_validation, val_loss = sess.run([output, cost], feed_dict=feed_dict_valid)
                    val_acc = sess.run(accuracy, feed_dict=feed_dict_valid)
                    print_progress_training(number_iteration=validation_iteration, index_iteration=k, metrics_acc=val_acc, metrics_loss=val_loss, type_progress='val')
                    tmp_val_loss.append(val_loss)
                    tmp_val_acc.append(val_acc)

                avg_val_loss = sum(tmp_val_loss) / (len(tmp_val_loss) + 0.0001)
                avg_val_acc = sum(tmp_val_acc) / (len(tmp_val_acc) + 0.0001)
                if avg_val_acc > best_val_accuracy:
                    main_graph_saver.save(sess=sess, save_path=base_model_path)
                    output_saver.save(sess=sess, save_path=full_model_path)
                    best_val_accuracy = avg_val_acc
                    sign = 'Found the Best ' + str(counter_model)
                    counter_model += 1
                train_accuracy.append(avg_train_acc)
                train_losess.append(avg_train_loss)
                val_accuracy.append(avg_val_acc)
                val_losess.append(avg_val_loss)
                print(msg.format(i, avg_train_loss, avg_train_acc, avg_val_loss, avg_val_acc, sign))

        return (
         train_accuracy, train_losess, val_accuracy, val_losess)