# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/BioClients/pubchem/ftp/pubchem_ftp_compound_assaystats.py
# Compiled at: 2020-03-30 12:51:55
# Size of source mod 2**32: 9488 bytes
import os, sys, re, getopt, gzip, zipfile, hier_scaffolds_assaystats

def main--- This code section failed: ---

 L.  31         0  LOAD_GLOBAL              os
                2  LOAD_ATTR                path
                4  LOAD_METHOD              basename
                6  LOAD_GLOBAL              sys
                8  LOAD_ATTR                argv
               10  LOAD_CONST               0
               12  BINARY_SUBSCR    
               14  CALL_METHOD_1         1  ''
               16  STORE_GLOBAL             PROG

 L.  32        18  LOAD_GLOBAL              os
               20  LOAD_METHOD              getcwd
               22  CALL_METHOD_0         0  ''
               24  LOAD_STR                 '/data/scratch'
               26  BINARY_ADD       
               28  STORE_GLOBAL             SCRATCHDIR

 L.  34        30  LOAD_STR                 '\n  %(PROG)s - \n\n  required:\n  --inmols=<INMOLS> ... mols w/ cids (smiles)\n  --csvdir=<DIR>   ... dir containing input csv.gz assay data\n  --zipdir=<DIR>   ... dir containing zipfiles containing input csv.gz assay data\n  --csvfile=<FILE>   ... input csv.gz assay data\n  --o=<OUTSCAFS> ... output mols with data (smiles)\n\n  options:\n  --aids=<AIDS> ... list of AIDs to select within --csvdir dir\n  --aidfile=<AIDFILE> ... file of AIDs to select within --csvdir dir\n  --cidfile=<CIDFILE> ... file of CIDs to select (ignore others)\n\n  --use_sids     ... use SIDs instead of CIDs (all i/o)\n  --n_max_aids=<N> ... mostly for debugging\n  --v            ... verbose\n  --vv           ... very verbose\n  --h            ... this help\n'

 L.  54        32  LOAD_STR                 'PROG'
               34  LOAD_GLOBAL              PROG
               36  BUILD_MAP_1           1 

 L.  34        38  BINARY_MODULO    
               40  STORE_FAST               'usage'

 L.  56        42  LOAD_CODE                <code_object ErrorExit>
               44  LOAD_STR                 'main.<locals>.ErrorExit'
               46  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               48  STORE_FAST               'ErrorExit'

 L.  61        50  LOAD_CONST               None
               52  STORE_FAST               'csvdir'

 L.  62        54  LOAD_STR                 '/home/data/pubchem/bioassay/csv/data'
               56  STORE_FAST               'zipdir'

 L.  63        58  LOAD_CONST               None
               60  STORE_FAST               'csvfile'

 L.  63        62  LOAD_CONST               0
               64  STORE_FAST               'verbose'

 L.  64        66  LOAD_CONST               None
               68  STORE_FAST               'ofile'

 L.  64        70  LOAD_CONST               None
               72  STORE_FAST               'inmolsfile'

 L.  65        74  LOAD_CONST               None
               76  STORE_FAST               'aids'

 L.  65        78  LOAD_CONST               None
               80  STORE_FAST               'aidfile'

 L.  65        82  LOAD_CONST               None
               84  STORE_FAST               'cidfile'

 L.  66        86  LOAD_CONST               False
               88  STORE_FAST               'use_sids'

 L.  67        90  LOAD_CONST               None
               92  STORE_FAST               'n_max_aids'

 L.  68        94  LOAD_GLOBAL              getopt
               96  LOAD_METHOD              getopt
               98  LOAD_GLOBAL              sys
              100  LOAD_ATTR                argv
              102  LOAD_CONST               1
              104  LOAD_CONST               None
              106  BUILD_SLICE_2         2 
              108  BINARY_SUBSCR    
              110  LOAD_STR                 ''
              112  LOAD_STR                 'h'
              114  LOAD_STR                 'v'
              116  LOAD_STR                 'vv'
              118  LOAD_STR                 'csvdir='
              120  LOAD_STR                 'zipdir='

 L.  69       122  LOAD_STR                 'aids='

 L.  69       124  LOAD_STR                 'aidfile='

 L.  69       126  LOAD_STR                 'csvfile='

 L.  69       128  LOAD_STR                 'o='

 L.  69       130  LOAD_STR                 'inmols='

 L.  69       132  LOAD_STR                 'n_max_aids='

 L.  70       134  LOAD_STR                 'cidfile='

 L.  70       136  LOAD_STR                 'use_sids'

 L.  68       138  BUILD_LIST_13        13 
              140  CALL_METHOD_3         3  ''
              142  UNPACK_SEQUENCE_2     2 
              144  STORE_FAST               'opts'
              146  STORE_FAST               'pargs'

 L.  71       148  LOAD_FAST                'opts'
              150  POP_JUMP_IF_TRUE    160  'to 160'

 L.  71       152  LOAD_FAST                'ErrorExit'
              154  LOAD_FAST                'usage'
              156  CALL_FUNCTION_1       1  ''
              158  POP_TOP          
            160_0  COME_FROM           150  '150'

 L.  72       160  LOAD_FAST                'opts'
              162  GET_ITER         
              164  FOR_ITER            392  'to 392'
              166  UNPACK_SEQUENCE_2     2 
              168  STORE_FAST               'opt'
              170  STORE_FAST               'val'

 L.  73       172  LOAD_FAST                'opt'
              174  LOAD_STR                 '--h'
              176  COMPARE_OP               ==
              178  POP_JUMP_IF_FALSE   190  'to 190'

 L.  73       180  LOAD_FAST                'ErrorExit'
              182  LOAD_FAST                'usage'
              184  CALL_FUNCTION_1       1  ''
              186  POP_TOP          
              188  JUMP_BACK           164  'to 164'
            190_0  COME_FROM           178  '178'

 L.  74       190  LOAD_FAST                'opt'
              192  LOAD_STR                 '--inmols'
              194  COMPARE_OP               ==
              196  POP_JUMP_IF_FALSE   204  'to 204'

 L.  74       198  LOAD_FAST                'val'
              200  STORE_FAST               'inmolsfile'
              202  JUMP_BACK           164  'to 164'
            204_0  COME_FROM           196  '196'

 L.  75       204  LOAD_FAST                'opt'
              206  LOAD_STR                 '--o'
              208  COMPARE_OP               ==
              210  POP_JUMP_IF_FALSE   218  'to 218'

 L.  75       212  LOAD_FAST                'val'
              214  STORE_FAST               'ofile'
              216  JUMP_BACK           164  'to 164'
            218_0  COME_FROM           210  '210'

 L.  76       218  LOAD_FAST                'opt'
              220  LOAD_STR                 '--csvdir'
              222  COMPARE_OP               ==
              224  POP_JUMP_IF_FALSE   232  'to 232'

 L.  76       226  LOAD_FAST                'val'
              228  STORE_FAST               'csvdir'
              230  JUMP_BACK           164  'to 164'
            232_0  COME_FROM           224  '224'

 L.  77       232  LOAD_FAST                'opt'
              234  LOAD_STR                 '--zipdir'
              236  COMPARE_OP               ==
              238  POP_JUMP_IF_FALSE   246  'to 246'

 L.  77       240  LOAD_FAST                'val'
              242  STORE_FAST               'zipdir'
              244  JUMP_BACK           164  'to 164'
            246_0  COME_FROM           238  '238'

 L.  78       246  LOAD_FAST                'opt'
              248  LOAD_STR                 '--csvfile'
              250  COMPARE_OP               ==
          252_254  POP_JUMP_IF_FALSE   262  'to 262'

 L.  78       256  LOAD_FAST                'val'
              258  STORE_FAST               'csvfile'
              260  JUMP_BACK           164  'to 164'
            262_0  COME_FROM           252  '252'

 L.  79       262  LOAD_FAST                'opt'
              264  LOAD_STR                 '--aids'
              266  COMPARE_OP               ==
          268_270  POP_JUMP_IF_FALSE   278  'to 278'

 L.  79       272  LOAD_FAST                'val'
              274  STORE_FAST               'aids'
              276  JUMP_BACK           164  'to 164'
            278_0  COME_FROM           268  '268'

 L.  80       278  LOAD_FAST                'opt'
              280  LOAD_STR                 '--aidfile'
              282  COMPARE_OP               ==
          284_286  POP_JUMP_IF_FALSE   294  'to 294'

 L.  80       288  LOAD_FAST                'val'
              290  STORE_FAST               'aidfile'
              292  JUMP_BACK           164  'to 164'
            294_0  COME_FROM           284  '284'

 L.  81       294  LOAD_FAST                'opt'
              296  LOAD_STR                 '--cidfile'
              298  COMPARE_OP               ==
          300_302  POP_JUMP_IF_FALSE   310  'to 310'

 L.  81       304  LOAD_FAST                'val'
              306  STORE_FAST               'cidfile'
              308  JUMP_BACK           164  'to 164'
            310_0  COME_FROM           300  '300'

 L.  82       310  LOAD_FAST                'opt'
              312  LOAD_STR                 '--use_sids'
              314  COMPARE_OP               ==
          316_318  POP_JUMP_IF_FALSE   326  'to 326'

 L.  82       320  LOAD_CONST               True
              322  STORE_FAST               'use_sids'
              324  JUMP_BACK           164  'to 164'
            326_0  COME_FROM           316  '316'

 L.  83       326  LOAD_FAST                'opt'
              328  LOAD_STR                 '--n_max_aids'
              330  COMPARE_OP               ==
          332_334  POP_JUMP_IF_FALSE   346  'to 346'

 L.  83       336  LOAD_GLOBAL              int
              338  LOAD_FAST                'val'
              340  CALL_FUNCTION_1       1  ''
              342  STORE_FAST               'n_max_aids'
              344  JUMP_BACK           164  'to 164'
            346_0  COME_FROM           332  '332'

 L.  84       346  LOAD_FAST                'opt'
              348  LOAD_STR                 '--vv'
              350  COMPARE_OP               ==
          352_354  POP_JUMP_IF_FALSE   362  'to 362'

 L.  84       356  LOAD_CONST               2
              358  STORE_FAST               'verbose'
              360  JUMP_BACK           164  'to 164'
            362_0  COME_FROM           352  '352'

 L.  85       362  LOAD_FAST                'opt'
              364  LOAD_STR                 '--v'
              366  COMPARE_OP               ==
          368_370  POP_JUMP_IF_FALSE   378  'to 378'

 L.  85       372  LOAD_CONST               1
              374  STORE_FAST               'verbose'
              376  JUMP_BACK           164  'to 164'
            378_0  COME_FROM           368  '368'

 L.  86       378  LOAD_FAST                'ErrorExit'
              380  LOAD_STR                 'Illegal option: %s'
              382  LOAD_FAST                'val'
              384  BINARY_MODULO    
              386  CALL_FUNCTION_1       1  ''
              388  POP_TOP          
              390  JUMP_BACK           164  'to 164'

 L.  88       392  LOAD_FAST                'csvdir'
          394_396  POP_JUMP_IF_TRUE    422  'to 422'
              398  LOAD_FAST                'zipdir'
          400_402  POP_JUMP_IF_TRUE    422  'to 422'
              404  LOAD_FAST                'csvfile'
          406_408  POP_JUMP_IF_TRUE    422  'to 422'

 L.  89       410  LOAD_FAST                'ErrorExit'
              412  LOAD_STR                 'csvdir or zipdir or file required\n'
              414  LOAD_FAST                'usage'
              416  BINARY_ADD       
              418  CALL_FUNCTION_1       1  ''
              420  POP_TOP          
            422_0  COME_FROM           406  '406'
            422_1  COME_FROM           400  '400'
            422_2  COME_FROM           394  '394'

 L.  90       422  LOAD_FAST                'ofile'
          424_426  POP_JUMP_IF_TRUE    440  'to 440'

 L.  91       428  LOAD_FAST                'ErrorExit'
              430  LOAD_STR                 'output file required\n'
              432  LOAD_FAST                'usage'
              434  BINARY_ADD       
              436  CALL_FUNCTION_1       1  ''
              438  POP_TOP          
            440_0  COME_FROM           424  '424'

 L.  92       440  LOAD_FAST                'inmolsfile'
          442_444  POP_JUMP_IF_TRUE    458  'to 458'

 L.  93       446  LOAD_FAST                'ErrorExit'
              448  LOAD_STR                 '--inmols file required\n'
              450  LOAD_FAST                'usage'
              452  BINARY_ADD       
              454  CALL_FUNCTION_1       1  ''
              456  POP_TOP          
            458_0  COME_FROM           442  '442'

 L.  95       458  LOAD_GLOBAL              file
              460  LOAD_FAST                'inmolsfile'
              462  CALL_FUNCTION_1       1  ''
              464  STORE_FAST               'finmols'

 L.  96       466  LOAD_FAST                'finmols'
          468_470  POP_JUMP_IF_TRUE    484  'to 484'

 L.  96       472  LOAD_FAST                'ErrorExit'
              474  LOAD_STR                 'cannot open: %s'
              476  LOAD_FAST                'inmolsfile'
              478  BINARY_MODULO    
              480  CALL_FUNCTION_1       1  ''
              482  POP_TOP          
            484_0  COME_FROM           468  '468'

 L.  97       484  LOAD_GLOBAL              file
              486  LOAD_FAST                'ofile'
              488  LOAD_STR                 'w'
              490  CALL_FUNCTION_2       2  ''
              492  STORE_FAST               'fout'

 L.  98       494  LOAD_FAST                'fout'
          496_498  POP_JUMP_IF_TRUE    512  'to 512'

 L.  98       500  LOAD_FAST                'ErrorExit'
              502  LOAD_STR                 'cannot open: %s'
              504  LOAD_FAST                'ofile'
              506  BINARY_MODULO    
              508  CALL_FUNCTION_1       1  ''
              510  POP_TOP          
            512_0  COME_FROM           496  '496'

 L. 100       512  BUILD_LIST_0          0 
              514  STORE_FAST               'aidset'

 L. 101       516  LOAD_FAST                'aids'
          518_520  POP_JUMP_IF_FALSE   574  'to 574'

 L. 102       522  LOAD_GLOBAL              re
              524  LOAD_METHOD              split
              526  LOAD_STR                 '[\\s,]+'
              528  LOAD_FAST                'aids'
              530  CALL_METHOD_2         2  ''
              532  GET_ITER         
              534  FOR_ITER            574  'to 574'
              536  STORE_FAST               'val'

 L. 103       538  LOAD_FAST                'val'
              540  LOAD_METHOD              strip
              542  CALL_METHOD_0         0  ''
          544_546  POP_JUMP_IF_TRUE    552  'to 552'

 L. 103   548_550  JUMP_BACK           534  'to 534'
            552_0  COME_FROM           544  '544'

 L. 104       552  LOAD_FAST                'aidset'
              554  LOAD_METHOD              append
              556  LOAD_GLOBAL              int
              558  LOAD_FAST                'val'
              560  LOAD_METHOD              strip
              562  CALL_METHOD_0         0  ''
              564  CALL_FUNCTION_1       1  ''
              566  CALL_METHOD_1         1  ''
              568  POP_TOP          
          570_572  JUMP_BACK           534  'to 534'
            574_0  COME_FROM           518  '518'

 L. 105       574  LOAD_FAST                'aidfile'
          576_578  POP_JUMP_IF_FALSE   658  'to 658'

 L. 106       580  LOAD_GLOBAL              file
              582  LOAD_FAST                'aidfile'
              584  CALL_FUNCTION_1       1  ''
              586  STORE_FAST               'f'

 L. 107       588  LOAD_FAST                'f'
          590_592  POP_JUMP_IF_TRUE    606  'to 606'

 L. 108       594  LOAD_FAST                'ErrorExit'
              596  LOAD_STR                 'cannot open: %s'
              598  LOAD_FAST                'aidfile'
              600  BINARY_MODULO    
              602  CALL_FUNCTION_1       1  ''
              604  POP_TOP          
            606_0  COME_FROM           590  '590'

 L. 109       606  LOAD_FAST                'f'
              608  LOAD_METHOD              readlines
              610  CALL_METHOD_0         0  ''
              612  STORE_FAST               'lines'

 L. 110       614  LOAD_FAST                'lines'
              616  GET_ITER         
              618  FOR_ITER            658  'to 658'
              620  STORE_FAST               'line'

 L. 111       622  LOAD_FAST                'line'
              624  LOAD_METHOD              strip
              626  CALL_METHOD_0         0  ''
          628_630  POP_JUMP_IF_TRUE    636  'to 636'

 L. 111   632_634  JUMP_BACK           618  'to 618'
            636_0  COME_FROM           628  '628'

 L. 112       636  LOAD_FAST                'aidset'
              638  LOAD_METHOD              append
              640  LOAD_GLOBAL              int
              642  LOAD_FAST                'line'
              644  LOAD_METHOD              strip
              646  CALL_METHOD_0         0  ''
              648  CALL_FUNCTION_1       1  ''
              650  CALL_METHOD_1         1  ''
              652  POP_TOP          
          654_656  JUMP_BACK           618  'to 618'
            658_0  COME_FROM           576  '576'

 L. 113       658  BUILD_MAP_0           0 
              660  STORE_FAST               'cidset'

 L. 114       662  LOAD_FAST                'cidfile'
          664_666  POP_JUMP_IF_FALSE   758  'to 758'

 L. 115       668  LOAD_GLOBAL              file
              670  LOAD_FAST                'cidfile'
              672  CALL_FUNCTION_1       1  ''
              674  STORE_FAST               'f'

 L. 116       676  LOAD_FAST                'f'
          678_680  POP_JUMP_IF_TRUE    694  'to 694'

 L. 117       682  LOAD_FAST                'ErrorExit'
              684  LOAD_STR                 'cannot open: %s'
              686  LOAD_FAST                'cidfile'
              688  BINARY_MODULO    
              690  CALL_FUNCTION_1       1  ''
              692  POP_TOP          
            694_0  COME_FROM           678  '678'

 L. 118       694  LOAD_FAST                'f'
              696  LOAD_METHOD              readlines
              698  CALL_METHOD_0         0  ''
              700  STORE_FAST               'lines'

 L. 119       702  LOAD_FAST                'lines'
              704  GET_ITER         
              706  FOR_ITER            758  'to 758'
              708  STORE_FAST               'line'

 L. 120       710  LOAD_FAST                'line'
              712  LOAD_METHOD              strip
              714  CALL_METHOD_0         0  ''
          716_718  POP_JUMP_IF_TRUE    724  'to 724'

 L. 120   720_722  JUMP_BACK           706  'to 706'
            724_0  COME_FROM           716  '716'

 L. 121       724  LOAD_GLOBAL              re
              726  LOAD_METHOD              sub
              728  LOAD_STR                 '\\s.*$'
              730  LOAD_STR                 ''
              732  LOAD_FAST                'line'
              734  CALL_METHOD_3         3  ''
              736  STORE_FAST               'line'

 L. 122       738  LOAD_CONST               True
              740  LOAD_FAST                'cidset'
              742  LOAD_GLOBAL              int
              744  LOAD_FAST                'line'
              746  LOAD_METHOD              strip
              748  CALL_METHOD_0         0  ''
              750  CALL_FUNCTION_1       1  ''
              752  STORE_SUBSCR     
          754_756  JUMP_BACK           706  'to 706'
            758_0  COME_FROM           664  '664'

 L. 123       758  LOAD_GLOBAL              len
              760  LOAD_FAST                'cidset'
              762  LOAD_METHOD              keys
              764  CALL_METHOD_0         0  ''
              766  CALL_FUNCTION_1       1  ''
              768  LOAD_CONST               0
              770  COMPARE_OP               ==
          772_774  POP_JUMP_IF_FALSE   780  'to 780'

 L. 123       776  LOAD_CONST               None
              778  STORE_FAST               'cidset'
            780_0  COME_FROM           772  '772'

 L. 125       780  BUILD_LIST_0          0 
              782  STORE_FAST               'files'

 L. 126       784  LOAD_FAST                'csvdir'
          786_788  POP_JUMP_IF_FALSE   936  'to 936'

 L. 127       790  LOAD_GLOBAL              os
              792  LOAD_METHOD              listdir
              794  LOAD_FAST                'csvdir'
              796  CALL_METHOD_1         1  ''
              798  GET_ITER         
              800  FOR_ITER            932  'to 932'
              802  STORE_FAST               'fname_csv_gz'

 L. 128       804  LOAD_GLOBAL              re
              806  LOAD_METHOD              search
              808  LOAD_STR                 '\\.csv\\.gz'
              810  LOAD_FAST                'fname_csv_gz'
              812  CALL_METHOD_2         2  ''
          814_816  POP_JUMP_IF_TRUE    822  'to 822'

 L. 128   818_820  JUMP_BACK           800  'to 800'
            822_0  COME_FROM           814  '814'

 L. 129       822  SETUP_FINALLY       846  'to 846'

 L. 130       824  LOAD_GLOBAL              int
              826  LOAD_GLOBAL              re
              828  LOAD_METHOD              sub
              830  LOAD_STR                 '\\.csv\\.gz'
              832  LOAD_STR                 ''
              834  LOAD_FAST                'fname_csv_gz'
              836  CALL_METHOD_3         3  ''
              838  CALL_FUNCTION_1       1  ''
              840  STORE_FAST               'aid'
              842  POP_BLOCK        
              844  JUMP_FORWARD        882  'to 882'
            846_0  COME_FROM_FINALLY   822  '822'

 L. 131       846  POP_TOP          
              848  POP_TOP          
              850  POP_TOP          

 L. 132       852  LOAD_GLOBAL              print
              854  LOAD_GLOBAL              sys
              856  LOAD_ATTR                stderr
              858  BINARY_RSHIFT    
              860  LOAD_STR                 'cannot parse AID: "%s"'
              862  LOAD_FAST                'fname_csv_gz'
              864  BINARY_MODULO    
              866  BUILD_TUPLE_2         2 
              868  POP_TOP          

 L. 133       870  POP_EXCEPT       
          872_874  JUMP_BACK           800  'to 800'
              876  POP_EXCEPT       
              878  JUMP_FORWARD        882  'to 882'
              880  END_FINALLY      
            882_0  COME_FROM           878  '878'
            882_1  COME_FROM           844  '844'

 L. 134       882  LOAD_FAST                'aidset'
          884_886  POP_JUMP_IF_FALSE   902  'to 902'
              888  LOAD_FAST                'aid'
              890  LOAD_FAST                'aidset'
              892  COMPARE_OP               not-in
          894_896  POP_JUMP_IF_FALSE   902  'to 902'

 L. 134   898_900  JUMP_BACK           800  'to 800'
            902_0  COME_FROM           894  '894'
            902_1  COME_FROM           884  '884'

 L. 135       902  LOAD_FAST                'csvdir'
              904  LOAD_STR                 '/'
              906  BINARY_ADD       
              908  LOAD_FAST                'fname_csv_gz'
              910  BINARY_ADD       
              912  STORE_FAST               'fpath_csv_gz'

 L. 136       914  LOAD_FAST                'files'
              916  LOAD_METHOD              append
              918  LOAD_FAST                'fpath_csv_gz'
              920  LOAD_FAST                'aid'
              922  BUILD_TUPLE_2         2 
              924  CALL_METHOD_1         1  ''
              926  POP_TOP          
          928_930  JUMP_BACK           800  'to 800'
          932_934  JUMP_FORWARD       1312  'to 1312'
            936_0  COME_FROM           786  '786'

 L. 137       936  LOAD_FAST                'zipdir'
          938_940  POP_JUMP_IF_FALSE  1242  'to 1242'

 L. 138       942  LOAD_GLOBAL              os
              944  LOAD_METHOD              listdir
              946  LOAD_FAST                'zipdir'
              948  CALL_METHOD_1         1  ''
              950  GET_ITER         
          952_954  FOR_ITER           1240  'to 1240'
              956  STORE_FAST               'fname_zip'

 L. 139       958  LOAD_GLOBAL              re
              960  LOAD_METHOD              search
              962  LOAD_STR                 '\\.zip'
              964  LOAD_FAST                'fname_zip'
              966  CALL_METHOD_2         2  ''
          968_970  POP_JUMP_IF_TRUE    976  'to 976'

 L. 139   972_974  JUMP_BACK           952  'to 952'
            976_0  COME_FROM           968  '968'

 L. 140       976  LOAD_FAST                'zipdir'
              978  LOAD_STR                 '/'
              980  BINARY_ADD       
              982  LOAD_FAST                'fname_zip'
              984  BINARY_ADD       
              986  STORE_FAST               'fpath_zip'

 L. 141       988  SETUP_FINALLY      1006  'to 1006'

 L. 142       990  LOAD_GLOBAL              zipfile
              992  LOAD_METHOD              ZipFile
              994  LOAD_FAST                'fpath_zip'
              996  LOAD_STR                 'r'
              998  CALL_METHOD_2         2  ''
             1000  STORE_FAST               'zf'
             1002  POP_BLOCK        
             1004  JUMP_FORWARD       1042  'to 1042'
           1006_0  COME_FROM_FINALLY   988  '988'

 L. 143      1006  POP_TOP          
             1008  POP_TOP          
             1010  POP_TOP          

 L. 144      1012  LOAD_GLOBAL              print
             1014  LOAD_GLOBAL              sys
             1016  LOAD_ATTR                stderr
             1018  BINARY_RSHIFT    
             1020  LOAD_STR                 'ERROR: cannot read fpath_zip: "%s"'
             1022  LOAD_FAST                'fpath_zip'
             1024  BINARY_MODULO    
             1026  BUILD_TUPLE_2         2 
             1028  POP_TOP          

 L. 145      1030  POP_EXCEPT       
         1032_1034  JUMP_BACK           952  'to 952'
             1036  POP_EXCEPT       
             1038  JUMP_FORWARD       1042  'to 1042'
             1040  END_FINALLY      
           1042_0  COME_FROM          1038  '1038'
           1042_1  COME_FROM          1004  '1004'

 L. 146      1042  LOAD_FAST                'zf'
             1044  LOAD_METHOD              namelist
             1046  CALL_METHOD_0         0  ''
             1048  STORE_FAST               'flist_csv_gz'

 L. 147      1050  LOAD_FAST                'zf'
             1052  LOAD_METHOD              close
             1054  CALL_METHOD_0         0  ''
             1056  POP_TOP          

 L. 148      1058  LOAD_FAST                'flist_csv_gz'
             1060  GET_ITER         
             1062  FOR_ITER           1236  'to 1236'
             1064  STORE_FAST               'fpath_csv_gz'

 L. 149      1066  LOAD_GLOBAL              re
             1068  LOAD_METHOD              search
             1070  LOAD_STR                 '\\.csv\\.gz'
             1072  LOAD_FAST                'fpath_csv_gz'
             1074  CALL_METHOD_2         2  ''
         1076_1078  POP_JUMP_IF_TRUE   1084  'to 1084'

 L. 149  1080_1082  JUMP_BACK          1062  'to 1062'
           1084_0  COME_FROM          1076  '1076'

 L. 150      1084  SETUP_FINALLY      1142  'to 1142'

 L. 151      1086  LOAD_GLOBAL              re
             1088  LOAD_METHOD              search
             1090  LOAD_STR                 '/'
             1092  LOAD_FAST                'fpath_csv_gz'
             1094  CALL_METHOD_2         2  ''
         1096_1098  POP_JUMP_IF_FALSE  1116  'to 1116'

 L. 152      1100  LOAD_GLOBAL              re
             1102  LOAD_METHOD              sub
             1104  LOAD_STR                 '^.*/(\\d*)\\.csv\\.gz'
             1106  LOAD_STR                 '\\1'
             1108  LOAD_FAST                'fpath_csv_gz'
             1110  CALL_METHOD_3         3  ''
             1112  STORE_FAST               'txt'
             1114  JUMP_FORWARD       1130  'to 1130'
           1116_0  COME_FROM          1096  '1096'

 L. 154      1116  LOAD_GLOBAL              re
             1118  LOAD_METHOD              sub
             1120  LOAD_STR                 '\\.csv\\.gz'
             1122  LOAD_STR                 ''
             1124  LOAD_FAST                'fpath_csv_gz'
             1126  CALL_METHOD_3         3  ''
             1128  STORE_FAST               'txt'
           1130_0  COME_FROM          1114  '1114'

 L. 155      1130  LOAD_GLOBAL              int
             1132  LOAD_FAST                'txt'
             1134  CALL_FUNCTION_1       1  ''
             1136  STORE_FAST               'aid'
             1138  POP_BLOCK        
             1140  JUMP_FORWARD       1196  'to 1196'
           1142_0  COME_FROM_FINALLY  1084  '1084'

 L. 156      1142  POP_TOP          
             1144  POP_TOP          
             1146  POP_TOP          

 L. 157      1148  LOAD_GLOBAL              print
             1150  LOAD_GLOBAL              sys
             1152  LOAD_ATTR                stderr
             1154  BINARY_RSHIFT    
             1156  LOAD_STR                 'cannot parse AID: "%s"'
             1158  LOAD_FAST                'fpath_csv_gz'
             1160  BINARY_MODULO    
             1162  BUILD_TUPLE_2         2 
             1164  POP_TOP          

 L. 158      1166  LOAD_GLOBAL              print
             1168  LOAD_GLOBAL              sys
             1170  LOAD_ATTR                stderr
             1172  BINARY_RSHIFT    
             1174  LOAD_STR                 'DEBUG txt: "%s"'
             1176  LOAD_FAST                'txt'
             1178  BINARY_MODULO    
             1180  BUILD_TUPLE_2         2 
             1182  POP_TOP          

 L. 159      1184  POP_EXCEPT       
         1186_1188  JUMP_BACK          1062  'to 1062'
             1190  POP_EXCEPT       
             1192  JUMP_FORWARD       1196  'to 1196'
             1194  END_FINALLY      
           1196_0  COME_FROM          1192  '1192'
           1196_1  COME_FROM          1140  '1140'

 L. 160      1196  LOAD_FAST                'aidset'
         1198_1200  POP_JUMP_IF_FALSE  1216  'to 1216'
             1202  LOAD_FAST                'aid'
             1204  LOAD_FAST                'aidset'
             1206  COMPARE_OP               not-in
         1208_1210  POP_JUMP_IF_FALSE  1216  'to 1216'

 L. 160  1212_1214  JUMP_BACK          1062  'to 1062'
           1216_0  COME_FROM          1208  '1208'
           1216_1  COME_FROM          1198  '1198'

 L. 161      1216  LOAD_FAST                'files'
             1218  LOAD_METHOD              append
             1220  LOAD_FAST                'fpath_zip'
             1222  LOAD_FAST                'fpath_csv_gz'
             1224  LOAD_FAST                'aid'
             1226  BUILD_TUPLE_3         3 
             1228  CALL_METHOD_1         1  ''
             1230  POP_TOP          
         1232_1234  JUMP_BACK          1062  'to 1062'
         1236_1238  JUMP_BACK           952  'to 952'
             1240  JUMP_FORWARD       1312  'to 1312'
           1242_0  COME_FROM           938  '938'

 L. 163      1242  SETUP_FINALLY      1274  'to 1274'

 L. 164      1244  LOAD_GLOBAL              int
             1246  LOAD_GLOBAL              re
             1248  LOAD_METHOD              sub
             1250  LOAD_STR                 '\\.csv\\.gz'
             1252  LOAD_STR                 ''
             1254  LOAD_GLOBAL              os
             1256  LOAD_ATTR                path
             1258  LOAD_METHOD              basename
             1260  LOAD_FAST                'csvfile'
             1262  CALL_METHOD_1         1  ''
             1264  CALL_METHOD_3         3  ''
             1266  CALL_FUNCTION_1       1  ''
             1268  STORE_FAST               'aid'
             1270  POP_BLOCK        
             1272  JUMP_FORWARD       1298  'to 1298'
           1274_0  COME_FROM_FINALLY  1242  '1242'

 L. 165      1274  POP_TOP          
             1276  POP_TOP          
             1278  POP_TOP          

 L. 166      1280  LOAD_FAST                'ErrorExit'
             1282  LOAD_STR                 'cannot parse AID: "%s"'
             1284  LOAD_FAST                'csvfile'
             1286  BINARY_MODULO    
             1288  CALL_FUNCTION_1       1  ''
             1290  POP_TOP          
             1292  POP_EXCEPT       
             1294  JUMP_FORWARD       1298  'to 1298'
             1296  END_FINALLY      
           1298_0  COME_FROM          1294  '1294'
           1298_1  COME_FROM          1272  '1272'

 L. 167      1298  LOAD_FAST                'files'
             1300  LOAD_METHOD              append
             1302  LOAD_FAST                'csvfile'
             1304  LOAD_FAST                'aid'
             1306  BUILD_TUPLE_2         2 
             1308  CALL_METHOD_1         1  ''
             1310  POP_TOP          
           1312_0  COME_FROM          1240  '1240'
           1312_1  COME_FROM           932  '932'

 L. 169      1312  LOAD_CONST               0
             1314  STORE_FAST               'n_mols'

 L. 169      1316  BUILD_LIST_0          0 
             1318  STORE_FAST               'cidlist'

 L. 169      1320  BUILD_MAP_0           0 
             1322  STORE_FAST               'cid2smi'

 L. 171      1324  LOAD_FAST                'finmols'
             1326  LOAD_METHOD              readline
             1328  CALL_METHOD_0         0  ''
             1330  STORE_FAST               'line'

 L. 172      1332  LOAD_FAST                'line'
         1334_1336  POP_JUMP_IF_TRUE   1342  'to 1342'

 L. 172  1338_1340  BREAK_LOOP         1442  'to 1442'
           1342_0  COME_FROM          1334  '1334'

 L. 173      1342  LOAD_FAST                'n_mols'
             1344  LOAD_CONST               1
             1346  INPLACE_ADD      
             1348  STORE_FAST               'n_mols'

 L. 174      1350  LOAD_FAST                'line'
             1352  LOAD_METHOD              rstrip
             1354  CALL_METHOD_0         0  ''
             1356  STORE_FAST               'line'

 L. 175      1358  LOAD_FAST                'line'
             1360  LOAD_METHOD              split
             1362  CALL_METHOD_0         0  ''
             1364  STORE_FAST               'fields'

 L. 176      1366  LOAD_GLOBAL              len
             1368  LOAD_FAST                'fields'
             1370  CALL_FUNCTION_1       1  ''
             1372  LOAD_CONST               3
             1374  COMPARE_OP               <
         1376_1378  POP_JUMP_IF_FALSE  1400  'to 1400'

 L. 177      1380  LOAD_GLOBAL              print
             1382  LOAD_GLOBAL              sys
             1384  LOAD_ATTR                stderr
             1386  BINARY_RSHIFT    
             1388  LOAD_STR                 'Aaak! bad line:'
             1390  LOAD_FAST                'line'
             1392  BUILD_TUPLE_3         3 
             1394  POP_TOP          

 L. 178  1396_1398  JUMP_BACK          1324  'to 1324'
           1400_0  COME_FROM          1376  '1376'

 L. 179      1400  LOAD_FAST                'fields'
             1402  LOAD_CONST               0
             1404  BINARY_SUBSCR    
             1406  STORE_FAST               'smiles'

 L. 180      1408  LOAD_GLOBAL              int
             1410  LOAD_FAST                'fields'
             1412  LOAD_CONST               1
             1414  BINARY_SUBSCR    
             1416  CALL_FUNCTION_1       1  ''
             1418  STORE_FAST               'cid'

 L. 181      1420  LOAD_FAST                'cidlist'
             1422  LOAD_METHOD              append
             1424  LOAD_FAST                'cid'
             1426  CALL_METHOD_1         1  ''
             1428  POP_TOP          

 L. 182      1430  LOAD_FAST                'smiles'
             1432  LOAD_FAST                'cid2smi'
             1434  LOAD_FAST                'cid'
             1436  STORE_SUBSCR     
         1438_1440  JUMP_BACK          1324  'to 1324'

 L. 184      1442  LOAD_GLOBAL              print
             1444  LOAD_GLOBAL              sys
             1446  LOAD_ATTR                stderr
             1448  BINARY_RSHIFT    
             1450  LOAD_STR                 'mols read: %d'
             1452  LOAD_FAST                'n_mols'
             1454  BUILD_TUPLE_1         1 
             1456  BINARY_MODULO    
             1458  BUILD_TUPLE_2         2 
             1460  POP_TOP          

 L. 186      1462  LOAD_GLOBAL              os
             1464  LOAD_ATTR                path
             1466  LOAD_METHOD              isdir
             1468  LOAD_GLOBAL              SCRATCHDIR
             1470  CALL_METHOD_1         1  ''
         1472_1474  POP_JUMP_IF_FALSE  1492  'to 1492'
             1476  LOAD_GLOBAL              os
             1478  LOAD_METHOD              access
             1480  LOAD_GLOBAL              SCRATCHDIR
             1482  LOAD_GLOBAL              os
             1484  LOAD_ATTR                W_OK
             1486  CALL_METHOD_2         2  ''
         1488_1490  POP_JUMP_IF_TRUE   1532  'to 1532'
           1492_0  COME_FROM          1472  '1472'

 L. 187      1492  SETUP_FINALLY      1508  'to 1508'

 L. 188      1494  LOAD_GLOBAL              os
             1496  LOAD_METHOD              mkdir
             1498  LOAD_GLOBAL              SCRATCHDIR
             1500  CALL_METHOD_1         1  ''
             1502  POP_TOP          
             1504  POP_BLOCK        
             1506  JUMP_FORWARD       1532  'to 1532'
           1508_0  COME_FROM_FINALLY  1492  '1492'

 L. 189      1508  POP_TOP          
             1510  POP_TOP          
             1512  POP_TOP          

 L. 190      1514  LOAD_FAST                'ErrorExit'
             1516  LOAD_STR                 'SCRATCHDIR does not exist or is not writeable, and cannot be created: "%s"'
             1518  LOAD_GLOBAL              SCRATCHDIR
             1520  BINARY_MODULO    
             1522  CALL_FUNCTION_1       1  ''
             1524  POP_TOP          
             1526  POP_EXCEPT       
             1528  JUMP_FORWARD       1532  'to 1532'
             1530  END_FINALLY      
           1532_0  COME_FROM          1528  '1528'
           1532_1  COME_FROM          1506  '1506'
           1532_2  COME_FROM          1488  '1488'

 L. 197      1532  BUILD_MAP_0           0 
             1534  STORE_FAST               'cids'

 L. 197      1536  BUILD_LIST_0          0 
             1538  STORE_FAST               'cids_active'

 L. 198      1540  LOAD_GLOBAL              enumerate
             1542  LOAD_FAST                'files'
             1544  CALL_FUNCTION_1       1  ''
             1546  GET_ITER         
           1548_0  COME_FROM          1948  '1948'
           1548_1  COME_FROM          1938  '1938'
         1548_1550  FOR_ITER           1980  'to 1980'
             1552  UNPACK_SEQUENCE_2     2 
             1554  STORE_FAST               'i_file'
             1556  STORE_FAST               'f'

 L. 199      1558  LOAD_FAST                'csvdir'
         1560_1562  POP_JUMP_IF_FALSE  1584  'to 1584'

 L. 200      1564  LOAD_FAST                'f'
             1566  UNPACK_SEQUENCE_2     2 
             1568  STORE_FAST               'fpath_csv'
             1570  STORE_FAST               'aid'

 L. 201      1572  LOAD_GLOBAL              gzip
             1574  LOAD_METHOD              open
             1576  LOAD_FAST                'fpath_csv'
             1578  CALL_METHOD_1         1  ''
             1580  STORE_FAST               'f_csv'
             1582  JUMP_FORWARD       1678  'to 1678'
           1584_0  COME_FROM          1560  '1560'

 L. 202      1584  LOAD_FAST                'zipdir'
         1586_1588  POP_JUMP_IF_FALSE  1678  'to 1678'

 L. 203      1590  LOAD_FAST                'f'
             1592  UNPACK_SEQUENCE_3     3 
             1594  STORE_FAST               'fpath_zip'
             1596  STORE_FAST               'fpath_csv_gz'
             1598  STORE_FAST               'aid'

 L. 204      1600  LOAD_GLOBAL              zipfile
             1602  LOAD_METHOD              ZipFile
             1604  LOAD_FAST                'fpath_zip'
             1606  LOAD_STR                 'r'
             1608  CALL_METHOD_2         2  ''
             1610  STORE_FAST               'zf'

 L. 205      1612  LOAD_GLOBAL              os
             1614  LOAD_METHOD              getcwd
             1616  CALL_METHOD_0         0  ''
             1618  STORE_FAST               'cwd'

 L. 206      1620  LOAD_GLOBAL              os
             1622  LOAD_METHOD              chdir
             1624  LOAD_GLOBAL              SCRATCHDIR
             1626  CALL_METHOD_1         1  ''
             1628  POP_TOP          

 L. 207      1630  LOAD_FAST                'zf'
             1632  LOAD_METHOD              extract
             1634  LOAD_FAST                'fpath_csv_gz'
             1636  CALL_METHOD_1         1  ''
             1638  POP_TOP          

 L. 208      1640  LOAD_GLOBAL              os
             1642  LOAD_METHOD              chdir
             1644  LOAD_FAST                'cwd'
             1646  CALL_METHOD_1         1  ''
             1648  POP_TOP          

 L. 209      1650  LOAD_FAST                'zf'
             1652  LOAD_METHOD              close
             1654  CALL_METHOD_0         0  ''
             1656  POP_TOP          

 L. 210      1658  DELETE_FAST              'zf'

 L. 211      1660  LOAD_GLOBAL              gzip
             1662  LOAD_METHOD              open
             1664  LOAD_GLOBAL              SCRATCHDIR
             1666  LOAD_STR                 '/'
             1668  BINARY_ADD       
             1670  LOAD_FAST                'fpath_csv_gz'
             1672  BINARY_ADD       
             1674  CALL_METHOD_1         1  ''
             1676  STORE_FAST               'f_csv'
           1678_0  COME_FROM          1586  '1586'
           1678_1  COME_FROM          1582  '1582'

 L. 213      1678  LOAD_FAST                'f_csv'
             1680  LOAD_METHOD              read
             1682  CALL_METHOD_0         0  ''
             1684  STORE_FAST               'ftxt'

 L. 214      1686  LOAD_FAST                'f_csv'
             1688  LOAD_METHOD              close
             1690  CALL_METHOD_0         0  ''
             1692  POP_TOP          

 L. 215      1694  DELETE_FAST              'f_csv'

 L. 216      1696  LOAD_GLOBAL              hier_scaffolds_assaystats
             1698  LOAD_METHOD              ExtractOutcomes
             1700  LOAD_FAST                'ftxt'
             1702  LOAD_FAST                'cidset'
             1704  LOAD_FAST                'use_sids'
             1706  CALL_METHOD_3         3  ''
             1708  STORE_FAST               'cids_this'

 L. 217      1710  DELETE_FAST              'ftxt'

 L. 218      1712  LOAD_CONST               0
             1714  STORE_FAST               'n_active'

 L. 219      1716  LOAD_FAST                'cids_this'
             1718  LOAD_METHOD              keys
             1720  CALL_METHOD_0         0  ''
             1722  GET_ITER         
           1724_0  COME_FROM          1798  '1798'
             1724  FOR_ITER           1814  'to 1814'
             1726  STORE_FAST               'cid'

 L. 220      1728  LOAD_FAST                'cid2smi'
             1730  LOAD_METHOD              has_key
             1732  LOAD_FAST                'cid'
             1734  CALL_METHOD_1         1  ''
         1736_1738  POP_JUMP_IF_TRUE   1744  'to 1744'

 L. 220  1740_1742  JUMP_BACK          1724  'to 1724'
           1744_0  COME_FROM          1736  '1736'

 L. 221      1744  LOAD_FAST                'cids'
             1746  LOAD_METHOD              has_key
             1748  LOAD_FAST                'cid'
             1750  CALL_METHOD_1         1  ''
         1752_1754  POP_JUMP_IF_TRUE   1764  'to 1764'

 L. 221      1756  BUILD_MAP_0           0 
             1758  LOAD_FAST                'cids'
             1760  LOAD_FAST                'cid'
             1762  STORE_SUBSCR     
           1764_0  COME_FROM          1752  '1752'

 L. 222      1764  LOAD_FAST                'cids_this'
             1766  LOAD_FAST                'cid'
             1768  BINARY_SUBSCR    
             1770  LOAD_STR                 'outcome'
             1772  BINARY_SUBSCR    
             1774  LOAD_FAST                'cids'
             1776  LOAD_FAST                'cid'
             1778  BINARY_SUBSCR    
             1780  LOAD_FAST                'aid'
             1782  STORE_SUBSCR     

 L. 223      1784  LOAD_FAST                'cids'
             1786  LOAD_FAST                'cid'
             1788  BINARY_SUBSCR    
             1790  LOAD_FAST                'aid'
             1792  BINARY_SUBSCR    
             1794  LOAD_CONST               2
             1796  COMPARE_OP               ==
         1798_1800  POP_JUMP_IF_FALSE  1724  'to 1724'

 L. 223      1802  LOAD_FAST                'n_active'
             1804  LOAD_CONST               1
             1806  INPLACE_ADD      
             1808  STORE_FAST               'n_active'
         1810_1812  JUMP_BACK          1724  'to 1724'

 L. 224      1814  LOAD_FAST                'verbose'
         1816_1818  POP_JUMP_IF_FALSE  1916  'to 1916'

 L. 225      1820  LOAD_GLOBAL              sys
             1822  LOAD_ATTR                stderr
             1824  LOAD_METHOD              write
             1826  LOAD_STR                 '%3d. AID %4d: '
             1828  LOAD_FAST                'i_file'
             1830  LOAD_FAST                'aid'
             1832  BUILD_TUPLE_2         2 
             1834  BINARY_MODULO    
             1836  CALL_METHOD_1         1  ''
             1838  POP_TOP          

 L. 226      1840  LOAD_GLOBAL              sys
             1842  LOAD_ATTR                stderr
             1844  LOAD_METHOD              write
             1846  LOAD_STR                 'active/total: %6d /%6d\n'
             1848  LOAD_FAST                'n_active'
             1850  LOAD_GLOBAL              len
             1852  LOAD_FAST                'cids_this'
             1854  LOAD_METHOD              keys
             1856  CALL_METHOD_0         0  ''
             1858  CALL_FUNCTION_1       1  ''
             1860  BUILD_TUPLE_2         2 
             1862  BINARY_MODULO    
             1864  CALL_METHOD_1         1  ''
             1866  POP_TOP          

 L. 227      1868  LOAD_FAST                'i_file'
             1870  LOAD_CONST               10
             1872  BINARY_MODULO    
         1874_1876  POP_JUMP_IF_TRUE   1916  'to 1916'

 L. 228      1878  LOAD_GLOBAL              sys
             1880  LOAD_ATTR                stderr
             1882  LOAD_METHOD              write
             1884  LOAD_STR                 'done %3d / %3d (%.1f%%)'
             1886  LOAD_FAST                'i_file'
             1888  LOAD_GLOBAL              len
             1890  LOAD_FAST                'files'
             1892  CALL_FUNCTION_1       1  ''
             1894  LOAD_CONST               100.0
             1896  LOAD_FAST                'i_file'
             1898  BINARY_MULTIPLY  
             1900  LOAD_GLOBAL              len
             1902  LOAD_FAST                'files'
             1904  CALL_FUNCTION_1       1  ''
             1906  BINARY_TRUE_DIVIDE
             1908  BUILD_TUPLE_3         3 
             1910  BINARY_MODULO    
             1912  CALL_METHOD_1         1  ''
             1914  POP_TOP          
           1916_0  COME_FROM          1874  '1874'
           1916_1  COME_FROM          1816  '1816'

 L. 229      1916  DELETE_FAST              'cids_this'

 L. 231      1918  LOAD_GLOBAL              os
             1920  LOAD_METHOD              unlink
             1922  LOAD_GLOBAL              SCRATCHDIR
             1924  LOAD_STR                 '/'
             1926  BINARY_ADD       
             1928  LOAD_FAST                'fpath_csv_gz'
             1930  BINARY_ADD       
             1932  CALL_METHOD_1         1  ''
             1934  POP_TOP          

 L. 234      1936  LOAD_FAST                'n_max_aids'
         1938_1940  POP_JUMP_IF_FALSE  1548  'to 1548'
             1942  LOAD_FAST                'i_file'
             1944  LOAD_FAST                'n_max_aids'
             1946  COMPARE_OP               ==
         1948_1950  POP_JUMP_IF_FALSE  1548  'to 1548'

 L. 235      1952  LOAD_GLOBAL              print
             1954  LOAD_GLOBAL              sys
             1956  LOAD_ATTR                stderr
             1958  BINARY_RSHIFT    
             1960  LOAD_STR                 'n_max_aids limit reached: %d'
             1962  LOAD_FAST                'n_max_aids'
             1964  BINARY_MODULO    
             1966  BUILD_TUPLE_2         2 
             1968  POP_TOP          

 L. 236      1970  POP_TOP          
         1972_1974  BREAK_LOOP         1980  'to 1980'
         1976_1978  JUMP_BACK          1548  'to 1548'

 L. 238      1980  LOAD_GLOBAL              print
             1982  LOAD_GLOBAL              sys
             1984  LOAD_ATTR                stderr
             1986  BINARY_RSHIFT    
             1988  LOAD_STR                 'assay files read: %d'
             1990  LOAD_FAST                'i_file'
             1992  BINARY_MODULO    
             1994  BUILD_TUPLE_2         2 
             1996  POP_TOP          

 L. 240      1998  LOAD_CONST               0
             2000  STORE_FAST               'n_cid_notfound'

 L. 241      2002  LOAD_FAST                'fout'
             2004  LOAD_METHOD              write
             2006  LOAD_STR                 '#smiles cid aTested aActive sTested sActive\n'
             2008  CALL_METHOD_1         1  ''
             2010  POP_TOP          

 L. 243      2012  LOAD_FAST                'cidlist'
             2014  GET_ITER         
           2016_0  COME_FROM          2220  '2220'
             2016  FOR_ITER           2262  'to 2262'
             2018  STORE_FAST               'cid'

 L. 244      2020  BUILD_LIST_0          0 
             2022  STORE_FAST               'aids_tested'

 L. 244      2024  BUILD_LIST_0          0 
             2026  STORE_FAST               'aids_active'

 L. 245      2028  LOAD_CONST               0
             2030  STORE_FAST               'n_samples'

 L. 245      2032  LOAD_CONST               0
             2034  STORE_FAST               'n_samples_active'

 L. 246      2036  LOAD_FAST                'cid2smi'
             2038  LOAD_FAST                'cid'
             2040  BINARY_SUBSCR    
             2042  STORE_FAST               'smiles'

 L. 248      2044  LOAD_FAST                'cids'
             2046  LOAD_METHOD              has_key
             2048  LOAD_FAST                'cid'
             2050  CALL_METHOD_1         1  ''
         2052_2054  POP_JUMP_IF_TRUE   2086  'to 2086'

 L. 249      2056  LOAD_GLOBAL              print
             2058  LOAD_GLOBAL              sys
             2060  LOAD_ATTR                stderr
             2062  BINARY_RSHIFT    
             2064  LOAD_STR                 'NOTE: cannot find cid %d in any assay.'
             2066  LOAD_FAST                'cid'
             2068  BINARY_MODULO    
             2070  BUILD_TUPLE_2         2 
             2072  POP_TOP          

 L. 250      2074  LOAD_FAST                'n_cid_notfound'
             2076  LOAD_CONST               1
             2078  INPLACE_ADD      
             2080  STORE_FAST               'n_cid_notfound'

 L. 251  2082_2084  JUMP_BACK          2016  'to 2016'
           2086_0  COME_FROM          2052  '2052'

 L. 253      2086  LOAD_FAST                'cids'
             2088  LOAD_FAST                'cid'
             2090  BINARY_SUBSCR    
             2092  LOAD_METHOD              keys
             2094  CALL_METHOD_0         0  ''
             2096  GET_ITER         
           2098_0  COME_FROM          2162  '2162'
           2098_1  COME_FROM          2144  '2144'
             2098  FOR_ITER           2180  'to 2180'
             2100  STORE_FAST               'aid'

 L. 254      2102  LOAD_FAST                'aid'
             2104  LOAD_FAST                'aids_tested'
             2106  COMPARE_OP               not-in
         2108_2110  POP_JUMP_IF_FALSE  2122  'to 2122'

 L. 254      2112  LOAD_FAST                'aids_tested'
             2114  LOAD_METHOD              append
             2116  LOAD_FAST                'aid'
             2118  CALL_METHOD_1         1  ''
             2120  POP_TOP          
           2122_0  COME_FROM          2108  '2108'

 L. 255      2122  LOAD_FAST                'n_samples'
             2124  LOAD_CONST               1
             2126  INPLACE_ADD      
             2128  STORE_FAST               'n_samples'

 L. 256      2130  LOAD_FAST                'cids'
             2132  LOAD_FAST                'cid'
             2134  BINARY_SUBSCR    
             2136  LOAD_FAST                'aid'
             2138  BINARY_SUBSCR    
             2140  LOAD_CONST               2
             2142  COMPARE_OP               ==
         2144_2146  POP_JUMP_IF_FALSE  2098  'to 2098'

 L. 257      2148  LOAD_FAST                'n_samples_active'
             2150  LOAD_CONST               1
             2152  INPLACE_ADD      
             2154  STORE_FAST               'n_samples_active'

 L. 258      2156  LOAD_FAST                'aid'
             2158  LOAD_FAST                'aids_active'
             2160  COMPARE_OP               not-in
         2162_2164  POP_JUMP_IF_FALSE  2098  'to 2098'

 L. 258      2166  LOAD_FAST                'aids_active'
             2168  LOAD_METHOD              append
             2170  LOAD_FAST                'aid'
             2172  CALL_METHOD_1         1  ''
             2174  POP_TOP          
         2176_2178  JUMP_BACK          2098  'to 2098'

 L. 260      2180  LOAD_FAST                'fout'
             2182  LOAD_METHOD              write
             2184  LOAD_STR                 '%s %d %d %d %d %d\n'

 L. 261      2186  LOAD_FAST                'smiles'

 L. 262      2188  LOAD_FAST                'cid'

 L. 263      2190  LOAD_GLOBAL              len
             2192  LOAD_FAST                'aids_tested'
             2194  CALL_FUNCTION_1       1  ''

 L. 264      2196  LOAD_GLOBAL              len
             2198  LOAD_FAST                'aids_active'
             2200  CALL_FUNCTION_1       1  ''

 L. 265      2202  LOAD_FAST                'n_samples'

 L. 266      2204  LOAD_FAST                'n_samples_active'

 L. 260      2206  BUILD_TUPLE_6         6 
             2208  BINARY_MODULO    
             2210  CALL_METHOD_1         1  ''
             2212  POP_TOP          

 L. 267      2214  LOAD_FAST                'verbose'
             2216  LOAD_CONST               1
             2218  COMPARE_OP               >
         2220_2222  POP_JUMP_IF_FALSE  2016  'to 2016'

 L. 268      2224  LOAD_GLOBAL              sys
             2226  LOAD_ATTR                stderr
             2228  LOAD_METHOD              write

 L. 269      2230  LOAD_STR                 'cid=%d,aTested=%d,aActive=%d,sTested=%d,sActive%d\n'

 L. 270      2232  LOAD_FAST                'cid'

 L. 271      2234  LOAD_GLOBAL              len
             2236  LOAD_FAST                'aids_tested'
             2238  CALL_FUNCTION_1       1  ''

 L. 272      2240  LOAD_GLOBAL              len
             2242  LOAD_FAST                'aids_active'
             2244  CALL_FUNCTION_1       1  ''

 L. 273      2246  LOAD_FAST                'n_samples'

 L. 274      2248  LOAD_FAST                'n_samples_active'

 L. 269      2250  BUILD_TUPLE_5         5 
             2252  BINARY_MODULO    

 L. 268      2254  CALL_METHOD_1         1  ''
             2256  POP_TOP          
         2258_2260  JUMP_BACK          2016  'to 2016'

 L. 276      2262  LOAD_FAST                'fout'
             2264  LOAD_METHOD              close
             2266  CALL_METHOD_0         0  ''
             2268  POP_TOP          

 L. 278      2270  LOAD_STR                 'CID'
             2272  STORE_FAST               'id'

 L. 279      2274  LOAD_FAST                'use_sids'
         2276_2278  POP_JUMP_IF_FALSE  2284  'to 2284'

 L. 279      2280  LOAD_STR                 'SID'
             2282  STORE_FAST               'id'
           2284_0  COME_FROM          2276  '2276'

 L. 280      2284  LOAD_GLOBAL              print
             2286  LOAD_GLOBAL              sys
             2288  LOAD_ATTR                stderr
             2290  BINARY_RSHIFT    
             2292  LOAD_STR                 '%s: number of assay files: %d'
             2294  LOAD_GLOBAL              PROG
             2296  LOAD_GLOBAL              len
             2298  LOAD_FAST                'files'
             2300  CALL_FUNCTION_1       1  ''
             2302  BUILD_TUPLE_2         2 
             2304  BINARY_MODULO    
             2306  BUILD_TUPLE_2         2 
             2308  POP_TOP          

 L. 281      2310  LOAD_GLOBAL              print
             2312  LOAD_GLOBAL              sys
             2314  LOAD_ATTR                stderr
             2316  BINARY_RSHIFT    
             2318  LOAD_STR                 '%s: total %ss: %d'
             2320  LOAD_GLOBAL              PROG
             2322  LOAD_FAST                'id'
             2324  LOAD_GLOBAL              len
             2326  LOAD_FAST                'cids'
             2328  LOAD_METHOD              keys
             2330  CALL_METHOD_0         0  ''
             2332  CALL_FUNCTION_1       1  ''
             2334  BUILD_TUPLE_3         3 
             2336  BINARY_MODULO    
             2338  BUILD_TUPLE_2         2 
             2340  POP_TOP          

 L. 282      2342  LOAD_GLOBAL              print
             2344  LOAD_GLOBAL              sys
             2346  LOAD_ATTR                stderr
             2348  BINARY_RSHIFT    
             2350  LOAD_STR                 '%s: number of %ss: %d'
             2352  LOAD_GLOBAL              PROG
             2354  LOAD_FAST                'id'
             2356  LOAD_GLOBAL              len
             2358  LOAD_FAST                'cidlist'
             2360  CALL_FUNCTION_1       1  ''
             2362  BUILD_TUPLE_3         3 
             2364  BINARY_MODULO    
             2366  BUILD_TUPLE_2         2 
             2368  POP_TOP          

 L. 283      2370  LOAD_GLOBAL              print
             2372  LOAD_GLOBAL              sys
             2374  LOAD_ATTR                stderr
             2376  BINARY_RSHIFT    
             2378  LOAD_STR                 '%s: number of %ss not found in any assay: %d'
             2380  LOAD_GLOBAL              PROG
             2382  LOAD_FAST                'id'
             2384  LOAD_FAST                'n_cid_notfound'
             2386  BUILD_TUPLE_3         3 
             2388  BINARY_MODULO    
             2390  BUILD_TUPLE_2         2 
             2392  POP_TOP          

Parse error at or near `POP_EXCEPT' instruction at offset 876


if __name__ == '__main__':
    main()