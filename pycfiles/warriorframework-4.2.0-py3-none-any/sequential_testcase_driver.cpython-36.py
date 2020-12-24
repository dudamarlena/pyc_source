# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /data/users/snayak/WARRIOR-4.2.0/warriorframework_py3/warrior/WarriorCore/sequential_testcase_driver.py
# Compiled at: 2020-02-05 00:22:48
# Size of source mod 2**32: 22552 bytes
"""
Copyright 2017, Fujitsu Network Communications, Inc.
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import os, time, traceback
from . import testcase_driver
from . import onerror_driver
from warrior.Framework import Utils
from warrior.Framework.Utils.testcase_Utils import pNote
from warrior.Framework.Utils.print_Utils import print_info, print_error, print_debug, print_warning
from warrior.WarriorCore import testsuite_utils, common_execution_utils
from . import exec_type_driver

def update_suite_attribs(junit_resultfile, errors, skipped, tests, failures, time='0'):
    """Update suite attributes """
    testsuite_utils.pSuite_update_suite_attributes(junit_resultfile, str(errors), str(skipped), str(tests), str(failures), time)


def execute_sequential_testcases--- This code section failed: ---

 L.  64         0  LOAD_CONST               False
                2  STORE_FAST               'goto_tc'

 L.  66         4  LOAD_FAST                'suite_repository'
                6  LOAD_STR                 'junit_resultfile'
                8  BINARY_SUBSCR    
               10  STORE_FAST               'junit_resultfile'

 L.  67        12  LOAD_FAST                'suite_repository'
               14  LOAD_STR                 'suite_name'
               16  BINARY_SUBSCR    
               18  STORE_FAST               'suite_name'

 L.  68        20  LOAD_FAST                'suite_repository'
               22  LOAD_STR                 'testsuite_filepath'
               24  BINARY_SUBSCR    
               26  STORE_FAST               'testsuite_filepath'

 L.  69        28  LOAD_FAST                'suite_repository'
               30  LOAD_STR                 'def_on_error_action'
               32  BINARY_SUBSCR    
               34  STORE_FAST               'suite_error_action'

 L.  70        36  LOAD_FAST                'suite_repository'
               38  LOAD_STR                 'def_on_error_value'
               40  BINARY_SUBSCR    
               42  STORE_FAST               'suite_error_value'

 L.  71        44  LOAD_GLOBAL              os
               46  LOAD_ATTR                path
               48  LOAD_ATTR                dirname
               50  LOAD_FAST                'testsuite_filepath'
               52  CALL_FUNCTION_1       1  '1 positional argument'
               54  STORE_FAST               'testsuite_dir'

 L.  72        56  LOAD_CONST               None
               58  LOAD_FAST                'data_repository'
               60  LOAD_STR                 'wt_tc_timestamp'
               62  STORE_SUBSCR     

 L.  74        64  LOAD_CONST               0
               66  STORE_FAST               'errors'

 L.  75        68  LOAD_CONST               0
               70  STORE_FAST               'skipped'

 L.  76        72  LOAD_CONST               0
               74  STORE_FAST               'failures'

 L.  77        76  LOAD_CONST               0
               78  STORE_FAST               'tests'

 L.  78        80  LOAD_CONST               0
               82  STORE_FAST               'tc_duration'

 L.  79        84  BUILD_LIST_0          0 
               86  STORE_FAST               'tc_status_list'

 L.  80        88  BUILD_LIST_0          0 
               90  STORE_FAST               'tc_impact_list'

 L.  81        92  LOAD_STR                 'Impact'
               94  LOAD_STR                 'No Impact'
               96  LOAD_CONST               ('IMPACT', 'NOIMPACT')
               98  BUILD_CONST_KEY_MAP_2     2 
              100  STORE_FAST               'impact_dict'

 L.  82       102  BUILD_LIST_0          0 
              104  STORE_FAST               'tc_duration_list'

 L.  83       106  BUILD_LIST_0          0 
              108  STORE_FAST               'tc_junit_list'

 L.  85       110  SETUP_LOOP         2532  'to 2532'
              114  LOAD_FAST                'tests'
              116  LOAD_GLOBAL              len
              118  LOAD_FAST                'testcase_list'
              120  CALL_FUNCTION_1       1  '1 positional argument'
              122  COMPARE_OP               <
              124  POP_JUMP_IF_FALSE  2530  'to 2530'

 L.  86       128  LOAD_FAST                'testcase_list'
              130  LOAD_FAST                'tests'
              132  BINARY_SUBSCR    
              134  STORE_FAST               'testcase'

 L.  87       136  LOAD_FAST                'tests'
              138  LOAD_CONST               1
              140  INPLACE_ADD      
              142  STORE_FAST               'tests'

 L.  89       144  LOAD_GLOBAL              testsuite_utils
              146  LOAD_ATTR                get_path_from_xmlfile
              148  LOAD_FAST                'testcase'
              150  CALL_FUNCTION_1       1  '1 positional argument'
              152  STORE_FAST               'tc_rel_path'

 L.  90       154  LOAD_FAST                'tc_rel_path'
              156  LOAD_CONST               None
              158  COMPARE_OP               is-not
              160  POP_JUMP_IF_FALSE   178  'to 178'

 L.  91       162  LOAD_GLOBAL              Utils
              164  LOAD_ATTR                file_Utils
              166  LOAD_ATTR                getAbsPath
              168  LOAD_FAST                'tc_rel_path'
              170  LOAD_FAST                'testsuite_dir'
              172  CALL_FUNCTION_2       2  '2 positional arguments'
              174  STORE_FAST               'tc_path'
              176  JUMP_FORWARD        186  'to 186'
              178  ELSE                     '186'

 L.  94       178  LOAD_GLOBAL              str
              180  LOAD_FAST                'tc_rel_path'
              182  CALL_FUNCTION_1       1  '1 positional argument'
              184  STORE_FAST               'tc_path'
            186_0  COME_FROM           176  '176'

 L.  95       186  LOAD_GLOBAL              print_info
              188  LOAD_STR                 '\n'
              190  CALL_FUNCTION_1       1  '1 positional argument'
              192  POP_TOP          

 L.  96       194  LOAD_GLOBAL              print_debug
              196  LOAD_STR                 '<<<< Starting execution of Test case: {0}>>>>'
              198  LOAD_ATTR                format

 L.  97       200  LOAD_FAST                'tc_path'
              202  CALL_FUNCTION_1       1  '1 positional argument'
              204  CALL_FUNCTION_1       1  '1 positional argument'
              206  POP_TOP          

 L.  98       208  LOAD_GLOBAL              exec_type_driver
              210  LOAD_ATTR                main
              212  LOAD_FAST                'testcase'
              214  CALL_FUNCTION_1       1  '1 positional argument'
              216  UNPACK_SEQUENCE_2     2 
              218  STORE_FAST               'action'
              220  STORE_FAST               'tc_status'

 L.  99       222  LOAD_GLOBAL              testsuite_utils
              224  LOAD_ATTR                get_runtype_from_xmlfile
              226  LOAD_FAST                'testcase'
              228  CALL_FUNCTION_1       1  '1 positional argument'
              230  STORE_FAST               'tc_runtype'

 L. 100       232  LOAD_GLOBAL              Utils
              234  LOAD_ATTR                testcase_Utils
              236  LOAD_ATTR                get_impact_from_xmlfile
              238  LOAD_FAST                'testcase'
              240  CALL_FUNCTION_1       1  '1 positional argument'
              242  STORE_FAST               'tc_impact'

 L. 101       244  LOAD_GLOBAL              Utils
              246  LOAD_ATTR                testcase_Utils
              248  LOAD_ATTR                get_context_from_xmlfile
              250  LOAD_FAST                'testcase'
              252  CALL_FUNCTION_1       1  '1 positional argument'
              254  STORE_FAST               'tc_context'

 L. 102       256  LOAD_GLOBAL              testsuite_utils
              258  LOAD_ATTR                get_data_file_at_suite_step

 L. 103       260  LOAD_FAST                'testcase'
              262  LOAD_FAST                'suite_repository'
              264  CALL_FUNCTION_2       2  '2 positional arguments'
              266  STORE_FAST               'suite_step_data_file'

 L. 104       268  LOAD_GLOBAL              Utils
              270  LOAD_ATTR                xml_Utils
              272  LOAD_ATTR                get_attributevalue_from_directchildnode

 L. 105       274  LOAD_FAST                'testcase'
              276  LOAD_STR                 'onError'
              278  LOAD_STR                 'action'
              280  CALL_FUNCTION_3       3  '3 positional arguments'
              282  STORE_FAST               'tc_onError_action'

 L. 106       284  LOAD_FAST                'tc_onError_action'
              286  POP_JUMP_IF_FALSE   294  'to 294'
              290  LOAD_FAST                'tc_onError_action'
              292  JUMP_FORWARD        296  'to 296'
              294  ELSE                     '296'
              294  LOAD_FAST                'suite_error_action'
            296_0  COME_FROM           292  '292'
              296  STORE_FAST               'tc_onError_action'

 L. 107       298  LOAD_FAST                'suite_step_data_file'
              300  LOAD_CONST               None
              302  COMPARE_OP               is-not
              304  POP_JUMP_IF_FALSE   330  'to 330'

 L. 108       308  LOAD_GLOBAL              Utils
              310  LOAD_ATTR                file_Utils
              312  LOAD_ATTR                getAbsPath
              314  LOAD_FAST                'suite_step_data_file'

 L. 109       316  LOAD_FAST                'testsuite_dir'
              318  CALL_FUNCTION_2       2  '2 positional arguments'
              320  STORE_FAST               'data_file'

 L. 110       322  LOAD_FAST                'data_file'
              324  LOAD_FAST                'data_repository'
              326  LOAD_FAST                'tc_path'
              328  STORE_SUBSCR     
            330_0  COME_FROM           304  '304'

 L. 111       330  LOAD_FAST                'tc_impact'
              332  LOAD_FAST                'data_repository'
              334  LOAD_STR                 'wt_tc_impact'
              336  STORE_SUBSCR     

 L. 112       338  LOAD_FAST                'testcase'
              340  LOAD_ATTR                find
              342  LOAD_STR                 'runmode'
              344  CALL_FUNCTION_1       1  '1 positional argument'
              346  LOAD_CONST               None
              348  COMPARE_OP               is-not
              350  POP_JUMP_IF_FALSE   432  'to 432'

 L. 113       354  LOAD_FAST                'testcase'
              356  LOAD_ATTR                find
              358  LOAD_STR                 'runmode'
              360  CALL_FUNCTION_1       1  '1 positional argument'
              362  LOAD_ATTR                get
              364  LOAD_STR                 'attempt'
              366  CALL_FUNCTION_1       1  '1 positional argument'
              368  LOAD_CONST               None
              370  COMPARE_OP               is-not
              372  POP_JUMP_IF_FALSE   432  'to 432'

 L. 115       376  LOAD_FAST                'testcase'
              378  LOAD_ATTR                find
              380  LOAD_STR                 'runmode'
              382  CALL_FUNCTION_1       1  '1 positional argument'
              384  LOAD_ATTR                get
              386  LOAD_STR                 'attempt'
              388  CALL_FUNCTION_1       1  '1 positional argument'
              390  LOAD_CONST               1
              392  COMPARE_OP               ==
              394  POP_JUMP_IF_FALSE   406  'to 406'

 L. 116       398  LOAD_GLOBAL              print_info
              400  LOAD_STR                 '\n----------------- Start of Testcase Runmode Execution -----------------\n'
              402  CALL_FUNCTION_1       1  '1 positional argument'
              404  POP_TOP          
            406_0  COME_FROM           394  '394'

 L. 118       406  LOAD_GLOBAL              print_info
              408  LOAD_STR                 'TESTCASE ATTEMPT: {0}'
              410  LOAD_ATTR                format
              412  LOAD_FAST                'testcase'
              414  LOAD_ATTR                find
              416  LOAD_STR                 'runmode'
              418  CALL_FUNCTION_1       1  '1 positional argument'
              420  LOAD_ATTR                get

 L. 119       422  LOAD_STR                 'attempt'
              424  CALL_FUNCTION_1       1  '1 positional argument'
              426  CALL_FUNCTION_1       1  '1 positional argument'
              428  CALL_FUNCTION_1       1  '1 positional argument'
              430  POP_TOP          
            432_0  COME_FROM           372  '372'
            432_1  COME_FROM           350  '350'

 L. 120       432  LOAD_FAST                'testcase'
              434  LOAD_ATTR                find
              436  LOAD_STR                 'retry'
              438  CALL_FUNCTION_1       1  '1 positional argument'
              440  LOAD_CONST               None
              442  COMPARE_OP               is-not
              444  POP_JUMP_IF_FALSE   496  'to 496'

 L. 121       448  LOAD_FAST                'testcase'
              450  LOAD_ATTR                find
              452  LOAD_STR                 'retry'
              454  CALL_FUNCTION_1       1  '1 positional argument'
              456  LOAD_ATTR                get
              458  LOAD_STR                 'attempt'
              460  CALL_FUNCTION_1       1  '1 positional argument'
              462  LOAD_CONST               None
              464  COMPARE_OP               is-not
              466  POP_JUMP_IF_FALSE   496  'to 496'

 L. 122       470  LOAD_GLOBAL              print_info
              472  LOAD_STR                 'TESTCASE ATTEMPT: {0}'
              474  LOAD_ATTR                format
              476  LOAD_FAST                'testcase'
              478  LOAD_ATTR                find
              480  LOAD_STR                 'retry'
              482  CALL_FUNCTION_1       1  '1 positional argument'
              484  LOAD_ATTR                get

 L. 123       486  LOAD_STR                 'attempt'
              488  CALL_FUNCTION_1       1  '1 positional argument'
              490  CALL_FUNCTION_1       1  '1 positional argument'
              492  CALL_FUNCTION_1       1  '1 positional argument'
              494  POP_TOP          
            496_0  COME_FROM           466  '466'
            496_1  COME_FROM           444  '444'

 L. 125       496  LOAD_GLOBAL              Utils
              498  LOAD_ATTR                file_Utils
              500  LOAD_ATTR                fileExists
              502  LOAD_FAST                'tc_path'
              504  CALL_FUNCTION_1       1  '1 positional argument'
              506  POP_JUMP_IF_TRUE    520  'to 520'
              510  LOAD_FAST                'action'
              512  LOAD_CONST               False
              514  COMPARE_OP               is
            516_0  COME_FROM           506  '506'
              516  POP_JUMP_IF_FALSE  1236  'to 1236'

 L. 126       520  LOAD_GLOBAL              Utils
              522  LOAD_ATTR                file_Utils
              524  LOAD_ATTR                getFileName
              526  LOAD_FAST                'tc_path'
              528  CALL_FUNCTION_1       1  '1 positional argument'
              530  STORE_FAST               'tc_name'

 L. 127       532  LOAD_GLOBAL              testsuite_utils
              534  LOAD_ATTR                pSuite_testcase
              536  LOAD_FAST                'junit_resultfile'
              538  LOAD_FAST                'suite_name'

 L. 128       540  LOAD_FAST                'tc_name'
              542  LOAD_STR                 '0'
              544  LOAD_CONST               ('time',)
              546  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              548  POP_TOP          

 L. 130       550  LOAD_FAST                'goto_tc'
              552  UNARY_NOT        
              554  POP_JUMP_IF_FALSE   680  'to 680'
              558  LOAD_FAST                'action'
              560  LOAD_CONST               True
              562  COMPARE_OP               is
              564  POP_JUMP_IF_FALSE   680  'to 680'

 L. 131       568  SETUP_EXCEPT        616  'to 616'

 L. 132       570  LOAD_GLOBAL              testcase_driver
              572  LOAD_ATTR                main
              574  LOAD_FAST                'tc_path'

 L. 133       576  LOAD_FAST                'data_repository'

 L. 134       578  LOAD_FAST                'tc_context'

 L. 135       580  LOAD_FAST                'tc_runtype'

 L. 136       582  LOAD_FAST                'auto_defects'

 L. 137       584  LOAD_FAST                'suite_name'

 L. 138       586  LOAD_FAST                'tc_onError_action'

 L. 139       588  LOAD_FAST                'iter_ts_sys'
              590  LOAD_CONST               ('runtype', 'auto_defects', 'suite', 'tc_onError_action', 'iter_ts_sys')
              592  CALL_FUNCTION_KW_8     8  '8 total positional and keyword args'
              594  STORE_FAST               'tc_result'

 L. 141       596  LOAD_FAST                'tc_result'
              598  LOAD_CONST               0
              600  BINARY_SUBSCR    
              602  STORE_FAST               'tc_status'

 L. 142       604  LOAD_FAST                'tc_result'
              606  LOAD_CONST               1
              608  BINARY_SUBSCR    
              610  STORE_FAST               'tc_duration'
              612  POP_BLOCK        
              614  JUMP_FORWARD        676  'to 676'
            616_0  COME_FROM_EXCEPT    568  '568'

 L. 143       616  DUP_TOP          
              618  LOAD_GLOBAL              Exception
              620  COMPARE_OP               exception-match
              622  POP_JUMP_IF_FALSE   674  'to 674'
              626  POP_TOP          
              628  POP_TOP          
              630  POP_TOP          

 L. 144       632  LOAD_GLOBAL              print_error
              634  LOAD_STR                 'unexpected error {0}'
              636  LOAD_ATTR                format

 L. 145       638  LOAD_GLOBAL              traceback
              640  LOAD_ATTR                format_exc
              642  CALL_FUNCTION_0       0  '0 positional arguments'
              644  CALL_FUNCTION_1       1  '1 positional argument'
              646  CALL_FUNCTION_1       1  '1 positional argument'
              648  POP_TOP          

 L. 146       650  LOAD_CONST               (False, False)
              652  UNPACK_SEQUENCE_2     2 
              654  STORE_FAST               'tc_status'
              656  STORE_FAST               'tc_duration'

 L. 147       658  LOAD_GLOBAL              Utils
              660  LOAD_ATTR                testcase_Utils
              662  LOAD_ATTR                get_impact_from_xmlfile

 L. 148       664  LOAD_FAST                'testcase'
              666  CALL_FUNCTION_1       1  '1 positional argument'
              668  STORE_FAST               'tc_impact'
              670  POP_EXCEPT       
              672  JUMP_FORWARD        676  'to 676'
              674  END_FINALLY      
            676_0  COME_FROM           672  '672'
            676_1  COME_FROM           614  '614'
              676  JUMP_ABSOLUTE      1354  'to 1354'
            680_0  COME_FROM           554  '554'

 L. 150       680  LOAD_FAST                'goto_tc'
              682  POP_JUMP_IF_FALSE   826  'to 826'
              686  LOAD_FAST                'goto_tc'
              688  LOAD_GLOBAL              str
              690  LOAD_FAST                'tests'
              692  CALL_FUNCTION_1       1  '1 positional argument'
              694  COMPARE_OP               ==
              696  POP_JUMP_IF_FALSE   826  'to 826'
              700  LOAD_FAST                'action'
              702  LOAD_CONST               True
              704  COMPARE_OP               is
              706  POP_JUMP_IF_FALSE   826  'to 826'

 L. 152       710  SETUP_EXCEPT        762  'to 762'

 L. 153       712  LOAD_GLOBAL              testcase_driver
              714  LOAD_ATTR                main
              716  LOAD_FAST                'tc_path'

 L. 154       718  LOAD_FAST                'data_repository'

 L. 155       720  LOAD_FAST                'tc_context'

 L. 156       722  LOAD_FAST                'tc_runtype'

 L. 157       724  LOAD_FAST                'auto_defects'

 L. 158       726  LOAD_FAST                'suite_name'

 L. 159       728  LOAD_FAST                'tc_onError_action'

 L. 160       730  LOAD_FAST                'iter_ts_sys'
              732  LOAD_CONST               ('runtype', 'auto_defects', 'suite', 'tc_onError_action', 'iter_ts_sys')
              734  CALL_FUNCTION_KW_8     8  '8 total positional and keyword args'
              736  STORE_FAST               'tc_result'

 L. 161       738  LOAD_FAST                'tc_result'
              740  LOAD_CONST               0
              742  BINARY_SUBSCR    
              744  STORE_FAST               'tc_status'

 L. 162       746  LOAD_FAST                'tc_result'
              748  LOAD_CONST               1
              750  BINARY_SUBSCR    
              752  STORE_FAST               'tc_duration'

 L. 163       754  LOAD_CONST               False
              756  STORE_FAST               'goto_tc'
              758  POP_BLOCK        
              760  JUMP_FORWARD        822  'to 822'
            762_0  COME_FROM_EXCEPT    710  '710'

 L. 165       762  DUP_TOP          
              764  LOAD_GLOBAL              Exception
              766  COMPARE_OP               exception-match
              768  POP_JUMP_IF_FALSE   820  'to 820'
              772  POP_TOP          
              774  POP_TOP          
              776  POP_TOP          

 L. 166       778  LOAD_GLOBAL              print_error
              780  LOAD_STR                 'unexpected error {0}'
              782  LOAD_ATTR                format

 L. 167       784  LOAD_GLOBAL              traceback
              786  LOAD_ATTR                format_exc
              788  CALL_FUNCTION_0       0  '0 positional arguments'
              790  CALL_FUNCTION_1       1  '1 positional argument'
              792  CALL_FUNCTION_1       1  '1 positional argument'
              794  POP_TOP          

 L. 168       796  LOAD_CONST               (False, False)
              798  UNPACK_SEQUENCE_2     2 
              800  STORE_FAST               'tc_status'
              802  STORE_FAST               'tc_duration'

 L. 169       804  LOAD_GLOBAL              Utils
              806  LOAD_ATTR                testcase_Utils
              808  LOAD_ATTR                get_impact_from_xmlfile

 L. 170       810  LOAD_FAST                'testcase'
              812  CALL_FUNCTION_1       1  '1 positional argument'
              814  STORE_FAST               'tc_impact'
              816  POP_EXCEPT       
              818  JUMP_FORWARD        822  'to 822'
              820  END_FINALLY      
            822_0  COME_FROM           818  '818'
            822_1  COME_FROM           760  '760'
              822  JUMP_ABSOLUTE      1354  'to 1354'
            826_0  COME_FROM           696  '696'
            826_1  COME_FROM           682  '682'

 L. 173       826  LOAD_GLOBAL              print_info
              828  LOAD_STR                 'skipped testcase %s '
              830  LOAD_FAST                'tc_name'
              832  BINARY_MODULO    
              834  CALL_FUNCTION_1       1  '1 positional argument'
              836  POP_TOP          

 L. 174       838  LOAD_FAST                'skipped'
              840  LOAD_CONST               1
              842  INPLACE_ADD      
              844  STORE_FAST               'skipped'

 L. 175       846  LOAD_GLOBAL              testsuite_utils
              848  LOAD_ATTR                pSuite_testcase_skip
              850  LOAD_FAST                'junit_resultfile'
              852  CALL_FUNCTION_1       1  '1 positional argument'
              854  POP_TOP          

 L. 176       856  LOAD_GLOBAL              testsuite_utils
              858  LOAD_ATTR                pSuite_update_suite_attributes

 L. 177       860  LOAD_FAST                'junit_resultfile'
              862  LOAD_GLOBAL              str
              864  LOAD_FAST                'errors'
              866  CALL_FUNCTION_1       1  '1 positional argument'
              868  LOAD_GLOBAL              str
              870  LOAD_FAST                'skipped'
              872  CALL_FUNCTION_1       1  '1 positional argument'

 L. 178       874  LOAD_GLOBAL              str
              876  LOAD_FAST                'tests'
              878  CALL_FUNCTION_1       1  '1 positional argument'
              880  LOAD_GLOBAL              str
              882  LOAD_FAST                'failures'
              884  CALL_FUNCTION_1       1  '1 positional argument'
              886  LOAD_STR                 '0'
              888  LOAD_CONST               ('time',)
              890  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
              892  POP_TOP          

 L. 179       894  LOAD_FAST                'data_repository'
              896  LOAD_STR                 'wt_junit_object'
              898  BINARY_SUBSCR    
              900  LOAD_ATTR                update_count

 L. 180       902  LOAD_STR                 'skipped'
              904  LOAD_STR                 '1'
              906  LOAD_STR                 'ts'

 L. 181       908  LOAD_FAST                'data_repository'
              910  LOAD_STR                 'wt_ts_timestamp'
              912  BINARY_SUBSCR    
              914  CALL_FUNCTION_4       4  '4 positional arguments'
              916  POP_TOP          

 L. 182       918  LOAD_FAST                'data_repository'
              920  LOAD_STR                 'wt_junit_object'
              922  BINARY_SUBSCR    
              924  LOAD_ATTR                update_count

 L. 183       926  LOAD_STR                 'tests'
              928  LOAD_STR                 '1'
              930  LOAD_STR                 'ts'

 L. 184       932  LOAD_FAST                'data_repository'
              934  LOAD_STR                 'wt_ts_timestamp'
              936  BINARY_SUBSCR    
              938  CALL_FUNCTION_4       4  '4 positional arguments'
              940  POP_TOP          

 L. 185       942  LOAD_FAST                'data_repository'
              944  LOAD_STR                 'wt_junit_object'
              946  BINARY_SUBSCR    
              948  LOAD_ATTR                update_count

 L. 186       950  LOAD_STR                 'tests'
              952  LOAD_STR                 '1'
              954  LOAD_STR                 'pj'
              956  LOAD_STR                 'not applicable'
              958  CALL_FUNCTION_4       4  '4 positional arguments'
              960  POP_TOP          

 L. 187       962  LOAD_GLOBAL              str
              964  LOAD_GLOBAL              Utils
              966  LOAD_ATTR                datetime_utils
              968  LOAD_ATTR                get_current_timestamp
              970  CALL_FUNCTION_0       0  '0 positional arguments'
              972  CALL_FUNCTION_1       1  '1 positional argument'
              974  STORE_FAST               'tmp_timestamp'

 L. 188       976  LOAD_GLOBAL              time
              978  LOAD_ATTR                sleep
              980  LOAD_CONST               2
              982  CALL_FUNCTION_1       1  '1 positional argument'
              984  POP_TOP          

 L. 189       986  LOAD_FAST                'data_repository'
              988  LOAD_STR                 'wt_junit_object'
              990  BINARY_SUBSCR    
              992  LOAD_ATTR                create_testcase

 L. 190       994  LOAD_STR                 'from testsuite'

 L. 191       996  LOAD_FAST                'tmp_timestamp'

 L. 192       998  LOAD_FAST                'data_repository'
             1000  LOAD_STR                 'wt_ts_timestamp'
             1002  BINARY_SUBSCR    

 L. 193      1004  LOAD_FAST                'data_repository'
             1006  LOAD_STR                 'wt_suite_name'
             1008  BINARY_SUBSCR    

 L. 194      1010  LOAD_GLOBAL              os
             1012  LOAD_ATTR                path
             1014  LOAD_ATTR                splitext
             1016  LOAD_FAST                'tc_name'
             1018  CALL_FUNCTION_1       1  '1 positional argument'
             1020  LOAD_CONST               0
             1022  BINARY_SUBSCR    
             1024  LOAD_CONST               ('location', 'timestamp', 'ts_timestamp', 'classname', 'name')
             1026  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
             1028  POP_TOP          

 L. 195      1030  LOAD_FAST                'data_repository'
             1032  LOAD_STR                 'wt_junit_object'
             1034  BINARY_SUBSCR    
             1036  LOAD_ATTR                add_testcase_message

 L. 196      1038  LOAD_FAST                'tmp_timestamp'
             1040  LOAD_STR                 'skipped'
             1042  CALL_FUNCTION_2       2  '2 positional arguments'
             1044  POP_TOP          

 L. 197      1046  LOAD_FAST                'data_repository'
             1048  LOAD_STR                 'wt_junit_object'
             1050  BINARY_SUBSCR    
             1052  LOAD_ATTR                update_attr

 L. 198      1054  LOAD_STR                 'status'
             1056  LOAD_STR                 'SKIPPED'
             1058  LOAD_STR                 'tc'
             1060  LOAD_FAST                'tmp_timestamp'
             1062  CALL_FUNCTION_4       4  '4 positional arguments'
             1064  POP_TOP          

 L. 199      1066  LOAD_STR                 'SKIP'
             1068  LOAD_FAST                'data_repository'
             1070  LOAD_STR                 'testcase_%d_result'
             1072  LOAD_FAST                'tests'
             1074  BINARY_MODULO    
             1076  STORE_SUBSCR     

 L. 200      1078  LOAD_GLOBAL              Utils
             1080  LOAD_ATTR                file_Utils
             1082  LOAD_ATTR                fileExists
             1084  LOAD_FAST                'tc_path'
             1086  CALL_FUNCTION_1       1  '1 positional argument'
             1088  POP_JUMP_IF_FALSE  1108  'to 1108'

 L. 201      1092  LOAD_GLOBAL              Utils
             1094  LOAD_ATTR                xml_Utils
             1096  LOAD_ATTR                getChildTextbyParentTag

 L. 202      1098  LOAD_FAST                'tc_path'
             1100  LOAD_STR                 'Details'
             1102  LOAD_STR                 'Title'
             1104  CALL_FUNCTION_3       3  '3 positional arguments'
             1106  STORE_FAST               'title'
           1108_0  COME_FROM          1088  '1088'

 L. 203      1108  LOAD_GLOBAL              Utils
             1110  LOAD_ATTR                file_Utils
             1112  LOAD_ATTR                fileExists
             1114  LOAD_FAST                'tc_path'
             1116  CALL_FUNCTION_1       1  '1 positional argument'
             1118  POP_JUMP_IF_FALSE  1136  'to 1136'
             1122  LOAD_FAST                'title'
             1124  POP_JUMP_IF_FALSE  1136  'to 1136'
             1128  LOAD_FAST                'title'
             1130  LOAD_ATTR                strip
             1132  CALL_FUNCTION_0       0  '0 positional arguments'
             1134  JUMP_FORWARD       1138  'to 1138'
           1136_0  COME_FROM          1118  '1118'
             1136  LOAD_STR                 'None'
           1138_0  COME_FROM          1134  '1134'
             1138  STORE_FAST               'title'

 L. 204      1140  LOAD_FAST                'data_repository'
             1142  LOAD_STR                 'wt_junit_object'
             1144  BINARY_SUBSCR    
             1146  LOAD_ATTR                update_attr

 L. 205      1148  LOAD_STR                 'title'
             1150  LOAD_FAST                'title'
             1152  LOAD_STR                 'tc'
             1154  LOAD_FAST                'tmp_timestamp'
             1156  CALL_FUNCTION_4       4  '4 positional arguments'
             1158  POP_TOP          

 L. 206      1160  LOAD_FAST                'data_repository'
             1162  LOAD_STR                 'wt_junit_object'
             1164  BINARY_SUBSCR    
             1166  LOAD_ATTR                update_attr

 L. 207      1168  LOAD_STR                 'impact'
             1170  LOAD_FAST                'impact_dict'
             1172  LOAD_ATTR                get
             1174  LOAD_FAST                'tc_impact'
             1176  LOAD_ATTR                upper
             1178  CALL_FUNCTION_0       0  '0 positional arguments'
             1180  CALL_FUNCTION_1       1  '1 positional argument'

 L. 208      1182  LOAD_STR                 'tc'
             1184  LOAD_FAST                'tmp_timestamp'
             1186  CALL_FUNCTION_4       4  '4 positional arguments'
             1188  POP_TOP          

 L. 209      1190  LOAD_FAST                'data_repository'
             1192  LOAD_STR                 'wt_junit_object'
             1194  BINARY_SUBSCR    
             1196  LOAD_ATTR                update_attr

 L. 210      1198  LOAD_STR                 'onerror'
             1200  LOAD_STR                 'N/A'
             1202  LOAD_STR                 'tc'
             1204  LOAD_FAST                'tmp_timestamp'
             1206  CALL_FUNCTION_4       4  '4 positional arguments'
             1208  POP_TOP          

 L. 211      1210  LOAD_FAST                'data_repository'
             1212  LOAD_STR                 'wt_junit_object'
             1214  BINARY_SUBSCR    
             1216  LOAD_ATTR                output_junit

 L. 212      1218  LOAD_FAST                'data_repository'
             1220  LOAD_STR                 'wt_results_execdir'
             1222  BINARY_SUBSCR    

 L. 213      1224  LOAD_CONST               False
             1226  LOAD_CONST               ('print_summary',)
             1228  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1230  POP_TOP          

 L. 214      1232  CONTINUE            114  'to 114'
             1234  JUMP_FORWARD       1354  'to 1354'
             1236  ELSE                     '1354'

 L. 217      1236  LOAD_FAST                'errors'
             1238  LOAD_CONST               1
             1240  INPLACE_ADD      
             1242  STORE_FAST               'errors'

 L. 218      1244  LOAD_GLOBAL              print_error
             1246  LOAD_STR                 'Test case does not exist in the provided path: {0}'
             1248  LOAD_ATTR                format

 L. 219      1250  LOAD_FAST                'tc_path'
             1252  CALL_FUNCTION_1       1  '1 positional argument'
             1254  CALL_FUNCTION_1       1  '1 positional argument'
             1256  STORE_FAST               'msg'

 L. 220      1258  LOAD_GLOBAL              testsuite_utils
             1260  LOAD_ATTR                pSuite_testcase
             1262  LOAD_FAST                'junit_resultfile'
             1264  LOAD_FAST                'suite_name'

 L. 221      1266  LOAD_FAST                'tc_path'
             1268  LOAD_STR                 '0'
             1270  LOAD_CONST               ('time',)
             1272  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
             1274  POP_TOP          

 L. 222      1276  LOAD_GLOBAL              testsuite_utils
             1278  LOAD_ATTR                pSuite_testcase_error
             1280  LOAD_FAST                'junit_resultfile'
             1282  LOAD_FAST                'msg'
             1284  LOAD_STR                 '0'
             1286  CALL_FUNCTION_3       3  '3 positional arguments'
             1288  POP_TOP          

 L. 223      1290  LOAD_STR                 'ERROR'
             1292  STORE_FAST               'tc_status'

 L. 224      1294  LOAD_FAST                'goto_tc'
             1296  POP_JUMP_IF_FALSE  1320  'to 1320'
             1300  LOAD_FAST                'goto_tc'
             1302  LOAD_GLOBAL              str
             1304  LOAD_FAST                'tests'
             1306  CALL_FUNCTION_1       1  '1 positional argument'
             1308  COMPARE_OP               ==
             1310  POP_JUMP_IF_FALSE  1320  'to 1320'

 L. 225      1314  LOAD_CONST               False
             1316  STORE_FAST               'goto_tc'
             1318  JUMP_FORWARD       1354  'to 1354'
           1320_0  COME_FROM          1296  '1296'

 L. 226      1320  LOAD_FAST                'goto_tc'
             1322  POP_JUMP_IF_FALSE  1354  'to 1354'
             1326  LOAD_FAST                'goto_tc'
             1328  LOAD_GLOBAL              str
             1330  LOAD_FAST                'tests'
             1332  CALL_FUNCTION_1       1  '1 positional argument'
             1334  COMPARE_OP               !=
             1336  POP_JUMP_IF_FALSE  1354  'to 1354'

 L. 227      1340  LOAD_STR                 'ERROR'
             1342  LOAD_FAST                'data_repository'
             1344  LOAD_STR                 'testcase_%d_result'
             1346  LOAD_FAST                'tests'
             1348  BINARY_MODULO    
             1350  STORE_SUBSCR     

 L. 228      1352  CONTINUE            114  'to 114'
           1354_0  COME_FROM          1322  '1322'
           1354_1  COME_FROM          1318  '1318'
           1354_2  COME_FROM          1234  '1234'

 L. 230      1354  LOAD_GLOBAL              onerror_driver
             1356  LOAD_ATTR                main
             1358  LOAD_FAST                'testcase'
             1360  LOAD_FAST                'suite_error_action'

 L. 231      1362  LOAD_FAST                'suite_error_value'
             1364  CALL_FUNCTION_3       3  '3 positional arguments'
             1366  STORE_FAST               'goto_tc_num'

 L. 232      1368  LOAD_FAST                'goto_tc_num'
             1370  LOAD_CONST               False
             1372  COMPARE_OP               is
             1374  POP_JUMP_IF_FALSE  1384  'to 1384'

 L. 233      1378  LOAD_STR                 'Next'
             1380  STORE_FAST               'onerror'
             1382  JUMP_FORWARD       1412  'to 1412'
             1384  ELSE                     '1412'

 L. 234      1384  LOAD_FAST                'goto_tc_num'
             1386  LOAD_STR                 'ABORT'
             1388  COMPARE_OP               ==
             1390  POP_JUMP_IF_FALSE  1400  'to 1400'

 L. 235      1394  LOAD_STR                 'Abort'
             1396  STORE_FAST               'onerror'
             1398  JUMP_FORWARD       1412  'to 1412'
             1400  ELSE                     '1412'

 L. 237      1400  LOAD_STR                 'Goto:'
             1402  LOAD_GLOBAL              str
             1404  LOAD_FAST                'goto_tc_num'
             1406  CALL_FUNCTION_1       1  '1 positional argument'
             1408  BINARY_ADD       
             1410  STORE_FAST               'onerror'
           1412_0  COME_FROM          1398  '1398'
           1412_1  COME_FROM          1382  '1382'

 L. 238      1412  LOAD_FAST                'data_repository'
             1414  LOAD_STR                 'wt_junit_object'
             1416  BINARY_SUBSCR    
             1418  LOAD_ATTR                update_attr

 L. 239      1420  LOAD_STR                 'impact'
             1422  LOAD_FAST                'impact_dict'
             1424  LOAD_ATTR                get
             1426  LOAD_FAST                'tc_impact'
             1428  LOAD_ATTR                upper
             1430  CALL_FUNCTION_0       0  '0 positional arguments'
             1432  CALL_FUNCTION_1       1  '1 positional argument'
             1434  LOAD_STR                 'tc'

 L. 240      1436  LOAD_FAST                'data_repository'
             1438  LOAD_STR                 'wt_tc_timestamp'
             1440  BINARY_SUBSCR    
             1442  CALL_FUNCTION_4       4  '4 positional arguments'
             1444  POP_TOP          

 L. 241      1446  LOAD_FAST                'data_repository'
             1448  LOAD_STR                 'wt_junit_object'
             1450  BINARY_SUBSCR    
             1452  LOAD_ATTR                update_attr

 L. 242      1454  LOAD_STR                 'onerror'
             1456  LOAD_FAST                'onerror'
             1458  LOAD_STR                 'tc'

 L. 243      1460  LOAD_FAST                'data_repository'
             1462  LOAD_STR                 'wt_tc_timestamp'
             1464  BINARY_SUBSCR    
             1466  CALL_FUNCTION_4       4  '4 positional arguments'
             1468  POP_TOP          

 L. 246      1470  LOAD_GLOBAL              common_execution_utils
             1472  LOAD_ATTR                compute_status
             1474  LOAD_FAST                'testcase'
             1476  LOAD_FAST                'tc_status_list'

 L. 247      1478  LOAD_FAST                'tc_impact_list'

 L. 248      1480  LOAD_FAST                'tc_status'
             1482  LOAD_FAST                'tc_impact'
             1484  CALL_FUNCTION_5       5  '5 positional arguments'
             1486  UNPACK_SEQUENCE_2     2 
             1488  STORE_FAST               'tc_status_list'
             1490  STORE_FAST               'tc_impact_list'

 L. 249      1492  LOAD_FAST                'tc_duration_list'
             1494  LOAD_ATTR                append
             1496  LOAD_FAST                'tc_duration'
             1498  CALL_FUNCTION_1       1  '1 positional argument'
             1500  POP_TOP          

 L. 251      1502  LOAD_STR                 'PASS'
             1504  LOAD_STR                 'FAIL'
             1506  LOAD_STR                 'ERROR'

 L. 252      1508  LOAD_STR                 'SKIP'
             1510  LOAD_STR                 'RAN'
             1512  LOAD_CONST               ('TRUE', 'FALSE', 'ERROR', 'SKIP', 'RAN')
             1514  BUILD_CONST_KEY_MAP_5     5 
             1516  STORE_FAST               'string_status'

 L. 254      1518  LOAD_GLOBAL              str
             1520  LOAD_FAST                'tc_status'
             1522  CALL_FUNCTION_1       1  '1 positional argument'
             1524  LOAD_ATTR                upper
             1526  CALL_FUNCTION_0       0  '0 positional arguments'
             1528  LOAD_GLOBAL              list
             1530  LOAD_FAST                'string_status'
             1532  LOAD_ATTR                keys
             1534  CALL_FUNCTION_0       0  '0 positional arguments'
             1536  CALL_FUNCTION_1       1  '1 positional argument'
             1538  COMPARE_OP               in
             1540  POP_JUMP_IF_FALSE  1570  'to 1570'

 L. 255      1544  LOAD_FAST                'string_status'

 L. 256      1546  LOAD_GLOBAL              str
             1548  LOAD_FAST                'tc_status'
             1550  CALL_FUNCTION_1       1  '1 positional argument'
             1552  LOAD_ATTR                upper
             1554  CALL_FUNCTION_0       0  '0 positional arguments'
             1556  BINARY_SUBSCR    
             1558  LOAD_FAST                'data_repository'
             1560  LOAD_STR                 'testcase_%d_result'
             1562  LOAD_FAST                'tests'
             1564  BINARY_MODULO    
             1566  STORE_SUBSCR     
             1568  JUMP_FORWARD       1590  'to 1590'
             1570  ELSE                     '1590'

 L. 258      1570  LOAD_GLOBAL              print_error
             1572  LOAD_STR                 'unexpected testcase status, default to exception'
             1574  CALL_FUNCTION_1       1  '1 positional argument'
             1576  POP_TOP          

 L. 259      1578  LOAD_STR                 'ERROR'
             1580  LOAD_FAST                'data_repository'
             1582  LOAD_STR                 'testcase_%d_result'
             1584  LOAD_FAST                'tests'
             1586  BINARY_MODULO    
             1588  STORE_SUBSCR     
           1590_0  COME_FROM          1568  '1568'

 L. 261      1590  LOAD_FAST                'tc_impact'
             1592  LOAD_ATTR                upper
             1594  CALL_FUNCTION_0       0  '0 positional arguments'
             1596  LOAD_STR                 'IMPACT'
             1598  COMPARE_OP               ==
             1600  POP_JUMP_IF_FALSE  1610  'to 1610'

 L. 262      1604  LOAD_STR                 'Status of the executed test case impacts Testsuite result'
             1606  STORE_FAST               'msg'
             1608  JUMP_FORWARD       1628  'to 1628'
             1610  ELSE                     '1628'

 L. 263      1610  LOAD_FAST                'tc_impact'
             1612  LOAD_ATTR                upper
             1614  CALL_FUNCTION_0       0  '0 positional arguments'
             1616  LOAD_STR                 'NOIMPACT'
             1618  COMPARE_OP               ==
             1620  POP_JUMP_IF_FALSE  1628  'to 1628'

 L. 264      1624  LOAD_STR                 'Status of the executed test case does not impact '
             1626  STORE_FAST               'msg'
           1628_0  COME_FROM          1620  '1620'
           1628_1  COME_FROM          1608  '1608'

 L. 266      1628  LOAD_GLOBAL              print_debug
             1630  LOAD_FAST                'msg'
             1632  CALL_FUNCTION_1       1  '1 positional argument'
             1634  POP_TOP          

 L. 268      1636  LOAD_GLOBAL              common_execution_utils
             1638  LOAD_ATTR                get_runmode_from_xmlfile

 L. 269      1640  LOAD_FAST                'testcase'
             1642  CALL_FUNCTION_1       1  '1 positional argument'
             1644  UNPACK_SEQUENCE_3     3 
             1646  STORE_FAST               'runmode'
             1648  STORE_FAST               'value'
             1650  STORE_FAST               '_'

 L. 271      1652  LOAD_GLOBAL              common_execution_utils
             1654  LOAD_ATTR                get_retry_from_xmlfile
             1656  LOAD_FAST                'testcase'
             1658  CALL_FUNCTION_1       1  '1 positional argument'
             1660  UNPACK_SEQUENCE_5     5 
             1662  STORE_FAST               'retry_type'
             1664  STORE_FAST               'retry_cond'
             1666  STORE_FAST               'retry_cond_value'
             1668  STORE_FAST               'retry_value'
             1670  STORE_FAST               'retry_interval'

 L. 273      1672  LOAD_FAST                'runmode'
             1674  LOAD_CONST               None
             1676  COMPARE_OP               is-not
             1678  POP_JUMP_IF_TRUE   1692  'to 1692'
             1682  LOAD_FAST                'tc_status'
             1684  LOAD_STR                 'ERROR'
             1686  COMPARE_OP               ==
           1688_0  COME_FROM          1678  '1678'
             1688  POP_JUMP_IF_FALSE  2098  'to 2098'

 L. 274      1692  LOAD_FAST                'tc_status'
             1694  LOAD_CONST               True
             1696  COMPARE_OP               is
             1698  POP_JUMP_IF_FALSE  1742  'to 1742'

 L. 275      1702  LOAD_GLOBAL              testsuite_utils
             1704  LOAD_ATTR                update_tc_duration
             1706  LOAD_GLOBAL              str
             1708  LOAD_FAST                'tc_duration'
             1710  CALL_FUNCTION_1       1  '1 positional argument'
             1712  CALL_FUNCTION_1       1  '1 positional argument'
             1714  POP_TOP          

 L. 278      1716  LOAD_FAST                'runmode'
             1718  LOAD_ATTR                upper
             1720  CALL_FUNCTION_0       0  '0 positional arguments'
             1722  LOAD_STR                 'RUP'
             1724  COMPARE_OP               ==
             1726  POP_JUMP_IF_FALSE  2094  'to 2094'

 L. 279      1730  LOAD_GLOBAL              str
             1732  LOAD_FAST                'value'
             1734  CALL_FUNCTION_1       1  '1 positional argument'
             1736  STORE_FAST               'goto_tc'
             1738  JUMP_ABSOLUTE      2470  'to 2470'
             1742  ELSE                     '2096'

 L. 280      1742  LOAD_FAST                'tc_status'
             1744  LOAD_STR                 'ERROR'
             1746  COMPARE_OP               ==
             1748  POP_JUMP_IF_TRUE   1762  'to 1762'
             1752  LOAD_FAST                'tc_status'
             1754  LOAD_STR                 'EXCEPTION'
             1756  COMPARE_OP               ==
           1758_0  COME_FROM          1748  '1748'
             1758  POP_JUMP_IF_FALSE  1928  'to 1928'

 L. 281      1762  LOAD_FAST                'errors'
             1764  LOAD_CONST               1
             1766  INPLACE_ADD      
             1768  STORE_FAST               'errors'

 L. 282      1770  LOAD_GLOBAL              testsuite_utils
             1772  LOAD_ATTR                pSuite_testcase_error

 L. 283      1774  LOAD_FAST                'junit_resultfile'

 L. 284      1776  LOAD_STR                 'Encountered error/exception during TC execution'

 L. 285      1778  LOAD_GLOBAL              str
             1780  LOAD_FAST                'tc_duration'
             1782  CALL_FUNCTION_1       1  '1 positional argument'
             1784  CALL_FUNCTION_3       3  '3 positional arguments'
             1786  POP_TOP          

 L. 286      1788  LOAD_GLOBAL              onerror_driver
             1790  LOAD_ATTR                main
             1792  LOAD_FAST                'testcase'
             1794  LOAD_FAST                'suite_error_action'

 L. 287      1796  LOAD_FAST                'suite_error_value'
             1798  CALL_FUNCTION_3       3  '3 positional arguments'
             1800  STORE_FAST               'goto_tc'

 L. 288      1802  LOAD_FAST                'goto_tc'
             1804  LOAD_CONST               ('ABORT', 'ABORT_AS_ERROR')
             1806  COMPARE_OP               in
             1808  POP_JUMP_IF_FALSE  1852  'to 1852'

 L. 289      1812  LOAD_GLOBAL              update_suite_attribs
             1814  LOAD_FAST                'junit_resultfile'
             1816  LOAD_GLOBAL              str
             1818  LOAD_FAST                'errors'
             1820  CALL_FUNCTION_1       1  '1 positional argument'

 L. 290      1822  LOAD_GLOBAL              str
             1824  LOAD_FAST                'skipped'
             1826  CALL_FUNCTION_1       1  '1 positional argument'
             1828  LOAD_GLOBAL              str
             1830  LOAD_FAST                'tests'
             1832  CALL_FUNCTION_1       1  '1 positional argument'

 L. 291      1834  LOAD_GLOBAL              str
             1836  LOAD_FAST                'failures'
             1838  CALL_FUNCTION_1       1  '1 positional argument'
             1840  LOAD_STR                 '0'
             1842  LOAD_CONST               ('time',)
             1844  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
             1846  POP_TOP          

 L. 292      1848  BREAK_LOOP       
             1850  JUMP_FORWARD       1888  'to 1888'
             1852  ELSE                     '1888'

 L. 295      1852  LOAD_FAST                'goto_tc'
             1854  POP_JUMP_IF_FALSE  1888  'to 1888'
             1858  LOAD_GLOBAL              int
             1860  LOAD_FAST                'goto_tc'
             1862  CALL_FUNCTION_1       1  '1 positional argument'
             1864  LOAD_FAST                'tests'
             1866  COMPARE_OP               <
             1868  POP_JUMP_IF_FALSE  1888  'to 1888'

 L. 296      1872  LOAD_GLOBAL              int
             1874  LOAD_FAST                'goto_tc'
             1876  CALL_FUNCTION_1       1  '1 positional argument'
             1878  LOAD_CONST               1
             1880  BINARY_SUBTRACT  
             1882  STORE_FAST               'tests'

 L. 297      1884  LOAD_CONST               False
             1886  STORE_FAST               'goto_tc'
           1888_0  COME_FROM          1868  '1868'
           1888_1  COME_FROM          1854  '1854'
           1888_2  COME_FROM          1850  '1850'

 L. 299      1888  LOAD_GLOBAL              int
             1890  LOAD_FAST                'goto_tc'
             1892  CALL_FUNCTION_1       1  '1 positional argument'
             1894  LOAD_GLOBAL              len
             1896  LOAD_FAST                'testcase_list'
             1898  CALL_FUNCTION_1       1  '1 positional argument'
             1900  COMPARE_OP               >
             1902  POP_JUMP_IF_FALSE  2094  'to 2094'

 L. 300      1906  LOAD_GLOBAL              print_warning
             1908  LOAD_STR                 "The goto value {} is more than no of TC's {} so skipping all the TC's"
             1910  LOAD_ATTR                format

 L. 301      1912  LOAD_FAST                'goto_tc'
             1914  LOAD_GLOBAL              len
             1916  LOAD_FAST                'testcase_list'
             1918  CALL_FUNCTION_1       1  '1 positional argument'
             1920  CALL_FUNCTION_2       2  '2 positional arguments'
             1922  CALL_FUNCTION_1       1  '1 positional argument'
             1924  POP_TOP          
             1926  JUMP_FORWARD       2094  'to 2094'
             1928  ELSE                     '2094'

 L. 302      1928  LOAD_FAST                'tc_status'
             1930  LOAD_CONST               False
             1932  COMPARE_OP               is
             1934  POP_JUMP_IF_FALSE  2470  'to 2470'

 L. 303      1938  LOAD_FAST                'failures'
             1940  LOAD_CONST               1
             1942  INPLACE_ADD      
             1944  STORE_FAST               'failures'

 L. 304      1946  LOAD_GLOBAL              testsuite_utils
             1948  LOAD_ATTR                pSuite_testcase_failure
             1950  LOAD_FAST                'junit_resultfile'

 L. 305      1952  LOAD_GLOBAL              str
             1954  LOAD_FAST                'tc_duration'
             1956  CALL_FUNCTION_1       1  '1 positional argument'
             1958  LOAD_CONST               ('time',)
             1960  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1962  POP_TOP          

 L. 306      1964  LOAD_GLOBAL              onerror_driver
             1966  LOAD_ATTR                main
             1968  LOAD_FAST                'testcase'
             1970  LOAD_FAST                'suite_error_action'

 L. 307      1972  LOAD_FAST                'suite_error_value'
             1974  CALL_FUNCTION_3       3  '3 positional arguments'
             1976  STORE_FAST               'goto_tc'

 L. 308      1978  LOAD_FAST                'goto_tc'
             1980  LOAD_CONST               ('ABORT', 'ABORT_AS_ERROR')
             1982  COMPARE_OP               in
             1984  POP_JUMP_IF_FALSE  2028  'to 2028'

 L. 309      1988  LOAD_GLOBAL              update_suite_attribs
             1990  LOAD_FAST                'junit_resultfile'
             1992  LOAD_GLOBAL              str
             1994  LOAD_FAST                'errors'
             1996  CALL_FUNCTION_1       1  '1 positional argument'

 L. 310      1998  LOAD_GLOBAL              str
             2000  LOAD_FAST                'skipped'
             2002  CALL_FUNCTION_1       1  '1 positional argument'
             2004  LOAD_GLOBAL              str
             2006  LOAD_FAST                'tests'
             2008  CALL_FUNCTION_1       1  '1 positional argument'

 L. 311      2010  LOAD_GLOBAL              str
             2012  LOAD_FAST                'failures'
             2014  CALL_FUNCTION_1       1  '1 positional argument'
             2016  LOAD_STR                 '0'
             2018  LOAD_CONST               ('time',)
             2020  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
             2022  POP_TOP          

 L. 312      2024  BREAK_LOOP       
             2026  JUMP_FORWARD       2064  'to 2064'
             2028  ELSE                     '2064'

 L. 315      2028  LOAD_FAST                'goto_tc'
             2030  POP_JUMP_IF_FALSE  2064  'to 2064'
             2034  LOAD_GLOBAL              int
             2036  LOAD_FAST                'goto_tc'
             2038  CALL_FUNCTION_1       1  '1 positional argument'
             2040  LOAD_FAST                'tests'
             2042  COMPARE_OP               <
             2044  POP_JUMP_IF_FALSE  2064  'to 2064'

 L. 316      2048  LOAD_GLOBAL              int
             2050  LOAD_FAST                'goto_tc'
             2052  CALL_FUNCTION_1       1  '1 positional argument'
             2054  LOAD_CONST               1
             2056  BINARY_SUBTRACT  
             2058  STORE_FAST               'tests'

 L. 317      2060  LOAD_CONST               False
             2062  STORE_FAST               'goto_tc'
           2064_0  COME_FROM          2044  '2044'
           2064_1  COME_FROM          2030  '2030'
           2064_2  COME_FROM          2026  '2026'

 L. 320      2064  LOAD_FAST                'goto_tc'
             2066  UNARY_NOT        
             2068  POP_JUMP_IF_FALSE  2470  'to 2470'
             2072  LOAD_FAST                'runmode'
             2074  LOAD_ATTR                upper
             2076  CALL_FUNCTION_0       0  '0 positional arguments'
             2078  LOAD_STR                 'RUF'
             2080  COMPARE_OP               ==
             2082  POP_JUMP_IF_FALSE  2470  'to 2470'

 L. 321      2086  LOAD_GLOBAL              str
             2088  LOAD_FAST                'value'
             2090  CALL_FUNCTION_1       1  '1 positional argument'
             2092  STORE_FAST               'goto_tc'
           2094_0  COME_FROM          1926  '1926'
           2094_1  COME_FROM          1902  '1902'
             2094  JUMP_FORWARD       2470  'to 2470'
             2098  ELSE                     '2470'

 L. 322      2098  LOAD_FAST                'retry_type'
             2100  LOAD_CONST               None
             2102  COMPARE_OP               is-not
             2104  POP_JUMP_IF_FALSE  2470  'to 2470'

 L. 323      2108  LOAD_FAST                'retry_type'
             2110  LOAD_ATTR                upper
             2112  CALL_FUNCTION_0       0  '0 positional arguments'
             2114  LOAD_STR                 'IF'
             2116  COMPARE_OP               ==
             2118  POP_JUMP_IF_FALSE  2280  'to 2280'

 L. 324      2122  SETUP_EXCEPT       2220  'to 2220'

 L. 325      2124  LOAD_FAST                'data_repository'
             2126  LOAD_FAST                'retry_cond'
             2128  BINARY_SUBSCR    
             2130  LOAD_FAST                'retry_cond_value'
             2132  COMPARE_OP               ==
             2134  POP_JUMP_IF_FALSE  2192  'to 2192'

 L. 326      2138  LOAD_CONST               True
             2140  STORE_FAST               'condition_met'

 L. 327      2142  LOAD_GLOBAL              pNote
             2144  LOAD_STR                 'Wait for {0}sec before retrying'
             2146  LOAD_ATTR                format

 L. 328      2148  LOAD_FAST                'retry_interval'
             2150  CALL_FUNCTION_1       1  '1 positional argument'
             2152  CALL_FUNCTION_1       1  '1 positional argument'
             2154  POP_TOP          

 L. 329      2156  LOAD_GLOBAL              pNote
             2158  LOAD_STR                 "The given condition '{0}' matches the expected value '{1}'"
             2160  LOAD_ATTR                format

 L. 330      2162  LOAD_FAST                'data_repository'
             2164  LOAD_FAST                'retry_cond'
             2166  BINARY_SUBSCR    

 L. 331      2168  LOAD_FAST                'retry_cond_value'
             2170  CALL_FUNCTION_2       2  '2 positional arguments'
             2172  CALL_FUNCTION_1       1  '1 positional argument'
             2174  POP_TOP          

 L. 332      2176  LOAD_GLOBAL              time
             2178  LOAD_ATTR                sleep
             2180  LOAD_GLOBAL              int
             2182  LOAD_FAST                'retry_interval'
             2184  CALL_FUNCTION_1       1  '1 positional argument'
             2186  CALL_FUNCTION_1       1  '1 positional argument'
             2188  POP_TOP          
             2190  JUMP_FORWARD       2216  'to 2216'
             2192  ELSE                     '2216'

 L. 334      2192  LOAD_CONST               False
             2194  STORE_FAST               'condition_met'

 L. 335      2196  LOAD_GLOBAL              print_warning
             2198  LOAD_STR                 "The condition value '{0}' does not match with the expected value '{1}'"
             2200  LOAD_ATTR                format

 L. 338      2202  LOAD_FAST                'data_repository'
             2204  LOAD_FAST                'retry_cond'
             2206  BINARY_SUBSCR    

 L. 339      2208  LOAD_FAST                'retry_cond_value'
             2210  CALL_FUNCTION_2       2  '2 positional arguments'
             2212  CALL_FUNCTION_1       1  '1 positional argument'
             2214  POP_TOP          
           2216_0  COME_FROM          2190  '2190'
             2216  POP_BLOCK        
             2218  JUMP_FORWARD       2260  'to 2260'
           2220_0  COME_FROM_EXCEPT   2122  '2122'

 L. 340      2220  DUP_TOP          
             2222  LOAD_GLOBAL              KeyError
             2224  COMPARE_OP               exception-match
             2226  POP_JUMP_IF_FALSE  2258  'to 2258'
             2230  POP_TOP          
             2232  POP_TOP          
             2234  POP_TOP          

 L. 341      2236  LOAD_GLOBAL              print_warning
             2238  LOAD_STR                 "The given condition '{0}' is not there in the data repository"
             2240  LOAD_ATTR                format

 L. 343      2242  LOAD_FAST                'retry_cond_value'
             2244  CALL_FUNCTION_1       1  '1 positional argument'
             2246  CALL_FUNCTION_1       1  '1 positional argument'
             2248  POP_TOP          

 L. 344      2250  LOAD_CONST               False
             2252  STORE_FAST               'condition_met'
             2254  POP_EXCEPT       
             2256  JUMP_FORWARD       2260  'to 2260'
             2258  END_FINALLY      
           2260_0  COME_FROM          2256  '2256'
           2260_1  COME_FROM          2218  '2218'

 L. 345      2260  LOAD_FAST                'condition_met'
             2262  LOAD_CONST               False
             2264  COMPARE_OP               is
             2266  POP_JUMP_IF_FALSE  2470  'to 2470'

 L. 346      2270  LOAD_GLOBAL              str
             2272  LOAD_FAST                'retry_value'
             2274  CALL_FUNCTION_1       1  '1 positional argument'
             2276  STORE_FAST               'goto_tc'
             2278  JUMP_FORWARD       2470  'to 2470'
             2280  ELSE                     '2470'

 L. 348      2280  LOAD_FAST                'retry_type'
             2282  LOAD_ATTR                upper
             2284  CALL_FUNCTION_0       0  '0 positional arguments'
             2286  LOAD_STR                 'IF NOT'
             2288  COMPARE_OP               ==
             2290  POP_JUMP_IF_FALSE  2470  'to 2470'

 L. 349      2294  SETUP_EXCEPT       2392  'to 2392'

 L. 350      2296  LOAD_FAST                'data_repository'
             2298  LOAD_FAST                'retry_cond'
             2300  BINARY_SUBSCR    
             2302  LOAD_FAST                'retry_cond_value'
             2304  COMPARE_OP               !=
             2306  POP_JUMP_IF_FALSE  2364  'to 2364'

 L. 351      2310  LOAD_CONST               True
             2312  STORE_FAST               'condition_met'

 L. 352      2314  LOAD_GLOBAL              pNote
             2316  LOAD_STR                 'Wait for {0}sec before retrying'
             2318  LOAD_ATTR                format

 L. 353      2320  LOAD_FAST                'retry_interval'
             2322  CALL_FUNCTION_1       1  '1 positional argument'
             2324  CALL_FUNCTION_1       1  '1 positional argument'
             2326  POP_TOP          

 L. 354      2328  LOAD_GLOBAL              pNote
             2330  LOAD_STR                 "The condition value '{0}' does not match with the expected value '{1}'"
             2332  LOAD_ATTR                format

 L. 356      2334  LOAD_FAST                'data_repository'
             2336  LOAD_FAST                'retry_cond'
             2338  BINARY_SUBSCR    

 L. 357      2340  LOAD_FAST                'retry_cond_value'
             2342  CALL_FUNCTION_2       2  '2 positional arguments'
             2344  CALL_FUNCTION_1       1  '1 positional argument'
             2346  POP_TOP          

 L. 358      2348  LOAD_GLOBAL              time
             2350  LOAD_ATTR                sleep
             2352  LOAD_GLOBAL              int
             2354  LOAD_FAST                'retry_interval'
             2356  CALL_FUNCTION_1       1  '1 positional argument'
             2358  CALL_FUNCTION_1       1  '1 positional argument'
             2360  POP_TOP          
             2362  JUMP_FORWARD       2388  'to 2388'
             2364  ELSE                     '2388'

 L. 360      2364  LOAD_CONST               False
             2366  STORE_FAST               'condition_met'

 L. 361      2368  LOAD_GLOBAL              print_warning
             2370  LOAD_STR                 "The given condition '{0}' matches the expected value '{1}'"
             2372  LOAD_ATTR                format

 L. 364      2374  LOAD_FAST                'data_repository'
             2376  LOAD_FAST                'retry_cond'
             2378  BINARY_SUBSCR    

 L. 365      2380  LOAD_FAST                'retry_cond_value'
             2382  CALL_FUNCTION_2       2  '2 positional arguments'
             2384  CALL_FUNCTION_1       1  '1 positional argument'
             2386  POP_TOP          
           2388_0  COME_FROM          2362  '2362'
             2388  POP_BLOCK        
             2390  JUMP_FORWARD       2432  'to 2432'
           2392_0  COME_FROM_EXCEPT   2294  '2294'

 L. 366      2392  DUP_TOP          
             2394  LOAD_GLOBAL              KeyError
             2396  COMPARE_OP               exception-match
             2398  POP_JUMP_IF_FALSE  2430  'to 2430'
             2402  POP_TOP          
             2404  POP_TOP          
             2406  POP_TOP          

 L. 367      2408  LOAD_CONST               False
             2410  STORE_FAST               'condition_met'

 L. 368      2412  LOAD_GLOBAL              print_warning
             2414  LOAD_STR                 "The given condition '{0}' is not there in the data repository"
             2416  LOAD_ATTR                format

 L. 370      2418  LOAD_FAST                'retry_cond_value'
             2420  CALL_FUNCTION_1       1  '1 positional argument'
             2422  CALL_FUNCTION_1       1  '1 positional argument'
             2424  POP_TOP          
             2426  POP_EXCEPT       
             2428  JUMP_FORWARD       2432  'to 2432'
             2430  END_FINALLY      
           2432_0  COME_FROM          2428  '2428'
           2432_1  COME_FROM          2390  '2390'

 L. 371      2432  LOAD_FAST                'condition_met'
             2434  LOAD_CONST               False
             2436  COMPARE_OP               is
             2438  POP_JUMP_IF_FALSE  2470  'to 2470'

 L. 372      2442  LOAD_GLOBAL              pNote
             2444  LOAD_STR                 "The given condition '{0}' matched with the value '{1}'"
             2446  LOAD_ATTR                format

 L. 373      2448  LOAD_FAST                'data_repository'
             2450  LOAD_FAST                'retry_cond'
             2452  BINARY_SUBSCR    

 L. 374      2454  LOAD_FAST                'retry_cond_value'
             2456  CALL_FUNCTION_2       2  '2 positional arguments'
             2458  CALL_FUNCTION_1       1  '1 positional argument'
             2460  POP_TOP          

 L. 375      2462  LOAD_GLOBAL              str
             2464  LOAD_FAST                'retry_value'
             2466  CALL_FUNCTION_1       1  '1 positional argument'
             2468  STORE_FAST               'goto_tc'
           2470_0  COME_FROM          2438  '2438'
           2470_1  COME_FROM          2290  '2290'
           2470_2  COME_FROM          2278  '2278'
           2470_3  COME_FROM          2266  '2266'
           2470_4  COME_FROM          2104  '2104'
           2470_5  COME_FROM          2094  '2094'
           2470_6  COME_FROM          2082  '2082'
           2470_7  COME_FROM          2068  '2068'
           2470_8  COME_FROM          1934  '1934'

 L. 378      2470  LOAD_GLOBAL              update_suite_attribs
             2472  LOAD_FAST                'junit_resultfile'
             2474  LOAD_GLOBAL              str
             2476  LOAD_FAST                'errors'
             2478  CALL_FUNCTION_1       1  '1 positional argument'

 L. 379      2480  LOAD_GLOBAL              str
             2482  LOAD_FAST                'skipped'
             2484  CALL_FUNCTION_1       1  '1 positional argument'
             2486  LOAD_GLOBAL              str
             2488  LOAD_FAST                'tests'
             2490  CALL_FUNCTION_1       1  '1 positional argument'
             2492  LOAD_GLOBAL              str
             2494  LOAD_FAST                'failures'
             2496  CALL_FUNCTION_1       1  '1 positional argument'

 L. 380      2498  LOAD_STR                 '0'
             2500  LOAD_CONST               ('time',)
             2502  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
             2504  POP_TOP          

 L. 383      2506  LOAD_FAST                'ts_iter'
             2508  LOAD_CONST               False
             2510  COMPARE_OP               is
             2512  POP_JUMP_IF_FALSE   114  'to 114'

 L. 384      2514  LOAD_FAST                'tc_junit_list'
             2516  LOAD_ATTR                append
             2518  LOAD_FAST                'data_repository'
             2520  LOAD_STR                 'wt_junit_object'
             2522  BINARY_SUBSCR    
             2524  CALL_FUNCTION_1       1  '1 positional argument'
             2526  POP_TOP          
             2528  JUMP_BACK           114  'to 114'
           2530_0  COME_FROM           124  '124'
             2530  POP_BLOCK        
           2532_0  COME_FROM_LOOP      110  '110'

 L. 388      2532  LOAD_FAST                'ts_iter'
             2534  LOAD_CONST               True
             2536  COMPARE_OP               is
             2538  POP_JUMP_IF_FALSE  2550  'to 2550'

 L. 389      2542  LOAD_FAST                'data_repository'
             2544  LOAD_STR                 'wt_junit_object'
             2546  BINARY_SUBSCR    
             2548  STORE_FAST               'tc_junit_list'
           2550_0  COME_FROM          2538  '2538'

 L. 392      2550  LOAD_FAST                'testcase'
             2552  LOAD_ATTR                find
             2554  LOAD_STR                 'runmode'
             2556  CALL_FUNCTION_1       1  '1 positional argument'
             2558  LOAD_CONST               None
             2560  COMPARE_OP               is-not
             2562  POP_JUMP_IF_FALSE  2630  'to 2630'

 L. 393      2566  LOAD_FAST                'testcase'
             2568  LOAD_ATTR                find
             2570  LOAD_STR                 'runmode'
             2572  CALL_FUNCTION_1       1  '1 positional argument'
             2574  LOAD_ATTR                get
             2576  LOAD_STR                 'attempt'
             2578  CALL_FUNCTION_1       1  '1 positional argument'
             2580  LOAD_CONST               None
             2582  COMPARE_OP               is-not
             2584  POP_JUMP_IF_FALSE  2630  'to 2630'

 L. 394      2588  LOAD_FAST                'testcase'
             2590  LOAD_ATTR                find
             2592  LOAD_STR                 'runmode'
             2594  CALL_FUNCTION_1       1  '1 positional argument'
             2596  LOAD_ATTR                get
             2598  LOAD_STR                 'attempt'
             2600  CALL_FUNCTION_1       1  '1 positional argument'

 L. 395      2602  LOAD_FAST                'testcase'
             2604  LOAD_ATTR                find
             2606  LOAD_STR                 'runmode'
             2608  CALL_FUNCTION_1       1  '1 positional argument'
             2610  LOAD_ATTR                get
             2612  LOAD_STR                 'runmode_val'
             2614  CALL_FUNCTION_1       1  '1 positional argument'
             2616  COMPARE_OP               ==
             2618  POP_JUMP_IF_FALSE  2630  'to 2630'

 L. 396      2622  LOAD_GLOBAL              print_info
             2624  LOAD_STR                 '\n----------------- End of Testcase Runmode Execution -----------------\n'
             2626  CALL_FUNCTION_1       1  '1 positional argument'
             2628  POP_TOP          
           2630_0  COME_FROM          2618  '2618'
           2630_1  COME_FROM          2584  '2584'
           2630_2  COME_FROM          2562  '2562'

 L. 398      2630  LOAD_GLOBAL              Utils
             2632  LOAD_ATTR                testcase_Utils
             2634  LOAD_ATTR                compute_status_using_impact

 L. 399      2636  LOAD_FAST                'tc_status_list'
             2638  LOAD_FAST                'tc_impact_list'
             2640  CALL_FUNCTION_2       2  '2 positional arguments'
             2642  STORE_FAST               'suite_status'

 L. 401      2644  LOAD_FAST                'tc_parallel'
             2646  POP_JUMP_IF_FALSE  2736  'to 2736'

 L. 402      2650  LOAD_FAST                'data_repository'
             2652  LOAD_STR                 'wt_tc_impact'
             2654  BINARY_SUBSCR    
             2656  STORE_FAST               'tc_impact'

 L. 403      2658  LOAD_FAST                'tc_impact'
             2660  LOAD_ATTR                upper
             2662  CALL_FUNCTION_0       0  '0 positional arguments'
             2664  LOAD_STR                 'IMPACT'
             2666  COMPARE_OP               ==
             2668  POP_JUMP_IF_FALSE  2678  'to 2678'

 L. 404      2672  LOAD_STR                 'Status of the executed test case impacts Testsuite result'
             2674  STORE_FAST               'msg'
             2676  JUMP_FORWARD       2696  'to 2696'
             2678  ELSE                     '2696'

 L. 405      2678  LOAD_FAST                'tc_impact'
             2680  LOAD_ATTR                upper
             2682  CALL_FUNCTION_0       0  '0 positional arguments'
             2684  LOAD_STR                 'NOIMPACT'
             2686  COMPARE_OP               ==
             2688  POP_JUMP_IF_FALSE  2696  'to 2696'

 L. 406      2692  LOAD_STR                 'Status of the executed test case does not impact Teststuie result'
             2694  STORE_FAST               'msg'
           2696_0  COME_FROM          2688  '2688'
           2696_1  COME_FROM          2676  '2676'

 L. 407      2696  LOAD_GLOBAL              print_debug
             2698  LOAD_FAST                'msg'
             2700  CALL_FUNCTION_1       1  '1 positional argument'
             2702  POP_TOP          

 L. 408      2704  LOAD_GLOBAL              Utils
             2706  LOAD_ATTR                file_Utils
             2708  LOAD_ATTR                getFileName
             2710  LOAD_FAST                'tc_path'
             2712  CALL_FUNCTION_1       1  '1 positional argument'
             2714  STORE_FAST               'tc_name'

 L. 411      2716  LOAD_FAST                'queue'
             2718  LOAD_ATTR                put
             2720  LOAD_FAST                'tc_status_list'
             2722  LOAD_FAST                'tc_name'
             2724  LOAD_FAST                'tc_impact_list'
             2726  LOAD_FAST                'tc_duration_list'

 L. 412      2728  LOAD_FAST                'tc_junit_list'
             2730  BUILD_TUPLE_5         5 
             2732  CALL_FUNCTION_1       1  '1 positional argument'
             2734  POP_TOP          
           2736_0  COME_FROM          2646  '2646'

 L. 413      2736  LOAD_FAST                'suite_status'
             2738  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_BLOCK' instruction at offset 2530


def main(testcase_list, suite_repository, data_repository, from_project, auto_defects, iter_ts_sys=None, tc_parallel=False, queue=False, ts_iter=False):
    """Executes testcases in a testsuite sequentially """
    try:
        testsuite_status = execute_sequential_testcases(testcase_list, suite_repository, data_repository, from_project, auto_defects, iter_ts_sys, tc_parallel, queue, ts_iter)
    except Exception:
        testsuite_status = False
        print_error('unexpected error {0}'.format(traceback.format_exc))

    return testsuite_status