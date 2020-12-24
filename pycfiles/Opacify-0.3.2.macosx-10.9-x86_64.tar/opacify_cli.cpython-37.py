# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/opacify/opacify_cli.py
# Compiled at: 2019-01-25 04:06:00
# Size of source mod 2**32: 6543 bytes
import sys, os, time, argparse
from opacify import Opacify, StatusCodes
from opacify import INFOTXT, EPILOG
if sys.version_info[0] < 3:
    import reddit
else:
    from opacify import reddit

def version():
    return INFOTXT


def dump_messages(o):
    for status in o.results.get():
        for i in range(len(status.codes)):
            code = status.codes[i]
            msg = status.messages[i]
            if code == StatusCodes.OK:
                continue
            print('%s: %s' % (code.name, msg))


def main--- This code section failed: ---

 L.  28         0  LOAD_GLOBAL              argparse
                2  LOAD_ATTR                ArgumentParser

 L.  29         4  LOAD_GLOBAL              INFOTXT

 L.  30         6  LOAD_GLOBAL              argparse
                8  LOAD_ATTR                RawDescriptionHelpFormatter

 L.  31        10  LOAD_GLOBAL              EPILOG
               12  LOAD_CONST               ('description', 'formatter_class', 'epilog')
               14  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               16  STORE_FAST               'parser'

 L.  33        18  LOAD_FAST                'parser'
               20  LOAD_ATTR                add_subparsers
               22  LOAD_STR                 'func'
               24  LOAD_CONST               ('dest',)
               26  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               28  STORE_FAST               'subparser'

 L.  34        30  LOAD_GLOBAL              sys
               32  LOAD_ATTR                version_info
               34  LOAD_CONST               0
               36  BINARY_SUBSCR    
               38  LOAD_CONST               3
               40  COMPARE_OP               <
               42  POP_JUMP_IF_FALSE    50  'to 50'

 L.  35        44  LOAD_CONST               True
               46  LOAD_FAST                'subparser'
               48  STORE_ATTR               required
             50_0  COME_FROM            42  '42'

 L.  36        50  LOAD_FAST                'subparser'
               52  LOAD_ATTR                add_parser
               54  LOAD_STR                 'pacify'
               56  LOAD_STR                 'Run in pacify mode (builds manifest from input file)'

 L.  37        58  LOAD_STR                 'Run in pacify mode (builds manifest from input file)'
               60  LOAD_CONST               ('description', 'help')
               62  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               64  STORE_FAST               'group1'

 L.  38        66  LOAD_FAST                'subparser'
               68  LOAD_ATTR                add_parser
               70  LOAD_STR                 'satisfy'
               72  LOAD_STR                 'Run in satisfy mode (rebuilds file using manifest)'

 L.  39        74  LOAD_STR                 'Run in satisfy mode (extracts file using manifest)'
               76  LOAD_CONST               ('description', 'help')
               78  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               80  STORE_FAST               'group2'

 L.  40        82  LOAD_FAST                'subparser'
               84  LOAD_ATTR                add_parser
               86  LOAD_STR                 'verify'
               88  LOAD_STR                 'Validate manifest URLs and response length'

 L.  41        90  LOAD_STR                 'Validate manifest URLs and response length'
               92  LOAD_CONST               ('description', 'help')
               94  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               96  STORE_FAST               'group3'

 L.  42        98  LOAD_FAST                'subparser'
              100  LOAD_ATTR                add_parser
              102  LOAD_STR                 'reddit'
              104  LOAD_STR                 'Auto-generate a urls file from reddit links'

 L.  43       106  LOAD_STR                 'Auto-generate a urls file from reddit links'
              108  LOAD_CONST               ('description', 'help')
              110  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              112  STORE_FAST               'group4'

 L.  45       114  LOAD_FAST                'group4'
              116  LOAD_ATTR                add_argument
              118  LOAD_STR                 '-o'
              120  LOAD_STR                 '--out'
              122  LOAD_CONST               True
              124  LOAD_STR                 'Path to write urls to'
              126  LOAD_CONST               ('required', 'help')
              128  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              130  POP_TOP          

 L.  46       132  LOAD_FAST                'group4'
              134  LOAD_ATTR                add_argument
              136  LOAD_STR                 '-c'
              138  LOAD_STR                 '--count'
              140  LOAD_CONST               True
              142  LOAD_STR                 'How many links to get'
              144  LOAD_CONST               ('required', 'help')
              146  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              148  POP_TOP          

 L.  47       150  LOAD_FAST                'group1'
              152  LOAD_ATTR                add_argument
              154  LOAD_STR                 '-i'
              156  LOAD_STR                 '--input'
              158  LOAD_CONST               True
              160  LOAD_STR                 'Path to input file'
              162  LOAD_CONST               ('required', 'help')
              164  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              166  POP_TOP          

 L.  48       168  LOAD_FAST                'group1'
              170  LOAD_ATTR                add_argument
              172  LOAD_STR                 '-u'
              174  LOAD_STR                 '--urls'
              176  LOAD_CONST               True
              178  LOAD_STR                 'Path to urls file'
              180  LOAD_CONST               ('required', 'help')
              182  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              184  POP_TOP          

 L.  49       186  LOAD_FAST                'group1'
              188  LOAD_ATTR                add_argument
              190  LOAD_STR                 '-m'
              192  LOAD_STR                 '--manifest'
              194  LOAD_CONST               True
              196  LOAD_STR                 'Output path of manifest file'
              198  LOAD_CONST               ('required', 'help')
              200  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              202  POP_TOP          

 L.  50       204  LOAD_FAST                'group1'
              206  LOAD_ATTR                add_argument
              208  LOAD_STR                 '-c'
              210  LOAD_STR                 '--cache'
              212  LOAD_CONST               True
              214  LOAD_STR                 'Path to cache directory'
              216  LOAD_CONST               ('required', 'help')
              218  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              220  POP_TOP          

 L.  51       222  LOAD_FAST                'group1'
              224  LOAD_ATTR                add_argument
              226  LOAD_STR                 '-k'
              228  LOAD_STR                 '--keep'
              230  LOAD_STR                 'store_const'
              232  LOAD_CONST               True

 L.  52       234  LOAD_STR                 'Do not remove cache after completed. Useful for testing'
              236  LOAD_CONST               ('action', 'const', 'help')
              238  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              240  POP_TOP          

 L.  53       242  LOAD_FAST                'group1'
              244  LOAD_ATTR                add_argument
              246  LOAD_STR                 '-f'
              248  LOAD_STR                 '--force'
              250  LOAD_STR                 'store_const'
              252  LOAD_CONST               True
              254  LOAD_STR                 'Overwrite manifest if it exists'
              256  LOAD_CONST               ('action', 'const', 'help')
              258  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              260  POP_TOP          

 L.  54       262  LOAD_FAST                'group1'
              264  LOAD_ATTR                add_argument
              266  LOAD_STR                 '-d'
              268  LOAD_STR                 '--debug'
              270  LOAD_STR                 'store_const'
              272  LOAD_CONST               True
              274  LOAD_STR                 'Turn on debug output'
              276  LOAD_CONST               ('action', 'const', 'help')
              278  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              280  POP_TOP          

 L.  55       282  LOAD_FAST                'group1'
              284  LOAD_ATTR                add_argument
              286  LOAD_STR                 '-t'
              288  LOAD_STR                 '--threads'
              290  LOAD_STR                 'Run processing multiple threads'
              292  LOAD_CONST               ('help',)
              294  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              296  POP_TOP          

 L.  56       298  LOAD_FAST                'group1'
              300  LOAD_ATTR                add_argument
              302  LOAD_STR                 '-s'
              304  LOAD_STR                 '--chunksize'
              306  LOAD_STR                 'Specify a different chunk size (default is 1 byte)'
              308  LOAD_CONST               ('help',)
              310  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              312  POP_TOP          

 L.  58       314  LOAD_FAST                'group2'
              316  LOAD_ATTR                add_argument
              318  LOAD_STR                 '-m'
              320  LOAD_STR                 '--manifest'
              322  LOAD_CONST               True
              324  LOAD_STR                 'Path of manifest file'
              326  LOAD_CONST               ('required', 'help')
              328  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              330  POP_TOP          

 L.  59       332  LOAD_FAST                'group2'
              334  LOAD_ATTR                add_argument
              336  LOAD_STR                 '-o'
              338  LOAD_STR                 '--out'
              340  LOAD_CONST               True
              342  LOAD_STR                 'Path to write output file to'
              344  LOAD_CONST               ('required', 'help')
              346  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              348  POP_TOP          

 L.  60       350  LOAD_FAST                'group2'
              352  LOAD_ATTR                add_argument
              354  LOAD_STR                 '-c'
              356  LOAD_STR                 '--cache'
              358  LOAD_CONST               True
              360  LOAD_STR                 'Path to cache directory'
              362  LOAD_CONST               ('required', 'help')
              364  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              366  POP_TOP          

 L.  61       368  LOAD_FAST                'group2'
              370  LOAD_ATTR                add_argument
              372  LOAD_STR                 '-k'
              374  LOAD_STR                 '--keep'
              376  LOAD_STR                 'store_const'
              378  LOAD_CONST               True

 L.  62       380  LOAD_STR                 'Do not remove cache after completed. Useful for testing'
              382  LOAD_CONST               ('action', 'const', 'help')
              384  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              386  POP_TOP          

 L.  63       388  LOAD_FAST                'group2'
              390  LOAD_ATTR                add_argument
              392  LOAD_STR                 '-f'
              394  LOAD_STR                 '--force'
              396  LOAD_STR                 'store_const'
              398  LOAD_CONST               True
              400  LOAD_STR                 'Overwrite output file if it exists'
              402  LOAD_CONST               False
              404  LOAD_CONST               ('action', 'const', 'help', 'default')
              406  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
              408  POP_TOP          

 L.  64       410  LOAD_FAST                'group2'
              412  LOAD_ATTR                add_argument
              414  LOAD_STR                 '-d'
              416  LOAD_STR                 '--debug'
              418  LOAD_STR                 'store_const'
              420  LOAD_CONST               True
              422  LOAD_STR                 'Turn on debug output'
              424  LOAD_CONST               ('action', 'const', 'help')
              426  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              428  POP_TOP          

 L.  65       430  LOAD_FAST                'group3'
              432  LOAD_ATTR                add_argument
              434  LOAD_STR                 '-m'
              436  LOAD_STR                 '--manifest'
              438  LOAD_CONST               True
              440  LOAD_STR                 'Path of manifest file'
              442  LOAD_CONST               ('required', 'help')
              444  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              446  POP_TOP          

 L.  66       448  LOAD_FAST                'group3'
              450  LOAD_ATTR                add_argument
              452  LOAD_STR                 '-d'
              454  LOAD_STR                 '--debug'
              456  LOAD_STR                 'store_const'
              458  LOAD_CONST               True
              460  LOAD_STR                 'Turn on debug output'
              462  LOAD_CONST               ('action', 'const', 'help')
              464  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              466  POP_TOP          

 L.  67       468  LOAD_FAST                'parser'
              470  LOAD_ATTR                add_argument
              472  LOAD_STR                 '-V'
              474  LOAD_STR                 '--version'
              476  LOAD_STR                 'Display Opacify version info'

 L.  68       478  LOAD_STR                 'version'
              480  LOAD_GLOBAL              version
              482  CALL_FUNCTION_0       0  '0 positional arguments'
              484  LOAD_CONST               ('help', 'action', 'version')
              486  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              488  POP_TOP          

 L.  69       490  LOAD_FAST                'parser'
              492  LOAD_METHOD              parse_args
              494  CALL_METHOD_0         0  '0 positional arguments'
              496  STORE_FAST               'args'

 L.  70       498  LOAD_STR                 'cache'
              500  STORE_FAST               'cache'

 L.  71       502  LOAD_FAST                'args'
              504  LOAD_ATTR                func
              506  LOAD_CONST               ('pacify', 'satisfy')
              508  COMPARE_OP               in
          510_512  POP_JUMP_IF_FALSE   528  'to 528'

 L.  72       514  LOAD_FAST                'args'
              516  LOAD_ATTR                cache
          518_520  POP_JUMP_IF_FALSE   528  'to 528'

 L.  73       522  LOAD_FAST                'args'
              524  LOAD_ATTR                cache
              526  STORE_FAST               'cache'
            528_0  COME_FROM           518  '518'
            528_1  COME_FROM           510  '510'

 L.  74       528  LOAD_GLOBAL              time
              530  LOAD_METHOD              time
              532  CALL_METHOD_0         0  '0 positional arguments'
              534  STORE_FAST               'start_timer'

 L.  75       536  LOAD_GLOBAL              getattr
              538  LOAD_FAST                'args'
              540  LOAD_STR                 'debug'
              542  LOAD_CONST               False
              544  CALL_FUNCTION_3       3  '3 positional arguments'
              546  STORE_FAST               'debug'

 L.  76       548  LOAD_GLOBAL              getattr
              550  LOAD_FAST                'args'
              552  LOAD_STR                 'threads'
              554  LOAD_CONST               None
              556  CALL_FUNCTION_3       3  '3 positional arguments'
              558  STORE_FAST               'n_threads'

 L.  77       560  LOAD_GLOBAL              Opacify
              562  LOAD_FAST                'cache'
              564  LOAD_FAST                'debug'
              566  LOAD_CONST               ('cache_dir', 'debug')
              568  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              570  STORE_FAST               'o'

 L.  78       572  LOAD_CONST               None
              574  STORE_FAST               'r'

 L.  79       576  LOAD_FAST                'args'
              578  LOAD_ATTR                func
              580  LOAD_STR                 'pacify'
              582  COMPARE_OP               ==
          584_586  POP_JUMP_IF_FALSE   828  'to 828'

 L.  80       588  LOAD_FAST                'args'
              590  LOAD_ATTR                chunksize
          592_594  POP_JUMP_IF_FALSE   608  'to 608'

 L.  81       596  LOAD_GLOBAL              int
              598  LOAD_FAST                'args'
              600  LOAD_ATTR                chunksize
              602  CALL_FUNCTION_1       1  '1 positional argument'
              604  LOAD_FAST                'o'
              606  STORE_ATTR               chunk_size
            608_0  COME_FROM           592  '592'

 L.  82       608  LOAD_FAST                'o'
              610  LOAD_ATTR                pacify

 L.  83       612  LOAD_FAST                'args'
              614  LOAD_ATTR                input

 L.  84       616  LOAD_FAST                'args'
              618  LOAD_ATTR                urls

 L.  85       620  LOAD_FAST                'args'
              622  LOAD_ATTR                manifest

 L.  86       624  LOAD_FAST                'args'
              626  LOAD_ATTR                force

 L.  87       628  LOAD_FAST                'args'
              630  LOAD_ATTR                keep

 L.  88       632  LOAD_FAST                'n_threads'
              634  LOAD_CONST               ('input_file', 'url_file', 'manifest', 'overwrite', 'keep_cache', 'threads')
              636  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
              638  STORE_FAST               'r'

 L.  90       640  LOAD_GLOBAL              print
              642  LOAD_STR                 '\n'
              644  CALL_FUNCTION_1       1  '1 positional argument'
              646  POP_TOP          

 L.  91       648  LOAD_GLOBAL              time
              650  LOAD_METHOD              time
              652  CALL_METHOD_0         0  '0 positional arguments'
              654  STORE_FAST               'end_timer'

 L.  92       656  LOAD_FAST                'o'
              658  LOAD_ATTR                total_chunk_size
              660  LOAD_CONST               1
              662  BINARY_ADD       
              664  LOAD_GLOBAL              float
              666  LOAD_FAST                'o'
              668  LOAD_ATTR                total_chunks
              670  LOAD_CONST               1
              672  BINARY_ADD       
              674  CALL_FUNCTION_1       1  '1 positional argument'
              676  BINARY_TRUE_DIVIDE
              678  STORE_FAST               'avg_chunk_size'

 L.  94       680  LOAD_FAST                'r'
              682  LOAD_GLOBAL              StatusCodes
              684  LOAD_ATTR                OK
              686  COMPARE_OP               !=
          688_690  POP_JUMP_IF_FALSE   710  'to 710'

 L.  95       692  LOAD_GLOBAL              print
              694  LOAD_STR                 'ERROR: Failed to pacify:'
              696  CALL_FUNCTION_1       1  '1 positional argument'
              698  POP_TOP          

 L.  96       700  LOAD_GLOBAL              dump_messages
              702  LOAD_FAST                'o'
              704  CALL_FUNCTION_1       1  '1 positional argument'
              706  POP_TOP          
              708  JUMP_FORWARD       1192  'to 1192'
            710_0  COME_FROM           688  '688'

 L.  98       710  LOAD_GLOBAL              print
              712  LOAD_STR                 'Wrote manifest to: %s'
              714  LOAD_FAST                'args'
              716  LOAD_ATTR                manifest
              718  BINARY_MODULO    
              720  CALL_FUNCTION_1       1  '1 positional argument'
              722  POP_TOP          

 L.  99       724  LOAD_GLOBAL              print
              726  LOAD_STR                 '   Avg chunk size: %.2f'
              728  LOAD_FAST                'avg_chunk_size'
              730  BINARY_MODULO    
              732  CALL_FUNCTION_1       1  '1 positional argument'
              734  POP_TOP          

 L. 100       736  LOAD_GLOBAL              print
              738  LOAD_STR                 '     Total chunks: %s'
              740  LOAD_FAST                'o'
              742  LOAD_ATTR                total_chunks
              744  BINARY_MODULO    
              746  CALL_FUNCTION_1       1  '1 positional argument'
              748  POP_TOP          

 L. 101       750  LOAD_GLOBAL              print
              752  LOAD_STR                 '    Manifest size: %s'
              754  LOAD_GLOBAL              os
              756  LOAD_ATTR                path
              758  LOAD_METHOD              getsize
              760  LOAD_FAST                'args'
              762  LOAD_ATTR                manifest
              764  CALL_METHOD_1         1  '1 positional argument'
              766  BINARY_MODULO    
              768  CALL_FUNCTION_1       1  '1 positional argument'
              770  POP_TOP          

 L. 104       772  LOAD_GLOBAL              print
              774  LOAD_STR                 '    Original size: %s'
              776  LOAD_FAST                'o'
              778  LOAD_ATTR                clength
              780  BINARY_MODULO    
              782  CALL_FUNCTION_1       1  '1 positional argument'
              784  POP_TOP          

 L. 105       786  LOAD_GLOBAL              print
              788  LOAD_STR                 '           sha256: %s...'
              790  LOAD_FAST                'o'
              792  LOAD_ATTR                digest
              794  LOAD_CONST               None
              796  LOAD_CONST               16
              798  BUILD_SLICE_2         2 
              800  BINARY_SUBSCR    
              802  BINARY_MODULO    
              804  CALL_FUNCTION_1       1  '1 positional argument'
              806  POP_TOP          

 L. 106       808  LOAD_GLOBAL              print
              810  LOAD_STR                 '         Duration: %.3fs'
              812  LOAD_FAST                'end_timer'
              814  LOAD_FAST                'start_timer'
              816  BINARY_SUBTRACT  
              818  BINARY_MODULO    
              820  CALL_FUNCTION_1       1  '1 positional argument'
              822  POP_TOP          
          824_826  JUMP_FORWARD       1192  'to 1192'
            828_0  COME_FROM           584  '584'

 L. 107       828  LOAD_FAST                'args'
              830  LOAD_ATTR                func
              832  LOAD_STR                 'satisfy'
              834  COMPARE_OP               ==
          836_838  POP_JUMP_IF_FALSE   988  'to 988'

 L. 108       840  LOAD_FAST                'o'
              842  LOAD_ATTR                satisfy
              844  LOAD_FAST                'args'
              846  LOAD_ATTR                manifest
              848  LOAD_FAST                'args'
              850  LOAD_ATTR                out
              852  LOAD_FAST                'args'
              854  LOAD_ATTR                keep
              856  LOAD_FAST                'args'
              858  LOAD_ATTR                force
              860  LOAD_CONST               ('manifest', 'out_file', 'keep_cache', 'overwrite')
              862  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              864  STORE_FAST               'r'

 L. 109       866  LOAD_GLOBAL              print
              868  LOAD_STR                 '\n'
              870  CALL_FUNCTION_1       1  '1 positional argument'
              872  POP_TOP          

 L. 111       874  LOAD_FAST                'r'
              876  LOAD_GLOBAL              StatusCodes
              878  LOAD_ATTR                OK
              880  COMPARE_OP               !=
          882_884  POP_JUMP_IF_FALSE   904  'to 904'

 L. 112       886  LOAD_GLOBAL              print
              888  LOAD_STR                 'ERROR: Failed to satisfy:'
              890  CALL_FUNCTION_1       1  '1 positional argument'
              892  POP_TOP          

 L. 113       894  LOAD_GLOBAL              dump_messages
              896  LOAD_FAST                'o'
              898  CALL_FUNCTION_1       1  '1 positional argument'
              900  POP_TOP          
              902  JUMP_FORWARD        986  'to 986'
            904_0  COME_FROM           882  '882'

 L. 115       904  LOAD_GLOBAL              time
              906  LOAD_METHOD              time
              908  CALL_METHOD_0         0  '0 positional arguments'
              910  STORE_FAST               'end_timer'

 L. 116       912  LOAD_GLOBAL              print
              914  LOAD_STR                 '    Manifest size: %s'
              916  LOAD_GLOBAL              os
              918  LOAD_ATTR                path
              920  LOAD_METHOD              getsize
              922  LOAD_FAST                'args'
              924  LOAD_ATTR                manifest
              926  CALL_METHOD_1         1  '1 positional argument'
              928  BINARY_MODULO    
              930  CALL_FUNCTION_1       1  '1 positional argument'
              932  POP_TOP          

 L. 117       934  LOAD_GLOBAL              print
              936  LOAD_STR                 '      Output size: %s'
              938  LOAD_FAST                'o'
              940  LOAD_ATTR                clength
              942  BINARY_MODULO    
              944  CALL_FUNCTION_1       1  '1 positional argument'
              946  POP_TOP          

 L. 118       948  LOAD_GLOBAL              print
              950  LOAD_STR                 '           sha256: %s...'
              952  LOAD_FAST                'o'
              954  LOAD_ATTR                digest
              956  LOAD_CONST               None
              958  LOAD_CONST               16
              960  BUILD_SLICE_2         2 
              962  BINARY_SUBSCR    
              964  BINARY_MODULO    
              966  CALL_FUNCTION_1       1  '1 positional argument'
              968  POP_TOP          

 L. 119       970  LOAD_GLOBAL              print
              972  LOAD_STR                 '         Duration: %.3fs'
              974  LOAD_FAST                'end_timer'
              976  LOAD_FAST                'start_timer'
              978  BINARY_SUBTRACT  
              980  BINARY_MODULO    
              982  CALL_FUNCTION_1       1  '1 positional argument'
              984  POP_TOP          
            986_0  COME_FROM           902  '902'
              986  JUMP_FORWARD       1192  'to 1192'
            988_0  COME_FROM           836  '836'

 L. 120       988  LOAD_FAST                'args'
              990  LOAD_ATTR                func
              992  LOAD_STR                 'reddit'
              994  COMPARE_OP               ==
          996_998  POP_JUMP_IF_FALSE  1134  'to 1134'

 L. 121      1000  LOAD_GLOBAL              print
             1002  LOAD_STR                 'Generating urls from reddit data...'
             1004  CALL_FUNCTION_1       1  '1 positional argument'
             1006  POP_TOP          

 L. 122      1008  LOAD_STR                 'w'
             1010  STORE_FAST               'mode'

 L. 123      1012  LOAD_GLOBAL              os
             1014  LOAD_ATTR                path
             1016  LOAD_METHOD              exists
             1018  LOAD_FAST                'args'
             1020  LOAD_ATTR                out
             1022  CALL_METHOD_1         1  '1 positional argument'
         1024_1026  POP_JUMP_IF_FALSE  1046  'to 1046'

 L. 124      1028  LOAD_GLOBAL              print
             1030  LOAD_STR                 'NOTE: %s exists. Appending to file.'
             1032  LOAD_FAST                'args'
             1034  LOAD_ATTR                out
             1036  BINARY_MODULO    
             1038  CALL_FUNCTION_1       1  '1 positional argument'
             1040  POP_TOP          

 L. 125      1042  LOAD_STR                 'a'
             1044  STORE_FAST               'mode'
           1046_0  COME_FROM          1024  '1024'

 L. 126      1046  LOAD_GLOBAL              reddit
             1048  LOAD_ATTR                reddit_get_links
             1050  LOAD_FAST                'args'
             1052  LOAD_ATTR                count
             1054  LOAD_CONST               5
             1056  LOAD_CONST               600
             1058  LOAD_CONST               ('count', 'sleep', 'giveup')
             1060  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
             1062  STORE_FAST               'links'

 L. 127      1064  LOAD_GLOBAL              open
             1066  LOAD_FAST                'args'
             1068  LOAD_ATTR                out
             1070  LOAD_FAST                'mode'
             1072  CALL_FUNCTION_2       2  '2 positional arguments'
           1074_0  COME_FROM           708  '708'
             1074  SETUP_WITH         1112  'to 1112'
             1076  STORE_FAST               'f'

 L. 128      1078  SETUP_LOOP         1108  'to 1108'
             1080  LOAD_FAST                'links'
             1082  GET_ITER         
             1084  FOR_ITER           1106  'to 1106'
             1086  STORE_FAST               'link'

 L. 129      1088  LOAD_FAST                'f'
             1090  LOAD_METHOD              write
             1092  LOAD_STR                 '%s\n'
             1094  LOAD_FAST                'link'
             1096  BINARY_MODULO    
             1098  CALL_METHOD_1         1  '1 positional argument'
             1100  POP_TOP          
         1102_1104  JUMP_BACK          1084  'to 1084'
             1106  POP_BLOCK        
           1108_0  COME_FROM_LOOP     1078  '1078'
             1108  POP_BLOCK        
             1110  LOAD_CONST               None
           1112_0  COME_FROM_WITH     1074  '1074'
             1112  WITH_CLEANUP_START
             1114  WITH_CLEANUP_FINISH
             1116  END_FINALLY      

 L. 130      1118  LOAD_GLOBAL              print
             1120  LOAD_STR                 'Wrote urls data to: %s'
             1122  LOAD_FAST                'args'
             1124  LOAD_ATTR                out
             1126  BINARY_MODULO    
             1128  CALL_FUNCTION_1       1  '1 positional argument'
             1130  POP_TOP          
             1132  JUMP_FORWARD       1192  'to 1192'
           1134_0  COME_FROM           996  '996'

 L. 133      1134  LOAD_FAST                'parser'
             1136  LOAD_METHOD              print_help
             1138  CALL_METHOD_0         0  '0 positional arguments'
             1140  POP_TOP          

 L. 134      1142  LOAD_FAST                'args'
             1144  LOAD_ATTR                func
         1146_1148  POP_JUMP_IF_FALSE  1192  'to 1192'

 L. 135      1150  LOAD_FAST                'args'
             1152  LOAD_ATTR                func
             1154  LOAD_STR                 'func'
             1156  COMPARE_OP               !=
         1158_1160  POP_JUMP_IF_FALSE  1192  'to 1192'

 L. 136      1162  LOAD_GLOBAL              print
             1164  LOAD_STR                 ''
             1166  CALL_FUNCTION_1       1  '1 positional argument'
             1168  POP_TOP          

 L. 137      1170  LOAD_GLOBAL              print
             1172  LOAD_STR                 'NOTICE: Not yet implemented: %s'
             1174  LOAD_FAST                'args'
             1176  LOAD_ATTR                func
             1178  BINARY_MODULO    
             1180  CALL_FUNCTION_1       1  '1 positional argument'
             1182  POP_TOP          

 L. 138      1184  LOAD_GLOBAL              print
             1186  LOAD_STR                 ''
             1188  CALL_FUNCTION_1       1  '1 positional argument'
             1190  POP_TOP          
           1192_0  COME_FROM          1158  '1158'
           1192_1  COME_FROM          1146  '1146'
           1192_2  COME_FROM          1132  '1132'
           1192_3  COME_FROM           986  '986'
           1192_4  COME_FROM           824  '824'

 L. 139      1192  LOAD_FAST                'r'
             1194  LOAD_GLOBAL              StatusCodes
             1196  LOAD_ATTR                OK
             1198  COMPARE_OP               ==
         1200_1202  POP_JUMP_IF_FALSE  1220  'to 1220'
             1204  LOAD_FAST                'args'
             1206  LOAD_ATTR                debug
         1208_1210  POP_JUMP_IF_FALSE  1220  'to 1220'

 L. 140      1212  LOAD_GLOBAL              dump_messages
             1214  LOAD_FAST                'o'
             1216  CALL_FUNCTION_1       1  '1 positional argument'
             1218  POP_TOP          
           1220_0  COME_FROM          1208  '1208'
           1220_1  COME_FROM          1200  '1200'

Parse error at or near `COME_FROM' instruction at offset 1074_0