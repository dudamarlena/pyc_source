# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\LTTL\Processor.py
# Compiled at: 2019-10-11 17:22:08
# Size of source mod 2**32: 84634 bytes
"""Module Processor.py
Copyright 2012-2016 LangTech Sarl (info@langtech.ch)
---------------------------------------------------------------------------
This file is part of the LTTL package v2.0.

LTTL v2.0 is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

LTTL v2.0 is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with LTTL v2.0. If not, see <http://www.gnu.org/licenses/>.
"""
from __future__ import division
from __future__ import absolute_import
from __future__ import unicode_literals
from math import sqrt
from builtins import range
from builtins import str as text
import numpy as np
from .Segmentation import Segmentation
from .Table import *
from .Utils import get_average, get_variety, get_expected_subsample_variety, tuple_to_simple_dict, sample_dict, prepend_unit_with_category, generate_random_annotation_key, get_unused_char_in_segmentation, iround
__version__ = '1.0.6'

def count_in_context(units=None, contexts=None, progress_callback=None):
    """Count units in contexts.

    Parameter units is a dict with the following keys and values:
    KEY                     VALUE                           DEFAULT
    segmentation            unit segmentation               None
    annotation_key          annotation to be counted        None
    seq_length              length of unit sequences        1
    intra_seq_delimiter     string for joining sequences    '#'

    Parameter contexts is a dict with the following keys and values:
    KEY                     VALUE                           DEFAULT
    segmentation            context segmentation            None
    annotation_key          annotation to be counted        None
    merge                   merge contexts together?        False

    Returns an IntPivotCrosstab table.
    """
    default_units = {'segmentation':None, 
     'annotation_key':None, 
     'seq_length':1, 
     'intra_seq_delimiter':'#'}
    default_contexts = {'segmentation':None, 
     'annotation_key':None, 
     'merge':False}
    if units is not None:
        default_units.update(units)
    units = default_units
    if contexts is not None:
        default_contexts.update(contexts)
    contexts = default_contexts
    freq = dict()
    context_types = list()
    unit_types = list()
    if contexts['segmentation'] is not None and units['segmentation'] is not None:
        context_type = '__global__'
        context_annotation_key = contexts['annotation_key']
        context_segmentation = contexts['segmentation']
        unit_segmentation = units['segmentation']
        unit_annotation_key = units['annotation_key']
        unit_seq_length = units['seq_length']
        seq_join = units['intra_seq_delimiter'].join
        if unit_seq_length > 1:
            if unit_annotation_key is not None:
                unit_list = [u.annotations.get(unit_annotation_key, '__none__') for u in unit_segmentation]
            else:
                unit_list = [u.get_content() for u in unit_segmentation]
            for context_index, context_segment in enumerate(context_segmentation):
                context_token = context_segment
                if not contexts['merge']:
                    if context_annotation_key is not None:
                        context_type = context_segment.annotations.get(context_annotation_key, '__none__')
                    else:
                        context_type = context_segment.get_content()
                    if context_type not in context_types:
                        context_types.append(context_type)
                    for unit_seq_index in context_token.get_contained_sequence_indices(unit_segmentation, unit_seq_length):
                        unit_type = seq_join(unit_list[unit_seq_index:unit_seq_index + unit_seq_length])
                        if unit_type not in unit_types:
                            unit_types.append(unit_type)
                        type_pair = (
                         context_type, unit_type)
                        freq[type_pair] = freq.get(type_pair, 0) + 1

                    if progress_callback:
                        progress_callback()

            if len(freq) > 0:
                if len(context_types) == 0:
                    context_types.append(context_type)
        else:
            for context_token in contexts['segmentation']:
                if not contexts['merge']:
                    if context_annotation_key is not None:
                        context_type = context_token.annotations.get(context_annotation_key, '__none__')
                    else:
                        context_type = context_token.get_content()
                    for unit_token in context_token.get_contained_segments(unit_segmentation):
                        if unit_annotation_key:
                            unit_type = unit_token.annotations.get(unit_annotation_key, '__none__')
                        else:
                            unit_type = unit_token.get_content()
                        if context_type not in context_types:
                            context_types.append(context_type)
                        if unit_type not in unit_types:
                            unit_types.append(unit_type)
                        type_pair = (
                         context_type, unit_type)
                        freq[type_pair] = freq.get(type_pair, 0) + 1

                    if progress_callback:
                        progress_callback()

    else:
        if units['segmentation'] is not None:
            context_type = '__global__'
            context_types.append(context_type)
            unit_annotation_key = units['annotation_key']
            unit_segmentation = units['segmentation']
            unit_segmentation_length = len(units['segmentation'])
            unit_seq_length = units['seq_length']
            seq_join = units['intra_seq_delimiter'].join
            if unit_seq_length > 1:
                if unit_annotation_key is not None:
                    unit_list = [u.annotations.get(unit_annotation_key, '__none__') for u in unit_segmentation]
                else:
                    unit_list = [u.get_content() for u in unit_segmentation]
                for unit_index in range(unit_segmentation_length - (unit_seq_length - 1)):
                    unit_type = seq_join(unit_list[unit_index:unit_index + unit_seq_length])
                    if unit_type not in unit_types:
                        unit_types.append(unit_type)
                    type_pair = (
                     context_type, unit_type)
                    freq[type_pair] = freq.get(type_pair, 0) + 1
                    if progress_callback:
                        progress_callback()

            else:
                if unit_annotation_key is not None:
                    unit_list = [u.annotations.get(unit_annotation_key, '__none__') for u in unit_segmentation]
                else:
                    unit_list = [u.get_content() for u in unit_segmentation]
                unit_types = list(set(unit_list))
                for unit_type in unit_list:
                    type_pair = (
                     context_type, unit_type)
                    freq[type_pair] = freq.get(type_pair, 0) + 1
                    if progress_callback:
                        progress_callback()

        elif len(context_types) and isinstance(context_types[0], int):
            header_type = 'continuous'
        else:
            header_type = 'string'
        return IntPivotCrosstab(context_types, unit_types, freq, '__unit__', 'string', '__context__', header_type, dict([(u, 'continuous') for u in unit_types]), None, 0, None)


def count_in_window(units=None, window_size=1, progress_callback=None):
    """Count units in sliding window.

    Parameter units is a dict with the following keys and values:
    KEY                     VALUE                            DEFAULT
    segmentation            unit segmentation                None
    annotation_key          annotation to be counted         None
    seq_length              length of unit sequences         1
    intra_seq_delimiter     string for joining sequences     '#'

    Returns an IntPivotCrosstab table.
    """
    default_units = {'segmentation':None, 
     'annotation_key':None, 
     'seq_length':1, 
     'intra_seq_delimiter':'#'}
    if units is not None:
        default_units.update(units)
    units = default_units
    freq = dict()
    unit_types = list()
    window_type = 1
    if units['segmentation'] is not None and len(units['segmentation']) >= window_size >= units['seq_length']:
        unit_segmentation = units['segmentation']
        unit_annotation_key = units['annotation_key']
        if unit_annotation_key is not None:
            unit_list = [unit_token.annotations.get(unit_annotation_key, '__none__') for unit_token in unit_segmentation]
        else:
            unit_list = [u.get_content() for u in unit_segmentation]
        if units['seq_length'] > 1:
            seq_join = units['intra_seq_delimiter'].join
            unit_seq_length = units['seq_length']
            first_window = unit_list[:window_size]
            window_freq = dict()
            for unit_index in range(window_size - (unit_seq_length - 1)):
                unit_type = seq_join(first_window[unit_index:unit_index + unit_seq_length])
                if unit_type not in unit_types:
                    unit_types.append(unit_type)
                window_freq[unit_type] = window_freq.get(unit_type, 0) + 1

            freq = dict([(('1', k), v) for k, v in iteritems(window_freq)])
            if progress_callback:
                progress_callback()
            for window_index in range(1, len(units['segmentation']) - (window_size - 1)):
                window_freq[seq_join(unit_list[window_index - 1:window_index + unit_seq_length - 1])] -= 1
                new_unit = seq_join(unit_list[window_index + window_size - unit_seq_length:window_index + window_size])
                window_freq[new_unit] = window_freq.get(new_unit, 0) + 1
                if new_unit not in unit_types:
                    unit_types.append(new_unit)
                window_type = window_index + 1
                window_str = text(window_type)
                freq.update(dict([((window_str, k), v) for k, v in iteritems(window_freq)]))
                if progress_callback:
                    progress_callback()

        else:
            unit_types = list(set(unit_list))
            first_window = unit_list[:window_size]
            window_freq = dict()
            for unit_token in first_window:
                window_freq[unit_token] = window_freq.get(unit_token, 0) + 1

            freq = dict([(('1', k), v) for k, v in iteritems(window_freq)])
            if progress_callback:
                progress_callback()
            for window_index in range(1, len(units['segmentation']) - (window_size - 1)):
                window_freq[unit_list[(window_index - 1)]] -= 1
                new_unit = unit_list[(window_index + window_size - 1)]
                window_freq[new_unit] = window_freq.get(new_unit, 0) + 1
                window_type = window_index + 1
                window_str = text(window_type)
                freq.update(dict([((window_str, k), v) for k, v in iteritems(window_freq)]))
                if progress_callback:
                    progress_callback()

    return IntPivotCrosstab([text(i) for i in range(1, window_type + 1)], unit_types, freq, '__unit__', 'string', '__context__', 'continuous', dict([(u, 'continuous') for u in unit_types]), None, 0, None)


def count_in_chain--- This code section failed: ---

 L. 528         0  LOAD_CONST               None

 L. 529         2  LOAD_CONST               None

 L. 530         4  LOAD_CONST               1

 L. 531         6  LOAD_STR                 '#'
                8  LOAD_CONST               ('segmentation', 'annotation_key', 'seq_length', 'intra_seq_delimiter')
               10  BUILD_CONST_KEY_MAP_4     4 
               12  STORE_FAST               'default_units'

 L. 534        14  LOAD_CONST               1

 L. 535        16  LOAD_CONST               0

 L. 536        18  LOAD_STR                 '_'

 L. 537        20  LOAD_CONST               False
               22  LOAD_CONST               ('left_size', 'right_size', 'unit_pos_marker', 'merge_strings')
               24  BUILD_CONST_KEY_MAP_4     4 
               26  STORE_FAST               'default_contexts'

 L. 539        28  LOAD_FAST                'units'
               30  LOAD_CONST               None
               32  COMPARE_OP               is-not
               34  POP_JUMP_IF_FALSE    46  'to 46'

 L. 540        36  LOAD_FAST                'default_units'
               38  LOAD_ATTR                update
               40  LOAD_FAST                'units'
               42  CALL_FUNCTION_1       1  '1 positional argument'
               44  POP_TOP          
             46_0  COME_FROM            34  '34'

 L. 541        46  LOAD_FAST                'default_units'
               48  STORE_FAST               'units'

 L. 542        50  LOAD_FAST                'contexts'
               52  LOAD_CONST               None
               54  COMPARE_OP               is-not
               56  POP_JUMP_IF_FALSE    68  'to 68'

 L. 543        58  LOAD_FAST                'default_contexts'
               60  LOAD_ATTR                update
               62  LOAD_FAST                'contexts'
               64  CALL_FUNCTION_1       1  '1 positional argument'
               66  POP_TOP          
             68_0  COME_FROM            56  '56'

 L. 544        68  LOAD_FAST                'default_contexts'
               70  STORE_FAST               'contexts'

 L. 546        72  LOAD_GLOBAL              dict
               74  CALL_FUNCTION_0       0  '0 positional arguments'
               76  STORE_FAST               'freq'

 L. 547        78  LOAD_GLOBAL              list
               80  CALL_FUNCTION_0       0  '0 positional arguments'
               82  STORE_FAST               'context_types'

 L. 548        84  LOAD_GLOBAL              list
               86  CALL_FUNCTION_0       0  '0 positional arguments'
               88  STORE_FAST               'unit_types'

 L. 551        90  LOAD_FAST                'units'
               92  LOAD_STR                 'segmentation'
               94  BINARY_SUBSCR    
               96  STORE_FAST               'unit_segmentation'

 L. 552        98  LOAD_FAST                'units'
              100  LOAD_STR                 'annotation_key'
              102  BINARY_SUBSCR    
              104  STORE_DEREF              'unit_annotation_key'

 L. 553       106  LOAD_FAST                'units'
              108  LOAD_STR                 'seq_length'
              110  BINARY_SUBSCR    
              112  STORE_FAST               'unit_seq_length'

 L. 554       114  LOAD_FAST                'contexts'
              116  LOAD_STR                 'left_size'
              118  BINARY_SUBSCR    
              120  STORE_FAST               'context_left_size'

 L. 555       122  LOAD_FAST                'contexts'
              124  LOAD_STR                 'right_size'
              126  BINARY_SUBSCR    
              128  STORE_FAST               'context_right_size'

 L. 556       130  LOAD_FAST                'contexts'
              132  LOAD_STR                 'unit_pos_marker'
              134  BINARY_SUBSCR    
              136  STORE_FAST               'unit_pos_marker'

 L. 557       138  LOAD_FAST                'units'
              140  LOAD_STR                 'intra_seq_delimiter'
              142  BINARY_SUBSCR    
              144  LOAD_ATTR                join
              146  STORE_FAST               'seq_join'

 L. 558       148  LOAD_FAST                'context_left_size'
              150  LOAD_FAST                'context_right_size'
              152  BINARY_ADD       
              154  LOAD_FAST                'unit_seq_length'
              156  BINARY_ADD       
              158  STORE_FAST               'window_size'

 L. 559       160  LOAD_FAST                'contexts'
              162  LOAD_STR                 'merge_strings'
              164  BINARY_SUBSCR    
              166  STORE_FAST               'merge_strings'

 L. 562       168  LOAD_FAST                'unit_segmentation'
              170  LOAD_CONST               None
              172  COMPARE_OP               is-not
              174  JUMP_IF_FALSE_OR_POP   186  'to 186'

 L. 563       176  LOAD_FAST                'window_size'
              178  LOAD_GLOBAL              len
              180  LOAD_FAST                'unit_segmentation'
              182  CALL_FUNCTION_1       1  '1 positional argument'
              184  COMPARE_OP               <=
            186_0  COME_FROM           174  '174'
              186  POP_JUMP_IF_FALSE   782  'to 782'

 L. 567       190  LOAD_DEREF               'unit_annotation_key'
              192  LOAD_CONST               None
              194  COMPARE_OP               is-not
              196  POP_JUMP_IF_FALSE   218  'to 218'

 L. 569       198  LOAD_CLOSURE             'unit_annotation_key'
              200  BUILD_TUPLE_1         1 
              202  LOAD_LISTCOMP            '<code_object <listcomp>>'
              204  LOAD_STR                 'count_in_chain.<locals>.<listcomp>'
              206  MAKE_FUNCTION_8          'closure'

 L. 575       208  LOAD_FAST                'unit_segmentation'
              210  GET_ITER         
              212  CALL_FUNCTION_1       1  '1 positional argument'
              214  STORE_FAST               'unit_list'
              216  JUMP_FORWARD        232  'to 232'
              218  ELSE                     '232'

 L. 578       218  LOAD_LISTCOMP            '<code_object <listcomp>>'
              220  LOAD_STR                 'count_in_chain.<locals>.<listcomp>'
              222  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              224  LOAD_FAST                'unit_segmentation'
              226  GET_ITER         
              228  CALL_FUNCTION_1       1  '1 positional argument'
              230  STORE_FAST               'unit_list'
            232_0  COME_FROM           216  '216'

 L. 581       232  LOAD_LISTCOMP            '<code_object <listcomp>>'
              234  LOAD_STR                 'count_in_chain.<locals>.<listcomp>'
              236  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              238  LOAD_FAST                'unit_segmentation'
              240  GET_ITER         
              242  CALL_FUNCTION_1       1  '1 positional argument'
              244  STORE_FAST               'str_indices'

 L. 584       246  LOAD_FAST                'unit_seq_length'
              248  LOAD_CONST               1
              250  COMPARE_OP               >
              252  POP_JUMP_IF_FALSE   524  'to 524'

 L. 587       256  SETUP_LOOP          782  'to 782'
              260  LOAD_GLOBAL              range

 L. 588       262  LOAD_GLOBAL              len
              264  LOAD_FAST                'units'
              266  LOAD_STR                 'segmentation'
              268  BINARY_SUBSCR    
              270  CALL_FUNCTION_1       1  '1 positional argument'
              272  LOAD_FAST                'window_size'
              274  LOAD_CONST               1
              276  BINARY_SUBTRACT  
              278  BINARY_SUBTRACT  
              280  CALL_FUNCTION_1       1  '1 positional argument'
              282  GET_ITER         
              284  FOR_ITER            518  'to 518'
              286  STORE_FAST               'window_index'

 L. 593       288  LOAD_FAST                'str_indices'

 L. 594       290  LOAD_FAST                'window_index'
              292  LOAD_FAST                'window_index'
              294  LOAD_FAST                'window_size'
              296  BINARY_ADD       
              298  BUILD_SLICE_2         2 
              300  BINARY_SUBSCR    
              302  STORE_FAST               'idx_sequence'

 L. 597       304  LOAD_FAST                'merge_strings'
              306  UNARY_NOT        
              308  POP_JUMP_IF_FALSE   352  'to 352'

 L. 598       312  LOAD_FAST                'idx_sequence'
              314  LOAD_ATTR                count
              316  LOAD_FAST                'idx_sequence'
              318  LOAD_CONST               0
              320  BINARY_SUBSCR    
              322  CALL_FUNCTION_1       1  '1 positional argument'
              324  LOAD_GLOBAL              len
              326  LOAD_FAST                'idx_sequence'
              328  CALL_FUNCTION_1       1  '1 positional argument'
              330  COMPARE_OP               !=
              332  POP_JUMP_IF_FALSE   352  'to 352'

 L. 600       336  LOAD_FAST                'progress_callback'
              338  POP_JUMP_IF_FALSE   284  'to 284'

 L. 601       342  LOAD_FAST                'progress_callback'
              344  CALL_FUNCTION_0       0  '0 positional arguments'
              346  POP_TOP          

 L. 602       348  CONTINUE            284  'to 284'
            352_0  COME_FROM           332  '332'
            352_1  COME_FROM           308  '308'

 L. 605       352  LOAD_STR                 '%s%s%s'

 L. 606       354  LOAD_FAST                'seq_join'

 L. 607       356  LOAD_FAST                'unit_list'
              358  LOAD_FAST                'window_index'
              360  LOAD_FAST                'window_index'
              362  LOAD_FAST                'context_left_size'
              364  BINARY_ADD       
              366  BUILD_SLICE_2         2 
              368  BINARY_SUBSCR    
              370  CALL_FUNCTION_1       1  '1 positional argument'

 L. 609       372  LOAD_FAST                'unit_pos_marker'

 L. 610       374  LOAD_FAST                'seq_join'

 L. 611       376  LOAD_FAST                'unit_list'

 L. 612       378  LOAD_FAST                'window_index'
              380  LOAD_FAST                'context_left_size'
              382  BINARY_ADD       
              384  LOAD_FAST                'unit_seq_length'
              386  BINARY_ADD       

 L. 613       388  LOAD_FAST                'window_index'
              390  LOAD_FAST                'window_size'
              392  BINARY_ADD       
              394  BUILD_SLICE_2         2 
              396  BINARY_SUBSCR    
              398  CALL_FUNCTION_1       1  '1 positional argument'
              400  BUILD_TUPLE_3         3 
              402  BINARY_MODULO    
              404  STORE_FAST               'context_type'

 L. 619       406  LOAD_FAST                'seq_join'

 L. 620       408  LOAD_FAST                'unit_list'

 L. 621       410  LOAD_FAST                'window_index'
              412  LOAD_FAST                'context_left_size'
              414  BINARY_ADD       

 L. 623       416  LOAD_FAST                'window_index'
              418  LOAD_FAST                'context_left_size'
              420  BINARY_ADD       
              422  LOAD_FAST                'unit_seq_length'
              424  BINARY_ADD       
              426  BUILD_SLICE_2         2 
              428  BINARY_SUBSCR    
              430  CALL_FUNCTION_1       1  '1 positional argument'
              432  STORE_FAST               'unit_type'

 L. 628       434  LOAD_FAST                'context_type'
              436  LOAD_FAST                'context_types'
              438  COMPARE_OP               not-in
              440  POP_JUMP_IF_FALSE   454  'to 454'

 L. 629       444  LOAD_FAST                'context_types'
              446  LOAD_ATTR                append
              448  LOAD_FAST                'context_type'
              450  CALL_FUNCTION_1       1  '1 positional argument'
              452  POP_TOP          
            454_0  COME_FROM           440  '440'

 L. 630       454  LOAD_FAST                'unit_type'
              456  LOAD_FAST                'unit_types'
              458  COMPARE_OP               not-in
              460  POP_JUMP_IF_FALSE   474  'to 474'

 L. 631       464  LOAD_FAST                'unit_types'
              466  LOAD_ATTR                append
              468  LOAD_FAST                'unit_type'
              470  CALL_FUNCTION_1       1  '1 positional argument'
              472  POP_TOP          
            474_0  COME_FROM           460  '460'

 L. 634       474  LOAD_FAST                'context_type'
              476  LOAD_FAST                'unit_type'
              478  BUILD_TUPLE_2         2 
              480  STORE_FAST               'type_pair'

 L. 635       482  LOAD_FAST                'freq'
              484  LOAD_ATTR                get
              486  LOAD_FAST                'type_pair'
              488  LOAD_CONST               0
              490  CALL_FUNCTION_2       2  '2 positional arguments'
              492  LOAD_CONST               1
              494  BINARY_ADD       
              496  LOAD_FAST                'freq'
              498  LOAD_FAST                'type_pair'
              500  STORE_SUBSCR     

 L. 637       502  LOAD_FAST                'progress_callback'
              504  POP_JUMP_IF_FALSE   284  'to 284'

 L. 638       508  LOAD_FAST                'progress_callback'
              510  CALL_FUNCTION_0       0  '0 positional arguments'
              512  POP_TOP          
              514  JUMP_BACK           284  'to 284'
              518  POP_BLOCK        
              520  JUMP_FORWARD        782  'to 782'
              524  ELSE                     '782'

 L. 644       524  LOAD_GLOBAL              list

 L. 645       526  LOAD_GLOBAL              set

 L. 646       528  LOAD_FAST                'unit_list'

 L. 647       530  LOAD_FAST                'context_left_size'

 L. 648       532  LOAD_GLOBAL              len
              534  LOAD_FAST                'units'
              536  LOAD_STR                 'segmentation'
              538  BINARY_SUBSCR    
              540  CALL_FUNCTION_1       1  '1 positional argument'
              542  LOAD_FAST                'context_right_size'
              544  BINARY_SUBTRACT  
              546  BUILD_SLICE_2         2 
              548  BINARY_SUBSCR    
              550  CALL_FUNCTION_1       1  '1 positional argument'
              552  CALL_FUNCTION_1       1  '1 positional argument'
              554  STORE_FAST               'unit_types'

 L. 654       556  SETUP_LOOP          782  'to 782'
              558  LOAD_GLOBAL              range

 L. 655       560  LOAD_GLOBAL              len
              562  LOAD_FAST                'units'
              564  LOAD_STR                 'segmentation'
              566  BINARY_SUBSCR    
              568  CALL_FUNCTION_1       1  '1 positional argument'
              570  LOAD_FAST                'window_size'
              572  LOAD_CONST               1
              574  BINARY_SUBTRACT  
              576  BINARY_SUBTRACT  
              578  CALL_FUNCTION_1       1  '1 positional argument'
              580  GET_ITER         
              582  FOR_ITER            780  'to 780'
              584  STORE_FAST               'window_index'

 L. 660       586  LOAD_FAST                'str_indices'

 L. 661       588  LOAD_FAST                'window_index'
              590  LOAD_FAST                'window_index'
              592  LOAD_FAST                'window_size'
              594  BINARY_ADD       
              596  BUILD_SLICE_2         2 
              598  BINARY_SUBSCR    
              600  STORE_FAST               'idx_sequence'

 L. 664       602  LOAD_FAST                'merge_strings'
              604  UNARY_NOT        
              606  POP_JUMP_IF_FALSE   650  'to 650'

 L. 665       610  LOAD_FAST                'idx_sequence'
              612  LOAD_ATTR                count
              614  LOAD_FAST                'idx_sequence'
              616  LOAD_CONST               0
              618  BINARY_SUBSCR    
              620  CALL_FUNCTION_1       1  '1 positional argument'
              622  LOAD_GLOBAL              len
              624  LOAD_FAST                'idx_sequence'
              626  CALL_FUNCTION_1       1  '1 positional argument'
              628  COMPARE_OP               !=
              630  POP_JUMP_IF_FALSE   650  'to 650'

 L. 667       634  LOAD_FAST                'progress_callback'
              636  POP_JUMP_IF_FALSE   582  'to 582'

 L. 668       640  LOAD_FAST                'progress_callback'
              642  CALL_FUNCTION_0       0  '0 positional arguments'
              644  POP_TOP          

 L. 669       646  CONTINUE            582  'to 582'
            650_0  COME_FROM           606  '606'

 L. 672       650  LOAD_STR                 '%s%s%s'

 L. 673       652  LOAD_FAST                'seq_join'

 L. 674       654  LOAD_FAST                'unit_list'
              656  LOAD_FAST                'window_index'
              658  LOAD_FAST                'window_index'
              660  LOAD_FAST                'context_left_size'
              662  BINARY_ADD       
              664  BUILD_SLICE_2         2 
              666  BINARY_SUBSCR    
              668  CALL_FUNCTION_1       1  '1 positional argument'

 L. 676       670  LOAD_FAST                'unit_pos_marker'

 L. 677       672  LOAD_FAST                'seq_join'

 L. 678       674  LOAD_FAST                'unit_list'

 L. 679       676  LOAD_FAST                'window_index'
              678  LOAD_FAST                'context_left_size'
              680  BINARY_ADD       
              682  LOAD_CONST               1
              684  BINARY_ADD       

 L. 680       686  LOAD_FAST                'window_index'
              688  LOAD_FAST                'window_size'
              690  BINARY_ADD       
              692  BUILD_SLICE_2         2 
              694  BINARY_SUBSCR    
              696  CALL_FUNCTION_1       1  '1 positional argument'
              698  BUILD_TUPLE_3         3 
              700  BINARY_MODULO    
              702  STORE_FAST               'context_type'

 L. 686       704  LOAD_FAST                'unit_list'
              706  LOAD_FAST                'window_index'
              708  LOAD_FAST                'context_left_size'
              710  BINARY_ADD       
              712  BINARY_SUBSCR    
              714  STORE_FAST               'unit_type'

 L. 689       716  LOAD_FAST                'context_type'
              718  LOAD_FAST                'context_types'
              720  COMPARE_OP               not-in
              722  POP_JUMP_IF_FALSE   736  'to 736'

 L. 690       726  LOAD_FAST                'context_types'
              728  LOAD_ATTR                append
              730  LOAD_FAST                'context_type'
              732  CALL_FUNCTION_1       1  '1 positional argument'
              734  POP_TOP          
            736_0  COME_FROM           722  '722'

 L. 693       736  LOAD_FAST                'context_type'
              738  LOAD_FAST                'unit_type'
              740  BUILD_TUPLE_2         2 
              742  STORE_FAST               'type_pair'

 L. 694       744  LOAD_FAST                'freq'
              746  LOAD_ATTR                get
              748  LOAD_FAST                'type_pair'
              750  LOAD_CONST               0
              752  CALL_FUNCTION_2       2  '2 positional arguments'
              754  LOAD_CONST               1
              756  BINARY_ADD       
              758  LOAD_FAST                'freq'
              760  LOAD_FAST                'type_pair'
              762  STORE_SUBSCR     

 L. 696       764  LOAD_FAST                'progress_callback'
              766  POP_JUMP_IF_FALSE   582  'to 582'

 L. 697       770  LOAD_FAST                'progress_callback'
              772  CALL_FUNCTION_0       0  '0 positional arguments'
              774  POP_TOP          
              776  JUMP_BACK           582  'to 582'
              780  POP_BLOCK        
            782_0  COME_FROM_LOOP      556  '556'
            782_1  COME_FROM           520  '520'
            782_2  COME_FROM           186  '186'

 L. 701       782  LOAD_GLOBAL              IntPivotCrosstab

 L. 702       784  LOAD_FAST                'context_types'

 L. 703       786  LOAD_FAST                'unit_types'

 L. 704       788  LOAD_FAST                'freq'

 L. 705       790  LOAD_STR                 '__unit__'

 L. 706       792  LOAD_STR                 'string'

 L. 707       794  LOAD_STR                 '__context__'

 L. 708       796  LOAD_STR                 'string'

 L. 709       798  LOAD_GLOBAL              dict
              800  LOAD_LISTCOMP            '<code_object <listcomp>>'
              802  LOAD_STR                 'count_in_chain.<locals>.<listcomp>'
              804  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              806  LOAD_FAST                'unit_types'
              808  GET_ITER         
              810  CALL_FUNCTION_1       1  '1 positional argument'
              812  CALL_FUNCTION_1       1  '1 positional argument'

 L. 710       814  LOAD_CONST               None

 L. 711       816  LOAD_CONST               0

 L. 712       818  LOAD_CONST               None
              820  CALL_FUNCTION_11     11  '11 positional arguments'
              822  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_FORWARD' instruction at offset 520


def length_in_context(units=None, averaging=None, contexts=None, progress_callback=None):
    """Compute length of segmentation / av. length of units in contexts.

    Parameter averaging is a dict with the following keys and values:
    KEY                     VALUE                           DEFAULT
    segmentation            averaging unit segmentation     None
    std_deviation           compute standard deviation      False

    Parameter contexts is a dict with the following keys and values:
    KEY                     VALUE                           DEFAULT
    segmentation            context segmentation            None
    annotation_key          annotation to be used           None
    merge                   merge contexts together?        False

    NB: When some form of averaging is performed with large segmentations,
    execution can be *dramatically* slower if standard deviation is
    computed.

    Returns a Table.
    """
    default_contexts = {'segmentation':None, 
     'annotation_key':None, 
     'merge':False}
    default_averaging = {'segmentation':None, 
     'std_deviation':False}
    if contexts is not None:
        default_contexts.update(contexts)
    else:
        contexts = default_contexts
        if averaging is not None:
            default_averaging.update(averaging)
        averaging = default_averaging
        values = dict()
        context_types = list()
        col_ids = list()
        if contexts['segmentation'] is not None and units is not None:
            context_annotation_key = contexts['annotation_key']
            context_segmentation = contexts['segmentation']
            if contexts['merge']:
                context_types = [
                 '__global__']
            else:
                if context_annotation_key is not None:
                    context_list = [c.annotations.get(context_annotation_key, '__none__') for c in context_segmentation if c.annotations is not None]
                else:
                    context_list = [c.get_content() for c in context_segmentation if c is not None]
            if averaging['segmentation'] is not None:
                lengths = dict()
                for context_index, context_segment in enumerate(contexts['segmentation']):
                    context_token = context_segment
                    if contexts['merge']:
                        context_type = '__global__'
                    else:
                        context_type = context_list[context_index]
                        if context_type not in context_types:
                            context_types.append(context_type)
                        averaging_units = context_token.get_contained_segments(averaging['segmentation'])
                        my_lengths = [len(averaging_unit.get_contained_segments(units)) for averaging_unit in averaging_units]
                        try:
                            lengths[context_type].extend(my_lengths)
                        except KeyError:
                            lengths[context_type] = my_lengths

                    if progress_callback:
                        progress_callback()

                print(lengths)
                for context_type in context_types:
                    values[(context_type, '__length_average__')] = np.mean(lengths[context_type])
                    values[(context_type, '__length_count__')] = len(lengths[context_type])
                    if averaging['std_deviation']:
                        values[(context_type, '__length_std_deviation__')] = np.std(lengths[context_type])

                if len(values) > 0:
                    col_ids.append('__length_average__')
                    col_ids.append('__length_count__')
                    if averaging['std_deviation']:
                        col_ids.append('__length_std_deviation__')
            else:
                for context_index, context_segment in enumerate(contexts['segmentation']):
                    context_token = context_segment
                    if not contexts['merge']:
                        context_type = context_list[context_index]
                        if context_type not in context_types:
                            context_types.append(context_type)
                        values[(context_type, '__length__')] = values.get((
                         context_type, '__length__'), 0) + len(context_token.get_contained_segments(units))
                        if progress_callback:
                            progress_callback()

            if len(values) > 0:
                col_ids.append('__length__')
        else:
            if units is not None:
                if averaging['segmentation'] is not None:
                    context_type = '__global__'
                    context_types.append(context_type)
                    lengths = [len(averaging_unit.get_contained_segments(units)) for averaging_unit in averaging['segmentation']]
                    values[(context_type, '__length_average__')] = np.mean(lengths)
                    values[(context_type, '__length_count__')] = len(lengths)
                    if averaging['std_deviation']:
                        values[(context_type, '__length_std_deviation__')] = np.std(lengths)
                    if len(values) > 0:
                        col_ids.append('__length_average__')
                        col_ids.append('__length_count__')
                        if averaging['std_deviation']:
                            col_ids.append('__length_std_deviation__')
                else:
                    context_type = '__global__'
                    context_types.append(context_type)
                    values[(context_type, '__length__')] = len(units)
                    if len(values) > 0:
                        col_ids.append('__length__')
            if len(values) > 0:
                if len(context_types) == 0:
                    context_types.append(context_type)
            if averaging['segmentation'] is not None:
                length_col_name = '__length_average__'
            else:
                length_col_name = '__length__'
        context_types[:] = [c for c in context_types if (
         c, length_col_name) in values if values[(c, length_col_name)]]
        values = dict((key, value) for key, value in iteritems(values) if key[0] in context_types)
        if len(context_types):
            if isinstance(context_types[0], int):
                header_type = 'continuous'
        header_type = 'string'
    return Table(context_types, col_ids, values, '__col__', 'string', '__context__', header_type, dict([(c, 'continuous') for c in col_ids]), None, None, None)


def length_in_window(units=None, averaging=None, window_size=1, progress_callback=None):
    """Compute average length of units in sliding window.

    Parameter averaging is a dict with the following keys and values:
    KEY                     VALUE                           DEFAULT
    segmentation            averaging unit segmentation     None
    std_deviation           compute standard deviation      False

    NB: When some form of averaging is performed with large segmentations,
    execution can be dramatically slower if standard deviation is
    computed.

    Returns a Table.
    """
    default_averaging = {'segmentation':None, 
     'std_deviation':False}
    if averaging is not None:
        default_averaging.update(averaging)
    averaging = default_averaging
    values = dict()
    window_type = 0
    col_ids = list()
    if units is not None and averaging['segmentation'] is not None and window_size <= len(averaging['segmentation']):
        averaging_segmentation = averaging['segmentation']
        if averaging['std_deviation']:
            lengths = [len(a.get_contained_segments(units)) for a in averaging_segmentation[:window_size]]
            sum_values = sum(lengths)
            sum_squares = sum(l * l for l in lengths)
            average = sum_values / window_size
            stdev = math.sqrt(sum_squares / window_size - average * average)
            window_type = 1
            values[('1', '__length_average__')] = average
            values[('1', '__length_std_deviation__')] = stdev
            values[('1', '__length_count__')] = window_size
            if progress_callback:
                progress_callback()
            for window_index in range(1, len(averaging_segmentation) - (window_size - 1)):
                window_type = window_index + 1
                removed_length = lengths.pop(0)
                sum_values -= removed_length
                sum_squares -= removed_length * removed_length
                added_length = len(averaging_segmentation[(window_index + window_size - 1)].get_contained_segments(units))
                lengths.append(added_length)
                sum_values += added_length
                sum_squares += added_length * added_length
                average = sum_values / window_size
                stdev = math.sqrt(sum_squares / window_size - average * average)
                window_str = text(window_type)
                values[(window_str, '__length_average__')] = average
                values[(window_str, '__length_std_deviation__')] = stdev
                values[(window_str, '__length_count__')] = window_size
                if progress_callback:
                    progress_callback()

        else:
            lengths = [len(a.get_contained_segments(units)) for a in averaging_segmentation[:window_size]]
            sum_values = sum(lengths)
            average = sum_values / window_size
            window_type = 1
            values[('1', '__length_average__')] = average
            values[('1', '__length_count__')] = window_size
            if progress_callback:
                progress_callback()
            for window_index in range(1, len(averaging_segmentation) - (window_size - 1)):
                window_type = window_index + 1
                removed_length = lengths.pop(0)
                sum_values -= removed_length
                added_length = len(averaging_segmentation[(window_index + window_size - 1)].get_contained_segments(units))
                lengths.append(added_length)
                sum_values += added_length
                average = sum_values / window_size
                window_str = text(window_type)
                values[(window_str, '__length_average__')] = average
                values[(window_str, '__length_count__')] = window_size
                if progress_callback:
                    progress_callback()

        if len(values) > 0:
            col_ids.append('__length_average__')
            if averaging['std_deviation']:
                col_ids.append('__length_std_deviation__')
            col_ids.append('__length_count__')
    return Table([text(i) for i in range(1, window_type + 1)], col_ids, values, '__col__', 'string', '__context__', 'continuous', dict([(c, 'continuous') for c in col_ids]), None, None, None)


def variety_in_context(units=None, categories=None, contexts=None, measure_per_category=False, apply_resampling=False, subsample_size=None, num_subsamples=None, progress_callback=None):
    """Get variety of units in contexts.

    Parameter units is a dict with the following keys and values:
    KEY                     VALUE                           DEFAULT
    segmentation            unit segmentation               None
    annotation_key          annotation to be considered     None
    seq_length              length of unit sequences        1
    weighting               Bool                            False

    Parameter categories is a dict with the following keys and values:
    KEY                     VALUE                           DEFAULT
    annotation_key          annotation to be considered     None
    weighting               Bool                            False
    adjust                  Bool                            True

    Parameter contexts is a dict with the following keys and values:
    KEY                     VALUE                           DEFAULT
    segmentation            context segmentation            None
    annotation_key          annotation to be considered     None
    merge                   merge contexts together?        False

    Returns a Table.
    """
    default_units = {'segmentation':None, 
     'annotation_key':None, 
     'seq_length':1, 
     'weighting':False}
    default_categories = {'annotation_key':None, 
     'weighting':False, 
     'adjust':True}
    default_contexts = {'segmentation':None, 
     'annotation_key':None, 
     'merge':False, 
     'weighting':False}
    if units is not None:
        default_units.update(units)
    units = default_units
    if categories is not None:
        default_categories.update(categories)
    else:
        categories = default_categories
        if contexts is not None:
            default_contexts.update(contexts)
        else:
            contexts = default_contexts
            target_NLTTR = 0
            if measure_per_category:
                if units['seq_length'] > 1:
                    raise ValueError('Cannot measure diversity per category when sequence length is greater than 1')
                new_annotation_key = generate_random_annotation_key(units['segmentation'])
                category_delimiter = get_unused_char_in_segmentation(units['segmentation'], categories['annotation_key'])
                recoded_units = prepend_unit_with_category(units['segmentation'], category_delimiter, new_annotation_key, categories['annotation_key'], units['annotation_key'])
                counts = count_in_context({'segmentation':recoded_units, 
                 'annotation_key':new_annotation_key, 
                 'seq_length':units['seq_length']}, contexts, progress_callback)
                if apply_resampling and categories['adjust']:
                    category_counts = count_in_context({'segmentation':units['segmentation'], 
                     'annotation_key':categories['annotation_key'], 
                     'seq_length':units['seq_length']}, contexts, progress_callback)
                    expected_varieties = list()
                    for row_id in category_counts.row_ids:
                        row = tuple_to_simple_dict(category_counts.values, row_id)
                        try:
                            expected_varieties.append(get_expected_subsample_variety(row, subsample_size))
                        except ValueError:
                            pass

                    if expected_varieties:
                        target_NLTTR = max(expected_varieties) / subsample_size
            else:
                counts = count_in_context(units, contexts, progress_callback)
                category_delimiter = None
            new_values = dict()
            if len(counts.row_ids) == 1:
                if counts.row_ids[0] == '__global__':
                    default_row_id = '__global__'
            default_row_id = None
        for row_id in counts.row_ids:
            row = tuple_to_simple_dict(counts.values, row_id)
            if default_row_id is not None:
                row_id = default_row_id
            if apply_resampling:
                if measure_per_category:
                    if categories['adjust']:
                        cat_row = tuple_to_simple_dict(category_counts.values, row_id)
                        if subsample_size > sum(cat_row.values()):
                            continue
                        size_low, size_high = 2, subsample_size
                        size_tmp = size_high
                        NLTTR_tmp = get_expected_subsample_variety(cat_row, size_tmp) / size_tmp
                        while True:
                            if NLTTR_tmp == target_NLTTR or size_low == size_high:
                                break
                            else:
                                if size_high - size_low == 1:
                                    high = get_expected_subsample_variety(cat_row, size_high) / size_high
                                    low = get_expected_subsample_variety(cat_row, size_low) / size_low
                                    if high - target_NLTTR < target_NLTTR - low:
                                        size_tmp = size_high
                                    else:
                                        size_tmp = size_low
                                    break
                                size_tmp = iround((size_low + size_high) / 2)
                                NLTTR_tmp = get_expected_subsample_variety(cat_row, size_tmp) / size_tmp
                                if NLTTR_tmp < target_NLTTR:
                                    size_high = size_tmp
                                elif NLTTR_tmp > target_NLTTR:
                                    pass
                                size_low = size_tmp

                    else:
                        size_tmp = subsample_size
                    varieties = list()
                    for i in range(num_subsamples):
                        try:
                            sampled_row = sample_dict(row, size_tmp)
                            varieties.append(get_variety(sampled_row,
                              unit_weighting=(units['weighting']),
                              category_weighting=(categories['weighting']),
                              category_delimiter=category_delimiter))
                        except ValueError:
                            break

                    if varieties:
                        new_values[(row_id, '__variety_average__')], new_values[(row_id, '__variety_std_deviation__')] = get_average(varieties)
                        if categories['adjust']:
                            new_values[(row_id, '__subsample_size__')] = size_tmp
                        new_values[(row_id, '__variety_count__')] = num_subsamples
                else:
                    if units['weighting']:
                        varieties = list()
                        for i in range(num_subsamples):
                            try:
                                sampled_row = sample_dict(row, subsample_size)
                                varieties.append(get_variety(sampled_row,
                                  unit_weighting=(units['weighting']),
                                  category_weighting=(categories['weighting']),
                                  category_delimiter=category_delimiter))
                            except ValueError:
                                break

                        if varieties:
                            new_values[(row_id, '__variety_average__')], new_values[(row_id, '__variety_std_deviation__')] = get_average(varieties)
                            new_values[(row_id, '__variety_count__')] = num_subsamples
                        else:
                            try:
                                new_values[(row_id, '__expected_variety__')] = get_expected_subsample_variety(row, subsample_size)
                            except ValueError:
                                pass

                    else:
                        new_values[(row_id, '__variety__')] = get_variety(row,
                          unit_weighting=(units['weighting']),
                          category_weighting=(categories['weighting']),
                          category_delimiter=category_delimiter)
                if progress_callback:
                    progress_callback()

        if default_row_id is not None:
            counts.row_ids[0] = default_row_id
        if apply_resampling:
            if measure_per_category:
                new_col_ids = ['__variety_average__',
                 '__variety_std_deviation__']
                if categories['adjust']:
                    new_col_ids.append('__subsample_size__')
                new_col_ids.append('__variety_count__')
            else:
                if units['weighting']:
                    new_col_ids = ['__variety_average__',
                     '__variety_std_deviation__',
                     '__variety_count__']
                else:
                    new_col_ids = ['__expected_variety__']
        else:
            new_col_ids = [
             '__variety__']
    return Table(counts.row_ids[:], new_col_ids, new_values, '__col__', 'string', counts.header_col_id, counts.header_col_type, dict([(c, 'continuous') for c in new_col_ids]), None, None, None)


def variety_in_window(units=None, categories=None, measure_per_category=False, window_size=1, apply_resampling=False, subsample_size=None, num_subsamples=None, progress_callback=None):
    """Get variety of units in sliding window.

    Parameter units is a dict with the following keys and values:
    KEY                     VALUE                           DEFAULT
    segmentation            unit segmentation               None
    annotation_key          annotation to be considered     None
    seq_length              length of unit sequences        1
    weighting               Bool                            False

    Parameter categories is a dict with the following keys and values:
    KEY                     VALUE                           DEFAULT
    annotation_key          annotation to be considered     None
    weighting               Bool                            False
    adjust                  Bool                            True

    Returns a Table.
    """
    default_units = {'segmentation':None, 
     'annotation_key':None, 
     'seq_length':1, 
     'weighting':False}
    default_categories = {'annotation_key':None, 
     'weighting':False, 
     'adjust':True}
    if units is not None:
        default_units.update(units)
    else:
        units = default_units
        if categories is not None:
            default_categories.update(categories)
        categories = default_categories
        target_NLTTR = 0
        if measure_per_category:
            if units['seq_length'] > 1:
                raise ValueError('Cannot measure diversity per category when sequence length is greater than 1')
            new_annotation_key = generate_random_annotation_key(units['segmentation'])
            category_delimiter = get_unused_char_in_segmentation(units['segmentation'], categories['annotation_key'])
            recoded_units = prepend_unit_with_category(units['segmentation'], category_delimiter, new_annotation_key, categories['annotation_key'], units['annotation_key'])
            counts = count_in_window({'segmentation':recoded_units, 
             'annotation_key':new_annotation_key, 
             'seq_length':units['seq_length'], 
             'weighting':units['weighting']}, window_size, progress_callback)
            if apply_resampling and categories['adjust']:
                category_counts = count_in_window({'segmentation':units['segmentation'], 
                 'annotation_key':categories['annotation_key'], 
                 'seq_length':units['seq_length']}, window_size, progress_callback)
                expected_varieties = list()
                for row_id in category_counts.row_ids:
                    row = tuple_to_simple_dict(category_counts.values, row_id)
                    try:
                        expected_varieties.append(get_expected_subsample_variety(row, subsample_size))
                    except ValueError:
                        pass

                if expected_varieties:
                    target_NLTTR = max(expected_varieties) / subsample_size
        else:
            counts = count_in_window(units, window_size, progress_callback)
            category_delimiter = None
        new_values = dict()
        for row_id in counts.row_ids:
            row = tuple_to_simple_dict(counts.values, row_id)
            if apply_resampling:
                if measure_per_category:
                    if categories['adjust']:
                        cat_row = tuple_to_simple_dict(category_counts.values, row_id)
                        if subsample_size > sum(cat_row.values()):
                            continue
                        size_low, size_high = 2, subsample_size
                        size_tmp = size_high
                        NLTTR_tmp = get_expected_subsample_variety(cat_row, size_tmp) / size_tmp
                        while True:
                            if NLTTR_tmp == target_NLTTR or size_low == size_high:
                                break
                            else:
                                if size_high - size_low == 1:
                                    high = get_expected_subsample_variety(cat_row, size_high) / size_high
                                    low = get_expected_subsample_variety(cat_row, size_low) / size_low
                                    if high - target_NLTTR < target_NLTTR - low:
                                        size_tmp = size_high
                                    else:
                                        size_tmp = size_low
                                    break
                                size_tmp = iround((size_low + size_high) / 2)
                                NLTTR_tmp = get_expected_subsample_variety(cat_row, size_tmp) / size_tmp
                                if NLTTR_tmp < target_NLTTR:
                                    size_high = size_tmp
                                elif NLTTR_tmp > target_NLTTR:
                                    pass
                                size_low = size_tmp

                    else:
                        size_tmp = subsample_size
                    varieties = list()
                    for i in range(num_subsamples):
                        try:
                            sampled_row = sample_dict(row, size_tmp)
                            varieties.append(get_variety(sampled_row,
                              unit_weighting=(units['weighting']),
                              category_weighting=(categories['weighting']),
                              category_delimiter=category_delimiter))
                        except ValueError:
                            break

                    if varieties:
                        new_values[(row_id, '__variety_average__')], new_values[(row_id, '__variety_std_deviation__')] = get_average(varieties)
                        new_values[(row_id, '__subsample_size__')] = size_tmp
                        new_values[(row_id, '__variety_count__')] = num_subsamples
                else:
                    if units['weighting']:
                        varieties = list()
                        for i in range(num_subsamples):
                            try:
                                sampled_row = sample_dict(row, subsample_size)
                                varieties.append(get_variety(sampled_row,
                                  unit_weighting=(units['weighting']),
                                  category_weighting=(categories['weighting']),
                                  category_delimiter=category_delimiter))
                            except ValueError:
                                break

                        if varieties:
                            new_values[(row_id, '__variety_average__')], new_values[(row_id, '__variety_std_deviation__')] = get_average(varieties)
                            new_values[(row_id, '__variety_count__')] = num_subsamples
                        else:
                            try:
                                new_values[(row_id, '__expected_variety__')] = get_expected_subsample_variety(row, subsample_size)
                            except ValueError:
                                pass

                    else:
                        new_values[(row_id, '__variety__')] = get_variety(row,
                          unit_weighting=(units['weighting']),
                          category_weighting=(categories['weighting']),
                          category_delimiter=category_delimiter)
                if progress_callback:
                    progress_callback()

        if apply_resampling:
            if measure_per_category:
                new_col_ids = ['__variety_average__',
                 '__variety_std_deviation__',
                 '__subsample_size__',
                 '__variety_count__']
            else:
                if units['weighting']:
                    new_col_ids = ['__variety_average__',
                     '__variety_std_deviation__',
                     '__variety_count__']
                else:
                    new_col_ids = ['__expected_variety__']
        else:
            new_col_ids = [
             '__variety__']
    return Table(counts.row_ids[:], new_col_ids, new_values, '__col__', 'string', '__context__', 'continuous', dict([(c, 'continuous') for c in new_col_ids]), None, None, None)


def annotate_contexts(units=None, multiple_values=None, contexts=None, progress_callback=None):
    """Annotate contexts.

    Parameter units is a dict with the following keys and values:
    KEY                     VALUE                           DEFAULT
    segmentation            unit segmentation               None
    annotation_key          annotation to be added          None
    seq_length              length of unit sequences        1
    intra_seq_delimiter     string for joining sequences    '#'

    Parameter multiple_values is a dict with following keys and values:
    KEY                     VALUE                           DEFAULT
    sort_order              order for sorting values        'Frequency'
    reverse                 reverse sort order?             False
    keep_only_first         keep only first value?          True
    value_delimiter         string for joining values       '|'

    Parameter contexts is a dict with the following keys and values:
    KEY                     VALUE                           DEFAULT
    segmentation            context segmentation            None
    annotation_key          annotation to annotated (sic)   None
    merge                   merge contexts together?        False

    Returns a table.
    """
    default_units = {'segmentation':None, 
     'annotation_key':None, 
     'seq_length':1, 
     'intra_seq_delimiter':'#'}
    default_multiple_values = {'sort_order':'Frequency', 
     'reverse':True, 
     'keep_only_first':True, 
     'value_delimiter':'|'}
    default_contexts = {'segmentation':None, 
     'annotation_key':None, 
     'merge':False}
    if units is not None:
        default_units.update(units)
    units = default_units
    if multiple_values is not None:
        default_multiple_values.update(multiple_values)
    multiple_values = default_multiple_values
    if contexts is not None:
        default_contexts.update(contexts)
    contexts = default_contexts
    counts = count_in_context(units, contexts, progress_callback)
    new_values = dict()
    for row_id in counts.row_ids:
        row = tuple_to_simple_dict(counts.values, row_id)
        if multiple_values['sort_order'] == 'Frequency':
            annotations = sorted(row,
              key=(row.__getitem__),
              reverse=(multiple_values['reverse']))
        else:
            if multiple_values['sort_order'] == 'ASCII':
                annotations = sorted((row.keys()),
                  reverse=(multiple_values['reverse']))
        if multiple_values['keep_only_first']:
            new_values[(row_id, '__annotation__')] = annotations[0]
        else:
            new_values[(row_id, '__annotation__')] = multiple_values['value_delimiter'].join(text(a) for a in annotations)

    return Table(counts.row_ids[:], [
     '__annotation__'], new_values, '__col__', 'string', counts.header_col_id, counts.header_col_type, {'__annotation__': 'discrete'}, '__annotation__', None, None)


def context(units=None, contexts=None, progress_callback=None):
    """Concordance based on containing segmentation.

    Parameter units is a dict with the following keys and values:
    KEY                     VALUE                           DEFAULT
    segmentation            unit segmentation               None
    annotation_key          annotation to be displayed      None
    separate_annotation     display annotation in own col.  True

    Parameter contexts is a dict with the following keys and values:
    KEY                     VALUE                           DEFAULT
    segmentation            context segmentation            None
    annotation_key          annotation to be displayed      None
    max_num_chars           maximum number of chars         None

    Returns a table.
    """
    default_units = {'segmentation':None, 
     'annotation_key':None, 
     'separate_annotation':True}
    default_contexts = {'segmentation':None, 
     'annotation_key':None, 
     'max_num_chars':None}
    if units is not None:
        default_units.update(units)
    units = default_units
    if contexts is not None:
        default_contexts.update(contexts)
    contexts = default_contexts
    row_id = 0
    new_values = dict()
    has_imm_left = False
    has_imm_right = False
    unit_segmentation = units['segmentation']
    unit_annotation_key = units['annotation_key']
    context_segmentation = contexts['segmentation']
    context_annotation_key = contexts['annotation_key']
    max_num_chars = contexts['max_num_chars']
    for context_index, context_segment in enumerate(context_segmentation):
        context_token = context_segment
        if context_annotation_key is not None:
            context_annotation = context_token.annotations.get(context_annotation_key, '__none__')
        if max_num_chars is None:
            max_len = len(context_token.get_content())
        else:
            max_len = max_num_chars
        for unit_index in context_token.get_contained_segment_indices(unit_segmentation):
            row_id += 1
            new_values[(row_id, '__pos__')] = context_index + 1
            unit_token = unit_segmentation[unit_index]
            new_values[(row_id, '__key_segment__')] = unit_token.get_content()
            if unit_annotation_key is not None:
                annotation_value = unit_token.annotations.get(unit_annotation_key, '__none__')
                if units['separate_annotation']:
                    new_values[(row_id, unit_annotation_key)] = annotation_value
                else:
                    new_values[(row_id, '__key_segment__')] = annotation_value
            unit_start = unit_token.start or 0
            unit_end = unit_token.end or len(Segmentation.get_data(unit_token.str_index))
            context_start = context_token.start or 0
            context_end = context_token.end or len(Segmentation.get_data(context_token.str_index))
            if context_start < unit_start:
                imm_left_start = max(context_start, unit_start - max_len)
                if unit_start > imm_left_start:
                    new_values[(row_id, '__left__')] = Segmentation.get_data(unit_token.str_index)[imm_left_start:unit_start]
                    has_imm_left = True
            if context_end > unit_end:
                imm_right_end = min(context_end, unit_end + max_len)
                if imm_right_end > unit_end:
                    new_values[(row_id, '__right__')] = Segmentation.get_data(unit_token.str_index)[unit_end:imm_right_end]
                    has_imm_right = True
                if context_annotation_key is not None:
                    new_values[(row_id, context_annotation_key)] = context_annotation

        if progress_callback:
            progress_callback()

    col_ids = ['__pos__']
    if has_imm_left:
        col_ids.append('__left__')
    col_ids.append('__key_segment__')
    if has_imm_right:
        col_ids.append('__right__')
    if unit_annotation_key is not None:
        if units['separate_annotation']:
            col_ids.append(unit_annotation_key)
    if context_annotation_key is not None:
        col_ids.append(context_annotation_key)
    col_types = dict([(p, 'string') for p in col_ids])
    col_types['__pos__'] = 'continuous'
    return Table(range(1, row_id + 1), col_ids, new_values, '__col__', 'string', '__id__', 'continuous', col_types, None, None, None)


def neighbors(units=None, contexts=None, progress_callback=None):
    """Concordance based on neighboring segments.

    Parameter units is a dict with the following keys and values:
    KEY                     VALUE                           DEFAULT
    segmentation            unit segmentation               None
    annotation_key          annotation to be displayed      None
    separate_annotation     display annotation in own col.  True

    Parameter contexts is a dict with the following keys and values:
    KEY                     VALUE                           DEFAULT
    segmentation            context segmentation            None
    annotation_key          annotation to be displayed      None
    max_distance            maximum distance of neighbors   None
    merge_strings           treat strings as contiguous?    False

    Returns a table.
    """
    default_units = {'segmentation':None, 
     'annotation_key':None, 
     'separate_annotation':True}
    default_contexts = {'segmentation':None, 
     'annotation_key':None, 
     'max_distance':None, 
     'merge_strings':False}
    if units is not None:
        default_units.update(units)
    else:
        units = default_units
        if contexts is not None:
            default_contexts.update(contexts)
        contexts = default_contexts
        row_id = 0
        new_values = dict()
        if contexts['max_distance'] is not None:
            adjacent_positions = range(1, contexts['max_distance'] + 1)
        else:
            adjacent_positions = range(1, len(contexts['segmentation']))
    unit_segmentation = units['segmentation']
    unit_annotation_key = units['annotation_key']
    context_annotation_key = contexts['annotation_key']
    context_segmentation = contexts['segmentation']
    merge_strings = contexts['merge_strings']
    for context_index, context_segment in enumerate(context_segmentation):
        context_token = context_segment
        for unit_index in context_token.get_contained_segment_indices(unit_segmentation):
            row_id += 1
            new_values[(row_id, '__pos__')] = context_index + 1
            unit_token = unit_segmentation[unit_index]
            new_values[(row_id, '__key_segment__')] = unit_token.get_content()
            if unit_annotation_key is not None:
                annotation_value = unit_token.annotations.get(unit_annotation_key, '__none__')
                if units['separate_annotation']:
                    new_values[(row_id, unit_annotation_key)] = annotation_value
                else:
                    new_values[(row_id, '__key_segment__')] = annotation_value
            unit_token_str_index = unit_token.get_real_str_index()
            for pos in adjacent_positions:
                left_index = context_index - pos
                if left_index >= 0:
                    left_token = context_segmentation[left_index]
                    if merge_strings or unit_token_str_index == left_token.get_real_str_index():
                        if context_annotation_key is not None:
                            string_value = left_token.annotations.get(context_annotation_key, '__none__')
                        else:
                            string_value = left_token.get_content()
                        new_values[(row_id, text(pos) + 'L')] = string_value
                right_index = context_index + pos
                if right_index < len(context_segmentation):
                    right_token = context_segmentation[right_index]
                    if merge_strings or unit_token_str_index == right_token.get_real_str_index():
                        if context_annotation_key is not None:
                            string_value = right_token.annotations.get(context_annotation_key, '__none__')
                        else:
                            string_value = right_token.get_content()
                        new_values[(row_id, text(pos) + 'R')] = string_value

        if progress_callback:
            progress_callback()

    col_ids = ['__pos__']
    col_ids.extend([text(p) + 'L' for p in reversed(adjacent_positions)])
    col_ids.append('__key_segment__')
    col_ids.extend([text(p) + 'R' for p in adjacent_positions])
    if unit_annotation_key is not None:
        if units['separate_annotation']:
            col_ids.append(unit_annotation_key)
    col_types = dict([(p, 'string') for p in col_ids])
    col_types['__pos__'] = 'continuous'
    return Table(range(1, row_id + 1), col_ids, new_values, '__col__', 'string', '__id__', 'continuous', col_types, None, None, None)


def collocations(units=None, contexts=None, progress_callback=None):
    """Collocations based on neighboring segments.

    Parameter contexts is a dict with the following keys and values:
    KEY                     VALUE                           DEFAULT
    segmentation            context segmentation            None
    annotation_key          annotation to be displayed      None
    max_distance            maximum distance of neighbors   None
    min_frequency           minimum type frequency          1
    merge_strings           treat strings as contiguous?    False

    Returns a table.
    """
    default_contexts = {'segmentation':None, 
     'annotation_key':None, 
     'max_distance':None, 
     'min_frequency':1, 
     'merge_strings':False}
    if contexts is not None:
        default_contexts.update(contexts)
    else:
        contexts = default_contexts
        neighbor_indices = set()
        global_freq = dict()
        local_freq = dict()
        new_values = dict()
        if contexts['max_distance'] is not None:
            adjacent_positions = range(1, contexts['max_distance'] + 1)
        else:
            adjacent_positions = range(1, len(contexts['segmentation']))
        context_annotation_key = contexts['annotation_key']
        context_segmentation = contexts['segmentation']
        context_min_frequency = contexts['min_frequency']
        merge_strings = contexts['merge_strings']
        if context_annotation_key is not None:
            context_list = [c.annotations.get(context_annotation_key, '__none__') for c in context_segmentation]
        else:
            context_list = [c.get_content() for c in context_segmentation]
        for context_index, context_segment in enumerate(context_segmentation):
            context_token = context_segment
            global_freq[context_list[context_index]] = global_freq.get(context_list[context_index], 0) + 1
            for unit_index in context_token.get_contained_segment_indices(units):
                unit_token_str_index = units[unit_index].get_real_str_index()
                for pos in adjacent_positions:
                    left_index = context_index - pos
                    if left_index >= 0:
                        if merge_strings or unit_token_str_index == context_segmentation[left_index].get_real_str_index():
                            neighbor_indices.add(left_index)
                        right_index = context_index + pos
                        if right_index < len(context_segmentation) and (merge_strings or unit_token_str_index == context_segmentation[right_index].get_real_str_index()):
                            neighbor_indices.add(right_index)

            if progress_callback:
                progress_callback()

        for neighbor in [context_list[i] for i in neighbor_indices]:
            local_freq[neighbor] = local_freq.get(neighbor, 0) + 1

        if context_min_frequency > 1:
            neighbor_types = [i for i in sorted(local_freq.keys()) if global_freq[i] >= context_min_frequency]
        else:
            neighbor_types = sorted(local_freq.keys())
    local_total_count = sum([local_freq[t] for t in neighbor_types])
    global_total_count = sum(global_freq.values())
    for neighbor_type in neighbor_types:
        local_prob = local_freq[neighbor_type] / local_total_count
        global_prob = global_freq[neighbor_type] / global_total_count
        new_values[(neighbor_type, '__mutual_info__')] = math.log(local_prob / global_prob, 2)
        new_values[(neighbor_type, '__local_freq__')] = local_freq[neighbor_type]
        new_values[(neighbor_type, '__local_prob__')] = local_prob
        new_values[(neighbor_type, '__global_freq__')] = global_freq[neighbor_type]
        new_values[(neighbor_type, '__global_prob__')] = global_prob

    col_ids = [
     '__mutual_info__',
     '__local_freq__',
     '__local_prob__',
     '__global_freq__',
     '__global_prob__']
    return Table(neighbor_types, col_ids, new_values, '__col__', 'string', '__unit__', 'string', dict([(c, 'continuous') for c in col_ids]), None, None, None)


def cooc_in_window(units=None, window_size=2, progress_callback=None):
    """ Measure the cooccurrence in sliding window """
    contingency = count_in_window(units, window_size, progress_callback)
    normalized = contingency.to_normalized('presence/absence')
    np_contingency = normalized.to_numpy()
    cooc = np.dot(np.transpose(np_contingency), np_contingency)
    try:
        new_header_row_id = contingency.header_row_id[:-2] + '2' + contingency.header_row_id[-2:]
        return IntPivotCrosstab.from_numpy(contingency.col_ids[:], contingency.col_ids[:], cooc, contingency.header_row_id, contingency.header_row_type, new_header_row_id, contingency.header_row_type, contingency.col_type)
    except IndexError:
        return IntPivotCrosstab(list(), list(), dict())


def cooc_in_context(units=None, contexts=None, units2=None, progress_callback=None):
    """ Measure the cooccurrence in a context type segmentation"""
    contingency = count_in_context(units, contexts, progress_callback)
    normalized = contingency.to_normalized('presence/absence')
    np_contingency = normalized.to_numpy()
    if units2 is not None:
        contingency2 = count_in_context(units2, contexts, progress_callback)
        normalized2 = contingency2.to_normalized('presence/absence')
        np_contingency2 = normalized2.to_numpy()
        row_labels = contingency.row_ids
        row_labels2 = contingency2.row_ids
        keep_from_contingency = [i for i in xrange(len(row_labels)) if row_labels[i] in row_labels2]
        keep_from_contingency2 = [i for i in xrange(len(row_labels2)) if row_labels2[i] in row_labels]
        try:
            np_contingency = np_contingency[keep_from_contingency].astype(int)
            np_contingency2 = np_contingency2[keep_from_contingency2].astype(int)
            cooc = np.dot(np.transpose(np_contingency2), np_contingency)
            if contingency.header_row_id == contingency2.header_row_id:
                new_header_row_id = contingency.header_row_id[:-2] + '2' + contingency.header_row_id[-2:]
            else:
                new_header_row_id = contingency.header_row_id
            return IntPivotCrosstab.from_numpy(contingency2.col_ids[:], contingency.col_ids[:], cooc, contingency.header_row_id, contingency.header_row_type, new_header_row_id, contingency2.header_row_type, contingency.col_type)
        except IndexError:
            return IntPivotCrosstab(list(), list(), dict())

    else:
        cooc = np.dot(np.transpose(np_contingency), np_contingency)
    try:
        new_header_row_id = contingency.header_row_id[:-2] + '2' + contingency.header_row_id[-2:]
        return IntPivotCrosstab.from_numpy(contingency.col_ids[:], contingency.col_ids[:], cooc, contingency.header_row_id, contingency.header_row_type, new_header_row_id, contingency.header_row_type, contingency.col_type)
    except IndexError:
        return IntPivotCrosstab(list(), list(), dict())