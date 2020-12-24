# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\procode\tools\weather.py
# Compiled at: 2019-09-02 23:27:16
# Size of source mod 2**32: 4967 bytes
from urllib import request
import re, pinyin.pinyin, json, time
from lxml import etree
pc_city = {'anhui': 'hefei', 
 'beijing': 'beijing', 
 'chongqing': 'chongqing', 
 'fujian': 'fuzhou', 
 'gansu': 'lanzhou', 
 'guangdong': 'GuangZhou', 
 'guangxi': 'NanNing', 
 'guizhou': 'GuiYang', 
 'hainan': 'HaiKou', 
 'hebei': 'ShiJiaZhuang', 
 'heilongjiang': 'HaErBin', 
 'henan': 'ZhengZhou', 
 'xianggang': 'xianggang', 
 'hubei': 'WuHan', 
 'hunan': 'ChangSha', 
 'neimenggu': 'HuHeHaoTe', 
 'jiangsu': 'NanJing', 
 'jiangxi': 'NanChang', 
 'jilin': 'ChangChun', 
 'liaoning': 'ShenYang', 
 'aomen': 'aomen', 
 'ningxia': 'YinChuan', 
 'qinghai': 'XiNing', 
 'shanxi': 'XiAn', 
 'shandong': 'JiNan', 
 'shanghaishi': 'shanghai', 
 'shanx': 'TaiYuan', 
 'sichuan': 'ChengDu', 
 'tianjin': 'tianjin', 
 'xizang': 'LaSa', 
 'xinjiang': 'WuLuMuQi', 
 'yunnan': 'KunMing', 
 'zhejiang': 'HangZhou', 
 'taiwang': 'TaiBei'}

def getweather--- This code section failed: ---

 L.  49         0  LOAD_GLOBAL              request
                3  LOAD_ATTR                urlopen
                6  LOAD_STR                 'http://pv.sohu.com/cityjson'
                9  CALL_FUNCTION_1       1  '1 positional, 0 named'
               12  STORE_FAST               'res'

 L.  50        15  LOAD_FAST                'res'
               18  LOAD_ATTR                read
               21  CALL_FUNCTION_0       0  '0 positional, 0 named'
               24  LOAD_ATTR                decode
               27  LOAD_STR                 'gbk'
               30  CALL_FUNCTION_1       1  '1 positional, 0 named'
               33  STORE_FAST               'city_info'

 L.  51        36  LOAD_GLOBAL              print
               39  LOAD_FAST                'city_info'
               42  CALL_FUNCTION_1       1  '1 positional, 0 named'
               45  POP_TOP          

 L.  52        46  LOAD_GLOBAL              str
               49  LOAD_FAST                'city_info'
               52  CALL_FUNCTION_1       1  '1 positional, 0 named'
               55  LOAD_ATTR                split
               58  LOAD_STR                 '='
               61  CALL_FUNCTION_1       1  '1 positional, 0 named'
               64  LOAD_CONST               1
               67  BINARY_SUBSCR    
               68  LOAD_ATTR                split
               71  LOAD_STR                 ','
               74  CALL_FUNCTION_1       1  '1 positional, 0 named'
               77  LOAD_CONST               2
               80  BINARY_SUBSCR    
               81  LOAD_ATTR                split
               84  LOAD_STR                 '"'
               87  CALL_FUNCTION_1       1  '1 positional, 0 named'
               90  LOAD_CONST               3
               93  BINARY_SUBSCR    
               94  STORE_FAST               'addr'

 L.  53        97  LOAD_GLOBAL              pinyin
              100  LOAD_ATTR                get
              103  LOAD_FAST                'addr'
              106  LOAD_STR                 'format'
              109  LOAD_STR                 'strip'
              112  CALL_FUNCTION_257   257  '1 positional, 1 named'
              115  STORE_FAST               'py'

 L.  54       118  LOAD_FAST                'py'
              121  LOAD_ATTR                split
              124  LOAD_STR                 'sheng'
              127  LOAD_CONST               1
              130  CALL_FUNCTION_2       2  '2 positional, 0 named'
              133  LOAD_CONST               0
              136  BINARY_SUBSCR    
              137  LOAD_ATTR                replace
              140  LOAD_STR                 ' '
              143  LOAD_STR                 ''
              146  CALL_FUNCTION_2       2  '2 positional, 0 named'
              149  STORE_FAST               'provice'

 L.  57       152  LOAD_CONST               None
              155  STORE_FAST               'city'

 L.  58       158  SETUP_EXCEPT        215  'to 215'

 L.  59       161  LOAD_FAST                'py'
              164  LOAD_ATTR                split
              167  LOAD_STR                 'shi'
              170  CALL_FUNCTION_1       1  '1 positional, 0 named'
              173  LOAD_CONST               0
              176  BINARY_SUBSCR    
              177  LOAD_ATTR                split
              180  LOAD_STR                 'sheng'
              183  CALL_FUNCTION_1       1  '1 positional, 0 named'

 L.  60       186  LOAD_CONST               1
              189  BINARY_SUBSCR    
              190  LOAD_ATTR                strip
              193  CALL_FUNCTION_0       0  '0 positional, 0 named'
              196  LOAD_ATTR                replace
              199  LOAD_STR                 ' '
              202  LOAD_STR                 ''
              205  CALL_FUNCTION_2       2  '2 positional, 0 named'
              208  STORE_FAST               'city'
              211  POP_BLOCK        
              212  JUMP_FORWARD        258  'to 258'
            215_0  COME_FROM_EXCEPT    158  '158'

 L.  61       215  DUP_TOP          
              216  LOAD_GLOBAL              Exception
              219  COMPARE_OP               exception-match
              222  POP_JUMP_IF_FALSE   257  'to 257'
              225  POP_TOP          
              226  STORE_FAST               'e'
              229  POP_TOP          
              230  SETUP_FINALLY       244  'to 244'

 L.  62       233  LOAD_CONST               None
              236  STORE_FAST               'city'
              239  POP_BLOCK        
              240  POP_EXCEPT       
              241  LOAD_CONST               None
            244_0  COME_FROM_FINALLY   230  '230'
              244  LOAD_CONST               None
              247  STORE_FAST               'e'
              250  DELETE_FAST              'e'
              253  END_FINALLY      
              254  JUMP_FORWARD        258  'to 258'
              257  END_FINALLY      
            258_0  COME_FROM           254  '254'
            258_1  COME_FROM           212  '212'

 L.  65       258  LOAD_FAST                'city'
              261  UNARY_NOT        
              262  POP_JUMP_IF_TRUE    277  'to 277'
              265  LOAD_FAST                'city'
              268  LOAD_CONST               None
              271  COMPARE_OP               ==
            274_0  COME_FROM           262  '262'
              274  POP_JUMP_IF_FALSE   337  'to 337'

 L.  66       277  SETUP_LOOP          337  'to 337'
              280  LOAD_GLOBAL              pc_city
              283  LOAD_ATTR                items
              286  CALL_FUNCTION_0       0  '0 positional, 0 named'
              289  GET_ITER         
              290  FOR_ITER            336  'to 336'
              293  UNPACK_SEQUENCE_2     2 
              296  STORE_FAST               'k'
              299  STORE_FAST               'v'

 L.  67       302  LOAD_FAST                'k'
              305  LOAD_FAST                'provice'
              308  COMPARE_OP               ==
              311  POP_JUMP_IF_TRUE    326  'to 326'
              314  LOAD_FAST                'k'
              317  LOAD_FAST                'provice'
              320  COMPARE_OP               in
            323_0  COME_FROM           311  '311'
              323  POP_JUMP_IF_FALSE   290  'to 290'

 L.  68       326  LOAD_FAST                'v'
              329  STORE_FAST               'city'

 L.  69       332  BREAK_LOOP       
            333_0  COME_FROM           323  '323'
              333  JUMP_BACK           290  'to 290'
              336  POP_BLOCK        
            337_0  COME_FROM_LOOP      277  '277'
            337_1  COME_FROM           274  '274'

 L.  71       337  LOAD_STR                 'http://qq.ip138.com/weather/%s/%s.htm'
              340  LOAD_FAST                'provice'
              343  LOAD_FAST                'city'
              346  BUILD_TUPLE_2         2 
              349  BINARY_MODULO    
              350  STORE_FAST               'url'

 L.  73       353  LOAD_FAST                'city'
              356  LOAD_STR                 'shanghai'
              359  COMPARE_OP               ==
              362  POP_JUMP_IF_FALSE   375  'to 375'

 L.  74       365  LOAD_STR                 'http://qq.ip138.com/weather/%s'
              368  LOAD_FAST                'city'
              371  BINARY_MODULO    
              372  STORE_FAST               'url'
            375_0  COME_FROM           362  '362'

 L.  77       375  LOAD_GLOBAL              request
              378  LOAD_ATTR                urlopen
              381  LOAD_FAST                'url'
              384  CALL_FUNCTION_1       1  '1 positional, 0 named'
              387  LOAD_ATTR                read
              390  CALL_FUNCTION_0       0  '0 positional, 0 named'
              393  LOAD_ATTR                decode
              396  LOAD_STR                 'gbk'
              399  CALL_FUNCTION_1       1  '1 positional, 0 named'
              402  STORE_FAST               'wea_info'

 L.  80       405  LOAD_GLOBAL              etree
              408  LOAD_ATTR                HTML
              411  LOAD_FAST                'wea_info'
              414  CALL_FUNCTION_1       1  '1 positional, 0 named'
              417  STORE_FAST               'tree'

 L.  81       420  LOAD_FAST                'tree'
              423  LOAD_ATTR                xpath
              426  LOAD_STR                 "/descendant::table[@class='t12']/tr"
              429  CALL_FUNCTION_1       1  '1 positional, 0 named'
              432  STORE_FAST               'nodes'

 L.  82       435  LOAD_FAST                'nodes'
              438  LOAD_CONST               1
              441  LOAD_CONST               None
              444  BUILD_SLICE_2         2 
              447  BINARY_SUBSCR    
              448  STORE_FAST               'n_nodes'

 L.  84       451  BUILD_LIST_0          0 
              454  STORE_FAST               'weathers'

 L.  85       457  SETUP_LOOP          679  'to 679'
              460  LOAD_GLOBAL              range
              463  LOAD_GLOBAL              len
              466  LOAD_FAST                'n_nodes'
              469  CALL_FUNCTION_1       1  '1 positional, 0 named'
              472  CALL_FUNCTION_1       1  '1 positional, 0 named'
              475  GET_ITER         
              476  FOR_ITER            678  'to 678'
              479  STORE_FAST               'n'

 L.  86       482  LOAD_FAST                'n_nodes'
              485  LOAD_FAST                'n'
              488  BINARY_SUBSCR    
              489  LOAD_ATTR                xpath
              492  LOAD_STR                 'td'
              495  CALL_FUNCTION_1       1  '1 positional, 0 named'
              498  STORE_FAST               'items'

 L.  87       501  BUILD_LIST_0          0 
              504  STORE_FAST               'weathers_items'

 L.  88       507  SETUP_LOOP          662  'to 662'
              510  LOAD_FAST                'items'
              513  GET_ITER         
              514  FOR_ITER            661  'to 661'
              517  STORE_FAST               'r'

 L.  89       520  LOAD_FAST                'r'
              523  LOAD_ATTR                text
              526  LOAD_CONST               None
              529  COMPARE_OP               is
              532  POP_JUMP_IF_FALSE   642  'to 642'

 L.  90       535  LOAD_FAST                'r'
              538  LOAD_ATTR                xpath
              541  LOAD_STR                 'img'
              544  CALL_FUNCTION_1       1  '1 positional, 0 named'
              547  STORE_FAST               'tq'

 L.  91       550  LOAD_STR                 ''
              553  STORE_FAST               'qt_str'

 L.  92       556  SETUP_LOOP          626  'to 626'
              559  LOAD_FAST                'tq'
              562  GET_ITER         
              563  FOR_ITER            625  'to 625'
              566  STORE_FAST               'i_tq'

 L.  93       569  LOAD_FAST                'qt_str'
              572  LOAD_STR                 ''
              575  COMPARE_OP               ==
              578  POP_JUMP_IF_FALSE   599  'to 599'

 L.  94       581  LOAD_FAST                'i_tq'
              584  LOAD_ATTR                get
              587  LOAD_STR                 'alt'
              590  CALL_FUNCTION_1       1  '1 positional, 0 named'
              593  STORE_FAST               'qt_str'
              596  JUMP_BACK           563  'to 563'
              599  ELSE                     '622'

 L.  96       599  LOAD_FAST                'qt_str'
              602  LOAD_STR                 '转'
              605  BINARY_ADD       
              606  LOAD_FAST                'i_tq'
              609  LOAD_ATTR                get
              612  LOAD_STR                 'alt'
              615  CALL_FUNCTION_1       1  '1 positional, 0 named'
              618  BINARY_ADD       
              619  STORE_FAST               'qt_str'
              622  JUMP_BACK           563  'to 563'
              625  POP_BLOCK        
            626_0  COME_FROM_LOOP      556  '556'

 L.  97       626  LOAD_FAST                'weathers_items'
              629  LOAD_ATTR                append
              632  LOAD_FAST                'qt_str'
              635  CALL_FUNCTION_1       1  '1 positional, 0 named'
              638  POP_TOP          
              639  JUMP_BACK           514  'to 514'
              642  ELSE                     '658'

 L.  99       642  LOAD_FAST                'weathers_items'
              645  LOAD_ATTR                append
              648  LOAD_FAST                'r'
              651  LOAD_ATTR                text
              654  CALL_FUNCTION_1       1  '1 positional, 0 named'
              657  POP_TOP          
              658  JUMP_BACK           514  'to 514'
              661  POP_BLOCK        
            662_0  COME_FROM_LOOP      507  '507'

 L. 100       662  LOAD_FAST                'weathers'
              665  LOAD_ATTR                append
              668  LOAD_FAST                'weathers_items'
              671  CALL_FUNCTION_1       1  '1 positional, 0 named'
              674  POP_TOP          
              675  JUMP_BACK           476  'to 476'
              678  POP_BLOCK        
            679_0  COME_FROM_LOOP      457  '457'

 L. 104       679  LOAD_GLOBAL              time
              682  LOAD_ATTR                localtime
              685  CALL_FUNCTION_0       0  '0 positional, 0 named'
              688  STORE_FAST               'n_time'

 L. 105       691  LOAD_FAST                'n_time'
              694  LOAD_ATTR                tm_year
              697  STORE_FAST               'n_year'

 L. 106       700  LOAD_FAST                'n_time'
              703  LOAD_ATTR                tm_mon
              706  STORE_FAST               'n_mon'

 L. 107       709  LOAD_FAST                'n_time'
              712  LOAD_ATTR                tm_mday
              715  STORE_FAST               'n_day'

 L. 109       718  LOAD_STR                 'date'
              721  LOAD_STR                 ''

 L. 110       724  LOAD_STR                 'weather'
              727  LOAD_STR                 ''

 L. 111       730  LOAD_STR                 'temperature'
              733  LOAD_STR                 ''

 L. 112       736  LOAD_STR                 'wind'
              739  LOAD_STR                 ''

 L. 113       742  LOAD_STR                 'addr'
              745  LOAD_STR                 ''

 L. 114       748  LOAD_STR                 'icon'
              751  LOAD_STR                 ''
              754  BUILD_MAP_6           6 
              757  STORE_FAST               'todayweather'

 L. 115       760  SETUP_LOOP         1355  'to 1355'
              763  LOAD_GLOBAL              range
              766  LOAD_GLOBAL              len
              769  LOAD_FAST                'weathers'
              772  LOAD_CONST               0
              775  BINARY_SUBSCR    
              776  CALL_FUNCTION_1       1  '1 positional, 0 named'
              779  CALL_FUNCTION_1       1  '1 positional, 0 named'
              782  GET_ITER         
              783  FOR_ITER           1354  'to 1354'
              786  STORE_FAST               'i'

 L. 116       789  LOAD_FAST                'weathers'
              792  LOAD_CONST               0
              795  BINARY_SUBSCR    
              796  LOAD_FAST                'i'
              799  BINARY_SUBSCR    
              800  LOAD_ATTR                find

 L. 117       803  LOAD_GLOBAL              str
              806  LOAD_FAST                'n_year'
              809  CALL_FUNCTION_1       1  '1 positional, 0 named'
              812  LOAD_STR                 '-'
              815  BINARY_ADD       
              816  LOAD_GLOBAL              str
              819  LOAD_FAST                'n_mon'
              822  CALL_FUNCTION_1       1  '1 positional, 0 named'
              825  BINARY_ADD       
              826  LOAD_STR                 '-'
              829  BINARY_ADD       
              830  LOAD_GLOBAL              str
              833  LOAD_FAST                'n_day'
              836  CALL_FUNCTION_1       1  '1 positional, 0 named'
              839  BINARY_ADD       
              840  CALL_FUNCTION_1       1  '1 positional, 0 named'
              843  LOAD_CONST               -1
              846  COMPARE_OP               !=
              849  POP_JUMP_IF_FALSE   783  'to 783'

 L. 118       852  SETUP_LOOP         1351  'to 1351'
              855  LOAD_GLOBAL              range
              858  LOAD_GLOBAL              len
              861  LOAD_FAST                'weathers'
              864  CALL_FUNCTION_1       1  '1 positional, 0 named'
              867  CALL_FUNCTION_1       1  '1 positional, 0 named'
              870  GET_ITER         
              871  FOR_ITER           1344  'to 1344'
              874  STORE_FAST               'j'

 L. 119       877  LOAD_FAST                'j'
              880  LOAD_CONST               0
              883  COMPARE_OP               ==
              886  POP_JUMP_IF_FALSE   910  'to 910'

 L. 120       889  LOAD_FAST                'weathers'
              892  LOAD_FAST                'j'
              895  BINARY_SUBSCR    
              896  LOAD_FAST                'i'
              899  BINARY_SUBSCR    
              900  LOAD_FAST                'todayweather'
              903  LOAD_STR                 'date'
              906  STORE_SUBSCR     
              907  JUMP_BACK           871  'to 871'
              910  ELSE                     '1341'

 L. 121       910  LOAD_FAST                'j'
              913  LOAD_CONST               1
              916  COMPARE_OP               ==
              919  POP_JUMP_IF_FALSE  1278  'to 1278'

 L. 122       922  LOAD_FAST                'weathers'
              925  LOAD_FAST                'j'
              928  BINARY_SUBSCR    
              929  LOAD_FAST                'i'
              932  BINARY_SUBSCR    
              933  LOAD_FAST                'todayweather'
              936  LOAD_STR                 'weather'
              939  STORE_SUBSCR     

 L. 123       940  LOAD_GLOBAL              str
              943  LOAD_FAST                'weathers'
              946  LOAD_FAST                'j'
              949  BINARY_SUBSCR    
              950  LOAD_FAST                'i'
              953  BINARY_SUBSCR    
              954  CALL_FUNCTION_1       1  '1 positional, 0 named'
              957  LOAD_ATTR                find
              960  LOAD_STR                 '转'
              963  CALL_FUNCTION_1       1  '1 positional, 0 named'
              966  POP_JUMP_IF_FALSE  1005  'to 1005'

 L. 124       969  LOAD_GLOBAL              str
              972  LOAD_FAST                'weathers'
              975  LOAD_FAST                'j'
              978  BINARY_SUBSCR    
              979  LOAD_FAST                'i'
              982  BINARY_SUBSCR    
              983  CALL_FUNCTION_1       1  '1 positional, 0 named'
              986  LOAD_ATTR                split
              989  LOAD_STR                 '转'
              992  CALL_FUNCTION_1       1  '1 positional, 0 named'
              995  LOAD_CONST               -1
              998  BINARY_SUBSCR    
              999  STORE_FAST               'n_weather'
             1002  JUMP_FORWARD       1025  'to 1025'
             1005  ELSE                     '1025'

 L. 126      1005  LOAD_GLOBAL              str
             1008  LOAD_FAST                'weathers'
             1011  LOAD_FAST                'j'
             1014  BINARY_SUBSCR    
             1015  LOAD_FAST                'i'
             1018  BINARY_SUBSCR    
             1019  CALL_FUNCTION_1       1  '1 positional, 0 named'
             1022  STORE_FAST               'n_weather'
           1025_0  COME_FROM          1002  '1002'

 L. 128      1025  LOAD_GLOBAL              str
             1028  LOAD_FAST                'n_weather'
             1031  CALL_FUNCTION_1       1  '1 positional, 0 named'
             1034  LOAD_ATTR                find
             1037  LOAD_STR                 '雨'
             1040  CALL_FUNCTION_1       1  '1 positional, 0 named'
             1043  LOAD_CONST               0
             1046  COMPARE_OP               >=
             1049  POP_JUMP_IF_FALSE  1065  'to 1065'

 L. 129      1052  LOAD_STR                 '&#xe649;'
             1055  LOAD_FAST                'todayweather'
             1058  LOAD_STR                 'icon'
             1061  STORE_SUBSCR     
             1062  JUMP_ABSOLUTE      1341  'to 1341'
             1065  ELSE                     '1275'

 L. 130      1065  LOAD_GLOBAL              str
             1068  LOAD_FAST                'n_weather'
             1071  CALL_FUNCTION_1       1  '1 positional, 0 named'
             1074  LOAD_ATTR                find
             1077  LOAD_STR                 '雪'
             1080  CALL_FUNCTION_1       1  '1 positional, 0 named'
             1083  LOAD_CONST               0
             1086  COMPARE_OP               >=
             1089  POP_JUMP_IF_FALSE  1105  'to 1105'

 L. 131      1092  LOAD_STR                 '&#xe64b;'
             1095  LOAD_FAST                'todayweather'
             1098  LOAD_STR                 'icon'
             1101  STORE_SUBSCR     
             1102  JUMP_ABSOLUTE      1341  'to 1341'
             1105  ELSE                     '1275'

 L. 132      1105  LOAD_GLOBAL              str
             1108  LOAD_FAST                'n_weather'
             1111  CALL_FUNCTION_1       1  '1 positional, 0 named'
             1114  LOAD_ATTR                find
             1117  LOAD_STR                 '晴'
             1120  CALL_FUNCTION_1       1  '1 positional, 0 named'
             1123  LOAD_CONST               0
             1126  COMPARE_OP               >=
             1129  POP_JUMP_IF_FALSE  1145  'to 1145'

 L. 133      1132  LOAD_STR                 '&#xe64d;'
             1135  LOAD_FAST                'todayweather'
             1138  LOAD_STR                 'icon'
             1141  STORE_SUBSCR     
             1142  JUMP_ABSOLUTE      1341  'to 1341'
             1145  ELSE                     '1275'

 L. 134      1145  LOAD_GLOBAL              str
             1148  LOAD_FAST                'n_weather'
             1151  CALL_FUNCTION_1       1  '1 positional, 0 named'
             1154  LOAD_ATTR                find
             1157  LOAD_STR                 '阴'
             1160  CALL_FUNCTION_1       1  '1 positional, 0 named'
             1163  LOAD_CONST               0
             1166  COMPARE_OP               >=
             1169  POP_JUMP_IF_FALSE  1185  'to 1185'

 L. 135      1172  LOAD_STR                 '&#xe64c;'
             1175  LOAD_FAST                'todayweather'
             1178  LOAD_STR                 'icon'
             1181  STORE_SUBSCR     
             1182  JUMP_ABSOLUTE      1341  'to 1341'
             1185  ELSE                     '1275'

 L. 136      1185  LOAD_GLOBAL              str
             1188  LOAD_FAST                'n_weather'
             1191  CALL_FUNCTION_1       1  '1 positional, 0 named'
             1194  LOAD_ATTR                find
             1197  LOAD_STR                 '多云'
             1200  CALL_FUNCTION_1       1  '1 positional, 0 named'
             1203  LOAD_CONST               0
             1206  COMPARE_OP               >=
             1209  POP_JUMP_IF_FALSE  1225  'to 1225'

 L. 137      1212  LOAD_STR                 '&#xe64e;'
             1215  LOAD_FAST                'todayweather'
             1218  LOAD_STR                 'icon'
             1221  STORE_SUBSCR     
             1222  JUMP_ABSOLUTE      1341  'to 1341'
             1225  ELSE                     '1275'

 L. 138      1225  LOAD_GLOBAL              str
             1228  LOAD_FAST                'n_weather'
             1231  CALL_FUNCTION_1       1  '1 positional, 0 named'
             1234  LOAD_ATTR                find
             1237  LOAD_STR                 '雨夹雪'
             1240  CALL_FUNCTION_1       1  '1 positional, 0 named'
             1243  LOAD_CONST               0
             1246  COMPARE_OP               >=
             1249  POP_JUMP_IF_FALSE  1265  'to 1265'

 L. 139      1252  LOAD_STR                 '&#xe64a;'
             1255  LOAD_FAST                'todayweather'
             1258  LOAD_STR                 'icon'
             1261  STORE_SUBSCR     
             1262  JUMP_ABSOLUTE      1341  'to 1341'
             1265  ELSE                     '1275'

 L. 141      1265  LOAD_STR                 '&#xe64d;'
             1268  LOAD_FAST                'todayweather'
             1271  LOAD_STR                 'icon'
             1274  STORE_SUBSCR     
             1275  JUMP_BACK           871  'to 871'
             1278  ELSE                     '1341'

 L. 142      1278  LOAD_FAST                'j'
             1281  LOAD_CONST               2
             1284  COMPARE_OP               ==
             1287  POP_JUMP_IF_FALSE  1311  'to 1311'

 L. 143      1290  LOAD_FAST                'weathers'
             1293  LOAD_FAST                'j'
             1296  BINARY_SUBSCR    
             1297  LOAD_FAST                'i'
             1300  BINARY_SUBSCR    
             1301  LOAD_FAST                'todayweather'
             1304  LOAD_STR                 'temperature'
             1307  STORE_SUBSCR     
             1308  JUMP_BACK           871  'to 871'
             1311  ELSE                     '1341'

 L. 144      1311  LOAD_FAST                'j'
             1314  LOAD_CONST               3
             1317  COMPARE_OP               ==
             1320  POP_JUMP_IF_FALSE   871  'to 871'

 L. 145      1323  LOAD_FAST                'weathers'
             1326  LOAD_FAST                'j'
             1329  BINARY_SUBSCR    
             1330  LOAD_FAST                'i'
             1333  BINARY_SUBSCR    
             1334  LOAD_FAST                'todayweather'
             1337  LOAD_STR                 'wind'
             1340  STORE_SUBSCR     
           1341_0  COME_FROM          1320  '1320'
             1341  JUMP_BACK           871  'to 871'
             1344  POP_BLOCK        
             1345  JUMP_BACK           783  'to 783'
           1348_0  COME_FROM_LOOP      852  '852'

 L. 147      1348  CONTINUE            783  'to 783'
             1351  JUMP_BACK           783  'to 783'
             1354  POP_BLOCK        
           1355_0  COME_FROM_LOOP      760  '760'

 L. 148      1355  LOAD_FAST                'addr'
             1358  LOAD_FAST                'todayweather'
             1361  LOAD_STR                 'addr'
             1364  STORE_SUBSCR     

 L. 150      1365  LOAD_FAST                'todayweather'
             1368  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_BACK' instruction at offset 1345