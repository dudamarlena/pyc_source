# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ryan/anaconda3/envs/wsl2/lib/python3.8/site-packages/pyEQL/chemical_formula.py
# Compiled at: 2020-04-22 01:04:47
# Size of source mod 2**32: 30286 bytes
"""
This module contains classes, functions, and methods to facilitate the
input, output, and parsing of chemical formulas for pyEQL.

The correct case must be used when specifying elements.

:copyright: 2013-2020 by Ryan S. Kingsbury
:license: LGPL, see LICENSE for more details.

"""
import logging
from pyEQL.logging_system import Unique
logger = logging.getLogger(__name__)
unique = Unique()
logger.addFilter(unique)
ch = logging.StreamHandler()
formatter = logging.Formatter('(%(name)s) - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

def _invalid_formula(reason):
    raise ValueError('Invalid chemical formula specified - %s' % reason)


def _check_formula--- This code section failed: ---

 L.  75         0  LOAD_FAST                'formula'
                2  LOAD_CONST               0
                4  BINARY_SUBSCR    
                6  LOAD_METHOD              isalpha
                8  CALL_METHOD_0         0  ''
               10  POP_JUMP_IF_TRUE     32  'to 32'
               12  LOAD_FAST                'formula'
               14  LOAD_CONST               0
               16  BINARY_SUBSCR    
               18  LOAD_STR                 '('
               20  COMPARE_OP               ==
               22  POP_JUMP_IF_TRUE     32  'to 32'

 L.  76        24  LOAD_GLOBAL              _invalid_formula
               26  LOAD_STR                 'formula must begin with an element or open parenthesis'
               28  CALL_FUNCTION_1       1  ''
               30  POP_TOP          
             32_0  COME_FROM            22  '22'
             32_1  COME_FROM            10  '10'

 L.  79        32  LOAD_STR                 '+'
               34  LOAD_FAST                'formula'
               36  COMPARE_OP               in
               38  POP_JUMP_IF_FALSE    56  'to 56'
               40  LOAD_STR                 '-'
               42  LOAD_FAST                'formula'
               44  COMPARE_OP               in
               46  POP_JUMP_IF_FALSE    56  'to 56'

 L.  80        48  LOAD_GLOBAL              _invalid_formula
               50  LOAD_STR                 'ionic formulas cannot contain mismatched charge symbols'
               52  CALL_FUNCTION_1       1  ''
               54  POP_TOP          
             56_0  COME_FROM            46  '46'
             56_1  COME_FROM            38  '38'

 L.  83        56  LOAD_STR                 '+'
               58  LOAD_FAST                'formula'
               60  COMPARE_OP               in
               62  POP_JUMP_IF_FALSE   172  'to 172'

 L.  84        64  LOAD_FAST                'formula'
               66  LOAD_METHOD              count
               68  LOAD_STR                 '+'
               70  CALL_METHOD_1         1  ''
               72  LOAD_CONST               1
               74  COMPARE_OP               ==
               76  POP_JUMP_IF_FALSE   112  'to 112'

 L.  85        78  LOAD_FAST                'formula'
               80  LOAD_CONST               -1
               82  BINARY_SUBSCR    
               84  LOAD_STR                 '+'
               86  COMPARE_OP               ==

 L.  84        88  POP_JUMP_IF_TRUE    112  'to 112'

 L.  85        90  LOAD_FAST                'formula'
               92  LOAD_CONST               -1
               94  BINARY_SUBSCR    
               96  LOAD_METHOD              isnumeric
               98  CALL_METHOD_0         0  ''

 L.  84       100  POP_JUMP_IF_TRUE    112  'to 112'

 L.  87       102  LOAD_GLOBAL              _invalid_formula

 L.  88       104  LOAD_STR                 'ionic formulas must end with one or more charge symbols or a single charge symbol and a number'

 L.  87       106  CALL_FUNCTION_1       1  ''
              108  POP_TOP          
              110  JUMP_FORWARD        170  'to 170'
            112_0  COME_FROM           100  '100'
            112_1  COME_FROM            88  '88'
            112_2  COME_FROM            76  '76'

 L.  90       112  LOAD_FAST                'formula'
              114  LOAD_METHOD              count
              116  LOAD_STR                 '+'
              118  CALL_METHOD_1         1  ''
              120  LOAD_CONST               1
              122  COMPARE_OP               >
              124  POP_JUMP_IF_FALSE   170  'to 170'

 L.  91       126  LOAD_FAST                'formula'
              128  LOAD_METHOD              find
              130  LOAD_STR                 '+'
              132  CALL_METHOD_1         1  ''
              134  STORE_FAST               'start'

 L.  92       136  LOAD_FAST                'formula'
              138  LOAD_FAST                'start'
              140  LOAD_CONST               None
              142  BUILD_SLICE_2         2 
              144  BINARY_SUBSCR    
              146  GET_ITER         
            148_0  COME_FROM           158  '158'
              148  FOR_ITER            170  'to 170'
              150  STORE_FAST               'char'

 L.  93       152  LOAD_FAST                'char'
              154  LOAD_STR                 '+'
              156  COMPARE_OP               !=
              158  POP_JUMP_IF_FALSE   148  'to 148'

 L.  94       160  LOAD_GLOBAL              _invalid_formula

 L.  95       162  LOAD_STR                 'ionic formulas must end with one or more charge symbols or a single charge symbol and a number'

 L.  94       164  CALL_FUNCTION_1       1  ''
              166  POP_TOP          
              168  JUMP_BACK           148  'to 148'
            170_0  COME_FROM           124  '124'
            170_1  COME_FROM           110  '110'
              170  JUMP_FORWARD        294  'to 294'
            172_0  COME_FROM            62  '62'

 L.  97       172  LOAD_STR                 '-'
              174  LOAD_FAST                'formula'
              176  COMPARE_OP               in
          178_180  POP_JUMP_IF_FALSE   294  'to 294'

 L.  98       182  LOAD_FAST                'formula'
              184  LOAD_METHOD              count
              186  LOAD_STR                 '-'
              188  CALL_METHOD_1         1  ''
              190  LOAD_CONST               1
              192  COMPARE_OP               ==
              194  POP_JUMP_IF_FALSE   230  'to 230'

 L.  99       196  LOAD_FAST                'formula'
              198  LOAD_CONST               -1
              200  BINARY_SUBSCR    
              202  LOAD_STR                 '-'
              204  COMPARE_OP               ==

 L.  98       206  POP_JUMP_IF_TRUE    230  'to 230'

 L.  99       208  LOAD_FAST                'formula'
              210  LOAD_CONST               -1
              212  BINARY_SUBSCR    
              214  LOAD_METHOD              isnumeric
              216  CALL_METHOD_0         0  ''

 L.  98       218  POP_JUMP_IF_TRUE    230  'to 230'

 L. 101       220  LOAD_GLOBAL              _invalid_formula

 L. 102       222  LOAD_STR                 'ionic formulas must end with one or more charge symbols or a single charge symbol and a number'

 L. 101       224  CALL_FUNCTION_1       1  ''
              226  POP_TOP          
              228  JUMP_FORWARD        294  'to 294'
            230_0  COME_FROM           218  '218'
            230_1  COME_FROM           206  '206'
            230_2  COME_FROM           194  '194'

 L. 104       230  LOAD_FAST                'formula'
              232  LOAD_METHOD              count
              234  LOAD_STR                 '-'
              236  CALL_METHOD_1         1  ''
              238  LOAD_CONST               1
              240  COMPARE_OP               >
          242_244  POP_JUMP_IF_FALSE   294  'to 294'

 L. 105       246  LOAD_FAST                'formula'
              248  LOAD_METHOD              find
              250  LOAD_STR                 '-'
              252  CALL_METHOD_1         1  ''
              254  STORE_FAST               'start'

 L. 106       256  LOAD_FAST                'formula'
              258  LOAD_FAST                'start'
              260  LOAD_CONST               None
              262  BUILD_SLICE_2         2 
              264  BINARY_SUBSCR    
              266  GET_ITER         
            268_0  COME_FROM           278  '278'
              268  FOR_ITER            294  'to 294'
              270  STORE_FAST               'char'

 L. 107       272  LOAD_FAST                'char'
              274  LOAD_STR                 '-'
              276  COMPARE_OP               !=
          278_280  POP_JUMP_IF_FALSE   268  'to 268'

 L. 108       282  LOAD_GLOBAL              _invalid_formula

 L. 109       284  LOAD_STR                 'ionic formulas must end with one or more charge symbols or a single charge symbol and a number'

 L. 108       286  CALL_FUNCTION_1       1  ''
              288  POP_TOP          
          290_292  JUMP_BACK           268  'to 268'
            294_0  COME_FROM           242  '242'
            294_1  COME_FROM           228  '228'
            294_2  COME_FROM           178  '178'
            294_3  COME_FROM           170  '170'

 L. 113       294  LOAD_FAST                'formula'
              296  LOAD_METHOD              count
              298  LOAD_STR                 '('
              300  CALL_METHOD_1         1  ''
              302  LOAD_FAST                'formula'
              304  LOAD_METHOD              count
              306  LOAD_STR                 ')'
              308  CALL_METHOD_1         1  ''
              310  COMPARE_OP               !=
          312_314  POP_JUMP_IF_FALSE   324  'to 324'

 L. 114       316  LOAD_GLOBAL              _invalid_formula
              318  LOAD_STR                 'parentheses mismatch'
              320  CALL_FUNCTION_1       1  ''
              322  POP_TOP          
            324_0  COME_FROM           312  '312'

 L. 117       324  LOAD_FAST                'formula'
              326  LOAD_METHOD              endswith
              328  LOAD_STR                 '('
              330  CALL_METHOD_1         1  ''
          332_334  POP_JUMP_IF_FALSE   344  'to 344'

 L. 118       336  LOAD_GLOBAL              _invalid_formula
              338  LOAD_STR                 'formula cannot end with open parenthesis'
              340  CALL_FUNCTION_1       1  ''
              342  POP_TOP          
            344_0  COME_FROM           332  '332'

 L. 121       344  LOAD_GLOBAL              list
              346  LOAD_FAST                'formula'
              348  CALL_FUNCTION_1       1  ''
              350  STORE_FAST               'input_list'

 L. 123       352  LOAD_GLOBAL              range
              354  LOAD_GLOBAL              len
              356  LOAD_FAST                'input_list'
              358  CALL_FUNCTION_1       1  ''
              360  CALL_FUNCTION_1       1  ''
              362  GET_ITER         
          364_366  FOR_ITER           1010  'to 1010'
              368  STORE_FAST               'i'

 L. 124   370_372  SETUP_FINALLY       984  'to 984'

 L. 126       374  LOAD_STR                 '('
              376  LOAD_STR                 ')'
              378  BUILD_LIST_2          2 
              380  STORE_FAST               'parentheses'

 L. 127       382  LOAD_STR                 '+'
              384  LOAD_STR                 '-'
              386  BUILD_LIST_2          2 
              388  STORE_FAST               'charge_symbols'

 L. 130       390  LOAD_FAST                'input_list'
              392  LOAD_FAST                'i'
              394  BINARY_SUBSCR    
              396  LOAD_METHOD              isalnum
              398  CALL_METHOD_0         0  ''

 L. 129   400_402  POP_JUMP_IF_TRUE    444  'to 444'

 L. 131       404  LOAD_FAST                'input_list'
              406  LOAD_FAST                'i'
              408  BINARY_SUBSCR    
              410  LOAD_FAST                'parentheses'
              412  COMPARE_OP               in

 L. 129   414_416  POP_JUMP_IF_TRUE    444  'to 444'

 L. 132       418  LOAD_FAST                'input_list'
              420  LOAD_FAST                'i'
              422  BINARY_SUBSCR    
              424  LOAD_FAST                'charge_symbols'
              426  COMPARE_OP               in

 L. 129   428_430  POP_JUMP_IF_TRUE    444  'to 444'

 L. 134       432  LOAD_GLOBAL              _invalid_formula
              434  LOAD_STR                 'contains invalid character'
              436  CALL_FUNCTION_1       1  ''
              438  POP_TOP          
          440_442  JUMP_FORWARD        980  'to 980'
            444_0  COME_FROM           428  '428'
            444_1  COME_FROM           414  '414'
            444_2  COME_FROM           400  '400'

 L. 136       444  LOAD_FAST                'input_list'
              446  LOAD_FAST                'i'
              448  BINARY_SUBSCR    
              450  LOAD_STR                 '('
              452  COMPARE_OP               ==
          454_456  POP_JUMP_IF_FALSE   550  'to 550'

 L. 138       458  LOAD_FAST                'input_list'
              460  LOAD_FAST                'i'
              462  LOAD_CONST               1
              464  BINARY_ADD       
              466  BINARY_SUBSCR    
              468  LOAD_METHOD              isalpha
              470  CALL_METHOD_0         0  ''
          472_474  POP_JUMP_IF_TRUE    484  'to 484'

 L. 139       476  LOAD_GLOBAL              _invalid_formula
              478  LOAD_STR                 'parentheses must contain elements'
              480  CALL_FUNCTION_1       1  ''
              482  POP_TOP          
            484_0  COME_FROM           472  '472'

 L. 142       484  SETUP_FINALLY       516  'to 516'

 L. 143       486  LOAD_FAST                'i'
              488  LOAD_FAST                'input_list'
              490  LOAD_METHOD              index
              492  LOAD_STR                 ')'
              494  LOAD_FAST                'i'
              496  CALL_METHOD_2         2  ''
              498  COMPARE_OP               <
          500_502  POP_JUMP_IF_TRUE    512  'to 512'

 L. 144       504  LOAD_GLOBAL              _invalid_formula

 L. 145       506  LOAD_STR                 'open parenthesis must precede closed parenthesis'

 L. 144       508  CALL_FUNCTION_1       1  ''
              510  POP_TOP          
            512_0  COME_FROM           500  '500'
              512  POP_BLOCK        
              514  JUMP_FORWARD        980  'to 980'
            516_0  COME_FROM_FINALLY   484  '484'

 L. 149       516  DUP_TOP          
              518  LOAD_GLOBAL              ValueError
              520  COMPARE_OP               exception-match
          522_524  POP_JUMP_IF_FALSE   544  'to 544'
              526  POP_TOP          
              528  POP_TOP          
              530  POP_TOP          

 L. 150       532  LOAD_GLOBAL              _invalid_formula
              534  LOAD_STR                 'open parenthesis must precede closed parenthesis'
              536  CALL_FUNCTION_1       1  ''
              538  POP_TOP          
              540  POP_EXCEPT       
              542  JUMP_FORWARD        980  'to 980'
            544_0  COME_FROM           522  '522'
              544  END_FINALLY      
          546_548  JUMP_FORWARD        980  'to 980'
            550_0  COME_FROM           454  '454'

 L. 162       550  LOAD_FAST                'input_list'
              552  LOAD_FAST                'i'
              554  BINARY_SUBSCR    
              556  LOAD_METHOD              isupper
              558  CALL_METHOD_0         0  ''
          560_562  POP_JUMP_IF_FALSE   724  'to 724'

 L. 163       564  SETUP_FINALLY       698  'to 698'

 L. 164       566  LOAD_FAST                'input_list'
              568  LOAD_FAST                'i'
              570  LOAD_CONST               1
              572  BINARY_ADD       
              574  BINARY_SUBSCR    
              576  LOAD_METHOD              islower
              578  CALL_METHOD_0         0  ''
          580_582  POP_JUMP_IF_FALSE   694  'to 694'

 L. 165       584  SETUP_FINALLY       642  'to 642'

 L. 166       586  LOAD_FAST                'input_list'
              588  LOAD_FAST                'i'
              590  LOAD_CONST               2
              592  BINARY_ADD       
              594  BINARY_SUBSCR    
              596  LOAD_METHOD              islower
              598  CALL_METHOD_0         0  ''
          600_602  POP_JUMP_IF_FALSE   638  'to 638'

 L. 167       604  LOAD_FAST                'input_list'
              606  LOAD_METHOD              pop
              608  LOAD_FAST                'i'
              610  LOAD_CONST               2
              612  BINARY_ADD       
              614  CALL_METHOD_1         1  ''
              616  STORE_FAST               'char'

 L. 168       618  LOAD_FAST                'input_list'
              620  LOAD_FAST                'i'
              622  LOAD_CONST               1
              624  BINARY_ADD       
              626  DUP_TOP_TWO      
              628  BINARY_SUBSCR    
              630  LOAD_FAST                'char'
              632  INPLACE_ADD      
              634  ROT_THREE        
              636  STORE_SUBSCR     
            638_0  COME_FROM           600  '600'
              638  POP_BLOCK        
              640  JUMP_FORWARD        664  'to 664'
            642_0  COME_FROM_FINALLY   584  '584'

 L. 169       642  DUP_TOP          
              644  LOAD_GLOBAL              IndexError
              646  COMPARE_OP               exception-match
          648_650  POP_JUMP_IF_FALSE   662  'to 662'
              652  POP_TOP          
              654  POP_TOP          
              656  POP_TOP          

 L. 170       658  POP_EXCEPT       
              660  JUMP_FORWARD        664  'to 664'
            662_0  COME_FROM           648  '648'
              662  END_FINALLY      
            664_0  COME_FROM           660  '660'
            664_1  COME_FROM           640  '640'

 L. 171       664  LOAD_FAST                'input_list'
              666  LOAD_METHOD              pop
              668  LOAD_FAST                'i'
              670  LOAD_CONST               1
              672  BINARY_ADD       
              674  CALL_METHOD_1         1  ''
              676  STORE_FAST               'char'

 L. 172       678  LOAD_FAST                'input_list'
              680  LOAD_FAST                'i'
              682  DUP_TOP_TWO      
              684  BINARY_SUBSCR    
              686  LOAD_FAST                'char'
              688  INPLACE_ADD      
              690  ROT_THREE        
              692  STORE_SUBSCR     
            694_0  COME_FROM           580  '580'
              694  POP_BLOCK        
              696  JUMP_FORWARD        980  'to 980'
            698_0  COME_FROM_FINALLY   564  '564'

 L. 173       698  DUP_TOP          
              700  LOAD_GLOBAL              IndexError
              702  COMPARE_OP               exception-match
          704_706  POP_JUMP_IF_FALSE   718  'to 718'
              708  POP_TOP          
              710  POP_TOP          
              712  POP_TOP          

 L. 174       714  POP_EXCEPT       
              716  JUMP_FORWARD        980  'to 980'
            718_0  COME_FROM           704  '704'
              718  END_FINALLY      
          720_722  JUMP_FORWARD        980  'to 980'
            724_0  COME_FROM           560  '560'

 L. 177       724  LOAD_FAST                'input_list'
              726  LOAD_FAST                'i'
              728  BINARY_SUBSCR    
              730  LOAD_METHOD              isnumeric
              732  CALL_METHOD_0         0  ''
          734_736  POP_JUMP_IF_FALSE   820  'to 820'

 L. 178       738  SETUP_FINALLY       796  'to 796'

 L. 179       740  LOAD_FAST                'i'
              742  LOAD_CONST               1
              744  BINARY_ADD       
              746  STORE_FAST               'j'

 L. 180       748  LOAD_FAST                'input_list'
              750  LOAD_FAST                'j'
              752  BINARY_SUBSCR    
              754  LOAD_METHOD              isnumeric
              756  CALL_METHOD_0         0  ''
          758_760  POP_JUMP_IF_FALSE   792  'to 792'

 L. 181       762  LOAD_FAST                'input_list'
              764  LOAD_METHOD              pop
              766  LOAD_FAST                'j'
              768  CALL_METHOD_1         1  ''
              770  STORE_FAST               'char'

 L. 182       772  LOAD_FAST                'input_list'
              774  LOAD_FAST                'i'
              776  DUP_TOP_TWO      
              778  BINARY_SUBSCR    
              780  LOAD_FAST                'char'
              782  INPLACE_ADD      
              784  ROT_THREE        
              786  STORE_SUBSCR     
          788_790  JUMP_BACK           748  'to 748'
            792_0  COME_FROM           758  '758'
              792  POP_BLOCK        
              794  JUMP_FORWARD        818  'to 818'
            796_0  COME_FROM_FINALLY   738  '738'

 L. 183       796  DUP_TOP          
              798  LOAD_GLOBAL              IndexError
              800  COMPARE_OP               exception-match
          802_804  POP_JUMP_IF_FALSE   816  'to 816'
              806  POP_TOP          
              808  POP_TOP          
              810  POP_TOP          

 L. 184       812  POP_EXCEPT       
              814  JUMP_FORWARD        818  'to 818'
            816_0  COME_FROM           802  '802'
              816  END_FINALLY      
            818_0  COME_FROM           814  '814'
            818_1  COME_FROM           794  '794'
              818  JUMP_FORWARD        980  'to 980'
            820_0  COME_FROM           734  '734'

 L. 187       820  LOAD_FAST                'input_list'
              822  LOAD_FAST                'i'
              824  BINARY_SUBSCR    
              826  LOAD_STR                 '+'
              828  COMPARE_OP               ==
          830_832  POP_JUMP_IF_TRUE    848  'to 848'
              834  LOAD_FAST                'input_list'
              836  LOAD_FAST                'i'
              838  BINARY_SUBSCR    
              840  LOAD_STR                 '-'
              842  COMPARE_OP               ==
          844_846  POP_JUMP_IF_FALSE   980  'to 980'
            848_0  COME_FROM           830  '830'

 L. 188       848  SETUP_FINALLY       956  'to 956'

 L. 189       850  LOAD_FAST                'input_list'
              852  LOAD_FAST                'i'
              854  LOAD_CONST               1
              856  BINARY_ADD       
              858  BINARY_SUBSCR    
              860  LOAD_STR                 '+'
              862  COMPARE_OP               ==
          864_866  POP_JUMP_IF_TRUE    886  'to 886'
              868  LOAD_FAST                'input_list'
              870  LOAD_FAST                'i'
              872  LOAD_CONST               1
              874  BINARY_ADD       
              876  BINARY_SUBSCR    
              878  LOAD_STR                 '-'
              880  COMPARE_OP               ==
          882_884  POP_JUMP_IF_FALSE   952  'to 952'
            886_0  COME_FROM           864  '864'

 L. 190       886  LOAD_FAST                'i'
              888  LOAD_CONST               1
              890  BINARY_ADD       
              892  STORE_FAST               'j'

 L. 191       894  LOAD_FAST                'input_list'
              896  LOAD_FAST                'j'
              898  BINARY_SUBSCR    
              900  LOAD_STR                 '+'
              902  COMPARE_OP               ==
          904_906  POP_JUMP_IF_TRUE    922  'to 922'
              908  LOAD_FAST                'input_list'
              910  LOAD_FAST                'j'
              912  BINARY_SUBSCR    
              914  LOAD_STR                 '-'
              916  COMPARE_OP               ==
          918_920  POP_JUMP_IF_FALSE   952  'to 952'
            922_0  COME_FROM           904  '904'

 L. 192       922  LOAD_FAST                'input_list'
              924  LOAD_METHOD              pop
              926  LOAD_FAST                'j'
              928  CALL_METHOD_1         1  ''
              930  STORE_FAST               'char'

 L. 193       932  LOAD_FAST                'input_list'
              934  LOAD_FAST                'i'
              936  DUP_TOP_TWO      
              938  BINARY_SUBSCR    
              940  LOAD_FAST                'char'
              942  INPLACE_ADD      
              944  ROT_THREE        
            946_0  COME_FROM           514  '514'
              946  STORE_SUBSCR     
          948_950  JUMP_BACK           894  'to 894'
            952_0  COME_FROM           918  '918'
            952_1  COME_FROM           882  '882'
              952  POP_BLOCK        
            954_0  COME_FROM           696  '696'
              954  JUMP_FORWARD        978  'to 978'
            956_0  COME_FROM_FINALLY   848  '848'

 L. 194       956  DUP_TOP          
              958  LOAD_GLOBAL              IndexError
              960  COMPARE_OP               exception-match
          962_964  POP_JUMP_IF_FALSE   976  'to 976'
              966  POP_TOP          
              968  POP_TOP          
              970  POP_TOP          

 L. 195       972  POP_EXCEPT       
            974_0  COME_FROM           716  '716'
            974_1  COME_FROM           542  '542'
              974  JUMP_FORWARD        978  'to 978'
            976_0  COME_FROM           962  '962'
              976  END_FINALLY      
            978_0  COME_FROM           974  '974'
            978_1  COME_FROM           954  '954'
              978  JUMP_FORWARD        980  'to 980'
            980_0  COME_FROM           978  '978'
            980_1  COME_FROM           844  '844'
            980_2  COME_FROM           818  '818'
            980_3  COME_FROM           720  '720'
            980_4  COME_FROM           546  '546'
            980_5  COME_FROM           440  '440'

 L. 198       980  POP_BLOCK        
              982  JUMP_BACK           364  'to 364'
            984_0  COME_FROM_FINALLY   370  '370'

 L. 200       984  DUP_TOP          
              986  LOAD_GLOBAL              IndexError
              988  COMPARE_OP               exception-match
          990_992  POP_JUMP_IF_FALSE  1004  'to 1004'
              994  POP_TOP          
              996  POP_TOP          
              998  POP_TOP          

 L. 201      1000  POP_EXCEPT       
             1002  JUMP_BACK           364  'to 364'
           1004_0  COME_FROM           990  '990'
             1004  END_FINALLY      
         1006_1008  JUMP_BACK           364  'to 364'

 L. 204      1010  LOAD_FAST                'input_list'
             1012  GET_ITER         
           1014_0  COME_FROM          1034  '1034'
           1014_1  COME_FROM          1024  '1024'
             1014  FOR_ITER           1050  'to 1050'
             1016  STORE_FAST               'item'

 L. 205      1018  LOAD_FAST                'item'
             1020  LOAD_METHOD              isalpha
             1022  CALL_METHOD_0         0  ''
         1024_1026  POP_JUMP_IF_FALSE  1014  'to 1014'

 L. 206      1028  LOAD_GLOBAL              is_valid_element
             1030  LOAD_FAST                'item'
             1032  CALL_FUNCTION_1       1  ''
         1034_1036  POP_JUMP_IF_TRUE   1014  'to 1014'

 L. 207      1038  LOAD_GLOBAL              _invalid_formula
             1040  LOAD_STR                 'invalid element symbol'
             1042  CALL_FUNCTION_1       1  ''
             1044  POP_TOP          
         1046_1048  JUMP_BACK          1014  'to 1014'

 L. 209      1050  LOAD_FAST                'input_list'
             1052  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM' instruction at offset 946_0


def _remove_parentheses(formula):
    """
    Remove parentheses from a formula and distribute the associated numbers
    as appropriate.

    NOTE: does not support nested parentheses as these violate
    the formatting rules for chemical formulas

    >>> _remove_parentheses('(Fe2)(SO4)3')
    ['Fe', '2', 'S', '3', 'O', '12']

    See Also
    --------
    _check_formula
    """
    input_list = _check_formula(formula)
    output_list = []
    i = 0
    while i < len(input_list):
        if input_list[i] == '(':
            start = i
            stop = input_list.index')'i
            if input_list[(stop + 1)].isnumeric():
                num = int(input_list[(stop + 1)])
                i = stop + 2
            else:
                num = 1
                i = stop + 1
        for j in range(start + 1, stop):
            if input_list[j].isalpha() and input_list[(j + 1)].isnumeric():
                output_list.append(input_list[j])
                output_list.append(str(int(input_list[(j + 1)]) * num))
            elif input_list[j].isalpha():
                output_list.append(input_list[j])
                if num > 1:
                    output_list.append(str(num))
            output_list.append(input_list[i])
            i = i + 1

    return output_list


def _consolidate_formula(formula):
    """
    Consolidate a formula into its simplest form, containing only one
    instance of each element and no parentheses

    Examples
    --------
    >>> _consolidate_formula('CH3(CH2)6CH3')
    ['C', 8, 'H', 18]
    >>> _consolidate_formula('(Fe)2(SO4)4')
    ['Fe', 2, 'S', 4, 'O', 16]
    >>> _consolidate_formula('Fe(OH)2+')
    ['Fe', 1, 'O', 2, 'H', 2, '+1']

    """
    input_list = _remove_parentheses(formula)
    output_list = []
    for i in range(0, len(input_list)):
        if input_list[i].isalpha():
            try:
                if input_list[(i + 1)].isnumeric():
                    quantity = input_list[(i + 1)]
                else:
                    quantity = 1
            except IndexError:
                quantity = 1

            if input_list[i] in output_list:
                index = output_list.index(input_list[i])
                output_list[(index + 1)] += int(quantity)
            else:
                output_list.append(input_list[i])
                output_list.append(int(quantity))
        charge = get_formal_charge(formula)
        if charge > 0:
            output_list.append('+' + str(charge))
        else:
            if charge < 0:
                output_list.append(str(charge))
        return output_list


def is_valid_element(formula):
    """
    Check whether a string is a valid atomic symbol

    Parameters
    ----------
    :formula: str
            String representing an atomic symbol. First letter must be
            uppercase, second letter must be lowercase.

    Returns
    -------
    bool
            True if the string is a valid atomic symbol. False otherwise.

    Examples
    --------
    >>> is_valid_element('Cu')
    True
    >>> is_valid_element('Na+')
    False
    """
    if formula in atomic_numbers:
        return True
    _invalid_formula('invalid element symbol')
    return False


def is_valid_formula--- This code section failed: ---

 L. 389         0  SETUP_FINALLY        16  'to 16'

 L. 390         2  LOAD_GLOBAL              _check_formula
                4  LOAD_FAST                'formula'
                6  CALL_FUNCTION_1       1  ''
                8  POP_TOP          

 L. 391        10  POP_BLOCK        
               12  LOAD_CONST               True
               14  RETURN_VALUE     
             16_0  COME_FROM_FINALLY     0  '0'

 L. 392        16  POP_TOP          
               18  POP_TOP          
               20  POP_TOP          

 L. 393        22  POP_EXCEPT       
               24  LOAD_CONST               False
               26  RETURN_VALUE     
               28  END_FINALLY      

Parse error at or near `RETURN_VALUE' instruction at offset 14


def contains(formula, element):
    """
    Check whether a formula contains a given element.

    Parameters
    ----------
    formula: str
        String representing a molecular formula. e.g. 'H2O' or 'FeOH+'
        Valid molecular formulas must meet the following criteria:

        #. Are composed of valid atomic symbols that start with capital letters
        #. Contain no non-alphanumeric characters other than '(', ')',
           '+', or '-'
        #. If a '+' or '-' is present, the formula must contain ONLY '+' or
           '-' (e.g. 'Na+-' is invalid) and the formula must end with either
           a series of charges (e.g. 'Fe+++') or a numeric charge (e.g. 'Fe+3')
        #. Formula must contain matching numbers of '(' and ')'
        #. Open parentheses must precede closed parentheses
    element: str
        String representing the element to check for. Must be a valid element
        name.

    Returns
    -------
    bool
            True if the formula contains the element. False otherwise.

    Examples
    --------
    >>> contains('Fe2(SO4)3','Fe')
    True
    >>> contains('NaCOOH','S')
    False
    """
    if is_valid_element(element):
        if element in get_elements(formula):
            return True
        return False


def get_element_numbers(formula):
    """
    Return the atomic numbers of the elements in a chemical formula

    Parameters
    ----------
    formula: str
            String representing a chemical formula

    Examples
    --------
    >>> get_element_numbers('FeSO4')
    [26, 16, 8]

    """
    input_list = get_elements(formula)
    output_list = []
    for item in input_list:
        output_list.append(atomic_numbers[item][0])
    else:
        return output_list


def get_element_names(formula):
    """
    Return the names of the elements in a chemical formula

    Parameters
    ----------
    formula: str
            String representing a chemical formula

    Examples
    --------
    >>> get_element_names('FeSO4')
    ['Iron', 'Sulfur', 'Oxygen']

    """
    input_list = get_elements(formula)
    output_list = []
    for item in input_list:
        output_list.append(atomic_numbers[item][1])
    else:
        return output_list


def hill_order--- This code section failed: ---

 L. 518         0  LOAD_GLOBAL              _consolidate_formula
                2  LOAD_FAST                'formula'
                4  CALL_FUNCTION_1       1  ''
                6  STORE_FAST               'temp_list'

 L. 519         8  LOAD_STR                 ''
               10  STORE_FAST               'hill'

 L. 522        12  LOAD_STR                 'C'
               14  LOAD_FAST                'temp_list'
               16  COMPARE_OP               in
               18  POP_JUMP_IF_FALSE   136  'to 136'

 L. 523        20  LOAD_CONST               ('C', 'H')
               22  GET_ITER         
             24_0  COME_FROM            34  '34'
               24  FOR_ITER            136  'to 136'
               26  STORE_FAST               'item'

 L. 524        28  LOAD_FAST                'item'
               30  LOAD_FAST                'temp_list'
               32  COMPARE_OP               in
               34  POP_JUMP_IF_FALSE    24  'to 24'

 L. 525        36  LOAD_FAST                'temp_list'
               38  LOAD_METHOD              index
               40  LOAD_FAST                'item'
               42  CALL_METHOD_1         1  ''
               44  STORE_FAST               'index'

 L. 526        46  LOAD_FAST                'hill'
               48  LOAD_FAST                'item'
               50  INPLACE_ADD      
               52  STORE_FAST               'hill'

 L. 528        54  LOAD_FAST                'temp_list'
               56  LOAD_FAST                'index'
               58  LOAD_CONST               1
               60  BINARY_ADD       
               62  BINARY_SUBSCR    
               64  LOAD_CONST               1
               66  COMPARE_OP               >
               68  POP_JUMP_IF_FALSE    94  'to 94'

 L. 529        70  LOAD_FAST                'hill'
               72  LOAD_GLOBAL              str
               74  LOAD_FAST                'temp_list'
               76  LOAD_METHOD              pop
               78  LOAD_FAST                'index'
               80  LOAD_CONST               1
               82  BINARY_ADD       
               84  CALL_METHOD_1         1  ''
               86  CALL_FUNCTION_1       1  ''
               88  INPLACE_ADD      
               90  STORE_FAST               'hill'
               92  JUMP_FORWARD        124  'to 124'
             94_0  COME_FROM            68  '68'

 L. 530        94  LOAD_FAST                'temp_list'
               96  LOAD_FAST                'index'
               98  LOAD_CONST               1
              100  BINARY_ADD       
              102  BINARY_SUBSCR    
              104  LOAD_CONST               1
              106  COMPARE_OP               ==
              108  POP_JUMP_IF_FALSE   124  'to 124'

 L. 531       110  LOAD_FAST                'temp_list'
              112  LOAD_METHOD              pop
              114  LOAD_FAST                'index'
              116  LOAD_CONST               1
              118  BINARY_ADD       
              120  CALL_METHOD_1         1  ''
              122  POP_TOP          
            124_0  COME_FROM           108  '108'
            124_1  COME_FROM            92  '92'

 L. 532       124  LOAD_FAST                'temp_list'
              126  LOAD_METHOD              remove
              128  LOAD_FAST                'item'
              130  CALL_METHOD_1         1  ''
              132  POP_TOP          
              134  JUMP_BACK            24  'to 24'
            136_0  COME_FROM            18  '18'

 L. 536       136  BUILD_LIST_0          0 
              138  STORE_FAST               'tuple_list'

 L. 537       140  LOAD_FAST                'temp_list'
              142  GET_ITER         
              144  FOR_ITER            220  'to 220'
              146  STORE_FAST               'item'

 L. 538       148  LOAD_FAST                'temp_list'
              150  LOAD_METHOD              index
              152  LOAD_FAST                'item'
              154  CALL_METHOD_1         1  ''
              156  STORE_FAST               'index'

 L. 539       158  SETUP_FINALLY       194  'to 194'

 L. 540       160  LOAD_FAST                'item'
              162  LOAD_METHOD              isalpha
              164  CALL_METHOD_0         0  ''
              166  POP_JUMP_IF_FALSE   190  'to 190'

 L. 541       168  LOAD_FAST                'tuple_list'
              170  LOAD_METHOD              append
              172  LOAD_FAST                'item'
              174  LOAD_FAST                'temp_list'
              176  LOAD_FAST                'index'
              178  LOAD_CONST               1
              180  BINARY_ADD       
              182  BINARY_SUBSCR    
              184  BUILD_TUPLE_2         2 
              186  CALL_METHOD_1         1  ''
              188  POP_TOP          
            190_0  COME_FROM           166  '166'
              190  POP_BLOCK        
              192  JUMP_BACK           144  'to 144'
            194_0  COME_FROM_FINALLY   158  '158'

 L. 542       194  DUP_TOP          
              196  LOAD_GLOBAL              AttributeError
              198  COMPARE_OP               exception-match
              200  POP_JUMP_IF_FALSE   216  'to 216'
              202  POP_TOP          
              204  POP_TOP          
              206  POP_TOP          

 L. 543       208  POP_EXCEPT       
              210  JUMP_BACK           144  'to 144'
              212  POP_EXCEPT       
              214  JUMP_BACK           144  'to 144'
            216_0  COME_FROM           200  '200'
              216  END_FINALLY      
              218  JUMP_BACK           144  'to 144'

 L. 546       220  LOAD_FAST                'tuple_list'
              222  LOAD_METHOD              sort
              224  CALL_METHOD_0         0  ''
              226  POP_TOP          

 L. 549       228  LOAD_FAST                'tuple_list'
              230  GET_ITER         
              232  FOR_ITER            298  'to 298'
              234  STORE_FAST               'item'

 L. 550       236  LOAD_FAST                'item'
              238  LOAD_CONST               1
              240  BINARY_SUBSCR    
              242  LOAD_CONST               1
              244  COMPARE_OP               ==
          246_248  POP_JUMP_IF_FALSE   268  'to 268'

 L. 551       250  LOAD_FAST                'hill'
              252  LOAD_GLOBAL              str
              254  LOAD_FAST                'item'
              256  LOAD_CONST               0
              258  BINARY_SUBSCR    
              260  CALL_FUNCTION_1       1  ''
              262  INPLACE_ADD      
              264  STORE_FAST               'hill'
              266  JUMP_BACK           232  'to 232'
            268_0  COME_FROM           246  '246'

 L. 553       268  LOAD_FAST                'hill'
              270  LOAD_GLOBAL              str
              272  LOAD_FAST                'item'
              274  LOAD_CONST               0
              276  BINARY_SUBSCR    
              278  CALL_FUNCTION_1       1  ''
              280  LOAD_GLOBAL              str
              282  LOAD_FAST                'item'
              284  LOAD_CONST               1
              286  BINARY_SUBSCR    
              288  CALL_FUNCTION_1       1  ''
              290  BINARY_ADD       
              292  INPLACE_ADD      
              294  STORE_FAST               'hill'
              296  JUMP_BACK           232  'to 232'

 L. 556       298  LOAD_GLOBAL              get_formal_charge
              300  LOAD_FAST                'formula'
              302  CALL_FUNCTION_1       1  ''
              304  STORE_FAST               'charge'

 L. 557       306  LOAD_FAST                'charge'
              308  LOAD_CONST               0
              310  COMPARE_OP               !=
          312_314  POP_JUMP_IF_FALSE   328  'to 328'

 L. 558       316  LOAD_FAST                'hill'
              318  LOAD_GLOBAL              str
              320  LOAD_FAST                'charge'
              322  CALL_FUNCTION_1       1  ''
              324  INPLACE_ADD      
              326  STORE_FAST               'hill'
            328_0  COME_FROM           312  '312'

 L. 560       328  LOAD_FAST                'hill'
              330  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_EXCEPT' instruction at offset 212


def get_elements(formula):
    """
    Return a list of strings representing the elements in a
    molecular formula, with no duplicates.

    Examples
    --------
    >>> get_elements('FeSO4')
    ['Fe', 'S', 'O']
    >>> get_elements('CH3(CH2)4(CO)3')
    ['C', 'H', 'O']

    See Also
    --------
    _check_formula
    """
    input_list = _consolidate_formula(formula)
    output_list = []
    for item in input_list:
        if item in atomic_numbers:
            output_list.append(item)
        return output_list


def get_formal_charge(formula):
    """
    Return the formal charge on a molecule based on its formula

    Examples
    --------
    >>> get_formal_charge('Na+')
    1
    >>> get_formal_charge('PO4-3')
    -3
    >>> get_formal_charge('Fe+++')
    3

    See Also
    --------
    _check_formula

    """
    input_list = _check_formula(formula)
    if '+' in input_list:
        index = input_list.index('+')
        try:
            formal_charge = 1 * int(input_list[(index + 1)])
        except IndexError:
            formal_charge = 1

    else:
        if '-' in input_list:
            index = input_list.index('-')
            try:
                formal_charge = -1 * int(input_list[(index + 1)])
            except IndexError:
                formal_charge = -1

        else:
            if '+' in input_list[(-1)]:
                formal_charge = int(1 * input_list[(-1)].count('+'))
            else:
                if '-' in input_list[(-1)]:
                    formal_charge = int(-1 * input_list[(-1)].count('-'))
                else:
                    formal_charge = 0
    return formal_charge


def get_element_mole_ratio(formula, element):
    """
    compute the  moles of a specific element per mole of formula

    Parameters
    ----------
    formula: str
        String representing a molecular formula. e.g. 'H2O' or 'FeOH+'
        Valid molecular formulas must meet the following criteria:

        #. Are composed of valid atomic symbols that start with capital letters
        #. Contain no non-alphanumeric characters other than '(', ')',
           '+', or '-'
        #. If a '+' or '-' is present, the formula must contain ONLY '+' or
           '-' (e.g. 'Na+-' is invalid) and the formula must end with either
           a series of charges (e.g. 'Fe+++') or a numeric charge (e.g. 'Fe+3')
        #. Formula must contain matching numbers of '(' and ')'
        #. Open parentheses must precede closed parentheses
    element: str
        String representing the element to check for. Must be a valid element
        name.

    Returns
    -------
    number
            The number of moles of element per mole of formula, mol/mol.

    >>> get_element_mole_ratio('NaCl','Na')
    1
    >>> get_element_mole_ratio('H2O','H')
    2
    >>> get_element_mole_ratio('H2O','Br')
    0
    >>> get_element_mole_ratio('CH3CH2CH3','C')
    3

    See Also
    --------
    contains
    consolidate_formula
    get_element_weight
    get_element_weight_fraction

    """
    if contains(formula, element):
        input_list = _consolidate_formula(formula)
        index = input_list.index(element)
        moles = input_list[(index + 1)]
    else:
        moles = 0
    return moles


def get_element_weight(formula, element):
    """
    compute the  weight of a specific element in a formula

    Parameters
    ----------
    formula: str
        String representing a molecular formula. e.g. 'H2O' or 'FeOH+'
        Valid molecular formulas must meet the following criteria:

        #. Are composed of valid atomic symbols that start with capital letters
        #. Contain no non-alphanumeric characters other than '(', ')',
           '+', or '-'
        #. If a '+' or '-' is present, the formula must contain ONLY '+' or
           '-' (e.g. 'Na+-' is invalid) and the formula must end with either
           a series of charges (e.g. 'Fe+++') or a numeric charge (e.g. 'Fe+3')
        #. Formula must contain matching numbers of '(' and ')'
        #. Open parentheses must precede closed parentheses
    element: str
        String representing the element to check for. Must be a valid element
        name.

    Returns
    -------
    number
            The weight of the specified element within the formula, g/mol.

    >>> get_element_weight('NaCl','Na')
    22.98977
    >>> get_element_weight('H2O','H')
    2.01588
    >>> get_element_weight('H2O','Br')
    0.0
    >>> get_element_weight('CH3CH2CH3','C')
    36.0321

    See Also
    --------
    contains
    _consolidate_formula
    elements
    get_element_mole_ratio

    """
    moles = get_element_mole_ratio(formula, element)
    if moles != 0:
        from pyEQL.elements import ELEMENTS
        mass = ELEMENTS[element].mass
        wt = mass * moles
    else:
        wt = 0.0
    return wt


def get_element_weight_fraction(formula, element):
    """
    compute the  weight fraction of a specific element in a formula

    Parameters
    ----------
    formula: str
        String representing a molecular formula. e.g. 'H2O' or 'FeOH+'
        Valid molecular formulas must meet the following criteria:

        #. Are composed of valid atomic symbols that start with capital letters
        #. Contain no non-alphanumeric characters other than '(', ')',
           '+', or '-'
        #. If a '+' or '-' is present, the formula must contain ONLY '+' or
           '-' (e.g. 'Na+-' is invalid) and the formula must end with either
           a series of charges (e.g. 'Fe+++') or a numeric charge (e.g. 'Fe+3')
        #. Formula must contain matching numbers of '(' and ')'
        #. Open parentheses must precede closed parentheses
    element: str
        String representing the element to check for. Must be a valid element
        name.

    Returns
    -------
    number
            The weight fraction of the specified element within the formula.

    >>> get_element_weight_fraction('NaCl','Na')
    0.39337...
    >>> get_element_weight_fraction('H2O','H')
    0.111898...
    >>> get_element_weight_fraction('H2O','Br')
    0.0
    >>> get_element_weight_fraction('CH3CH2CH3','C')
    0.8171355...

    See Also
    --------
    get_element_weight
    contains
    _consolidate_formula
    elements

    """
    wt = get_element_weight(formula, element)
    frac = wt / get_molecular_weight(formula)
    return frac


def get_molecular_weight(formula):
    """
    compute the molecular weight of a formula

    >>> get_molecular_weight('Na+')
    22.98977
    >>> get_molecular_weight('H2O')
    18.01528
    >>> get_molecular_weight('CH3CH2CH3')
    44.09562

    See Also
    --------
    _consolidate_formula
    elements

    """
    from pyEQL.elements import ELEMENTS
    input_list = _consolidate_formula(formula)
    mw = 0
    for item in input_list:
        try:
            if item.isalpha():
                index = input_list.index(item)
                quantity = input_list[(index + 1)]
                mass = ELEMENTS[item].mass
                mw += mass * quantity
        except AttributeError:
            pass

    else:
        return mw


def print_latex(formula):
    """
    Print a LaTeX - formatted version of the formula

    Examples
    ---------
    >>> print_latex('Fe2SO4')
    Fe_2SO_4
    >>> print_latex('CH3CH2CH3')
    CH_3CH_2CH_3
    >>> print_latex('Fe2(OH)2+2')
    Fe_2(OH)_2^+^2

    """
    output = ''
    for i in range(len(formula)):
        if formula[i].isnumeric():
            if i > 0:
                if formula[(i - 1)] == '+' or formula[(i - 1)] == '-':
                    output += '^'
                else:
                    output += '_'
        if formula[i] == '+' or formula[i] == '-':
            output += '^'
        output += formula[i]
    else:
        print(output)


atomic_numbers = {'H':(1, 'Hydrogen'), 
 'He':(2, 'Helium'), 
 'Li':(3, 'Lithium'), 
 'Be':(4, 'Beryllium'), 
 'B':(5, 'Boron'), 
 'C':(6, 'Carbon'), 
 'N':(7, 'Nitrogen'), 
 'O':(8, 'Oxygen'), 
 'F':(9, 'Fluorine'), 
 'Ne':(10, 'Neon'), 
 'Na':(11, 'Sodium'), 
 'Mg':(12, 'Magnesium'), 
 'Al':(13, 'Aluminum'), 
 'Si':(14, 'Silicon'), 
 'P':(15, 'Phosphorus'), 
 'S':(16, 'Sulfur'), 
 'Cl':(17, 'Chlorine'), 
 'Ar':(18, 'Argon'), 
 'K':(19, 'Potassium'), 
 'Ca':(20, 'Calcium'), 
 'Sc':(21, 'Scandium'), 
 'Ti':(22, 'Titanium'), 
 'V':(23, 'Vanadium'), 
 'Cr':(24, 'Chromium'), 
 'Mn':(25, 'Manganese'), 
 'Fe':(26, 'Iron'), 
 'Co':(27, 'Cobalt'), 
 'Ni':(28, 'Nickel'), 
 'Cu':(29, 'Copper'), 
 'Zn':(30, 'Zinc'), 
 'Ga':(31, 'Gallium'), 
 'Ge':(32, 'Germanium'), 
 'As':(33, 'Arsenic'), 
 'Se':(34, 'Selenium'), 
 'Br':(35, 'Bromine'), 
 'Kr':(36, 'Krypton'), 
 'Rb':(37, 'Rubidium'), 
 'Sr':(38, 'Strontium'), 
 'Y':(39, 'Yttrium'), 
 'Zr':(40, 'Zirconium'), 
 'Nb':(41, 'Niobium'), 
 'Mo':(42, 'Molybdenum'), 
 'Tc':(43, 'Technetium'), 
 'Ru':(44, 'Ruthenium'), 
 'Rh':(45, 'Rhodium'), 
 'Pd':(46, 'Palladium'), 
 'Ag':(47, 'Silver'), 
 'Cd':(48, 'Cadmium'), 
 'In':(49, 'Indium'), 
 'Sn':(50, 'Tin'), 
 'Sb':(51, 'Antimony'), 
 'Te':(52, 'Tellurium'), 
 'I':(53, 'Iodine'), 
 'Xe':(54, 'Xenon'), 
 'Cs':(55, 'Cesium'), 
 'Ba':(56, 'Barium'), 
 'La':(57, 'Lanthanum'), 
 'Ce':(58, 'Cerium'), 
 'Pr':(59, 'Praseodymium'), 
 'Nd':(60, 'Neodymium'), 
 'Pm':(61, 'Promethium'), 
 'Sm':(62, 'Samarium'), 
 'Eu':(63, 'Europium'), 
 'Gd':(64, 'Gadolinium'), 
 'Tb':(65, 'Terbium'), 
 'Dy':(66, 'Dysprosium'), 
 'Ho':(67, 'Holmium'), 
 'Er':(68, 'Erbium'), 
 'Tm':(69, 'Thulium'), 
 'Yb':(70, 'Ytterbium'), 
 'Lu':(71, 'Lutetium'), 
 'Hf':(72, 'Hafnium'), 
 'Ta':(73, 'Tantalum'), 
 'W':(74, 'Tungsten'), 
 'Re':(75, 'Rhenium'), 
 'Os':(76, 'Osmium'), 
 'Ir':(77, 'Iridium'), 
 'Pt':(78, 'Platinum'), 
 'Au':(79, 'Gold'), 
 'Hg':(80, 'Mercury'), 
 'Tl':(81, 'Thallium'), 
 'Pb':(82, 'Lead'), 
 'Bi':(83, 'Bismuth'), 
 'Po':(84, 'Polonium'), 
 'At':(85, 'Astatine'), 
 'Rn':(86, 'Radon'), 
 'Fr':(87, 'Francium'), 
 'Ra':(88, 'Radium'), 
 'Ac':(89, 'Actinium'), 
 'Th':(90, 'Thorium'), 
 'Pa':(91, 'Protactinium'), 
 'U':(92, 'Uranium'), 
 'Np':(93, 'Neptunium'), 
 'Pu':(94, 'Plutonium'), 
 'Am':(95, 'Americium'), 
 'Cm':(96, 'Curium'), 
 'Bk':(97, 'Berkelium'), 
 'Cf':(98, 'Californium'), 
 'Es':(99, 'Einsteinium'), 
 'Fm':(100, 'Fermium'), 
 'Md':(101, 'Mendelevium'), 
 'No':(102, 'Nobelium'), 
 'Lr':(103, 'Lawrencium'), 
 'Rf':(104, 'Rutherfordium'), 
 'Db':(105, 'Dubnium'), 
 'Sg':(106, 'Seaborgium'), 
 'Bh':(107, 'Bohrium'), 
 'Hs':(108, 'Hassium'), 
 'Mt':(109, 'Meitnerium'), 
 'Ds':(110, 'Darmstadtium'), 
 'Rg':(111, 'Roentgenium'), 
 'Cn':(112, 'Copernicium'), 
 'Uut':(113, 'Ununtrium'), 
 'Fl':(114, 'Flerovium'), 
 'Uup':(115, 'Ununpentium'), 
 'Lv':(116, 'Livermorium'), 
 'Uus':(117, 'Ununseptium'), 
 'Uuo':(118, 'Ununoctium')}