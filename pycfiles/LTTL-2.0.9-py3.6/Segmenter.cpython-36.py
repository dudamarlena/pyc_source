# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\LTTL\Segmenter.py
# Compiled at: 2017-10-13 08:45:38
# Size of source mod 2**32: 50941 bytes
"""Module Segmentation.py
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
---------------------------------------------------------------------------
Provides public functions:
- concatenate()
- tokenize()
- select()
- threshold()
- sample()
- intersect()
- import_xml()
- recode)
- bypass()
"""
from __future__ import division
from __future__ import absolute_import
from __future__ import unicode_literals
import re, random, unicodedata
from .Segmentation import Segmentation
from .Segment import Segment
from .Input import Input
from .Utils import iround
from builtins import range
from builtins import str as text
from builtins import dict
__version__ = '1.0.6'

def concatenate(segmentations, label='my_concatenation', copy_annotations=True, import_labels_as='component_label', sort=False, auto_number_as=None, merge_duplicates=False, progress_callback=None):
    """Take a list of segmentations and concatenates them into a new one

    :param segmentations: list of segmentations to concatenate

    :param label: label assigned to output segmentation

    :param copy_annotations: boolean indicating whether annotations associated
    with input segments should be copied to output

    :param import_labels_as: annotation key to which input segmentation
    labels should be associated (as annotation values) in output segments
    (default 'component_label')

    :param auto_number_as: unless set to None (default), a string indicating
    the annotation key which should be used for storing an automatically
    generated numeric index for each segment.

    :param sort: boolean indicating whether output segments should be sorted by
    address (str_index, then start position, then end position)

    :param merge_duplicates: boolean indicating whether output segments with
    the same address should be merged into a single segment.

    :param progress_callback: callback for monitoring progress ticks (1 for each
    input segment)

    :return: new segmentation containing the concatenated segments
    """
    new_segments = Segmentation()
    new_segments.label = label
    str_indices = list()
    for segmentation in segmentations:
        for k in segmentation.str_index_ptr.keys():
            if k not in str_indices:
                str_indices.append(k)

    if sort:
        str_indices = sorted(str_indices)
    for index in str_indices:
        merge_ptr = list()
        for segmentation in segmentations:
            if index in segmentation.str_index_ptr:
                merge_ptr.append((
                 segmentation,
                 segmentation.str_index_ptr[index],
                 segmentation[segmentation.str_index_ptr[index]]))

        last_seen = None
        while len(merge_ptr) > 0:
            _min = merge_ptr[0]
            _argmin = 0
            for i, ptr in enumerate(merge_ptr[1:]):
                if (
                 ptr[2].start, ptr[2].end) < (_min[2].start, _min[2].end):
                    _min = ptr
                    _argmin = i + 1

            segment = _min[2]
            segmentation = merge_ptr[_argmin][0]
            if merge_ptr[_argmin][1] + 1 >= len(merge_ptr[_argmin][0]):
                del merge_ptr[_argmin]
            else:
                merge_ptr[_argmin] = (
                 merge_ptr[_argmin][0],
                 merge_ptr[_argmin][1] + 1,
                 merge_ptr[_argmin][0][(merge_ptr[_argmin][1] + 1)])
                if merge_ptr[_argmin][2].str_index != index:
                    del merge_ptr[_argmin]
                elif import_labels_as is not None and len(import_labels_as) > 0:
                    new_segment = segment.deepcopy(annotations={import_labels_as: segmentation.label},
                      update=copy_annotations)
                else:
                    new_segment = segment.deepcopy(update=copy_annotations)
                if merge_duplicates and last_seen and last_seen.start == new_segment.start and last_seen.end == new_segment.end:
                    last_segment = new_segments[(-1)]
                    last_segment.annotations.update(new_segment.annotations)
                    new_segments[-1] = last_segment
                else:
                    new_segments.append(new_segment)
            last_seen = segment
            if progress_callback:
                progress_callback()

    if auto_number_as is not None:
        if len(auto_number_as) > 0:
            _auto_number(new_segments, auto_number_as)
    return new_segments


def tokenize--- This code section failed: ---

 L. 245         0  LOAD_GLOBAL              Segmentation
                2  LOAD_CONST               None
                4  LOAD_FAST                'label'
                6  CALL_FUNCTION_2       2  '2 positional arguments'
                8  STORE_FAST               'new_segmentation'

 L. 246        10  LOAD_GLOBAL              list
               12  CALL_FUNCTION_0       0  '0 positional arguments'
               14  STORE_FAST               'annotation_k_backref_indices'

 L. 247        16  LOAD_GLOBAL              list
               18  CALL_FUNCTION_0       0  '0 positional arguments'
               20  STORE_FAST               'annotation_v_backref_indices'

 L. 248        22  LOAD_GLOBAL              list
               24  CALL_FUNCTION_0       0  '0 positional arguments'
               26  STORE_FAST               'annotation_key_format'

 L. 249        28  LOAD_GLOBAL              list
               30  CALL_FUNCTION_0       0  '0 positional arguments'
               32  STORE_FAST               'annotation_value_format'

 L. 250        34  LOAD_GLOBAL              re
               36  LOAD_ATTR                compile
               38  LOAD_STR                 '&([0-9]+)'
               40  CALL_FUNCTION_1       1  '1 positional argument'
               42  STORE_FAST               'contains_backrefs'

 L. 253        44  SETUP_LOOP          288  'to 288'
               46  LOAD_FAST                'regexes'
               48  GET_ITER         
               50  FOR_ITER            286  'to 286'
               52  STORE_FAST               'regex'

 L. 256        54  LOAD_GLOBAL              len
               56  LOAD_FAST                'regex'
               58  CALL_FUNCTION_1       1  '1 positional argument'
               60  LOAD_CONST               3
               62  COMPARE_OP               ==
               64  POP_JUMP_IF_FALSE   240  'to 240'

 L. 259        66  LOAD_GLOBAL              list
               68  LOAD_FAST                'regex'
               70  LOAD_CONST               2
               72  BINARY_SUBSCR    
               74  CALL_FUNCTION_1       1  '1 positional argument'
               76  LOAD_CONST               0
               78  BINARY_SUBSCR    
               80  STORE_FAST               'key'

 L. 260        82  LOAD_GLOBAL              list
               84  LOAD_FAST                'regex'
               86  LOAD_CONST               2
               88  BINARY_SUBSCR    
               90  LOAD_ATTR                values
               92  CALL_FUNCTION_0       0  '0 positional arguments'
               94  CALL_FUNCTION_1       1  '1 positional argument'
               96  LOAD_CONST               0
               98  BINARY_SUBSCR    
              100  STORE_FAST               'value'

 L. 264       102  LOAD_FAST                'annotation_k_backref_indices'
              104  LOAD_ATTR                append

 L. 265       106  LOAD_LISTCOMP            '<code_object <listcomp>>'
              108  LOAD_STR                 'tokenize.<locals>.<listcomp>'
              110  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              112  LOAD_FAST                'contains_backrefs'
              114  LOAD_ATTR                findall
              116  LOAD_FAST                'key'
              118  CALL_FUNCTION_1       1  '1 positional argument'
              120  GET_ITER         
              122  CALL_FUNCTION_1       1  '1 positional argument'
              124  CALL_FUNCTION_1       1  '1 positional argument'
              126  POP_TOP          

 L. 267       128  LOAD_FAST                'annotation_v_backref_indices'
              130  LOAD_ATTR                append

 L. 268       132  LOAD_LISTCOMP            '<code_object <listcomp>>'
              134  LOAD_STR                 'tokenize.<locals>.<listcomp>'
              136  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              138  LOAD_FAST                'contains_backrefs'
              140  LOAD_ATTR                findall
              142  LOAD_FAST                'value'
              144  CALL_FUNCTION_1       1  '1 positional argument'
              146  GET_ITER         
              148  CALL_FUNCTION_1       1  '1 positional argument'
              150  CALL_FUNCTION_1       1  '1 positional argument'
              152  POP_TOP          

 L. 274       154  LOAD_GLOBAL              len
              156  LOAD_FAST                'annotation_k_backref_indices'
              158  LOAD_CONST               -1
              160  BINARY_SUBSCR    
              162  CALL_FUNCTION_1       1  '1 positional argument'
              164  POP_JUMP_IF_FALSE   186  'to 186'

 L. 275       166  LOAD_FAST                'annotation_key_format'
              168  LOAD_ATTR                append

 L. 276       170  LOAD_FAST                'contains_backrefs'
              172  LOAD_ATTR                sub
              174  LOAD_STR                 '%s'
              176  LOAD_FAST                'key'
              178  CALL_FUNCTION_2       2  '2 positional arguments'
              180  CALL_FUNCTION_1       1  '1 positional argument'
              182  POP_TOP          
              184  JUMP_FORWARD        196  'to 196'
              186  ELSE                     '196'

 L. 279       186  LOAD_FAST                'annotation_key_format'
              188  LOAD_ATTR                append
              190  LOAD_CONST               None
              192  CALL_FUNCTION_1       1  '1 positional argument'
              194  POP_TOP          
            196_0  COME_FROM           184  '184'

 L. 280       196  LOAD_GLOBAL              len
              198  LOAD_FAST                'annotation_v_backref_indices'
              200  LOAD_CONST               -1
              202  BINARY_SUBSCR    
              204  CALL_FUNCTION_1       1  '1 positional argument'
              206  POP_JUMP_IF_FALSE   228  'to 228'

 L. 281       208  LOAD_FAST                'annotation_value_format'
              210  LOAD_ATTR                append

 L. 282       212  LOAD_FAST                'contains_backrefs'
              214  LOAD_ATTR                sub
              216  LOAD_STR                 '%s'
              218  LOAD_FAST                'value'
              220  CALL_FUNCTION_2       2  '2 positional arguments'
              222  CALL_FUNCTION_1       1  '1 positional argument'
              224  POP_TOP          
              226  JUMP_FORWARD        238  'to 238'
              228  ELSE                     '238'

 L. 285       228  LOAD_FAST                'annotation_value_format'
              230  LOAD_ATTR                append
              232  LOAD_CONST               None
              234  CALL_FUNCTION_1       1  '1 positional argument'
              236  POP_TOP          
            238_0  COME_FROM           226  '226'
              238  JUMP_BACK            50  'to 50'
              240  ELSE                     '284'

 L. 290       240  LOAD_FAST                'annotation_k_backref_indices'
              242  LOAD_ATTR                append
              244  LOAD_GLOBAL              list
              246  CALL_FUNCTION_0       0  '0 positional arguments'
              248  CALL_FUNCTION_1       1  '1 positional argument'
              250  POP_TOP          

 L. 291       252  LOAD_FAST                'annotation_v_backref_indices'
              254  LOAD_ATTR                append
              256  LOAD_GLOBAL              list
              258  CALL_FUNCTION_0       0  '0 positional arguments'
              260  CALL_FUNCTION_1       1  '1 positional argument'
              262  POP_TOP          

 L. 292       264  LOAD_FAST                'annotation_key_format'
              266  LOAD_ATTR                append
              268  LOAD_CONST               None
              270  CALL_FUNCTION_1       1  '1 positional argument'
              272  POP_TOP          

 L. 293       274  LOAD_FAST                'annotation_value_format'
              276  LOAD_ATTR                append
              278  LOAD_CONST               None
              280  CALL_FUNCTION_1       1  '1 positional argument'
              282  POP_TOP          
              284  JUMP_BACK            50  'to 50'
              286  POP_BLOCK        
            288_0  COME_FROM_LOOP       44  '44'

 L. 296       288  SETUP_LOOP         1076  'to 1076'
              292  LOAD_FAST                'segmentation'
              294  GET_ITER         
              296  FOR_ITER           1074  'to 1074'
              300  STORE_FAST               'segment'

 L. 298       302  LOAD_GLOBAL              list
              304  CALL_FUNCTION_0       0  '0 positional arguments'
              306  STORE_FAST               'new_segments'

 L. 299       308  LOAD_FAST                'segment'
              310  LOAD_ATTR                str_index
              312  STORE_FAST               'str_index'

 L. 300       314  LOAD_FAST                'segment'
              316  LOAD_ATTR                start
              318  JUMP_IF_TRUE_OR_POP   324  'to 324'
              322  LOAD_CONST               0
            324_0  COME_FROM           318  '318'
              324  STORE_FAST               'start'

 L. 301       326  LOAD_FAST                'segment'
              328  LOAD_ATTR                get_content
              330  CALL_FUNCTION_0       0  '0 positional arguments'
              332  STORE_FAST               'content'

 L. 304       334  LOAD_FAST                'import_annotations'
              336  POP_JUMP_IF_FALSE   364  'to 364'
              340  LOAD_FAST                'segment'
              342  LOAD_ATTR                annotations
              344  LOAD_CONST               None
              346  COMPARE_OP               is-not
              348  POP_JUMP_IF_FALSE   364  'to 364'

 L. 305       352  LOAD_FAST                'segment'
              354  LOAD_ATTR                annotations
              356  LOAD_ATTR                copy
              358  CALL_FUNCTION_0       0  '0 positional arguments'
              360  STORE_FAST               'old_segment_annotation_copy'
              362  JUMP_FORWARD        368  'to 368'
            364_0  COME_FROM           336  '336'

 L. 307       364  LOAD_CONST               None
              366  STORE_FAST               'old_segment_annotation_copy'
            368_0  COME_FROM           362  '362'

 L. 310       368  SETUP_LOOP         1044  'to 1044'
              372  LOAD_GLOBAL              range
              374  LOAD_GLOBAL              len
              376  LOAD_FAST                'regexes'
              378  CALL_FUNCTION_1       1  '1 positional argument'
              380  CALL_FUNCTION_1       1  '1 positional argument'
              382  GET_ITER         
              384  FOR_ITER           1042  'to 1042'
              388  STORE_FAST               'regex_index'

 L. 311       390  LOAD_FAST                'regexes'
              392  LOAD_FAST                'regex_index'
              394  BINARY_SUBSCR    
              396  STORE_FAST               'regex'

 L. 314       398  LOAD_FAST                'old_segment_annotation_copy'
              400  LOAD_CONST               None
              402  COMPARE_OP               is-not
              404  POP_JUMP_IF_FALSE   418  'to 418'

 L. 315       408  LOAD_FAST                'old_segment_annotation_copy'
              410  LOAD_ATTR                copy
              412  CALL_FUNCTION_0       0  '0 positional arguments'
              414  STORE_FAST               'regex_annotations'
              416  JUMP_FORWARD        422  'to 422'
              418  ELSE                     '422'

 L. 317       418  LOAD_CONST               None
              420  STORE_FAST               'regex_annotations'
            422_0  COME_FROM           416  '416'

 L. 319       422  LOAD_FAST                'regex'
              424  LOAD_CONST               1
              426  BINARY_SUBSCR    
              428  LOAD_STR                 'tokenize'
              430  COMPARE_OP               ==
              432  POP_JUMP_IF_FALSE   740  'to 740'

 L. 322       436  SETUP_LOOP         1026  'to 1026'
              440  LOAD_GLOBAL              re
              442  LOAD_ATTR                finditer
              444  LOAD_FAST                'regex'
              446  LOAD_CONST               0
              448  BINARY_SUBSCR    
              450  LOAD_FAST                'content'
              452  CALL_FUNCTION_2       2  '2 positional arguments'
              454  GET_ITER         
              456  FOR_ITER            734  'to 734'
              460  STORE_DEREF              'match'

 L. 323       462  LOAD_CONST               None
              464  STORE_FAST               'key'

 L. 324       466  LOAD_CONST               None
              468  STORE_FAST               'value'

 L. 328       470  LOAD_GLOBAL              len
              472  LOAD_FAST                'annotation_k_backref_indices'
              474  LOAD_FAST                'regex_index'
              476  BINARY_SUBSCR    
              478  CALL_FUNCTION_1       1  '1 positional argument'
              480  POP_JUMP_IF_FALSE   520  'to 520'

 L. 333       484  LOAD_FAST                'annotation_key_format'
              486  LOAD_FAST                'regex_index'
              488  BINARY_SUBSCR    
              490  LOAD_GLOBAL              tuple

 L. 335       492  LOAD_CLOSURE             'match'
              494  BUILD_TUPLE_1         1 
              496  LOAD_LISTCOMP            '<code_object <listcomp>>'
              498  LOAD_STR                 'tokenize.<locals>.<listcomp>'
              500  MAKE_FUNCTION_8          'closure'

 L. 336       502  LOAD_FAST                'annotation_k_backref_indices'

 L. 337       504  LOAD_FAST                'regex_index'
              506  BINARY_SUBSCR    
              508  GET_ITER         
              510  CALL_FUNCTION_1       1  '1 positional argument'
              512  CALL_FUNCTION_1       1  '1 positional argument'
              514  BINARY_MODULO    
              516  STORE_FAST               'key'
              518  JUMP_FORWARD        550  'to 550'
              520  ELSE                     '550'

 L. 344       520  LOAD_GLOBAL              len
              522  LOAD_FAST                'regex'
              524  CALL_FUNCTION_1       1  '1 positional argument'
              526  LOAD_CONST               3
              528  COMPARE_OP               ==
              530  POP_JUMP_IF_FALSE   550  'to 550'

 L. 345       534  LOAD_GLOBAL              list
              536  LOAD_FAST                'regex'
              538  LOAD_CONST               2
              540  BINARY_SUBSCR    
              542  CALL_FUNCTION_1       1  '1 positional argument'
              544  LOAD_CONST               0
              546  BINARY_SUBSCR    
              548  STORE_FAST               'key'
            550_0  COME_FROM           530  '530'
            550_1  COME_FROM           518  '518'

 L. 349       550  LOAD_GLOBAL              len
              552  LOAD_FAST                'annotation_v_backref_indices'
              554  LOAD_FAST                'regex_index'
              556  BINARY_SUBSCR    
              558  CALL_FUNCTION_1       1  '1 positional argument'
              560  POP_JUMP_IF_FALSE   600  'to 600'

 L. 353       564  LOAD_FAST                'annotation_value_format'
              566  LOAD_FAST                'regex_index'
              568  BINARY_SUBSCR    
              570  LOAD_GLOBAL              tuple

 L. 355       572  LOAD_CLOSURE             'match'
              574  BUILD_TUPLE_1         1 
              576  LOAD_LISTCOMP            '<code_object <listcomp>>'
              578  LOAD_STR                 'tokenize.<locals>.<listcomp>'
              580  MAKE_FUNCTION_8          'closure'

 L. 356       582  LOAD_FAST                'annotation_v_backref_indices'

 L. 357       584  LOAD_FAST                'regex_index'
              586  BINARY_SUBSCR    
              588  GET_ITER         
              590  CALL_FUNCTION_1       1  '1 positional argument'
              592  CALL_FUNCTION_1       1  '1 positional argument'
              594  BINARY_MODULO    
              596  STORE_FAST               'value'
              598  JUMP_FORWARD        634  'to 634'
              600  ELSE                     '634'

 L. 362       600  LOAD_GLOBAL              len
              602  LOAD_FAST                'regex'
              604  CALL_FUNCTION_1       1  '1 positional argument'
              606  LOAD_CONST               3
              608  COMPARE_OP               ==
              610  POP_JUMP_IF_FALSE   634  'to 634'

 L. 363       614  LOAD_GLOBAL              list
              616  LOAD_FAST                'regex'
              618  LOAD_CONST               2
              620  BINARY_SUBSCR    
              622  LOAD_ATTR                values
              624  CALL_FUNCTION_0       0  '0 positional arguments'
              626  CALL_FUNCTION_1       1  '1 positional argument'
              628  LOAD_CONST               0
              630  BINARY_SUBSCR    
              632  STORE_FAST               'value'
            634_0  COME_FROM           610  '610'
            634_1  COME_FROM           598  '598'

 L. 367       634  LOAD_FAST                'regex_annotations'
              636  LOAD_CONST               None
              638  COMPARE_OP               is-not
              640  POP_JUMP_IF_FALSE   654  'to 654'

 L. 368       644  LOAD_FAST                'regex_annotations'
              646  LOAD_ATTR                copy
              648  CALL_FUNCTION_0       0  '0 positional arguments'
              650  STORE_FAST               'new_segment_annotations'
              652  JUMP_FORWARD        660  'to 660'
              654  ELSE                     '660'

 L. 370       654  LOAD_GLOBAL              dict
              656  CALL_FUNCTION_0       0  '0 positional arguments'
              658  STORE_FAST               'new_segment_annotations'
            660_0  COME_FROM           652  '652'

 L. 373       660  LOAD_FAST                'key'
              662  LOAD_CONST               None
              664  COMPARE_OP               is-not
              666  POP_JUMP_IF_FALSE   694  'to 694'
              670  LOAD_FAST                'value'
              672  LOAD_CONST               None
              674  COMPARE_OP               is-not
              676  POP_JUMP_IF_FALSE   694  'to 694'

 L. 374       680  LOAD_FAST                'new_segment_annotations'
              682  LOAD_ATTR                update
              684  LOAD_FAST                'key'
              686  LOAD_FAST                'value'
              688  BUILD_MAP_1           1 
              690  CALL_FUNCTION_1       1  '1 positional argument'
              692  POP_TOP          
            694_0  COME_FROM           676  '676'
            694_1  COME_FROM           666  '666'

 L. 377       694  LOAD_FAST                'new_segments'
              696  LOAD_ATTR                append

 L. 378       698  LOAD_GLOBAL              Segment

 L. 379       700  LOAD_FAST                'str_index'

 L. 380       702  LOAD_FAST                'start'
              704  LOAD_DEREF               'match'
              706  LOAD_ATTR                start
              708  CALL_FUNCTION_0       0  '0 positional arguments'
              710  BINARY_ADD       

 L. 381       712  LOAD_FAST                'start'
              714  LOAD_DEREF               'match'
              716  LOAD_ATTR                end
              718  CALL_FUNCTION_0       0  '0 positional arguments'
              720  BINARY_ADD       

 L. 382       722  LOAD_FAST                'new_segment_annotations'
              724  CALL_FUNCTION_4       4  '4 positional arguments'
              726  CALL_FUNCTION_1       1  '1 positional argument'
              728  POP_TOP          
              730  JUMP_BACK           456  'to 456'
              734  POP_BLOCK        
              736  JUMP_FORWARD       1026  'to 1026'
              740  ELSE                     '1026'

 L. 387       740  LOAD_FAST                'regex'
              742  LOAD_CONST               1
              744  BINARY_SUBSCR    
              746  LOAD_STR                 'split'
              748  COMPARE_OP               ==
              750  POP_JUMP_IF_FALSE  1002  'to 1002'

 L. 391       754  LOAD_FAST                'regex_annotations'
              756  LOAD_CONST               None
              758  COMPARE_OP               is-not
              760  POP_JUMP_IF_FALSE   774  'to 774'

 L. 392       764  LOAD_FAST                'regex_annotations'
              766  LOAD_ATTR                copy
              768  CALL_FUNCTION_0       0  '0 positional arguments'
              770  STORE_FAST               'new_segment_annotations'
              772  JUMP_FORWARD        780  'to 780'
              774  ELSE                     '780'

 L. 394       774  LOAD_GLOBAL              dict
              776  CALL_FUNCTION_0       0  '0 positional arguments'
              778  STORE_FAST               'new_segment_annotations'
            780_0  COME_FROM           772  '772'

 L. 398       780  LOAD_GLOBAL              len
              782  LOAD_FAST                'regex'
              784  CALL_FUNCTION_1       1  '1 positional argument'
              786  LOAD_CONST               3
              788  COMPARE_OP               ==
              790  POP_JUMP_IF_FALSE   844  'to 844'

 L. 399       794  LOAD_GLOBAL              list
              796  LOAD_FAST                'regex'
              798  LOAD_CONST               2
              800  BINARY_SUBSCR    
              802  CALL_FUNCTION_1       1  '1 positional argument'
              804  LOAD_CONST               0
              806  BINARY_SUBSCR    
              808  STORE_FAST               'key'

 L. 400       810  LOAD_GLOBAL              list
              812  LOAD_FAST                'regex'
              814  LOAD_CONST               2
              816  BINARY_SUBSCR    
              818  LOAD_ATTR                values
              820  CALL_FUNCTION_0       0  '0 positional arguments'
              822  CALL_FUNCTION_1       1  '1 positional argument'
              824  LOAD_CONST               0
              826  BINARY_SUBSCR    
              828  STORE_FAST               'value'

 L. 401       830  LOAD_FAST                'new_segment_annotations'
              832  LOAD_ATTR                update
              834  LOAD_FAST                'key'
              836  LOAD_FAST                'value'
              838  BUILD_MAP_1           1 
              840  CALL_FUNCTION_1       1  '1 positional argument'
              842  POP_TOP          
            844_0  COME_FROM           790  '790'

 L. 404       844  LOAD_FAST                'start'
              846  STORE_FAST               'previous_end_pos'

 L. 405       848  SETUP_LOOP          954  'to 954'
              850  LOAD_GLOBAL              re
              852  LOAD_ATTR                finditer
              854  LOAD_FAST                'regex'
              856  LOAD_CONST               0
              858  BINARY_SUBSCR    
              860  LOAD_FAST                'content'
              862  CALL_FUNCTION_2       2  '2 positional arguments'
              864  GET_ITER         
              866  FOR_ITER            952  'to 952'
              868  STORE_DEREF              'match'

 L. 409       870  LOAD_FAST                'start'
              872  LOAD_DEREF               'match'
              874  LOAD_ATTR                start
              876  CALL_FUNCTION_0       0  '0 positional arguments'
              878  BINARY_ADD       
              880  LOAD_FAST                'previous_end_pos'
              882  COMPARE_OP               ==
              884  POP_JUMP_IF_FALSE   904  'to 904'

 L. 410       888  LOAD_FAST                'start'
              890  LOAD_DEREF               'match'
              892  LOAD_ATTR                end
              894  CALL_FUNCTION_0       0  '0 positional arguments'
              896  BINARY_ADD       
              898  STORE_FAST               'previous_end_pos'

 L. 411       900  CONTINUE            866  'to 866'
              904  ELSE                     '950'

 L. 414       904  LOAD_FAST                'new_segments'
              906  LOAD_ATTR                append

 L. 415       908  LOAD_GLOBAL              Segment

 L. 416       910  LOAD_FAST                'str_index'

 L. 417       912  LOAD_FAST                'previous_end_pos'

 L. 418       914  LOAD_FAST                'start'
              916  LOAD_DEREF               'match'
              918  LOAD_ATTR                start
              920  CALL_FUNCTION_0       0  '0 positional arguments'
              922  BINARY_ADD       

 L. 419       924  LOAD_FAST                'new_segment_annotations'
              926  LOAD_ATTR                copy
              928  CALL_FUNCTION_0       0  '0 positional arguments'
              930  CALL_FUNCTION_4       4  '4 positional arguments'
              932  CALL_FUNCTION_1       1  '1 positional argument'
              934  POP_TOP          

 L. 422       936  LOAD_FAST                'start'
              938  LOAD_DEREF               'match'
              940  LOAD_ATTR                end
              942  CALL_FUNCTION_0       0  '0 positional arguments'
              944  BINARY_ADD       
              946  STORE_FAST               'previous_end_pos'
              948  JUMP_BACK           866  'to 866'
              952  POP_BLOCK        
            954_0  COME_FROM_LOOP      848  '848'

 L. 426       954  LOAD_FAST                'start'
              956  LOAD_GLOBAL              len
              958  LOAD_FAST                'content'
              960  CALL_FUNCTION_1       1  '1 positional argument'
              962  BINARY_ADD       
              964  STORE_FAST               'segment_end_pos'

 L. 427       966  LOAD_FAST                'previous_end_pos'
              968  LOAD_FAST                'segment_end_pos'
              970  COMPARE_OP               <
              972  POP_JUMP_IF_FALSE  1026  'to 1026'

 L. 428       976  LOAD_FAST                'new_segments'
              978  LOAD_ATTR                append

 L. 429       980  LOAD_GLOBAL              Segment

 L. 430       982  LOAD_FAST                'str_index'

 L. 431       984  LOAD_FAST                'previous_end_pos'

 L. 432       986  LOAD_FAST                'segment_end_pos'

 L. 433       988  LOAD_FAST                'new_segment_annotations'
              990  LOAD_ATTR                copy
              992  CALL_FUNCTION_0       0  '0 positional arguments'
              994  CALL_FUNCTION_4       4  '4 positional arguments'
              996  CALL_FUNCTION_1       1  '1 positional argument'
              998  POP_TOP          
             1000  JUMP_FORWARD       1026  'to 1026'
             1002  ELSE                     '1026'

 L. 439      1002  LOAD_GLOBAL              ValueError

 L. 440      1004  LOAD_STR                 'Unknown regex mode "'
             1006  LOAD_FAST                'regex'
             1008  LOAD_CONST               1
             1010  BINARY_SUBSCR    
             1012  BINARY_ADD       
             1014  LOAD_STR                 '", '
             1016  BINARY_ADD       

 L. 441      1018  LOAD_STR                 'should be either "tokenize" or "split"'
             1020  BINARY_ADD       
             1022  CALL_FUNCTION_1       1  '1 positional argument'
             1024  RAISE_VARARGS_1       1  'exception'
           1026_0  COME_FROM          1000  '1000'
           1026_1  COME_FROM           972  '972'
           1026_2  COME_FROM           736  '736'

 L. 444      1026  LOAD_FAST                'progress_callback'
             1028  POP_JUMP_IF_FALSE   384  'to 384'

 L. 445      1032  LOAD_FAST                'progress_callback'
             1034  CALL_FUNCTION_0       0  '0 positional arguments'
             1036  POP_TOP          
             1038  JUMP_BACK           384  'to 384'
             1042  POP_BLOCK        
           1044_0  COME_FROM_LOOP      368  '368'

 L. 448      1044  LOAD_FAST                'new_segments'
             1046  LOAD_ATTR                sort
             1048  LOAD_LAMBDA              '<code_object <lambda>>'
             1050  LOAD_STR                 'tokenize.<locals>.<lambda>'
             1052  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
             1054  LOAD_CONST               ('key',)
             1056  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
             1058  POP_TOP          

 L. 455      1060  LOAD_FAST                'new_segmentation'
             1062  LOAD_ATTR                extend
             1064  LOAD_FAST                'new_segments'
             1066  CALL_FUNCTION_1       1  '1 positional argument'
             1068  POP_TOP          
             1070  JUMP_BACK           296  'to 296'
             1074  POP_BLOCK        
           1076_0  COME_FROM_LOOP      288  '288'

 L. 458      1076  LOAD_FAST                'merge_duplicates'
             1078  POP_JUMP_IF_FALSE  1092  'to 1092'

 L. 459      1082  LOAD_GLOBAL              _merge_duplicate_segments
             1084  LOAD_FAST                'new_segmentation'
             1086  LOAD_CONST               False
             1088  CALL_FUNCTION_2       2  '2 positional arguments'
             1090  STORE_FAST               'new_segmentation'
           1092_0  COME_FROM          1078  '1078'

 L. 462      1092  LOAD_FAST                'auto_number_as'
             1094  LOAD_CONST               None
             1096  COMPARE_OP               is-not
             1098  POP_JUMP_IF_FALSE  1126  'to 1126'
             1102  LOAD_GLOBAL              len
             1104  LOAD_FAST                'auto_number_as'
             1106  CALL_FUNCTION_1       1  '1 positional argument'
             1108  LOAD_CONST               0
             1110  COMPARE_OP               >
             1112  POP_JUMP_IF_FALSE  1126  'to 1126'

 L. 463      1116  LOAD_GLOBAL              _auto_number
             1118  LOAD_FAST                'new_segmentation'
             1120  LOAD_FAST                'auto_number_as'
             1122  CALL_FUNCTION_2       2  '2 positional arguments'
             1124  POP_TOP          
           1126_0  COME_FROM          1112  '1112'
           1126_1  COME_FROM          1098  '1098'

 L. 465      1126  LOAD_FAST                'new_segmentation'
             1128  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_FORWARD' instruction at offset 736


def select(segmentation, regex, mode='include', annotation_key=None, label='selected_data', copy_annotations=True, auto_number_as=None, progress_callback=None):
    """In-/exclude segments in a segmentation based on a regex

    :param segmentation: the segmentation whose segments will be selected

    :param regex: the compiled regex that each segment will be matched against

    :param mode: either 'include' (default) or 'exclude'. The former means that
    matching segments will be kept in the output, and the other way round for
    the latter

    :param annotation_key: unless set to None (default), a string indicating
    the annotation key whose value should be matched against the regex in place
    of the segment's content.

    :param label: the label assigned to the output segmentation

    :param copy_annotations: boolean indicating whether annotations associated
    with input segments should be copied to output segments (default True)

    :param auto_number_as: unless set to None (default), a string indicating
    the annotation key which should be used for storing an automatically
    generated numeric index for each segment

    :param progress_callback: callback for monitoring progress ticks (1 for each
    input segment)

    :return: a tuple whose first element is a new segmentation containing the
    selected segments, and whose second value is a new segmentation containing
    the segments that have not been selected (the latter has the same label as
    the former, prefixed by 'NEG_')
    """
    new_segmentation = Segmentation(list(), label)
    neg_segmentation = Segmentation(list(), 'NEG_' + label)
    for segment in segmentation:
        if annotation_key:
            if annotation_key in segment.annotations:
                match = regex.search(text(segment.annotations[annotation_key]))
            else:
                match = None
        else:
            match = regex.search(segment.get_content())
        new_segment = segment.deepcopy(update=copy_annotations)
        if match and mode == 'include' or not match and mode == 'exclude':
            new_segmentation.append(new_segment)
        else:
            neg_segmentation.append(new_segment)
        if progress_callback:
            progress_callback()

    if auto_number_as is not None:
        if len(auto_number_as) > 0:
            _auto_number(new_segmentation, auto_number_as)
            _auto_number(neg_segmentation, auto_number_as)
    return (
     new_segmentation, neg_segmentation)


def threshold(segmentation, min_count=None, max_count=None, annotation_key=None, label='thresholded_data', copy_annotations=True, auto_number_as=None, progress_callback=None):
    """Include segments in a segmentation based on min/max count

    :param segmentation: the segmentation whose segments will be selected

    :param min_count: the minimum count threshold for a segment type to
    be included in the output (default None)

    :param max_count: the maximum count threshold for a segment type to
    be included in the output (default None)

    :param annotation_key: unless set to None (default), a string indicating
    the annotation key whose value will be counted in place of the segment's
    content to determine in-/exclusion

    :param label: the label assigned to the output segmentation

    :param copy_annotations: boolean indicating whether annotations associated
    with input segments should be copied to output segments (default True)

    :param auto_number_as: unless set to None (default), a string indicating
    the annotation key which should be used for storing an automatically
    generated numeric index for each segment

    :param progress_callback: callback for monitoring progress ticks (1 for each
    input segment)

    :return: a tuple whose first element is a new segmentation containing the
    selected segments, and whose second value is a new segmentation containing
    the segments that have not been selected (the latter has the same label as
    the former, prefixed by 'NEG_')
    """
    if min_count is None:
        min_count = 0
    else:
        if max_count is None:
            max_count = len(segmentation)
        else:
            if annotation_key is None:
                token_list = [u.get_content() for u in segmentation]
            else:
                token_list = [u.annotations[annotation_key] for u in segmentation if annotation_key in u.annotations]
        count = dict()
        for token in token_list:
            try:
                count[token] += 1
            except KeyError:
                count[token] = 1

        new_segmentation = Segmentation(list(), label)
        neg_segmentation = Segmentation(list(), 'NEG_' + label)
        for segment in segmentation:
            if annotation_key:
                try:
                    token = segment.annotations[annotation_key]
                except KeyError:
                    token = '__none__'

            else:
                token = segment.get_content()
            new_segment = segment.deepcopy(update=copy_annotations)
            if min_count <= count[token] <= max_count:
                new_segmentation.append(new_segment)
            else:
                neg_segmentation.append(new_segment)
            if progress_callback:
                progress_callback()

        if auto_number_as is not None:
            if len(auto_number_as) > 0:
                _auto_number(new_segmentation, auto_number_as)
                _auto_number(neg_segmentation, auto_number_as)
    return (
     new_segmentation, neg_segmentation)


def sample(segmentation, sample_size, mode='random', label='sampled_data', copy_annotations=True, auto_number_as=None, progress_callback=None):
    """Draw a sample from a segmentation

    :param segmentation: the segmentation whose segments will be sampled

    :param sample_size: the number of segments to sample

    :param mode: either 'random' (default) or 'systematic'; the former means
    that segments can be taken from any position in the input segmentation,
    while the latter means that segments are sampled at fixed intervals (every
    n-th input segment, starting from the first).

    :param label: the label assigned to the output segmentation

    :param copy_annotations: boolean indicating whether annotations associated
    with input segments should be copied to output segments (default True)

    :param auto_number_as: unless set to None (default), a string indicating
    the annotation key which should be used for storing an automatically
    generated numeric index for each segment

    :param progress_callback: callback for monitoring progress ticks (1 for each
    input segment)

    :return: a tuple whose first element is a new segmentation containing the
    sampled segments, and whose second value is a new segmentation containing
    the segments that have not been sampled (the latter has the same label as
    the former, prefixed by 'NEG_')
    """
    new_segmentation = Segmentation(None, label)
    neg_segmentation = Segmentation(None, 'NEG_' + label)
    if mode == 'random':
        sampled_indices = sorted(random.sample(range(len(segmentation)), sample_size))
    else:
        if mode == 'systematic':
            step = 1 / (sample_size / len(segmentation))
            step = iround(step)
            sampled_indices = list(range(len(segmentation)))[::step]
        else:
            raise ValueError('Unknown sampling mode "' + mode + '", ' + 'should be either "random" or "systematic"')
    for index, segment in enumerate(segmentation):
        new_segment = segment.deepcopy(update=copy_annotations)
        if index in sampled_indices:
            new_segmentation.append(new_segment)
        else:
            neg_segmentation.append(new_segment)
        if progress_callback:
            progress_callback()

    if auto_number_as is not None:
        if len(auto_number_as) > 0:
            _auto_number(new_segmentation, auto_number_as)
            _auto_number(neg_segmentation, auto_number_as)
    return (
     new_segmentation, neg_segmentation)


def intersect(source, filtering, source_annotation_key=None, filtering_annotation_key=None, mode='include', label='selected_data', copy_annotations=True, auto_number_as=None, progress_callback=None):
    """In-/exclude segments in a segmentation ("source") based on whether these
    types occur in another segmentation ("filtering").

    :param source: the source segmentation, whose segments will be included in
    or excluded from the output

    :param filtering: the filtering segmentation, whose segments will be used
    to determine in-/exclusion of source segments

    :param source_annotation_key: unless set to None (default), a string
    indicating the annotation key whose value will be used in place of source
    segment content to determine in-/exclusion

    :param filtering_annotation_key: unless set to None (default), a string
    indicating the annotation key whose value will be used in place of
    filtering segment content to determine in-/exclusion

    :param mode: either 'include' (default) or 'exclude'. The former means that
    source segments present in filtering segmentation will be kept in the
    output, and the latter means that they will be excluded from the output.

    :param label: the label assigned to the output segmentation

    :param copy_annotations: boolean indicating whether annotations associated
    with input segments should be copied to output segments (default True)

    :param auto_number_as: unless set to None (default), a string indicating
    the annotation key which should be used for storing an automatically
    generated numeric index for each segment

    :param progress_callback: callback for monitoring progress ticks (1 for
    each source segment)

    :return: a tuple whose first element is a new segmentation containing the
    selected segments, and whose second value is a new segmentation containing
    the segments that have not been selected (the latter has the same label as
    the former, prefixed by 'NEG_')
    """
    if filtering_annotation_key is not None:
        filtering_list = [s.annotations[filtering_annotation_key] for s in filtering if filtering_annotation_key in s.annotations]
    else:
        filtering_list = [s.get_content() for s in filtering]
    filtering_set = set(filtering_list)
    new_segmentation = Segmentation(list(), label)
    neg_segmentation = Segmentation(list(), 'NEG_' + label)
    for segment in source:
        new_segment = segment.deepcopy(update=copy_annotations)
        if source_annotation_key:
            if source_annotation_key in segment.annotations:
                match = text(segment.annotations[source_annotation_key]) in filtering_set
            else:
                match = 0
        else:
            match = segment.get_content() in filtering_set
        if match and mode == 'include' or not match and mode == 'exclude':
            new_segmentation.append(new_segment)
        else:
            neg_segmentation.append(new_segment)
        if progress_callback:
            progress_callback()

    if auto_number_as is not None:
        if len(auto_number_as) > 0:
            _auto_number(new_segmentation, auto_number_as)
            _auto_number(neg_segmentation, auto_number_as)
    return (
     new_segmentation, neg_segmentation)


def import_xml(segmentation, element, conditions=None, import_element_as=None, label='xml_data', import_annotations=True, merge_duplicates=False, auto_number_as=None, remove_markup=False, preserve_leaves=False, progress_callback=None):
    """Create a segmentation based on the xml content of an existing one.

    Each occurrence of a specified xml tag is converted into a segment, and
    its attribute-value pairs are converted into annotation key-value pairs.

    Empty elements are discarded since they cannot be represented by LTTL's
    data model.

    XML processing is rather crude for the time being: no attempt to
    resolve entities, detect errors and recover from them, and so on.

    :param segmentation: the segmentation whose segment's content will be
    parsed

    :param element: the specific xml tag used for creating segments

    :param conditions: a dict where each key is the name of an attribute
    and each value is a compiled regex that must be satisfied by the
    attribute value for an occurrence of the element to be selected,
    e.g. {'class': re.compile(r'^navigation$')} (default None)

    :param import_element_as: unless set to None (default), a string indicating
    the annotation key which should be used for storing the name of the
    xml element

    :param label: the label assigned to the output segmentation

    :param import_annotations: boolean indicating whether annotations
    associated with input segments should be copied to output segments
    extracted from them (default True)

    :param merge_duplicates: boolean indicating whether output segments with
    the same address should be merged into a single segment (default False)

    :param auto_number_as: unless set to None (default), a string indicating
    the annotation key which should be used for storing an automatically
    generated numeric index for each segment

    :param remove_markup: a boolean indicating whether markup occurring within
    the xml elements being retrieved should be discarded or kept (default
    True). If discarded, more segments will usually be generated, since LTTL's
    data model has no means of representing discontinuous units with a single
    segment.

    :param preserve_leaves: a boolean determining the processing of the very
    particular case where (a) extracted elements are exactly embedded in one
    another, (b) they have different values for the same attribute, (c) the
    remove_markup parameter is selected and (d) the merge_duplicates option
    as well. In such a case, the method will seek to fuse the considered
    elements into one, and it will only be able to keep one of the conflicting
    annotation values; if preserve_leaves is False (default), the value
    associated to the element closest to the root in the XML tree will be kept,
    otherwise the value of the element closest to the "surface" will be kept.

    :param progress_callback: callback for monitoring progress ticks (1 for
    each input segment)

    :return: new segmentation containing the extracted segments
    """
    if conditions is None:
        conditions = dict()
    else:
        tag_regex = re.compile('</?[^>]+?/?>')
        stack = list()
        attr_stack = list()
        new_segmentation = Segmentation(list(), label)
        element = element.replace('<', '').replace('>', '')

        def filter_segment(str_index, start, end, annotations):
            start = start or 0
            if end is None:
                end = len(Segmentation.get_data(str_index))
            if start == end:
                return False
            else:
                for attr, value_regex in conditions.items():
                    if attr not in annotations or not value_regex.search(annotations[attr]):
                        return False

                return True

        temp_segments = list()
        for old_segment in segmentation:
            old_content = old_segment.get_content()
            if import_annotations:
                old_anno_copy = old_segment.annotations.copy()
            else:
                old_anno_copy = dict()
            if import_element_as is not None:
                if len(import_element_as) > 0:
                    old_anno_copy.update({import_element_as: element})
                old_str_index = old_segment.str_index
                old_start = old_segment.start or 0
                for match in re.finditer(tag_regex, old_content):
                    tag_start = old_start + match.start()
                    tag_end = old_start + match.end()
                    tag = Segmentation.get_data(old_str_index)[tag_start:tag_end]
                    tag_desc = _parse_xml_tag(tag)
                    if remove_markup:
                        for index in range(len(stack)):
                            if stack[index][(-1)][0] == old_str_index:
                                stack[index][(-1)][2] = tag_start
                            else:
                                anno = old_anno_copy.copy()
                                anno.update(attr_stack[index])
                                stack[index].append([old_str_index, 0, tag_start, anno])

                        if tag_desc['element'] == element:
                            if not tag_desc['is_empty']:
                                if tag_desc['is_opening']:
                                    stack.append(list())
                                    attr_stack.append(tag_desc['attributes'])
                                else:
                                    if stack:
                                        temp_segments.extend([Segments[0]s[1]s[2]s[3] for s in stack.pop() if filter_segments[0]s[1]s[2]s[3]])
                                        attr_stack.pop()
                                    else:
                                        raise ValueError('xml parsing error')
                        for index in range(len(stack)):
                            anno = old_anno_copy.copy()
                            anno.update(attr_stack[index])
                            stack[index].append([old_str_index, tag_end, None, anno])

                    else:
                        for index in range(len(stack)):
                            if stack[index][(-1)][0] != old_str_index:
                                anno = old_anno_copy.copy()
                                anno.update(attr_stack[index])
                                stack[index].append([
                                 old_str_index, 0, None, anno])

                        if tag_desc['element'] == element and not tag_desc['is_empty']:
                            if tag_desc['is_opening']:
                                anno = old_anno_copy.copy()
                                anno.update(tag_desc['attributes'])
                                stack.append([
                                 [
                                  old_str_index, tag_end, None, anno]])
                                attr_stack.append(tag_desc['attributes'])
                            else:
                                if stack:
                                    stack[(-1)][(-1)][2] = tag_start
                                    temp_segments.extend([Segments[0]s[1]s[2]s[3] for s in stack.pop() if filter_segments[0]s[1]s[2]s[3]])
                                    attr_stack.pop()
                                else:
                                    raise ValueError('xml parsing error (orphan closing tag)')

                if progress_callback:
                    progress_callback()

        temp_segments = sorted(temp_segments,
          key=(lambda seg: (seg.str_index, seg.start, seg.end)))
        new_segmentation.extend(temp_segments)
        if stack:
            raise ValueError('xml parsing error (missing closing tag)')
        if merge_duplicates:
            new_segmentation = _merge_duplicate_segments(new_segmentation, preserve_leaves)
        if auto_number_as is not None:
            if len(auto_number_as) > 0:
                _auto_number(new_segmentation, auto_number_as)
    return new_segmentation


def recode(segmentation, substitutions=None, case=None, remove_accents=False, label='my_recoded_data', copy_annotations=True, progress_callback=None):
    """Recode the string(s) associated with a segmentation.

    Standard preprocessing options (change case and remove accents) are
    available, as well as regex-based substitutions. Note that if both types of
    recoding are requested, preprocessing is applied prior to substitutions.

    :param segmentation: the segmentation whose segments' content will be
    recoded

    :param substitutions: a list of tuple, where each tuple has a compiled
    regex as first element, and a replacement string as second element (see
    below); substitutions are successively applied to each segment of the input
    segmentation.

    :param case: unless set to None (default), a unicode string indicating how
    case should be modified (either 'lower' or 'upper')

    :param remove_accents: boolean indicating whether accents should be removed
    (default True)

    :param label: the label assigned to the output segmentation

    :param copy_annotations: boolean indicating whether annotations associated
    with input segments should be copied to output segments (default True)

    :param progress_callback: callback for monitoring progress ticks (1 for
    each input segment)

    :return: tuple whose first element is a new segmentation containing the
    recoded segments (this will be an Input object if it contains only one
    segment, and a Segmentation object if it contains more than one segments or
    if no string was modified by the specified recoding operations); the second
    element is the total number of replacements performed.

    Replacement strings may contain backreferences in the form of an ampersand
    (&) immediately followed by a digit referring to the group to be captured
    (the form &+digit, which is not standard in Python, is used here for
    consistency with LTTL.Segmenter.tokenize()).

    A ValueError exception is raised if input segmentation is overlapping.
    """
    if not segmentation.is_non_overlapping():
        raise ValueError('Cannot apply recoder to overlapping segmentation.')
    new_objects = list()
    backref = re.compile('&(?=[0-9]+)')
    last_recoded = False
    old_str_index = -1
    new_str_index = -1
    total_num_subs = 0
    for segment in segmentation:
        original_text = segment.get_content()
        recoded_text = original_text
        if case == 'lower':
            recoded_text = recoded_text.lower()
        else:
            if case == 'upper':
                recoded_text = recoded_text.upper()
        if remove_accents:
            recoded_text = ''.join(c for c in unicodedata.normalize('NFD', recoded_text) if unicodedata.category(c) != 'Mn')
        if substitutions is not None:
            for substitution in substitutions:
                repl_string = backref.sub('\\\\', substitution[1])
                recoded_text, num_subs = substitution[0].subn(repl_string, recoded_text)
                total_num_subs += num_subs

        if recoded_text != original_text:
            new_input = Input()
            new_input.update(recoded_text, label)
            modified_segment = new_input[0]
            if copy_annotations:
                modified_segment.annotations.update(segment.annotations.copy())
                new_input[0] = modified_segment
            last_recoded = True
            new_objects.append(new_input)
        else:
            if last_recoded:
                if segment.str_index == old_str_index:
                    Segmentation.set_data(-1, old_str_index)
                    new_str_index = len(Segmentation.data) - 1
            else:
                if segment.str_index != old_str_index:
                    old_str_index = segment.str_index
                    new_str_index = segment.str_index
                new_segment = Segment(str_index=new_str_index,
                  start=(segment.start),
                  end=(segment.end))
                if copy_annotations:
                    new_segment.annotations.update(segment.annotations)
            last_recoded = False
            new_objects.append(new_segment)
        if progress_callback:
            progress_callback()

    if len(new_objects) == 1:
        if isinstance(new_objects[0], Input):
            return (
             new_objects[0], total_num_subs)
    new_segmentation = Segmentation(None, label)
    for new_object in new_objects:
        if isinstance(new_object, Input):
            new_segmentation.append(new_object[0])
        else:
            new_segmentation.append(new_object)

    return (
     new_segmentation, total_num_subs)


def bypass(segmentation, label='bypassed_data'):
    """Return a verbatim copy of a segmentation

    :param segmentation: the segmentation whose segments' content will be
    deep copied

    :param label: the label assigned to the output segmentation

    :return: deep copied segmentation.
    """
    return Segmentation([s.deepcopy() for s in segmentation], label)


def _merge_duplicate_segments(segmentation, take_first=False):
    """Delete duplicate segments in a segmentation and merge their annotations

    Using the fact that segments are always ordered by (start,end) and
    str_index are contiguous, it only needs to look for consecutively identical
    segments.

    :param segmentation: the list of input segments can be a Segmentation or
    a list

    :param take_first: if set to True the annotations of the first segment, in
    case of conflit when merging, are not overwritten

    :return: output segmentation with merged segments
    """
    new_segments = Segmentation(label=(segmentation.label))
    last_seen = None
    for segment in segmentation:
        if last_seen:
            if last_seen.str_index == segment.str_index:
                if last_seen.start == segment.start:
                    if last_seen.end == segment.end:
                        last_segment = new_segments[(-1)]
                        if take_first:
                            segment.annotations.update(last_segment.annotations)
                            new_segments[-1] = segment
                        else:
                            last_segment.annotations.update(segment.annotations)
                        new_segments[-1] = last_segment
        else:
            new_segments.append(segment)
        last_seen = segment

    return new_segments


def _auto_number(segmentation, annotation_key):
    """Add annotation with integers from 1 to N to segments in a list (in place)

    :param segment_list: the list of segments to auto-number

    :param annotation_key: the annotation key with which generated numbers will
    be associated
    """
    counter = 1
    for index, segment in enumerate(segmentation):
        segment.annotations[annotation_key] = counter
        segmentation[index] = segment
        counter += 1


def _parse_xml_tag(tag):
    """Parse an xml tag and return a dict describing it.

    :return: a dict with following keys:
    - is_element:   False for processing instructions, comments, etc.
    - is_opening:   True if tag is element opening tag, False otherwise
    - is_empty:     True if tag is empty element, False otherwise
    - element:      element name (None if not is_element)
    - attributes:   a dict with a key-value pair for each xml attribute
    If parsing fails somehow, return value is None.
    """
    element_regex = re.compile('((:|[^\\W\\d])([\\w.:-])*)', re.U)
    attribute_regex = re.compile('((:|[^\\W\\d])([\\w.:-])*)\\s*=\\s*([\'"])(.+?)(?<!\\\\)\\4', re.U)
    tag_description = {'is_element':False, 
     'is_opening':False, 
     'is_empty':False, 
     'element':None, 
     'attributes':dict()}
    if tag[1] == '!' or tag[1] == '?':
        return tag_description
    elem = re.search(element_regex, tag)
    if elem:
        tag_description['is_element'] = True
        tag_description['element'] = elem.group(1)
        for attr in re.finditer(attribute_regex, tag):
            tag_description['attributes'][attr.group(1)] = attr.group(5)

        if tag[1] != '/':
            tag_description['is_opening'] = True
        if tag[(-2)] == '/':
            tag_description['is_empty'] = True
        return tag_description