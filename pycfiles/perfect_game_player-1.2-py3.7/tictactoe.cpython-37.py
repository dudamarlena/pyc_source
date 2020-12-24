# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\pgameplayer\solvers\tictactoe.py
# Compiled at: 2019-12-29 04:05:57
# Size of source mod 2**32: 6479 bytes
from pgameplayer import minimax_tree
import copy

def compute_position_heuristic(board, player_token):
    """

    :param board:
    :param player_token:
    :return:
    """
    xo_diff = 0
    if board[0][0] == 'x':
        xo_diff += 3
    else:
        if board[0][0] == 'o':
            xo_diff -= 3
        elif board[0][2] == 'x':
            xo_diff += 3
        else:
            if board[0][2] == 'o':
                xo_diff -= 3
    if board[2][0] == 'x':
        xo_diff += 3
    else:
        if board[2][0] == 'o':
            xo_diff -= 3
        elif board[2][2] == 'x':
            xo_diff += 3
        else:
            if board[2][2] == 'o':
                xo_diff -= 3
    if board[0][1] == 'x':
        xo_diff += 1
    else:
        if board[0][1] == 'o':
            xo_diff -= 1
        elif board[2][1] == 'x':
            xo_diff += 1
        else:
            if board[2][1] == 'o':
                xo_diff -= 1
    if board[1][0] == 'x':
        xo_diff += 3
    else:
        if board[1][0] == 'o':
            xo_diff -= 3
        elif board[1][2] == 'x':
            xo_diff += 3
        else:
            if board[1][2] == 'o':
                xo_diff -= 3
    if board[1][1] == 'x':
        xo_diff += 5
    else:
        if board[1][1] == 'o':
            xo_diff -= 5
        return xo_diff


def compute_simple_heuristic--- This code section failed: ---

 L.  72         0  LOAD_CONST               0
                2  STORE_FAST               'x_pot_wins'

 L.  73         4  LOAD_CONST               0
                6  STORE_FAST               'o_pot_wins'

 L.  75         8  SETUP_LOOP          202  'to 202'
               10  LOAD_GLOBAL              range
               12  LOAD_CONST               3
               14  CALL_FUNCTION_1       1  '1 positional argument'
               16  GET_ITER         
             18_0  COME_FROM           188  '188'
             18_1  COME_FROM           166  '166'
               18  FOR_ITER            200  'to 200'
               20  STORE_FAST               'r'

 L.  76        22  LOAD_FAST                'board'
               24  LOAD_FAST                'r'
               26  BINARY_SUBSCR    
               28  LOAD_CONST               0
               30  BINARY_SUBSCR    
               32  LOAD_FAST                'board'
               34  LOAD_FAST                'r'
               36  BINARY_SUBSCR    
               38  LOAD_CONST               1
               40  BINARY_SUBSCR    
               42  DUP_TOP          
               44  ROT_THREE        
               46  COMPARE_OP               ==
               48  POP_JUMP_IF_FALSE    58  'to 58'
               50  LOAD_STR                 'o'
               52  COMPARE_OP               ==
               54  POP_JUMP_IF_FALSE    78  'to 78'
               56  JUMP_FORWARD         62  'to 62'
             58_0  COME_FROM            48  '48'
               58  POP_TOP          
               60  JUMP_FORWARD         78  'to 78'
             62_0  COME_FROM            56  '56'
               62  LOAD_FAST                'board'
               64  LOAD_FAST                'r'
               66  BINARY_SUBSCR    
               68  LOAD_CONST               2
               70  BINARY_SUBSCR    
               72  LOAD_STR                 '.'
               74  COMPARE_OP               ==
               76  POP_JUMP_IF_TRUE    190  'to 190'
             78_0  COME_FROM            60  '60'
             78_1  COME_FROM            54  '54'
               78  LOAD_FAST                'board'
               80  LOAD_FAST                'r'
               82  BINARY_SUBSCR    
               84  LOAD_CONST               0
               86  BINARY_SUBSCR    
               88  LOAD_FAST                'board'
               90  LOAD_FAST                'r'
               92  BINARY_SUBSCR    
               94  LOAD_CONST               2
               96  BINARY_SUBSCR    
               98  DUP_TOP          
              100  ROT_THREE        
              102  COMPARE_OP               ==
              104  POP_JUMP_IF_FALSE   114  'to 114'
              106  LOAD_STR                 'o'
              108  COMPARE_OP               ==
              110  POP_JUMP_IF_FALSE   134  'to 134'
              112  JUMP_FORWARD        118  'to 118'
            114_0  COME_FROM           104  '104'
              114  POP_TOP          
              116  JUMP_FORWARD        134  'to 134'
            118_0  COME_FROM           112  '112'
              118  LOAD_FAST                'board'
              120  LOAD_FAST                'r'
              122  BINARY_SUBSCR    
              124  LOAD_CONST               1
              126  BINARY_SUBSCR    
              128  LOAD_STR                 '.'
              130  COMPARE_OP               ==
              132  POP_JUMP_IF_TRUE    190  'to 190'
            134_0  COME_FROM           116  '116'
            134_1  COME_FROM           110  '110'

 L.  77       134  LOAD_FAST                'board'
              136  LOAD_FAST                'r'
              138  BINARY_SUBSCR    
              140  LOAD_CONST               2
              142  BINARY_SUBSCR    
              144  LOAD_FAST                'board'
              146  LOAD_FAST                'r'
              148  BINARY_SUBSCR    
              150  LOAD_CONST               1
              152  BINARY_SUBSCR    
              154  DUP_TOP          
              156  ROT_THREE        
              158  COMPARE_OP               ==
              160  POP_JUMP_IF_FALSE   170  'to 170'
              162  LOAD_STR                 'o'
              164  COMPARE_OP               ==
              166  POP_JUMP_IF_FALSE    18  'to 18'
              168  JUMP_FORWARD        174  'to 174'
            170_0  COME_FROM           160  '160'
              170  POP_TOP          
              172  JUMP_BACK            18  'to 18'
            174_0  COME_FROM           168  '168'
              174  LOAD_FAST                'board'
              176  LOAD_FAST                'r'
              178  BINARY_SUBSCR    
              180  LOAD_CONST               0
              182  BINARY_SUBSCR    
              184  LOAD_STR                 '.'
              186  COMPARE_OP               ==
              188  POP_JUMP_IF_FALSE    18  'to 18'
            190_0  COME_FROM           132  '132'
            190_1  COME_FROM            76  '76'

 L.  78       190  LOAD_FAST                'o_pot_wins'
              192  LOAD_CONST               1
              194  INPLACE_ADD      
              196  STORE_FAST               'o_pot_wins'
              198  JUMP_BACK            18  'to 18'
              200  POP_BLOCK        
            202_0  COME_FROM_LOOP        8  '8'

 L.  79       202  SETUP_LOOP          408  'to 408'
              204  LOAD_GLOBAL              range
              206  LOAD_CONST               3
              208  CALL_FUNCTION_1       1  '1 positional argument'
              210  GET_ITER         
            212_0  COME_FROM           394  '394'
            212_1  COME_FROM           372  '372'
              212  FOR_ITER            406  'to 406'
              214  STORE_FAST               'r'

 L.  80       216  LOAD_FAST                'board'
              218  LOAD_CONST               0
              220  BINARY_SUBSCR    
              222  LOAD_FAST                'r'
              224  BINARY_SUBSCR    
              226  LOAD_FAST                'board'
              228  LOAD_CONST               1
              230  BINARY_SUBSCR    
              232  LOAD_FAST                'r'
              234  BINARY_SUBSCR    
              236  DUP_TOP          
              238  ROT_THREE        
              240  COMPARE_OP               ==
              242  POP_JUMP_IF_FALSE   254  'to 254'
              244  LOAD_STR                 'o'
              246  COMPARE_OP               ==
          248_250  POP_JUMP_IF_FALSE   276  'to 276'
              252  JUMP_FORWARD        258  'to 258'
            254_0  COME_FROM           242  '242'
              254  POP_TOP          
              256  JUMP_FORWARD        276  'to 276'
            258_0  COME_FROM           252  '252'
              258  LOAD_FAST                'board'
              260  LOAD_CONST               2
              262  BINARY_SUBSCR    
              264  LOAD_FAST                'r'
              266  BINARY_SUBSCR    
              268  LOAD_STR                 '.'
              270  COMPARE_OP               ==
          272_274  POP_JUMP_IF_TRUE    396  'to 396'
            276_0  COME_FROM           256  '256'
            276_1  COME_FROM           248  '248'
              276  LOAD_FAST                'board'
              278  LOAD_CONST               0
              280  BINARY_SUBSCR    
              282  LOAD_FAST                'r'
              284  BINARY_SUBSCR    
              286  LOAD_FAST                'board'
              288  LOAD_CONST               2
              290  BINARY_SUBSCR    
              292  LOAD_FAST                'r'
              294  BINARY_SUBSCR    
              296  DUP_TOP          
              298  ROT_THREE        
              300  COMPARE_OP               ==
          302_304  POP_JUMP_IF_FALSE   316  'to 316'
              306  LOAD_STR                 'o'
              308  COMPARE_OP               ==
          310_312  POP_JUMP_IF_FALSE   338  'to 338'
              314  JUMP_FORWARD        320  'to 320'
            316_0  COME_FROM           302  '302'
              316  POP_TOP          
              318  JUMP_FORWARD        338  'to 338'
            320_0  COME_FROM           314  '314'
              320  LOAD_FAST                'board'
              322  LOAD_CONST               1
              324  BINARY_SUBSCR    
              326  LOAD_FAST                'r'
              328  BINARY_SUBSCR    
              330  LOAD_STR                 '.'
              332  COMPARE_OP               ==
          334_336  POP_JUMP_IF_TRUE    396  'to 396'
            338_0  COME_FROM           318  '318'
            338_1  COME_FROM           310  '310'

 L.  81       338  LOAD_FAST                'board'
              340  LOAD_CONST               2
              342  BINARY_SUBSCR    
              344  LOAD_FAST                'r'
              346  BINARY_SUBSCR    
              348  LOAD_FAST                'board'
              350  LOAD_CONST               1
              352  BINARY_SUBSCR    
              354  LOAD_FAST                'r'
              356  BINARY_SUBSCR    
              358  DUP_TOP          
              360  ROT_THREE        
              362  COMPARE_OP               ==
          364_366  POP_JUMP_IF_FALSE   376  'to 376'
              368  LOAD_STR                 'o'
              370  COMPARE_OP               ==
              372  POP_JUMP_IF_FALSE   212  'to 212'
              374  JUMP_FORWARD        380  'to 380'
            376_0  COME_FROM           364  '364'
              376  POP_TOP          
              378  JUMP_BACK           212  'to 212'
            380_0  COME_FROM           374  '374'
              380  LOAD_FAST                'board'
              382  LOAD_CONST               0
              384  BINARY_SUBSCR    
              386  LOAD_FAST                'r'
              388  BINARY_SUBSCR    
              390  LOAD_STR                 '.'
              392  COMPARE_OP               ==
              394  POP_JUMP_IF_FALSE   212  'to 212'
            396_0  COME_FROM           334  '334'
            396_1  COME_FROM           272  '272'

 L.  82       396  LOAD_FAST                'o_pot_wins'
              398  LOAD_CONST               1
              400  INPLACE_ADD      
              402  STORE_FAST               'o_pot_wins'
              404  JUMP_BACK           212  'to 212'
              406  POP_BLOCK        
            408_0  COME_FROM_LOOP      202  '202'

 L.  84       408  SETUP_LOOP          622  'to 622'
              410  LOAD_GLOBAL              range
              412  LOAD_CONST               3
              414  CALL_FUNCTION_1       1  '1 positional argument'
              416  GET_ITER         
            418_0  COME_FROM           604  '604'
            418_1  COME_FROM           580  '580'
              418  FOR_ITER            620  'to 620'
              420  STORE_FAST               'r'

 L.  85       422  LOAD_FAST                'board'
              424  LOAD_FAST                'r'
              426  BINARY_SUBSCR    
              428  LOAD_CONST               0
              430  BINARY_SUBSCR    
              432  LOAD_FAST                'board'
              434  LOAD_FAST                'r'
              436  BINARY_SUBSCR    
              438  LOAD_CONST               1
              440  BINARY_SUBSCR    
              442  DUP_TOP          
              444  ROT_THREE        
              446  COMPARE_OP               ==
          448_450  POP_JUMP_IF_FALSE   462  'to 462'
              452  LOAD_STR                 'x'
              454  COMPARE_OP               ==
          456_458  POP_JUMP_IF_FALSE   484  'to 484'
              460  JUMP_FORWARD        466  'to 466'
            462_0  COME_FROM           448  '448'
              462  POP_TOP          
              464  JUMP_FORWARD        484  'to 484'
            466_0  COME_FROM           460  '460'
              466  LOAD_FAST                'board'
              468  LOAD_FAST                'r'
              470  BINARY_SUBSCR    
              472  LOAD_CONST               2
              474  BINARY_SUBSCR    
              476  LOAD_STR                 '.'
              478  COMPARE_OP               ==
          480_482  POP_JUMP_IF_TRUE    608  'to 608'
            484_0  COME_FROM           464  '464'
            484_1  COME_FROM           456  '456'
              484  LOAD_FAST                'board'
              486  LOAD_FAST                'r'
              488  BINARY_SUBSCR    
              490  LOAD_CONST               0
              492  BINARY_SUBSCR    
              494  LOAD_FAST                'board'
              496  LOAD_FAST                'r'
              498  BINARY_SUBSCR    
              500  LOAD_CONST               2
              502  BINARY_SUBSCR    
              504  DUP_TOP          
              506  ROT_THREE        
              508  COMPARE_OP               ==
          510_512  POP_JUMP_IF_FALSE   524  'to 524'
              514  LOAD_STR                 'x'
              516  COMPARE_OP               ==
          518_520  POP_JUMP_IF_FALSE   546  'to 546'
              522  JUMP_FORWARD        528  'to 528'
            524_0  COME_FROM           510  '510'
              524  POP_TOP          
              526  JUMP_FORWARD        546  'to 546'
            528_0  COME_FROM           522  '522'
              528  LOAD_FAST                'board'
              530  LOAD_FAST                'r'
              532  BINARY_SUBSCR    

 L.  86       534  LOAD_CONST               1
              536  BINARY_SUBSCR    
              538  LOAD_STR                 '.'
              540  COMPARE_OP               ==
          542_544  POP_JUMP_IF_TRUE    608  'to 608'
            546_0  COME_FROM           526  '526'
            546_1  COME_FROM           518  '518'

 L.  87       546  LOAD_FAST                'board'
              548  LOAD_FAST                'r'
              550  BINARY_SUBSCR    
              552  LOAD_CONST               2
              554  BINARY_SUBSCR    
              556  LOAD_FAST                'board'
              558  LOAD_FAST                'r'
              560  BINARY_SUBSCR    
              562  LOAD_CONST               1
              564  BINARY_SUBSCR    
              566  DUP_TOP          
              568  ROT_THREE        
              570  COMPARE_OP               ==
          572_574  POP_JUMP_IF_FALSE   586  'to 586'
              576  LOAD_STR                 'x'
              578  COMPARE_OP               ==
          580_582  POP_JUMP_IF_FALSE   418  'to 418'
              584  JUMP_FORWARD        590  'to 590'
            586_0  COME_FROM           572  '572'
              586  POP_TOP          
              588  JUMP_BACK           418  'to 418'
            590_0  COME_FROM           584  '584'
              590  LOAD_FAST                'board'
              592  LOAD_FAST                'r'
              594  BINARY_SUBSCR    
              596  LOAD_CONST               0
              598  BINARY_SUBSCR    
              600  LOAD_STR                 '.'
              602  COMPARE_OP               ==
          604_606  POP_JUMP_IF_FALSE   418  'to 418'
            608_0  COME_FROM           542  '542'
            608_1  COME_FROM           480  '480'

 L.  88       608  LOAD_FAST                'x_pot_wins'
              610  LOAD_CONST               1
              612  INPLACE_ADD      
              614  STORE_FAST               'x_pot_wins'
          616_618  JUMP_BACK           418  'to 418'
              620  POP_BLOCK        
            622_0  COME_FROM_LOOP      408  '408'

 L.  89       622  SETUP_LOOP          836  'to 836'
              624  LOAD_GLOBAL              range
              626  LOAD_CONST               3
              628  CALL_FUNCTION_1       1  '1 positional argument'
              630  GET_ITER         
            632_0  COME_FROM           818  '818'
            632_1  COME_FROM           794  '794'
              632  FOR_ITER            834  'to 834'
              634  STORE_FAST               'r'

 L.  90       636  LOAD_FAST                'board'
              638  LOAD_CONST               0
              640  BINARY_SUBSCR    
              642  LOAD_FAST                'r'
              644  BINARY_SUBSCR    
              646  LOAD_FAST                'board'
              648  LOAD_CONST               1
              650  BINARY_SUBSCR    
              652  LOAD_FAST                'r'
              654  BINARY_SUBSCR    
              656  DUP_TOP          
              658  ROT_THREE        
              660  COMPARE_OP               ==
          662_664  POP_JUMP_IF_FALSE   676  'to 676'
              666  LOAD_STR                 'x'
              668  COMPARE_OP               ==
          670_672  POP_JUMP_IF_FALSE   698  'to 698'
              674  JUMP_FORWARD        680  'to 680'
            676_0  COME_FROM           662  '662'
              676  POP_TOP          
              678  JUMP_FORWARD        698  'to 698'
            680_0  COME_FROM           674  '674'
              680  LOAD_FAST                'board'
              682  LOAD_CONST               2
              684  BINARY_SUBSCR    
              686  LOAD_FAST                'r'
              688  BINARY_SUBSCR    
              690  LOAD_STR                 '.'
              692  COMPARE_OP               ==
          694_696  POP_JUMP_IF_TRUE    822  'to 822'
            698_0  COME_FROM           678  '678'
            698_1  COME_FROM           670  '670'
              698  LOAD_FAST                'board'
              700  LOAD_CONST               0
              702  BINARY_SUBSCR    
              704  LOAD_FAST                'r'
              706  BINARY_SUBSCR    
              708  LOAD_FAST                'board'
              710  LOAD_CONST               2
              712  BINARY_SUBSCR    
              714  LOAD_FAST                'r'
              716  BINARY_SUBSCR    
              718  DUP_TOP          
              720  ROT_THREE        
              722  COMPARE_OP               ==
          724_726  POP_JUMP_IF_FALSE   738  'to 738'
              728  LOAD_STR                 'x'
              730  COMPARE_OP               ==
          732_734  POP_JUMP_IF_FALSE   760  'to 760'
              736  JUMP_FORWARD        742  'to 742'
            738_0  COME_FROM           724  '724'
              738  POP_TOP          
              740  JUMP_FORWARD        760  'to 760'
            742_0  COME_FROM           736  '736'
              742  LOAD_FAST                'board'
              744  LOAD_CONST               1
              746  BINARY_SUBSCR    

 L.  91       748  LOAD_FAST                'r'
              750  BINARY_SUBSCR    
              752  LOAD_STR                 '.'
              754  COMPARE_OP               ==
          756_758  POP_JUMP_IF_TRUE    822  'to 822'
            760_0  COME_FROM           740  '740'
            760_1  COME_FROM           732  '732'

 L.  92       760  LOAD_FAST                'board'
              762  LOAD_CONST               2
              764  BINARY_SUBSCR    
              766  LOAD_FAST                'r'
              768  BINARY_SUBSCR    
              770  LOAD_FAST                'board'
              772  LOAD_CONST               1
              774  BINARY_SUBSCR    
              776  LOAD_FAST                'r'
              778  BINARY_SUBSCR    
              780  DUP_TOP          
              782  ROT_THREE        
              784  COMPARE_OP               ==
          786_788  POP_JUMP_IF_FALSE   800  'to 800'
              790  LOAD_STR                 'x'
              792  COMPARE_OP               ==
          794_796  POP_JUMP_IF_FALSE   632  'to 632'
              798  JUMP_FORWARD        804  'to 804'
            800_0  COME_FROM           786  '786'
              800  POP_TOP          
              802  JUMP_BACK           632  'to 632'
            804_0  COME_FROM           798  '798'
              804  LOAD_FAST                'board'
              806  LOAD_CONST               0
              808  BINARY_SUBSCR    
              810  LOAD_FAST                'r'
              812  BINARY_SUBSCR    
              814  LOAD_STR                 '.'
              816  COMPARE_OP               ==
          818_820  POP_JUMP_IF_FALSE   632  'to 632'
            822_0  COME_FROM           756  '756'
            822_1  COME_FROM           694  '694'

 L.  93       822  LOAD_FAST                'x_pot_wins'
              824  LOAD_CONST               1
              826  INPLACE_ADD      
              828  STORE_FAST               'x_pot_wins'
          830_832  JUMP_BACK           632  'to 632'
              834  POP_BLOCK        
            836_0  COME_FROM_LOOP      622  '622'

 L.  95       836  LOAD_FAST                'board'
              838  LOAD_CONST               0
              840  BINARY_SUBSCR    
              842  LOAD_CONST               0
              844  BINARY_SUBSCR    
              846  LOAD_FAST                'board'
              848  LOAD_CONST               1
              850  BINARY_SUBSCR    
              852  LOAD_CONST               1
              854  BINARY_SUBSCR    
              856  DUP_TOP          
              858  ROT_THREE        
              860  COMPARE_OP               ==
          862_864  POP_JUMP_IF_FALSE   876  'to 876'
              866  LOAD_STR                 'x'
              868  COMPARE_OP               ==
          870_872  POP_JUMP_IF_FALSE   898  'to 898'
              874  JUMP_FORWARD        880  'to 880'
            876_0  COME_FROM           862  '862'
              876  POP_TOP          
              878  JUMP_FORWARD        898  'to 898'
            880_0  COME_FROM           874  '874'
              880  LOAD_FAST                'board'
              882  LOAD_CONST               2
              884  BINARY_SUBSCR    
              886  LOAD_CONST               2
              888  BINARY_SUBSCR    
              890  LOAD_STR                 '.'
              892  COMPARE_OP               ==
          894_896  POP_JUMP_IF_TRUE   1022  'to 1022'
            898_0  COME_FROM           878  '878'
            898_1  COME_FROM           870  '870'
              898  LOAD_FAST                'board'
              900  LOAD_CONST               0
              902  BINARY_SUBSCR    
              904  LOAD_CONST               0
              906  BINARY_SUBSCR    
              908  LOAD_FAST                'board'
              910  LOAD_CONST               2
              912  BINARY_SUBSCR    
              914  LOAD_CONST               2
              916  BINARY_SUBSCR    
              918  DUP_TOP          
              920  ROT_THREE        
              922  COMPARE_OP               ==
          924_926  POP_JUMP_IF_FALSE   938  'to 938'
              928  LOAD_STR                 'x'
              930  COMPARE_OP               ==
          932_934  POP_JUMP_IF_FALSE   960  'to 960'
              936  JUMP_FORWARD        942  'to 942'
            938_0  COME_FROM           924  '924'
              938  POP_TOP          
              940  JUMP_FORWARD        960  'to 960'
            942_0  COME_FROM           936  '936'
              942  LOAD_FAST                'board'
              944  LOAD_CONST               1
              946  BINARY_SUBSCR    

 L.  96       948  LOAD_CONST               1
              950  BINARY_SUBSCR    
              952  LOAD_STR                 '.'
              954  COMPARE_OP               ==
          956_958  POP_JUMP_IF_TRUE   1022  'to 1022'
            960_0  COME_FROM           940  '940'
            960_1  COME_FROM           932  '932'

 L.  97       960  LOAD_FAST                'board'
              962  LOAD_CONST               2
              964  BINARY_SUBSCR    
              966  LOAD_CONST               2
              968  BINARY_SUBSCR    
              970  LOAD_FAST                'board'
              972  LOAD_CONST               1
              974  BINARY_SUBSCR    
              976  LOAD_CONST               1
              978  BINARY_SUBSCR    
              980  DUP_TOP          
              982  ROT_THREE        
              984  COMPARE_OP               ==
          986_988  POP_JUMP_IF_FALSE  1000  'to 1000'
              990  LOAD_STR                 'x'
              992  COMPARE_OP               ==
          994_996  POP_JUMP_IF_FALSE  1030  'to 1030'
              998  JUMP_FORWARD       1004  'to 1004'
           1000_0  COME_FROM           986  '986'
             1000  POP_TOP          
             1002  JUMP_FORWARD       1030  'to 1030'
           1004_0  COME_FROM           998  '998'
             1004  LOAD_FAST                'board'
             1006  LOAD_CONST               0
             1008  BINARY_SUBSCR    
             1010  LOAD_CONST               0
             1012  BINARY_SUBSCR    
             1014  LOAD_STR                 '.'
             1016  COMPARE_OP               ==
         1018_1020  POP_JUMP_IF_FALSE  1030  'to 1030'
           1022_0  COME_FROM           956  '956'
           1022_1  COME_FROM           894  '894'

 L.  98      1022  LOAD_FAST                'x_pot_wins'
             1024  LOAD_CONST               1
             1026  INPLACE_ADD      
             1028  STORE_FAST               'x_pot_wins'
           1030_0  COME_FROM          1018  '1018'
           1030_1  COME_FROM          1002  '1002'
           1030_2  COME_FROM           994  '994'

 L. 100      1030  LOAD_FAST                'board'
             1032  LOAD_CONST               0
             1034  BINARY_SUBSCR    
             1036  LOAD_CONST               0
             1038  BINARY_SUBSCR    
             1040  LOAD_FAST                'board'
             1042  LOAD_CONST               1
             1044  BINARY_SUBSCR    
             1046  LOAD_CONST               1
             1048  BINARY_SUBSCR    
             1050  DUP_TOP          
             1052  ROT_THREE        
             1054  COMPARE_OP               ==
         1056_1058  POP_JUMP_IF_FALSE  1070  'to 1070'
             1060  LOAD_STR                 'o'
             1062  COMPARE_OP               ==
         1064_1066  POP_JUMP_IF_FALSE  1092  'to 1092'
             1068  JUMP_FORWARD       1074  'to 1074'
           1070_0  COME_FROM          1056  '1056'
             1070  POP_TOP          
             1072  JUMP_FORWARD       1092  'to 1092'
           1074_0  COME_FROM          1068  '1068'
             1074  LOAD_FAST                'board'
             1076  LOAD_CONST               2
             1078  BINARY_SUBSCR    
             1080  LOAD_CONST               2
             1082  BINARY_SUBSCR    
             1084  LOAD_STR                 '.'
             1086  COMPARE_OP               ==
         1088_1090  POP_JUMP_IF_TRUE   1216  'to 1216'
           1092_0  COME_FROM          1072  '1072'
           1092_1  COME_FROM          1064  '1064'
             1092  LOAD_FAST                'board'
             1094  LOAD_CONST               0
             1096  BINARY_SUBSCR    
             1098  LOAD_CONST               0
             1100  BINARY_SUBSCR    
             1102  LOAD_FAST                'board'
             1104  LOAD_CONST               2
             1106  BINARY_SUBSCR    
             1108  LOAD_CONST               2
             1110  BINARY_SUBSCR    
             1112  DUP_TOP          
             1114  ROT_THREE        
             1116  COMPARE_OP               ==
         1118_1120  POP_JUMP_IF_FALSE  1132  'to 1132'
             1122  LOAD_STR                 'o'
             1124  COMPARE_OP               ==
         1126_1128  POP_JUMP_IF_FALSE  1154  'to 1154'
             1130  JUMP_FORWARD       1136  'to 1136'
           1132_0  COME_FROM          1118  '1118'
             1132  POP_TOP          
             1134  JUMP_FORWARD       1154  'to 1154'
           1136_0  COME_FROM          1130  '1130'
             1136  LOAD_FAST                'board'
             1138  LOAD_CONST               1
             1140  BINARY_SUBSCR    

 L. 101      1142  LOAD_CONST               1
             1144  BINARY_SUBSCR    
             1146  LOAD_STR                 '.'
             1148  COMPARE_OP               ==
         1150_1152  POP_JUMP_IF_TRUE   1216  'to 1216'
           1154_0  COME_FROM          1134  '1134'
           1154_1  COME_FROM          1126  '1126'

 L. 102      1154  LOAD_FAST                'board'
             1156  LOAD_CONST               2
             1158  BINARY_SUBSCR    
             1160  LOAD_CONST               2
             1162  BINARY_SUBSCR    
             1164  LOAD_FAST                'board'
             1166  LOAD_CONST               1
             1168  BINARY_SUBSCR    
             1170  LOAD_CONST               1
             1172  BINARY_SUBSCR    
             1174  DUP_TOP          
             1176  ROT_THREE        
             1178  COMPARE_OP               ==
         1180_1182  POP_JUMP_IF_FALSE  1194  'to 1194'
             1184  LOAD_STR                 'o'
             1186  COMPARE_OP               ==
         1188_1190  POP_JUMP_IF_FALSE  1224  'to 1224'
             1192  JUMP_FORWARD       1198  'to 1198'
           1194_0  COME_FROM          1180  '1180'
             1194  POP_TOP          
             1196  JUMP_FORWARD       1224  'to 1224'
           1198_0  COME_FROM          1192  '1192'
             1198  LOAD_FAST                'board'
             1200  LOAD_CONST               0
             1202  BINARY_SUBSCR    
             1204  LOAD_CONST               0
             1206  BINARY_SUBSCR    
             1208  LOAD_STR                 '.'
             1210  COMPARE_OP               ==
         1212_1214  POP_JUMP_IF_FALSE  1224  'to 1224'
           1216_0  COME_FROM          1150  '1150'
           1216_1  COME_FROM          1088  '1088'

 L. 103      1216  LOAD_FAST                'o_pot_wins'
             1218  LOAD_CONST               1
             1220  INPLACE_ADD      
             1222  STORE_FAST               'o_pot_wins'
           1224_0  COME_FROM          1212  '1212'
           1224_1  COME_FROM          1196  '1196'
           1224_2  COME_FROM          1188  '1188'

 L. 105      1224  LOAD_FAST                'board'
             1226  LOAD_CONST               0
             1228  BINARY_SUBSCR    
             1230  LOAD_CONST               2
             1232  BINARY_SUBSCR    
             1234  LOAD_FAST                'board'
             1236  LOAD_CONST               1
             1238  BINARY_SUBSCR    
             1240  LOAD_CONST               1
             1242  BINARY_SUBSCR    
             1244  DUP_TOP          
             1246  ROT_THREE        
             1248  COMPARE_OP               ==
         1250_1252  POP_JUMP_IF_FALSE  1264  'to 1264'
             1254  LOAD_STR                 'x'
             1256  COMPARE_OP               ==
         1258_1260  POP_JUMP_IF_FALSE  1286  'to 1286'
             1262  JUMP_FORWARD       1268  'to 1268'
           1264_0  COME_FROM          1250  '1250'
             1264  POP_TOP          
             1266  JUMP_FORWARD       1286  'to 1286'
           1268_0  COME_FROM          1262  '1262'
             1268  LOAD_FAST                'board'
             1270  LOAD_CONST               2
             1272  BINARY_SUBSCR    
             1274  LOAD_CONST               1
             1276  BINARY_SUBSCR    
             1278  LOAD_STR                 '.'
             1280  COMPARE_OP               ==
         1282_1284  POP_JUMP_IF_TRUE   1410  'to 1410'
           1286_0  COME_FROM          1266  '1266'
           1286_1  COME_FROM          1258  '1258'
             1286  LOAD_FAST                'board'
             1288  LOAD_CONST               0
             1290  BINARY_SUBSCR    
             1292  LOAD_CONST               2
             1294  BINARY_SUBSCR    
             1296  LOAD_FAST                'board'
             1298  LOAD_CONST               2
             1300  BINARY_SUBSCR    
             1302  LOAD_CONST               1
             1304  BINARY_SUBSCR    
             1306  DUP_TOP          
             1308  ROT_THREE        
             1310  COMPARE_OP               ==
         1312_1314  POP_JUMP_IF_FALSE  1326  'to 1326'
             1316  LOAD_STR                 'x'
             1318  COMPARE_OP               ==
         1320_1322  POP_JUMP_IF_FALSE  1348  'to 1348'
             1324  JUMP_FORWARD       1330  'to 1330'
           1326_0  COME_FROM          1312  '1312'
             1326  POP_TOP          
             1328  JUMP_FORWARD       1348  'to 1348'
           1330_0  COME_FROM          1324  '1324'
             1330  LOAD_FAST                'board'
             1332  LOAD_CONST               1
             1334  BINARY_SUBSCR    

 L. 106      1336  LOAD_CONST               1
             1338  BINARY_SUBSCR    
             1340  LOAD_STR                 '.'
             1342  COMPARE_OP               ==
         1344_1346  POP_JUMP_IF_TRUE   1410  'to 1410'
           1348_0  COME_FROM          1328  '1328'
           1348_1  COME_FROM          1320  '1320'

 L. 107      1348  LOAD_FAST                'board'
             1350  LOAD_CONST               2
             1352  BINARY_SUBSCR    
             1354  LOAD_CONST               1
             1356  BINARY_SUBSCR    
             1358  LOAD_FAST                'board'
             1360  LOAD_CONST               1
             1362  BINARY_SUBSCR    
             1364  LOAD_CONST               1
             1366  BINARY_SUBSCR    
             1368  DUP_TOP          
             1370  ROT_THREE        
             1372  COMPARE_OP               ==
         1374_1376  POP_JUMP_IF_FALSE  1388  'to 1388'
             1378  LOAD_STR                 'x'
             1380  COMPARE_OP               ==
         1382_1384  POP_JUMP_IF_FALSE  1418  'to 1418'
             1386  JUMP_FORWARD       1392  'to 1392'
           1388_0  COME_FROM          1374  '1374'
             1388  POP_TOP          
             1390  JUMP_FORWARD       1418  'to 1418'
           1392_0  COME_FROM          1386  '1386'
             1392  LOAD_FAST                'board'
             1394  LOAD_CONST               0
             1396  BINARY_SUBSCR    
             1398  LOAD_CONST               2
             1400  BINARY_SUBSCR    
             1402  LOAD_STR                 '.'
             1404  COMPARE_OP               ==
         1406_1408  POP_JUMP_IF_FALSE  1418  'to 1418'
           1410_0  COME_FROM          1344  '1344'
           1410_1  COME_FROM          1282  '1282'

 L. 108      1410  LOAD_FAST                'x_pot_wins'
             1412  LOAD_CONST               1
             1414  INPLACE_ADD      
             1416  STORE_FAST               'x_pot_wins'
           1418_0  COME_FROM          1406  '1406'
           1418_1  COME_FROM          1390  '1390'
           1418_2  COME_FROM          1382  '1382'

 L. 110      1418  LOAD_FAST                'board'
             1420  LOAD_CONST               0
             1422  BINARY_SUBSCR    
             1424  LOAD_CONST               2
             1426  BINARY_SUBSCR    
             1428  LOAD_FAST                'board'
             1430  LOAD_CONST               1
             1432  BINARY_SUBSCR    
             1434  LOAD_CONST               1
             1436  BINARY_SUBSCR    
             1438  DUP_TOP          
             1440  ROT_THREE        
             1442  COMPARE_OP               ==
         1444_1446  POP_JUMP_IF_FALSE  1458  'to 1458'
             1448  LOAD_STR                 'o'
             1450  COMPARE_OP               ==
         1452_1454  POP_JUMP_IF_FALSE  1480  'to 1480'
             1456  JUMP_FORWARD       1462  'to 1462'
           1458_0  COME_FROM          1444  '1444'
             1458  POP_TOP          
             1460  JUMP_FORWARD       1480  'to 1480'
           1462_0  COME_FROM          1456  '1456'
             1462  LOAD_FAST                'board'
             1464  LOAD_CONST               2
             1466  BINARY_SUBSCR    
             1468  LOAD_CONST               1
             1470  BINARY_SUBSCR    
             1472  LOAD_STR                 '.'
             1474  COMPARE_OP               ==
         1476_1478  POP_JUMP_IF_TRUE   1604  'to 1604'
           1480_0  COME_FROM          1460  '1460'
           1480_1  COME_FROM          1452  '1452'
             1480  LOAD_FAST                'board'
             1482  LOAD_CONST               0
             1484  BINARY_SUBSCR    
             1486  LOAD_CONST               2
             1488  BINARY_SUBSCR    
             1490  LOAD_FAST                'board'
             1492  LOAD_CONST               2
             1494  BINARY_SUBSCR    
             1496  LOAD_CONST               1
             1498  BINARY_SUBSCR    
             1500  DUP_TOP          
             1502  ROT_THREE        
             1504  COMPARE_OP               ==
         1506_1508  POP_JUMP_IF_FALSE  1520  'to 1520'
             1510  LOAD_STR                 'o'
             1512  COMPARE_OP               ==
         1514_1516  POP_JUMP_IF_FALSE  1542  'to 1542'
             1518  JUMP_FORWARD       1524  'to 1524'
           1520_0  COME_FROM          1506  '1506'
             1520  POP_TOP          
             1522  JUMP_FORWARD       1542  'to 1542'
           1524_0  COME_FROM          1518  '1518'
             1524  LOAD_FAST                'board'
             1526  LOAD_CONST               1
             1528  BINARY_SUBSCR    

 L. 111      1530  LOAD_CONST               1
             1532  BINARY_SUBSCR    
             1534  LOAD_STR                 '.'
             1536  COMPARE_OP               ==
         1538_1540  POP_JUMP_IF_TRUE   1604  'to 1604'
           1542_0  COME_FROM          1522  '1522'
           1542_1  COME_FROM          1514  '1514'

 L. 112      1542  LOAD_FAST                'board'
             1544  LOAD_CONST               2
             1546  BINARY_SUBSCR    
             1548  LOAD_CONST               1
             1550  BINARY_SUBSCR    
             1552  LOAD_FAST                'board'
             1554  LOAD_CONST               1
             1556  BINARY_SUBSCR    
             1558  LOAD_CONST               1
             1560  BINARY_SUBSCR    
             1562  DUP_TOP          
             1564  ROT_THREE        
             1566  COMPARE_OP               ==
         1568_1570  POP_JUMP_IF_FALSE  1582  'to 1582'
             1572  LOAD_STR                 'o'
             1574  COMPARE_OP               ==
         1576_1578  POP_JUMP_IF_FALSE  1612  'to 1612'
             1580  JUMP_FORWARD       1586  'to 1586'
           1582_0  COME_FROM          1568  '1568'
             1582  POP_TOP          
             1584  JUMP_FORWARD       1612  'to 1612'
           1586_0  COME_FROM          1580  '1580'
             1586  LOAD_FAST                'board'
             1588  LOAD_CONST               0
             1590  BINARY_SUBSCR    
             1592  LOAD_CONST               2
             1594  BINARY_SUBSCR    
             1596  LOAD_STR                 '.'
             1598  COMPARE_OP               ==
         1600_1602  POP_JUMP_IF_FALSE  1612  'to 1612'
           1604_0  COME_FROM          1538  '1538'
           1604_1  COME_FROM          1476  '1476'

 L. 113      1604  LOAD_FAST                'o_pot_wins'
             1606  LOAD_CONST               1
             1608  INPLACE_ADD      
             1610  STORE_FAST               'o_pot_wins'
           1612_0  COME_FROM          1600  '1600'
           1612_1  COME_FROM          1584  '1584'
           1612_2  COME_FROM          1576  '1576'

 L. 116      1612  LOAD_FAST                'x_pot_wins'
             1614  LOAD_FAST                'o_pot_wins'
             1616  BINARY_SUBTRACT  
             1618  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_BLOCK' instruction at offset 200


def win_for_player(board, player_token):
    for r in range(3):
        if board[r][0] == player_token:
            if board[r][1] == player_token:
                if board[r][2] == player_token:
                    return True
        if board[0][r] == player_token and board[1][r] == player_token and board[2][r] == player_token:
            return True

    if board[0][0] == player_token:
        if board[1][1] == player_token:
            if board[2][2] == player_token:
                return True
    if board[0][2] == player_token:
        if board[1][1] == player_token:
            if board[2][0] == player_token:
                return True
    return False


class TicTacToeNode(minimax_tree.Node):
    __doc__ = '\n    Specialized class of Node.\n    It represents one board position with the heuristic value for the given players move\n    '
    heuristic = compute_position_heuristic

    def __init__(self, board):
        """

        :param board: 3x3 character array with 'x','o' and '.'
        """
        self.state = board
        self.player = True
        self.value = None
        self.best_move = None

    def if_leaf(self):
        """
        checks if node is either a win, loss or draw.
        :return: boolean
        """
        if win_for_player(self.state, 'x') or win_for_player(self.state, 'o'):
            return True
        if any(('.' in row for row in self.state)):
            return False
        return True

    def generate_moves(self, player):
        """
        Generates list of valid possible moves
        :param player: Boolean. x or o
        :return: list
        """
        curboard = copy.copy(self.state)
        next_state = []
        if player:
            for r in range(3):
                for c in range(3):
                    if curboard[r][c] == '.':
                        newnode = TicTacToeNode(copy.deepcopy(self.state))
                        newnode.state[r][c] = 'x'
                        next_state.append(newnode)

        else:
            for r in range(3):
                for c in range(3):
                    if curboard[r][c] == '.':
                        newnode = TicTacToeNode(copy.deepcopy(self.state))
                        newnode.state[r][c] = 'o'
                        next_state.append(newnode)

        return next_state

    def evaluate(self):
        """ Set value of board. If its not a win, loss or a draw then heuristic is evaluated.

        """
        if win_for_player(self.state, 'x'):
            self.value = minimax_tree.PINF
        else:
            if win_for_player(self.state, 'o'):
                self.value = minimax_tree.NINF
            else:
                if not any(('.' in row for row in self.state)):
                    self.value = 0
                else:
                    self.value = TicTacToeNode.heuristic(self.state, self.player)
        return self.value