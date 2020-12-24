# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\drgpom\methods\pom.py
# Compiled at: 2020-04-08 07:54:09
# Size of source mod 2**32: 71672 bytes
"""
Created on Mon Feb 08 12:14:25 2016
Functions for running a population of models loop

@author: Oliver Britton
"""
import os, sys, numpy as np, pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(style='whitegrid')
import multiprocessing as mp, collections, datetime, pickle, time
from functools import partial
from IPython.display import clear_output
from .biomarkers import neuron_biomarkers as nb
from .biomarkers import davidson_biomarkers as db
from . import simulation_helpers as sh
from neuron import h
import neuron
from . import loadneuron as ln
ln.load_neuron_mechanisms(verbose=True)

def load_parameters(filename):
    parameters = pd.read_csv(filename, sep=',', header=None)
    return parameters


def read_trace(filename, skiprows=0):
    data = np.loadtxt(filename, skiprows=skiprows)
    trace = {'t':data[:, 0],  'v':data[:, 1]}
    return trace


load_trace = read_trace

def save_trace(trace, filename):
    """ TODO - make this able to handle current recordings - e.g. save as csv with column headers
    using pandas
    """
    with open(filename, 'wb') as (f):
        pickle.dump(trace, f)


def plot_trace(filename):
    data = read_trace(filename)
    plt.plot(data['t'], data['v'])


def load(filename):
    with open(filename, 'rb') as (f):
        pom = pickle.load(f)
    return pom


def make_pom_name(name):
    date = time.strftime('%d%m%y')
    return '{}_{}'.format(name, date)


def allowed_save_types():
    return ('fig', 'trace', 'both', 'all', 'none', None)


def process_save_type(save_type):
    if save_type in ('fig', 'trace'):
        return [
         save_type]
    if save_type == 'both':
        return [
         'fig', 'trace']
    if save_type == 'all':
        return [
         'fig', 'trace']
    if save_type == None or save_type == 'none':
        return []
    raise ValueError('save_type {} not found'.format(save_type))


def get_function_args(function):
    """ Just a reminder of how to get the args of a function """
    import inspect
    args = inspect.getargspec(function)[0]
    return args


def set_dataframe_types(df):
    """
    Set all columns in a pd.DataFrame where all data have the same type to that type
    """
    typed_df = df.copy()
    for column in typed_df:
        types = [type(i) for i in typed_df[column]]
        if all([i == types[0] for i in types]):
            typed_df[column] = typed_df[column].astype(types[0])

    return typed_df


def dump_exception(e, filename='debug.txt'):
    with open(filename, 'w') as (f):
        f.write(str(e))


def simulate_iclamp--- This code section failed: ---

 L. 193         0  LOAD_CONST               0
                2  LOAD_CONST               None
                4  IMPORT_NAME              neuron
                6  STORE_FAST               'neuron'

 L. 194         8  LOAD_CONST               0
               10  LOAD_CONST               ('h',)
               12  IMPORT_NAME              neuron
               14  IMPORT_FROM              h
               16  STORE_FAST               'h'
               18  POP_TOP          

 L. 195        20  LOAD_STR                 'iclamp'
               22  STORE_FAST               'sim_type'

 L. 199        24  LOAD_FAST                'stim_func'
               26  LOAD_STR                 'h.IClamp'
               28  COMPARE_OP               ==
               30  POP_JUMP_IF_FALSE    40  'to 40'

 L. 200        32  LOAD_FAST                'h'
               34  LOAD_ATTR                IClamp
               36  STORE_FAST               'stim_func'
               38  JUMP_FORWARD         70  'to 70'
             40_0  COME_FROM            30  '30'

 L. 201        40  LOAD_FAST                'stim_func'
               42  LOAD_STR                 'h.IRamp'
               44  COMPARE_OP               ==
               46  POP_JUMP_IF_FALSE    56  'to 56'

 L. 202        48  LOAD_FAST                'h'
               50  LOAD_ATTR                IRamp
               52  STORE_FAST               'stim_func'
               54  JUMP_FORWARD         70  'to 70'
             56_0  COME_FROM            46  '46'

 L. 204        56  LOAD_GLOBAL              ValueError
               58  LOAD_STR                 'stim_func: {} not found'
               60  LOAD_METHOD              format
               62  LOAD_FAST                'stim_func'
               64  CALL_METHOD_1         1  '1 positional argument'
               66  CALL_FUNCTION_1       1  '1 positional argument'
               68  RAISE_VARARGS_1       1  'exception instance'
             70_0  COME_FROM            54  '54'
             70_1  COME_FROM            38  '38'

 L. 207        70  BUILD_MAP_0           0 
               72  STORE_FAST               'results'

 L. 208        74  LOAD_FAST                'sim_id'
               76  LOAD_FAST                'results'
               78  LOAD_STR                 'sim_id'
               80  STORE_SUBSCR     

 L. 209        82  LOAD_FAST                'biomarker_names'
               84  STORE_FAST               'results_names'

 L. 210        86  SETUP_LOOP          110  'to 110'
               88  LOAD_FAST                'results_names'
               90  GET_ITER         
               92  FOR_ITER            108  'to 108'
               94  STORE_FAST               'name'

 L. 211        96  LOAD_GLOBAL              np
               98  LOAD_ATTR                nan
              100  LOAD_FAST                'results'
              102  LOAD_FAST                'name'
              104  STORE_SUBSCR     
              106  JUMP_BACK            92  'to 92'
              108  POP_BLOCK        
            110_0  COME_FROM_LOOP       86  '86'

 L. 212       110  LOAD_GLOBAL              np
              112  LOAD_ATTR                nan
              114  LOAD_FAST                'results'
              116  LOAD_STR                 'Firing pattern'
              118  STORE_SUBSCR     

 L. 217       120  LOAD_GLOBAL              sh
              122  LOAD_ATTR                build_model
              124  LOAD_FAST                'mechanisms'
              126  LOAD_FAST                'mechanism_names'
              128  LOAD_CONST               None
              130  LOAD_CONST               True
              132  LOAD_CONST               ('mechanisms', 'mechanism_names', 'conductances', 'mechanism_is_full_parameter_name')
              134  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              136  STORE_FAST               'cell'

 L. 218       138  LOAD_FAST                'celsius'
              140  LOAD_FAST                'h'
              142  STORE_ATTR               celsius

 L. 222       144  LOAD_GLOBAL              sh
              146  LOAD_METHOD              get_dynamic_ion_mechanisms
              148  CALL_METHOD_0         0  '0 positional arguments'
              150  STORE_FAST               'ion_mechanisms'

 L. 223       152  SETUP_LOOP          188  'to 188'
              154  LOAD_FAST                'ion_mechanisms'
              156  GET_ITER         
            158_0  COME_FROM           168  '168'
              158  FOR_ITER            186  'to 186'
              160  STORE_FAST               'ion'

 L. 224       162  LOAD_FAST                'ion'
              164  LOAD_FAST                'ions'
              166  COMPARE_OP               in
              168  POP_JUMP_IF_FALSE   158  'to 158'

 L. 225       170  LOAD_FAST                'cell'
              172  LOAD_METHOD              insert
              174  LOAD_FAST                'ion_mechanisms'
              176  LOAD_FAST                'ion'
              178  BINARY_SUBSCR    
              180  CALL_METHOD_1         1  '1 positional argument'
              182  POP_TOP          
              184  JUMP_BACK           158  'to 158'
              186  POP_BLOCK        
            188_0  COME_FROM_LOOP      152  '152'

 L. 231       188  LOAD_FAST                'ions'

 L. 232       190  LOAD_FAST                't_stop'

 L. 233       192  LOAD_FAST                'dur'

 L. 234       194  LOAD_FAST                'delay'

 L. 235       196  LOAD_FAST                'interval'

 L. 236       198  LOAD_FAST                'num_stims'

 L. 237       200  LOAD_FAST                'stim_func'
              202  LOAD_CONST               ('ions', 't_stop', 'dur', 'delay', 'interval', 'num_stims', 'stim_func')
              204  BUILD_CONST_KEY_MAP_7     7 
              206  STORE_FAST               'sim_kwargs'

 L. 242       208  LOAD_GLOBAL              nb
              210  LOAD_ATTR                calculate_rheobase
              212  LOAD_FAST                'cell'
              214  LOAD_CONST               0.1
              216  LOAD_CONST               5.0

 L. 243       218  LOAD_CONST               False
              220  LOAD_FAST                'sim_kwargs'
              222  LOAD_CONST               ('amp_step', 'amp_max', 'make_plot', 'sim_kwargs')
              224  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              226  STORE_FAST               'rheobase'

 L. 247       228  LOAD_FAST                'rheobase'
              230  LOAD_GLOBAL              nb
              232  LOAD_ATTR                RHEO_FAIL
              234  COMPARE_OP               is
          236_238  POP_JUMP_IF_FALSE   260  'to 260'

 L. 248       240  LOAD_GLOBAL              nb
              242  LOAD_ATTR                calculate_rheobase
              244  LOAD_FAST                'cell'
              246  LOAD_CONST               1.0
              248  LOAD_CONST               50.0

 L. 249       250  LOAD_CONST               False
              252  LOAD_FAST                'sim_kwargs'
              254  LOAD_CONST               ('amp_step', 'amp_max', 'make_plot', 'sim_kwargs')
              256  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              258  STORE_FAST               'rheobase'
            260_0  COME_FROM           236  '236'

 L. 252       260  LOAD_FAST                'rheobase'
              262  LOAD_GLOBAL              nb
              264  LOAD_ATTR                RHEO_FAIL
              266  COMPARE_OP               is-not
          268_270  POP_JUMP_IF_FALSE   278  'to 278'

 L. 253       272  LOAD_CONST               True
              274  STORE_FAST               'rheobase_found'
              276  JUMP_FORWARD        282  'to 282'
            278_0  COME_FROM           268  '268'

 L. 255       278  LOAD_CONST               False
              280  STORE_FAST               'rheobase_found'
            282_0  COME_FROM           276  '276'

 L. 258       282  LOAD_FAST                'rheobase_found'
          284_286  POP_JUMP_IF_TRUE    308  'to 308'
              288  LOAD_FAST                'amp'
              290  LOAD_CONST               None
              292  COMPARE_OP               is-not
          294_296  POP_JUMP_IF_TRUE    308  'to 308'
              298  LOAD_STR                 'rheobase_sim_for_stim_amp'
              300  LOAD_FAST                'flags'
              302  COMPARE_OP               in
          304_306  POP_JUMP_IF_FALSE  1080  'to 1080'
            308_0  COME_FROM           294  '294'
            308_1  COME_FROM           284  '284'

 L. 259       308  BUILD_LIST_0          0 
              310  STORE_FAST               'stims'

 L. 260       312  SETUP_LOOP          440  'to 440'
              314  LOAD_GLOBAL              range
              316  LOAD_FAST                'num_stims'
              318  CALL_FUNCTION_1       1  '1 positional argument'
              320  GET_ITER         
              322  FOR_ITER            438  'to 438'
              324  STORE_FAST               'stim_idx'

 L. 261       326  LOAD_FAST                'stims'
              328  LOAD_METHOD              append
              330  LOAD_FAST                'stim_func'
              332  LOAD_CONST               0.5
              334  LOAD_FAST                'cell'
              336  LOAD_CONST               ('sec',)
              338  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              340  CALL_METHOD_1         1  '1 positional argument'
              342  POP_TOP          

 L. 262       344  LOAD_FAST                'dur'
              346  LOAD_FAST                'stims'
              348  LOAD_CONST               -1
              350  BINARY_SUBSCR    
              352  STORE_ATTR               dur

 L. 263       354  LOAD_FAST                'delay'
              356  LOAD_FAST                'stim_idx'
              358  LOAD_FAST                'dur'
              360  LOAD_FAST                'interval'
              362  BINARY_ADD       
              364  BINARY_MULTIPLY  
              366  BINARY_ADD       
              368  LOAD_FAST                'stims'
              370  LOAD_CONST               -1
              372  BINARY_SUBSCR    
              374  STORE_ATTR               delay

 L. 265       376  LOAD_FAST                'amp'
              378  LOAD_CONST               None
              380  COMPARE_OP               is
          382_384  POP_JUMP_IF_FALSE   424  'to 424'

 L. 267       386  LOAD_STR                 'rheobase_sim_for_stim_amp'
              388  LOAD_FAST                'flags'
              390  COMPARE_OP               not-in
          392_394  POP_JUMP_IF_FALSE   408  'to 408'

 L. 268       396  LOAD_FAST                'rheobase'
              398  LOAD_FAST                'stims'
              400  LOAD_CONST               -1
              402  BINARY_SUBSCR    
              404  STORE_ATTR               amp
              406  JUMP_FORWARD        422  'to 422'
            408_0  COME_FROM           392  '392'

 L. 271       408  LOAD_FAST                'flags'
              410  LOAD_STR                 'rheobase_sim_for_stim_amp'
              412  BINARY_SUBSCR    
              414  LOAD_FAST                'stims'
              416  LOAD_CONST               -1
              418  BINARY_SUBSCR    
              420  STORE_ATTR               amp
            422_0  COME_FROM           406  '406'
              422  JUMP_BACK           322  'to 322'
            424_0  COME_FROM           382  '382'

 L. 274       424  LOAD_FAST                'amp'
              426  LOAD_FAST                'stims'
              428  LOAD_CONST               -1
              430  BINARY_SUBSCR    
              432  STORE_ATTR               amp
          434_436  JUMP_BACK           322  'to 322'
              438  POP_BLOCK        
            440_0  COME_FROM_LOOP      312  '312'

 L. 276       440  LOAD_GLOBAL              sh
              442  LOAD_ATTR                set_vt
              444  LOAD_FAST                'cell'
              446  LOAD_CONST               ('cell',)
              448  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              450  UNPACK_SEQUENCE_2     2 
              452  STORE_FAST               'v'
              454  STORE_FAST               't'

 L. 277       456  LOAD_GLOBAL              sh
              458  LOAD_METHOD              record_currents
              460  LOAD_FAST                'cell'
              462  LOAD_FAST                'outputs'
              464  CALL_METHOD_2         2  '2 positional arguments'
              466  STORE_FAST               'vectors'

 L. 279       468  LOAD_FAST                'h'
              470  LOAD_METHOD              finitialize
              472  LOAD_FAST                'v_init'
              474  CALL_METHOD_1         1  '1 positional argument'
              476  POP_TOP          

 L. 280       478  LOAD_FAST                'neuron'
              480  LOAD_METHOD              run
              482  LOAD_FAST                't_stop'
              484  CALL_METHOD_1         1  '1 positional argument'
              486  POP_TOP          

 L. 283       488  LOAD_GLOBAL              np
              490  LOAD_METHOD              array
              492  LOAD_FAST                'v'
              494  CALL_METHOD_1         1  '1 positional argument'
              496  LOAD_GLOBAL              np
              498  LOAD_METHOD              array
              500  LOAD_FAST                't'
              502  CALL_METHOD_1         1  '1 positional argument'
              504  ROT_TWO          
              506  STORE_FAST               'v'
              508  STORE_FAST               't'

 L. 287       510  LOAD_GLOBAL              sh
              512  LOAD_METHOD              recast_recorded_currents
              514  LOAD_FAST                'vectors'
              516  CALL_METHOD_1         1  '1 positional argument'
              518  STORE_FAST               'vectors'

 L. 290       520  LOAD_FAST                'sampling_freq'
              522  LOAD_CONST               20000
              524  COMPARE_OP               ==
          526_528  POP_JUMP_IF_FALSE   630  'to 630'

 L. 295       530  LOAD_FAST                't'
              532  LOAD_CONST               None
              534  LOAD_CONST               None
              536  LOAD_CONST               2
              538  BUILD_SLICE_3         3 
              540  BINARY_SUBSCR    
              542  STORE_FAST               't'

 L. 295       544  LOAD_FAST                'v'
              546  LOAD_CONST               None
              548  LOAD_CONST               None
              550  LOAD_CONST               2
              552  BUILD_SLICE_3         3 
              554  BINARY_SUBSCR    
              556  STORE_FAST               'v'

 L. 298       558  SETUP_LOOP          638  'to 638'
              560  LOAD_FAST                'vectors'
              562  LOAD_METHOD              items
              564  CALL_METHOD_0         0  '0 positional arguments'
              566  GET_ITER         
              568  FOR_ITER            626  'to 626'
              570  UNPACK_SEQUENCE_2     2 
              572  STORE_FAST               'cur_name'
              574  STORE_FAST               'cur'

 L. 299       576  SETUP_LOOP          622  'to 622'
              578  LOAD_FAST                'cur'
              580  GET_ITER         
              582  FOR_ITER            620  'to 620'
              584  STORE_FAST               'cur_component'

 L. 300       586  LOAD_FAST                'vectors'
              588  LOAD_FAST                'cur_name'
              590  BINARY_SUBSCR    
              592  LOAD_FAST                'cur_component'
              594  BINARY_SUBSCR    
              596  LOAD_CONST               None
              598  LOAD_CONST               None
              600  LOAD_CONST               2
              602  BUILD_SLICE_3         3 
              604  BINARY_SUBSCR    
              606  LOAD_FAST                'vectors'
              608  LOAD_FAST                'cur_name'
              610  BINARY_SUBSCR    
              612  LOAD_FAST                'cur_component'
              614  STORE_SUBSCR     
          616_618  JUMP_BACK           582  'to 582'
              620  POP_BLOCK        
            622_0  COME_FROM_LOOP      576  '576'
          622_624  JUMP_BACK           568  'to 568'
              626  POP_BLOCK        
              628  JUMP_FORWARD        638  'to 638'
            630_0  COME_FROM           526  '526'

 L. 304       630  LOAD_GLOBAL              ValueError
              632  LOAD_STR                 'Sampling frequencies other than 20 kHz not supported yet.'
              634  CALL_FUNCTION_1       1  '1 positional argument'
              636  RAISE_VARARGS_1       1  'exception instance'
            638_0  COME_FROM           628  '628'
            638_1  COME_FROM_LOOP      558  '558'

 L. 307       638  LOAD_GLOBAL              nb
              640  LOAD_METHOD              split_trace_into_aps
              642  LOAD_FAST                't'
              644  LOAD_FAST                'v'
              646  CALL_METHOD_2         2  '2 positional arguments'
              648  STORE_FAST               'traces'

 L. 309       650  LOAD_GLOBAL              nb
              652  LOAD_ATTR                calculate_simple_biomarkers
              654  LOAD_FAST                'traces'
              656  LOAD_FAST                'cell'
              658  LOAD_STR                 'remove'
              660  LOAD_CONST               ('how_to_handle_nans',)
              662  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              664  STORE_FAST               'biomarkers'

 L. 311       666  SETUP_EXCEPT        770  'to 770'

 L. 313       668  SETUP_LOOP          766  'to 766'
              670  LOAD_FAST                'flags'
              672  GET_ITER         
            674_0  COME_FROM           684  '684'
              674  FOR_ITER            764  'to 764'
              676  STORE_FAST               'flag'

 L. 315       678  LOAD_FAST                'flag'
              680  LOAD_STR                 'ramp_threshold_sim_for_width'
              682  COMPARE_OP               ==
          684_686  POP_JUMP_IF_FALSE   674  'to 674'

 L. 316       688  LOAD_FAST                'flags'
              690  LOAD_FAST                'flag'
              692  BINARY_SUBSCR    
              694  STORE_FAST               '_threshold'

 L. 317       696  LOAD_GLOBAL              nb
              698  LOAD_ATTR                average_biomarker_values

 L. 318       700  LOAD_GLOBAL              nb
              702  LOAD_ATTR                calculate_ap_width
              704  LOAD_FAST                'traces'
              706  LOAD_CONST               0.0
              708  LOAD_FAST                '_threshold'
              710  LOAD_STR                 'voltage'
              712  LOAD_CONST               ('alpha', 'threshold', 'method')
              714  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'

 L. 319       716  LOAD_STR                 'remove'
              718  LOAD_CONST               ('how_to_handle_nans',)
              720  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              722  LOAD_FAST                'biomarkers'
              724  LOAD_STR                 'APFullWidth'
              726  STORE_SUBSCR     

 L. 320       728  LOAD_GLOBAL              nb
              730  LOAD_ATTR                average_biomarker_values

 L. 321       732  LOAD_GLOBAL              nb
              734  LOAD_ATTR                calculate_ap_width
              736  LOAD_FAST                'traces'
              738  LOAD_CONST               0.5
              740  LOAD_FAST                '_threshold'
              742  LOAD_STR                 'voltage'
              744  LOAD_CONST               ('alpha', 'threshold', 'method')
              746  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'

 L. 322       748  LOAD_STR                 'remove'
              750  LOAD_CONST               ('how_to_handle_nans',)
              752  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              754  LOAD_FAST                'biomarkers'
              756  LOAD_STR                 'APHalfWidth'
              758  STORE_SUBSCR     
          760_762  JUMP_BACK           674  'to 674'
              764  POP_BLOCK        
            766_0  COME_FROM_LOOP      668  '668'
              766  POP_BLOCK        
              768  JUMP_FORWARD        866  'to 866'
            770_0  COME_FROM_EXCEPT    666  '666'

 L. 324       770  DUP_TOP          
              772  LOAD_GLOBAL              Exception
              774  COMPARE_OP               exception-match
          776_778  POP_JUMP_IF_FALSE   864  'to 864'
              780  POP_TOP          
              782  STORE_FAST               'e'
              784  POP_TOP          
              786  SETUP_FINALLY       852  'to 852'

 L. 325       788  LOAD_GLOBAL              open
              790  LOAD_STR                 '{}_{}.txt'
              792  LOAD_METHOD              format
              794  LOAD_FAST                'sim_id'
              796  LOAD_FAST                'stim_func'
              798  CALL_METHOD_2         2  '2 positional arguments'
              800  LOAD_STR                 'w'
              802  CALL_FUNCTION_2       2  '2 positional arguments'
              804  SETUP_WITH          842  'to 842'
              806  STORE_FAST               'f'

 L. 326       808  LOAD_FAST                'f'
              810  LOAD_METHOD              write
              812  LOAD_GLOBAL              str
              814  LOAD_FAST                'e'
              816  CALL_FUNCTION_1       1  '1 positional argument'
              818  CALL_METHOD_1         1  '1 positional argument'
              820  POP_TOP          

 L. 327       822  LOAD_STR                 'FAILURE'
              824  LOAD_FAST                'biomarkers'
              826  LOAD_STR                 'APFullWidth'
              828  STORE_SUBSCR     

 L. 328       830  LOAD_STR                 'FAILURE'
              832  LOAD_FAST                'biomarkers'
              834  LOAD_STR                 'APHalfWidth'
              836  STORE_SUBSCR     
              838  POP_BLOCK        
              840  LOAD_CONST               None
            842_0  COME_FROM_WITH      804  '804'
              842  WITH_CLEANUP_START
              844  WITH_CLEANUP_FINISH
              846  END_FINALLY      
              848  POP_BLOCK        
              850  LOAD_CONST               None
            852_0  COME_FROM_FINALLY   786  '786'
              852  LOAD_CONST               None
              854  STORE_FAST               'e'
              856  DELETE_FAST              'e'
              858  END_FINALLY      
              860  POP_EXCEPT       
              862  JUMP_FORWARD        866  'to 866'
            864_0  COME_FROM           776  '776'
              864  END_FINALLY      
            866_0  COME_FROM           862  '862'
            866_1  COME_FROM           768  '768'

 L. 335       866  LOAD_FAST                'num_stims'
              868  LOAD_CONST               1
              870  COMPARE_OP               ==
          872_874  POP_JUMP_IF_FALSE   998  'to 998'

 L. 336       876  LOAD_FAST                'delay'
              878  STORE_FAST               'stim_start'

 L. 337       880  LOAD_FAST                'delay'
              882  LOAD_FAST                'dur'
              884  BINARY_ADD       
              886  STORE_FAST               'stim_end'

 L. 338       888  SETUP_EXCEPT        912  'to 912'

 L. 339       890  LOAD_GLOBAL              nb
              892  LOAD_METHOD              determine_firing_pattern
              894  LOAD_FAST                'traces'
              896  LOAD_FAST                'stim_start'
              898  LOAD_FAST                'stim_end'
              900  CALL_METHOD_3         3  '3 positional arguments'
              902  LOAD_FAST                'biomarkers'
              904  LOAD_STR                 'Firing pattern'
              906  STORE_SUBSCR     
              908  POP_BLOCK        
              910  JUMP_FORWARD        996  'to 996'
            912_0  COME_FROM_EXCEPT    888  '888'

 L. 340       912  DUP_TOP          
              914  LOAD_GLOBAL              Exception
              916  COMPARE_OP               exception-match
          918_920  POP_JUMP_IF_FALSE   994  'to 994'
              922  POP_TOP          
              924  STORE_FAST               'e'
              926  POP_TOP          
              928  SETUP_FINALLY       982  'to 982'

 L. 341       930  LOAD_GLOBAL              open
              932  LOAD_STR                 '{}_{}'
              934  LOAD_METHOD              format
              936  LOAD_FAST                'sim_id'
              938  LOAD_GLOBAL              str
              940  LOAD_FAST                'stim_func'
              942  CALL_FUNCTION_1       1  '1 positional argument'
              944  CALL_METHOD_2         2  '2 positional arguments'
              946  LOAD_STR                 'w'
              948  CALL_FUNCTION_2       2  '2 positional arguments'
              950  SETUP_WITH          972  'to 972'
              952  STORE_FAST               'f'

 L. 342       954  LOAD_FAST                'f'
              956  LOAD_METHOD              write
              958  LOAD_GLOBAL              str
              960  LOAD_FAST                'e'
              962  CALL_FUNCTION_1       1  '1 positional argument'
              964  CALL_METHOD_1         1  '1 positional argument'
              966  POP_TOP          
              968  POP_BLOCK        
              970  LOAD_CONST               None
            972_0  COME_FROM_WITH      950  '950'
              972  WITH_CLEANUP_START
              974  WITH_CLEANUP_FINISH
              976  END_FINALLY      
              978  POP_BLOCK        
              980  LOAD_CONST               None
            982_0  COME_FROM_FINALLY   928  '928'
              982  LOAD_CONST               None
              984  STORE_FAST               'e'
              986  DELETE_FAST              'e'
              988  END_FINALLY      
              990  POP_EXCEPT       
              992  JUMP_FORWARD        996  'to 996'
            994_0  COME_FROM           918  '918'
              994  END_FINALLY      
            996_0  COME_FROM           992  '992'
            996_1  COME_FROM           910  '910'
              996  JUMP_FORWARD       1012  'to 1012'
            998_0  COME_FROM           872  '872'

 L. 344       998  LOAD_STR                 "Couldn't determine as num stims = {}, not 1"
             1000  LOAD_METHOD              format
             1002  LOAD_FAST                'num_stims'
             1004  CALL_METHOD_1         1  '1 positional argument'
             1006  LOAD_FAST                'biomarkers'
             1008  LOAD_STR                 'Firing pattern'
             1010  STORE_SUBSCR     
           1012_0  COME_FROM           996  '996'

 L. 346      1012  SETUP_LOOP         1040  'to 1040'
             1014  LOAD_FAST                'biomarkers'
             1016  GET_ITER         
             1018  FOR_ITER           1038  'to 1038'
             1020  STORE_FAST               'result'

 L. 347      1022  LOAD_FAST                'biomarkers'
             1024  LOAD_FAST                'result'
             1026  BINARY_SUBSCR    
             1028  LOAD_FAST                'results'
             1030  LOAD_FAST                'result'
             1032  STORE_SUBSCR     
         1034_1036  JUMP_BACK          1018  'to 1018'
             1038  POP_BLOCK        
           1040_0  COME_FROM_LOOP     1012  '1012'

 L. 350      1040  LOAD_FAST                't'
             1042  LOAD_FAST                'v'
             1044  LOAD_CONST               ('t', 'v')
             1046  BUILD_CONST_KEY_MAP_2     2 
             1048  STORE_FAST               'trace'

 L. 351      1050  SETUP_LOOP         1104  'to 1104'
             1052  LOAD_FAST                'vectors'
             1054  GET_ITER         
             1056  FOR_ITER           1076  'to 1076'
             1058  STORE_FAST               'vector'

 L. 352      1060  LOAD_FAST                'vectors'
             1062  LOAD_FAST                'vector'
             1064  BINARY_SUBSCR    
             1066  LOAD_FAST                'trace'
             1068  LOAD_FAST                'vector'
             1070  STORE_SUBSCR     
         1072_1074  JUMP_BACK          1056  'to 1056'
             1076  POP_BLOCK        
             1078  JUMP_FORWARD       1104  'to 1104'
           1080_0  COME_FROM           304  '304'

 L. 354      1080  LOAD_FAST                'rheobase_found'
             1082  LOAD_CONST               False
             1084  COMPARE_OP               ==
         1086_1088  POP_JUMP_IF_FALSE  1096  'to 1096'

 L. 355      1090  LOAD_CONST               None
             1092  STORE_FAST               'trace'
             1094  JUMP_FORWARD       1104  'to 1104'
           1096_0  COME_FROM          1086  '1086'

 L. 358      1096  LOAD_GLOBAL              ValueError
             1098  LOAD_STR                 'rheobase_found is not valid'
             1100  CALL_FUNCTION_1       1  '1 positional argument'
             1102  RAISE_VARARGS_1       1  'exception instance'
           1104_0  COME_FROM          1094  '1094'
           1104_1  COME_FROM          1078  '1078'
           1104_2  COME_FROM_LOOP     1050  '1050'

 L. 361      1104  LOAD_GLOBAL              sh
             1106  LOAD_ATTR                simulation
             1108  LOAD_CONST               0.0
             1110  LOAD_CONST               3000
             1112  LOAD_CONST               0
             1114  LOAD_CONST               0
             1116  LOAD_CONST               1
             1118  LOAD_CONST               3000.0
             1120  LOAD_CONST               False
             1122  LOAD_FAST                'cell'
             1124  LOAD_CONST               ('amp', 'dur', 'delay', 'interval', 'num_stims', 't_stop', 'make_plot', 'model')
             1126  CALL_FUNCTION_KW_8     8  '8 total positional and keyword args'
             1128  STORE_FAST               'rmp_out'

 L. 364      1130  LOAD_GLOBAL              nb
             1132  LOAD_METHOD              SplitTraceIntoAPs
             1134  LOAD_FAST                'rmp_out'
             1136  LOAD_STR                 't'
             1138  BINARY_SUBSCR    
             1140  LOAD_FAST                'rmp_out'
             1142  LOAD_STR                 'v'
             1144  BINARY_SUBSCR    
             1146  CALL_METHOD_2         2  '2 positional arguments'
             1148  STORE_FAST               'rmp_traces'

 L. 366      1150  LOAD_GLOBAL              np
             1152  LOAD_METHOD              mean
             1154  LOAD_GLOBAL              nb
             1156  LOAD_METHOD              CalculateRMP
             1158  LOAD_FAST                'rmp_traces'
             1160  CALL_METHOD_1         1  '1 positional argument'
             1162  CALL_METHOD_1         1  '1 positional argument'
             1164  LOAD_FAST                'results'
             1166  LOAD_STR                 'RMP'
             1168  STORE_SUBSCR     

 L. 369      1170  LOAD_FAST                'rheobase'
             1172  LOAD_FAST                'results'
             1174  LOAD_STR                 'Rheobase'
             1176  STORE_SUBSCR     

 L. 372      1178  LOAD_FAST                'options'
             1180  LOAD_STR                 'plot'
             1182  BINARY_SUBSCR    
             1184  STORE_FAST               'plot'

 L. 373      1186  LOAD_FAST                'options'
             1188  LOAD_STR                 'save'
             1190  BINARY_SUBSCR    
             1192  STORE_FAST               'save'

 L. 374      1194  LOAD_FAST                'save'
             1196  LOAD_CONST               True
             1198  COMPARE_OP               ==
         1200_1202  POP_JUMP_IF_FALSE  1342  'to 1342'

 L. 375      1204  LOAD_FAST                'options'
             1206  LOAD_STR                 'save_type'
             1208  BINARY_SUBSCR    
             1210  STORE_FAST               'save_type'

 L. 376      1212  LOAD_GLOBAL              process_save_type
             1214  LOAD_FAST                'save_type'
             1216  CALL_FUNCTION_1       1  '1 positional argument'
             1218  STORE_FAST               'save_types'

 L. 377      1220  LOAD_STR                 'fig'
             1222  LOAD_FAST                'save_types'
             1224  COMPARE_OP               in
         1226_1228  POP_JUMP_IF_FALSE  1238  'to 1238'

 L. 379      1230  LOAD_FAST                'trace'
             1232  LOAD_FAST                'results'
             1234  LOAD_STR                 'trace'
             1236  STORE_SUBSCR     
           1238_0  COME_FROM          1226  '1226'

 L. 380      1238  LOAD_STR                 'trace'
             1240  LOAD_FAST                'save_types'
             1242  COMPARE_OP               in
         1244_1246  POP_JUMP_IF_FALSE  1342  'to 1342'

 L. 381      1248  LOAD_STR                 '{}.pickle'
             1250  LOAD_METHOD              format
             1252  LOAD_FAST                'sim_id'
             1254  CALL_METHOD_1         1  '1 positional argument'
             1256  STORE_FAST               'filename'

 L. 382      1258  SETUP_LOOP         1304  'to 1304'
             1260  LOAD_CONST               ('simulation_name', 'population_name')
             1262  GET_ITER         
           1264_0  COME_FROM          1278  '1278'
             1264  FOR_ITER           1302  'to 1302'
             1266  STORE_FAST               'name'

 L. 384      1268  LOAD_FAST                'name'
             1270  LOAD_FAST                'metadata'
             1272  LOAD_METHOD              keys
             1274  CALL_METHOD_0         0  '0 positional arguments'
             1276  COMPARE_OP               in
         1278_1280  POP_JUMP_IF_FALSE  1264  'to 1264'

 L. 385      1282  LOAD_STR                 '{}_{}'
             1284  LOAD_METHOD              format
             1286  LOAD_FAST                'metadata'
             1288  LOAD_FAST                'name'
             1290  BINARY_SUBSCR    
             1292  LOAD_FAST                'filename'
             1294  CALL_METHOD_2         2  '2 positional arguments'
             1296  STORE_FAST               'filename'
         1298_1300  JUMP_BACK          1264  'to 1264'
             1302  POP_BLOCK        
           1304_0  COME_FROM_LOOP     1258  '1258'

 L. 387      1304  LOAD_FAST                'options'
             1306  LOAD_STR                 'save_dir'
             1308  BINARY_SUBSCR    
         1310_1312  POP_JUMP_IF_FALSE  1332  'to 1332'

 L. 388      1314  LOAD_GLOBAL              os
             1316  LOAD_ATTR                path
             1318  LOAD_METHOD              join
             1320  LOAD_FAST                'options'
             1322  LOAD_STR                 'save_dir'
             1324  BINARY_SUBSCR    
             1326  LOAD_FAST                'filename'
             1328  CALL_METHOD_2         2  '2 positional arguments'
             1330  STORE_FAST               'filename'
           1332_0  COME_FROM          1310  '1310'

 L. 389      1332  LOAD_GLOBAL              save_trace
             1334  LOAD_FAST                'trace'
             1336  LOAD_FAST                'filename'
             1338  CALL_FUNCTION_2       2  '2 positional arguments'
             1340  POP_TOP          
           1342_0  COME_FROM          1244  '1244'
           1342_1  COME_FROM          1200  '1200'

 L. 391      1342  LOAD_FAST                'plot'
         1344_1346  POP_JUMP_IF_FALSE  1348  'to 1348'
           1348_0  COME_FROM          1344  '1344'

 L. 393      1348  LOAD_GLOBAL              dump_exception
             1350  LOAD_FAST                'results'
             1352  CALL_FUNCTION_1       1  '1 positional argument'
             1354  POP_TOP          

 L. 394      1356  LOAD_FAST                'results'
             1358  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_GLOBAL' instruction at offset 1104


def simulate_vclamp(sim_id, biomarker_names, mechanisms, mechanism_names, ions, t_stop, outputs, hold, steps, delta, durations, celsius, options, metadata, flags):
    """
    Simulation of standard voltage clamp protocol.
    Example implementing following protocol for K+ recordings from Anabios:
    mech = {'kdrtf': 1.0, 'nav18hw': 2.0,}
    mech_names =['kdrtf', 'nav18hw']
    simulate_vclamp(mechanisms=mech, mechanism_names=@TODO, hold=-70.0, steps=[-80,80], delta=10.0, durations=[1100,500,500], outputs=['v', 'ik'])

    1. Hold at -70 mV for 1100 ms
    2. Pulse from -80 to 80 mV with delta=10mV
    3. Hold at -70 mV for 500 ms
    
    Parameters
    ----------------
    sim_id (int) - identifier for the simulation
    biomarker_names (list of strings) 
    mechanisms - dict of mechanism details to construct model channels from
    mechanism_names - names of each mechanism (e.g. ion channel names)
    ions (list of strings) - ions needed in model (e.g. ['Na', 'Ca', 'K'])
    t_stop (float, ms)
    outputs (list of strings) - options to specify output including 'ik' (total k+ current biomarkers)
    hold (float, mV) - holding potential
    delta (float, mV or None) - size of steps or None to specify steps manually
    steps (list of floats, mV or list) start and end of voltage clamp if delta is specified or list of every step
    durations (3 element list of floats, ms) - start of each stage of voltage clamp 
    celsius (oC)
    options (dict)
    metadata(dict)
    flags(dict) - flags for special options such as passing extra data to the simulation
    
    Returns
    -----------
    results - dict, contents - depends on "outputs"
    results['sim_id'] - identifier for the simulation
    results['ik_steps_absmax'] - array of absolute peak k+ currents at each step
    @TODOs
    Biomarkers of curve fitting
    """
    import neuron
    from neuron import h
    sim_type = 'vclamp'
    plot = options['plot']
    save = options['save']
    if save == True:
        save_type = options['save_type']
    elif delta == None and not len(steps) > 0:
        raise AssertionError
    else:
        steps = np.arangesteps[0](steps[1] + 0.1 * delta)delta
    results = {}
    results['sim_id'] = sim_id
    results_names = biomarker_names
    for name in results_names:
        results[name] = np.nan

    if 'ik' in outputs:
        ik_steps_absmax = np.zeros(len(steps))
        ik_steps_absmax[:] = np.nan
    for i, step in enumerate(steps):
        cell = sh.build_model(mechanisms=mechanisms, mechanism_names=mechanism_names,
          conductances=None,
          mechanism_is_full_parameter_name=True)
        h.celsius = celsius
        if 'K' in ions:
            oldstyle = h.ion_style('k_ion', 1, 2, 1, 1, 0, sec=cell)
        if 'Na' in ions:
            oldstyle = h.ion_style('na_ion', 1, 2, 1, 1, 0, sec=cell)
        if 'Ca' in ions:
            oldstyle = h.ion_style('ca_ion', 1, 2, 1, 1, 0, sec=cell)
        v, t = sh.set_vt(cell=cell)
        vectors = sh.record_currents(cell, outputs)
        clamp = h.VClamp(0.5, sec=cell)
        clamp.amp[0] = hold
        clamp.dur[0] = durations[0]
        clamp.amp[1] = step
        clamp.dur[1] = durations[1]
        clamp.amp[2] = hold
        clamp.dur[2] = durations[2]
        h.finitialize(hold)
        neuron.run(t_stop)
        if i == 0:
            trace = {'t': t}
        trace['v_{}'.format(step)] = v
        for vector in vectors:
            trace['{}_{}'.format(vector, step)] = vectors[vector]

        if 'ik' in outputs:
            ik_steps_absmax[i] = nb.absmax(vectors['ik'])

    if 'ik' in outputs:
        results['ik_steps_absmax'] = ik_steps_absmax
    plot = options['plot']
    save = options['save']
    if save == True:
        save_type = options['save_type']
        save_types = process_save_type(save_type)
        if 'fig' in save_types:
            results['trace'] = trace
        if 'trace' in save_types:
            filename = '{}.pickle'.format(sim_id)
            for name in ('simulation_name', 'population_name'):
                if name in metadata.keys():
                    filename = '{}_{}'.format(metadata[name], filename)

            save_trace(trace, filename)
    if plot:
        pass
    return results


class PopulationOfModels(object):

    def __init__(self, name, model_details, simulation_protocols=None, parameter_filename=None, parameter_set_details=None):
        """
        Main class for running populations of models in NEURON
        
        Parameters
        ----------------
        name: str - name to identify population
        
        model_details: dict, format is:
        {'mechanisms':{mechanism_details}}
        where mechanism_details=
        {'neuron_name_of_current':{'name of each parameter of that current to vary':'name of that parameter in neuron'}}
        E.g.: 
        model_details = {'mechanisms':{}}
        model_details['mechanisms']['nav17vw_named'] = {'GNav17':'gbar_nav17vw_named'}
 
        sim_protocols: dict, for format see Simulation class for each simulation function
        
        NOTE: Only one of parameter_filename and parameter_set_details can be anything other than None, to uniquely define the parameter set of the population.
        
        parameter_filename: str, default None - use this to load an existing parameter set
        
        parameter_set_details: dict, format is:
            'num_models':int
            'parameter_data': list of parameter names
            e.g. ['GNav17', 'GNav18']
            OR
            dict of parameter names and sampling ranges
            e.g. {'GNav17':[0.0,0.4], 'GNav18':[0.,4.0]}
            'minimum': None (non-uniform parameter scaling) or float (uniform parameter scaling)- if None have to provide dict for parameter data
            'maximum': See minimum.
            'save': bool - whether to save parameter set independent of population
            'output_filename': string - where to save parameter set
        
        Steps for running a population of models simulation:
        1. Read in parameters or generate and save a new set
        2. Set up simulation protocols (initialise from inputs)
        3. For each parameter set:
            4. Build a model
            5. Run the model using simulation protocols
            6. Calculate biomarkers from each simulation
            7. Collect all biomarkers from that model and add to results
        8. Collate and possibly save all biomarkers and any required simulation data
        9. (Optional) Analyse biomarkers and present summary data and/or visualisations if asked for
        
        Example: see examples @TODO: make examples and example dir in source
        
        To dos: 
        1. Support non-conductance parameters through updating sh.build_model "
        2. Parallelised simulations. "
        3. Support multi-compartment models and simulations (possibly in a separate class?). 
        """
        self.name = name
        self.model_details = model_details
        self.setup_mechanisms()
        if (parameter_filename is not None) & (parameter_set_details is not None):
            raise ValueError('Both parameter filename and parameter details have been provided, choose one or the other.')
        self.setup_parameters(parameter_filename=parameter_filename, parameter_set_details=parameter_set_details)
        self.model_description = self.get_model_description()
        self.setup_results()
        self.simulations = {}
        self.traces = {}
        self.calibration_complete = False
        self.calibration_applied = False
        self.calibration = None
        self.calibrated_indices = None
        self.simulation_protocols = simulation_protocols
        self.current_set = None
        self.celsius = 32.0
        self.blocks = {}

    def setup_results(self):
        """
        Setup the main results dataframe to store parameters, biomarkers and model metadata. Load parameters and model information into the dataframe as part of the setup process.
        """
        self.results = self.parameters.copy(deep=True)
        param_names = self.results.columns
        arrays = [['Parameters'] * len(param_names), param_names]
        columns = pd.MultiIndex.from_arrays(arrays, names=['', ''])
        self.results.columns = columns
        self.results.index.name = 'Model'

    def setup_mechanisms(self):
        """ Load mechanism details from model details dictionary """
        self.mechanisms = self.model_details['mechanisms']
        self.mechanism_names = list(self.mechanisms.keys())
        for mechanism, parameters in self.mechanisms.items():
            for _, param_var_name in parameters.items():
                if mechanism != param_var_name[-len(mechanism):]:
                    raise NameError('Parameter name {} is not consistent with associated mechanism name {}.'.format(param_var_name, mechanism))

        self.parameter_names = []
        self.parameter_designations = {}
        for mechanism in self.mechanisms:
            self.parameter_names.extend(list(self.mechanisms[mechanism].keys()))
            self.parameter_designations.update(self.mechanisms[mechanism])

        assert len(self.mechanism_names) == len(set(self.mechanism_names)), 'Mechanism names are not all unique.'
        assert len(self.parameter_names) == len(set(self.parameter_names)), 'Parameter names are not all unique.'
        assert len(self.parameter_designations) == len(set(self.parameter_designations)), 'Parameter designations are not all unique.'

    def setup_parameters(self, parameter_filename=None, parameter_set_details=None):
        """ Load or generate a parameter set for simulations. """
        if (parameter_filename is not None) & (parameter_set_details is not None):
            raise ValueError('Both parameter_filename and parameter_set_details are mutually exclusive, set one of them to None so we know which one to use.')
        elif parameter_filename:
            parameters, header = self.load_parameter_set(parameter_filename, load_comment=True, comment='#')
        else:
            if parameter_set_details:
                num_models = parameter_set_details['num_models']
                parameter_data = parameter_set_details['parameter_data']
                save = parameter_set_details['save']
                output_filename = parameter_set_details['output_filename']
                if isinstance(parameter_data, list):
                    minimum = parameter_set_details['minimum']
                    maximum = parameter_set_details['maximum']
                else:
                    minimum = None
                    maximum = None
                parameters, header = sh.build_parameter_set(num_models=num_models, parameter_data=parameter_data, minimum=minimum, maximum=maximum, filename=output_filename, save=save)
            else:
                raise ValueError('No filename to load or details provided to set up parameters.')
        self.parameters = parameters
        self.parameter_details = header

    def load_calibration_ranges(self, calibration_ranges=None, calibration_filename=None):
        """ Load calibration ranges from a dataframe or a file """
        if calibration_filename:
            calibration_ranges = pd.read_csv(calibration_filename)
            self.calibration_ranges = calibration_ranges
        else:
            if calibration_ranges:
                assert type(calibration_ranges) == pd.DataFrame, 'Supplied calibration ranges are not a pandas DataFrame'
                self.calibration_ranges = calibration_ranges
            else:
                raise ValueError('No calibration range or filename supplied.')

    def get_model_description(self):
        """
        Construct a string describing the model attached to a parameter set.
        Model description format:
        'Population of models with currents: x, y and z, varying parameters i, j, k, l,m,n,o. Population class constructed on -date-.'
        """
        mechanisms = ', '.join(self.mechanism_names)
        parameter_details = self.parameter_details
        date = time.strftime('%d/%m/%Y')
        model_description = 'Population of models with mechanisms: {0}. Parameters: {1}. Population class initialized on {2}.'.formatmechanismsparameter_detailsdate
        return model_description

    def setup_simulation(self, name, simulation_type, protocols, options=None, rerun=False):
        """
        Initialises a simulation 
        
        Parameters
        ----------------
        name: str, default 'sim'
        simulation_type: str, default 'IClamp', options: 'IClamp', 'VClamp', 'Test' (case insensitive)
        protocols: dict, default None, contents dependent on 'type'.
        options
        
        """
        if name in self.simulations.keys():
            name_collision = True
            if rerun == False:
                raise ValueError('Simulation name {} is already present.'.format(name))
        else:
            name_collision = False
        protocols['simulation_type'] = simulation_type
        self.simulations[name] = Simulation(name, protocols, options=options, population=self)
        self.simulations[name].rerun = rerun
        self.simulations[name].name_collision = name_collision

    def run_simulation(self, name, simulation_type, protocols=None, cores=1, save_type='fig', save_dir=None, benchmark=True, rerun=False):
        """
        Runs simulations on all models in results, whether that is an initial sample or a calibrated population.
        
        Example (in iPython):
        test_pop_$date$.py:
        # read in args
        
        # create population and simulation parameters
        pop.run_simulation(simulation_parameters, sim_name='Test')
        
        clean_notebook.py
        %run test_pop.py cores=4
        
        Parameters
        ----------------
        simulation_protocols: dict of protocol for simulation - see Simulation class for formats
        
        Returns
        -----------
        Nothing, concats simulation results to self.results, unless rerun is set to true,
        in which case it overwrites results.
        
        """
        if protocols == None:
            protocols = self.simulation_protocols
        elif not protocols != None:
            raise AssertionError('Simulation protocol not set.')
        else:
            parameters = self.results['Parameters']
            if rerun == False:
                self.setup_simulation(name, simulation_type, protocols, rerun=rerun)
            else:
                if rerun == True:
                    self.simulations[name].rerun = True
                    self.simulations[name].name_collision = True
                    self.simulations[name].reset_simulation()
                else:
                    raise ValueError('rerun not bool')
            sim = self.simulations[name]
            sim.pom_simulation(simulation_type=simulation_type,
              cores=cores,
              save_type=save_type,
              save_dir=save_dir,
              benchmark=benchmark,
              rerun=rerun)
            print('Sim results:\n {}'.format(sim.results))
            sim_results = sim.results
            formatted_results = pd.DataFrame(columns=(pd.MultiIndex.from_product([[name], sim_results.columns])),
              index=(self.results.index))
            formatted_results[:] = sim_results
            if self.simulations[name].name_collision == False:
                self.results = pd.concat([self.results, formatted_results], axis=1)
            else:
                if self.simulations[name].name_collision == True:
                    _df = formatted_results[name].copy()
                    self.results[name] = _df
                else:
                    raise ValueError('name_collision not set')

    def calibrate_population(self, biomarker_names, simulation_name, calibration_ranges='Davidson', stds=None, verbose=True):
        """ 
        Calibrate the current parameter sets, saving the data on calibration criteria passing to a dataframe which is set as the
        active calibration.
        """
        assert type(simulation_name) == str
        if calibration_ranges == 'Davidson':
            if stds == None:
                stds = 1.0
            ranges = db.CalibrationData(num_stds=stds)
            results = self.results.copy(deep=True)
            calibration = pd.DataFrame(index=(results.index), columns=biomarker_names)
            for biomarker in biomarker_names:
                minimum = ranges.loc[biomarker]['Min']
                maximum = ranges.loc[biomarker]['Max']
                if verbose:
                    num_in_range = ((self.results[(simulation_name, biomarker)] >= minimum) & (self.results[(simulation_name, biomarker)] <= maximum)).sum()
                    num_over = (self.results[(simulation_name, biomarker)] >= maximum).sum()
                    num_under = (self.results[(simulation_name, biomarker)] < minimum).sum()
                    num_nans = pd.isnull(self.results[(simulation_name, biomarker)]).sum()
                    total = num_in_range + num_over + num_under + num_nans
                    print('Biomarker: {}. Num in range: {}. Num over max: {}. Num under min: {}. Nans: {}. Total {}.'.format(biomarker, num_in_range, num_over, num_under, num_nans, total))
                single_biomarker_calibration = (results[(simulation_name, biomarker)] >= minimum) & (results[(simulation_name, biomarker)] <= maximum)
                results = results[single_biomarker_calibration]
                calibration[biomarker] = single_biomarker_calibration

        else:
            raise ValueError('Calibration_ranges value not understood.')
        if self.calibration_complete == False:
            self.uncalibrated_results = self.results.copy(deep=True)
            self.calibration_complete = True
        self.calibration = calibration
        self.calibrated_indices = results.index
        self.results = results
        self.calibration_applied = True

    def calibrate(self, biomarkers, ranges):
        """ Simple function to perform calibration of a set of biomarkers against a set of ranges.
        biomarkers is a pd.DataFrame of biomarker values 
        ranges is a pd.Dataframe of biomarker ranges 
        output is a boolean pd.Series for whether each biomarker set was within all ranges or not 
        """
        calibration = pd.Series(True, index=(biomarkers.index))
        for biomarker in biomarkers:
            calibration = calibration & (biomarkers[biomarker] <= ranges[biomarker].loc['max'])
            calibration = calibration & (biomarkers[biomarker] >= ranges[biomarker].loc['min'])

        return calibration

    def revert_calibration(self, preserve_calibration=False):
        """ Revert population to uncalibrated state, optionally saving the calibration and calibrated results in a separate dataframe """
        if self.calibration_applied & self.calibration_complete:
            if preserve_calibration:
                self.calibrated_results = self.results.copy(deep=True)
                self.reverted_calibration = self.calibration.copy(deep=True)
            self.results = self.uncalibrated_results.copy(deep=True)
            self.calibration = None
            self.uncalibrated_results = None
            self.calibration_complete = False
            self.calibration_applied = False
        else:
            raise ValueError('Calibration is not complete and applied.')

    def plot_parameters(self):
        pass

    def plot_biomarkers(self, name):
        pass

    def something_with_clustering(self):
        pass

    def parameter_correlations(self):
        pass

    def save(self, filename=None):
        if filename == None:
            filename = '{}.pkl'.format(self.name)
        self.active_model = None
        with open(filename, 'wb') as (f):
            pickle.dump(self, f)

    def save_parameter_set(self, filename, save_comment=True, comment='#'):
        """
        Save parameter set and details to a csv file
        """
        with open(filename, 'w') as (f):
            comment_char = comment
            f.write('{} {}\n'.format(comment_char, self.parameter_details))
            parameter_sets = self.parameters.round(6)
            parameter_sets.to_csv(f)

    def load_parameter_set(self, filename, load_comment=False, comment='#'):
        """
        Load a parameter set CSV file and return as a dataframe. Optionally, also
        return any commented lines at the top of the file. 
        """
        parameters = pd.read_csv(filename, sep=',', comment=comment, index_col=0)
        if load_comment:
            comments = ''
            with open(filename, 'r') as (f):
                while True:
                    line = f.readline()
                    if line[0] == comment:
                        comments += line.lstrip(' ' + comment)
                    else:
                        break

            return (
             parameters, comments)
        return parameters

    def apply_calibration(self):
        """
        Update self.results to only include the results for the calibrated parameters. Store
        the old results in self.uncalibrated_results.
        """
        if self.calibration_complete:
            self.uncalibrated_results = self.results.copy(deep=True)
            self.results = self.results.loc[self.calibration.all(axis=1)]
            self.calibration_applied = True
        else:
            print('Calibration not performed yet.')

    def remove_calibration(self):
        """
        Remove the last applied calibration and store the calibrated results if required.
        Applying then removing a calibration should return self.results back to where it started, however calibrated_results and uncalibrated_results will now exist as separate dataframes. This may be unwanted behaviour in the future, so there may need to be a cleanup function.
        """
        if self.calibration_applied:
            self.calibrated_results = self.results.copy(deep=True)
            self.results = self.uncalibrated_results.copy(deep=True)
            self.calibration_applied = False
        else:
            print('Calibration not currently applied to results.')

    def replace_mechanism(self, old_mech_name, new_mech_name):
        for i, mech_name in enumerate(self.mechanism_names):
            if mech_name == old_mech_name:
                self.mechanism_names[i] = new_mech_name

        old_params = self.mechanisms.pop(old_mech_name, None)
        new_params = {}
        for name, param in old_params.items():
            new_params[name] = param.replace(old_mech_name, new_mech_name)
            self.parameter_designations[name] = param.replace(old_mech_name, new_mech_name)

        self.mechanisms[new_mech_name] = new_params
        self.model_description = self.model_description.replace(old_mech_name, new_mech_name)

    def rename(self, name):
        self.name = name

    def get_simulation_names(self):
        return sorted(list(self.simulations.keys()))


class Simulation(object):
    __doc__ = "\n    Main class for running all kinds of simulations\n    \n    Assumptions:\n    One instance of the Simulation class will run one simulation set and not be reused.\n    When run_simucalculate\n    one instance of each biomarker for each parameter set.\n    For each parameter set, the base model structure will be the same.\n    \n    Parameters\n    -----------------\n    sim_name: str, default 'simulation'\n    population: PopulationOfModels, default None\n    \n    \n    Examples\n    -----------\n    Use for a single simulation:\n    @To do\n    Use as part of a POM simulation:\n    @To do\n    To generate the format for protocols:\n    sim = Simulation(name='test',protocols=None, population=pop)\n    sim.empty_simulation_protocol(sim_name)\n    \n    "

    def __init__(self, name, protocols, options=None, population=None):
        self.name = name
        self.protocols = protocols
        self.traces = {}
        self.plotting_pointer = 0
        self.num_subplots = 100
        self.rerun = None
        self.name_collision = None
        if population != None:
            self.population = population
            self.simulation_ran = False
        else:
            raise ValueError('Population must be supplied to run simulation, for single cell simulations use simulation_helpers module.')
        if options == None:
            self.options = options
        else:
            assert False, 'options not enabled in constructor'

    def reset_simulation(self):
        """ 
        Reset simulation for a rerun.
        """
        self.traces = {}
        self.plotting_pointer = 0

    def pom_simulation(self, simulation_type, cores=1, save_type='fig', save_dir=None, benchmark=True, rerun=False):
        """
        Run simulations 
        
        Parameters
        -----------------
        simulation_type: string
        cores: int, default 1
        plot: bool, default False
        save_type: str, default 'fig', options are defined in allowed_save_types()
        save_dir: str, default None
        benchmark: bool, default True
        rerun: bool, default False
        
        Returns
        -----------
        Dataframe of biomarker results indexed by their index in the population
        associated with this simulation class.
        """
        if (self.simulation_ran == True) & (self.rerun == False):
            raise ValueError('This simulation has already been ran, cannot run same simulation againwith the same simulator with name: {} without specifying simulation is a rerun.'.format(self.name))
        if self.population == None:
            raise ValueError('No population specified - cannot run population of models simulation!')
        assert save_type in allowed_save_types(), 'Save type not recognised.'
        options = {'save_type':save_type,  'save_dir':save_dir}
        self.options = options
        self.protocols['options'] = options
        metadata = {'population_name':self.population.name, 
         'simulation_name':self.name}
        self.protocols['metadata'] = metadata
        self.set_simulation_function(simulation_type)
        num_sims = len(self.population.results.index)
        self.results = pd.DataFrame(index=(self.population.results.index),
          columns=(self.get_biomarker_names(simulation_type, self.protocols['outputs'])))
        self.model_indices = self.population.results.index.tolist()
        self.model_indices.sort()
        self.model_indices = tuple(self.model_indices)
        assert len(self.model_indices) == len(set(self.model_indices)), 'Duplicates in model indices.'
        print('Simulation set of {} simulations begun.'.format(num_sims))
        start = time.time()
        pool = mp.Pool(processes=cores)
        self.count = 0
        for _, model_idx in enumerate(self.model_indices):
            mechanisms = self.build_parameters(model_idx)
            sim_kwargs = self.build_simulation_kwargs(sim_id=model_idx,
              simulation_type=simulation_type,
              simulation_parameters=(self.protocols),
              mechanisms=mechanisms)
            pool.apply_async((self.simulation_function), kwds=sim_kwargs, callback=(self.log_result))

        pool.close()
        pool.join()
        if benchmark:
            print('Simulations finished in {} s'.format(time.time() - start))
        if ('fig' in process_save_type(save_type)) & (len(self.traces) > 0):
            plotted = True
            timeout_counter = 0
            while plotted:
                filename = '{0}_{1}_traces_{2}.png'.formatself.population.nameself.nameself.count
                plotted = self.trace_plot((self.num_subplots), filename, force_plot=True)
                if plotted:
                    self.count += 1
                timeout_counter += 1
                if timeout_counter > 10 * num_sims / self.num_subplots:
                    raise RuntimeError('Plotting timed out at end of simulation.')

        self.simulation_ran = True

    def set_simulation_function(self, simulation_type):
        """
        Function to set simulation 
        """
        simulation_type = simulation_type.lower()
        if simulation_type == 'iclamp':
            self.simulation_function = simulate_iclamp
        else:
            if simulation_type == 'vclamp':
                self.simulation_function = simulate_vclamp
            else:
                raise ValueError('simulation type: {} is not found.'.format(simulation_type))

    def build_parameters(self, model_idx):
        """
        Construct parameter data for a model including parameter changes if required
        @TODO! - Think about how we want to use mechanisms and mechanism names - is there a better format?
        @TODO - Understand how to handle multiprocessing errors so we can return an error message if the
        parameter names and mechanism names don't line up.
        @TODO - We have we have population.parameter_designations, population.mechanism_names and
        population.results['Parameters']....should we consolidate at least the parameters and mechanism
        names into a single data structure?

        Format of parameter_scaling is a dict with format:
        {parameter:scaling_factor}
        where parameter is the public parameter name shown in pop.results
        and where scaling factor is a number that the base parameter value will be multiplied by
        """
        active_parameters = self.population.results['Parameters'].loc[model_idx].copy()
        if 'parameter_scaling' in self.protocols:
            for param, scaling_factor in self.protocols['parameter_scaling'].items():
                assert param in self.population.parameter_designations, 'Parameter {} not present in parameter designations'.format(param)
                active_parameters.loc[param] *= scaling_factor

        mechanisms = {self.population.parameter_designations[param]:val for param, val in active_parameters.items()}
        return mechanisms

    def get_simulation_protocol_names(self):
        """
        Gets list of parameter names for each simulation 
        """
        names = {}
        names['always'] = [
         'sim_id', 'options', 'metadata']
        names['clamp'] = ['mechanisms', 'mechanism_names', 'biomarker_names', 'ions', 't_stop', 'outputs', 'celsius']
        names['iclamp'] = ['amp', 'dur', 'delay', 'interval', 'num_stims', 'stim_func', 'v_init', 'sampling_freq']
        names['vclamp'] = ['hold', 'steps', 'delta', 'durations']
        names['optional'] = ['flags', 'parameter_scaling']
        return names

    def build_simulation_kwargs(self, sim_id, simulation_type, simulation_parameters, mechanisms):
        """
        Setup dict of keyword arguments to feed to simulation function
        """
        simulation_type = simulation_type.lower()
        assert simulation_type in ('iclamp', 'vclamp', 'test'), 'Simulation type: {} not found'.format(simulation_type)
        simulation_parameters['sim_id'] = sim_id
        simulation_parameters['mechanisms'] = mechanisms
        simulation_parameters['mechanism_names'] = self.population.mechanism_names
        simulation_parameters['biomarker_names'] = self.get_biomarker_names(simulation_type, simulation_parameters['outputs'])
        names = self.get_simulation_protocol_names()
        kwargs = {}
        if simulation_type in ('iclamp', 'vclamp'):
            for kwarg in names['clamp']:
                kwargs[kwarg] = simulation_parameters[kwarg]

            assert set(kwargs.keys()) == set(names['clamp']), 'Parameters common to iclamp+vclamp missing.'
        for kwarg in names[simulation_type]:
            kwargs[kwarg] = simulation_parameters[kwarg]

        for kwarg in names['optional']:
            if kwarg == 'flags':
                if kwarg in simulation_parameters:
                    kwargs['flags'] = self.process_flags(simulation_parameters['flags'], sim_id)
                else:
                    kwargs['flags'] = {}

        for kwarg in names['always']:
            kwargs[kwarg] = simulation_parameters[kwarg]

        assert set(kwargs.keys()) == set(get_function_args(self.simulation_function)), "Kwargs don't match function argument list"
        return kwargs

    def empty_simulation_protocol(self, simulation_type):
        """ 
        Return dict with empty values to show required structure of simulation protocol for
        a given simulation type for user filling out.
        Therefore, we don't include parameters about mechanisms or sim_ids that are filled out internally.
        """
        simulation_type = simulation_type.lower()
        names = self.get_simulation_protocol_names()
        kwargs = {}
        if simulation_type in ('iclamp', 'vclamp'):
            for kwarg in [name for name in names['clamp'] if name not in ('mechanisms',
                                                                          'mechanism_names',
                                                                          'biomarker_names')]:
                kwargs[kwarg] = None

        for kwarg in names[simulation_type]:
            kwargs[kwarg] = None

        for kwarg in names['always']:
            if kwarg not in ('sim_id', 'metadata', 'options'):
                kwargs[kwarg] = None

        return kwargs

    def get_simulation_protocol_defaults(self):
        """ 
        Get default values for simulation protocols.
        This could be useful if some are missing in the input? 
        Or do we want to enforce having all the inputs?
        I think we want to force all inputs for research purposes - makes every 
        simulation parameter explicit.
        """
        assert False, 'Not implemented to encourage simulation inputs to be explicitly documented in run scripts.'

    def get_biomarker_names(self, sim_type, outputs):
        """ 
        Generate the list of biomarker names we'll calculate.
        Currently a bit messy as to add a new biomarker we need to add it here
        and in the simulation code. But it should cause an error if I miss one or the other.
        
        Returns
        -----------
        List of biomarker names for the simulation type given, for the output codes specified.
        """
        biomarker_names = {}
        biomarker_names['iclamp'] = [
         'APFullWidth', 'APPeak', 'APRiseTime', 'APSlopeMin', 'APSlopeMax',
         'AHPAmp', 'AHPTau', 'AHPTrough', 'ISI', 'RMP', 'Rheobase', 'Firing pattern']
        biomarker_names['vclamp'] = []
        if outputs:
            if 'ik' in outputs:
                biomarker_names['iclamp'].extend([])
                biomarker_names['vclamp'].extend(['ik_steps_absmax'])
            if 'ina' in outputs:
                biomarker_names['iclamp'].extend([])
                biomarker_names['vclamp'].extend([])
        return biomarker_names[sim_type.lower()]

    def process_flags(self, flags, sim_id):
        """
        Processes any flags given to the simulation and returns the correct information.
        """
        processed_flags = {}
        for flag, val in flags.items():
            assert flag in self.allowed_flags(), 'Flag {} not in allowed_flags'.format(flag)
            if flag == 'ramp_threshold_sim_for_width':
                sim_name = val
                assert self.population != None, 'Need a population'
                assert sim_name in self.population.results.columns, 'sim_name {} not found'.format(sim_name)
                assert sim_id in self.population.results.index, 'sim_id {} not found'.format(sim_id)
                threshold = self.population.results.at[(sim_id, (sim_name, 'Threshold'))]
                processed_flags[flag] = threshold
            elif flag == 'rheobase_sim_for_stim_amp':
                sim_name = val
                assert sim_name in self.population.results.columns, 'sim_name {} not found'.format(sim_name)
                assert sim_id in self.population.results.index, 'sim_id {} not found'.format(sim_id)
                amp = self.population.results.at[(sim_id, (sim_name, 'Rheobase'))]
                processed_flags[flag] = amp
            else:
                raise ValueError('Flag {} not supported.'.format(flag))

        return processed_flags

    def allowed_flags(self):
        """
        Returns a list of allowed strings to be passed to simulations as flags
        """
        allowed_flags = []
        allowed_flags.append('ramp_threshold_sim_for_width')
        allowed_flags.append('rheobase_sim_for_stim_amp')
        return allowed_flags

    def log_test(self, result):
        for biomarker in self.results.columns:
            self.results.loc[(0, biomarker)] = result

    def log_result(self, result):
        """
        Stores the result from a simulation using callback functionality. 
        """
        keys = result.keys()
        biomarker_names = [key for key in keys if key not in ('sim_id', 'trace')]
        sim_id = result['sim_id']
        for biomarker in biomarker_names:
            self.results.at[(sim_id, biomarker)] = result[biomarker]

        if (self.options['save'] == True) & ('fig' in process_save_type(self.options['save_type'])):
            self.traces[sim_id] = result['trace']
        filename = filename = '{0}_{1}_traces_{2}.png'.formatself.population.nameself.nameself.count
        plotted = self.trace_plot(self.num_subplots, filename)
        if plotted:
            self.count += 1

    def trace_plot(self, traces_to_plot, filename, force_plot=False, require_contiguous=True):
        """  
        If we want to save subplots of traces, decide if we have enough saved traces to plot
        First implementation was to just look for contiguous blocks - but what if we plot 1->101 
        and miss trace 0 in the first?
        Second implementation (CURRENTLY USED): demand we start with the first sim_id, then when we've done a plot
        move the pointer to sim_id+traces_to_plot+1.
        """
        if (self.options['save'] == True) & ('fig' in process_save_type(self.options['save_type'])):
            subplot_dim = int(np.ceil(np.sqrt(traces_to_plot)))
            make_plot = False
            num_traces = len(self.traces)
            if (force_plot == True) & (num_traces > 0):
                make_plot = True
            if num_traces >= traces_to_plot:
                if require_contiguous == True:
                    ids = self.traces.keys()
                    ids = sorted(ids)
                    required_format = self.model_indices[self.plotting_pointer:self.plotting_pointer + traces_to_plot]
                    if all([i == j for i, j in zip(ids[0:traces_to_plot], required_format)]):
                        make_plot = True
                        self.plotting_pointer += traces_to_plot
                else:
                    make_plot = True
            if make_plot == True:
                ids = sorted(self.traces.keys())
                ids = ids[0:traces_to_plot]
                outputs = self.protocols['outputs']
                fig = plt.figure(figsize=(40, 40))
                legend_plotted = False
                for i, sim_id in enumerate(ids):
                    plt.subplotsubplot_dimsubplot_dim(i + 1)
                    trace = self.traces[sim_id]
                    if isinstance(trace, np.ndarray):
                        for j in range(1, trace.shape[1]):
                            plt.plot(trace[:, 0], trace[:, j])

                    else:
                        if isinstance(trace, dict):
                            for key in [key for key in trace.keys() if key != 't']:
                                _data = trace[key]
                                if isinstance(_data, dict):
                                    for _current_type, _current in _data.items():
                                        _ndarray_current = np.array(_current)
                                        if len(trace['t']) == len(_ndarray_current):
                                            plt.plot(trace['t'], _ndarray_current)

                                elif len(trace['t']) == len(_data):
                                    plt.plot(trace['t'], _data)

                    if legend_plotted == False:
                        if isinstance(trace, dict):
                            legend = [key for key in trace.keys() if key != 't']
                        else:
                            legend = [
                             'Vm']
                        plt.legend(legend)
                        legend_plotted = True
                    firing_pattern = self.results.at[(sim_id, 'Firing pattern')]
                    plt.title('{}: {}'.format(sim_id, firing_pattern))

                fig.savefig(filename, dpi=150)
                plt.close(fig)
                fig = None
                print('Saved to {}, number of traces stored = {}'.format(filename, len(self.traces)))
                sys.stdout.flush()
                for id in ids:
                    del self.traces[id]

                return True
            if make_plot == False:
                return False
            raise ValueError('make_plot is invalid value: {}'.format(make_plot))