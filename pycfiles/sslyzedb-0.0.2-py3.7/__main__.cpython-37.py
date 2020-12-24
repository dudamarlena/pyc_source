# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\sslyzedb\__main__.py
# Compiled at: 2019-02-25 15:01:07
# Size of source mod 2**32: 9213 bytes
import logging, csv, os, sys, ipaddress
from sslyzedb.core.dbmodel import Project, Scan, Target, get_session, create_db
from sslyzedb.core.scanner import *
from sslyzedb.core.report import *
from sslyzedb.utils import *
from sslyzedb import logger

def get_connection_string(args):
    if args.sql is not None:
        if args.sql != '':
            return args.sql
    if 'SSLYZEDB' in os.environ:
        return os.environ['SSLYZEDB']
    raise Exception('DB connection string missing! Provide if either via the "--sql" parameter or by setting the "SSLYZEDB" environment variable')


def run--- This code section failed: ---

 L.  24         0  LOAD_CONST               0
                2  LOAD_CONST               None
                4  IMPORT_NAME              argparse
                6  STORE_FAST               'argparse'

 L.  25         8  LOAD_FAST                'argparse'
               10  LOAD_ATTR                ArgumentParser
               12  LOAD_STR                 'SSLZye on DB'
               14  LOAD_CONST               ('description',)
               16  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               18  STORE_FAST               'parser'

 L.  26        20  LOAD_FAST                'parser'
               22  LOAD_ATTR                add_argument
               24  LOAD_STR                 '-v'
               26  LOAD_STR                 '--verbose'
               28  LOAD_STR                 'count'
               30  LOAD_CONST               0
               32  LOAD_CONST               ('action', 'default')
               34  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
               36  POP_TOP          

 L.  27        38  LOAD_FAST                'parser'
               40  LOAD_ATTR                add_argument
               42  LOAD_STR                 '--sql'
               44  LOAD_STR                 'sql engine address, if not present the script will look for the "SSLYZEDB" environment variable'
               46  LOAD_CONST               ('help',)
               48  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               50  POP_TOP          

 L.  29        52  LOAD_FAST                'parser'
               54  LOAD_ATTR                add_subparsers
               56  LOAD_STR                 'commands'
               58  LOAD_CONST               ('help',)
               60  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               62  STORE_FAST               'subparsers'

 L.  30        64  LOAD_CONST               True
               66  LOAD_FAST                'subparsers'
               68  STORE_ATTR               required

 L.  31        70  LOAD_STR                 'command'
               72  LOAD_FAST                'subparsers'
               74  STORE_ATTR               dest

 L.  33        76  LOAD_FAST                'subparsers'
               78  LOAD_ATTR                add_parser
               80  LOAD_STR                 'db'
               82  LOAD_STR                 'Database operations'
               84  LOAD_CONST               ('help',)
               86  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               88  STORE_FAST               'db_group'

 L.  34        90  LOAD_FAST                'db_group'
               92  LOAD_ATTR                add_argument
               94  LOAD_STR                 'cmd'
               96  LOAD_STR                 '?'
               98  LOAD_STR                 'create'
              100  BUILD_LIST_1          1 
              102  LOAD_STR                 'Database commands.'
              104  LOAD_CONST               ('nargs', 'choices', 'help')
              106  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              108  POP_TOP          

 L.  35       110  LOAD_FAST                'db_group'
              112  LOAD_ATTR                add_argument
              114  LOAD_STR                 'rest'
              116  LOAD_FAST                'argparse'
              118  LOAD_ATTR                REMAINDER
              120  LOAD_CONST               ('nargs',)
              122  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              124  POP_TOP          

 L.  37       126  LOAD_FAST                'subparsers'
              128  LOAD_ATTR                add_parser
              130  LOAD_STR                 'createproject'
              132  LOAD_STR                 'Creates project and gives back the project id'
              134  LOAD_CONST               ('help',)
              136  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              138  STORE_FAST               'createproject_group'

 L.  38       140  LOAD_FAST                'createproject_group'
              142  LOAD_ATTR                add_argument
              144  LOAD_STR                 'name'
              146  LOAD_STR                 'Project name'
              148  LOAD_CONST               ('help',)
              150  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              152  POP_TOP          

 L.  40       154  LOAD_FAST                'subparsers'
              156  LOAD_ATTR                add_parser
              158  LOAD_STR                 'createscan'
              160  LOAD_STR                 'Creates a new scan and adds targets'
              162  LOAD_CONST               ('help',)
              164  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              166  STORE_FAST               'createscan_group'

 L.  41       168  LOAD_FAST                'createscan_group'
              170  LOAD_ATTR                add_argument
              172  LOAD_STR                 'projectid'
              174  LOAD_STR                 'Project id that defines the scope'
              176  LOAD_CONST               ('help',)
              178  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              180  POP_TOP          

 L.  42       182  LOAD_FAST                'createscan_group'
              184  LOAD_ATTR                add_argument
              186  LOAD_STR                 '--retries'
              188  LOAD_GLOBAL              int
              190  LOAD_CONST               3
              192  LOAD_STR                 'How many times a host should be probed in case network fails'
              194  LOAD_CONST               ('type', 'default', 'help')
              196  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              198  POP_TOP          

 L.  43       200  LOAD_FAST                'createscan_group'
              202  LOAD_ATTR                add_argument
              204  LOAD_STR                 '--timeout'
              206  LOAD_GLOBAL              int
              208  LOAD_CONST               5
              210  LOAD_STR                 'Timeout in seconds to be waiting for a host'
              212  LOAD_CONST               ('type', 'default', 'help')
              214  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              216  POP_TOP          

 L.  44       218  LOAD_FAST                'createscan_group'
              220  LOAD_ATTR                add_argument
              222  LOAD_STR                 '--processes'
              224  LOAD_GLOBAL              int
              226  LOAD_CONST               12
              228  LOAD_STR                 'Number of processes (threads) used for scanning'
              230  LOAD_CONST               ('type', 'default', 'help')
              232  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              234  POP_TOP          

 L.  45       236  LOAD_FAST                'createscan_group'
              238  LOAD_ATTR                add_argument
              240  LOAD_STR                 '--processes-per-hostname'
              242  LOAD_GLOBAL              int
              244  LOAD_CONST               3
              246  LOAD_STR                 'Maximum number of parallel scanning processes per host'
              248  LOAD_CONST               ('type', 'default', 'help')
              250  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              252  POP_TOP          

 L.  47       254  LOAD_FAST                'subparsers'
              256  LOAD_ATTR                add_parser
              258  LOAD_STR                 'addtarget'
              260  LOAD_STR                 'Adds target(s) to scan id'
              262  LOAD_CONST               ('help',)
              264  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              266  STORE_FAST               'addtarget_group'

 L.  48       268  LOAD_FAST                'addtarget_group'
              270  LOAD_ATTR                add_argument
              272  LOAD_STR                 'scanid'
              274  LOAD_STR                 'Project id that defines the scope'
              276  LOAD_CONST               ('help',)
              278  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              280  POP_TOP          

 L.  49       282  LOAD_FAST                'addtarget_group'
              284  LOAD_ATTR                add_argument
              286  LOAD_STR                 '-t'
              288  LOAD_STR                 '--target'
              290  LOAD_STR                 'append'
              292  LOAD_STR                 'Hostname or IP of target, in <host/ip>:<port> format. if port not supplied, 443 will be used as default.'
              294  LOAD_CONST               ('action', 'help')
              296  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              298  POP_TOP          

 L.  50       300  LOAD_FAST                'addtarget_group'
              302  LOAD_ATTR                add_argument
              304  LOAD_STR                 '-f'
              306  LOAD_STR                 '--target_file'
              308  LOAD_STR                 'append'
              310  LOAD_STR                 'targets file, one target per line. target format is the same as for -t'
              312  LOAD_CONST               ('action', 'help')
              314  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              316  POP_TOP          

 L.  52       318  LOAD_FAST                'subparsers'
              320  LOAD_ATTR                add_parser
              322  LOAD_STR                 'addcommand'
              324  LOAD_STR                 'Adds command(s) to scan id'
              326  LOAD_CONST               ('help',)
              328  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              330  STORE_FAST               'addcmd_group'

 L.  53       332  LOAD_FAST                'addcmd_group'
              334  LOAD_ATTR                add_argument
              336  LOAD_STR                 'scanid'
              338  LOAD_STR                 'Project id that defines the scope'
              340  LOAD_CONST               ('help',)
              342  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              344  POP_TOP          

 L.  54       346  LOAD_FAST                'addcmd_group'
              348  LOAD_ATTR                add_argument
              350  LOAD_STR                 'commands'
              352  LOAD_FAST                'argparse'
              354  LOAD_ATTR                REMAINDER
              356  LOAD_STR                 'Scan commands'
              358  LOAD_CONST               ('nargs', 'help')
              360  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              362  POP_TOP          

 L.  56       364  LOAD_FAST                'subparsers'
              366  LOAD_ATTR                add_parser
              368  LOAD_STR                 'scan'
              370  LOAD_STR                 'Start scanning'
              372  LOAD_CONST               ('help',)
              374  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              376  STORE_FAST               'scan_group'

 L.  57       378  LOAD_FAST                'scan_group'
              380  LOAD_ATTR                add_argument
              382  LOAD_STR                 'scanid'
              384  LOAD_STR                 'Scan id that defines the scope'
              386  LOAD_CONST               ('help',)
              388  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              390  POP_TOP          

 L.  58       392  LOAD_FAST                'scan_group'
              394  LOAD_ATTR                add_argument
              396  LOAD_STR                 '-p'
              398  LOAD_STR                 '--progress-bar'
              400  LOAD_STR                 'store_true'
              402  LOAD_STR                 'Show progress bar for scanning'
              404  LOAD_CONST               ('action', 'help')
              406  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              408  POP_TOP          

 L.  60       410  LOAD_FAST                'subparsers'
              412  LOAD_ATTR                add_parser
              414  LOAD_STR                 'report'
              416  LOAD_STR                 'Generate report'
              418  LOAD_CONST               ('help',)
              420  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              422  STORE_FAST               'report_group'

 L.  61       424  LOAD_FAST                'report_group'
              426  LOAD_ATTR                add_argument
              428  LOAD_STR                 'scanid'
              430  LOAD_STR                 'Scan id that defines the scope'
              432  LOAD_CONST               ('help',)
              434  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              436  POP_TOP          

 L.  62       438  LOAD_FAST                'report_group'
              440  LOAD_ATTR                add_argument
              442  LOAD_STR                 '-o'
              444  LOAD_STR                 '--outfile'
              446  LOAD_STR                 'File to write the report to, otherwise STDOUT'
              448  LOAD_CONST               ('help',)
              450  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              452  POP_TOP          

 L.  63       454  LOAD_FAST                'report_group'
              456  LOAD_ATTR                add_argument
              458  LOAD_STR                 '--full-report'
              460  LOAD_STR                 'store_true'
              462  LOAD_STR                 'Causes all ciphers to be inculded in the report'
              464  LOAD_CONST               ('action', 'help')
              466  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              468  POP_TOP          

 L.  65       470  LOAD_FAST                'subparsers'
              472  LOAD_ATTR                add_parser
              474  LOAD_STR                 'quick'
              476  LOAD_STR                 'Generate report'
              478  LOAD_CONST               ('help',)
              480  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              482  STORE_FAST               'quick_group'

 L.  66       484  LOAD_FAST                'quick_group'
              486  LOAD_ATTR                add_argument
              488  LOAD_STR                 '-t'
              490  LOAD_STR                 '--target'
              492  LOAD_STR                 'append'
              494  LOAD_STR                 'Hostname or IP of target, in <host/ip>:<port> format. if port not supplied, 443 will be used as default.'
              496  LOAD_CONST               ('action', 'help')
              498  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              500  POP_TOP          

 L.  67       502  LOAD_FAST                'quick_group'
              504  LOAD_ATTR                add_argument
              506  LOAD_STR                 '-f'
              508  LOAD_STR                 '--target_file'
              510  LOAD_STR                 'append'
              512  LOAD_STR                 'targets file, one target per line. target format is the same as for -t'
              514  LOAD_CONST               ('action', 'help')
              516  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              518  POP_TOP          

 L.  68       520  LOAD_FAST                'quick_group'
              522  LOAD_ATTR                add_argument
              524  LOAD_STR                 '-o'
              526  LOAD_STR                 '--outfile'
              528  LOAD_STR                 'File to write the report to, otherwise STDOUT'
              530  LOAD_CONST               ('help',)
              532  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              534  POP_TOP          

 L.  69       536  LOAD_FAST                'quick_group'
              538  LOAD_ATTR                add_argument
              540  LOAD_STR                 '--full-report'
              542  LOAD_STR                 'store_true'
              544  LOAD_STR                 'Causes all ciphers to be inculded in the report'
              546  LOAD_CONST               ('action', 'help')
              548  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              550  POP_TOP          

 L.  70       552  LOAD_FAST                'quick_group'
              554  LOAD_ATTR                add_argument
              556  LOAD_STR                 '-p'
              558  LOAD_STR                 '--progress-bar'
              560  LOAD_STR                 'store_true'
              562  LOAD_STR                 'Show progress bar for scanning'
              564  LOAD_CONST               ('action', 'help')
              566  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              568  POP_TOP          

 L.  72       570  LOAD_FAST                'parser'
              572  LOAD_METHOD              parse_args
              574  CALL_METHOD_0         0  '0 positional arguments'
              576  STORE_FAST               'args'

 L.  76       578  LOAD_FAST                'args'
              580  LOAD_ATTR                verbose
              582  LOAD_CONST               0
              584  COMPARE_OP               ==
          586_588  POP_JUMP_IF_FALSE   618  'to 618'

 L.  77       590  LOAD_GLOBAL              logging
              592  LOAD_ATTR                basicConfig
              594  LOAD_GLOBAL              logging
              596  LOAD_ATTR                INFO
              598  LOAD_CONST               ('level',)
              600  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              602  POP_TOP          

 L.  78       604  LOAD_GLOBAL              logger
              606  LOAD_METHOD              setLevel
              608  LOAD_GLOBAL              logging
              610  LOAD_ATTR                INFO
              612  CALL_METHOD_1         1  '1 positional argument'
              614  POP_TOP          
              616  JUMP_FORWARD        680  'to 680'
            618_0  COME_FROM           586  '586'

 L.  79       618  LOAD_FAST                'args'
              620  LOAD_ATTR                verbose
              622  LOAD_CONST               1
              624  COMPARE_OP               ==
          626_628  POP_JUMP_IF_FALSE   658  'to 658'

 L.  80       630  LOAD_GLOBAL              logging
              632  LOAD_ATTR                basicConfig
              634  LOAD_GLOBAL              logging
              636  LOAD_ATTR                DEBUG
              638  LOAD_CONST               ('level',)
              640  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              642  POP_TOP          

 L.  81       644  LOAD_GLOBAL              logger
              646  LOAD_METHOD              setLevel
              648  LOAD_GLOBAL              logging
              650  LOAD_ATTR                DEBUG
              652  CALL_METHOD_1         1  '1 positional argument'
              654  POP_TOP          
              656  JUMP_FORWARD        680  'to 680'
            658_0  COME_FROM           626  '626'

 L.  83       658  LOAD_GLOBAL              logging
              660  LOAD_ATTR                basicConfig
              662  LOAD_CONST               1
              664  LOAD_CONST               ('level',)
              666  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              668  POP_TOP          

 L.  84       670  LOAD_GLOBAL              logger
              672  LOAD_METHOD              setLevel
              674  LOAD_CONST               1
              676  CALL_METHOD_1         1  '1 positional argument'
              678  POP_TOP          
            680_0  COME_FROM           656  '656'
            680_1  COME_FROM           616  '616'

 L.  86       680  LOAD_FAST                'args'
              682  LOAD_ATTR                command
              684  LOAD_STR                 'db'
              686  COMPARE_OP               ==
          688_690  POP_JUMP_IF_FALSE   744  'to 744'

 L.  87       692  LOAD_FAST                'args'
              694  LOAD_ATTR                cmd
              696  LOAD_STR                 'create'
              698  COMPARE_OP               ==
          700_702  POP_JUMP_IF_FALSE   726  'to 726'

 L.  88       704  LOAD_GLOBAL              get_connection_string
              706  LOAD_FAST                'args'
              708  CALL_FUNCTION_1       1  '1 positional argument'
              710  STORE_FAST               'conn'

 L.  89       712  LOAD_GLOBAL              create_db
              714  LOAD_FAST                'conn'
              716  LOAD_FAST                'args'
              718  LOAD_ATTR                verbose
              720  CALL_FUNCTION_2       2  '2 positional arguments'
              722  POP_TOP          
              724  JUMP_FORWARD       2252  'to 2252'
            726_0  COME_FROM           700  '700'

 L.  92       726  LOAD_GLOBAL              Exception
              728  LOAD_STR                 'Unsupported DB subcommand %s'
              730  LOAD_FAST                'args'
              732  LOAD_ATTR                cmd
              734  BINARY_MODULO    
              736  CALL_FUNCTION_1       1  '1 positional argument'
              738  RAISE_VARARGS_1       1  'exception instance'
          740_742  JUMP_FORWARD       2252  'to 2252'
            744_0  COME_FROM           688  '688'

 L.  94       744  LOAD_FAST                'args'
              746  LOAD_ATTR                command
              748  LOAD_STR                 'createproject'
              750  COMPARE_OP               ==
          752_754  POP_JUMP_IF_FALSE   854  'to 854'

 L.  95       756  LOAD_GLOBAL              get_connection_string
              758  LOAD_FAST                'args'
              760  CALL_FUNCTION_1       1  '1 positional argument'
              762  STORE_FAST               'conn'

 L.  96       764  LOAD_GLOBAL              get_session
              766  LOAD_FAST                'conn'
              768  LOAD_FAST                'args'
              770  LOAD_ATTR                verbose
              772  CALL_FUNCTION_2       2  '2 positional arguments'
              774  STORE_FAST               'session'

 L.  97       776  LOAD_GLOBAL              logging
              778  LOAD_METHOD              debug
              780  LOAD_STR                 'Creating project'
              782  CALL_METHOD_1         1  '1 positional argument'
              784  POP_TOP          

 L.  98       786  LOAD_GLOBAL              Project
              788  LOAD_FAST                'args'
              790  LOAD_ATTR                name
              792  LOAD_STR                 ''
              794  CALL_FUNCTION_2       2  '2 positional arguments'
              796  STORE_FAST               'project'

 L.  99       798  LOAD_FAST                'session'
              800  LOAD_METHOD              add
              802  LOAD_FAST                'project'
              804  CALL_METHOD_1         1  '1 positional argument'
              806  POP_TOP          

 L. 100       808  LOAD_FAST                'session'
              810  LOAD_METHOD              commit
              812  CALL_METHOD_0         0  '0 positional arguments'
              814  POP_TOP          

 L. 101       816  LOAD_FAST                'session'
              818  LOAD_METHOD              refresh
              820  LOAD_FAST                'project'
              822  CALL_METHOD_1         1  '1 positional argument'
              824  POP_TOP          

 L. 102       826  LOAD_FAST                'session'
              828  LOAD_METHOD              close
              830  CALL_METHOD_0         0  '0 positional arguments'
              832  POP_TOP          

 L. 103       834  LOAD_GLOBAL              logging
              836  LOAD_METHOD              info
              838  LOAD_STR                 'Created project with ID %s'
              840  LOAD_FAST                'project'
              842  LOAD_ATTR                id
              844  BINARY_MODULO    
              846  CALL_METHOD_1         1  '1 positional argument'
              848  POP_TOP          
          850_852  JUMP_FORWARD       2252  'to 2252'
            854_0  COME_FROM           752  '752'

 L. 105       854  LOAD_FAST                'args'
              856  LOAD_ATTR                command
              858  LOAD_STR                 'createscan'
              860  COMPARE_OP               ==
          862_864  POP_JUMP_IF_FALSE  1008  'to 1008'

 L. 106       866  LOAD_GLOBAL              get_connection_string
              868  LOAD_FAST                'args'
              870  CALL_FUNCTION_1       1  '1 positional argument'
              872  STORE_FAST               'conn'

 L. 107       874  LOAD_GLOBAL              get_session
              876  LOAD_FAST                'conn'
              878  LOAD_FAST                'args'
              880  LOAD_ATTR                verbose
              882  CALL_FUNCTION_2       2  '2 positional arguments'
              884  STORE_FAST               'session'

 L. 108       886  LOAD_GLOBAL              logging
              888  LOAD_METHOD              debug
              890  LOAD_STR                 'Creating scan'
              892  CALL_METHOD_1         1  '1 positional argument'
              894  POP_TOP          

 L. 109       896  LOAD_FAST                'session'
              898  LOAD_METHOD              query
              900  LOAD_GLOBAL              Project
              902  CALL_METHOD_1         1  '1 positional argument'
              904  LOAD_METHOD              get
              906  LOAD_FAST                'args'
              908  LOAD_ATTR                projectid
              910  CALL_METHOD_1         1  '1 positional argument'
              912  STORE_FAST               'project'

 L. 110       914  LOAD_GLOBAL              Scan
              916  CALL_FUNCTION_0       0  '0 positional arguments'
              918  STORE_FAST               'scan'

 L. 111       920  LOAD_FAST                'args'
              922  LOAD_ATTR                retries
              924  LOAD_FAST                'scan'
              926  STORE_ATTR               network_retries

 L. 112       928  LOAD_FAST                'args'
              930  LOAD_ATTR                timeout
              932  LOAD_FAST                'scan'
              934  STORE_ATTR               network_timeout

 L. 113       936  LOAD_FAST                'args'
              938  LOAD_ATTR                processes
              940  LOAD_FAST                'scan'
              942  STORE_ATTR               max_processes_nb

 L. 114       944  LOAD_FAST                'args'
              946  LOAD_ATTR                processes_per_hostname
              948  LOAD_FAST                'scan'
              950  STORE_ATTR               max_processes_per_hostname_nb

 L. 115       952  LOAD_FAST                'session'
              954  LOAD_METHOD              add
              956  LOAD_FAST                'scan'
              958  CALL_METHOD_1         1  '1 positional argument'
              960  POP_TOP          

 L. 116       962  LOAD_FAST                'session'
              964  LOAD_METHOD              commit
              966  CALL_METHOD_0         0  '0 positional arguments'
              968  POP_TOP          

 L. 117       970  LOAD_FAST                'session'
              972  LOAD_METHOD              refresh
              974  LOAD_FAST                'scan'
              976  CALL_METHOD_1         1  '1 positional argument'
              978  POP_TOP          

 L. 118       980  LOAD_FAST                'session'
              982  LOAD_METHOD              close
              984  CALL_METHOD_0         0  '0 positional arguments'
              986  POP_TOP          

 L. 119       988  LOAD_GLOBAL              logging
              990  LOAD_METHOD              debug
              992  LOAD_STR                 'Created scan with ID %s'
              994  LOAD_FAST                'scan'
              996  LOAD_ATTR                id
              998  BINARY_MODULO    
             1000  CALL_METHOD_1         1  '1 positional argument'
             1002  POP_TOP          
         1004_1006  JUMP_FORWARD       2252  'to 2252'
           1008_0  COME_FROM           862  '862'

 L. 121      1008  LOAD_FAST                'args'
             1010  LOAD_ATTR                command
             1012  LOAD_STR                 'addtarget'
             1014  COMPARE_OP               ==
         1016_1018  POP_JUMP_IF_FALSE  1230  'to 1230'

 L. 122      1020  LOAD_GLOBAL              get_connection_string
             1022  LOAD_FAST                'args'
             1024  CALL_FUNCTION_1       1  '1 positional argument'
             1026  STORE_FAST               'conn'

 L. 123      1028  LOAD_GLOBAL              get_session
             1030  LOAD_FAST                'conn'
             1032  LOAD_FAST                'args'
             1034  LOAD_ATTR                verbose
             1036  CALL_FUNCTION_2       2  '2 positional arguments'
             1038  STORE_FAST               'session'

 L. 124      1040  LOAD_FAST                'session'
             1042  LOAD_METHOD              query
             1044  LOAD_GLOBAL              Scan
             1046  CALL_METHOD_1         1  '1 positional argument'
             1048  LOAD_METHOD              get
             1050  LOAD_FAST                'args'
             1052  LOAD_ATTR                scanid
             1054  CALL_METHOD_1         1  '1 positional argument'
             1056  STORE_FAST               'scan'

 L. 126      1058  LOAD_FAST                'args'
             1060  LOAD_ATTR                target_file
         1062_1064  POP_JUMP_IF_FALSE  1152  'to 1152'

 L. 127      1066  SETUP_LOOP         1152  'to 1152'
             1068  LOAD_FAST                'args'
             1070  LOAD_ATTR                target_file
             1072  GET_ITER         
             1074  FOR_ITER           1150  'to 1150'
             1076  STORE_FAST               'filename'

 L. 128      1078  LOAD_GLOBAL              open
             1080  LOAD_FAST                'filename'
             1082  LOAD_STR                 'r'
             1084  CALL_FUNCTION_2       2  '2 positional arguments'
             1086  SETUP_WITH         1140  'to 1140'
             1088  STORE_FAST               'f'

 L. 129      1090  SETUP_LOOP         1136  'to 1136'
             1092  LOAD_FAST                'f'
             1094  GET_ITER         
             1096  FOR_ITER           1134  'to 1134'
             1098  STORE_FAST               'line'

 L. 130      1100  LOAD_FAST                'line'
             1102  LOAD_METHOD              strip
             1104  CALL_METHOD_0         0  '0 positional arguments'
             1106  STORE_FAST               'line'

 L. 131      1108  LOAD_GLOBAL              Target
             1110  LOAD_METHOD              from_line
             1112  LOAD_FAST                'line'
             1114  CALL_METHOD_1         1  '1 positional argument'
             1116  STORE_FAST               'target'

 L. 132      1118  LOAD_FAST                'scan'
             1120  LOAD_ATTR                targets
             1122  LOAD_METHOD              append
             1124  LOAD_FAST                'target'
             1126  CALL_METHOD_1         1  '1 positional argument'
             1128  POP_TOP          
         1130_1132  JUMP_BACK          1096  'to 1096'
             1134  POP_BLOCK        
           1136_0  COME_FROM_LOOP     1090  '1090'
             1136  POP_BLOCK        
             1138  LOAD_CONST               None
           1140_0  COME_FROM_WITH     1086  '1086'
             1140  WITH_CLEANUP_START
             1142  WITH_CLEANUP_FINISH
             1144  END_FINALLY      
         1146_1148  JUMP_BACK          1074  'to 1074'
             1150  POP_BLOCK        
           1152_0  COME_FROM_LOOP     1066  '1066'
           1152_1  COME_FROM          1062  '1062'

 L. 134      1152  LOAD_FAST                'args'
             1154  LOAD_ATTR                target
         1156_1158  POP_JUMP_IF_FALSE  1200  'to 1200'

 L. 135      1160  SETUP_LOOP         1200  'to 1200'
             1162  LOAD_FAST                'args'
             1164  LOAD_ATTR                target
             1166  GET_ITER         
             1168  FOR_ITER           1198  'to 1198'
             1170  STORE_FAST               'targetentry'

 L. 136      1172  LOAD_GLOBAL              Target
             1174  LOAD_METHOD              from_line
             1176  LOAD_FAST                'targetentry'
             1178  CALL_METHOD_1         1  '1 positional argument'
             1180  STORE_FAST               'target'

 L. 137      1182  LOAD_FAST                'scan'
             1184  LOAD_ATTR                targets
             1186  LOAD_METHOD              append
             1188  LOAD_FAST                'target'
             1190  CALL_METHOD_1         1  '1 positional argument'
             1192  POP_TOP          
         1194_1196  JUMP_BACK          1168  'to 1168'
             1198  POP_BLOCK        
           1200_0  COME_FROM_LOOP     1160  '1160'
           1200_1  COME_FROM          1156  '1156'

 L. 138      1200  LOAD_FAST                'session'
             1202  LOAD_METHOD              add
             1204  LOAD_FAST                'scan'
             1206  CALL_METHOD_1         1  '1 positional argument'
             1208  POP_TOP          

 L. 139      1210  LOAD_FAST                'session'
             1212  LOAD_METHOD              commit
             1214  CALL_METHOD_0         0  '0 positional arguments'
             1216  POP_TOP          

 L. 140      1218  LOAD_FAST                'session'
             1220  LOAD_METHOD              close
             1222  CALL_METHOD_0         0  '0 positional arguments'
             1224  POP_TOP          
         1226_1228  JUMP_FORWARD       2252  'to 2252'
           1230_0  COME_FROM          1016  '1016'

 L. 142      1230  LOAD_FAST                'args'
             1232  LOAD_ATTR                command
             1234  LOAD_STR                 'addcommand'
             1236  COMPARE_OP               ==
         1238_1240  POP_JUMP_IF_FALSE  1370  'to 1370'

 L. 143      1242  LOAD_GLOBAL              get_connection_string
             1244  LOAD_FAST                'args'
             1246  CALL_FUNCTION_1       1  '1 positional argument'
             1248  STORE_FAST               'conn'

 L. 144      1250  LOAD_GLOBAL              get_session
             1252  LOAD_FAST                'conn'
             1254  LOAD_FAST                'args'
             1256  LOAD_ATTR                verbose
             1258  CALL_FUNCTION_2       2  '2 positional arguments'
             1260  STORE_FAST               'session'

 L. 145      1262  LOAD_FAST                'session'
             1264  LOAD_METHOD              query
             1266  LOAD_GLOBAL              Scan
             1268  CALL_METHOD_1         1  '1 positional argument'
             1270  LOAD_METHOD              get
             1272  LOAD_FAST                'args'
             1274  LOAD_ATTR                scanid
             1276  CALL_METHOD_1         1  '1 positional argument'
             1278  STORE_FAST               'scan'

 L. 146      1280  SETUP_LOOP         1340  'to 1340'
             1282  LOAD_FAST                'args'
             1284  LOAD_ATTR                commands
             1286  GET_ITER         
             1288  FOR_ITER           1338  'to 1338'
             1290  STORE_FAST               'command'

 L. 147      1292  LOAD_GLOBAL              SSLYZECommand
             1294  LOAD_FAST                'command'
             1296  LOAD_METHOD              upper
             1298  CALL_METHOD_0         0  '0 positional arguments'
             1300  BINARY_SUBSCR    
             1302  STORE_FAST               'c'

 L. 148      1304  LOAD_GLOBAL              ScanCommand
             1306  CALL_FUNCTION_0       0  '0 positional arguments'
             1308  STORE_FAST               'sc'

 L. 149      1310  LOAD_FAST                'args'
             1312  LOAD_ATTR                scanid
             1314  LOAD_FAST                'sc'
             1316  STORE_ATTR               scan_id

 L. 150      1318  LOAD_FAST                'c'
             1320  LOAD_FAST                'sc'
             1322  STORE_ATTR               command

 L. 151      1324  LOAD_FAST                'session'
             1326  LOAD_METHOD              add
             1328  LOAD_FAST                'sc'
             1330  CALL_METHOD_1         1  '1 positional argument'
             1332  POP_TOP          
         1334_1336  JUMP_BACK          1288  'to 1288'
             1338  POP_BLOCK        
           1340_0  COME_FROM_LOOP     1280  '1280'

 L. 153      1340  LOAD_FAST                'session'
             1342  LOAD_METHOD              commit
             1344  CALL_METHOD_0         0  '0 positional arguments'
             1346  POP_TOP          

 L. 154      1348  LOAD_FAST                'session'
             1350  LOAD_METHOD              close
             1352  CALL_METHOD_0         0  '0 positional arguments'
             1354  POP_TOP          

 L. 155      1356  LOAD_GLOBAL              logging
             1358  LOAD_METHOD              debug
             1360  LOAD_STR                 'Commands added'
             1362  CALL_METHOD_1         1  '1 positional argument'
             1364  POP_TOP          
         1366_1368  JUMP_FORWARD       2252  'to 2252'
           1370_0  COME_FROM          1238  '1238'

 L. 157      1370  LOAD_FAST                'args'
             1372  LOAD_ATTR                command
             1374  LOAD_STR                 'scan'
             1376  COMPARE_OP               ==
         1378_1380  POP_JUMP_IF_FALSE  1432  'to 1432'

 L. 158      1382  LOAD_GLOBAL              get_connection_string
             1384  LOAD_FAST                'args'
             1386  CALL_FUNCTION_1       1  '1 positional argument'
             1388  STORE_FAST               'conn'

 L. 159      1390  LOAD_GLOBAL              get_session
             1392  LOAD_FAST                'conn'
             1394  LOAD_FAST                'args'
             1396  LOAD_ATTR                verbose
             1398  CALL_FUNCTION_2       2  '2 positional arguments'
             1400  STORE_FAST               'session'

 L. 160      1402  LOAD_GLOBAL              logging
             1404  LOAD_METHOD              debug
             1406  LOAD_STR                 'Starting scan'
             1408  CALL_METHOD_1         1  '1 positional argument'
             1410  POP_TOP          

 L. 161      1412  LOAD_GLOBAL              start_scanner
             1414  LOAD_FAST                'session'
             1416  LOAD_FAST                'args'
             1418  LOAD_ATTR                scanid
             1420  LOAD_FAST                'args'
             1422  LOAD_ATTR                progress_bar
             1424  CALL_FUNCTION_3       3  '3 positional arguments'
             1426  POP_TOP          
         1428_1430  JUMP_FORWARD       2252  'to 2252'
           1432_0  COME_FROM          1378  '1378'

 L. 163      1432  LOAD_FAST                'args'
             1434  LOAD_ATTR                command
             1436  LOAD_STR                 'report'
             1438  COMPARE_OP               ==
         1440_1442  POP_JUMP_IF_FALSE  1602  'to 1602'

 L. 164      1444  LOAD_GLOBAL              get_connection_string
             1446  LOAD_FAST                'args'
             1448  CALL_FUNCTION_1       1  '1 positional argument'
             1450  STORE_FAST               'conn'

 L. 165      1452  LOAD_GLOBAL              get_session
             1454  LOAD_FAST                'conn'
             1456  LOAD_FAST                'args'
             1458  LOAD_ATTR                verbose
             1460  CALL_FUNCTION_2       2  '2 positional arguments'
             1462  STORE_FAST               'session'

 L. 166      1464  LOAD_GLOBAL              logging
             1466  LOAD_METHOD              debug
             1468  LOAD_STR                 'Starting reporting'
             1470  CALL_METHOD_1         1  '1 positional argument'
             1472  POP_TOP          

 L. 167      1474  LOAD_GLOBAL              generate_report
             1476  LOAD_FAST                'session'
             1478  LOAD_FAST                'args'
             1480  LOAD_ATTR                scanid
             1482  LOAD_FAST                'args'
             1484  LOAD_ATTR                full_report
             1486  CALL_FUNCTION_3       3  '3 positional arguments'
             1488  STORE_FAST               'data_lines'

 L. 168      1490  LOAD_FAST                'args'
             1492  LOAD_ATTR                outfile
             1494  LOAD_CONST               None
             1496  COMPARE_OP               is-not
         1498_1500  POP_JUMP_IF_FALSE  1568  'to 1568'

 L. 169      1502  LOAD_GLOBAL              open
             1504  LOAD_FAST                'args'
             1506  LOAD_ATTR                outfile
             1508  LOAD_STR                 'wb'
             1510  CALL_FUNCTION_2       2  '2 positional arguments'
             1512  SETUP_WITH         1560  'to 1560'
             1514  STORE_FAST               'f'

 L. 170      1516  SETUP_LOOP         1556  'to 1556'
             1518  LOAD_FAST                'data_lines'
             1520  GET_ITER         
             1522  FOR_ITER           1554  'to 1554'
             1524  STORE_FAST               'line'

 L. 171      1526  LOAD_FAST                'f'
             1528  LOAD_METHOD              write
             1530  LOAD_STR                 '\t'
             1532  LOAD_METHOD              join
             1534  LOAD_FAST                'line'
             1536  CALL_METHOD_1         1  '1 positional argument'
             1538  LOAD_METHOD              encode
             1540  CALL_METHOD_0         0  '0 positional arguments'
             1542  LOAD_CONST               b'\r\n'
             1544  BINARY_ADD       
             1546  CALL_METHOD_1         1  '1 positional argument'
             1548  POP_TOP          
         1550_1552  JUMP_BACK          1522  'to 1522'
             1554  POP_BLOCK        
           1556_0  COME_FROM_LOOP     1516  '1516'
             1556  POP_BLOCK        
             1558  LOAD_CONST               None
           1560_0  COME_FROM_WITH     1512  '1512'
             1560  WITH_CLEANUP_START
             1562  WITH_CLEANUP_FINISH
             1564  END_FINALLY      
             1566  JUMP_FORWARD       2252  'to 2252'
           1568_0  COME_FROM          1498  '1498'

 L. 173      1568  SETUP_LOOP         1598  'to 1598'
             1570  LOAD_FAST                'data_lines'
             1572  GET_ITER         
             1574  FOR_ITER           1596  'to 1596'
             1576  STORE_FAST               'line'

 L. 174      1578  LOAD_GLOBAL              print
             1580  LOAD_STR                 '\t'
             1582  LOAD_METHOD              join
             1584  LOAD_FAST                'line'
             1586  CALL_METHOD_1         1  '1 positional argument'
             1588  CALL_FUNCTION_1       1  '1 positional argument'
             1590  POP_TOP          
         1592_1594  JUMP_BACK          1574  'to 1574'
             1596  POP_BLOCK        
           1598_0  COME_FROM_LOOP     1568  '1568'
         1598_1600  JUMP_FORWARD       2252  'to 2252'
           1602_0  COME_FROM          1440  '1440'

 L. 176      1602  LOAD_FAST                'args'
             1604  LOAD_ATTR                command
             1606  LOAD_STR                 'quick'
             1608  COMPARE_OP               ==
         1610_1612  POP_JUMP_IF_FALSE  2252  'to 2252'

 L. 177      1614  LOAD_FAST                'args'
             1616  LOAD_ATTR                target_file
         1618_1620  POP_JUMP_IF_TRUE   1648  'to 1648'
             1622  LOAD_FAST                'args'
             1624  LOAD_ATTR                target
         1626_1628  POP_JUMP_IF_TRUE   1648  'to 1648'

 L. 178      1630  LOAD_GLOBAL              print
             1632  LOAD_STR                 'Not targets supplied! Use either -t or -f'
             1634  CALL_FUNCTION_1       1  '1 positional argument'
             1636  POP_TOP          

 L. 179      1638  LOAD_GLOBAL              sys
             1640  LOAD_METHOD              exit
             1642  LOAD_CONST               1
             1644  CALL_METHOD_1         1  '1 positional argument'
             1646  POP_TOP          
           1648_0  COME_FROM          1626  '1626'
           1648_1  COME_FROM          1618  '1618'

 L. 180      1648  LOAD_GLOBAL              get_connection_string
             1650  LOAD_FAST                'args'
             1652  CALL_FUNCTION_1       1  '1 positional argument'
             1654  STORE_FAST               'conn'

 L. 181      1656  LOAD_GLOBAL              create_db
             1658  LOAD_FAST                'conn'
             1660  LOAD_FAST                'args'
             1662  LOAD_ATTR                verbose
             1664  CALL_FUNCTION_2       2  '2 positional arguments'
             1666  POP_TOP          

 L. 182      1668  LOAD_GLOBAL              get_session
             1670  LOAD_FAST                'conn'
             1672  LOAD_FAST                'args'
             1674  LOAD_ATTR                verbose
             1676  CALL_FUNCTION_2       2  '2 positional arguments'
             1678  STORE_FAST               'session'

 L. 183      1680  LOAD_GLOBAL              logging
             1682  LOAD_METHOD              debug
             1684  LOAD_STR                 'Creating project'
             1686  CALL_METHOD_1         1  '1 positional argument'
             1688  POP_TOP          

 L. 184      1690  LOAD_GLOBAL              Project
             1692  LOAD_STR                 'quick'
             1694  LOAD_STR                 ''
             1696  CALL_FUNCTION_2       2  '2 positional arguments'
             1698  STORE_FAST               'project'

 L. 185      1700  LOAD_FAST                'session'
             1702  LOAD_METHOD              add
             1704  LOAD_FAST                'project'
             1706  CALL_METHOD_1         1  '1 positional argument'
             1708  POP_TOP          

 L. 186      1710  LOAD_FAST                'session'
             1712  LOAD_METHOD              commit
             1714  CALL_METHOD_0         0  '0 positional arguments'
             1716  POP_TOP          

 L. 187      1718  LOAD_FAST                'session'
             1720  LOAD_METHOD              refresh
             1722  LOAD_FAST                'project'
             1724  CALL_METHOD_1         1  '1 positional argument'
             1726  POP_TOP          

 L. 188      1728  LOAD_GLOBAL              logging
             1730  LOAD_METHOD              info
             1732  LOAD_STR                 'Created project with ID %s'
             1734  LOAD_FAST                'project'
             1736  LOAD_ATTR                id
             1738  BINARY_MODULO    
             1740  CALL_METHOD_1         1  '1 positional argument'
             1742  POP_TOP          

 L. 189      1744  LOAD_GLOBAL              logging
             1746  LOAD_METHOD              debug
             1748  LOAD_STR                 'Creating scan'
             1750  CALL_METHOD_1         1  '1 positional argument'
             1752  POP_TOP          

 L. 190      1754  LOAD_FAST                'session'
             1756  LOAD_METHOD              query
             1758  LOAD_GLOBAL              Project
             1760  CALL_METHOD_1         1  '1 positional argument'
             1762  LOAD_METHOD              get
             1764  LOAD_FAST                'project'
             1766  LOAD_ATTR                id
             1768  CALL_METHOD_1         1  '1 positional argument'
             1770  STORE_FAST               'project'

 L. 191      1772  LOAD_GLOBAL              Scan
             1774  CALL_FUNCTION_0       0  '0 positional arguments'
             1776  STORE_FAST               'scan'

 L. 192      1778  LOAD_FAST                'session'
             1780  LOAD_METHOD              add
             1782  LOAD_FAST                'scan'
             1784  CALL_METHOD_1         1  '1 positional argument'
             1786  POP_TOP          

 L. 193      1788  LOAD_FAST                'session'
             1790  LOAD_METHOD              commit
             1792  CALL_METHOD_0         0  '0 positional arguments'
             1794  POP_TOP          

 L. 194      1796  LOAD_FAST                'session'
             1798  LOAD_METHOD              refresh
             1800  LOAD_FAST                'scan'
             1802  CALL_METHOD_1         1  '1 positional argument'
             1804  POP_TOP          

 L. 195      1806  LOAD_GLOBAL              logging
             1808  LOAD_METHOD              debug
             1810  LOAD_STR                 'Created scan with ID %s'
             1812  LOAD_FAST                'scan'
             1814  LOAD_ATTR                id
             1816  BINARY_MODULO    
             1818  CALL_METHOD_1         1  '1 positional argument'
             1820  POP_TOP          

 L. 196      1822  LOAD_FAST                'session'
             1824  LOAD_METHOD              query
             1826  LOAD_GLOBAL              Scan
             1828  CALL_METHOD_1         1  '1 positional argument'
             1830  LOAD_METHOD              get
             1832  LOAD_FAST                'scan'
             1834  LOAD_ATTR                id
             1836  CALL_METHOD_1         1  '1 positional argument'
             1838  STORE_FAST               'scan'

 L. 198      1840  LOAD_FAST                'args'
             1842  LOAD_ATTR                target_file
         1844_1846  POP_JUMP_IF_FALSE  1934  'to 1934'

 L. 199      1848  SETUP_LOOP         1934  'to 1934'
             1850  LOAD_FAST                'args'
             1852  LOAD_ATTR                target_file
             1854  GET_ITER         
             1856  FOR_ITER           1932  'to 1932'
             1858  STORE_FAST               'filename'

 L. 200      1860  LOAD_GLOBAL              open
             1862  LOAD_FAST                'filename'
             1864  LOAD_STR                 'r'
             1866  CALL_FUNCTION_2       2  '2 positional arguments'
             1868  SETUP_WITH         1922  'to 1922'
             1870  STORE_FAST               'f'

 L. 201      1872  SETUP_LOOP         1918  'to 1918'
             1874  LOAD_FAST                'f'
             1876  GET_ITER         
             1878  FOR_ITER           1916  'to 1916'
             1880  STORE_FAST               'line'

 L. 202      1882  LOAD_FAST                'line'
             1884  LOAD_METHOD              strip
             1886  CALL_METHOD_0         0  '0 positional arguments'
             1888  STORE_FAST               'line'

 L. 203      1890  LOAD_GLOBAL              Target
             1892  LOAD_METHOD              from_line
             1894  LOAD_FAST                'line'
             1896  CALL_METHOD_1         1  '1 positional argument'
             1898  STORE_FAST               'target'

 L. 204      1900  LOAD_FAST                'scan'
             1902  LOAD_ATTR                targets
             1904  LOAD_METHOD              append
             1906  LOAD_FAST                'target'
             1908  CALL_METHOD_1         1  '1 positional argument'
             1910  POP_TOP          
         1912_1914  JUMP_BACK          1878  'to 1878'
             1916  POP_BLOCK        
           1918_0  COME_FROM_LOOP     1872  '1872'
             1918  POP_BLOCK        
             1920  LOAD_CONST               None
           1922_0  COME_FROM_WITH     1868  '1868'
             1922  WITH_CLEANUP_START
             1924  WITH_CLEANUP_FINISH
             1926  END_FINALLY      
         1928_1930  JUMP_BACK          1856  'to 1856'
             1932  POP_BLOCK        
           1934_0  COME_FROM_LOOP     1848  '1848'
           1934_1  COME_FROM          1844  '1844'

 L. 206      1934  LOAD_FAST                'args'
             1936  LOAD_ATTR                target
         1938_1940  POP_JUMP_IF_FALSE  1982  'to 1982'

 L. 207      1942  SETUP_LOOP         1982  'to 1982'
             1944  LOAD_FAST                'args'
             1946  LOAD_ATTR                target
             1948  GET_ITER         
             1950  FOR_ITER           1980  'to 1980'
             1952  STORE_FAST               'targetentry'

 L. 208      1954  LOAD_GLOBAL              Target
             1956  LOAD_METHOD              from_line
             1958  LOAD_FAST                'targetentry'
             1960  CALL_METHOD_1         1  '1 positional argument'
             1962  STORE_FAST               'target'

 L. 209      1964  LOAD_FAST                'scan'
             1966  LOAD_ATTR                targets
             1968  LOAD_METHOD              append
             1970  LOAD_FAST                'target'
             1972  CALL_METHOD_1         1  '1 positional argument'
             1974  POP_TOP          
         1976_1978  JUMP_BACK          1950  'to 1950'
             1980  POP_BLOCK        
           1982_0  COME_FROM_LOOP     1942  '1942'
           1982_1  COME_FROM          1938  '1938'

 L. 211      1982  LOAD_FAST                'session'
             1984  LOAD_METHOD              add
             1986  LOAD_FAST                'scan'
             1988  CALL_METHOD_1         1  '1 positional argument'
             1990  POP_TOP          

 L. 212      1992  LOAD_FAST                'session'
             1994  LOAD_METHOD              commit
             1996  CALL_METHOD_0         0  '0 positional arguments'
             1998  POP_TOP          

 L. 213      2000  LOAD_FAST                'session'
             2002  LOAD_METHOD              query
             2004  LOAD_GLOBAL              Scan
             2006  CALL_METHOD_1         1  '1 positional argument'
             2008  LOAD_METHOD              get
             2010  LOAD_FAST                'scan'
             2012  LOAD_ATTR                id
             2014  CALL_METHOD_1         1  '1 positional argument'
             2016  STORE_FAST               'scan'

 L. 214      2018  LOAD_GLOBAL              SSLYZECommand
             2020  LOAD_ATTR                ALL
             2022  STORE_FAST               'c'

 L. 215      2024  LOAD_GLOBAL              ScanCommand
             2026  CALL_FUNCTION_0       0  '0 positional arguments'
             2028  STORE_FAST               'sc'

 L. 216      2030  LOAD_FAST                'scan'
             2032  LOAD_ATTR                id
             2034  LOAD_FAST                'sc'
             2036  STORE_ATTR               scan_id

 L. 217      2038  LOAD_FAST                'c'
             2040  LOAD_FAST                'sc'
             2042  STORE_ATTR               command

 L. 218      2044  LOAD_FAST                'session'
             2046  LOAD_METHOD              add
             2048  LOAD_FAST                'sc'
             2050  CALL_METHOD_1         1  '1 positional argument'
             2052  POP_TOP          

 L. 219      2054  LOAD_FAST                'session'
             2056  LOAD_METHOD              commit
             2058  CALL_METHOD_0         0  '0 positional arguments'
             2060  POP_TOP          

 L. 220      2062  LOAD_GLOBAL              logging
             2064  LOAD_METHOD              debug
             2066  LOAD_STR                 'Commands added'
             2068  CALL_METHOD_1         1  '1 positional argument'
             2070  POP_TOP          

 L. 221      2072  LOAD_GLOBAL              logging
             2074  LOAD_METHOD              debug
             2076  LOAD_STR                 'Starting scan'
             2078  CALL_METHOD_1         1  '1 positional argument'
             2080  POP_TOP          

 L. 223      2082  LOAD_GLOBAL              start_scanner
             2084  LOAD_FAST                'session'
             2086  LOAD_FAST                'scan'
             2088  LOAD_ATTR                id
             2090  LOAD_FAST                'args'
             2092  LOAD_ATTR                progress_bar
             2094  CALL_FUNCTION_3       3  '3 positional arguments'
             2096  POP_TOP          

 L. 224      2098  LOAD_GLOBAL              get_session
             2100  LOAD_FAST                'conn'
             2102  LOAD_FAST                'args'
             2104  LOAD_ATTR                verbose
             2106  CALL_FUNCTION_2       2  '2 positional arguments'
             2108  STORE_FAST               'session'

 L. 225      2110  LOAD_FAST                'session'
             2112  LOAD_METHOD              query
             2114  LOAD_GLOBAL              Scan
             2116  CALL_METHOD_1         1  '1 positional argument'
             2118  LOAD_METHOD              get
             2120  LOAD_FAST                'scan'
             2122  LOAD_ATTR                id
             2124  CALL_METHOD_1         1  '1 positional argument'
             2126  STORE_FAST               'scan'

 L. 226      2128  LOAD_GLOBAL              generate_report
             2130  LOAD_FAST                'session'
             2132  LOAD_FAST                'scan'
             2134  LOAD_ATTR                id
             2136  LOAD_FAST                'args'
             2138  LOAD_ATTR                full_report
             2140  CALL_FUNCTION_3       3  '3 positional arguments'
             2142  STORE_FAST               'data_lines'

 L. 227      2144  LOAD_FAST                'args'
             2146  LOAD_ATTR                outfile
             2148  LOAD_CONST               None
             2150  COMPARE_OP               is-not
         2152_2154  POP_JUMP_IF_FALSE  2222  'to 2222'

 L. 228      2156  LOAD_GLOBAL              open
             2158  LOAD_FAST                'args'
             2160  LOAD_ATTR                outfile
             2162  LOAD_STR                 'wb'
             2164  CALL_FUNCTION_2       2  '2 positional arguments'
             2166  SETUP_WITH         2214  'to 2214'
             2168  STORE_FAST               'f'

 L. 229      2170  SETUP_LOOP         2210  'to 2210'
             2172  LOAD_FAST                'data_lines'
             2174  GET_ITER         
             2176  FOR_ITER           2208  'to 2208'
             2178  STORE_FAST               'line'

 L. 230      2180  LOAD_FAST                'f'
             2182  LOAD_METHOD              write
             2184  LOAD_STR                 '\t'
             2186  LOAD_METHOD              join
             2188  LOAD_FAST                'line'
             2190  CALL_METHOD_1         1  '1 positional argument'
             2192  LOAD_METHOD              encode
             2194  CALL_METHOD_0         0  '0 positional arguments'
             2196  LOAD_CONST               b'\r\n'
             2198  BINARY_ADD       
             2200  CALL_METHOD_1         1  '1 positional argument'
             2202  POP_TOP          
         2204_2206  JUMP_BACK          2176  'to 2176'
             2208  POP_BLOCK        
           2210_0  COME_FROM_LOOP     2170  '2170'
             2210  POP_BLOCK        
             2212  LOAD_CONST               None
           2214_0  COME_FROM_WITH     2166  '2166'
             2214  WITH_CLEANUP_START
             2216  WITH_CLEANUP_FINISH
           2218_0  COME_FROM          1566  '1566'
             2218  END_FINALLY      
             2220  JUMP_FORWARD       2252  'to 2252'
           2222_0  COME_FROM          2152  '2152'

 L. 232      2222  SETUP_LOOP         2252  'to 2252'
             2224  LOAD_FAST                'data_lines'
             2226  GET_ITER         
             2228  FOR_ITER           2250  'to 2250'
             2230  STORE_FAST               'line'

 L. 233      2232  LOAD_GLOBAL              print
           2234_0  COME_FROM           724  '724'
             2234  LOAD_STR                 '\t'
             2236  LOAD_METHOD              join
             2238  LOAD_FAST                'line'
             2240  CALL_METHOD_1         1  '1 positional argument'
             2242  CALL_FUNCTION_1       1  '1 positional argument'
             2244  POP_TOP          
         2246_2248  JUMP_BACK          2228  'to 2228'
             2250  POP_BLOCK        
           2252_0  COME_FROM_LOOP     2222  '2222'
           2252_1  COME_FROM          2220  '2220'
           2252_2  COME_FROM          1610  '1610'
           2252_3  COME_FROM          1598  '1598'
           2252_4  COME_FROM          1428  '1428'
           2252_5  COME_FROM          1366  '1366'
           2252_6  COME_FROM          1226  '1226'
           2252_7  COME_FROM          1004  '1004'
           2252_8  COME_FROM           850  '850'
           2252_9  COME_FROM           740  '740'

Parse error at or near `COME_FROM' instruction at offset 2218_0


if __name__ == '__main__':
    run()