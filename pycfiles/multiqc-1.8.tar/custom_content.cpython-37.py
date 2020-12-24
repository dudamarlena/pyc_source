# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/philewels/GitHub/MultiQC/multiqc/modules/custom_content/custom_content.py
# Compiled at: 2019-11-13 05:22:42
# Size of source mod 2**32: 22269 bytes
""" Core MultiQC module to parse output from custom script output """
from __future__ import print_function
import base64
from collections import defaultdict, OrderedDict
import logging, json, os, yaml
from multiqc import config
from multiqc.utils import report
from multiqc.modules.base_module import BaseMultiqcModule
from multiqc.plots import table, bargraph, linegraph, scatter, heatmap, beeswarm
log = logging.getLogger(__name__)

def yaml_ordered_load(stream):

    class OrderedLoader(yaml.SafeLoader):
        pass

    def construct_mapping(loader, node):
        loader.flatten_mapping(node)
        return OrderedDict(loader.construct_pairs(node))

    OrderedLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, construct_mapping)
    return yaml.load(stream, OrderedLoader)


def custom_module_classes--- This code section failed: ---

 L.  47         0  LOAD_GLOBAL              defaultdict
                2  LOAD_LAMBDA              '<code_object <lambda>>'
                4  LOAD_STR                 'custom_module_classes.<locals>.<lambda>'
                6  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
                8  CALL_FUNCTION_1       1  '1 positional argument'
               10  STORE_DEREF              'cust_mods'

 L.  50        12  LOAD_STR                 'custom_content'
               14  BUILD_LIST_1          1 
               16  STORE_FAST               'search_patterns'

 L.  53        18  LOAD_GLOBAL              getattr
               20  LOAD_GLOBAL              config
               22  LOAD_STR                 'custom_data'
               24  BUILD_MAP_0           0 
               26  CALL_FUNCTION_3       3  '3 positional arguments'
               28  STORE_FAST               'config_data'

 L.  54        30  SETUP_LOOP          272  'to 272'
               32  LOAD_FAST                'config_data'
               34  LOAD_METHOD              items
               36  CALL_METHOD_0         0  '0 positional arguments'
               38  GET_ITER         
               40  FOR_ITER            270  'to 270'
               42  UNPACK_SEQUENCE_2     2 
               44  STORE_FAST               'k'
               46  STORE_FAST               'f'

 L.  57        48  LOAD_GLOBAL              type
               50  LOAD_FAST                'f'
               52  CALL_FUNCTION_1       1  '1 positional argument'
               54  LOAD_GLOBAL              dict
               56  COMPARE_OP               !=
               58  POP_JUMP_IF_FALSE    78  'to 78'

 L.  58        60  LOAD_GLOBAL              log
               62  LOAD_METHOD              debug
               64  LOAD_STR                 'config.custom_data row was not a dictionary: {}'
               66  LOAD_METHOD              format
               68  LOAD_FAST                'k'
               70  CALL_METHOD_1         1  '1 positional argument'
               72  CALL_METHOD_1         1  '1 positional argument'
               74  POP_TOP          

 L.  59        76  CONTINUE             40  'to 40'
             78_0  COME_FROM            58  '58'

 L.  60        78  LOAD_FAST                'f'
               80  LOAD_METHOD              get
               82  LOAD_STR                 'id'
               84  LOAD_FAST                'k'
               86  CALL_METHOD_2         2  '2 positional arguments'
               88  STORE_FAST               'c_id'

 L.  63        90  LOAD_STR                 'data'
               92  LOAD_FAST                'f'
               94  COMPARE_OP               in
               96  POP_JUMP_IF_FALSE   186  'to 186'

 L.  64        98  LOAD_DEREF               'cust_mods'
              100  LOAD_FAST                'c_id'
              102  BINARY_SUBSCR    
              104  LOAD_STR                 'data'
              106  BINARY_SUBSCR    
              108  LOAD_METHOD              update
              110  LOAD_FAST                'f'
              112  LOAD_STR                 'data'
              114  BINARY_SUBSCR    
              116  CALL_METHOD_1         1  '1 positional argument'
              118  POP_TOP          

 L.  65       120  LOAD_DEREF               'cust_mods'
              122  LOAD_FAST                'c_id'
              124  BINARY_SUBSCR    
              126  LOAD_STR                 'config'
              128  BINARY_SUBSCR    
              130  LOAD_METHOD              update
              132  LOAD_DICTCOMP            '<code_object <dictcomp>>'
              134  LOAD_STR                 'custom_module_classes.<locals>.<dictcomp>'
              136  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              138  LOAD_FAST                'f'
              140  LOAD_METHOD              items
              142  CALL_METHOD_0         0  '0 positional arguments'
              144  GET_ITER         
              146  CALL_FUNCTION_1       1  '1 positional argument'
              148  CALL_METHOD_1         1  '1 positional argument'
              150  POP_TOP          

 L.  66       152  LOAD_DEREF               'cust_mods'
              154  LOAD_FAST                'c_id'
              156  BINARY_SUBSCR    
              158  LOAD_STR                 'config'
              160  BINARY_SUBSCR    
              162  LOAD_METHOD              get
              164  LOAD_STR                 'id'
              166  LOAD_FAST                'c_id'
              168  CALL_METHOD_2         2  '2 positional arguments'
              170  LOAD_DEREF               'cust_mods'
              172  LOAD_FAST                'c_id'
              174  BINARY_SUBSCR    
              176  LOAD_STR                 'config'
              178  BINARY_SUBSCR    
              180  LOAD_STR                 'id'
              182  STORE_SUBSCR     

 L.  67       184  CONTINUE             40  'to 40'
            186_0  COME_FROM            96  '96'

 L.  70       186  LOAD_FAST                'c_id'
              188  LOAD_GLOBAL              report
              190  LOAD_ATTR                files
              192  COMPARE_OP               in
              194  POP_JUMP_IF_FALSE   252  'to 252'

 L.  71       196  LOAD_FAST                'f'
              198  LOAD_DEREF               'cust_mods'
              200  LOAD_FAST                'c_id'
              202  BINARY_SUBSCR    
              204  LOAD_STR                 'config'
              206  STORE_SUBSCR     

 L.  72       208  LOAD_DEREF               'cust_mods'
              210  LOAD_FAST                'c_id'
              212  BINARY_SUBSCR    
              214  LOAD_STR                 'config'
              216  BINARY_SUBSCR    
              218  LOAD_METHOD              get
              220  LOAD_STR                 'id'
              222  LOAD_FAST                'c_id'
              224  CALL_METHOD_2         2  '2 positional arguments'
              226  LOAD_DEREF               'cust_mods'
              228  LOAD_FAST                'c_id'
              230  BINARY_SUBSCR    
              232  LOAD_STR                 'config'
              234  BINARY_SUBSCR    
              236  LOAD_STR                 'id'
              238  STORE_SUBSCR     

 L.  73       240  LOAD_FAST                'search_patterns'
              242  LOAD_METHOD              append
              244  LOAD_FAST                'c_id'
              246  CALL_METHOD_1         1  '1 positional argument'
              248  POP_TOP          

 L.  74       250  CONTINUE             40  'to 40'
            252_0  COME_FROM           194  '194'

 L.  77       252  LOAD_GLOBAL              log
              254  LOAD_METHOD              warn
              256  LOAD_STR                 "Found section '{}' in config for under custom_data, but no data or search patterns."
              258  LOAD_METHOD              format
              260  LOAD_FAST                'c_id'
              262  CALL_METHOD_1         1  '1 positional argument'
              264  CALL_METHOD_1         1  '1 positional argument'
              266  POP_TOP          
              268  JUMP_BACK            40  'to 40'
              270  POP_BLOCK        
            272_0  COME_FROM_LOOP       30  '30'

 L.  80       272  LOAD_GLOBAL              BaseMultiqcModule
              274  CALL_FUNCTION_0       0  '0 positional arguments'
              276  STORE_FAST               'bm'

 L.  81   278_280  SETUP_LOOP         1472  'to 1472'
              282  LOAD_FAST                'search_patterns'
              284  GET_ITER         
            286_0  COME_FROM          1446  '1446'
            286_1  COME_FROM          1436  '1436'
          286_288  FOR_ITER           1470  'to 1470'
              290  STORE_FAST               'k'

 L.  82       292  LOAD_CONST               0
              294  STORE_FAST               'num_sp_found_files'

 L.  83   296_298  SETUP_LOOP         1430  'to 1430'
              300  LOAD_FAST                'bm'
              302  LOAD_METHOD              find_log_files
              304  LOAD_FAST                'k'
              306  CALL_METHOD_1         1  '1 positional argument'
              308  GET_ITER         
          310_312  FOR_ITER           1428  'to 1428'
              314  STORE_FAST               'f'

 L.  84       316  LOAD_FAST                'num_sp_found_files'
              318  LOAD_CONST               1
              320  INPLACE_ADD      
              322  STORE_FAST               'num_sp_found_files'

 L.  86   324_326  SETUP_EXCEPT       1358  'to 1358'

 L.  87       328  LOAD_GLOBAL              os
              330  LOAD_ATTR                path
              332  LOAD_METHOD              splitext
              334  LOAD_FAST                'f'
              336  LOAD_STR                 'fn'
              338  BINARY_SUBSCR    
              340  CALL_METHOD_1         1  '1 positional argument'
              342  LOAD_CONST               1
              344  BINARY_SUBSCR    
              346  STORE_FAST               'f_extension'

 L.  90       348  LOAD_CONST               None
              350  STORE_FAST               'parsed_data'

 L.  91       352  LOAD_FAST                'f_extension'
              354  LOAD_STR                 '.yaml'
              356  COMPARE_OP               ==
          358_360  POP_JUMP_IF_TRUE    372  'to 372'
              362  LOAD_FAST                'f_extension'
              364  LOAD_STR                 '.yml'
              366  COMPARE_OP               ==
          368_370  POP_JUMP_IF_FALSE   470  'to 470'
            372_0  COME_FROM           358  '358'

 L.  92       372  SETUP_EXCEPT        390  'to 390'

 L.  93       374  LOAD_GLOBAL              yaml_ordered_load
              376  LOAD_FAST                'f'
              378  LOAD_STR                 'f'
              380  BINARY_SUBSCR    
              382  CALL_FUNCTION_1       1  '1 positional argument'
              384  STORE_FAST               'parsed_data'
              386  POP_BLOCK        
              388  JUMP_FORWARD        468  'to 468'
            390_0  COME_FROM_EXCEPT    372  '372'

 L.  94       390  DUP_TOP          
              392  LOAD_GLOBAL              Exception
              394  COMPARE_OP               exception-match
          396_398  POP_JUMP_IF_FALSE   466  'to 466'
              400  POP_TOP          
              402  STORE_FAST               'e'
              404  POP_TOP          
              406  SETUP_FINALLY       454  'to 454'

 L.  95       408  LOAD_GLOBAL              log
              410  LOAD_METHOD              warning
              412  LOAD_STR                 "Error parsing YAML file '{}' (probably invalid YAML)"
              414  LOAD_METHOD              format
              416  LOAD_FAST                'f'
              418  LOAD_STR                 'fn'
              420  BINARY_SUBSCR    
              422  CALL_METHOD_1         1  '1 positional argument'
              424  CALL_METHOD_1         1  '1 positional argument'
              426  POP_TOP          

 L.  96       428  LOAD_GLOBAL              log
              430  LOAD_ATTR                debug
              432  LOAD_STR                 'YAML error: {}'
              434  LOAD_METHOD              format
              436  LOAD_FAST                'e'
              438  CALL_METHOD_1         1  '1 positional argument'
              440  LOAD_CONST               True
              442  LOAD_CONST               ('exc_info',)
              444  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              446  POP_TOP          

 L.  97       448  BREAK_LOOP       
              450  POP_BLOCK        
              452  LOAD_CONST               None
            454_0  COME_FROM_FINALLY   406  '406'
              454  LOAD_CONST               None
              456  STORE_FAST               'e'
              458  DELETE_FAST              'e'
              460  END_FINALLY      
              462  POP_EXCEPT       
              464  JUMP_FORWARD        468  'to 468'
            466_0  COME_FROM           396  '396'
              466  END_FINALLY      
            468_0  COME_FROM           464  '464'
            468_1  COME_FROM           388  '388'
              468  JUMP_FORWARD        722  'to 722'
            470_0  COME_FROM           368  '368'

 L.  98       470  LOAD_FAST                'f_extension'
              472  LOAD_STR                 '.json'
              474  COMPARE_OP               ==
          476_478  POP_JUMP_IF_FALSE   580  'to 580'

 L.  99       480  SETUP_EXCEPT        504  'to 504'

 L. 101       482  LOAD_GLOBAL              json
              484  LOAD_ATTR                loads
              486  LOAD_FAST                'f'
              488  LOAD_STR                 'f'
              490  BINARY_SUBSCR    
              492  LOAD_GLOBAL              OrderedDict
              494  LOAD_CONST               ('object_pairs_hook',)
              496  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              498  STORE_FAST               'parsed_data'
              500  POP_BLOCK        
              502  JUMP_FORWARD        578  'to 578'
            504_0  COME_FROM_EXCEPT    480  '480'

 L. 102       504  DUP_TOP          
              506  LOAD_GLOBAL              Exception
              508  COMPARE_OP               exception-match
          510_512  POP_JUMP_IF_FALSE   576  'to 576'
              514  POP_TOP          
              516  STORE_FAST               'e'
              518  POP_TOP          
              520  SETUP_FINALLY       564  'to 564'

 L. 103       522  LOAD_GLOBAL              log
              524  LOAD_METHOD              warning
              526  LOAD_STR                 "Error parsing JSON file '{}' (probably invalid JSON)"
              528  LOAD_METHOD              format
              530  LOAD_FAST                'f'
              532  LOAD_STR                 'fn'
              534  BINARY_SUBSCR    
              536  CALL_METHOD_1         1  '1 positional argument'
              538  CALL_METHOD_1         1  '1 positional argument'
              540  POP_TOP          

 L. 104       542  LOAD_GLOBAL              log
              544  LOAD_METHOD              warning
              546  LOAD_STR                 'JSON error: {}'
              548  LOAD_METHOD              format
              550  LOAD_FAST                'e'
              552  CALL_METHOD_1         1  '1 positional argument'
              554  CALL_METHOD_1         1  '1 positional argument'
              556  POP_TOP          

 L. 105       558  BREAK_LOOP       
              560  POP_BLOCK        
              562  LOAD_CONST               None
            564_0  COME_FROM_FINALLY   520  '520'
              564  LOAD_CONST               None
              566  STORE_FAST               'e'
              568  DELETE_FAST              'e'
              570  END_FINALLY      
              572  POP_EXCEPT       
              574  JUMP_FORWARD        578  'to 578'
            576_0  COME_FROM           510  '510'
              576  END_FINALLY      
            578_0  COME_FROM           574  '574'
            578_1  COME_FROM           502  '502'
              578  JUMP_FORWARD        722  'to 722'
            580_0  COME_FROM           476  '476'

 L. 106       580  LOAD_FAST                'f_extension'
              582  LOAD_STR                 '.png'
              584  COMPARE_OP               ==
          586_588  POP_JUMP_IF_TRUE    610  'to 610'
              590  LOAD_FAST                'f_extension'
              592  LOAD_STR                 '.jpeg'
              594  COMPARE_OP               ==
          596_598  POP_JUMP_IF_TRUE    610  'to 610'
              600  LOAD_FAST                'f_extension'
              602  LOAD_STR                 '.jpg'
              604  COMPARE_OP               ==
          606_608  POP_JUMP_IF_FALSE   722  'to 722'
            610_0  COME_FROM           596  '596'
            610_1  COME_FROM           586  '586'

 L. 107       610  LOAD_GLOBAL              base64
              612  LOAD_METHOD              b64encode
              614  LOAD_FAST                'f'
              616  LOAD_STR                 'f'
              618  BINARY_SUBSCR    
              620  LOAD_METHOD              read
              622  CALL_METHOD_0         0  '0 positional arguments'
              624  CALL_METHOD_1         1  '1 positional argument'
              626  LOAD_METHOD              decode
              628  LOAD_STR                 'utf-8'
              630  CALL_METHOD_1         1  '1 positional argument'
              632  STORE_FAST               'image_string'

 L. 108       634  LOAD_FAST                'f_extension'
              636  LOAD_STR                 '.png'
              638  COMPARE_OP               ==
          640_642  POP_JUMP_IF_FALSE   648  'to 648'
              644  LOAD_STR                 'png'
              646  JUMP_FORWARD        650  'to 650'
            648_0  COME_FROM           640  '640'
              648  LOAD_STR                 'jpg'
            650_0  COME_FROM           646  '646'
              650  STORE_FAST               'image_format'

 L. 109       652  LOAD_STR                 '<div class="mqc-custom-content-image"><img src="data:image/{};base64,{}" /></div>'
              654  LOAD_METHOD              format
              656  LOAD_FAST                'image_format'
              658  LOAD_FAST                'image_string'
              660  CALL_METHOD_2         2  '2 positional arguments'
              662  STORE_FAST               'img_html'

 L. 111       664  LOAD_FAST                'f'
              666  LOAD_STR                 's_name'
              668  BINARY_SUBSCR    

 L. 112       670  LOAD_STR                 'image'

 L. 113       672  LOAD_FAST                'f'
              674  LOAD_STR                 's_name'
              676  BINARY_SUBSCR    
              678  LOAD_METHOD              replace
              680  LOAD_STR                 '_'
              682  LOAD_STR                 ' '
              684  CALL_METHOD_2         2  '2 positional arguments'
              686  LOAD_METHOD              replace
              688  LOAD_STR                 '-'
              690  LOAD_STR                 ' '
              692  CALL_METHOD_2         2  '2 positional arguments'
              694  LOAD_METHOD              replace
              696  LOAD_STR                 '.'
              698  LOAD_STR                 ' '
              700  CALL_METHOD_2         2  '2 positional arguments'

 L. 114       702  LOAD_STR                 'Embedded image <code>{}</code>'
              704  LOAD_METHOD              format
              706  LOAD_FAST                'f'
              708  LOAD_STR                 'fn'
              710  BINARY_SUBSCR    
              712  CALL_METHOD_1         1  '1 positional argument'

 L. 115       714  LOAD_FAST                'img_html'
              716  LOAD_CONST               ('id', 'plot_type', 'section_name', 'description', 'data')
              718  BUILD_CONST_KEY_MAP_5     5 
              720  STORE_FAST               'parsed_data'
            722_0  COME_FROM           606  '606'
            722_1  COME_FROM           578  '578'
            722_2  COME_FROM           468  '468'

 L. 117       722  LOAD_FAST                'parsed_data'
              724  LOAD_CONST               None
              726  COMPARE_OP               is-not
          728_730  POP_JUMP_IF_FALSE   882  'to 882'

 L. 118       732  LOAD_FAST                'parsed_data'
              734  LOAD_METHOD              get
              736  LOAD_STR                 'id'
              738  LOAD_FAST                'k'
              740  CALL_METHOD_2         2  '2 positional arguments'
              742  STORE_FAST               'c_id'

 L. 119       744  LOAD_GLOBAL              len
              746  LOAD_FAST                'parsed_data'
              748  LOAD_METHOD              get
              750  LOAD_STR                 'data'
              752  BUILD_MAP_0           0 
              754  CALL_METHOD_2         2  '2 positional arguments'
              756  CALL_FUNCTION_1       1  '1 positional argument'
              758  LOAD_CONST               0
              760  COMPARE_OP               >
          762_764  POP_JUMP_IF_FALSE   858  'to 858'

 L. 120       766  LOAD_GLOBAL              type
              768  LOAD_FAST                'parsed_data'
              770  LOAD_STR                 'data'
              772  BINARY_SUBSCR    
              774  CALL_FUNCTION_1       1  '1 positional argument'
              776  LOAD_GLOBAL              str
              778  COMPARE_OP               ==
          780_782  POP_JUMP_IF_FALSE   802  'to 802'

 L. 121       784  LOAD_FAST                'parsed_data'
              786  LOAD_STR                 'data'
              788  BINARY_SUBSCR    
              790  LOAD_DEREF               'cust_mods'
              792  LOAD_FAST                'c_id'
              794  BINARY_SUBSCR    
              796  LOAD_STR                 'data'
              798  STORE_SUBSCR     
              800  JUMP_FORWARD        824  'to 824'
            802_0  COME_FROM           780  '780'

 L. 123       802  LOAD_DEREF               'cust_mods'
              804  LOAD_FAST                'c_id'
              806  BINARY_SUBSCR    
              808  LOAD_STR                 'data'
              810  BINARY_SUBSCR    
              812  LOAD_METHOD              update
              814  LOAD_FAST                'parsed_data'
              816  LOAD_STR                 'data'
              818  BINARY_SUBSCR    
              820  CALL_METHOD_1         1  '1 positional argument'
              822  POP_TOP          
            824_0  COME_FROM           800  '800'

 L. 124       824  LOAD_DEREF               'cust_mods'
              826  LOAD_FAST                'c_id'
              828  BINARY_SUBSCR    
              830  LOAD_STR                 'config'
              832  BINARY_SUBSCR    
              834  LOAD_METHOD              update
              836  LOAD_DICTCOMP            '<code_object <dictcomp>>'
              838  LOAD_STR                 'custom_module_classes.<locals>.<dictcomp>'
              840  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              842  LOAD_FAST                'parsed_data'
              844  LOAD_METHOD              items
              846  CALL_METHOD_0         0  '0 positional arguments'
              848  GET_ITER         
              850  CALL_FUNCTION_1       1  '1 positional argument'
              852  CALL_METHOD_1         1  '1 positional argument'
              854  POP_TOP          
              856  JUMP_FORWARD       1354  'to 1354'
            858_0  COME_FROM           762  '762'

 L. 126       858  LOAD_GLOBAL              log
              860  LOAD_METHOD              warning
              862  LOAD_STR                 'No data found in {}'
              864  LOAD_METHOD              format
              866  LOAD_FAST                'f'
              868  LOAD_STR                 'fn'
              870  BINARY_SUBSCR    
              872  CALL_METHOD_1         1  '1 positional argument'
              874  CALL_METHOD_1         1  '1 positional argument'
              876  POP_TOP          
          878_880  JUMP_FORWARD       1354  'to 1354'
            882_0  COME_FROM           728  '728'

 L. 131       882  LOAD_GLOBAL              _find_file_header
              884  LOAD_FAST                'f'
              886  CALL_FUNCTION_1       1  '1 positional argument'
              888  STORE_FAST               'm_config'

 L. 132       890  LOAD_CONST               None
              892  STORE_FAST               's_name'

 L. 133       894  LOAD_FAST                'm_config'
              896  LOAD_CONST               None
              898  COMPARE_OP               is-not
          900_902  POP_JUMP_IF_FALSE   966  'to 966'

 L. 134       904  LOAD_FAST                'm_config'
              906  LOAD_METHOD              get
              908  LOAD_STR                 'id'
              910  LOAD_FAST                'k'
              912  CALL_METHOD_2         2  '2 positional arguments'
              914  STORE_FAST               'c_id'

 L. 136       916  LOAD_DEREF               'cust_mods'
              918  LOAD_METHOD              get
              920  LOAD_FAST                'c_id'
              922  BUILD_MAP_0           0 
              924  CALL_METHOD_2         2  '2 positional arguments'
              926  LOAD_METHOD              get
              928  LOAD_STR                 'config'
              930  BUILD_MAP_0           0 
              932  CALL_METHOD_2         2  '2 positional arguments'
              934  STORE_FAST               'b_config'

 L. 137       936  LOAD_FAST                'b_config'
              938  LOAD_METHOD              update
              940  LOAD_FAST                'm_config'
              942  CALL_METHOD_1         1  '1 positional argument'
              944  POP_TOP          

 L. 139       946  LOAD_GLOBAL              dict
              948  LOAD_FAST                'b_config'
              950  CALL_FUNCTION_1       1  '1 positional argument'
              952  STORE_FAST               'm_config'

 L. 140       954  LOAD_FAST                'm_config'
              956  LOAD_METHOD              get
              958  LOAD_STR                 'sample_name'
              960  CALL_METHOD_1         1  '1 positional argument'
              962  STORE_FAST               's_name'
              964  JUMP_FORWARD        990  'to 990'
            966_0  COME_FROM           900  '900'

 L. 142       966  LOAD_FAST                'k'
              968  STORE_FAST               'c_id'

 L. 143       970  LOAD_DEREF               'cust_mods'
              972  LOAD_METHOD              get
              974  LOAD_FAST                'c_id'
              976  BUILD_MAP_0           0 
              978  CALL_METHOD_2         2  '2 positional arguments'
              980  LOAD_METHOD              get
              982  LOAD_STR                 'config'
              984  BUILD_MAP_0           0 
              986  CALL_METHOD_2         2  '2 positional arguments'
              988  STORE_FAST               'm_config'
            990_0  COME_FROM           964  '964'

 L. 146       990  LOAD_FAST                's_name'
              992  LOAD_CONST               None
              994  COMPARE_OP               is
          996_998  POP_JUMP_IF_FALSE  1020  'to 1020'

 L. 147      1000  LOAD_FAST                'bm'
             1002  LOAD_METHOD              clean_s_name
             1004  LOAD_FAST                'f'
             1006  LOAD_STR                 's_name'
             1008  BINARY_SUBSCR    
             1010  LOAD_FAST                'f'
             1012  LOAD_STR                 'root'
             1014  BINARY_SUBSCR    
             1016  CALL_METHOD_2         2  '2 positional arguments'
             1018  STORE_FAST               's_name'
           1020_0  COME_FROM           996  '996'

 L. 150      1020  LOAD_FAST                'k'
             1022  LOAD_STR                 'custom_content'
             1024  COMPARE_OP               ==
         1026_1028  POP_JUMP_IF_FALSE  1034  'to 1034'

 L. 151      1030  LOAD_FAST                's_name'
             1032  STORE_FAST               'c_id'
           1034_0  COME_FROM          1026  '1026'

 L. 154      1034  LOAD_STR                 'files'
             1036  LOAD_FAST                'm_config'
             1038  COMPARE_OP               not-in
         1040_1042  POP_JUMP_IF_FALSE  1054  'to 1054'

 L. 155      1044  LOAD_GLOBAL              dict
             1046  CALL_FUNCTION_0       0  '0 positional arguments'
             1048  LOAD_FAST                'm_config'
             1050  LOAD_STR                 'files'
             1052  STORE_SUBSCR     
           1054_0  COME_FROM          1040  '1040'

 L. 156      1054  LOAD_FAST                'm_config'
             1056  LOAD_STR                 'files'
             1058  BINARY_SUBSCR    
             1060  LOAD_METHOD              update
             1062  LOAD_FAST                's_name'
             1064  LOAD_FAST                'f'
             1066  LOAD_STR                 'fn'
             1068  BINARY_SUBSCR    
             1070  LOAD_FAST                'f'
             1072  LOAD_STR                 'root'
             1074  BINARY_SUBSCR    
             1076  LOAD_CONST               ('fn', 'root')
             1078  BUILD_CONST_KEY_MAP_2     2 
             1080  BUILD_MAP_1           1 
             1082  CALL_METHOD_1         1  '1 positional argument'
             1084  POP_TOP          

 L. 159      1086  LOAD_FAST                'm_config'
             1088  LOAD_METHOD              get
             1090  LOAD_STR                 'file_format'
             1092  CALL_METHOD_1         1  '1 positional argument'
             1094  LOAD_CONST               None
             1096  COMPARE_OP               is
         1098_1100  POP_JUMP_IF_FALSE  1114  'to 1114'

 L. 160      1102  LOAD_GLOBAL              _guess_file_format
             1104  LOAD_FAST                'f'
             1106  CALL_FUNCTION_1       1  '1 positional argument'
             1108  LOAD_FAST                'm_config'
             1110  LOAD_STR                 'file_format'
             1112  STORE_SUBSCR     
           1114_0  COME_FROM          1098  '1098'

 L. 162      1114  SETUP_EXCEPT       1300  'to 1300'

 L. 163      1116  LOAD_GLOBAL              _parse_txt
             1118  LOAD_FAST                'f'
             1120  LOAD_FAST                'm_config'
             1122  CALL_FUNCTION_2       2  '2 positional arguments'
             1124  UNPACK_SEQUENCE_2     2 
             1126  STORE_FAST               'parsed_data'
             1128  STORE_FAST               'conf'

 L. 164      1130  LOAD_FAST                'parsed_data'
             1132  LOAD_CONST               None
             1134  COMPARE_OP               is
         1136_1138  POP_JUMP_IF_TRUE   1154  'to 1154'
             1140  LOAD_GLOBAL              len
             1142  LOAD_FAST                'parsed_data'
             1144  CALL_FUNCTION_1       1  '1 positional argument'
             1146  LOAD_CONST               0
             1148  COMPARE_OP               ==
         1150_1152  POP_JUMP_IF_FALSE  1176  'to 1176'
           1154_0  COME_FROM          1136  '1136'

 L. 165      1154  LOAD_GLOBAL              log
             1156  LOAD_METHOD              warning
             1158  LOAD_STR                 'Not able to parse custom data in {}'
             1160  LOAD_METHOD              format
             1162  LOAD_FAST                'f'
             1164  LOAD_STR                 'fn'
             1166  BINARY_SUBSCR    
             1168  CALL_METHOD_1         1  '1 positional argument'
             1170  CALL_METHOD_1         1  '1 positional argument'
             1172  POP_TOP          
             1174  JUMP_FORWARD       1296  'to 1296'
           1176_0  COME_FROM          1150  '1150'

 L. 168      1176  LOAD_FAST                'conf'
             1178  LOAD_METHOD              get
             1180  LOAD_STR                 'id'
             1182  CALL_METHOD_1         1  '1 positional argument'
             1184  LOAD_CONST               None
             1186  COMPARE_OP               is-not
         1188_1190  POP_JUMP_IF_FALSE  1202  'to 1202'

 L. 169      1192  LOAD_FAST                'conf'
             1194  LOAD_METHOD              get
             1196  LOAD_STR                 'id'
             1198  CALL_METHOD_1         1  '1 positional argument'
             1200  STORE_FAST               'c_id'
           1202_0  COME_FROM          1188  '1188'

 L. 171      1202  LOAD_GLOBAL              type
             1204  LOAD_FAST                'parsed_data'
             1206  CALL_FUNCTION_1       1  '1 positional argument'
             1208  LOAD_GLOBAL              list
             1210  COMPARE_OP               ==
         1212_1214  POP_JUMP_IF_FALSE  1230  'to 1230'

 L. 172      1216  LOAD_FAST                'parsed_data'
             1218  LOAD_DEREF               'cust_mods'
             1220  LOAD_FAST                'c_id'
             1222  BINARY_SUBSCR    
             1224  LOAD_STR                 'data'
             1226  STORE_SUBSCR     
             1228  JUMP_FORWARD       1278  'to 1278'
           1230_0  COME_FROM          1212  '1212'

 L. 173      1230  LOAD_FAST                'conf'
             1232  LOAD_METHOD              get
             1234  LOAD_STR                 'plot_type'
             1236  CALL_METHOD_1         1  '1 positional argument'
             1238  LOAD_STR                 'html'
             1240  COMPARE_OP               ==
         1242_1244  POP_JUMP_IF_FALSE  1260  'to 1260'

 L. 174      1246  LOAD_FAST                'parsed_data'
             1248  LOAD_DEREF               'cust_mods'
             1250  LOAD_FAST                'c_id'
             1252  BINARY_SUBSCR    
             1254  LOAD_STR                 'data'
             1256  STORE_SUBSCR     
             1258  JUMP_FORWARD       1278  'to 1278'
           1260_0  COME_FROM          1242  '1242'

 L. 176      1260  LOAD_DEREF               'cust_mods'
             1262  LOAD_FAST                'c_id'
             1264  BINARY_SUBSCR    
             1266  LOAD_STR                 'data'
             1268  BINARY_SUBSCR    
             1270  LOAD_METHOD              update
             1272  LOAD_FAST                'parsed_data'
             1274  CALL_METHOD_1         1  '1 positional argument'
             1276  POP_TOP          
           1278_0  COME_FROM          1258  '1258'
           1278_1  COME_FROM          1228  '1228'

 L. 177      1278  LOAD_DEREF               'cust_mods'
             1280  LOAD_FAST                'c_id'
             1282  BINARY_SUBSCR    
             1284  LOAD_STR                 'config'
             1286  BINARY_SUBSCR    
             1288  LOAD_METHOD              update
             1290  LOAD_FAST                'conf'
             1292  CALL_METHOD_1         1  '1 positional argument'
             1294  POP_TOP          
           1296_0  COME_FROM          1174  '1174'
             1296  POP_BLOCK        
             1298  JUMP_FORWARD       1354  'to 1354'
           1300_0  COME_FROM_EXCEPT   1114  '1114'

 L. 178      1300  DUP_TOP          
             1302  LOAD_GLOBAL              IndexError
             1304  LOAD_GLOBAL              AttributeError
             1306  LOAD_GLOBAL              TypeError
             1308  BUILD_TUPLE_3         3 
             1310  COMPARE_OP               exception-match
         1312_1314  POP_JUMP_IF_FALSE  1352  'to 1352'
             1316  POP_TOP          
             1318  POP_TOP          
             1320  POP_TOP          

 L. 179      1322  LOAD_GLOBAL              log
             1324  LOAD_ATTR                error
             1326  LOAD_STR                 'Unexpected parsing error for {}'
             1328  LOAD_METHOD              format
           1330_0  COME_FROM           856  '856'
             1330  LOAD_FAST                'f'
             1332  LOAD_STR                 'fn'
             1334  BINARY_SUBSCR    
             1336  CALL_METHOD_1         1  '1 positional argument'
             1338  LOAD_CONST               True
             1340  LOAD_CONST               ('exc_info',)
             1342  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1344  POP_TOP          

 L. 180      1346  RAISE_VARARGS_0       0  'reraise'
             1348  POP_EXCEPT       
             1350  JUMP_FORWARD       1354  'to 1354'
           1352_0  COME_FROM          1312  '1312'
             1352  END_FINALLY      
           1354_0  COME_FROM          1350  '1350'
           1354_1  COME_FROM          1298  '1298'
           1354_2  COME_FROM           878  '878'
             1354  POP_BLOCK        
             1356  JUMP_BACK           310  'to 310'
           1358_0  COME_FROM_EXCEPT    324  '324'

 L. 181      1358  DUP_TOP          
             1360  LOAD_GLOBAL              Exception
             1362  COMPARE_OP               exception-match
         1364_1366  POP_JUMP_IF_FALSE  1422  'to 1422'
             1368  POP_TOP          
             1370  STORE_FAST               'e'
             1372  POP_TOP          
             1374  SETUP_FINALLY      1410  'to 1410'

 L. 182      1376  LOAD_GLOBAL              log
             1378  LOAD_METHOD              error
             1380  LOAD_STR                 "Uncaught exception raised for file '{}'"
             1382  LOAD_METHOD              format
             1384  LOAD_FAST                'f'
             1386  LOAD_STR                 'fn'
             1388  BINARY_SUBSCR    
             1390  CALL_METHOD_1         1  '1 positional argument'
             1392  CALL_METHOD_1         1  '1 positional argument'
             1394  POP_TOP          

 L. 183      1396  LOAD_GLOBAL              log
             1398  LOAD_METHOD              exception
             1400  LOAD_FAST                'e'
             1402  CALL_METHOD_1         1  '1 positional argument'
             1404  POP_TOP          
             1406  POP_BLOCK        
             1408  LOAD_CONST               None
           1410_0  COME_FROM_FINALLY  1374  '1374'
             1410  LOAD_CONST               None
             1412  STORE_FAST               'e'
             1414  DELETE_FAST              'e'
             1416  END_FINALLY      
             1418  POP_EXCEPT       
             1420  JUMP_BACK           310  'to 310'
           1422_0  COME_FROM          1364  '1364'
             1422  END_FINALLY      
         1424_1426  JUMP_BACK           310  'to 310'
             1428  POP_BLOCK        
           1430_0  COME_FROM_LOOP      296  '296'

 L. 186      1430  LOAD_FAST                'num_sp_found_files'
             1432  LOAD_CONST               0
             1434  COMPARE_OP               ==
         1436_1438  POP_JUMP_IF_FALSE   286  'to 286'
             1440  LOAD_FAST                'k'
             1442  LOAD_STR                 'custom_content'
             1444  COMPARE_OP               !=
         1446_1448  POP_JUMP_IF_FALSE   286  'to 286'

 L. 187      1450  LOAD_GLOBAL              log
             1452  LOAD_METHOD              debug
             1454  LOAD_STR                 'No samples found: custom content ({})'
             1456  LOAD_METHOD              format
             1458  LOAD_FAST                'k'
             1460  CALL_METHOD_1         1  '1 positional argument'
             1462  CALL_METHOD_1         1  '1 positional argument'
             1464  POP_TOP          
         1466_1468  JUMP_BACK           286  'to 286'
             1470  POP_BLOCK        
           1472_0  COME_FROM_LOOP      278  '278'

 L. 190      1472  SETUP_LOOP         1514  'to 1514'
             1474  LOAD_DEREF               'cust_mods'
             1476  GET_ITER         
             1478  FOR_ITER           1512  'to 1512'
             1480  STORE_FAST               'k'

 L. 191      1482  LOAD_FAST                'bm'
             1484  LOAD_METHOD              ignore_samples
             1486  LOAD_DEREF               'cust_mods'
             1488  LOAD_FAST                'k'
             1490  BINARY_SUBSCR    
             1492  LOAD_STR                 'data'
             1494  BINARY_SUBSCR    
             1496  CALL_METHOD_1         1  '1 positional argument'
             1498  LOAD_DEREF               'cust_mods'
             1500  LOAD_FAST                'k'
             1502  BINARY_SUBSCR    
             1504  LOAD_STR                 'data'
             1506  STORE_SUBSCR     
         1508_1510  JUMP_BACK          1478  'to 1478'
             1512  POP_BLOCK        
           1514_0  COME_FROM_LOOP     1472  '1472'

 L. 194      1514  LOAD_CLOSURE             'cust_mods'
             1516  BUILD_TUPLE_1         1 
             1518  LOAD_LISTCOMP            '<code_object <listcomp>>'
             1520  LOAD_STR                 'custom_module_classes.<locals>.<listcomp>'
             1522  MAKE_FUNCTION_8          'closure'
             1524  LOAD_DEREF               'cust_mods'
             1526  GET_ITER         
             1528  CALL_FUNCTION_1       1  '1 positional argument'
             1530  STORE_FAST               'remove_cids'

 L. 195      1532  SETUP_LOOP         1554  'to 1554'
             1534  LOAD_FAST                'remove_cids'
             1536  GET_ITER         
             1538  FOR_ITER           1552  'to 1552'
             1540  STORE_FAST               'k'

 L. 196      1542  LOAD_DEREF               'cust_mods'
             1544  LOAD_FAST                'k'
             1546  DELETE_SUBSCR    
         1548_1550  JUMP_BACK          1538  'to 1538'
             1552  POP_BLOCK        
           1554_0  COME_FROM_LOOP     1532  '1532'

 L. 198      1554  LOAD_GLOBAL              len
             1556  LOAD_DEREF               'cust_mods'
             1558  CALL_FUNCTION_1       1  '1 positional argument'
             1560  LOAD_CONST               0
             1562  COMPARE_OP               ==
         1564_1566  POP_JUMP_IF_FALSE  1572  'to 1572'

 L. 199      1568  LOAD_GLOBAL              UserWarning
             1570  RAISE_VARARGS_1       1  'exception instance'
           1572_0  COME_FROM          1564  '1564'

 L. 202      1572  LOAD_GLOBAL              list
             1574  CALL_FUNCTION_0       0  '0 positional arguments'
             1576  STORE_DEREF              'parsed_modules'

 L. 203  1578_1580  SETUP_LOOP         2014  'to 2014'
             1582  LOAD_DEREF               'cust_mods'
             1584  LOAD_METHOD              items
             1586  CALL_METHOD_0         0  '0 positional arguments'
             1588  GET_ITER         
         1590_1592  FOR_ITER           2012  'to 2012'
             1594  UNPACK_SEQUENCE_2     2 
             1596  STORE_FAST               'module_id'
             1598  STORE_FAST               'mod'

 L. 206      1600  LOAD_FAST                'mod'
             1602  LOAD_STR                 'config'
             1604  BINARY_SUBSCR    
             1606  LOAD_METHOD              get
             1608  LOAD_STR                 'plot_type'
             1610  CALL_METHOD_1         1  '1 positional argument'
             1612  LOAD_STR                 'generalstats'
             1614  COMPARE_OP               ==
         1616_1618  POP_JUMP_IF_FALSE  1880  'to 1880'

 L. 207      1620  LOAD_FAST                'mod'
             1622  LOAD_STR                 'config'
             1624  BINARY_SUBSCR    
             1626  LOAD_METHOD              get
             1628  LOAD_STR                 'pconfig'
             1630  CALL_METHOD_1         1  '1 positional argument'
             1632  STORE_FAST               'gsheaders'

 L. 208      1634  LOAD_FAST                'gsheaders'
             1636  LOAD_CONST               None
             1638  COMPARE_OP               is
         1640_1642  POP_JUMP_IF_FALSE  1736  'to 1736'

 L. 209      1644  LOAD_GLOBAL              set
             1646  CALL_FUNCTION_0       0  '0 positional arguments'
             1648  STORE_FAST               'headers'

 L. 210      1650  SETUP_LOOP         1688  'to 1688'
             1652  LOAD_FAST                'mod'
             1654  LOAD_STR                 'data'
             1656  BINARY_SUBSCR    
             1658  LOAD_METHOD              values
             1660  CALL_METHOD_0         0  '0 positional arguments'
             1662  GET_ITER         
             1664  FOR_ITER           1686  'to 1686'
             1666  STORE_FAST               'd'

 L. 211      1668  LOAD_FAST                'headers'
             1670  LOAD_METHOD              update
             1672  LOAD_FAST                'd'
             1674  LOAD_METHOD              keys
             1676  CALL_METHOD_0         0  '0 positional arguments'
             1678  CALL_METHOD_1         1  '1 positional argument'
             1680  POP_TOP          
         1682_1684  JUMP_BACK          1664  'to 1664'
             1686  POP_BLOCK        
           1688_0  COME_FROM_LOOP     1650  '1650'

 L. 212      1688  LOAD_GLOBAL              list
             1690  LOAD_FAST                'headers'
             1692  CALL_FUNCTION_1       1  '1 positional argument'
             1694  STORE_FAST               'headers'

 L. 213      1696  LOAD_FAST                'headers'
             1698  LOAD_METHOD              sort
             1700  CALL_METHOD_0         0  '0 positional arguments'
             1702  POP_TOP          

 L. 214      1704  LOAD_GLOBAL              OrderedDict
             1706  CALL_FUNCTION_0       0  '0 positional arguments'
             1708  STORE_FAST               'gsheaders'

 L. 215      1710  SETUP_LOOP         1736  'to 1736'
             1712  LOAD_FAST                'headers'
             1714  GET_ITER         
             1716  FOR_ITER           1734  'to 1734'
             1718  STORE_FAST               'h'

 L. 216      1720  LOAD_GLOBAL              dict
             1722  CALL_FUNCTION_0       0  '0 positional arguments'
             1724  LOAD_FAST                'gsheaders'
             1726  LOAD_FAST                'h'
             1728  STORE_SUBSCR     
         1730_1732  JUMP_BACK          1716  'to 1716'
             1734  POP_BLOCK        
           1736_0  COME_FROM_LOOP     1710  '1710'
           1736_1  COME_FROM          1640  '1640'

 L. 219      1736  LOAD_GLOBAL              type
             1738  LOAD_FAST                'gsheaders'
             1740  CALL_FUNCTION_1       1  '1 positional argument'
             1742  LOAD_GLOBAL              list
             1744  COMPARE_OP               ==
         1746_1748  POP_JUMP_IF_FALSE  1808  'to 1808'

 L. 220      1750  LOAD_GLOBAL              OrderedDict
             1752  CALL_FUNCTION_0       0  '0 positional arguments'
             1754  STORE_FAST               'gsheaders_dict'

 L. 221      1756  SETUP_LOOP         1804  'to 1804'
             1758  LOAD_FAST                'gsheaders'
             1760  GET_ITER         
             1762  FOR_ITER           1802  'to 1802'
             1764  STORE_FAST               'gsheader'

 L. 222      1766  SETUP_LOOP         1798  'to 1798'
             1768  LOAD_FAST                'gsheader'
             1770  LOAD_METHOD              items
             1772  CALL_METHOD_0         0  '0 positional arguments'
             1774  GET_ITER         
             1776  FOR_ITER           1796  'to 1796'
             1778  UNPACK_SEQUENCE_2     2 
             1780  STORE_FAST               'col_id'
             1782  STORE_FAST               'col_data'

 L. 223      1784  LOAD_FAST                'col_data'
             1786  LOAD_FAST                'gsheaders_dict'
             1788  LOAD_FAST                'col_id'
             1790  STORE_SUBSCR     
         1792_1794  JUMP_BACK          1776  'to 1776'
             1796  POP_BLOCK        
           1798_0  COME_FROM_LOOP     1766  '1766'
         1798_1800  JUMP_BACK          1762  'to 1762'
             1802  POP_BLOCK        
           1804_0  COME_FROM_LOOP     1756  '1756'

 L. 224      1804  LOAD_FAST                'gsheaders_dict'
             1806  STORE_FAST               'gsheaders'
           1808_0  COME_FROM          1746  '1746'

 L. 227      1808  SETUP_LOOP         1862  'to 1862'
             1810  LOAD_FAST                'gsheaders'
             1812  GET_ITER         
           1814_0  COME_FROM          1828  '1828'
             1814  FOR_ITER           1860  'to 1860'
             1816  STORE_FAST               'm_id'

 L. 228      1818  LOAD_STR                 'namespace'
             1820  LOAD_FAST                'gsheaders'
             1822  LOAD_FAST                'm_id'
             1824  BINARY_SUBSCR    
             1826  COMPARE_OP               not-in
         1828_1830  POP_JUMP_IF_FALSE  1814  'to 1814'

 L. 229      1832  LOAD_FAST                'mod'
             1834  LOAD_STR                 'config'
             1836  BINARY_SUBSCR    
             1838  LOAD_METHOD              get
             1840  LOAD_STR                 'namespace'
             1842  LOAD_FAST                'module_id'
             1844  CALL_METHOD_2         2  '2 positional arguments'
             1846  LOAD_FAST                'gsheaders'
             1848  LOAD_FAST                'm_id'
             1850  BINARY_SUBSCR    
             1852  LOAD_STR                 'namespace'
             1854  STORE_SUBSCR     
         1856_1858  JUMP_BACK          1814  'to 1814'
             1860  POP_BLOCK        
           1862_0  COME_FROM_LOOP     1808  '1808'

 L. 231      1862  LOAD_FAST                'bm'
             1864  LOAD_METHOD              general_stats_addcols
             1866  LOAD_FAST                'mod'
             1868  LOAD_STR                 'data'
             1870  BINARY_SUBSCR    
             1872  LOAD_FAST                'gsheaders'
             1874  CALL_METHOD_2         2  '2 positional arguments'
             1876  POP_TOP          
             1878  JUMP_BACK          1590  'to 1590'
           1880_0  COME_FROM          1616  '1616'

 L. 235      1880  LOAD_DEREF               'parsed_modules'
             1882  LOAD_METHOD              append
             1884  LOAD_GLOBAL              MultiqcModule
             1886  LOAD_FAST                'module_id'
             1888  LOAD_FAST                'mod'
             1890  CALL_FUNCTION_2       2  '2 positional arguments'
             1892  CALL_METHOD_1         1  '1 positional argument'
             1894  POP_TOP          

 L. 236      1896  LOAD_FAST                'mod'
             1898  LOAD_STR                 'config'
             1900  BINARY_SUBSCR    
             1902  LOAD_METHOD              get
             1904  LOAD_STR                 'plot_type'
             1906  CALL_METHOD_1         1  '1 positional argument'
             1908  LOAD_STR                 'html'
             1910  COMPARE_OP               ==
         1912_1914  POP_JUMP_IF_FALSE  1932  'to 1932'

 L. 237      1916  LOAD_GLOBAL              log
             1918  LOAD_METHOD              info
             1920  LOAD_STR                 '{}: Found 1 sample (html)'
             1922  LOAD_METHOD              format
             1924  LOAD_FAST                'module_id'
             1926  CALL_METHOD_1         1  '1 positional argument'
             1928  CALL_METHOD_1         1  '1 positional argument'
             1930  POP_TOP          
           1932_0  COME_FROM          1912  '1912'

 L. 238      1932  LOAD_FAST                'mod'
             1934  LOAD_STR                 'config'
             1936  BINARY_SUBSCR    
             1938  LOAD_METHOD              get
             1940  LOAD_STR                 'plot_type'
             1942  CALL_METHOD_1         1  '1 positional argument'
             1944  LOAD_STR                 'image'
             1946  COMPARE_OP               ==
         1948_1950  POP_JUMP_IF_FALSE  1970  'to 1970'

 L. 239      1952  LOAD_GLOBAL              log
             1954  LOAD_METHOD              info
             1956  LOAD_STR                 '{}: Found 1 sample (image)'
             1958  LOAD_METHOD              format
             1960  LOAD_FAST                'module_id'
             1962  CALL_METHOD_1         1  '1 positional argument'
             1964  CALL_METHOD_1         1  '1 positional argument'
             1966  POP_TOP          
             1968  JUMP_BACK          1590  'to 1590'
           1970_0  COME_FROM          1948  '1948'

 L. 241      1970  LOAD_GLOBAL              log
             1972  LOAD_METHOD              info
             1974  LOAD_STR                 '{}: Found {} samples ({})'
             1976  LOAD_METHOD              format
             1978  LOAD_FAST                'module_id'
             1980  LOAD_GLOBAL              len
             1982  LOAD_FAST                'mod'
             1984  LOAD_STR                 'data'
             1986  BINARY_SUBSCR    
             1988  CALL_FUNCTION_1       1  '1 positional argument'
             1990  LOAD_FAST                'mod'
             1992  LOAD_STR                 'config'
             1994  BINARY_SUBSCR    
             1996  LOAD_METHOD              get
             1998  LOAD_STR                 'plot_type'
             2000  CALL_METHOD_1         1  '1 positional argument'
             2002  CALL_METHOD_3         3  '3 positional arguments'
             2004  CALL_METHOD_1         1  '1 positional argument'
             2006  POP_TOP          
         2008_2010  JUMP_BACK          1590  'to 1590'
             2012  POP_BLOCK        
           2014_0  COME_FROM_LOOP     1578  '1578'

 L. 244      2014  LOAD_GLOBAL              getattr
             2016  LOAD_GLOBAL              config
             2018  LOAD_STR                 'custom_content'
             2020  BUILD_MAP_0           0 
             2022  CALL_FUNCTION_3       3  '3 positional arguments'
             2024  LOAD_METHOD              get
             2026  LOAD_STR                 'order'
             2028  BUILD_LIST_0          0 
             2030  CALL_METHOD_2         2  '2 positional arguments'
             2032  STORE_DEREF              'mod_order'

 L. 245      2034  LOAD_CLOSURE             'mod_order'
             2036  BUILD_TUPLE_1         1 
             2038  LOAD_LISTCOMP            '<code_object <listcomp>>'
             2040  LOAD_STR                 'custom_module_classes.<locals>.<listcomp>'
             2042  MAKE_FUNCTION_8          'closure'
             2044  LOAD_DEREF               'parsed_modules'
             2046  GET_ITER         
             2048  CALL_FUNCTION_1       1  '1 positional argument'
             2050  STORE_FAST               'sorted_modules'

 L. 246      2052  LOAD_FAST                'sorted_modules'
             2054  LOAD_METHOD              extend
             2056  LOAD_CLOSURE             'parsed_modules'
             2058  BUILD_TUPLE_1         1 
             2060  LOAD_LISTCOMP            '<code_object <listcomp>>'
             2062  LOAD_STR                 'custom_module_classes.<locals>.<listcomp>'
             2064  MAKE_FUNCTION_8          'closure'
             2066  LOAD_DEREF               'mod_order'
             2068  GET_ITER         
             2070  CALL_FUNCTION_1       1  '1 positional argument'
             2072  CALL_METHOD_1         1  '1 positional argument'
             2074  POP_TOP          

 L. 249      2076  LOAD_GLOBAL              len
             2078  LOAD_FAST                'sorted_modules'
             2080  CALL_FUNCTION_1       1  '1 positional argument'
             2082  LOAD_CONST               0
             2084  COMPARE_OP               ==
         2086_2088  POP_JUMP_IF_FALSE  2094  'to 2094'

 L. 250      2090  LOAD_GLOBAL              UserWarning
             2092  RAISE_VARARGS_1       1  'exception instance'
           2094_0  COME_FROM          2086  '2086'

 L. 252      2094  LOAD_FAST                'sorted_modules'
             2096  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM' instruction at offset 1330_0


class MultiqcModule(BaseMultiqcModule):
    __doc__ = ' Module class, used for each custom content type '

    def __init__(self, c_id, mod):
        modname = mod['config'].get('section_name', c_id.replace('_', ' ').title)
        if modname == '' or modname is None:
            modname = 'Custom Content'
        superMultiqcModuleself.__init__(name=modname,
          anchor=(mod['config'].get('section_anchor', c_id)),
          href=(mod['config'].get('section_href')),
          info=(mod['config'].get('description')))
        pconfig = mod['config'].get('pconfig', {})
        if pconfig.get('title') is None:
            pconfig['title'] = modname
        elif mod['config'].get('plot_type') == 'table':
            pconfig['sortRows'] = pconfig.get('sortRows', False)
            headers = mod['config'].get('headers')
            self.add_section(plot=(table.plotmod['data']headerspconfig))
            self.write_data_file(mod['data'], 'multiqc_{}'.format(modname.lower.replace(' ', '_')))
        else:
            if mod['config'].get('plot_type') == 'bargraph':
                self.add_section(plot=(bargraph.plotmod['data']mod['config'].get('categories')pconfig))
            else:
                if mod['config'].get('plot_type') == 'linegraph':
                    self.add_section(plot=(linegraph.plot(mod['data'], pconfig)))
                else:
                    if mod['config'].get('plot_type') == 'scatter':
                        self.add_section(plot=(scatter.plot(mod['data'], pconfig)))
                    else:
                        if mod['config'].get('plot_type') == 'heatmap':
                            self.add_section(plot=(heatmap.plot(mod['data'], mod['config'].get('xcats'), mod['config'].get('ycats'), pconfig)))
                        else:
                            if mod['config'].get('plot_type') == 'beeswarm':
                                self.add_section(plot=(beeswarm.plot(mod['data'], pconfig)))
                            else:
                                if mod['config'].get('plot_type') == 'html':
                                    self.add_section(content=(mod['data']))
                                else:
                                    if mod['config'].get('plot_type') == 'image':
                                        self.add_section(content=(mod['data']))
                                    else:
                                        if mod['config'].get('plot_type') == None:
                                            log.warning("Plot type not found for content ID '{}'".format(c_id))
                                        else:
                                            log.warning("Error - custom content plot type '{}' not recognised for content ID {}".format(mod['config'].get('plot_type'), c_id))


def _find_file_header(f):
    hlines = []
    for l in f['f'].splitlines:
        if l.startswith('#'):
            hlines.append(l[1:])

    if len(hlines) == 0:
        return
    hconfig = None
    try:
        hconfig = yaml.safe_load('\n'.join(hlines))
        assert isinstancehconfigdict
    except yaml.YAMLError as e:
        try:
            log.warn('Could not parse comment file header for MultiQC custom content: {}'.format(f['fn']))
            log.debug(e)
        finally:
            e = None
            del e

    except AssertionError:
        log.debug('Custom Content comment file header looked wrong: {}'.format(hconfig))
    else:
        return hconfig


def _guess_file_format(f):
    """
    Tries to guess file format, first based on file extension (csv / tsv),
    then by looking for common column separators in the first 10 non-commented lines.
    Splits by tab / comma / space and counts resulting number of columns. Finds the most
    common column count, then comparsed how many lines had this number.
    eg. if tab, all 10 lines should have x columns when split by tab.
    Returns: csv | tsv | spaces   (spaces by default if all else fails)
    """
    filename, file_extension = os.path.splitext(f['fn'])
    tabs = []
    commas = []
    spaces = []
    j = 0
    for l in f['f'].splitlines:
        if not l.startswith('#'):
            j += 1
            tabs.append(len(l.split('\t')))
            commas.append(len(l.split(',')))
            spaces.append(len(l.split))
        if j == 10:
            break

    tab_mode = max((set(tabs)), key=(tabs.count))
    commas_mode = max((set(commas)), key=(commas.count))
    spaces_mode = max((set(spaces)), key=(spaces.count))
    tab_lc = tabs.count(tab_mode) if tab_mode > 1 else 0
    commas_lc = commas.count(commas_mode) if commas_mode > 1 else 0
    spaces_lc = spaces.count(spaces_mode) if spaces_mode > 1 else 0
    if tab_lc == j:
        return 'tsv'
    if commas_lc == j:
        return 'csv'
    if tab_lc > commas_lc:
        if tab_lc > spaces_lc:
            return 'tsv'
    if commas_lc > tab_lc:
        if commas_lc > spaces_lc:
            return 'csv'
    if spaces_lc > tab_lc:
        if spaces_lc > commas_lc:
            return 'spaces'
    if tab_mode == commas_lc:
        if tab_mode > spaces_lc:
            if tab_mode > commas_mode:
                return 'tsv'
            return 'csv'
    return 'spaces'


def _parse_txt(f, conf):
    sep = None
    if conf['file_format'] == 'csv':
        sep = ','
    if conf['file_format'] == 'tsv':
        sep = '\t'
    lines = f['f'].splitlines
    d = []
    if conf.get('plot_type') == 'html':
        for l in lines:
            if l:
                l.startswith('#') or d.append(l)

        return (
         '\n'.join(d), conf)
    ncols = None
    for l in lines:
        if l:
            sections = l.startswith('#') or l.split(sep)
            d.append(sections)
            if ncols is None:
                ncols = len(sections)
            elif ncols != len(sections):
                log.warn('Inconsistent number of columns found in {}! Skipping..'.format(f['fn']))
                return (None, conf)

    first_row_str = 0
    for i, l in enumerate(d):
        for j, v in enumerate(l):
            try:
                d[i][j] = float(v)
            except ValueError:
                if v.startswith('"') and v.endswith('"') or v.startswith("'"):
                    if v.endswith("'"):
                        v = v[1:-1]
                d[i][j] = v
                if i == 0:
                    first_row_str += 1

    all_numeric = all([type(l) == float for l in d[i][1:] for i in range1len(d)])
    if conf.get('plot_type') == 'generalstats':
        if len(d) >= 2:
            if ncols >= 2:
                data = defaultdict(dict)
                for i, l in enumerated[1:]1:
                    for j, v in enumeratel[1:]1:
                        data[l[0]][d[0][j]] = v

                return (
                 data, conf)
    if conf.get('plot_type') is None:
        if first_row_str == len(lines):
            if all_numeric:
                conf['plot_type'] = 'heatmap'
    if conf.get('plot_type') == 'heatmap':
        conf['xcats'] = d[0][1:]
        conf['ycats'] = [s[0] for s in d[1:]]
        data = [s[1:] for s in d[1:]]
        return (data, conf)
    if first_row_str == len(d[0]) or conf.get('plot_type') == 'table':
        data = OrderedDict
        for s in d[1:]:
            data[s[0]] = OrderedDict
            for i, v in enumerate(s[1:]):
                cat = str(d[0][(i + 1)])
                data[s[0]][cat] = v

        if conf.get('plot_type') is None:
            allfloats = True
            for r in d[1:]:
                for v in r[1:]:
                    allfloats = allfloats and type(v) == float

            if allfloats:
                conf['plot_type'] = 'bargraph'
            else:
                conf['plot_type'] = 'table'
        if conf.get('plot_type') == 'table':
            if d[0][0].strip != '':
                conf['pconfig'] = conf.get('pconfig', {})
                if not conf['pconfig'].get('col1_header'):
                    conf['pconfig']['col1_header'] = d[0][0].strip
        if conf.get('plot_type') == 'bargraph' or conf.get('plot_type') == 'table':
            return (
             data, conf)
        data = OrderedDict
    if conf.get('plot_type') is None:
        if len(d[0]) == 3:
            if type(d[0][0]) != float:
                if type(d[0][1]) == float:
                    if type(d[0][2]) == float:
                        conf['plot_type'] = 'scatter'
    if conf.get('plot_type') == 'scatter':
        data = dict
        for s in d:
            try:
                data[s[0]] = {'x':float(s[1]), 
                 'y':float(s[2])}
            except (IndexError, ValueError):
                pass

        return (
         data, conf)
    if len(d[0]) == 2:
        if conf.get('plot_type') is None:
            if type(d[0][0]) == float:
                if type(d[0][1]) == float:
                    conf['plot_type'] = 'linegraph'
        if conf.get('plot_type') is None:
            if type(d[0][0]) != float:
                if type(d[0][1]) == float:
                    conf['plot_type'] = 'bargraph'
        if not conf.get('plot_type') == 'linegraph':
            if conf.get('plot_type') == 'bargraph':
                if conf.get('id') is None:
                    conf['id'] = os.path.basename(f['root'])
                data = OrderedDict
                for s in d:
                    data[s[0]] = s[1]

                return (
                 {f['s_name']: data}, conf)
    if conf.get('plot_type') is None:
        if len(d[0]) > 4:
            if all_numeric:
                conf['plot_type'] = 'linegraph'
    if conf.get('plot_type') == 'linegraph':
        data = dict
        for s in d:
            data[s[0]] = dict
            for i, v in enumerate(s[1:]):
                j = i + 1
                data[s[0]][i + 1] = v

        return (
         data, conf)
    log.debug("Not able to figure out a plot type for '{}' ".format(f['fn']) + 'plot type = {}, all numeric = {}, first row str = {}'.formatconf.get('plot_type')all_numericfirst_row_str)
    return (None, conf)