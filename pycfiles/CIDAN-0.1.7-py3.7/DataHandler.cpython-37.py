# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/CIDAN/GUI/Data_Interaction/DataHandler.py
# Compiled at: 2020-04-29 16:40:22
# Size of source mod 2**32: 19325 bytes
import json, os
from typing import Dict
from PIL import Image
from skimage import feature
import numpy as np
from CIDAN.LSSC.functions.data_manipulation import load_filter_tif_stack, filter_stack, reshape_to_2d_over_time, pixel_num_to_2d_cord
from CIDAN.LSSC.functions.temporal_correlation import calculate_temporal_correlation
from CIDAN.LSSC.functions.pickle_funcs import *
import CIDAN.LSSC.process_data as process_data
import logging
logger1 = logging.getLogger('CIDAN.DataHandler')

class DataHandler:
    global_params_default = {'save_intermediate_steps':True, 
     'need_recalc_dataset_params':True, 
     'need_recalc_filter_params':True, 
     'need_recalc_box_params':True, 
     'need_recalc_eigen_params':True, 
     'need_recalc_roi_extraction_params':True, 
     'num_threads':1}
    dataset_params_default = {'dataset_path':'', 
     'slice_stack':False, 
     'slice_every':3, 
     'slice_start':0}
    filter_params_default = {'median_filter':False, 
     'median_filter_size':3, 
     'z_score':False}
    box_params_default = {'total_num_time_steps':1, 
     'total_num_spatial_boxes':4, 
     'spatial_overlap':30}
    eigen_params_default = {'eigen_vectors_already_generated':False, 
     'num_eig':50, 
     'normalize_w_k':2, 
     'metric':'l2', 
     'knn':20, 
     'accuracy':39, 
     'connections':40}
    roi_extraction_params_default = {'elbow_threshold_method':True, 
     'elbow_threshold_value':1, 
     'eigen_threshold_method':True, 
     'eigen_threshold_value':0.5, 
     'num_eigen_vector_select':10, 
     'merge_temporal_coef':0.95, 
     'roi_size_min':30, 
     'roi_size_max':600, 
     'merge':True, 
     'num_rois':25, 
     'fill_holes':True, 
     'refinement':True, 
     'max_iter':1000}

    def __init__(self, data_path, save_dir_path, save_dir_already_created, trials=[]):
        self.color_list = [
         (218, 67, 34),
         (132, 249, 22), (22, 249, 140), (22, 245, 249),
         (22, 132, 249), (224, 22, 249), (249, 22, 160)]
        self.save_dir_path = save_dir_path
        self.rois_loaded = False
        if save_dir_already_created:
            valid = self.load_param_json()
            self.calculate_filters()
            if self.rois_exist:
                self.load_rois()
                self.calculate_time_traces()
                self.rois_loaded = True
            assert valid, 'Save directory not valid'
        else:
            self.global_params = DataHandler.global_params_default.copy()
            self.dataset_params = DataHandler.dataset_params_default.copy()
            self.dataset_params['dataset_path'] = data_path
            self.dataset_params['trials'] = trials
            self.trials = trials
            self.filter_params = DataHandler.filter_params_default.copy()
            self.box_params = DataHandler.box_params_default.copy()
            self.box_params['total_num_time_steps'] = len(trials)
            self.eigen_params = DataHandler.eigen_params_default.copy()
            self.roi_extraction_params = DataHandler.roi_extraction_params_default.copy()
            valid = self.create_new_save_dir()
            if not valid:
                raise FileNotFoundError('Please chose an empty directory for your save directory')
            self.time_traces = []

    def __del__(self):
        for x in self.__dict__.items():
            self.__dict__[x] = None

    @property
    def param_path(self):
        return os.path.join(self.save_dir_path, 'parameters.json')

    @property
    def eigen_vectors_exist(self):
        eigen_dir = os.path.join(self.save_dir_path, 'eigen_vectors')
        file_names = ['eigen_vectors_box_{}_{}.pickle'.format(spatial_box_num, time_box_num) for spatial_box_num in range(self.box_params['total_num_spatial_boxes']) for time_box_num in range(self.box_params['total_num_time_steps'])]
        return all((pickle_exist(x, output_directory=eigen_dir) for x in file_names))

    @property
    def rois_exist(self):
        return pickle_exist('rois', output_directory=(self.save_dir_path))

    def load_rois(self):
        if pickle_exist('rois', output_directory=(self.save_dir_path)):
            self.clusters = pickle_load('rois', output_directory=(self.save_dir_path))
            self.gen_roi_display_variables()

    def save_rois(self, rois):
        if os.path.isdir(self.save_dir_path):
            pickle_save(rois, 'rois', output_directory=(self.save_dir_path))

    def load_param_json(self):
        try:
            with open(self.param_path, 'r') as (f):
                all_params = json.loads(f.read())
            self.global_params = all_params['global_params']
            self.dataset_params = all_params['dataset_params']
            self.filter_params = all_params['filter_params']
            self.box_params = all_params['box_params']
            self.eigen_params = all_params['eigen_params']
            self.roi_extraction_params = all_params['roi_extraction_params']
            self.trials = self.dataset_params['trials']
            return True
        except KeyError:
            raise KeyError('Please Choose a valid parameter file')
        except FileNotFoundError:
            raise FileNotFoundError("Can't find parameter file")
        except NameError:
            raise FileNotFoundError("Can't find parameter file")

    def save_new_param_json(self):
        try:
            with open(self.param_path, 'w') as (f):
                all_params = {'global_params':self.global_params,  'dataset_params':self.dataset_params, 
                 'filter_params':self.filter_params, 
                 'box_params':self.box_params, 
                 'eigen_params':self.eigen_params, 
                 'roi_extraction_params':self.roi_extraction_params}
                f.truncate(0)
                f.write(json.dumps(all_params))
        except:
            raise FileNotFoundError('Error saving parameters, please restart software')

    def create_new_save_dir(self):
        try:
            if not os.path.isdir(self.save_dir_path):
                os.mkdir(self.save_dir_path)
            else:
                eigen_vectors_folder_path = os.path.join(self.save_dir_path, 'eigen_vectors/')
                if not os.path.isdir(eigen_vectors_folder_path):
                    os.mkdir(eigen_vectors_folder_path)
                embedding_images_path = os.path.join(self.save_dir_path, 'embedding_norm_images/')
                os.path.isdir(embedding_images_path) or os.mkdir(embedding_images_path)
            return True
        except:
            raise FileNotFoundError("Couldn't create folder please try again")

    def change_global_param(self, param_name, new_value):
        if param_name in self.global_params:
            self.global_params[param_name] = new_value
            self.save_new_param_json()
            return True
        return False

    def change_dataset_param(self, param_name, new_value):
        if param_name in self.dataset_params:
            self.dataset_params[param_name] = new_value
            self.global_params['need_recalc_dataset_params'] = True
            self.save_new_param_json()
            return True
        return False

    def change_filter_param(self, param_name, new_value):
        if param_name in self.filter_params:
            self.filter_params[param_name] = new_value
            self.global_params['need_recalc_filter_params'] = True
            self.save_new_param_json()
            return True
        return False

    def change_box_param(self, param_name, new_value):
        if param_name in self.box_params:
            self.box_params[param_name] = new_value
            self.global_params['need_recalc_box_params'] = True
            self.global_params['need_recalc_eigen_params'] = True
            self.global_params['need_recalc_roi_extraction_params'] = True
            self.save_new_param_json()
            return True
        return False

    def change_eigen_param(self, param_name, new_value):
        if param_name in self.eigen_params:
            self.eigen_params[param_name] = new_value
            self.global_params['need_recalc_eigen_params'] = True
            self.save_new_param_json()
            return True
        return False

    def change_roi_extraction_param(self, param_name, new_value):
        if param_name in self.roi_extraction_params:
            self.roi_extraction_params[param_name] = new_value
            self.global_params['need_recalc_roi_extraction_params'] = True
            self.save_new_param_json()
            return True
        return False

    def calculate_dataset(self) -> np.ndarray:
        """Loads the dataset

        Returns
        -------
        """
        self.dataset = load_filter_tif_stack(path=[os.path.join(self.dataset_params['dataset_path'], x) for x in self.dataset_params['trials']],
          filter=False,
          median_filter=False,
          median_filter_size=(1, 3, 3),
          z_score=False,
          slice_stack=(self.dataset_params['slice_stack']),
          slice_start=(self.dataset_params['slice_start']),
          slice_every=(self.dataset_params['slice_every']))
        self.global_params['need_recalc_dataset_params'] = False
        self.shape = self.dataset.shape
        print('Finished Calculating Dataset')
        return self.dataset

    def calculate_filters--- This code section failed: ---

 L. 269         0  LOAD_FAST                'self'
                2  LOAD_ATTR                global_params
                4  LOAD_STR                 'need_recalc_filter_params'
                6  BINARY_SUBSCR    
                8  POP_JUMP_IF_TRUE     30  'to 30'
               10  LOAD_FAST                'self'
               12  LOAD_ATTR                global_params
               14  LOAD_STR                 'need_recalc_dataset_params'
               16  BINARY_SUBSCR    
               18  POP_JUMP_IF_TRUE     30  'to 30'

 L. 270        20  LOAD_GLOBAL              hasattr
               22  LOAD_FAST                'self'
               24  LOAD_STR                 'dataset_filtered'
               26  CALL_FUNCTION_2       2  '2 positional arguments'
               28  POP_JUMP_IF_TRUE    134  'to 134'
             30_0  COME_FROM            18  '18'
             30_1  COME_FROM             8  '8'

 L. 271        30  LOAD_FAST                'self'
               32  LOAD_METHOD              calculate_dataset
               34  CALL_METHOD_0         0  '0 positional arguments'
               36  STORE_FAST               'dataset'

 L. 272        38  LOAD_GLOBAL              filter_stack
               40  LOAD_FAST                'dataset'

 L. 273        42  LOAD_CONST               1
               44  LOAD_FAST                'self'
               46  LOAD_ATTR                filter_params
               48  LOAD_STR                 'median_filter_size'
               50  BINARY_SUBSCR    
               52  LOAD_FAST                'self'
               54  LOAD_ATTR                filter_params
               56  LOAD_STR                 'median_filter_size'
               58  BINARY_SUBSCR    
               60  BUILD_TUPLE_3         3 

 L. 274        62  LOAD_FAST                'self'
               64  LOAD_ATTR                filter_params

 L. 275        66  LOAD_STR                 'median_filter'
               68  BINARY_SUBSCR    

 L. 276        70  LOAD_FAST                'self'
               72  LOAD_ATTR                filter_params
               74  LOAD_STR                 'z_score'
               76  BINARY_SUBSCR    
               78  LOAD_CONST               ('stack', 'median_filter_size', 'median_filter', 'z_score')
               80  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
               82  LOAD_FAST                'self'
               84  STORE_ATTR               dataset_filtered

 L. 277        86  DELETE_FAST              'dataset'

 L. 278        88  LOAD_GLOBAL              np
               90  LOAD_ATTR                mean
               92  LOAD_FAST                'self'
               94  LOAD_ATTR                dataset_filtered
               96  LOAD_CONST               0
               98  LOAD_CONST               ('axis',)
              100  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              102  LOAD_FAST                'self'
              104  STORE_ATTR               mean_image

 L. 279       106  LOAD_GLOBAL              np
              108  LOAD_ATTR                max
              110  LOAD_FAST                'self'
              112  LOAD_ATTR                dataset_filtered
              114  LOAD_CONST               0
              116  LOAD_CONST               ('axis',)
              118  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              120  LOAD_FAST                'self'
              122  STORE_ATTR               max_image

 L. 281       124  LOAD_CONST               False
              126  LOAD_FAST                'self'
              128  LOAD_ATTR                global_params
              130  LOAD_STR                 'need_recalc_filter_params'
              132  STORE_SUBSCR     
            134_0  COME_FROM            28  '28'

 L. 282       134  LOAD_FAST                'self'
              136  LOAD_ATTR                dataset_filtered
              138  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM' instruction at offset 134_0

    def calculate_roi_extraction--- This code section failed: ---

 L. 290         0  LOAD_FAST                'self'
                2  LOAD_ATTR                global_params
                4  LOAD_STR                 'need_recalc_eigen_params'
                6  BINARY_SUBSCR    
                8  POP_JUMP_IF_TRUE     52  'to 52'
               10  LOAD_FAST                'self'
               12  LOAD_ATTR                global_params

 L. 291        14  LOAD_STR                 'need_recalc_roi_extraction_params'
               16  BINARY_SUBSCR    
               18  POP_JUMP_IF_TRUE     52  'to 52'
               20  LOAD_FAST                'self'
               22  LOAD_ATTR                global_params

 L. 292        24  LOAD_STR                 'need_recalc_box_parmas'
               26  BINARY_SUBSCR    
               28  POP_JUMP_IF_TRUE     52  'to 52'
               30  LOAD_FAST                'self'
               32  LOAD_ATTR                global_params
               34  LOAD_STR                 'need_recalc_dataset_params'
               36  BINARY_SUBSCR    
               38  POP_JUMP_IF_TRUE     52  'to 52'

 L. 293        40  LOAD_FAST                'self'
               42  LOAD_ATTR                global_params
               44  LOAD_STR                 'need_recalc_filter_params'
               46  BINARY_SUBSCR    
            48_50  POP_JUMP_IF_FALSE   552  'to 552'
             52_0  COME_FROM            38  '38'
             52_1  COME_FROM            28  '28'
             52_2  COME_FROM            18  '18'
             52_3  COME_FROM             8  '8'

 L. 294        52  LOAD_GLOBAL              int

 L. 295        54  LOAD_FAST                'self'
               56  LOAD_ATTR                box_params

 L. 296        58  LOAD_STR                 'total_num_spatial_boxes'
               60  BINARY_SUBSCR    
               62  LOAD_CONST               0.5
               64  BINARY_POWER     
               66  CALL_FUNCTION_1       1  '1 positional argument'
               68  LOAD_CONST               2
               70  BINARY_POWER     
               72  LOAD_FAST                'self'
               74  LOAD_ATTR                box_params

 L. 297        76  LOAD_STR                 'total_num_spatial_boxes'
               78  BINARY_SUBSCR    
               80  COMPARE_OP               ==
               82  POP_JUMP_IF_TRUE     92  'to 92'
               84  LOAD_ASSERT              AssertionError
               86  LOAD_STR                 'Please make sure Number of Spatial Boxes is a square number'
               88  CALL_FUNCTION_1       1  '1 positional argument'
               90  RAISE_VARARGS_1       1  'exception instance'
             92_0  COME_FROM            82  '82'

 L. 298     92_94  SETUP_EXCEPT        482  'to 482'

 L. 299        96  LOAD_GLOBAL              process_data
               98  LOAD_FAST                'self'
              100  LOAD_ATTR                global_params

 L. 300       102  LOAD_STR                 'num_threads'
              104  BINARY_SUBSCR    
              106  LOAD_CONST               False
              108  LOAD_STR                 ''

 L. 301       110  LOAD_FAST                'self'
              112  LOAD_ATTR                save_dir_path

 L. 302       114  LOAD_FAST                'self'
              116  LOAD_ATTR                global_params

 L. 303       118  LOAD_STR                 'save_intermediate_steps'
              120  BINARY_SUBSCR    

 L. 304       122  LOAD_CONST               False
              124  LOAD_STR                 ''

 L. 305       126  LOAD_FAST                'self'
              128  LOAD_METHOD              calculate_filters
              130  CALL_METHOD_0         0  '0 positional arguments'

 L. 306       132  LOAD_FAST                'self'
              134  LOAD_ATTR                global_params

 L. 307       136  LOAD_STR                 'need_recalc_eigen_params'
              138  BINARY_SUBSCR    
              140  UNARY_NOT        
              142  JUMP_IF_FALSE_OR_POP   158  'to 158'
              144  LOAD_FAST                'self'
              146  LOAD_ATTR                global_params
              148  LOAD_STR                 'save_intermediate_steps'
              150  BINARY_SUBSCR    
              152  JUMP_IF_FALSE_OR_POP   158  'to 158'
              154  LOAD_FAST                'self'
              156  LOAD_ATTR                eigen_vectors_exist
            158_0  COME_FROM           152  '152'
            158_1  COME_FROM           142  '142'

 L. 308       158  LOAD_CONST               True

 L. 309       160  LOAD_FAST                'self'
              162  LOAD_ATTR                box_params
              164  LOAD_STR                 'total_num_time_steps'
              166  BINARY_SUBSCR    

 L. 310       168  LOAD_FAST                'self'
              170  LOAD_ATTR                box_params

 L. 311       172  LOAD_STR                 'total_num_spatial_boxes'
              174  BINARY_SUBSCR    

 L. 312       176  LOAD_FAST                'self'
              178  LOAD_ATTR                box_params
              180  LOAD_STR                 'spatial_overlap'
              182  BINARY_SUBSCR    
              184  LOAD_CONST               2
              186  BINARY_FLOOR_DIVIDE
              188  LOAD_CONST               False

 L. 313       190  LOAD_CONST               False

 L. 314       192  LOAD_CONST               (1, 3, 3)

 L. 315       194  LOAD_CONST               False
              196  LOAD_CONST               False

 L. 316       198  LOAD_CONST               1
              200  LOAD_CONST               0
              202  LOAD_FAST                'self'
              204  LOAD_ATTR                eigen_params
              206  LOAD_STR                 'metric'
              208  BINARY_SUBSCR    

 L. 317       210  LOAD_FAST                'self'
              212  LOAD_ATTR                eigen_params
              214  LOAD_STR                 'knn'
              216  BINARY_SUBSCR    

 L. 318       218  LOAD_FAST                'self'
              220  LOAD_ATTR                eigen_params
              222  LOAD_STR                 'accuracy'
              224  BINARY_SUBSCR    

 L. 319       226  LOAD_FAST                'self'
              228  LOAD_ATTR                eigen_params
              230  LOAD_STR                 'connections'
              232  BINARY_SUBSCR    

 L. 320       234  LOAD_FAST                'self'
              236  LOAD_ATTR                eigen_params
              238  LOAD_STR                 'normalize_w_k'
              240  BINARY_SUBSCR    

 L. 321       242  LOAD_FAST                'self'
              244  LOAD_ATTR                eigen_params
              246  LOAD_STR                 'num_eig'
              248  BINARY_SUBSCR    

 L. 322       250  LOAD_FAST                'self'
              252  LOAD_ATTR                roi_extraction_params
              254  LOAD_STR                 'merge'
              256  BINARY_SUBSCR    

 L. 323       258  LOAD_FAST                'self'
              260  LOAD_ATTR                roi_extraction_params
              262  LOAD_STR                 'num_rois'
              264  BINARY_SUBSCR    

 L. 324       266  LOAD_FAST                'self'
              268  LOAD_ATTR                roi_extraction_params
              270  LOAD_STR                 'refinement'
              272  BINARY_SUBSCR    

 L. 325       274  LOAD_FAST                'self'
              276  LOAD_ATTR                roi_extraction_params

 L. 326       278  LOAD_STR                 'num_eigen_vector_select'
              280  BINARY_SUBSCR    

 L. 327       282  LOAD_FAST                'self'
              284  LOAD_ATTR                roi_extraction_params
              286  LOAD_STR                 'max_iter'
              288  BINARY_SUBSCR    

 L. 328       290  LOAD_FAST                'self'
              292  LOAD_ATTR                roi_extraction_params
              294  LOAD_STR                 'roi_size_min'
              296  BINARY_SUBSCR    

 L. 329       298  LOAD_FAST                'self'
              300  LOAD_ATTR                roi_extraction_params

 L. 330       302  LOAD_STR                 'fill_holes'
              304  BINARY_SUBSCR    

 L. 332       306  LOAD_FAST                'self'
              308  LOAD_ATTR                roi_extraction_params

 L. 333       310  LOAD_STR                 'elbow_threshold_method'
              312  BINARY_SUBSCR    

 L. 334       314  LOAD_FAST                'self'
              316  LOAD_ATTR                roi_extraction_params
              318  LOAD_STR                 'elbow_threshold_value'
              320  BINARY_SUBSCR    

 L. 335       322  LOAD_FAST                'self'
              324  LOAD_ATTR                roi_extraction_params

 L. 336       326  LOAD_STR                 'eigen_threshold_method'
              328  BINARY_SUBSCR    

 L. 337       330  LOAD_FAST                'self'
              332  LOAD_ATTR                roi_extraction_params

 L. 338       334  LOAD_STR                 'eigen_threshold_value'
              336  BINARY_SUBSCR    

 L. 339       338  LOAD_FAST                'self'
              340  LOAD_ATTR                roi_extraction_params
              342  LOAD_STR                 'merge_temporal_coef'
              344  BINARY_SUBSCR    

 L. 340       346  LOAD_FAST                'self'
              348  LOAD_ATTR                roi_extraction_params
              350  LOAD_STR                 'roi_size_max'
              352  BINARY_SUBSCR    
              354  LOAD_CONST               ('num_threads', 'test_images', 'test_output_dir', 'save_dir', 'save_intermediate_steps', 'load_data', 'data_path', 'image_data', 'eigen_vectors_already_generated', 'save_embedding_images', 'total_num_time_steps', 'total_num_spatial_boxes', 'spatial_overlap', 'filter', 'median_filter', 'median_filter_size', 'z_score', 'slice_stack', 'slice_every', 'slice_start', 'metric', 'knn', 'accuracy', 'connections', 'normalize_w_k', 'num_eig', 'merge', 'num_rois', 'refinement', 'num_eigen_vector_select', 'max_iter', 'roi_size_min', 'fill_holes', 'elbow_threshold_method', 'elbow_threshold_value', 'eigen_threshold_method', 'eigen_threshold_value', 'merge_temporal_coef', 'roi_size_max')
              356  CALL_FUNCTION_KW_39    39  '39 total positional and keyword args'
              358  LOAD_FAST                'self'
              360  STORE_ATTR               clusters

 L. 342       362  LOAD_CONST               False
              364  LOAD_FAST                'self'
              366  LOAD_ATTR                global_params
              368  LOAD_STR                 'need_recalc_eigen_params'
              370  STORE_SUBSCR     

 L. 343       372  LOAD_FAST                'self'
              374  LOAD_METHOD              save_rois
              376  LOAD_FAST                'self'
              378  LOAD_ATTR                clusters
              380  CALL_METHOD_1         1  '1 positional argument'
              382  POP_TOP          

 L. 344       384  LOAD_GLOBAL              print
              386  LOAD_STR                 'Calculating Time Traces:'
              388  CALL_FUNCTION_1       1  '1 positional argument'
              390  POP_TOP          

 L. 345       392  BUILD_LIST_0          0 
              394  LOAD_FAST                'self'
              396  STORE_ATTR               time_traces

 L. 346       398  SETUP_LOOP          456  'to 456'
              400  LOAD_FAST                'self'
              402  LOAD_ATTR                clusters
              404  GET_ITER         
              406  FOR_ITER            454  'to 454'
              408  STORE_FAST               'cluster'

 L. 348       410  LOAD_GLOBAL              reshape_to_2d_over_time
              412  LOAD_FAST                'self'
              414  LOAD_ATTR                dataset_filtered
              416  CALL_FUNCTION_1       1  '1 positional argument'
              418  STORE_FAST               'data_2d'

 L. 349       420  LOAD_GLOBAL              np
              422  LOAD_ATTR                average
              424  LOAD_FAST                'data_2d'
              426  LOAD_FAST                'cluster'
              428  BINARY_SUBSCR    
              430  LOAD_CONST               0
              432  LOAD_CONST               ('axis',)
              434  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              436  STORE_FAST               'time_trace'

 L. 350       438  LOAD_FAST                'self'
              440  LOAD_ATTR                time_traces
              442  LOAD_METHOD              append
              444  LOAD_FAST                'time_trace'
              446  CALL_METHOD_1         1  '1 positional argument'
              448  POP_TOP          
          450_452  JUMP_BACK           406  'to 406'
              454  POP_BLOCK        
            456_0  COME_FROM_LOOP      398  '398'

 L. 351       456  LOAD_FAST                'self'
              458  LOAD_METHOD              gen_roi_display_variables
              460  CALL_METHOD_0         0  '0 positional arguments'
              462  POP_TOP          

 L. 352       464  LOAD_FAST                'self'
              466  LOAD_METHOD              calculate_time_traces
              468  CALL_METHOD_0         0  '0 positional arguments'
              470  POP_TOP          

 L. 354       472  LOAD_CONST               True
              474  LOAD_FAST                'self'
              476  STORE_ATTR               rois_loaded
              478  POP_BLOCK        
              480  JUMP_FORWARD        552  'to 552'
            482_0  COME_FROM_EXCEPT     92  '92'

 L. 355       482  DUP_TOP          
              484  LOAD_GLOBAL              Exception
              486  COMPARE_OP               exception-match
          488_490  POP_JUMP_IF_FALSE   550  'to 550'
              492  POP_TOP          
              494  STORE_FAST               'e'
              496  POP_TOP          
              498  SETUP_FINALLY       538  'to 538'

 L. 356       500  LOAD_CONST               False
              502  LOAD_FAST                'self'
              504  LOAD_ATTR                global_params
              506  LOAD_STR                 'need_recalc_eigen_params'
              508  STORE_SUBSCR     

 L. 357       510  LOAD_GLOBAL              logger1
              512  LOAD_METHOD              error
              514  LOAD_FAST                'e'
              516  CALL_METHOD_1         1  '1 positional argument'
              518  POP_TOP          

 L. 358       520  LOAD_GLOBAL              print
              522  LOAD_STR                 'Please try again there was an internal error in the roi extraction process'
              524  CALL_FUNCTION_1       1  '1 positional argument'
              526  POP_TOP          

 L. 359       528  LOAD_GLOBAL              AssertionError
              530  CALL_FUNCTION_0       0  '0 positional arguments'
              532  RAISE_VARARGS_1       1  'exception instance'
              534  POP_BLOCK        
              536  LOAD_CONST               None
            538_0  COME_FROM_FINALLY   498  '498'
              538  LOAD_CONST               None
              540  STORE_FAST               'e'
              542  DELETE_FAST              'e'
              544  END_FINALLY      
              546  POP_EXCEPT       
              548  JUMP_FORWARD        552  'to 552'
            550_0  COME_FROM           488  '488'
              550  END_FINALLY      
            552_0  COME_FROM           548  '548'
            552_1  COME_FROM           480  '480'
            552_2  COME_FROM            48  '48'

Parse error at or near `COME_FROM' instruction at offset 552_1

    def gen_roi_display_variables(self):
        cluster_list_2d_cord = [pixel_num_to_2d_cord(x, volume_shape=(self.dataset_filtered.shape)) for x in self.clusters]
        self.cluster_max_cord_list = [np.max(x, axis=1) for x in cluster_list_2d_cord]
        self.cluster_min_cord_list = [np.min(x, axis=1) for x in cluster_list_2d_cord]
        self.pixel_with_rois_flat = np.zeros([
         self.dataset_filtered.shape[1] * self.dataset_filtered.shape[2]])
        self.pixel_with_rois_color_flat = np.zeros([
         self.dataset_filtered.shape[1] * self.dataset_filtered.shape[2], 3])
        for num, cluster in enumerate(self.clusters):
            cur_color = self.color_list[(num % len(self.color_list))]
            self.pixel_with_rois_flat[cluster] = num + 1
            self.pixel_with_rois_color_flat[cluster] = cur_color

        edge_roi_image = feature.canny(np.reshape(self.pixel_with_rois_flat, [
         self.dataset_filtered.shape[1],
         self.dataset_filtered.shape[2]]))
        self.edge_roi_image_flat = np.reshape(edge_roi_image, [-1, 1]) * 255
        self.pixel_with_rois_color = np.reshape(self.pixel_with_rois_color_flat, [
         self.dataset_filtered.shape[1],
         self.dataset_filtered.shape[2], 3])
        try:
            self.eigen_norm_image = np.asarray(Image.open(os.path.join(self.save_dir_path, 'embedding_norm_images/embedding_norm_image.png')))
        except:
            print("Can't generate eigen Norm image please try again")

    def calculate_time_traces(self):
        self.time_traces = [[]] * len(self.clusters)
        for cluster in range(len(self.clusters)):
            self.calculate_time_trace(cluster + 1)

        if os.path.isdir(self.save_dir_path):
            pickle_save((self.time_traces), 'time_traces', output_directory=(self.save_dir_path))
        self.gen_roi_display_variables()
        self.rois_loaded = True

    def calculate_time_trace(self, roi_num):
        """
        Calculates a time trace for a certain ROI and save to time trace list
        Parameters
        ----------
        roi_num roi to calculate for

        Returns
        -------

        """
        cluster = self.clusters[(roi_num - 1)]
        data_2d = reshape_to_2d_over_time(self.dataset_filtered)
        time_trace = np.average((data_2d[cluster]), axis=0)
        self.time_traces[roi_num - 1] = time_trace
        if os.path.isdir(self.save_dir_path):
            pickle_save((self.time_traces), 'time_traces', output_directory=(self.save_dir_path))

    def get_time_trace(self, num):
        return self.time_traces[(num - 1)]