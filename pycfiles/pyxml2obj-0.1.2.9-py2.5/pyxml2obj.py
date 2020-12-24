# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/pyxml2obj/pyxml2obj.py
# Compiled at: 2010-02-04 03:43:23
import warnings, re
from xml.sax import *

def XMLin(content, options={}):
    obj = xml2obj(options)
    obj.XMLin(content)
    return obj.tree


def XMLout(tree, options={}):
    obj = xml2obj(options)
    xml = obj.XMLout(tree)
    return xml


StrictMode = 0
KnownOptIn = ('keyattr keeproot forcecontent contentkey noattr                forcearray grouptags normalizespace valueattr').split()
KnownOptOut = ('keyattr keeproot contentkey noattr                rootname xmldecl noescape grouptags valueattr').split()
DefKeyAttr = ('name key id').split()
DefRootName = 'root'
DefContentKey = 'content'
DefXmlDecl = "<?xml version='1.0' standalone='yes'?>"

class xml2obj(ContentHandler):

    def __init__(self, options={}):
        known_opt = {}
        for key in KnownOptIn + KnownOptOut:
            known_opt[key] = None

        def_opt = {}
        for (key, val) in options.items():
            lkey = key.lower().replace('_', '')
            if lkey not in known_opt:
                raise KeyError('%s is not acceptable' % (lkey,))
            def_opt[lkey] = val

        self.def_opt = def_opt
        return

    def XMLin(self, content, options={}):
        self.handle_options('in', options)
        self.build_tree(content)

    def build_tree(self, content):
        parseString(content, self)

    def handle_options--- This code section failed: ---

 L.  51         0  BUILD_MAP             0 
                3  STORE_FAST            3  'known_opt'

 L.  52         6  LOAD_FAST             1  'dirn'
                9  LOAD_CONST               'in'
               12  COMPARE_OP            2  ==
               15  JUMP_IF_FALSE        31  'to 49'
               18  POP_TOP          

 L.  53        19  SETUP_LOOP           55  'to 77'
               22  LOAD_GLOBAL           0  'KnownOptIn'
               25  GET_ITER         
               26  FOR_ITER             16  'to 45'
               29  STORE_FAST            4  'key'

 L.  54        32  LOAD_FAST             4  'key'
               35  LOAD_FAST             3  'known_opt'
               38  LOAD_FAST             4  'key'
               41  STORE_SUBSCR     
               42  JUMP_BACK            26  'to 26'
               45  POP_BLOCK        
               46  JUMP_FORWARD         28  'to 77'
             49_0  COME_FROM            15  '15'
               49  POP_TOP          

 L.  56        50  SETUP_LOOP           24  'to 77'
               53  LOAD_GLOBAL           1  'KnownOptOut'
               56  GET_ITER         
               57  FOR_ITER             16  'to 76'
               60  STORE_FAST            4  'key'

 L.  57        63  LOAD_FAST             4  'key'
               66  LOAD_FAST             3  'known_opt'
               69  LOAD_FAST             4  'key'
               72  STORE_SUBSCR     
               73  JUMP_BACK            57  'to 57'
               76  POP_BLOCK        
             77_0  COME_FROM            50  '50'
             77_1  COME_FROM            19  '19'

 L.  59        77  LOAD_FAST             2  'options'
               80  STORE_FAST            5  'row_opt'

 L.  60        83  BUILD_MAP             0 
               86  LOAD_FAST             0  'self'
               89  STORE_ATTR            2  'opt'

 L.  62        92  SETUP_LOOP           92  'to 187'
               95  LOAD_FAST             5  'row_opt'
               98  GET_ITER         
               99  FOR_ITER             84  'to 186'
              102  UNPACK_SEQUENCE_2     2 
              105  STORE_FAST            4  'key'
              108  STORE_FAST            6  'val'

 L.  63       111  LOAD_FAST             4  'key'
              114  LOAD_ATTR             3  'lower'
              117  CALL_FUNCTION_0       0  None
              120  LOAD_ATTR             4  'replace'
              123  LOAD_CONST               '_'
              126  LOAD_CONST               ''
              129  CALL_FUNCTION_2       2  None
              132  STORE_FAST            7  'lkey'

 L.  64       135  LOAD_FAST             4  'key'
              138  LOAD_FAST             3  'known_opt'
              141  COMPARE_OP            7  not-in
              144  JUMP_IF_FALSE        22  'to 169'
            147_0  THEN                     170
              147  POP_TOP          

 L.  65       148  LOAD_GLOBAL           5  'KeyError'
              151  LOAD_CONST               '%s is not acceptable'
              154  LOAD_FAST             4  'key'
              157  CALL_FUNCTION_1       1  None
              160  CALL_FUNCTION_1       1  None
              163  RAISE_VARARGS_1       1  None
              166  JUMP_FORWARD          1  'to 170'
            169_0  COME_FROM           144  '144'
              169  POP_TOP          
            170_0  COME_FROM           166  '166'

 L.  66       170  LOAD_FAST             6  'val'
              173  LOAD_FAST             0  'self'
              176  LOAD_ATTR             2  'opt'
              179  LOAD_FAST             7  'lkey'
              182  STORE_SUBSCR     
              183  JUMP_BACK            99  'to 99'
              186  POP_BLOCK        
            187_0  COME_FROM            92  '92'

 L.  69       187  SETUP_LOOP           74  'to 264'
              190  LOAD_FAST             3  'known_opt'
              193  GET_ITER         
              194  FOR_ITER             66  'to 263'
              197  STORE_FAST            4  'key'

 L.  70       200  LOAD_FAST             4  'key'
              203  LOAD_FAST             0  'self'
              206  LOAD_ATTR             2  'opt'
              209  COMPARE_OP            7  not-in
              212  JUMP_IF_FALSE        44  'to 259'
              215  POP_TOP          

 L.  71       216  LOAD_FAST             4  'key'
              219  LOAD_FAST             0  'self'
              222  LOAD_ATTR             6  'def_opt'
              225  COMPARE_OP            6  in
              228  JUMP_IF_FALSE        24  'to 255'
              231  POP_TOP          

 L.  72       232  LOAD_FAST             0  'self'
              235  LOAD_ATTR             6  'def_opt'
              238  LOAD_FAST             4  'key'
              241  BINARY_SUBSCR    
              242  LOAD_FAST             0  'self'
              245  LOAD_ATTR             2  'opt'
              248  LOAD_FAST             4  'key'
              251  STORE_SUBSCR     
              252  JUMP_ABSOLUTE       260  'to 260'
            255_0  COME_FROM           228  '228'
              255  POP_TOP          
              256  JUMP_BACK           194  'to 194'
            259_0  COME_FROM           212  '212'
              259  POP_TOP          
              260  JUMP_BACK           194  'to 194'
              263  POP_BLOCK        
            264_0  COME_FROM           187  '187'

 L.  75       264  LOAD_CONST               'rootname'
              267  LOAD_FAST             0  'self'
              270  LOAD_ATTR             2  'opt'
              273  COMPARE_OP            6  in
              276  JUMP_IF_FALSE        35  'to 314'
              279  POP_TOP          

 L.  76       280  LOAD_FAST             0  'self'
              283  LOAD_ATTR             2  'opt'
              286  LOAD_CONST               'rootname'
              289  BINARY_SUBSCR    
              290  JUMP_IF_TRUE         17  'to 310'
              293  POP_TOP          

 L.  77       294  LOAD_CONST               ''
              297  LOAD_FAST             0  'self'
              300  LOAD_ATTR             2  'opt'
              303  LOAD_CONST               'rootname'
              306  STORE_SUBSCR     
              307  JUMP_ABSOLUTE       328  'to 328'
            310_0  COME_FROM           290  '290'
              310  POP_TOP          
              311  JUMP_FORWARD         14  'to 328'
            314_0  COME_FROM           276  '276'
              314  POP_TOP          

 L.  79       315  LOAD_GLOBAL           7  'DefRootName'
              318  LOAD_FAST             0  'self'
              321  LOAD_ATTR             2  'opt'
              324  LOAD_CONST               'rootname'
              327  STORE_SUBSCR     
            328_0  COME_FROM           311  '311'

 L.  81       328  LOAD_CONST               'xmldecl'
              331  LOAD_FAST             0  'self'
              334  LOAD_ATTR             2  'opt'
              337  COMPARE_OP            6  in
              340  JUMP_IF_FALSE        43  'to 386'
              343  POP_TOP          
              344  LOAD_GLOBAL           8  'str'
              347  LOAD_FAST             0  'self'
              350  LOAD_ATTR             2  'opt'
              353  LOAD_CONST               'xmldecl'
              356  BINARY_SUBSCR    
              357  CALL_FUNCTION_1       1  None
              360  LOAD_CONST               '1'
              363  COMPARE_OP            2  ==
              366  JUMP_IF_FALSE        17  'to 386'
            369_0  THEN                     387
              369  POP_TOP          

 L.  82       370  LOAD_GLOBAL           9  'DefXmlDecl'
              373  LOAD_FAST             0  'self'
              376  LOAD_ATTR             2  'opt'
              379  LOAD_CONST               'xmldecl'
              382  STORE_SUBSCR     
              383  JUMP_FORWARD          1  'to 387'
            386_0  COME_FROM           366  '366'
            386_1  COME_FROM           340  '340'
              386  POP_TOP          
            387_0  COME_FROM           383  '383'

 L.  84       387  LOAD_CONST               'contentkey'
              390  LOAD_FAST             0  'self'
              393  LOAD_ATTR             2  'opt'
              396  COMPARE_OP            6  in
              399  JUMP_IF_FALSE        75  'to 477'
              402  POP_TOP          

 L.  85       403  LOAD_GLOBAL          10  're'
              406  LOAD_ATTR            11  'match'
              409  LOAD_CONST               '^-(.*)$'
              412  LOAD_FAST             0  'self'
              415  LOAD_ATTR             2  'opt'
              418  LOAD_CONST               'contentkey'
              421  BINARY_SUBSCR    
              422  CALL_FUNCTION_2       2  None
              425  STORE_FAST            8  'm'

 L.  86       428  LOAD_FAST             8  'm'
              431  JUMP_IF_FALSE        39  'to 473'
              434  POP_TOP          

 L.  87       435  LOAD_FAST             8  'm'
              438  LOAD_ATTR            12  'group'
              441  LOAD_CONST               1
              444  CALL_FUNCTION_1       1  None
              447  LOAD_FAST             0  'self'
              450  LOAD_ATTR             2  'opt'
              453  LOAD_CONST               'contentkey'
              456  STORE_SUBSCR     

 L.  88       457  LOAD_CONST               1
              460  LOAD_FAST             0  'self'
              463  LOAD_ATTR             2  'opt'
              466  LOAD_CONST               'collapseagain'
              469  STORE_SUBSCR     
              470  JUMP_ABSOLUTE       491  'to 491'
            473_0  COME_FROM           431  '431'
              473  POP_TOP          
              474  JUMP_FORWARD         14  'to 491'
            477_0  COME_FROM           399  '399'
              477  POP_TOP          

 L.  90       478  LOAD_GLOBAL          13  'DefContentKey'
              481  LOAD_FAST             0  'self'
              484  LOAD_ATTR             2  'opt'
              487  LOAD_CONST               'contentkey'
              490  STORE_SUBSCR     
            491_0  COME_FROM           474  '474'

 L.  92       491  LOAD_CONST               'normalizespace'
              494  LOAD_FAST             0  'self'
              497  LOAD_ATTR             2  'opt'
              500  COMPARE_OP            7  not-in
              503  JUMP_IF_FALSE        17  'to 523'
            506_0  THEN                     524
              506  POP_TOP          

 L.  93       507  LOAD_CONST               0
              510  LOAD_FAST             0  'self'
              513  LOAD_ATTR             2  'opt'
              516  LOAD_CONST               'normalizespace'
              519  STORE_SUBSCR     
              520  JUMP_FORWARD          1  'to 524'
            523_0  COME_FROM           503  '503'
              523  POP_TOP          
            524_0  COME_FROM           520  '520'

 L.  96       524  LOAD_CONST               'forcearray'
              527  LOAD_FAST             0  'self'
              530  LOAD_ATTR             2  'opt'
              533  COMPARE_OP            6  in
              536  JUMP_IF_FALSE       127  'to 666'
              539  POP_TOP          

 L.  97       540  LOAD_GLOBAL          14  'isinstance'
              543  LOAD_FAST             0  'self'
              546  LOAD_ATTR             2  'opt'
              549  LOAD_CONST               'forcearray'
              552  BINARY_SUBSCR    
              553  LOAD_GLOBAL          15  'list'
              556  CALL_FUNCTION_2       2  None
              559  JUMP_IF_FALSE       100  'to 662'
              562  POP_TOP          

 L.  98       563  LOAD_FAST             0  'self'
              566  LOAD_ATTR             2  'opt'
              569  LOAD_CONST               'forcearray'
              572  BINARY_SUBSCR    
              573  STORE_FAST            9  'force_list'

 L.  99       576  LOAD_GLOBAL          16  'len'
              579  LOAD_FAST             9  'force_list'
              582  CALL_FUNCTION_1       1  None
              585  LOAD_CONST               0
              588  COMPARE_OP            4  >
              591  JUMP_IF_FALSE        51  'to 645'
              594  POP_TOP          

 L. 100       595  BUILD_MAP             0 
              598  LOAD_FAST             0  'self'
              601  LOAD_ATTR             2  'opt'
              604  LOAD_CONST               'forcearray'
              607  STORE_SUBSCR     

 L. 101       608  SETUP_LOOP           48  'to 659'
              611  LOAD_FAST             9  'force_list'
              614  GET_ITER         
              615  FOR_ITER             23  'to 641'
              618  STORE_FAST           10  'tag'

 L. 102       621  LOAD_CONST               1
              624  LOAD_FAST             0  'self'
              627  LOAD_ATTR             2  'opt'
              630  LOAD_CONST               'forcearray'
              633  BINARY_SUBSCR    
              634  LOAD_FAST            10  'tag'
              637  STORE_SUBSCR     
              638  JUMP_BACK           615  'to 615'
              641  POP_BLOCK        
              642  JUMP_ABSOLUTE       663  'to 663'
            645_0  COME_FROM           591  '591'
              645  POP_TOP          

 L. 104       646  LOAD_CONST               0
              649  LOAD_FAST             0  'self'
              652  LOAD_ATTR             2  'opt'
              655  LOAD_CONST               'forcearray'
              658  STORE_SUBSCR     
            659_0  COME_FROM           608  '608'
              659  JUMP_ABSOLUTE       680  'to 680'
            662_0  COME_FROM           559  '559'
              662  POP_TOP          
              663  JUMP_FORWARD         14  'to 680'
            666_0  COME_FROM           536  '536'
              666  POP_TOP          

 L. 106       667  LOAD_CONST               0
              670  LOAD_FAST             0  'self'
              673  LOAD_ATTR             2  'opt'
              676  LOAD_CONST               'forcearray'
              679  STORE_SUBSCR     
            680_0  COME_FROM           663  '663'

 L. 109       680  LOAD_CONST               'keyattr'
              683  LOAD_FAST             0  'self'
              686  LOAD_ATTR             2  'opt'
              689  COMPARE_OP            6  in
              692  JUMP_IF_FALSE       352  'to 1047'
              695  POP_TOP          

 L. 110       696  LOAD_GLOBAL          14  'isinstance'
              699  LOAD_FAST             0  'self'
              702  LOAD_ATTR             2  'opt'
              705  LOAD_CONST               'keyattr'
              708  BINARY_SUBSCR    
              709  LOAD_GLOBAL          17  'dict'
              712  CALL_FUNCTION_2       2  None
              715  JUMP_IF_FALSE       259  'to 977'
              718  POP_TOP          

 L. 112       719  LOAD_FAST             0  'self'
              722  LOAD_ATTR             2  'opt'
              725  LOAD_CONST               'keyattr'
              728  BINARY_SUBSCR    
              729  LOAD_FAST             0  'self'
              732  STORE_ATTR           18  'keyattr'

 L. 116       735  SETUP_LOOP          306  'to 1044'
              738  LOAD_FAST             0  'self'
              741  LOAD_ATTR             2  'opt'
              744  LOAD_CONST               'keyattr'
              747  BINARY_SUBSCR    
              748  GET_ITER         
              749  FOR_ITER            221  'to 973'
              752  STORE_FAST           11  'el'

 L. 117       755  LOAD_GLOBAL          10  're'
              758  LOAD_ATTR            11  'match'
              761  LOAD_CONST               '^(\\+|-)?(.*)$'
              764  LOAD_FAST             0  'self'
              767  LOAD_ATTR             2  'opt'
              770  LOAD_CONST               'keyattr'
              773  BINARY_SUBSCR    
              774  LOAD_FAST            11  'el'
              777  BINARY_SUBSCR    
              778  CALL_FUNCTION_2       2  None
              781  STORE_FAST            8  'm'

 L. 118       784  LOAD_FAST             8  'm'
              787  JUMP_IF_FALSE       165  'to 955'
              790  POP_TOP          

 L. 119       791  LOAD_FAST             8  'm'
              794  LOAD_ATTR            12  'group'
              797  LOAD_CONST               2
              800  CALL_FUNCTION_1       1  None
              803  LOAD_FAST             8  'm'
              806  LOAD_ATTR            12  'group'
              809  LOAD_CONST               1
              812  CALL_FUNCTION_1       1  None
              815  BUILD_LIST_2          2 
              818  LOAD_FAST             0  'self'
              821  LOAD_ATTR             2  'opt'
              824  LOAD_CONST               'keyattr'
              827  BINARY_SUBSCR    
              828  LOAD_FAST            11  'el'
              831  STORE_SUBSCR     

 L. 120       832  LOAD_FAST             0  'self'
              835  LOAD_ATTR             2  'opt'
              838  LOAD_CONST               'forcearray'
              841  BINARY_SUBSCR    
              842  LOAD_CONST               1
              845  COMPARE_OP            2  ==
              848  JUMP_IF_FALSE         7  'to 858'
            851_0  THEN                     859
              851  POP_TOP          

 L. 121       852  CONTINUE            749  'to 749'
              855  JUMP_FORWARD          1  'to 859'
            858_0  COME_FROM           848  '848'
              858  POP_TOP          
            859_0  COME_FROM           855  '855'

 L. 122       859  LOAD_GLOBAL          14  'isinstance'
              862  LOAD_FAST             0  'self'
              865  LOAD_ATTR             2  'opt'
              868  LOAD_CONST               'forcearray'
              871  BINARY_SUBSCR    
              872  LOAD_GLOBAL          17  'dict'
              875  CALL_FUNCTION_2       2  None
              878  JUMP_IF_FALSE        27  'to 908'
              881  POP_TOP          
              882  LOAD_FAST            11  'el'
              885  LOAD_FAST             0  'self'
              888  LOAD_ATTR             2  'opt'
              891  LOAD_CONST               'forcearray'
              894  BINARY_SUBSCR    
              895  COMPARE_OP            6  in
              898  JUMP_IF_FALSE         7  'to 908'
            901_0  THEN                     909
              901  POP_TOP          

 L. 123       902  CONTINUE            749  'to 749'
              905  JUMP_FORWARD          1  'to 909'
            908_0  COME_FROM           898  '898'
            908_1  COME_FROM           878  '878'
              908  POP_TOP          
            909_0  COME_FROM           905  '905'

 L. 124       909  LOAD_GLOBAL          19  'StrictMode'
              912  JUMP_IF_FALSE        36  'to 951'
              915  POP_TOP          
              916  LOAD_FAST             1  'dirn'
              919  LOAD_CONST               'in'
              922  COMPARE_OP            2  ==
              925  JUMP_IF_FALSE        23  'to 951'
              928  POP_TOP          

 L. 125       929  LOAD_GLOBAL          20  'ValueError'
              932  LOAD_CONST               '<%s> set in KeyAttr but not in ForceArray'
              935  LOAD_FAST            11  'el'
              938  BUILD_TUPLE_1         1 
              941  BINARY_MODULO    
              942  CALL_FUNCTION_1       1  None
              945  RAISE_VARARGS_1       1  None
              948  JUMP_ABSOLUTE       970  'to 970'
            951_0  COME_FROM           925  '925'
            951_1  COME_FROM           912  '912'
              951  POP_TOP          
              952  JUMP_BACK           749  'to 749'
            955_0  COME_FROM           787  '787'
              955  POP_TOP          

 L. 127       956  LOAD_FAST             0  'self'
              959  LOAD_ATTR             2  'opt'
              962  LOAD_CONST               'keyattr'
              965  BINARY_SUBSCR    
              966  LOAD_FAST            11  'el'
              969  DELETE_SUBSCR    
              970  JUMP_BACK           749  'to 749'
              973  POP_BLOCK        
            974_0  COME_FROM           735  '735'
              974  JUMP_ABSOLUTE      1091  'to 1091'
            977_0  COME_FROM           715  '715'
              977  POP_TOP          

 L. 128       978  LOAD_GLOBAL          14  'isinstance'
              981  LOAD_FAST             0  'self'
              984  LOAD_ATTR             2  'opt'
              987  LOAD_CONST               'keyattr'
              990  BINARY_SUBSCR    
              991  LOAD_GLOBAL          15  'list'
              994  CALL_FUNCTION_2       2  None
              997  JUMP_IF_FALSE        20  'to 1020'
             1000  POP_TOP          

 L. 129      1001  LOAD_FAST             0  'self'
             1004  LOAD_ATTR             2  'opt'
             1007  LOAD_CONST               'keyattr'
             1010  BINARY_SUBSCR    
             1011  LOAD_FAST             0  'self'
             1014  STORE_ATTR           18  'keyattr'
             1017  JUMP_ABSOLUTE      1091  'to 1091'
           1020_0  COME_FROM           997  '997'
             1020  POP_TOP          

 L. 131      1021  LOAD_FAST             0  'self'
             1024  LOAD_ATTR             2  'opt'
             1027  LOAD_CONST               'keyattr'
             1030  BINARY_SUBSCR    
             1031  BUILD_LIST_1          1 
             1034  LOAD_FAST             0  'self'
             1037  LOAD_ATTR             2  'opt'
             1040  LOAD_CONST               'keyattr'
             1043  STORE_SUBSCR     
             1044  JUMP_FORWARD         44  'to 1091'
           1047_0  COME_FROM           692  '692'
             1047  POP_TOP          

 L. 133      1048  LOAD_GLOBAL          19  'StrictMode'
             1051  JUMP_IF_FALSE        23  'to 1077'
           1054_0  THEN                     1078
             1054  POP_TOP          

 L. 134      1055  LOAD_GLOBAL          20  'ValueError'
             1058  LOAD_CONST               "No value specified for 'KeyAttr' option in call to XML%s()"
             1061  LOAD_FAST             1  'dirn'
             1064  BUILD_TUPLE_1         1 
             1067  BINARY_MODULO    
             1068  CALL_FUNCTION_1       1  None
             1071  RAISE_VARARGS_1       1  None
             1074  JUMP_FORWARD          1  'to 1078'
           1077_0  COME_FROM          1051  '1051'
             1077  POP_TOP          
           1078_0  COME_FROM          1074  '1074'

 L. 135      1078  LOAD_GLOBAL          21  'DefKeyAttr'
             1081  LOAD_FAST             0  'self'
             1084  LOAD_ATTR             2  'opt'
             1087  LOAD_CONST               'keyattr'
             1090  STORE_SUBSCR     
           1091_0  COME_FROM          1044  '1044'

 L. 138      1091  LOAD_GLOBAL          22  'hasattr'
             1094  LOAD_FAST             0  'self'
             1097  LOAD_ATTR             2  'opt'
             1100  LOAD_CONST               'grouptags'
             1103  CALL_FUNCTION_2       2  None
             1106  JUMP_IF_FALSE       112  'to 1221'
           1109_0  THEN                     1222
             1109  POP_TOP          

 L. 139      1110  LOAD_GLOBAL          14  'isinstance'
             1113  LOAD_FAST             0  'self'
             1116  LOAD_ATTR             2  'opt'
             1119  LOAD_CONST               'grouptags'
             1122  BINARY_SUBSCR    
             1123  LOAD_GLOBAL          17  'dict'
             1126  CALL_FUNCTION_2       2  None
             1129  JUMP_IF_TRUE         16  'to 1148'
           1132_0  THEN                     1149
             1132  POP_TOP          

 L. 140      1133  LOAD_GLOBAL          20  'ValueError'
             1136  LOAD_CONST               "Illegal value for 'GroupTags' option - expected a dictionary"
             1139  CALL_FUNCTION_1       1  None
             1142  RAISE_VARARGS_1       1  None
             1145  JUMP_FORWARD          1  'to 1149'
           1148_0  COME_FROM          1129  '1129'
             1148  POP_TOP          
           1149_0  COME_FROM          1145  '1145'

 L. 141      1149  SETUP_LOOP           70  'to 1222'
             1152  LOAD_FAST             0  'self'
             1155  LOAD_ATTR             2  'opt'
             1158  LOAD_CONST               'grouptags'
             1161  BINARY_SUBSCR    
             1162  GET_ITER         
             1163  FOR_ITER             51  'to 1217'
             1166  UNPACK_SEQUENCE_2     2 
             1169  STORE_FAST            4  'key'
             1172  STORE_FAST            6  'val'

 L. 142      1175  LOAD_FAST             4  'key'
             1178  LOAD_FAST             6  'val'
             1181  COMPARE_OP            2  ==
             1184  JUMP_IF_FALSE        26  'to 1213'
             1187  POP_TOP          

 L. 143      1188  LOAD_GLOBAL          20  'ValueError'
             1191  LOAD_CONST               "Bad value in GroupTags: '%s' => '%s'"
             1194  LOAD_FAST             4  'key'
             1197  LOAD_FAST             6  'val'
             1200  BUILD_TUPLE_2         2 
             1203  BINARY_MODULO    
             1204  CALL_FUNCTION_1       1  None
             1207  RAISE_VARARGS_1       1  None
             1210  JUMP_BACK          1163  'to 1163'
           1213_0  COME_FROM          1184  '1184'
             1213  POP_TOP          
             1214  JUMP_BACK          1163  'to 1163'
             1217  POP_BLOCK        
             1218  JUMP_FORWARD          1  'to 1222'
           1221_0  COME_FROM          1106  '1106'
             1221  POP_TOP          
           1222_0  COME_FROM          1149  '1149'

 L. 145      1222  LOAD_CONST               'valiables'
             1225  LOAD_FAST             0  'self'
             1228  LOAD_ATTR             2  'opt'
             1231  COMPARE_OP            6  in
             1234  JUMP_IF_FALSE        20  'to 1257'
             1237  POP_TOP          

 L. 146      1238  LOAD_FAST             0  'self'
             1241  LOAD_ATTR             2  'opt'
             1244  LOAD_CONST               'variables'
             1247  BINARY_SUBSCR    
             1248  LOAD_FAST             0  'self'
             1251  STORE_ATTR           23  '_var_values'
             1254  JUMP_FORWARD         30  'to 1287'
           1257_0  COME_FROM          1234  '1234'
             1257  POP_TOP          

 L. 147      1258  LOAD_CONST               'varattr'
             1261  LOAD_FAST             0  'self'
             1264  LOAD_ATTR             2  'opt'
             1267  COMPARE_OP            6  in
             1270  JUMP_IF_FALSE        13  'to 1286'
           1273_0  THEN                     1287
             1273  POP_TOP          

 L. 148      1274  BUILD_MAP             0 
             1277  LOAD_FAST             0  'self'
             1280  STORE_ATTR           23  '_var_values'
             1283  JUMP_FORWARD          1  'to 1287'
           1286_0  COME_FROM          1270  '1270'
             1286  POP_TOP          
           1287_0  COME_FROM          1283  '1283'
           1287_1  COME_FROM          1254  '1254'

Parse error at or near `JUMP_ABSOLUTE' instruction at offset 659

    def collapse(self, attr, tree):
        if 'noattr' in self.opt:
            attr = {}
        elif 'normalizespace' in self.opt and self.opt['normalizespace'] == 2:
            for (key, val) in attr.items():
                attr[key] = self.normalize_space(val)

        for (key, val) in zip(tree[::2], tree[1::2]):
            if isinstance(val, list):
                val = self.collapse(val[0], val[1:])
                if not val and 'suppressempty' in self.opt:
                    continue
            elif key == '0':
                if re.match('^\\s*$', val):
                    continue
                if hasattr(self, '_var_values'):
                    re.sub('\\$\\{(\\w+)\\}', lambda match: self.get_var(match.group(1)))
                if 'varattr' in self.opt:
                    var = self.opt['varattr']
                    if attr.has_key(var):
                        self.set_var(attr[var], val)
                if not len(attr) and val == tree[(-1)]:
                    return {self.opt['contentkey']: val} if 'forcecontent' in self.opt else val
                key = self.opt['contentkey']
            if attr.has_key(key):
                if isinstance(attr[key], list):
                    attr[key].append(val)
                else:
                    attr[key] = [
                     attr[key], val]
            elif val and isinstance(val, list):
                attr[key] = [
                 val]
            elif 'contentkey' in self.opt and key != self.opt['contentkey'] and (self.opt['forcearray'] == 1 or isinstance(self.opt['forcearray'], dict) and key in self.opt['forcearray']):
                attr[key] = [
                 val]
            else:
                attr[key] = val

        if self.opt.has_key('keyattr'):
            for (key, val) in attr.items():
                if val and isinstance(val, list):
                    attr[key] = self.array_to_hash(key, val)

        if self.opt.has_key('grouptags'):
            for (key, val) in attr.items():
                if not (isinstance(val, dict) and len(val) == 1):
                    continue
                if not self.opt['grouptags'].has_key(key):
                    continue
                (child_key, child_val) = val.popitem()
                if self.opt['grouptags'][key] == child_key:
                    attr[key] = child_val

        count = len(attr)
        if count == 1 and attr.has_key('anon') and isinstance(attr['anon'], list):
            return attr['anon']
        if not len(attr) and self.opt.has_key('suppressempty'):
            if self.opt['suppressempty'] == '':
                return ''
            return
        if self.opt.has_key('valueattr'):
            for (key, val) in attr.items():
                if not self.opt['valueattr'].has_key(key):
                    continue
                if not (isinstance(val, dict) and len(val) == 1):
                    continue
                k = val.keys()[0]
                if not k == self.opt['valueattr'][key]:
                    continue
                attr[key] = val[key]

        return attr

    def normalize_space(self, text):
        text = re.sub('\\s\\s+', ' ', text.strip())
        return text

    def array_to_hash(self, name, array):
        hash = {}
        if isinstance(self.opt['keyattr'], dict):
            if name not in self.opt['keyattr']:
                return array
            (key, flag) = self.opt['keyattr'][name]
            for item in array:
                if isinstance(item, dict) and key in item:
                    val = item[key]
                    if isinstance(val, list) or isinstance(val, dict):
                        if StrictMode:
                            raise ValueError("<%s> element has non-scalar '%s' key attribute" % (name, key))
                        warnings.warn("Warning: <%s> element has non-scalar '%s' key attribute" % (name, key))
                        return array
                    if self.opt['normalizespace'] == 1:
                        val = self.normalize_space(val)
                    hash[val] = item
                    if flag == '-':
                        hash[val]['-%s' % (key,)] = hash[val][key]
                    if flag != '+':
                        del hash[val][key]
                else:
                    if StrictMode:
                        raise ValueError('<%s> element has no %s key attribute' % (name, key))
                    warnings.warn("Warning: <%s> element has no '%s' key attribute" % (name, key))
                    return array

        for item in array:
            next = False
            if not isinstance(item, dict):
                return array
            for key in self.opt['keyattr']:
                if key in item:
                    val = item[key]
                    if isinstance(val, dict) or isinstance(val, list):
                        return array
                    if 'normalizespace' in self.opt and self.opt['normalizespace'] == 1:
                        val = self.normalize_space(val)
                    hash[val] = item
                    del hash[val][key]
                    next = True
                    break

            if next:
                continue
            return array

        if 'collapseagain' in self.opt:
            hash = self.collapse_content(hash)
        return hash

    def collapse_content(self, hash):
        contentkey = self.opt['contentkey']
        for val in hash.values():
            if not (isinstance(val, dict) and len(val) == 1 and contentkey in val):
                return hash

        for key in hash:
            hash[key] = hash[key][contentkey]

        return hash

    def XMLout(self, tree, options={}):
        self.handle_options('out', options)
        if isinstance(tree, list):
            tree = {'anon': tree}
        if 'keeproot' in self.opt and self.opt['keeproot']:
            keys = tree.keys()
            if len(tree) == 1:
                tree = tree[keys[0]]
                self.opt['rootname'] = keys[0]
        elif self.opt['rootname'] == '':
            if isinstance(tree, dict):
                treesave = tree
                tree = {}
                for key in treesave:
                    if isinstance(treesave[key], dict) or isinstance(treesave[key], list):
                        tree[key] = treesave[key]
                    else:
                        tree[key] = [
                         treesave[key]]

        self._ancestors = []
        xml = self.value_to_xml(tree, self.opt['rootname'], '')
        del self._ancestors
        if 'xmldecl' in self.opt and self.opt['xmldecl']:
            xml = self.opt['xmldecl'] + '\n' + xml
        return xml

    def value_to_xml(self, tree, name, indent):
        named = len(name) and 1 or 0
        nl = '\n'
        is_root = len(indent) == 0 and 1 or 0
        if 'noindent' in self.opt and self.opt['noindent']:
            indent = nl = ''
        if isinstance(tree, list) or isinstance(tree, dict):
            if len([ elem for elem in self._ancestors if elem == tree ]):
                raise ValueError('circular data structures not supported')
            self._ancestors.append(tree)
        elif named:
            content = tree if 'noescape' in self.opt else self.escape_value(tree)
            line = '%(indent)s<%(name)s>%(content)s</%(name)s>%(nl)s' % locals()
            return line
        else:
            return str(tree) + nl
        if isinstance(tree, dict) and len(tree) and self.opt['keyattr'] and not is_root:
            tree = self.hash_to_array(name, tree)
        result = []
        if isinstance(tree, dict):
            if 'grouptags' in self.opt and self.opt['grouptags']:
                tree = tree.copy()
                for (key, val) in tree.items():
                    if key in self.opt['grouptags']:
                        tree[key] = {self.opt['grouptags'][key]: val}

            nsdecls = ''
            default_ns_url = ''
            nested = []
            text_content = None
            if named:
                result.extend([indent, '<', name, nsdecls])
            if len(tree):
                first_arg = 1
                for key in self.sorted_keys(name, tree):
                    value = tree[key]
                    if not value:
                        if key[0] == '-':
                            continue
                        if key == self.opt['contentkey']:
                            text_content = ''
                        else:
                            value = ''
                    if not isinstance(value, dict) and not isinstance(value, list):
                        if 'valueattr' in self.opt and self.opt['valueattr']:
                            if key in self.opt['valueattr'] and self.opt['valueattr'][key]:
                                value = {self.opt['valueattr'][key]: value}
                    if isinstance(value, dict) or isinstance(value, list) or 'noattr' in self.opt:
                        nested.append(self.value_to_xml(value, key, indent + '  '))
                    else:
                        if not ('noescape' in self.opt and self.opt['noescape']):
                            value = self.escape_value(value)
                        if key == self.opt['contentkey']:
                            text_content = value
                        else:
                            result.extend([' ', key, '="', value, '"'])
                            first_arg = 0

            else:
                text_content = ''
            if nested or text_content is not None:
                if named:
                    result.append('>')
                    if text_content is not None:
                        result.append(text_content)
                        if len(nested):
                            nested[0].lstrip()
                    else:
                        result.append(nl)
                    if len(nested):
                        result.extend(nested)
                        result.append(indent)
                    result.extend(['</', name, '>', nl])
                else:
                    result.extend(nested)
            else:
                result.extend([' />', nl])
        elif isinstance(tree, list):
            for value in tree:
                if not isinstance(value, dict) and not isinstance(value, list):
                    result.extend([indent, '<', name, '>',
                     value if 'noescape' in self.opt and self.opt['noescape'] else self.escape_value(value),
                     '</', name, '>' + nl])
                elif isinstance(value, dict):
                    result.append(self.value_to_xml(value, name, indent))
                else:
                    result.extend([indent, '<', name, '>' + nl,
                     self.value_to_xml(value, 'anon', indent + '  '),
                     indent, '</', name, '>' + nl])

        else:
            raise ValueError("Can't encode a value of type: " + tree.__class__)
        if isinstance(tree, dict) or isinstance(tree, list):
            self._ancestors.pop()
        return ('').join(result)

    def sorted_keys(self, name, tree):
        hash = tree.copy()
        keyattr = self.opt['keyattr']
        key = []
        if isinstance(tree, dict):
            if name in keyattr and keyattr[name][0] in hash:
                key.append(keyattr[name][0])
                del hash[keyattr[name][0]]
        elif isinstance(tree, list):
            for item in keyattr:
                if item in hash:
                    key.append(item)
                    del hash[item]
                    break

        if len(hash) > 0:
            tmp = hash.keys()
            tmp.sort()
            key.extend(tmp)
        return key

    def escape_value(self, data):
        if data is None:
            return ''
        data = str(data)
        data = data.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')
        return data

    def hash_to_array(self, parent, hash):
        array = []
        for key in hash:
            value = hash[key]
            if not isinstance(value, dict):
                return hash
            if isinstance(self.opt['keyattr'], dict):
                if parent not in self.opt['keyattr']:
                    return hash
                array.append(self.copy_hash(value, [self.opt['keyattr'][parent][0], key]))
            else:
                array.append(self.copy_hash(value, [self.opt['keyattr'][0], key]))

        return array

    def copy_hash(self, orig, extra):
        result = orig.copy()
        result.update(dict(zip(extra[::2], extra[1::2])))
        return result

    def startDocument(self):
        self.lists = []
        self.curlist = self.tree = []

    def startElement(self, name, attrs):
        attributes = {}
        for attr in attrs.items():
            attributes[attr[0]] = attr[1]

        newlist = [
         attributes]
        self.curlist.extend([name, newlist])
        self.lists.append(self.curlist)
        self.curlist = newlist

    def characters(self, content):
        text = content
        pos = len(self.curlist) - 1
        if pos > 0 and self.curlist[(pos - 1)] == '0':
            self.curlist[pos] += text
        else:
            self.curlist.extend(['0', text])

    def endElement(self, name):
        self.curlist = self.lists.pop()

    def endDocument(self):
        del self.curlist
        del self.lists
        tree = self.tree
        del self.tree
        if 'keeproot' in self.opt:
            tree = self.collapse({}, tree)
        else:
            tree = self.collapse(tree[1][0], tree[1][1:])
        self.tree = tree


if __name__ == '__main__':
    xml = '\n    <opt>\n      <car license="LW1804" make="GM"   id="2">\n        <option key="1" pn="9926543-1167" desc="Steering Wheel"/>\n      </car>\n    </opt>\n    '
    opt = XMLin(xml, {'keyattr': {'car': 'license', 'option': 'pn'}, 'contentkey': '-content'})
    print opt
    hash1 = {'one': 1, 'two': 'II', 'three': '...'}
    xml = XMLout(hash1)
    tree = {'array': ['one', 'two', 'three']}
    expect = '\n    <root>\n      <array>one</array>\n      <array>two</array>\n      <array>three</array>\n    </root>\n    '
    xml = XMLout(tree)
    tree = {'country': {'England': {'capital': 'London'}, 'France': {'capital': 'Paris'}, 'Turkey': {'capital': 'Istanbul'}}}
    expected = '\n^\\s*<(\\w+)\\s*>\\s*\n(\n   <country(\\s*fullname="Turkey"  |\\s*capital="Istanbul" ){2}\\s*/>\\s*\n  |<country(\\s*fullname="France"  |\\s*capital="Paris"    ){2}\\s*/>\\s*\n  |<country(\\s*fullname="England" |\\s*capital="London"   ){2}\\s*/>\\s*\n){3}\n</\\1>\\s*$\n'
    xml = XMLout(tree, {'keyattr': {'country': 'fullname'}})
    xml = XMLout(tree, {'keyattr': {'country': '+fullname'}})
    tree = {'one': 1, 'content': 'text'}
    xml = XMLout(tree)