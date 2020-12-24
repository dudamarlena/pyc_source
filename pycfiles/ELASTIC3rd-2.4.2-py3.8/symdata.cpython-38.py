# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\elastic3rd\symmetry\symdata.py
# Compiled at: 2019-07-21 09:57:36
# Size of source mod 2**32: 11962 bytes
import numpy as np

def coef_crystal--- This code section failed: ---

 L.  11         0  LOAD_FAST                'CrystalType'
                2  LOAD_METHOD              lower
                4  CALL_METHOD_0         0  ''
                6  STORE_FAST               'CrystalType'

 L.  12         8  LOAD_FAST                'Ord'
               10  LOAD_CONST               2
               12  COMPARE_OP               ==
            14_16  POP_JUMP_IF_FALSE   846  'to 846'

 L.  13        18  LOAD_CONST               0.5
               20  LOAD_CONST               -0.5
               22  BUILD_LIST_2          2 
               24  STORE_FAST               'A'

 L.  14        26  LOAD_FAST                'CrystalType'
               28  LOAD_STR                 'triclinic'
               30  COMPARE_OP               ==
               32  POP_JUMP_IF_TRUE     42  'to 42'
               34  LOAD_FAST                'CrystalType'
               36  LOAD_STR                 'n'
               38  COMPARE_OP               ==
               40  POP_JUMP_IF_FALSE    92  'to 92'
             42_0  COME_FROM            32  '32'

 L.  15        42  LOAD_CONST               1
               44  LOAD_CONST               1
               46  LOAD_CONST               1
               48  LOAD_CONST               1
               50  LOAD_CONST               1
               52  LOAD_CONST               1
               54  LOAD_CONST               1
               56  LOAD_CONST               1
               58  LOAD_CONST               1
               60  LOAD_CONST               1
               62  LOAD_CONST               1
               64  LOAD_CONST               1
               66  LOAD_CONST               1
               68  LOAD_CONST               1
               70  LOAD_CONST               1
               72  LOAD_CONST               1
               74  LOAD_CONST               1
               76  LOAD_CONST               1
               78  LOAD_CONST               1
               80  LOAD_CONST               1
               82  LOAD_CONST               1
               84  BUILD_LIST_21        21 
               86  STORE_FAST               'CoefCoef'
            88_90  JUMP_ABSOLUTE      2650  'to 2650'
             92_0  COME_FROM            40  '40'

 L.  16        92  LOAD_FAST                'CrystalType'
               94  LOAD_STR                 'monoclinic'
               96  COMPARE_OP               ==
               98  POP_JUMP_IF_TRUE    108  'to 108'
              100  LOAD_FAST                'CrystalType'
              102  LOAD_STR                 'm'
              104  COMPARE_OP               ==
              106  POP_JUMP_IF_FALSE   158  'to 158'
            108_0  COME_FROM            98  '98'

 L.  17       108  LOAD_CONST               1
              110  LOAD_CONST               1
              112  LOAD_CONST               1
              114  LOAD_CONST               0
              116  LOAD_CONST               1
              118  LOAD_CONST               0
              120  LOAD_CONST               1
              122  LOAD_CONST               1
              124  LOAD_CONST               0
              126  LOAD_CONST               1
              128  LOAD_CONST               0
              130  LOAD_CONST               1
              132  LOAD_CONST               0
              134  LOAD_CONST               1
              136  LOAD_CONST               0
              138  LOAD_CONST               1
              140  LOAD_CONST               0
              142  LOAD_CONST               1
              144  LOAD_CONST               1
              146  LOAD_CONST               0
              148  LOAD_CONST               1
              150  BUILD_LIST_21        21 
              152  STORE_FAST               'CoefCoef'
          154_156  JUMP_ABSOLUTE      2650  'to 2650'
            158_0  COME_FROM           106  '106'

 L.  18       158  LOAD_FAST                'CrystalType'
              160  LOAD_STR                 'orthorhombic'
              162  COMPARE_OP               ==
              164  POP_JUMP_IF_TRUE    174  'to 174'
              166  LOAD_FAST                'CrystalType'
              168  LOAD_STR                 'o'
              170  COMPARE_OP               ==
              172  POP_JUMP_IF_FALSE   224  'to 224'
            174_0  COME_FROM           164  '164'

 L.  19       174  LOAD_CONST               1
              176  LOAD_CONST               1
              178  LOAD_CONST               1
              180  LOAD_CONST               0
              182  LOAD_CONST               0
              184  LOAD_CONST               0
              186  LOAD_CONST               1
              188  LOAD_CONST               1
              190  LOAD_CONST               0
              192  LOAD_CONST               0
              194  LOAD_CONST               0
              196  LOAD_CONST               1
              198  LOAD_CONST               0
              200  LOAD_CONST               0
              202  LOAD_CONST               0
              204  LOAD_CONST               1
              206  LOAD_CONST               0
              208  LOAD_CONST               0
              210  LOAD_CONST               1
              212  LOAD_CONST               0
              214  LOAD_CONST               1
              216  BUILD_LIST_21        21 
              218  STORE_FAST               'CoefCoef'
          220_222  JUMP_ABSOLUTE      2650  'to 2650'
            224_0  COME_FROM           172  '172'

 L.  20       224  LOAD_FAST                'CrystalType'
              226  LOAD_STR                 'tetragonal2'
              228  COMPARE_OP               ==
              230  POP_JUMP_IF_TRUE    242  'to 242'
              232  LOAD_FAST                'CrystalType'
              234  LOAD_STR                 't2'
              236  COMPARE_OP               ==
          238_240  POP_JUMP_IF_FALSE   292  'to 292'
            242_0  COME_FROM           230  '230'

 L.  21       242  LOAD_CONST               1
              244  LOAD_CONST               1
              246  LOAD_CONST               1
              248  LOAD_CONST               0
              250  LOAD_CONST               0
              252  LOAD_CONST               1
              254  LOAD_CONST               1
              256  LOAD_CONST               1
              258  LOAD_CONST               0
              260  LOAD_CONST               0
              262  LOAD_CONST               -1
              264  LOAD_CONST               1
              266  LOAD_CONST               0
              268  LOAD_CONST               0
              270  LOAD_CONST               0
              272  LOAD_CONST               1
              274  LOAD_CONST               0
              276  LOAD_CONST               0
              278  LOAD_CONST               1
              280  LOAD_CONST               0
              282  LOAD_CONST               1
              284  BUILD_LIST_21        21 
              286  STORE_FAST               'CoefCoef'
          288_290  JUMP_ABSOLUTE      2650  'to 2650'
            292_0  COME_FROM           238  '238'

 L.  22       292  LOAD_FAST                'CrystalType'
              294  LOAD_STR                 'tetragonal1'
              296  COMPARE_OP               ==
          298_300  POP_JUMP_IF_TRUE    312  'to 312'
              302  LOAD_FAST                'CrystalType'
              304  LOAD_STR                 't1'
              306  COMPARE_OP               ==
          308_310  POP_JUMP_IF_FALSE   362  'to 362'
            312_0  COME_FROM           298  '298'

 L.  23       312  LOAD_CONST               1
              314  LOAD_CONST               1
              316  LOAD_CONST               1
              318  LOAD_CONST               0
              320  LOAD_CONST               0
              322  LOAD_CONST               0
              324  LOAD_CONST               1
              326  LOAD_CONST               1
              328  LOAD_CONST               0
              330  LOAD_CONST               0
              332  LOAD_CONST               0
              334  LOAD_CONST               1
              336  LOAD_CONST               0
              338  LOAD_CONST               0
              340  LOAD_CONST               0
              342  LOAD_CONST               1
              344  LOAD_CONST               0
              346  LOAD_CONST               0
              348  LOAD_CONST               1
              350  LOAD_CONST               0
              352  LOAD_CONST               1
              354  BUILD_LIST_21        21 
              356  STORE_FAST               'CoefCoef'
          358_360  JUMP_ABSOLUTE      2650  'to 2650'
            362_0  COME_FROM           308  '308'

 L.  24       362  LOAD_FAST                'CrystalType'
              364  LOAD_STR                 'rhombohedral2'
              366  COMPARE_OP               ==
          368_370  POP_JUMP_IF_TRUE    382  'to 382'
              372  LOAD_FAST                'CrystalType'
              374  LOAD_STR                 'r2'
              376  COMPARE_OP               ==
          378_380  POP_JUMP_IF_FALSE   432  'to 432'
            382_0  COME_FROM           368  '368'

 L.  25       382  LOAD_CONST               1
              384  LOAD_CONST               1
              386  LOAD_CONST               1
              388  LOAD_CONST               1
              390  LOAD_CONST               1
              392  LOAD_CONST               0
              394  LOAD_CONST               1
              396  LOAD_CONST               1
              398  LOAD_CONST               -1
              400  LOAD_CONST               -1
              402  LOAD_CONST               0
              404  LOAD_CONST               1
              406  LOAD_CONST               0
              408  LOAD_CONST               0
              410  LOAD_CONST               0
              412  LOAD_CONST               1
              414  LOAD_CONST               0
              416  LOAD_CONST               -1
              418  LOAD_CONST               1
              420  LOAD_CONST               1
              422  LOAD_FAST                'A'
              424  BUILD_LIST_21        21 
              426  STORE_FAST               'CoefCoef'
          428_430  JUMP_ABSOLUTE      2650  'to 2650'
            432_0  COME_FROM           378  '378'

 L.  26       432  LOAD_FAST                'CrystalType'
              434  LOAD_STR                 'rhombohedral1'
              436  COMPARE_OP               ==
          438_440  POP_JUMP_IF_TRUE    452  'to 452'
              442  LOAD_FAST                'CrystalType'
              444  LOAD_STR                 'r1'
              446  COMPARE_OP               ==
          448_450  POP_JUMP_IF_FALSE   502  'to 502'
            452_0  COME_FROM           438  '438'

 L.  27       452  LOAD_CONST               1
              454  LOAD_CONST               1
              456  LOAD_CONST               1
              458  LOAD_CONST               1
              460  LOAD_CONST               0
              462  LOAD_CONST               0
              464  LOAD_CONST               1
              466  LOAD_CONST               1
              468  LOAD_CONST               -1
              470  LOAD_CONST               0
              472  LOAD_CONST               0
              474  LOAD_CONST               1
              476  LOAD_CONST               0
              478  LOAD_CONST               0
              480  LOAD_CONST               0
              482  LOAD_CONST               1
              484  LOAD_CONST               0
              486  LOAD_CONST               0
              488  LOAD_CONST               1
              490  LOAD_CONST               1
              492  LOAD_FAST                'A'
              494  BUILD_LIST_21        21 
              496  STORE_FAST               'CoefCoef'
          498_500  JUMP_ABSOLUTE      2650  'to 2650'
            502_0  COME_FROM           448  '448'

 L.  28       502  LOAD_FAST                'CrystalType'
              504  LOAD_STR                 'hexagonal2'
              506  COMPARE_OP               ==
          508_510  POP_JUMP_IF_TRUE    522  'to 522'
              512  LOAD_FAST                'CrystalType'
              514  LOAD_STR                 'h2'
              516  COMPARE_OP               ==
          518_520  POP_JUMP_IF_FALSE   572  'to 572'
            522_0  COME_FROM           508  '508'

 L.  29       522  LOAD_CONST               1
              524  LOAD_CONST               1
              526  LOAD_CONST               1
              528  LOAD_CONST               0
              530  LOAD_CONST               0
              532  LOAD_CONST               0
              534  LOAD_CONST               1
              536  LOAD_CONST               1
              538  LOAD_CONST               0
              540  LOAD_CONST               0
              542  LOAD_CONST               0
              544  LOAD_CONST               1
              546  LOAD_CONST               0
              548  LOAD_CONST               0
              550  LOAD_CONST               0
              552  LOAD_CONST               1
              554  LOAD_CONST               0
              556  LOAD_CONST               0
              558  LOAD_CONST               1
              560  LOAD_CONST               0
              562  LOAD_FAST                'A'
              564  BUILD_LIST_21        21 
              566  STORE_FAST               'CoefCoef'
          568_570  JUMP_ABSOLUTE      2650  'to 2650'
            572_0  COME_FROM           518  '518'

 L.  30       572  LOAD_FAST                'CrystalType'
              574  LOAD_STR                 'hexagonal1'
              576  COMPARE_OP               ==
          578_580  POP_JUMP_IF_TRUE    592  'to 592'
              582  LOAD_FAST                'CrystalType'
              584  LOAD_STR                 'h1'
              586  COMPARE_OP               ==
          588_590  POP_JUMP_IF_FALSE   640  'to 640'
            592_0  COME_FROM           578  '578'

 L.  31       592  LOAD_CONST               1
              594  LOAD_CONST               1
              596  LOAD_CONST               1
              598  LOAD_CONST               0
              600  LOAD_CONST               0
              602  LOAD_CONST               0
              604  LOAD_CONST               1
              606  LOAD_CONST               1
              608  LOAD_CONST               0
              610  LOAD_CONST               0
              612  LOAD_CONST               0
              614  LOAD_CONST               1
              616  LOAD_CONST               0
              618  LOAD_CONST               0
              620  LOAD_CONST               0
              622  LOAD_CONST               1
              624  LOAD_CONST               0
              626  LOAD_CONST               0
              628  LOAD_CONST               1
              630  LOAD_CONST               0
              632  LOAD_FAST                'A'
              634  BUILD_LIST_21        21 
              636  STORE_FAST               'CoefCoef'
              638  JUMP_FORWARD       2650  'to 2650'
            640_0  COME_FROM           588  '588'

 L.  32       640  LOAD_FAST                'CrystalType'
              642  LOAD_STR                 'cubic2'
              644  COMPARE_OP               ==
          646_648  POP_JUMP_IF_TRUE    660  'to 660'
              650  LOAD_FAST                'CrystalType'
              652  LOAD_STR                 'c2'
              654  COMPARE_OP               ==
          656_658  POP_JUMP_IF_FALSE   708  'to 708'
            660_0  COME_FROM           646  '646'

 L.  33       660  LOAD_CONST               1
              662  LOAD_CONST               1
              664  LOAD_CONST               1
              666  LOAD_CONST               0
              668  LOAD_CONST               0
              670  LOAD_CONST               0
              672  LOAD_CONST               1
              674  LOAD_CONST               1
              676  LOAD_CONST               0
              678  LOAD_CONST               0
              680  LOAD_CONST               0
              682  LOAD_CONST               1
              684  LOAD_CONST               0
              686  LOAD_CONST               0
              688  LOAD_CONST               0
              690  LOAD_CONST               1
              692  LOAD_CONST               0
              694  LOAD_CONST               0
              696  LOAD_CONST               1
              698  LOAD_CONST               0
              700  LOAD_CONST               1
              702  BUILD_LIST_21        21 
              704  STORE_FAST               'CoefCoef'
              706  JUMP_FORWARD       2650  'to 2650'
            708_0  COME_FROM           656  '656'

 L.  34       708  LOAD_FAST                'CrystalType'
              710  LOAD_STR                 'cubic1'
              712  COMPARE_OP               ==
          714_716  POP_JUMP_IF_TRUE    728  'to 728'
              718  LOAD_FAST                'CrystalType'
              720  LOAD_STR                 'c1'
              722  COMPARE_OP               ==
          724_726  POP_JUMP_IF_FALSE   776  'to 776'
            728_0  COME_FROM           714  '714'

 L.  35       728  LOAD_CONST               1
              730  LOAD_CONST               1
              732  LOAD_CONST               1
              734  LOAD_CONST               0
              736  LOAD_CONST               0
              738  LOAD_CONST               0
              740  LOAD_CONST               1
              742  LOAD_CONST               1
              744  LOAD_CONST               0
              746  LOAD_CONST               0
              748  LOAD_CONST               0
              750  LOAD_CONST               1
              752  LOAD_CONST               0
              754  LOAD_CONST               0
              756  LOAD_CONST               0
              758  LOAD_CONST               1
              760  LOAD_CONST               0
              762  LOAD_CONST               0
              764  LOAD_CONST               1
              766  LOAD_CONST               0
              768  LOAD_CONST               1
              770  BUILD_LIST_21        21 
              772  STORE_FAST               'CoefCoef'
              774  JUMP_FORWARD       2650  'to 2650'
            776_0  COME_FROM           724  '724'

 L.  36       776  LOAD_FAST                'CrystalType'
              778  LOAD_STR                 'isotropic'
              780  COMPARE_OP               ==
          782_784  POP_JUMP_IF_TRUE    796  'to 796'
              786  LOAD_FAST                'CrystalType'
              788  LOAD_STR                 'i'
              790  COMPARE_OP               ==
          792_794  POP_JUMP_IF_FALSE  2650  'to 2650'
            796_0  COME_FROM           782  '782'

 L.  37       796  LOAD_CONST               1
              798  LOAD_CONST               1
              800  LOAD_CONST               1
              802  LOAD_CONST               0
              804  LOAD_CONST               0
              806  LOAD_CONST               0
              808  LOAD_CONST               1
              810  LOAD_CONST               1
              812  LOAD_CONST               0
              814  LOAD_CONST               0
              816  LOAD_CONST               0
              818  LOAD_CONST               1
              820  LOAD_CONST               0
              822  LOAD_CONST               0
              824  LOAD_CONST               0
              826  LOAD_FAST                'A'
              828  LOAD_CONST               0
              830  LOAD_CONST               0
              832  LOAD_FAST                'A'
              834  LOAD_CONST               0
              836  LOAD_FAST                'A'
              838  BUILD_LIST_21        21 
              840  STORE_FAST               'CoefCoef'
          842_844  JUMP_FORWARD       2650  'to 2650'
            846_0  COME_FROM            14  '14'

 L.  38       846  LOAD_FAST                'Ord'
              848  LOAD_CONST               3
              850  COMPARE_OP               ==
          852_854  POP_JUMP_IF_FALSE  2650  'to 2650'

 L.  39       856  LOAD_CONST               1
              858  LOAD_CONST               1
              860  LOAD_CONST               -1
              862  BUILD_LIST_3          3 
              864  STORE_FAST               'A'

 L.  39       866  LOAD_CONST               -0.5
              868  LOAD_CONST               -1.5
              870  BUILD_LIST_2          2 
              872  STORE_FAST               'B'

 L.  39       874  LOAD_CONST               0.5
              876  LOAD_CONST               1.5
              878  BUILD_LIST_2          2 
              880  STORE_FAST               'C'

 L.  39       882  LOAD_CONST               -0.5
              884  LOAD_CONST               -0.25
              886  LOAD_CONST               0.75
              888  BUILD_LIST_3          3 
              890  STORE_FAST               'D'

 L.  39       892  LOAD_CONST               -1
              894  LOAD_CONST               -2
              896  BUILD_LIST_2          2 
              898  STORE_FAST               'E'

 L.  39       900  LOAD_CONST               -1
              902  LOAD_CONST               -2
              904  BUILD_LIST_2          2 
              906  STORE_FAST               'F'

 L.  40       908  LOAD_CONST               -0.5
              910  LOAD_CONST               0.5
              912  BUILD_LIST_2          2 
              914  STORE_FAST               'G'

 L.  40       916  LOAD_CONST               0.5
              918  LOAD_CONST               -0.5
              920  BUILD_LIST_2          2 
              922  STORE_FAST               'H'

 L.  40       924  LOAD_CONST               0.5
              926  LOAD_CONST               -0.25
              928  LOAD_CONST               -0.25
              930  BUILD_LIST_3          3 
              932  STORE_FAST               'I'

 L.  40       934  LOAD_CONST               0.5
              936  LOAD_CONST               -0.5
              938  BUILD_LIST_2          2 
              940  STORE_FAST               'J'

 L.  40       942  LOAD_CONST               -0.5
              944  LOAD_CONST               0.5
              946  BUILD_LIST_2          2 
              948  STORE_FAST               'K'

 L.  41       950  LOAD_CONST               0.5
              952  LOAD_CONST               -0.5
              954  BUILD_LIST_2          2 
              956  STORE_FAST               'L'

 L.  41       958  LOAD_CONST               0.25
              960  LOAD_CONST               -0.25
              962  BUILD_LIST_2          2 
              964  STORE_FAST               'M'

 L.  41       966  LOAD_CONST               0.125
              968  LOAD_CONST               -0.375
              970  LOAD_CONST               0.25
              972  BUILD_LIST_3          3 
              974  STORE_FAST               'N'

 L.  42       976  LOAD_FAST                'CrystalType'
              978  LOAD_STR                 'triclinic'
              980  COMPARE_OP               ==
          982_984  POP_JUMP_IF_TRUE    996  'to 996'
              986  LOAD_FAST                'CrystalType'
              988  LOAD_STR                 'n'
              990  COMPARE_OP               ==
          992_994  POP_JUMP_IF_FALSE  1116  'to 1116'
            996_0  COME_FROM           982  '982'

 L.  43       996  LOAD_CONST               1
              998  LOAD_CONST               1
             1000  LOAD_CONST               1
             1002  LOAD_CONST               1
             1004  LOAD_CONST               1
             1006  LOAD_CONST               1
             1008  LOAD_CONST               1
             1010  LOAD_CONST               1
             1012  LOAD_CONST               1
             1014  LOAD_CONST               1
             1016  LOAD_CONST               1
             1018  LOAD_CONST               1
             1020  LOAD_CONST               1
             1022  LOAD_CONST               1
             1024  LOAD_CONST               1
             1026  LOAD_CONST               1
             1028  LOAD_CONST               1
             1030  LOAD_CONST               1
             1032  LOAD_CONST               1
             1034  LOAD_CONST               1
             1036  LOAD_CONST               1
             1038  LOAD_CONST               1
             1040  LOAD_CONST               1
             1042  LOAD_CONST               1
             1044  LOAD_CONST               1
             1046  LOAD_CONST               1
             1048  LOAD_CONST               1
             1050  LOAD_CONST               1
             1052  LOAD_CONST               1
             1054  LOAD_CONST               1

 L.  44      1056  LOAD_CONST               1

 L.  44      1058  LOAD_CONST               1

 L.  44      1060  LOAD_CONST               1

 L.  44      1062  LOAD_CONST               1

 L.  44      1064  LOAD_CONST               1

 L.  44      1066  LOAD_CONST               1

 L.  44      1068  LOAD_CONST               1

 L.  44      1070  LOAD_CONST               1

 L.  44      1072  LOAD_CONST               1

 L.  44      1074  LOAD_CONST               1

 L.  44      1076  LOAD_CONST               1

 L.  44      1078  LOAD_CONST               1

 L.  44      1080  LOAD_CONST               1

 L.  44      1082  LOAD_CONST               1

 L.  44      1084  LOAD_CONST               1

 L.  44      1086  LOAD_CONST               1

 L.  44      1088  LOAD_CONST               1

 L.  44      1090  LOAD_CONST               1

 L.  44      1092  LOAD_CONST               1

 L.  44      1094  LOAD_CONST               1

 L.  44      1096  LOAD_CONST               1

 L.  44      1098  LOAD_CONST               1

 L.  44      1100  LOAD_CONST               1

 L.  44      1102  LOAD_CONST               1

 L.  44      1104  LOAD_CONST               1

 L.  44      1106  LOAD_CONST               1

 L.  43      1108  BUILD_LIST_56        56 
             1110  STORE_FAST               'CoefCoef'
         1112_1114  JUMP_FORWARD       2650  'to 2650'
           1116_0  COME_FROM           992  '992'

 L.  45      1116  LOAD_FAST                'CrystalType'
             1118  LOAD_STR                 'monoclinic'
             1120  COMPARE_OP               ==
         1122_1124  POP_JUMP_IF_TRUE   1136  'to 1136'
             1126  LOAD_FAST                'CrystalType'
             1128  LOAD_STR                 'm'
             1130  COMPARE_OP               ==
         1132_1134  POP_JUMP_IF_FALSE  1256  'to 1256'
           1136_0  COME_FROM          1122  '1122'

 L.  46      1136  LOAD_CONST               1
             1138  LOAD_CONST               1
             1140  LOAD_CONST               1
             1142  LOAD_CONST               0
             1144  LOAD_CONST               1
             1146  LOAD_CONST               0
             1148  LOAD_CONST               1
             1150  LOAD_CONST               1
             1152  LOAD_CONST               0
             1154  LOAD_CONST               1
             1156  LOAD_CONST               0
             1158  LOAD_CONST               1
             1160  LOAD_CONST               0
             1162  LOAD_CONST               1
             1164  LOAD_CONST               0
             1166  LOAD_CONST               1
             1168  LOAD_CONST               0
             1170  LOAD_CONST               1
             1172  LOAD_CONST               1
             1174  LOAD_CONST               0
             1176  LOAD_CONST               1
             1178  LOAD_CONST               1
             1180  LOAD_CONST               1
             1182  LOAD_CONST               0
             1184  LOAD_CONST               1
             1186  LOAD_CONST               0
             1188  LOAD_CONST               1
             1190  LOAD_CONST               0
             1192  LOAD_CONST               1
             1194  LOAD_CONST               0

 L.  47      1196  LOAD_CONST               1

 L.  47      1198  LOAD_CONST               0

 L.  47      1200  LOAD_CONST               1

 L.  47      1202  LOAD_CONST               1

 L.  47      1204  LOAD_CONST               0

 L.  47      1206  LOAD_CONST               1

 L.  47      1208  LOAD_CONST               1

 L.  47      1210  LOAD_CONST               0

 L.  47      1212  LOAD_CONST               1

 L.  47      1214  LOAD_CONST               0

 L.  47      1216  LOAD_CONST               1

 L.  47      1218  LOAD_CONST               0

 L.  47      1220  LOAD_CONST               1

 L.  47      1222  LOAD_CONST               1

 L.  47      1224  LOAD_CONST               0

 L.  47      1226  LOAD_CONST               1

 L.  47      1228  LOAD_CONST               0

 L.  47      1230  LOAD_CONST               1

 L.  47      1232  LOAD_CONST               0

 L.  47      1234  LOAD_CONST               0

 L.  47      1236  LOAD_CONST               1

 L.  47      1238  LOAD_CONST               0

 L.  47      1240  LOAD_CONST               1

 L.  47      1242  LOAD_CONST               0

 L.  47      1244  LOAD_CONST               1

 L.  47      1246  LOAD_CONST               0

 L.  46      1248  BUILD_LIST_56        56 
             1250  STORE_FAST               'CoefCoef'
         1252_1254  JUMP_FORWARD       2650  'to 2650'
           1256_0  COME_FROM          1132  '1132'

 L.  48      1256  LOAD_FAST                'CrystalType'
             1258  LOAD_STR                 'orthorhombic'
             1260  COMPARE_OP               ==
         1262_1264  POP_JUMP_IF_TRUE   1276  'to 1276'
             1266  LOAD_FAST                'CrystalType'
             1268  LOAD_STR                 'o'
             1270  COMPARE_OP               ==
         1272_1274  POP_JUMP_IF_FALSE  1396  'to 1396'
           1276_0  COME_FROM          1262  '1262'

 L.  49      1276  LOAD_CONST               1
             1278  LOAD_CONST               1
             1280  LOAD_CONST               1
             1282  LOAD_CONST               0
             1284  LOAD_CONST               0
             1286  LOAD_CONST               0
             1288  LOAD_CONST               1
             1290  LOAD_CONST               1
             1292  LOAD_CONST               0
             1294  LOAD_CONST               0
             1296  LOAD_CONST               0
             1298  LOAD_CONST               1
             1300  LOAD_CONST               0
             1302  LOAD_CONST               0
             1304  LOAD_CONST               0
             1306  LOAD_CONST               1
             1308  LOAD_CONST               0
             1310  LOAD_CONST               0
             1312  LOAD_CONST               1
             1314  LOAD_CONST               0
             1316  LOAD_CONST               1
             1318  LOAD_CONST               1
             1320  LOAD_CONST               1
             1322  LOAD_CONST               0
             1324  LOAD_CONST               0
             1326  LOAD_CONST               0
             1328  LOAD_CONST               1
             1330  LOAD_CONST               0
             1332  LOAD_CONST               0
             1334  LOAD_CONST               0

 L.  50      1336  LOAD_CONST               1

 L.  50      1338  LOAD_CONST               0

 L.  50      1340  LOAD_CONST               0

 L.  50      1342  LOAD_CONST               1

 L.  50      1344  LOAD_CONST               0

 L.  50      1346  LOAD_CONST               1

 L.  50      1348  LOAD_CONST               1

 L.  50      1350  LOAD_CONST               0

 L.  50      1352  LOAD_CONST               0

 L.  50      1354  LOAD_CONST               0

 L.  50      1356  LOAD_CONST               1

 L.  50      1358  LOAD_CONST               0

 L.  50      1360  LOAD_CONST               0

 L.  50      1362  LOAD_CONST               1

 L.  50      1364  LOAD_CONST               0

 L.  50      1366  LOAD_CONST               1

 L.  50      1368  LOAD_CONST               0

 L.  50      1370  LOAD_CONST               0

 L.  50      1372  LOAD_CONST               0

 L.  50      1374  LOAD_CONST               0

 L.  50      1376  LOAD_CONST               1

 L.  50      1378  LOAD_CONST               0

 L.  50      1380  LOAD_CONST               0

 L.  50      1382  LOAD_CONST               0

 L.  50      1384  LOAD_CONST               0

 L.  50      1386  LOAD_CONST               0

 L.  49      1388  BUILD_LIST_56        56 
             1390  STORE_FAST               'CoefCoef'
         1392_1394  JUMP_FORWARD       2650  'to 2650'
           1396_0  COME_FROM          1272  '1272'

 L.  51      1396  LOAD_FAST                'CrystalType'
             1398  LOAD_STR                 'tetragonal2'
             1400  COMPARE_OP               ==
         1402_1404  POP_JUMP_IF_TRUE   1416  'to 1416'
             1406  LOAD_FAST                'CrystalType'
             1408  LOAD_STR                 't2'
             1410  COMPARE_OP               ==
         1412_1414  POP_JUMP_IF_FALSE  1536  'to 1536'
           1416_0  COME_FROM          1402  '1402'

 L.  52      1416  LOAD_CONST               1
             1418  LOAD_CONST               1
             1420  LOAD_CONST               1
             1422  LOAD_CONST               0
             1424  LOAD_CONST               0
             1426  LOAD_CONST               1
             1428  LOAD_CONST               1
             1430  LOAD_CONST               1
             1432  LOAD_CONST               0
             1434  LOAD_CONST               0
             1436  LOAD_CONST               0
             1438  LOAD_CONST               1
             1440  LOAD_CONST               0
             1442  LOAD_CONST               0
             1444  LOAD_CONST               1
             1446  LOAD_CONST               1
             1448  LOAD_CONST               1
             1450  LOAD_CONST               0
             1452  LOAD_CONST               1
             1454  LOAD_CONST               0
             1456  LOAD_CONST               1
             1458  LOAD_CONST               1
             1460  LOAD_CONST               1
             1462  LOAD_CONST               0
             1464  LOAD_CONST               0
             1466  LOAD_CONST               -1
             1468  LOAD_CONST               1
             1470  LOAD_CONST               0
             1472  LOAD_CONST               0
             1474  LOAD_CONST               -1

 L.  53      1476  LOAD_CONST               1

 L.  53      1478  LOAD_CONST               -1

 L.  53      1480  LOAD_CONST               0

 L.  53      1482  LOAD_CONST               1

 L.  53      1484  LOAD_CONST               0

 L.  53      1486  LOAD_CONST               1

 L.  53      1488  LOAD_CONST               1

 L.  53      1490  LOAD_CONST               0

 L.  53      1492  LOAD_CONST               0

 L.  53      1494  LOAD_CONST               0

 L.  53      1496  LOAD_CONST               1

 L.  53      1498  LOAD_CONST               0

 L.  53      1500  LOAD_CONST               0

 L.  53      1502  LOAD_CONST               1

 L.  53      1504  LOAD_CONST               0

 L.  53      1506  LOAD_CONST               1

 L.  53      1508  LOAD_CONST               0

 L.  53      1510  LOAD_CONST               0

 L.  53      1512  LOAD_CONST               1

 L.  53      1514  LOAD_CONST               0

 L.  53      1516  LOAD_CONST               1

 L.  53      1518  LOAD_CONST               0

 L.  53      1520  LOAD_CONST               0

 L.  53      1522  LOAD_CONST               -1

 L.  53      1524  LOAD_CONST               0

 L.  53      1526  LOAD_CONST               0

 L.  52      1528  BUILD_LIST_56        56 
             1530  STORE_FAST               'CoefCoef'
         1532_1534  JUMP_FORWARD       2650  'to 2650'
           1536_0  COME_FROM          1412  '1412'

 L.  54      1536  LOAD_FAST                'CrystalType'
             1538  LOAD_STR                 'tetragonal1'
             1540  COMPARE_OP               ==
         1542_1544  POP_JUMP_IF_TRUE   1556  'to 1556'
             1546  LOAD_FAST                'CrystalType'
             1548  LOAD_STR                 't1'
             1550  COMPARE_OP               ==
         1552_1554  POP_JUMP_IF_FALSE  1676  'to 1676'
           1556_0  COME_FROM          1542  '1542'

 L.  55      1556  LOAD_CONST               1
             1558  LOAD_CONST               1
             1560  LOAD_CONST               1
             1562  LOAD_CONST               0
             1564  LOAD_CONST               0
             1566  LOAD_CONST               0
             1568  LOAD_CONST               1
             1570  LOAD_CONST               1
             1572  LOAD_CONST               0
             1574  LOAD_CONST               0
             1576  LOAD_CONST               0
             1578  LOAD_CONST               1
             1580  LOAD_CONST               0
             1582  LOAD_CONST               0
             1584  LOAD_CONST               0
             1586  LOAD_CONST               1
             1588  LOAD_CONST               0
             1590  LOAD_CONST               0
             1592  LOAD_CONST               1
             1594  LOAD_CONST               0
             1596  LOAD_CONST               1
             1598  LOAD_CONST               1
             1600  LOAD_CONST               1
             1602  LOAD_CONST               0
             1604  LOAD_CONST               0
             1606  LOAD_CONST               0
             1608  LOAD_CONST               1
             1610  LOAD_CONST               0
             1612  LOAD_CONST               0
             1614  LOAD_CONST               0
             1616  LOAD_CONST               1

 L.  56      1618  LOAD_CONST               0

 L.  56      1620  LOAD_CONST               0

 L.  56      1622  LOAD_CONST               1

 L.  56      1624  LOAD_CONST               0

 L.  56      1626  LOAD_CONST               1

 L.  56      1628  LOAD_CONST               1

 L.  56      1630  LOAD_CONST               0

 L.  56      1632  LOAD_CONST               0

 L.  56      1634  LOAD_CONST               0

 L.  56      1636  LOAD_CONST               1

 L.  56      1638  LOAD_CONST               0

 L.  56      1640  LOAD_CONST               0

 L.  56      1642  LOAD_CONST               1

 L.  56      1644  LOAD_CONST               0

 L.  56      1646  LOAD_CONST               1

 L.  56      1648  LOAD_CONST               0

 L.  56      1650  LOAD_CONST               0

 L.  56      1652  LOAD_CONST               0

 L.  56      1654  LOAD_CONST               0

 L.  56      1656  LOAD_CONST               1

 L.  56      1658  LOAD_CONST               0

 L.  56      1660  LOAD_CONST               0

 L.  56      1662  LOAD_CONST               0

 L.  56      1664  LOAD_CONST               0

 L.  56      1666  LOAD_CONST               0

 L.  55      1668  BUILD_LIST_56        56 
             1670  STORE_FAST               'CoefCoef'
         1672_1674  JUMP_FORWARD       2650  'to 2650'
           1676_0  COME_FROM          1552  '1552'

 L.  57      1676  LOAD_FAST                'CrystalType'
             1678  LOAD_STR                 'rhombohedral2'
             1680  COMPARE_OP               ==
         1682_1684  POP_JUMP_IF_TRUE   1696  'to 1696'
             1686  LOAD_FAST                'CrystalType'
             1688  LOAD_STR                 'r2'
             1690  COMPARE_OP               ==
         1692_1694  POP_JUMP_IF_FALSE  1816  'to 1816'
           1696_0  COME_FROM          1682  '1682'

 L.  58      1696  LOAD_CONST               1
             1698  LOAD_CONST               1
             1700  LOAD_CONST               1
             1702  LOAD_CONST               1
             1704  LOAD_CONST               1
             1706  LOAD_CONST               1
             1708  LOAD_FAST                'A'
             1710  LOAD_CONST               1
             1712  LOAD_CONST               1
             1714  LOAD_CONST               1
             1716  LOAD_CONST               -1
             1718  LOAD_CONST               1
             1720  LOAD_CONST               1
             1722  LOAD_CONST               1
             1724  LOAD_CONST               0
             1726  LOAD_CONST               1
             1728  LOAD_CONST               1
             1730  LOAD_FAST                'B'
             1732  LOAD_CONST               1
             1734  LOAD_FAST                'C'
             1736  LOAD_FAST                'D'
             1738  LOAD_CONST               1
             1740  LOAD_CONST               1
             1742  LOAD_FAST                'E'
             1744  LOAD_FAST                'F'
             1746  LOAD_CONST               1
             1748  LOAD_CONST               1
             1750  LOAD_CONST               -1
             1752  LOAD_CONST               -1
             1754  LOAD_CONST               0

 L.  59      1756  LOAD_CONST               1

 L.  59      1758  LOAD_CONST               -1

 L.  59      1760  LOAD_FAST                'G'

 L.  59      1762  LOAD_CONST               1

 L.  59      1764  LOAD_FAST                'H'

 L.  59      1766  LOAD_FAST                'I'

 L.  59      1768  LOAD_CONST               1

 L.  59      1770  LOAD_CONST               0

 L.  59      1772  LOAD_CONST               0

 L.  59      1774  LOAD_CONST               0

 L.  59      1776  LOAD_CONST               1

 L.  59      1778  LOAD_CONST               0

 L.  59      1780  LOAD_CONST               -1

 L.  59      1782  LOAD_CONST               1

 L.  59      1784  LOAD_CONST               1

 L.  59      1786  LOAD_FAST                'J'

 L.  59      1788  LOAD_CONST               1

 L.  59      1790  LOAD_CONST               1

 L.  59      1792  LOAD_CONST               1

 L.  59      1794  LOAD_CONST               -1

 L.  59      1796  LOAD_FAST                'K'

 L.  59      1798  LOAD_CONST               1

 L.  59      1800  LOAD_CONST               -1

 L.  59      1802  LOAD_CONST               -1

 L.  59      1804  LOAD_CONST               1

 L.  59      1806  LOAD_CONST               -1

 L.  58      1808  BUILD_LIST_56        56 
             1810  STORE_FAST               'CoefCoef'
         1812_1814  JUMP_FORWARD       2650  'to 2650'
           1816_0  COME_FROM          1692  '1692'

 L.  60      1816  LOAD_FAST                'CrystalType'
             1818  LOAD_STR                 'rhombohedral1'
             1820  COMPARE_OP               ==
         1822_1824  POP_JUMP_IF_TRUE   1836  'to 1836'
             1826  LOAD_FAST                'CrystalType'
             1828  LOAD_STR                 'r1'
             1830  COMPARE_OP               ==
         1832_1834  POP_JUMP_IF_FALSE  1956  'to 1956'
           1836_0  COME_FROM          1822  '1822'

 L.  61      1836  LOAD_CONST               1
             1838  LOAD_CONST               1
             1840  LOAD_CONST               1
             1842  LOAD_CONST               1
             1844  LOAD_CONST               0
             1846  LOAD_CONST               0
             1848  LOAD_FAST                'A'
             1850  LOAD_CONST               1
             1852  LOAD_CONST               1
             1854  LOAD_CONST               0
             1856  LOAD_CONST               0
             1858  LOAD_CONST               1
             1860  LOAD_CONST               1
             1862  LOAD_CONST               0
             1864  LOAD_CONST               0
             1866  LOAD_CONST               1
             1868  LOAD_CONST               0
             1870  LOAD_CONST               0
             1872  LOAD_CONST               1
             1874  LOAD_FAST                'C'
             1876  LOAD_FAST                'D'
             1878  LOAD_CONST               1
             1880  LOAD_CONST               1
             1882  LOAD_FAST                'E'
             1884  LOAD_CONST               0
             1886  LOAD_CONST               0
             1888  LOAD_CONST               1
             1890  LOAD_CONST               -1
             1892  LOAD_CONST               0
             1894  LOAD_CONST               0
             1896  LOAD_CONST               1

 L.  62      1898  LOAD_CONST               0

 L.  62      1900  LOAD_CONST               0

 L.  62      1902  LOAD_CONST               1

 L.  62      1904  LOAD_FAST                'H'

 L.  62      1906  LOAD_FAST                'I'

 L.  62      1908  LOAD_CONST               1

 L.  62      1910  LOAD_CONST               0

 L.  62      1912  LOAD_CONST               0

 L.  62      1914  LOAD_CONST               0

 L.  62      1916  LOAD_CONST               1

 L.  62      1918  LOAD_CONST               0

 L.  62      1920  LOAD_CONST               0

 L.  62      1922  LOAD_CONST               1

 L.  62      1924  LOAD_CONST               1

 L.  62      1926  LOAD_FAST                'J'

 L.  62      1928  LOAD_CONST               1

 L.  62      1930  LOAD_CONST               0

 L.  62      1932  LOAD_CONST               0

 L.  62      1934  LOAD_CONST               -1

 L.  62      1936  LOAD_FAST                'K'

 L.  62      1938  LOAD_CONST               1

 L.  62      1940  LOAD_CONST               0

 L.  62      1942  LOAD_CONST               0

 L.  62      1944  LOAD_CONST               0

 L.  62      1946  LOAD_CONST               0

 L.  61      1948  BUILD_LIST_56        56 
             1950  STORE_FAST               'CoefCoef'
         1952_1954  JUMP_FORWARD       2650  'to 2650'
           1956_0  COME_FROM          1832  '1832'

 L.  63      1956  LOAD_FAST                'CrystalType'
             1958  LOAD_STR                 'hexagonal2'
             1960  COMPARE_OP               ==
         1962_1964  POP_JUMP_IF_TRUE   1976  'to 1976'
             1966  LOAD_FAST                'CrystalType'
             1968  LOAD_STR                 'h2'
             1970  COMPARE_OP               ==
         1972_1974  POP_JUMP_IF_FALSE  2096  'to 2096'
           1976_0  COME_FROM          1962  '1962'

 L.  64      1976  LOAD_CONST               1
             1978  LOAD_CONST               1
             1980  LOAD_CONST               1
             1982  LOAD_CONST               0
             1984  LOAD_CONST               0
             1986  LOAD_CONST               1
             1988  LOAD_FAST                'A'
             1990  LOAD_CONST               1
             1992  LOAD_CONST               0
             1994  LOAD_CONST               0
             1996  LOAD_CONST               -1
             1998  LOAD_CONST               1
             2000  LOAD_CONST               0
             2002  LOAD_CONST               0
             2004  LOAD_CONST               0
             2006  LOAD_CONST               1
             2008  LOAD_CONST               1
             2010  LOAD_CONST               0
             2012  LOAD_CONST               1
             2014  LOAD_CONST               0
             2016  LOAD_FAST                'D'
             2018  LOAD_CONST               1
             2020  LOAD_CONST               1
             2022  LOAD_CONST               0
             2024  LOAD_CONST               0
             2026  LOAD_CONST               1
             2028  LOAD_CONST               1
             2030  LOAD_CONST               0
             2032  LOAD_CONST               0
             2034  LOAD_CONST               0
             2036  LOAD_CONST               1

 L.  65      2038  LOAD_CONST               -1

 L.  65      2040  LOAD_CONST               0

 L.  65      2042  LOAD_CONST               1

 L.  65      2044  LOAD_CONST               0

 L.  65      2046  LOAD_FAST                'I'

 L.  65      2048  LOAD_CONST               1

 L.  65      2050  LOAD_CONST               0

 L.  65      2052  LOAD_CONST               0

 L.  65      2054  LOAD_CONST               0

 L.  65      2056  LOAD_CONST               1

 L.  65      2058  LOAD_CONST               0

 L.  65      2060  LOAD_CONST               0

 L.  65      2062  LOAD_CONST               1

 L.  65      2064  LOAD_CONST               0

 L.  65      2066  LOAD_FAST                'J'

 L.  65      2068  LOAD_CONST               0

 L.  65      2070  LOAD_CONST               0

 L.  65      2072  LOAD_CONST               1

 L.  65      2074  LOAD_CONST               0

 L.  65      2076  LOAD_FAST                'K'

 L.  65      2078  LOAD_CONST               0

 L.  65      2080  LOAD_CONST               0

 L.  65      2082  LOAD_CONST               -1

 L.  65      2084  LOAD_CONST               0

 L.  65      2086  LOAD_CONST               -1

 L.  64      2088  BUILD_LIST_56        56 
             2090  STORE_FAST               'CoefCoef'
         2092_2094  JUMP_FORWARD       2650  'to 2650'
           2096_0  COME_FROM          1972  '1972'

 L.  66      2096  LOAD_FAST                'CrystalType'
             2098  LOAD_STR                 'hexagonal1'
             2100  COMPARE_OP               ==
         2102_2104  POP_JUMP_IF_TRUE   2116  'to 2116'
             2106  LOAD_FAST                'CrystalType'
             2108  LOAD_STR                 'h1'
             2110  COMPARE_OP               ==
         2112_2114  POP_JUMP_IF_FALSE  2236  'to 2236'
           2116_0  COME_FROM          2102  '2102'

 L.  67      2116  LOAD_CONST               1
             2118  LOAD_CONST               1
             2120  LOAD_CONST               1
             2122  LOAD_CONST               0
             2124  LOAD_CONST               0
             2126  LOAD_CONST               0
             2128  LOAD_FAST                'A'
             2130  LOAD_CONST               1
             2132  LOAD_CONST               0
             2134  LOAD_CONST               0
             2136  LOAD_CONST               0
             2138  LOAD_CONST               1
             2140  LOAD_CONST               0
             2142  LOAD_CONST               0
             2144  LOAD_CONST               0
             2146  LOAD_CONST               1
             2148  LOAD_CONST               0
             2150  LOAD_CONST               0
             2152  LOAD_CONST               1
             2154  LOAD_CONST               0
             2156  LOAD_FAST                'D'
             2158  LOAD_CONST               1
             2160  LOAD_CONST               1
             2162  LOAD_CONST               0
             2164  LOAD_CONST               0
             2166  LOAD_CONST               0
             2168  LOAD_CONST               1
             2170  LOAD_CONST               0
             2172  LOAD_CONST               0
             2174  LOAD_CONST               0
             2176  LOAD_CONST               1

 L.  68      2178  LOAD_CONST               0

 L.  68      2180  LOAD_CONST               0

 L.  68      2182  LOAD_CONST               1

 L.  68      2184  LOAD_CONST               0

 L.  68      2186  LOAD_FAST                'I'

 L.  68      2188  LOAD_CONST               1

 L.  68      2190  LOAD_CONST               0

 L.  68      2192  LOAD_CONST               0

 L.  68      2194  LOAD_CONST               0

 L.  68      2196  LOAD_CONST               1

 L.  68      2198  LOAD_CONST               0

 L.  68      2200  LOAD_CONST               0

 L.  68      2202  LOAD_CONST               1

 L.  68      2204  LOAD_CONST               0

 L.  68      2206  LOAD_FAST                'J'

 L.  68      2208  LOAD_CONST               0

 L.  68      2210  LOAD_CONST               0

 L.  68      2212  LOAD_CONST               0

 L.  68      2214  LOAD_CONST               0

 L.  68      2216  LOAD_FAST                'K'

 L.  68      2218  LOAD_CONST               0

 L.  68      2220  LOAD_CONST               0

 L.  68      2222  LOAD_CONST               0

 L.  68      2224  LOAD_CONST               0

 L.  68      2226  LOAD_CONST               0

 L.  67      2228  BUILD_LIST_56        56 
             2230  STORE_FAST               'CoefCoef'
         2232_2234  JUMP_FORWARD       2650  'to 2650'
           2236_0  COME_FROM          2112  '2112'

 L.  69      2236  LOAD_FAST                'CrystalType'
             2238  LOAD_STR                 'cubic2'
             2240  COMPARE_OP               ==
         2242_2244  POP_JUMP_IF_TRUE   2256  'to 2256'
             2246  LOAD_FAST                'CrystalType'
             2248  LOAD_STR                 'c2'
             2250  COMPARE_OP               ==
         2252_2254  POP_JUMP_IF_FALSE  2376  'to 2376'
           2256_0  COME_FROM          2242  '2242'

 L.  70      2256  LOAD_CONST               1
             2258  LOAD_CONST               1
             2260  LOAD_CONST               1
             2262  LOAD_CONST               0
             2264  LOAD_CONST               0
             2266  LOAD_CONST               0
             2268  LOAD_CONST               1
             2270  LOAD_CONST               1
             2272  LOAD_CONST               0
             2274  LOAD_CONST               0
             2276  LOAD_CONST               0
             2278  LOAD_CONST               1
             2280  LOAD_CONST               0
             2282  LOAD_CONST               0
             2284  LOAD_CONST               0
             2286  LOAD_CONST               1
             2288  LOAD_CONST               0
             2290  LOAD_CONST               0
             2292  LOAD_CONST               1
             2294  LOAD_CONST               0
             2296  LOAD_CONST               1
             2298  LOAD_CONST               1
             2300  LOAD_CONST               1
             2302  LOAD_CONST               0
             2304  LOAD_CONST               0
             2306  LOAD_CONST               0
             2308  LOAD_CONST               1
             2310  LOAD_CONST               0
             2312  LOAD_CONST               0
             2314  LOAD_CONST               0
             2316  LOAD_CONST               1

 L.  71      2318  LOAD_CONST               0

 L.  71      2320  LOAD_CONST               0

 L.  71      2322  LOAD_CONST               1

 L.  71      2324  LOAD_CONST               0

 L.  71      2326  LOAD_CONST               1

 L.  71      2328  LOAD_CONST               1

 L.  71      2330  LOAD_CONST               0

 L.  71      2332  LOAD_CONST               0

 L.  71      2334  LOAD_CONST               0

 L.  71      2336  LOAD_CONST               1

 L.  71      2338  LOAD_CONST               0

 L.  71      2340  LOAD_CONST               0

 L.  71      2342  LOAD_CONST               1

 L.  71      2344  LOAD_CONST               0

 L.  71      2346  LOAD_CONST               1

 L.  71      2348  LOAD_CONST               0

 L.  71      2350  LOAD_CONST               0

 L.  71      2352  LOAD_CONST               0

 L.  71      2354  LOAD_CONST               0

 L.  71      2356  LOAD_CONST               1

 L.  71      2358  LOAD_CONST               0

 L.  71      2360  LOAD_CONST               0

 L.  71      2362  LOAD_CONST               0

 L.  71      2364  LOAD_CONST               0

 L.  71      2366  LOAD_CONST               0

 L.  70      2368  BUILD_LIST_56        56 
             2370  STORE_FAST               'CoefCoef'
         2372_2374  JUMP_FORWARD       2650  'to 2650'
           2376_0  COME_FROM          2252  '2252'

 L.  72      2376  LOAD_FAST                'CrystalType'
             2378  LOAD_STR                 'cubic1'
             2380  COMPARE_OP               ==
         2382_2384  POP_JUMP_IF_TRUE   2396  'to 2396'
             2386  LOAD_FAST                'CrystalType'
             2388  LOAD_STR                 'c1'
             2390  COMPARE_OP               ==
         2392_2394  POP_JUMP_IF_FALSE  2514  'to 2514'
           2396_0  COME_FROM          2382  '2382'

 L.  73      2396  LOAD_CONST               1
             2398  LOAD_CONST               1
             2400  LOAD_CONST               1
             2402  LOAD_CONST               0
             2404  LOAD_CONST               0
             2406  LOAD_CONST               0
             2408  LOAD_CONST               1
             2410  LOAD_CONST               1
             2412  LOAD_CONST               0
             2414  LOAD_CONST               0
             2416  LOAD_CONST               0
             2418  LOAD_CONST               1
             2420  LOAD_CONST               0
             2422  LOAD_CONST               0
             2424  LOAD_CONST               0
             2426  LOAD_CONST               1
             2428  LOAD_CONST               0
             2430  LOAD_CONST               0
             2432  LOAD_CONST               1
             2434  LOAD_CONST               0
             2436  LOAD_CONST               1
             2438  LOAD_CONST               1
             2440  LOAD_CONST               1
             2442  LOAD_CONST               0
           2444_0  COME_FROM           638  '638'
             2444  LOAD_CONST               0
             2446  LOAD_CONST               0
             2448  LOAD_CONST               1
             2450  LOAD_CONST               0
             2452  LOAD_CONST               0
             2454  LOAD_CONST               0
             2456  LOAD_CONST               1

 L.  74      2458  LOAD_CONST               0

 L.  74      2460  LOAD_CONST               0

 L.  74      2462  LOAD_CONST               1

 L.  74      2464  LOAD_CONST               0

 L.  74      2466  LOAD_CONST               1

 L.  74      2468  LOAD_CONST               1

 L.  74      2470  LOAD_CONST               0

 L.  74      2472  LOAD_CONST               0

 L.  74      2474  LOAD_CONST               0

 L.  74      2476  LOAD_CONST               1

 L.  74      2478  LOAD_CONST               0

 L.  74      2480  LOAD_CONST               0

 L.  74      2482  LOAD_CONST               1

 L.  74      2484  LOAD_CONST               0

 L.  74      2486  LOAD_CONST               1

 L.  74      2488  LOAD_CONST               0

 L.  74      2490  LOAD_CONST               0

 L.  74      2492  LOAD_CONST               0

 L.  74      2494  LOAD_CONST               0

 L.  74      2496  LOAD_CONST               1

 L.  74      2498  LOAD_CONST               0

 L.  74      2500  LOAD_CONST               0

 L.  74      2502  LOAD_CONST               0

 L.  74      2504  LOAD_CONST               0

 L.  74      2506  LOAD_CONST               0

 L.  73      2508  BUILD_LIST_56        56 
             2510  STORE_FAST               'CoefCoef'
           2512_0  COME_FROM           706  '706'
             2512  JUMP_FORWARD       2650  'to 2650'
           2514_0  COME_FROM          2392  '2392'

 L.  75      2514  LOAD_FAST                'CrystalType'
             2516  LOAD_STR                 'isotropic'
             2518  COMPARE_OP               ==
         2520_2522  POP_JUMP_IF_TRUE   2534  'to 2534'
             2524  LOAD_FAST                'CrystalType'
             2526  LOAD_STR                 'i'
             2528  COMPARE_OP               ==
         2530_2532  POP_JUMP_IF_FALSE  2650  'to 2650'
           2534_0  COME_FROM          2520  '2520'

 L.  76      2534  LOAD_CONST               1
             2536  LOAD_CONST               1
             2538  LOAD_CONST               1
             2540  LOAD_CONST               0
             2542  LOAD_CONST               0
             2544  LOAD_CONST               0
             2546  LOAD_CONST               1
             2548  LOAD_CONST               1
             2550  LOAD_CONST               0
             2552  LOAD_CONST               0
             2554  LOAD_CONST               0
             2556  LOAD_CONST               1
             2558  LOAD_CONST               0
             2560  LOAD_CONST               0
             2562  LOAD_CONST               0
             2564  LOAD_FAST                'L'
             2566  LOAD_CONST               0
             2568  LOAD_CONST               0
             2570  LOAD_FAST                'M'
             2572  LOAD_CONST               0
             2574  LOAD_FAST                'M'
             2576  LOAD_CONST               1
             2578  LOAD_CONST               1
           2580_0  COME_FROM           774  '774'
             2580  LOAD_CONST               0
             2582  LOAD_CONST               0
             2584  LOAD_CONST               0
             2586  LOAD_CONST               1
             2588  LOAD_CONST               0
             2590  LOAD_CONST               0
             2592  LOAD_CONST               0
             2594  LOAD_FAST                'M'

 L.  77      2596  LOAD_CONST               0

 L.  77      2598  LOAD_CONST               0

 L.  77      2600  LOAD_FAST                'L'

 L.  77      2602  LOAD_CONST               0

 L.  77      2604  LOAD_FAST                'M'

 L.  77      2606  LOAD_CONST               1

 L.  77      2608  LOAD_CONST               0

 L.  77      2610  LOAD_CONST               0

 L.  77      2612  LOAD_CONST               0

 L.  77      2614  LOAD_FAST                'M'

 L.  77      2616  LOAD_CONST               0

 L.  77      2618  LOAD_CONST               0

 L.  77      2620  LOAD_FAST                'M'

 L.  77      2622  LOAD_CONST               0

 L.  77      2624  LOAD_FAST                'L'

 L.  77      2626  LOAD_CONST               0

 L.  77      2628  LOAD_CONST               0

 L.  77      2630  LOAD_CONST               0

 L.  77      2632  LOAD_CONST               0

 L.  77      2634  LOAD_FAST                'N'

 L.  77      2636  LOAD_CONST               0

 L.  77      2638  LOAD_CONST               0

 L.  77      2640  LOAD_CONST               0

 L.  77      2642  LOAD_CONST               0

 L.  77      2644  LOAD_CONST               0

 L.  76      2646  BUILD_LIST_56        56 
             2648  STORE_FAST               'CoefCoef'
           2650_0  COME_FROM          2530  '2530'
           2650_1  COME_FROM          2512  '2512'
           2650_2  COME_FROM          2372  '2372'
           2650_3  COME_FROM          2232  '2232'
           2650_4  COME_FROM          2092  '2092'
           2650_5  COME_FROM          1952  '1952'
           2650_6  COME_FROM          1812  '1812'
           2650_7  COME_FROM          1672  '1672'
           2650_8  COME_FROM          1532  '1532'
           2650_9  COME_FROM          1392  '1392'
          2650_10  COME_FROM          1252  '1252'
          2650_11  COME_FROM          1112  '1112'
          2650_12  COME_FROM           852  '852'
          2650_13  COME_FROM           842  '842'
          2650_14  COME_FROM           792  '792'

 L.  78      2650  LOAD_FAST                'CoefCoef'
             2652  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM' instruction at offset 2444_0


def coef_ind--- This code section failed: ---

 L.  83         0  LOAD_FAST                'CrystalType'
                2  LOAD_METHOD              lower
                4  CALL_METHOD_0         0  ''
                6  STORE_FAST               'CrystalType'

 L.  84         8  LOAD_FAST                'Ord'
               10  LOAD_CONST               2
               12  COMPARE_OP               ==
            14_16  POP_JUMP_IF_FALSE   846  'to 846'

 L.  85        18  LOAD_CONST               1
               20  LOAD_CONST               2
               22  BUILD_LIST_2          2 
               24  STORE_FAST               'A'

 L.  86        26  LOAD_FAST                'CrystalType'
               28  LOAD_STR                 'triclinic'
               30  COMPARE_OP               ==
               32  POP_JUMP_IF_TRUE     42  'to 42'
               34  LOAD_FAST                'CrystalType'
               36  LOAD_STR                 'n'
               38  COMPARE_OP               ==
               40  POP_JUMP_IF_FALSE    92  'to 92'
             42_0  COME_FROM            32  '32'

 L.  87        42  LOAD_CONST               1
               44  LOAD_CONST               2
               46  LOAD_CONST               3
               48  LOAD_CONST               4
               50  LOAD_CONST               5
               52  LOAD_CONST               6
               54  LOAD_CONST               7
               56  LOAD_CONST               8
               58  LOAD_CONST               9
               60  LOAD_CONST               10
               62  LOAD_CONST               11
               64  LOAD_CONST               12
               66  LOAD_CONST               13
               68  LOAD_CONST               14
               70  LOAD_CONST               15
               72  LOAD_CONST               16
               74  LOAD_CONST               17
               76  LOAD_CONST               18
               78  LOAD_CONST               19
               80  LOAD_CONST               20
               82  LOAD_CONST               21
               84  BUILD_LIST_21        21 
               86  STORE_FAST               'CoefInd'
            88_90  JUMP_ABSOLUTE      2650  'to 2650'
             92_0  COME_FROM            40  '40'

 L.  88        92  LOAD_FAST                'CrystalType'
               94  LOAD_STR                 'monoclinic'
               96  COMPARE_OP               ==
               98  POP_JUMP_IF_TRUE    108  'to 108'
              100  LOAD_FAST                'CrystalType'
              102  LOAD_STR                 'm'
              104  COMPARE_OP               ==
              106  POP_JUMP_IF_FALSE   158  'to 158'
            108_0  COME_FROM            98  '98'

 L.  89       108  LOAD_CONST               1
              110  LOAD_CONST               2
              112  LOAD_CONST               3
              114  LOAD_CONST               0
              116  LOAD_CONST               5
              118  LOAD_CONST               0
              120  LOAD_CONST               7
              122  LOAD_CONST               8
              124  LOAD_CONST               0
              126  LOAD_CONST               10
              128  LOAD_CONST               0
              130  LOAD_CONST               12
              132  LOAD_CONST               0
              134  LOAD_CONST               14
              136  LOAD_CONST               0
              138  LOAD_CONST               16
              140  LOAD_CONST               0
              142  LOAD_CONST               18
              144  LOAD_CONST               19
              146  LOAD_CONST               0
              148  LOAD_CONST               21
              150  BUILD_LIST_21        21 
              152  STORE_FAST               'CoefInd'
          154_156  JUMP_ABSOLUTE      2650  'to 2650'
            158_0  COME_FROM           106  '106'

 L.  90       158  LOAD_FAST                'CrystalType'
              160  LOAD_STR                 'orthorhombic'
              162  COMPARE_OP               ==
              164  POP_JUMP_IF_TRUE    174  'to 174'
              166  LOAD_FAST                'CrystalType'
              168  LOAD_STR                 'o'
              170  COMPARE_OP               ==
              172  POP_JUMP_IF_FALSE   224  'to 224'
            174_0  COME_FROM           164  '164'

 L.  91       174  LOAD_CONST               1
              176  LOAD_CONST               2
              178  LOAD_CONST               3
              180  LOAD_CONST               0
              182  LOAD_CONST               0
              184  LOAD_CONST               0
              186  LOAD_CONST               7
              188  LOAD_CONST               8
              190  LOAD_CONST               0
              192  LOAD_CONST               0
              194  LOAD_CONST               0
              196  LOAD_CONST               12
              198  LOAD_CONST               0
              200  LOAD_CONST               0
              202  LOAD_CONST               0
              204  LOAD_CONST               16
              206  LOAD_CONST               0
              208  LOAD_CONST               0
              210  LOAD_CONST               19
              212  LOAD_CONST               0
              214  LOAD_CONST               21
              216  BUILD_LIST_21        21 
              218  STORE_FAST               'CoefInd'
          220_222  JUMP_ABSOLUTE      2650  'to 2650'
            224_0  COME_FROM           172  '172'

 L.  92       224  LOAD_FAST                'CrystalType'
              226  LOAD_STR                 'tetragonal2'
              228  COMPARE_OP               ==
              230  POP_JUMP_IF_TRUE    242  'to 242'
              232  LOAD_FAST                'CrystalType'
              234  LOAD_STR                 't2'
              236  COMPARE_OP               ==
          238_240  POP_JUMP_IF_FALSE   292  'to 292'
            242_0  COME_FROM           230  '230'

 L.  93       242  LOAD_CONST               1
              244  LOAD_CONST               2
              246  LOAD_CONST               3
              248  LOAD_CONST               0
              250  LOAD_CONST               0
              252  LOAD_CONST               6
              254  LOAD_CONST               1
              256  LOAD_CONST               3
              258  LOAD_CONST               0
              260  LOAD_CONST               0
              262  LOAD_CONST               6
              264  LOAD_CONST               12
              266  LOAD_CONST               0
              268  LOAD_CONST               0
              270  LOAD_CONST               0
              272  LOAD_CONST               16
              274  LOAD_CONST               0
              276  LOAD_CONST               0
              278  LOAD_CONST               16
              280  LOAD_CONST               0
              282  LOAD_CONST               21
              284  BUILD_LIST_21        21 
              286  STORE_FAST               'CoefInd'
          288_290  JUMP_ABSOLUTE      2650  'to 2650'
            292_0  COME_FROM           238  '238'

 L.  94       292  LOAD_FAST                'CrystalType'
              294  LOAD_STR                 'tetragonal1'
              296  COMPARE_OP               ==
          298_300  POP_JUMP_IF_TRUE    312  'to 312'
              302  LOAD_FAST                'CrystalType'
              304  LOAD_STR                 't1'
              306  COMPARE_OP               ==
          308_310  POP_JUMP_IF_FALSE   362  'to 362'
            312_0  COME_FROM           298  '298'

 L.  95       312  LOAD_CONST               1
              314  LOAD_CONST               2
              316  LOAD_CONST               3
              318  LOAD_CONST               0
              320  LOAD_CONST               0
              322  LOAD_CONST               0
              324  LOAD_CONST               1
              326  LOAD_CONST               3
              328  LOAD_CONST               0
              330  LOAD_CONST               0
              332  LOAD_CONST               0
              334  LOAD_CONST               12
              336  LOAD_CONST               0
              338  LOAD_CONST               0
              340  LOAD_CONST               0
              342  LOAD_CONST               16
              344  LOAD_CONST               0
              346  LOAD_CONST               0
              348  LOAD_CONST               16
              350  LOAD_CONST               0
              352  LOAD_CONST               21
              354  BUILD_LIST_21        21 
              356  STORE_FAST               'CoefInd'
          358_360  JUMP_ABSOLUTE      2650  'to 2650'
            362_0  COME_FROM           308  '308'

 L.  96       362  LOAD_FAST                'CrystalType'
              364  LOAD_STR                 'rhombohedral2'
              366  COMPARE_OP               ==
          368_370  POP_JUMP_IF_TRUE    382  'to 382'
              372  LOAD_FAST                'CrystalType'
              374  LOAD_STR                 'r2'
              376  COMPARE_OP               ==
          378_380  POP_JUMP_IF_FALSE   432  'to 432'
            382_0  COME_FROM           368  '368'

 L.  97       382  LOAD_CONST               1
              384  LOAD_CONST               2
              386  LOAD_CONST               3
              388  LOAD_CONST               4
              390  LOAD_CONST               5
              392  LOAD_CONST               0
              394  LOAD_CONST               1
              396  LOAD_CONST               3
              398  LOAD_CONST               4
              400  LOAD_CONST               5
              402  LOAD_CONST               0
              404  LOAD_CONST               12
              406  LOAD_CONST               0
              408  LOAD_CONST               0
              410  LOAD_CONST               0
              412  LOAD_CONST               16
              414  LOAD_CONST               0
              416  LOAD_CONST               5
              418  LOAD_CONST               16
              420  LOAD_CONST               4
              422  LOAD_FAST                'A'
              424  BUILD_LIST_21        21 
              426  STORE_FAST               'CoefInd'
          428_430  JUMP_ABSOLUTE      2650  'to 2650'
            432_0  COME_FROM           378  '378'

 L.  98       432  LOAD_FAST                'CrystalType'
              434  LOAD_STR                 'rhombohedral1'
              436  COMPARE_OP               ==
          438_440  POP_JUMP_IF_TRUE    452  'to 452'
              442  LOAD_FAST                'CrystalType'
              444  LOAD_STR                 'r1'
              446  COMPARE_OP               ==
          448_450  POP_JUMP_IF_FALSE   502  'to 502'
            452_0  COME_FROM           438  '438'

 L.  99       452  LOAD_CONST               1
              454  LOAD_CONST               2
              456  LOAD_CONST               3
              458  LOAD_CONST               4
              460  LOAD_CONST               0
              462  LOAD_CONST               0
              464  LOAD_CONST               1
              466  LOAD_CONST               3
              468  LOAD_CONST               4
              470  LOAD_CONST               0
              472  LOAD_CONST               0
              474  LOAD_CONST               12
              476  LOAD_CONST               0
              478  LOAD_CONST               0
              480  LOAD_CONST               0
              482  LOAD_CONST               16
              484  LOAD_CONST               0
              486  LOAD_CONST               0
              488  LOAD_CONST               16
              490  LOAD_CONST               4
              492  LOAD_FAST                'A'
              494  BUILD_LIST_21        21 
              496  STORE_FAST               'CoefInd'
          498_500  JUMP_ABSOLUTE      2650  'to 2650'
            502_0  COME_FROM           448  '448'

 L. 100       502  LOAD_FAST                'CrystalType'
              504  LOAD_STR                 'hexagonal2'
              506  COMPARE_OP               ==
          508_510  POP_JUMP_IF_TRUE    522  'to 522'
              512  LOAD_FAST                'CrystalType'
              514  LOAD_STR                 'h2'
              516  COMPARE_OP               ==
          518_520  POP_JUMP_IF_FALSE   572  'to 572'
            522_0  COME_FROM           508  '508'

 L. 101       522  LOAD_CONST               1
              524  LOAD_CONST               2
              526  LOAD_CONST               3
              528  LOAD_CONST               0
              530  LOAD_CONST               0
              532  LOAD_CONST               0
              534  LOAD_CONST               1
              536  LOAD_CONST               3
              538  LOAD_CONST               0
              540  LOAD_CONST               0
              542  LOAD_CONST               0
              544  LOAD_CONST               12
              546  LOAD_CONST               0
              548  LOAD_CONST               0
              550  LOAD_CONST               0
              552  LOAD_CONST               16
              554  LOAD_CONST               0
              556  LOAD_CONST               0
              558  LOAD_CONST               16
              560  LOAD_CONST               0
              562  LOAD_FAST                'A'
              564  BUILD_LIST_21        21 
              566  STORE_FAST               'CoefInd'
          568_570  JUMP_ABSOLUTE      2650  'to 2650'
            572_0  COME_FROM           518  '518'

 L. 102       572  LOAD_FAST                'CrystalType'
              574  LOAD_STR                 'hexagonal1'
              576  COMPARE_OP               ==
          578_580  POP_JUMP_IF_TRUE    592  'to 592'
              582  LOAD_FAST                'CrystalType'
              584  LOAD_STR                 'h1'
              586  COMPARE_OP               ==
          588_590  POP_JUMP_IF_FALSE   640  'to 640'
            592_0  COME_FROM           578  '578'

 L. 103       592  LOAD_CONST               1
              594  LOAD_CONST               2
              596  LOAD_CONST               3
              598  LOAD_CONST               0
              600  LOAD_CONST               0
              602  LOAD_CONST               0
              604  LOAD_CONST               1
              606  LOAD_CONST               3
              608  LOAD_CONST               0
              610  LOAD_CONST               0
              612  LOAD_CONST               0
              614  LOAD_CONST               12
              616  LOAD_CONST               0
              618  LOAD_CONST               0
              620  LOAD_CONST               0
              622  LOAD_CONST               16
              624  LOAD_CONST               0
              626  LOAD_CONST               0
              628  LOAD_CONST               16
              630  LOAD_CONST               0
              632  LOAD_FAST                'A'
              634  BUILD_LIST_21        21 
              636  STORE_FAST               'CoefInd'
              638  JUMP_FORWARD       2650  'to 2650'
            640_0  COME_FROM           588  '588'

 L. 104       640  LOAD_FAST                'CrystalType'
              642  LOAD_STR                 'cubic2'
              644  COMPARE_OP               ==
          646_648  POP_JUMP_IF_TRUE    660  'to 660'
              650  LOAD_FAST                'CrystalType'
              652  LOAD_STR                 'c2'
              654  COMPARE_OP               ==
          656_658  POP_JUMP_IF_FALSE   708  'to 708'
            660_0  COME_FROM           646  '646'

 L. 105       660  LOAD_CONST               1
              662  LOAD_CONST               2
              664  LOAD_CONST               2
              666  LOAD_CONST               0
              668  LOAD_CONST               0
              670  LOAD_CONST               0
              672  LOAD_CONST               1
              674  LOAD_CONST               2
              676  LOAD_CONST               0
              678  LOAD_CONST               0
              680  LOAD_CONST               0
              682  LOAD_CONST               1
              684  LOAD_CONST               0
              686  LOAD_CONST               0
              688  LOAD_CONST               0
              690  LOAD_CONST               16
              692  LOAD_CONST               0
              694  LOAD_CONST               0
              696  LOAD_CONST               16
              698  LOAD_CONST               0
              700  LOAD_CONST               16
              702  BUILD_LIST_21        21 
              704  STORE_FAST               'CoefInd'
              706  JUMP_FORWARD       2650  'to 2650'
            708_0  COME_FROM           656  '656'

 L. 106       708  LOAD_FAST                'CrystalType'
              710  LOAD_STR                 'cubic1'
              712  COMPARE_OP               ==
          714_716  POP_JUMP_IF_TRUE    728  'to 728'
              718  LOAD_FAST                'CrystalType'
              720  LOAD_STR                 'c1'
              722  COMPARE_OP               ==
          724_726  POP_JUMP_IF_FALSE   776  'to 776'
            728_0  COME_FROM           714  '714'

 L. 107       728  LOAD_CONST               1
              730  LOAD_CONST               2
              732  LOAD_CONST               2
              734  LOAD_CONST               0
              736  LOAD_CONST               0
              738  LOAD_CONST               0
              740  LOAD_CONST               1
              742  LOAD_CONST               2
              744  LOAD_CONST               0
              746  LOAD_CONST               0
              748  LOAD_CONST               0
              750  LOAD_CONST               1
              752  LOAD_CONST               0
              754  LOAD_CONST               0
              756  LOAD_CONST               0
              758  LOAD_CONST               16
              760  LOAD_CONST               0
              762  LOAD_CONST               0
              764  LOAD_CONST               16
              766  LOAD_CONST               0
              768  LOAD_CONST               16
              770  BUILD_LIST_21        21 
              772  STORE_FAST               'CoefInd'
              774  JUMP_FORWARD       2650  'to 2650'
            776_0  COME_FROM           724  '724'

 L. 108       776  LOAD_FAST                'CrystalType'
              778  LOAD_STR                 'isotropic'
              780  COMPARE_OP               ==
          782_784  POP_JUMP_IF_TRUE    796  'to 796'
              786  LOAD_FAST                'CrystalType'
              788  LOAD_STR                 'i'
              790  COMPARE_OP               ==
          792_794  POP_JUMP_IF_FALSE  2650  'to 2650'
            796_0  COME_FROM           782  '782'

 L. 109       796  LOAD_CONST               1
              798  LOAD_CONST               2
              800  LOAD_CONST               2
              802  LOAD_CONST               0
              804  LOAD_CONST               0
              806  LOAD_CONST               0
              808  LOAD_CONST               1
              810  LOAD_CONST               2
              812  LOAD_CONST               0
              814  LOAD_CONST               0
              816  LOAD_CONST               0
              818  LOAD_CONST               1
              820  LOAD_CONST               0
              822  LOAD_CONST               0
              824  LOAD_CONST               0
              826  LOAD_FAST                'A'
              828  LOAD_CONST               0
              830  LOAD_CONST               0
              832  LOAD_FAST                'A'
              834  LOAD_CONST               0
              836  LOAD_FAST                'A'
              838  BUILD_LIST_21        21 
              840  STORE_FAST               'CoefInd'
          842_844  JUMP_FORWARD       2650  'to 2650'
            846_0  COME_FROM            14  '14'

 L. 110       846  LOAD_FAST                'Ord'
              848  LOAD_CONST               3
              850  COMPARE_OP               ==
          852_854  POP_JUMP_IF_FALSE  2650  'to 2650'

 L. 111       856  LOAD_CONST               1
              858  LOAD_CONST               2
              860  LOAD_CONST               22
              862  BUILD_LIST_3          3 
              864  STORE_FAST               'A'

 L. 111       866  LOAD_CONST               5
              868  LOAD_CONST               1
              870  BUILD_LIST_2          2 
              872  STORE_FAST               'B'

 L. 111       874  LOAD_CONST               4
              876  LOAD_CONST               9
              878  BUILD_LIST_2          2 
              880  STORE_FAST               'C'

 L. 111       882  LOAD_CONST               1
              884  LOAD_CONST               2
              886  LOAD_CONST               22
              888  BUILD_LIST_3          3 
              890  STORE_FAST               'D'

 L. 111       892  LOAD_CONST               4
              894  LOAD_CONST               9
              896  BUILD_LIST_2          2 
              898  STORE_FAST               'E'

 L. 111       900  LOAD_CONST               5
              902  LOAD_CONST               10
              904  BUILD_LIST_2          2 
              906  STORE_FAST               'F'

 L. 111       908  LOAD_CONST               5
              910  LOAD_CONST               10
              912  BUILD_LIST_2          2 
              914  STORE_FAST               'G'

 L. 112       916  LOAD_CONST               4
              918  LOAD_CONST               9
              920  BUILD_LIST_2          2 
              922  STORE_FAST               'H'

 L. 112       924  LOAD_CONST               1
              926  LOAD_CONST               2
              928  LOAD_CONST               22
              930  BUILD_LIST_3          3 
              932  STORE_FAST               'I'

 L. 112       934  LOAD_CONST               3
              936  LOAD_CONST               8
              938  BUILD_LIST_2          2 
              940  STORE_FAST               'J'

 L. 112       942  LOAD_CONST               16
              944  LOAD_CONST               19
              946  BUILD_LIST_2          2 
              948  STORE_FAST               'K'

 L. 112       950  LOAD_CONST               2
              952  LOAD_CONST               8
              954  BUILD_LIST_2          2 
              956  STORE_FAST               'L'

 L. 112       958  LOAD_CONST               1
              960  LOAD_CONST               2
              962  BUILD_LIST_2          2 
              964  STORE_FAST               'M'

 L. 112       966  LOAD_CONST               1
              968  LOAD_CONST               2
              970  LOAD_CONST               8
              972  BUILD_LIST_3          3 
              974  STORE_FAST               'N'

 L. 113       976  LOAD_FAST                'CrystalType'
              978  LOAD_STR                 'triclinic'
              980  COMPARE_OP               ==
          982_984  POP_JUMP_IF_TRUE    996  'to 996'
              986  LOAD_FAST                'CrystalType'
              988  LOAD_STR                 'n'
              990  COMPARE_OP               ==
          992_994  POP_JUMP_IF_FALSE  1116  'to 1116'
            996_0  COME_FROM           982  '982'

 L. 114       996  LOAD_CONST               1
              998  LOAD_CONST               2
             1000  LOAD_CONST               3
             1002  LOAD_CONST               4
             1004  LOAD_CONST               5
             1006  LOAD_CONST               6
             1008  LOAD_CONST               7
             1010  LOAD_CONST               8
             1012  LOAD_CONST               9
             1014  LOAD_CONST               10
             1016  LOAD_CONST               11
             1018  LOAD_CONST               12
             1020  LOAD_CONST               13
             1022  LOAD_CONST               14
             1024  LOAD_CONST               15
             1026  LOAD_CONST               16
             1028  LOAD_CONST               17
             1030  LOAD_CONST               18
             1032  LOAD_CONST               19
             1034  LOAD_CONST               20
             1036  LOAD_CONST               21
             1038  LOAD_CONST               22
             1040  LOAD_CONST               23
             1042  LOAD_CONST               24
             1044  LOAD_CONST               25
             1046  LOAD_CONST               26
             1048  LOAD_CONST               27
             1050  LOAD_CONST               28

 L. 115      1052  LOAD_CONST               29

 L. 115      1054  LOAD_CONST               30

 L. 115      1056  LOAD_CONST               31

 L. 115      1058  LOAD_CONST               32

 L. 115      1060  LOAD_CONST               33

 L. 115      1062  LOAD_CONST               34

 L. 115      1064  LOAD_CONST               35

 L. 115      1066  LOAD_CONST               36

 L. 115      1068  LOAD_CONST               37

 L. 115      1070  LOAD_CONST               38

 L. 115      1072  LOAD_CONST               39

 L. 115      1074  LOAD_CONST               40

 L. 115      1076  LOAD_CONST               41

 L. 115      1078  LOAD_CONST               42

 L. 115      1080  LOAD_CONST               43

 L. 115      1082  LOAD_CONST               44

 L. 115      1084  LOAD_CONST               45

 L. 115      1086  LOAD_CONST               46

 L. 115      1088  LOAD_CONST               47

 L. 115      1090  LOAD_CONST               48

 L. 115      1092  LOAD_CONST               49

 L. 115      1094  LOAD_CONST               50

 L. 115      1096  LOAD_CONST               51

 L. 115      1098  LOAD_CONST               52

 L. 115      1100  LOAD_CONST               53

 L. 115      1102  LOAD_CONST               54

 L. 115      1104  LOAD_CONST               55

 L. 115      1106  LOAD_CONST               56

 L. 114      1108  BUILD_LIST_56        56 
             1110  STORE_FAST               'CoefInd'
         1112_1114  JUMP_FORWARD       2650  'to 2650'
           1116_0  COME_FROM           992  '992'

 L. 116      1116  LOAD_FAST                'CrystalType'
             1118  LOAD_STR                 'monoclinic'
             1120  COMPARE_OP               ==
         1122_1124  POP_JUMP_IF_TRUE   1136  'to 1136'
             1126  LOAD_FAST                'CrystalType'
             1128  LOAD_STR                 'm'
             1130  COMPARE_OP               ==
         1132_1134  POP_JUMP_IF_FALSE  1256  'to 1256'
           1136_0  COME_FROM          1122  '1122'

 L. 117      1136  LOAD_CONST               1
             1138  LOAD_CONST               2
             1140  LOAD_CONST               3
             1142  LOAD_CONST               0
             1144  LOAD_CONST               5
             1146  LOAD_CONST               0
             1148  LOAD_CONST               7
             1150  LOAD_CONST               8
             1152  LOAD_CONST               0
             1154  LOAD_CONST               10
             1156  LOAD_CONST               0
             1158  LOAD_CONST               12
             1160  LOAD_CONST               0
             1162  LOAD_CONST               14
             1164  LOAD_CONST               0
             1166  LOAD_CONST               16
             1168  LOAD_CONST               0
             1170  LOAD_CONST               18
             1172  LOAD_CONST               19
             1174  LOAD_CONST               0
             1176  LOAD_CONST               21
             1178  LOAD_CONST               22
             1180  LOAD_CONST               23
             1182  LOAD_CONST               0
             1184  LOAD_CONST               25
             1186  LOAD_CONST               0
             1188  LOAD_CONST               27

 L. 118      1190  LOAD_CONST               0

 L. 118      1192  LOAD_CONST               29

 L. 118      1194  LOAD_CONST               0

 L. 118      1196  LOAD_CONST               31

 L. 118      1198  LOAD_CONST               0

 L. 118      1200  LOAD_CONST               33

 L. 118      1202  LOAD_CONST               34

 L. 118      1204  LOAD_CONST               0

 L. 118      1206  LOAD_CONST               36

 L. 118      1208  LOAD_CONST               37

 L. 118      1210  LOAD_CONST               0

 L. 118      1212  LOAD_CONST               39

 L. 118      1214  LOAD_CONST               0

 L. 118      1216  LOAD_CONST               41

 L. 118      1218  LOAD_CONST               0

 L. 118      1220  LOAD_CONST               43

 L. 118      1222  LOAD_CONST               44

 L. 118      1224  LOAD_CONST               0

 L. 118      1226  LOAD_CONST               46

 L. 118      1228  LOAD_CONST               0

 L. 118      1230  LOAD_CONST               48

 L. 118      1232  LOAD_CONST               0

 L. 118      1234  LOAD_CONST               0

 L. 118      1236  LOAD_CONST               51

 L. 118      1238  LOAD_CONST               0

 L. 118      1240  LOAD_CONST               53

 L. 118      1242  LOAD_CONST               0

 L. 118      1244  LOAD_CONST               55

 L. 118      1246  LOAD_CONST               0

 L. 117      1248  BUILD_LIST_56        56 
             1250  STORE_FAST               'CoefInd'
         1252_1254  JUMP_FORWARD       2650  'to 2650'
           1256_0  COME_FROM          1132  '1132'

 L. 119      1256  LOAD_FAST                'CrystalType'
             1258  LOAD_STR                 'orthorhombic'
             1260  COMPARE_OP               ==
         1262_1264  POP_JUMP_IF_TRUE   1276  'to 1276'
             1266  LOAD_FAST                'CrystalType'
             1268  LOAD_STR                 'o'
             1270  COMPARE_OP               ==
         1272_1274  POP_JUMP_IF_FALSE  1396  'to 1396'
           1276_0  COME_FROM          1262  '1262'

 L. 120      1276  LOAD_CONST               1
             1278  LOAD_CONST               2
             1280  LOAD_CONST               3
             1282  LOAD_CONST               0
             1284  LOAD_CONST               0
             1286  LOAD_CONST               0
             1288  LOAD_CONST               7
             1290  LOAD_CONST               8
             1292  LOAD_CONST               0
             1294  LOAD_CONST               0
             1296  LOAD_CONST               0
             1298  LOAD_CONST               12
             1300  LOAD_CONST               0
             1302  LOAD_CONST               0
             1304  LOAD_CONST               0
             1306  LOAD_CONST               16
             1308  LOAD_CONST               0
             1310  LOAD_CONST               0
             1312  LOAD_CONST               19
             1314  LOAD_CONST               0
             1316  LOAD_CONST               21
             1318  LOAD_CONST               22
             1320  LOAD_CONST               23
             1322  LOAD_CONST               0
             1324  LOAD_CONST               0
             1326  LOAD_CONST               0
             1328  LOAD_CONST               27
             1330  LOAD_CONST               0
             1332  LOAD_CONST               0

 L. 121      1334  LOAD_CONST               0

 L. 121      1336  LOAD_CONST               31

 L. 121      1338  LOAD_CONST               0

 L. 121      1340  LOAD_CONST               0

 L. 121      1342  LOAD_CONST               34

 L. 121      1344  LOAD_CONST               0

 L. 121      1346  LOAD_CONST               36

 L. 121      1348  LOAD_CONST               37

 L. 121      1350  LOAD_CONST               0

 L. 121      1352  LOAD_CONST               0

 L. 121      1354  LOAD_CONST               0

 L. 121      1356  LOAD_CONST               41

 L. 121      1358  LOAD_CONST               0

 L. 121      1360  LOAD_CONST               0

 L. 121      1362  LOAD_CONST               44

 L. 121      1364  LOAD_CONST               0

 L. 121      1366  LOAD_CONST               46

 L. 121      1368  LOAD_CONST               0

 L. 121      1370  LOAD_CONST               0

 L. 121      1372  LOAD_CONST               0

 L. 121      1374  LOAD_CONST               0

 L. 121      1376  LOAD_CONST               51

 L. 121      1378  LOAD_CONST               0

 L. 121      1380  LOAD_CONST               0

 L. 121      1382  LOAD_CONST               0

 L. 121      1384  LOAD_CONST               0

 L. 121      1386  LOAD_CONST               0

 L. 120      1388  BUILD_LIST_56        56 
             1390  STORE_FAST               'CoefInd'
         1392_1394  JUMP_FORWARD       2650  'to 2650'
           1396_0  COME_FROM          1272  '1272'

 L. 122      1396  LOAD_FAST                'CrystalType'
             1398  LOAD_STR                 'tetragonal2'
             1400  COMPARE_OP               ==
         1402_1404  POP_JUMP_IF_TRUE   1416  'to 1416'
             1406  LOAD_FAST                'CrystalType'
             1408  LOAD_STR                 't2'
             1410  COMPARE_OP               ==
         1412_1414  POP_JUMP_IF_FALSE  1536  'to 1536'
           1416_0  COME_FROM          1402  '1402'

 L. 123      1416  LOAD_CONST               1
             1418  LOAD_CONST               2
             1420  LOAD_CONST               3
             1422  LOAD_CONST               0
             1424  LOAD_CONST               0
             1426  LOAD_CONST               6
             1428  LOAD_CONST               2
             1430  LOAD_CONST               8
             1432  LOAD_CONST               0
             1434  LOAD_CONST               0
             1436  LOAD_CONST               0
             1438  LOAD_CONST               12
             1440  LOAD_CONST               0
             1442  LOAD_CONST               0
             1444  LOAD_CONST               15
             1446  LOAD_CONST               16
             1448  LOAD_CONST               17
             1450  LOAD_CONST               0
             1452  LOAD_CONST               19
             1454  LOAD_CONST               0
             1456  LOAD_CONST               21
             1458  LOAD_CONST               1
             1460  LOAD_CONST               3
             1462  LOAD_CONST               0
             1464  LOAD_CONST               0
             1466  LOAD_CONST               6
             1468  LOAD_CONST               12
             1470  LOAD_CONST               0
             1472  LOAD_CONST               0

 L. 124      1474  LOAD_CONST               15

 L. 124      1476  LOAD_CONST               19

 L. 124      1478  LOAD_CONST               17

 L. 124      1480  LOAD_CONST               0

 L. 124      1482  LOAD_CONST               16

 L. 124      1484  LOAD_CONST               0

 L. 124      1486  LOAD_CONST               21

 L. 124      1488  LOAD_CONST               37

 L. 124      1490  LOAD_CONST               0

 L. 124      1492  LOAD_CONST               0

 L. 124      1494  LOAD_CONST               0

 L. 124      1496  LOAD_CONST               41

 L. 124      1498  LOAD_CONST               0

 L. 124      1500  LOAD_CONST               0

 L. 124      1502  LOAD_CONST               41

 L. 124      1504  LOAD_CONST               0

 L. 124      1506  LOAD_CONST               46

 L. 124      1508  LOAD_CONST               0

 L. 124      1510  LOAD_CONST               0

 L. 124      1512  LOAD_CONST               49

 L. 124      1514  LOAD_CONST               0

 L. 124      1516  LOAD_CONST               51

 L. 124      1518  LOAD_CONST               0

 L. 124      1520  LOAD_CONST               0

 L. 124      1522  LOAD_CONST               49

 L. 124      1524  LOAD_CONST               0

 L. 124      1526  LOAD_CONST               0

 L. 123      1528  BUILD_LIST_56        56 
             1530  STORE_FAST               'CoefInd'
         1532_1534  JUMP_FORWARD       2650  'to 2650'
           1536_0  COME_FROM          1412  '1412'

 L. 125      1536  LOAD_FAST                'CrystalType'
             1538  LOAD_STR                 'tetragonal1'
             1540  COMPARE_OP               ==
         1542_1544  POP_JUMP_IF_TRUE   1556  'to 1556'
             1546  LOAD_FAST                'CrystalType'
             1548  LOAD_STR                 't1'
             1550  COMPARE_OP               ==
         1552_1554  POP_JUMP_IF_FALSE  1676  'to 1676'
           1556_0  COME_FROM          1542  '1542'

 L. 126      1556  LOAD_CONST               1
             1558  LOAD_CONST               2
             1560  LOAD_CONST               3
             1562  LOAD_CONST               0
             1564  LOAD_CONST               0
             1566  LOAD_CONST               0
             1568  LOAD_CONST               2
             1570  LOAD_CONST               8
             1572  LOAD_CONST               0
             1574  LOAD_CONST               0
             1576  LOAD_CONST               0
             1578  LOAD_CONST               12
             1580  LOAD_CONST               0
             1582  LOAD_CONST               0
             1584  LOAD_CONST               0
             1586  LOAD_CONST               16
             1588  LOAD_CONST               0
             1590  LOAD_CONST               0
             1592  LOAD_CONST               19
             1594  LOAD_CONST               0
             1596  LOAD_CONST               21
             1598  LOAD_CONST               1
             1600  LOAD_CONST               3
             1602  LOAD_CONST               0
             1604  LOAD_CONST               0
             1606  LOAD_CONST               0
             1608  LOAD_CONST               12
             1610  LOAD_CONST               0
             1612  LOAD_CONST               0
             1614  LOAD_CONST               0

 L. 127      1616  LOAD_CONST               19

 L. 127      1618  LOAD_CONST               0

 L. 127      1620  LOAD_CONST               0

 L. 127      1622  LOAD_CONST               16

 L. 127      1624  LOAD_CONST               0

 L. 127      1626  LOAD_CONST               21

 L. 127      1628  LOAD_CONST               37

 L. 127      1630  LOAD_CONST               0

 L. 127      1632  LOAD_CONST               0

 L. 127      1634  LOAD_CONST               0

 L. 127      1636  LOAD_CONST               41

 L. 127      1638  LOAD_CONST               0

 L. 127      1640  LOAD_CONST               0

 L. 127      1642  LOAD_CONST               41

 L. 127      1644  LOAD_CONST               0

 L. 127      1646  LOAD_CONST               46

 L. 127      1648  LOAD_CONST               0

 L. 127      1650  LOAD_CONST               0

 L. 127      1652  LOAD_CONST               0

 L. 127      1654  LOAD_CONST               0

 L. 127      1656  LOAD_CONST               51

 L. 127      1658  LOAD_CONST               0

 L. 127      1660  LOAD_CONST               0

 L. 127      1662  LOAD_CONST               0

 L. 127      1664  LOAD_CONST               0

 L. 127      1666  LOAD_CONST               0

 L. 126      1668  BUILD_LIST_56        56 
             1670  STORE_FAST               'CoefInd'
         1672_1674  JUMP_FORWARD       2650  'to 2650'
           1676_0  COME_FROM          1552  '1552'

 L. 128      1676  LOAD_FAST                'CrystalType'
             1678  LOAD_STR                 'rhombohedral2'
             1680  COMPARE_OP               ==
         1682_1684  POP_JUMP_IF_TRUE   1696  'to 1696'
             1686  LOAD_FAST                'CrystalType'
             1688  LOAD_STR                 'r2'
             1690  COMPARE_OP               ==
         1692_1694  POP_JUMP_IF_FALSE  1816  'to 1816'
           1696_0  COME_FROM          1682  '1682'

 L. 129      1696  LOAD_CONST               1
             1698  LOAD_CONST               2
             1700  LOAD_CONST               3
             1702  LOAD_CONST               4
             1704  LOAD_CONST               5
             1706  LOAD_CONST               6
             1708  LOAD_FAST                'A'
             1710  LOAD_CONST               8
             1712  LOAD_CONST               9
             1714  LOAD_CONST               10
             1716  LOAD_CONST               6
             1718  LOAD_CONST               12
             1720  LOAD_CONST               13
             1722  LOAD_CONST               14
             1724  LOAD_CONST               0
             1726  LOAD_CONST               16
             1728  LOAD_CONST               17
             1730  LOAD_FAST                'B'
             1732  LOAD_CONST               19
             1734  LOAD_FAST                'C'
             1736  LOAD_FAST                'D'
             1738  LOAD_CONST               22
             1740  LOAD_CONST               3
             1742  LOAD_FAST                'E'
             1744  LOAD_FAST                'F'
             1746  LOAD_CONST               6
             1748  LOAD_CONST               12
             1750  LOAD_CONST               13

 L. 130      1752  LOAD_CONST               14

 L. 130      1754  LOAD_CONST               0

 L. 130      1756  LOAD_CONST               19

 L. 130      1758  LOAD_CONST               17

 L. 130      1760  LOAD_FAST                'G'

 L. 130      1762  LOAD_CONST               16

 L. 130      1764  LOAD_FAST                'H'

 L. 130      1766  LOAD_FAST                'I'

 L. 130      1768  LOAD_CONST               37

 L. 130      1770  LOAD_CONST               0

 L. 130      1772  LOAD_CONST               0

 L. 130      1774  LOAD_CONST               0

 L. 130      1776  LOAD_CONST               41

 L. 130      1778  LOAD_CONST               0

 L. 130      1780  LOAD_CONST               14

 L. 130      1782  LOAD_CONST               41

 L. 130      1784  LOAD_CONST               13

 L. 130      1786  LOAD_FAST                'J'

 L. 130      1788  LOAD_CONST               47

 L. 130      1790  LOAD_CONST               48

 L. 130      1792  LOAD_CONST               17

 L. 130      1794  LOAD_CONST               47

 L. 130      1796  LOAD_FAST                'K'

 L. 130      1798  LOAD_CONST               9

 L. 130      1800  LOAD_CONST               48

 L. 130      1802  LOAD_CONST               17

 L. 130      1804  LOAD_CONST               10

 L. 130      1806  LOAD_CONST               6

 L. 129      1808  BUILD_LIST_56        56 
             1810  STORE_FAST               'CoefInd'
         1812_1814  JUMP_FORWARD       2650  'to 2650'
           1816_0  COME_FROM          1692  '1692'

 L. 131      1816  LOAD_FAST                'CrystalType'
             1818  LOAD_STR                 'rhombohedral1'
             1820  COMPARE_OP               ==
         1822_1824  POP_JUMP_IF_TRUE   1836  'to 1836'
             1826  LOAD_FAST                'CrystalType'
             1828  LOAD_STR                 'r1'
             1830  COMPARE_OP               ==
         1832_1834  POP_JUMP_IF_FALSE  1956  'to 1956'
           1836_0  COME_FROM          1822  '1822'

 L. 132      1836  LOAD_CONST               1
             1838  LOAD_CONST               2
             1840  LOAD_CONST               3
             1842  LOAD_CONST               4
             1844  LOAD_CONST               0
             1846  LOAD_CONST               0
             1848  LOAD_FAST                'A'
             1850  LOAD_CONST               8
             1852  LOAD_CONST               9
             1854  LOAD_CONST               0
             1856  LOAD_CONST               0
             1858  LOAD_CONST               12
             1860  LOAD_CONST               13
             1862  LOAD_CONST               0
             1864  LOAD_CONST               0
             1866  LOAD_CONST               16
             1868  LOAD_CONST               0
             1870  LOAD_CONST               0
             1872  LOAD_CONST               19
             1874  LOAD_FAST                'C'
             1876  LOAD_FAST                'D'
             1878  LOAD_CONST               22
             1880  LOAD_CONST               3
             1882  LOAD_FAST                'E'
             1884  LOAD_CONST               0
             1886  LOAD_CONST               0
             1888  LOAD_CONST               12
             1890  LOAD_CONST               13
             1892  LOAD_CONST               0
             1894  LOAD_CONST               0

 L. 133      1896  LOAD_CONST               19

 L. 133      1898  LOAD_CONST               0

 L. 133      1900  LOAD_CONST               0

 L. 133      1902  LOAD_CONST               16

 L. 133      1904  LOAD_FAST                'H'

 L. 133      1906  LOAD_FAST                'I'

 L. 133      1908  LOAD_CONST               37

 L. 133      1910  LOAD_CONST               0

 L. 133      1912  LOAD_CONST               0

 L. 133      1914  LOAD_CONST               0

 L. 133      1916  LOAD_CONST               41

 L. 133      1918  LOAD_CONST               0

 L. 133      1920  LOAD_CONST               0

 L. 133      1922  LOAD_CONST               41

 L. 133      1924  LOAD_CONST               13

 L. 133      1926  LOAD_FAST                'J'

 L. 133      1928  LOAD_CONST               47

 L. 133      1930  LOAD_CONST               0

 L. 133      1932  LOAD_CONST               0

 L. 133      1934  LOAD_CONST               47

 L. 133      1936  LOAD_FAST                'K'

 L. 133      1938  LOAD_CONST               9

 L. 133      1940  LOAD_CONST               0

 L. 133      1942  LOAD_CONST               0

 L. 133      1944  LOAD_CONST               0

 L. 133      1946  LOAD_CONST               0

 L. 132      1948  BUILD_LIST_56        56 
             1950  STORE_FAST               'CoefInd'
         1952_1954  JUMP_FORWARD       2650  'to 2650'
           1956_0  COME_FROM          1832  '1832'

 L. 134      1956  LOAD_FAST                'CrystalType'
             1958  LOAD_STR                 'hexagonal2'
             1960  COMPARE_OP               ==
         1962_1964  POP_JUMP_IF_TRUE   1976  'to 1976'
             1966  LOAD_FAST                'CrystalType'
             1968  LOAD_STR                 'h2'
             1970  COMPARE_OP               ==
         1972_1974  POP_JUMP_IF_FALSE  2096  'to 2096'
           1976_0  COME_FROM          1962  '1962'

 L. 135      1976  LOAD_CONST               1
             1978  LOAD_CONST               2
             1980  LOAD_CONST               3
             1982  LOAD_CONST               0
             1984  LOAD_CONST               0
             1986  LOAD_CONST               6
             1988  LOAD_FAST                'A'
             1990  LOAD_CONST               8
             1992  LOAD_CONST               0
             1994  LOAD_CONST               0
             1996  LOAD_CONST               6
             1998  LOAD_CONST               12
             2000  LOAD_CONST               0
             2002  LOAD_CONST               0
             2004  LOAD_CONST               0
             2006  LOAD_CONST               16
             2008  LOAD_CONST               17
             2010  LOAD_CONST               0
             2012  LOAD_CONST               19
             2014  LOAD_CONST               0
             2016  LOAD_FAST                'D'
             2018  LOAD_CONST               22
             2020  LOAD_CONST               3
             2022  LOAD_CONST               0
             2024  LOAD_CONST               0
             2026  LOAD_CONST               6
             2028  LOAD_CONST               12
             2030  LOAD_CONST               0
             2032  LOAD_CONST               0
             2034  LOAD_CONST               0

 L. 136      2036  LOAD_CONST               19

 L. 136      2038  LOAD_CONST               17

 L. 136      2040  LOAD_CONST               0

 L. 136      2042  LOAD_CONST               16

 L. 136      2044  LOAD_CONST               0

 L. 136      2046  LOAD_FAST                'I'

 L. 136      2048  LOAD_CONST               37

 L. 136      2050  LOAD_CONST               0

 L. 136      2052  LOAD_CONST               0

 L. 136      2054  LOAD_CONST               0

 L. 136      2056  LOAD_CONST               41

 L. 136      2058  LOAD_CONST               0

 L. 136      2060  LOAD_CONST               0

 L. 136      2062  LOAD_CONST               41

 L. 136      2064  LOAD_CONST               0

 L. 136      2066  LOAD_FAST                'J'

 L. 136      2068  LOAD_CONST               0

 L. 136      2070  LOAD_CONST               0

 L. 136      2072  LOAD_CONST               17

 L. 136      2074  LOAD_CONST               0

 L. 136      2076  LOAD_FAST                'K'

 L. 136      2078  LOAD_CONST               0

 L. 136      2080  LOAD_CONST               0

 L. 136      2082  LOAD_CONST               17

 L. 136      2084  LOAD_CONST               0

 L. 136      2086  LOAD_CONST               6

 L. 135      2088  BUILD_LIST_56        56 
             2090  STORE_FAST               'CoefInd'
         2092_2094  JUMP_FORWARD       2650  'to 2650'
           2096_0  COME_FROM          1972  '1972'

 L. 137      2096  LOAD_FAST                'CrystalType'
             2098  LOAD_STR                 'hexagonal1'
             2100  COMPARE_OP               ==
         2102_2104  POP_JUMP_IF_TRUE   2116  'to 2116'
             2106  LOAD_FAST                'CrystalType'
             2108  LOAD_STR                 'h1'
             2110  COMPARE_OP               ==
         2112_2114  POP_JUMP_IF_FALSE  2236  'to 2236'
           2116_0  COME_FROM          2102  '2102'

 L. 138      2116  LOAD_CONST               1
             2118  LOAD_CONST               2
             2120  LOAD_CONST               3
             2122  LOAD_CONST               0
             2124  LOAD_CONST               0
             2126  LOAD_CONST               0
             2128  LOAD_FAST                'A'
             2130  LOAD_CONST               8
             2132  LOAD_CONST               0
             2134  LOAD_CONST               0
             2136  LOAD_CONST               0
             2138  LOAD_CONST               12
             2140  LOAD_CONST               0
             2142  LOAD_CONST               0
             2144  LOAD_CONST               0
             2146  LOAD_CONST               16
             2148  LOAD_CONST               0
             2150  LOAD_CONST               0
             2152  LOAD_CONST               19
             2154  LOAD_CONST               0
             2156  LOAD_FAST                'D'
             2158  LOAD_CONST               22
             2160  LOAD_CONST               3
             2162  LOAD_CONST               0
             2164  LOAD_CONST               0
             2166  LOAD_CONST               0
             2168  LOAD_CONST               12
             2170  LOAD_CONST               0
             2172  LOAD_CONST               0
             2174  LOAD_CONST               0

 L. 139      2176  LOAD_CONST               19

 L. 139      2178  LOAD_CONST               0

 L. 139      2180  LOAD_CONST               0

 L. 139      2182  LOAD_CONST               16

 L. 139      2184  LOAD_CONST               0

 L. 139      2186  LOAD_FAST                'I'

 L. 139      2188  LOAD_CONST               37

 L. 139      2190  LOAD_CONST               0

 L. 139      2192  LOAD_CONST               0

 L. 139      2194  LOAD_CONST               0

 L. 139      2196  LOAD_CONST               41

 L. 139      2198  LOAD_CONST               0

 L. 139      2200  LOAD_CONST               0

 L. 139      2202  LOAD_CONST               41

 L. 139      2204  LOAD_CONST               0

 L. 139      2206  LOAD_FAST                'J'

 L. 139      2208  LOAD_CONST               0

 L. 139      2210  LOAD_CONST               0

 L. 139      2212  LOAD_CONST               0

 L. 139      2214  LOAD_CONST               0

 L. 139      2216  LOAD_FAST                'K'

 L. 139      2218  LOAD_CONST               0

 L. 139      2220  LOAD_CONST               0

 L. 139      2222  LOAD_CONST               0

 L. 139      2224  LOAD_CONST               0

 L. 139      2226  LOAD_CONST               0

 L. 138      2228  BUILD_LIST_56        56 
             2230  STORE_FAST               'CoefInd'
         2232_2234  JUMP_FORWARD       2650  'to 2650'
           2236_0  COME_FROM          2112  '2112'

 L. 140      2236  LOAD_FAST                'CrystalType'
             2238  LOAD_STR                 'cubic2'
             2240  COMPARE_OP               ==
         2242_2244  POP_JUMP_IF_TRUE   2256  'to 2256'
             2246  LOAD_FAST                'CrystalType'
             2248  LOAD_STR                 'c2'
             2250  COMPARE_OP               ==
         2252_2254  POP_JUMP_IF_FALSE  2376  'to 2376'
           2256_0  COME_FROM          2242  '2242'

 L. 141      2256  LOAD_CONST               1
             2258  LOAD_CONST               2
             2260  LOAD_CONST               3
             2262  LOAD_CONST               0
             2264  LOAD_CONST               0
             2266  LOAD_CONST               0
             2268  LOAD_CONST               3
             2270  LOAD_CONST               8
             2272  LOAD_CONST               0
             2274  LOAD_CONST               0
             2276  LOAD_CONST               0
             2278  LOAD_CONST               2
             2280  LOAD_CONST               0
             2282  LOAD_CONST               0
             2284  LOAD_CONST               0
             2286  LOAD_CONST               16
             2288  LOAD_CONST               0
             2290  LOAD_CONST               0
             2292  LOAD_CONST               19
             2294  LOAD_CONST               0
             2296  LOAD_CONST               21
             2298  LOAD_CONST               1
             2300  LOAD_CONST               2
             2302  LOAD_CONST               0
             2304  LOAD_CONST               0
             2306  LOAD_CONST               0
             2308  LOAD_CONST               3
             2310  LOAD_CONST               0
             2312  LOAD_CONST               0
             2314  LOAD_CONST               0
             2316  LOAD_CONST               21

 L. 142      2318  LOAD_CONST               0

 L. 142      2320  LOAD_CONST               0

 L. 142      2322  LOAD_CONST               16

 L. 142      2324  LOAD_CONST               0

 L. 142      2326  LOAD_CONST               19

 L. 142      2328  LOAD_CONST               1

 L. 142      2330  LOAD_CONST               0

 L. 142      2332  LOAD_CONST               0

 L. 142      2334  LOAD_CONST               0

 L. 142      2336  LOAD_CONST               19

 L. 142      2338  LOAD_CONST               0

 L. 142      2340  LOAD_CONST               0

 L. 142      2342  LOAD_CONST               21

 L. 142      2344  LOAD_CONST               0

 L. 142      2346  LOAD_CONST               16

 L. 142      2348  LOAD_CONST               0

 L. 142      2350  LOAD_CONST               0

 L. 142      2352  LOAD_CONST               0

 L. 142      2354  LOAD_CONST               0

 L. 142      2356  LOAD_CONST               51

 L. 142      2358  LOAD_CONST               0

 L. 142      2360  LOAD_CONST               0

 L. 142      2362  LOAD_CONST               0

 L. 142      2364  LOAD_CONST               0

 L. 142      2366  LOAD_CONST               0

 L. 141      2368  BUILD_LIST_56        56 
             2370  STORE_FAST               'CoefInd'
         2372_2374  JUMP_FORWARD       2650  'to 2650'
           2376_0  COME_FROM          2252  '2252'

 L. 143      2376  LOAD_FAST                'CrystalType'
             2378  LOAD_STR                 'cubic1'
             2380  COMPARE_OP               ==
         2382_2384  POP_JUMP_IF_TRUE   2396  'to 2396'
             2386  LOAD_FAST                'CrystalType'
             2388  LOAD_STR                 'c1'
             2390  COMPARE_OP               ==
         2392_2394  POP_JUMP_IF_FALSE  2514  'to 2514'
           2396_0  COME_FROM          2382  '2382'

 L. 144      2396  LOAD_CONST               1
             2398  LOAD_CONST               2
             2400  LOAD_CONST               2
             2402  LOAD_CONST               0
             2404  LOAD_CONST               0
             2406  LOAD_CONST               0
             2408  LOAD_CONST               2
             2410  LOAD_CONST               8
             2412  LOAD_CONST               0
             2414  LOAD_CONST               0
             2416  LOAD_CONST               0
             2418  LOAD_CONST               2
             2420  LOAD_CONST               0
             2422  LOAD_CONST               0
             2424  LOAD_CONST               0
             2426  LOAD_CONST               16
             2428  LOAD_CONST               0
             2430  LOAD_CONST               0
             2432  LOAD_CONST               19
             2434  LOAD_CONST               0
             2436  LOAD_CONST               19
             2438  LOAD_CONST               1
             2440  LOAD_CONST               2
             2442  LOAD_CONST               0
           2444_0  COME_FROM           638  '638'
             2444  LOAD_CONST               0
             2446  LOAD_CONST               0
             2448  LOAD_CONST               2
             2450  LOAD_CONST               0
             2452  LOAD_CONST               0
             2454  LOAD_CONST               0
             2456  LOAD_CONST               19

 L. 145      2458  LOAD_CONST               0

 L. 145      2460  LOAD_CONST               0

 L. 145      2462  LOAD_CONST               16

 L. 145      2464  LOAD_CONST               0

 L. 145      2466  LOAD_CONST               19

 L. 145      2468  LOAD_CONST               1

 L. 145      2470  LOAD_CONST               0

 L. 145      2472  LOAD_CONST               0

 L. 145      2474  LOAD_CONST               0

 L. 145      2476  LOAD_CONST               19

 L. 145      2478  LOAD_CONST               0

 L. 145      2480  LOAD_CONST               0

 L. 145      2482  LOAD_CONST               19

 L. 145      2484  LOAD_CONST               0

 L. 145      2486  LOAD_CONST               16

 L. 145      2488  LOAD_CONST               0

 L. 145      2490  LOAD_CONST               0

 L. 145      2492  LOAD_CONST               0

 L. 145      2494  LOAD_CONST               0

 L. 145      2496  LOAD_CONST               51

 L. 145      2498  LOAD_CONST               0

 L. 145      2500  LOAD_CONST               0

 L. 145      2502  LOAD_CONST               0

 L. 145      2504  LOAD_CONST               0

 L. 145      2506  LOAD_CONST               0

 L. 144      2508  BUILD_LIST_56        56 
             2510  STORE_FAST               'CoefInd'
           2512_0  COME_FROM           706  '706'
             2512  JUMP_FORWARD       2650  'to 2650'
           2514_0  COME_FROM          2392  '2392'

 L. 146      2514  LOAD_FAST                'CrystalType'
             2516  LOAD_STR                 'isotropic'
             2518  COMPARE_OP               ==
         2520_2522  POP_JUMP_IF_TRUE   2534  'to 2534'
             2524  LOAD_FAST                'CrystalType'
             2526  LOAD_STR                 'i'
             2528  COMPARE_OP               ==
         2530_2532  POP_JUMP_IF_FALSE  2650  'to 2650'
           2534_0  COME_FROM          2520  '2520'

 L. 147      2534  LOAD_CONST               1
             2536  LOAD_CONST               2
             2538  LOAD_CONST               2
             2540  LOAD_CONST               0
             2542  LOAD_CONST               0
             2544  LOAD_CONST               0
             2546  LOAD_CONST               2
             2548  LOAD_CONST               8
             2550  LOAD_CONST               0
             2552  LOAD_CONST               0
             2554  LOAD_CONST               0
             2556  LOAD_CONST               2
             2558  LOAD_CONST               0
             2560  LOAD_CONST               0
             2562  LOAD_CONST               0
             2564  LOAD_FAST                'L'
             2566  LOAD_CONST               0
             2568  LOAD_CONST               0
             2570  LOAD_FAST                'M'
             2572  LOAD_CONST               0
             2574  LOAD_FAST                'M'
             2576  LOAD_CONST               1
             2578  LOAD_CONST               2
           2580_0  COME_FROM           774  '774'
             2580  LOAD_CONST               0
             2582  LOAD_CONST               0
             2584  LOAD_CONST               0
             2586  LOAD_CONST               2
             2588  LOAD_CONST               0
             2590  LOAD_CONST               0
             2592  LOAD_CONST               0
             2594  LOAD_FAST                'M'
             2596  LOAD_CONST               0
             2598  LOAD_CONST               0

 L. 148      2600  LOAD_FAST                'L'

 L. 148      2602  LOAD_CONST               0

 L. 148      2604  LOAD_FAST                'M'

 L. 148      2606  LOAD_CONST               1

 L. 148      2608  LOAD_CONST               0

 L. 148      2610  LOAD_CONST               0

 L. 148      2612  LOAD_CONST               0

 L. 148      2614  LOAD_FAST                'M'

 L. 148      2616  LOAD_CONST               0

 L. 148      2618  LOAD_CONST               0

 L. 148      2620  LOAD_FAST                'M'

 L. 148      2622  LOAD_CONST               0

 L. 148      2624  LOAD_FAST                'L'

 L. 148      2626  LOAD_CONST               0

 L. 148      2628  LOAD_CONST               0

 L. 148      2630  LOAD_CONST               0

 L. 148      2632  LOAD_CONST               0

 L. 148      2634  LOAD_FAST                'N'

 L. 148      2636  LOAD_CONST               0

 L. 148      2638  LOAD_CONST               0

 L. 148      2640  LOAD_CONST               0

 L. 148      2642  LOAD_CONST               0

 L. 148      2644  LOAD_CONST               0

 L. 147      2646  BUILD_LIST_56        56 
             2648  STORE_FAST               'CoefInd'
           2650_0  COME_FROM          2530  '2530'
           2650_1  COME_FROM          2512  '2512'
           2650_2  COME_FROM          2372  '2372'
           2650_3  COME_FROM          2232  '2232'
           2650_4  COME_FROM          2092  '2092'
           2650_5  COME_FROM          1952  '1952'
           2650_6  COME_FROM          1812  '1812'
           2650_7  COME_FROM          1672  '1672'
           2650_8  COME_FROM          1532  '1532'
           2650_9  COME_FROM          1392  '1392'
          2650_10  COME_FROM          1252  '1252'
          2650_11  COME_FROM          1112  '1112'
          2650_12  COME_FROM           852  '852'
          2650_13  COME_FROM           842  '842'
          2650_14  COME_FROM           792  '792'

 L. 149      2650  LOAD_FAST                'CoefInd'
             2652  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM' instruction at offset 2444_0


def get_unique(CoefInd):
    n = len(CoefInd)
    CoefUniq = []
    for i in range(0, n):
        coefi = CoefInd[i]
        if type(coefi) is int:
            if coefi == 0:
                pass
            elif coefi not in CoefUniq:
                CoefUniq.append(coefi)
        return CoefUniq


def group2crytyp--- This code section failed: ---

 L. 168         0  LOAD_FAST                'group'
                2  LOAD_STR                 '1'
                4  COMPARE_OP               ==
                6  POP_JUMP_IF_TRUE     16  'to 16'
                8  LOAD_FAST                'group'
               10  LOAD_STR                 '-1'
               12  COMPARE_OP               ==
               14  POP_JUMP_IF_FALSE    24  'to 24'
             16_0  COME_FROM             6  '6'

 L. 169        16  LOAD_STR                 'triclinic'
               18  STORE_FAST               'CrystalType'
            20_22  JUMP_FORWARD        340  'to 340'
             24_0  COME_FROM            14  '14'

 L. 170        24  LOAD_FAST                'group'
               26  LOAD_STR                 '2'
               28  COMPARE_OP               ==
               30  POP_JUMP_IF_TRUE     48  'to 48'
               32  LOAD_FAST                'group'
               34  LOAD_STR                 'm'
               36  COMPARE_OP               ==
               38  POP_JUMP_IF_TRUE     48  'to 48'
               40  LOAD_FAST                'group'
               42  LOAD_STR                 '2/m'
               44  COMPARE_OP               ==
               46  POP_JUMP_IF_FALSE    56  'to 56'
             48_0  COME_FROM            38  '38'
             48_1  COME_FROM            30  '30'

 L. 171        48  LOAD_STR                 'monoclinic'
               50  STORE_FAST               'CrystalType'
            52_54  JUMP_FORWARD        340  'to 340'
             56_0  COME_FROM            46  '46'

 L. 172        56  LOAD_FAST                'group'
               58  LOAD_STR                 '222'
               60  COMPARE_OP               ==
               62  POP_JUMP_IF_TRUE     80  'to 80'
               64  LOAD_FAST                'group'
               66  LOAD_STR                 'mm2'
               68  COMPARE_OP               ==
               70  POP_JUMP_IF_TRUE     80  'to 80'
               72  LOAD_FAST                'group'
               74  LOAD_STR                 '222/mmm'
               76  COMPARE_OP               ==
               78  POP_JUMP_IF_FALSE    86  'to 86'
             80_0  COME_FROM            70  '70'
             80_1  COME_FROM            62  '62'

 L. 173        80  LOAD_STR                 'orthorhombic'
               82  STORE_FAST               'CrystalType'
               84  JUMP_FORWARD        340  'to 340'
             86_0  COME_FROM            78  '78'

 L. 174        86  LOAD_FAST                'group'
               88  LOAD_STR                 '4'
               90  COMPARE_OP               ==
               92  POP_JUMP_IF_TRUE    110  'to 110'
               94  LOAD_FAST                'group'
               96  LOAD_STR                 '-4'
               98  COMPARE_OP               ==
              100  POP_JUMP_IF_TRUE    110  'to 110'
              102  LOAD_FAST                'group'
              104  LOAD_STR                 '4/m'
              106  COMPARE_OP               ==
              108  POP_JUMP_IF_FALSE   116  'to 116'
            110_0  COME_FROM           100  '100'
            110_1  COME_FROM            92  '92'

 L. 175       110  LOAD_STR                 'tetragonal2'
              112  STORE_FAST               'CrystalType'
              114  JUMP_FORWARD        340  'to 340'
            116_0  COME_FROM           108  '108'

 L. 176       116  LOAD_FAST                'group'
              118  LOAD_STR                 '422'
              120  COMPARE_OP               ==
              122  POP_JUMP_IF_TRUE    148  'to 148'
              124  LOAD_FAST                'group'
              126  LOAD_STR                 '4mm'
              128  COMPARE_OP               ==
              130  POP_JUMP_IF_TRUE    148  'to 148'
              132  LOAD_FAST                'group'
              134  LOAD_STR                 '-42m'
              136  COMPARE_OP               ==
              138  POP_JUMP_IF_TRUE    148  'to 148'
              140  LOAD_FAST                'group'
              142  LOAD_STR                 '422/mmm'
              144  COMPARE_OP               ==
              146  POP_JUMP_IF_FALSE   154  'to 154'
            148_0  COME_FROM           138  '138'
            148_1  COME_FROM           130  '130'
            148_2  COME_FROM           122  '122'

 L. 177       148  LOAD_STR                 'tetragonal1'
              150  STORE_FAST               'CrystalType'
              152  JUMP_FORWARD        340  'to 340'
            154_0  COME_FROM           146  '146'

 L. 178       154  LOAD_FAST                'group'
              156  LOAD_STR                 '23'
              158  COMPARE_OP               ==
              160  POP_JUMP_IF_TRUE    170  'to 170'
              162  LOAD_FAST                'group'
              164  LOAD_STR                 '2/m-3'
              166  COMPARE_OP               ==
              168  POP_JUMP_IF_FALSE   176  'to 176'
            170_0  COME_FROM           160  '160'

 L. 179       170  LOAD_STR                 'cubic2'
              172  STORE_FAST               'CrystalType'
              174  JUMP_FORWARD        340  'to 340'
            176_0  COME_FROM           168  '168'

 L. 180       176  LOAD_FAST                'group'
              178  LOAD_STR                 '432'
              180  COMPARE_OP               ==
              182  POP_JUMP_IF_TRUE    200  'to 200'
              184  LOAD_FAST                'group'
              186  LOAD_STR                 '-43m'
              188  COMPARE_OP               ==
              190  POP_JUMP_IF_TRUE    200  'to 200'
              192  LOAD_FAST                'group'
              194  LOAD_STR                 '4/m-32/m'
              196  COMPARE_OP               ==
              198  POP_JUMP_IF_FALSE   206  'to 206'
            200_0  COME_FROM           190  '190'
            200_1  COME_FROM           182  '182'

 L. 181       200  LOAD_STR                 'cubic1'
              202  STORE_FAST               'CrystalType'
              204  JUMP_FORWARD        340  'to 340'
            206_0  COME_FROM           198  '198'

 L. 182       206  LOAD_FAST                'group'
              208  LOAD_STR                 '3'
              210  COMPARE_OP               ==
              212  POP_JUMP_IF_TRUE    222  'to 222'
              214  LOAD_FAST                'group'
              216  LOAD_STR                 '-3'
              218  COMPARE_OP               ==
              220  POP_JUMP_IF_FALSE   228  'to 228'
            222_0  COME_FROM           212  '212'

 L. 183       222  LOAD_STR                 'rhombohedral2'
              224  STORE_FAST               'CrystalType'
              226  JUMP_FORWARD        340  'to 340'
            228_0  COME_FROM           220  '220'

 L. 184       228  LOAD_FAST                'group'
              230  LOAD_STR                 '32'
              232  COMPARE_OP               ==
              234  POP_JUMP_IF_TRUE    254  'to 254'
              236  LOAD_FAST                'group'
              238  LOAD_STR                 '3m'
              240  COMPARE_OP               ==
              242  POP_JUMP_IF_TRUE    254  'to 254'
              244  LOAD_FAST                'group'
              246  LOAD_STR                 '-32/m'
              248  COMPARE_OP               ==
          250_252  POP_JUMP_IF_FALSE   260  'to 260'
            254_0  COME_FROM           242  '242'
            254_1  COME_FROM           234  '234'

 L. 185       254  LOAD_STR                 'rhombohedral1'
              256  STORE_FAST               'CrystalType'
              258  JUMP_FORWARD        340  'to 340'
            260_0  COME_FROM           250  '250'

 L. 186       260  LOAD_FAST                'group'
              262  LOAD_STR                 '6'
              264  COMPARE_OP               ==
          266_268  POP_JUMP_IF_TRUE    290  'to 290'
              270  LOAD_FAST                'group'
              272  LOAD_STR                 '-6'
              274  COMPARE_OP               ==
          276_278  POP_JUMP_IF_TRUE    290  'to 290'
              280  LOAD_FAST                'group'
              282  LOAD_STR                 '6/m'
              284  COMPARE_OP               ==
          286_288  POP_JUMP_IF_FALSE   296  'to 296'
            290_0  COME_FROM           276  '276'
            290_1  COME_FROM           266  '266'

 L. 187       290  LOAD_STR                 'hexagonal2'
              292  STORE_FAST               'CrystalType'
              294  JUMP_FORWARD        340  'to 340'
            296_0  COME_FROM           286  '286'

 L. 188       296  LOAD_FAST                'group'
              298  LOAD_STR                 '622'
              300  COMPARE_OP               ==
          302_304  POP_JUMP_IF_TRUE    336  'to 336'
              306  LOAD_FAST                'group'
              308  LOAD_STR                 '6mm'
              310  COMPARE_OP               ==
          312_314  POP_JUMP_IF_TRUE    336  'to 336'
              316  LOAD_FAST                'group'
              318  LOAD_STR                 '-6m2'
              320  COMPARE_OP               ==
          322_324  POP_JUMP_IF_TRUE    336  'to 336'
              326  LOAD_FAST                'group'
              328  LOAD_STR                 '622/mmm'
              330  COMPARE_OP               ==
          332_334  POP_JUMP_IF_FALSE   340  'to 340'
            336_0  COME_FROM           322  '322'
            336_1  COME_FROM           312  '312'
            336_2  COME_FROM           302  '302'

 L. 189       336  LOAD_STR                 'hexagonal1'
              338  STORE_FAST               'CrystalType'
            340_0  COME_FROM           332  '332'
            340_1  COME_FROM           294  '294'
            340_2  COME_FROM           258  '258'
            340_3  COME_FROM           226  '226'
            340_4  COME_FROM           204  '204'
            340_5  COME_FROM           174  '174'
            340_6  COME_FROM           152  '152'
            340_7  COME_FROM           114  '114'
            340_8  COME_FROM            84  '84'
            340_9  COME_FROM            52  '52'
           340_10  COME_FROM            20  '20'

 L. 190       340  LOAD_FAST                'CrystalType'
              342  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_FORWARD' instruction at offset 152