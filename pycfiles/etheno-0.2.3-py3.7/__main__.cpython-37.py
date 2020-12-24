# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/etheno/__main__.py
# Compiled at: 2019-06-27 23:49:12
# Size of source mod 2**32: 20458 bytes
import argparse, json, os, shlex, sys
from threading import Thread
from .client import RpcProxyClient
from .differentials import DifferentialTester
from .echidna import echidna_exists, EchidnaPlugin, install_echidna
from .etheno import app, EthenoView, GETH_DEFAULT_RPC_PORT, ETHENO, VERSION_NAME
from .genesis import Account, make_accounts, make_genesis
from .jsonrpc import EventSummaryExportPlugin, JSONRPCExportPlugin
from .synchronization import AddressSynchronizingClient, RawTransactionClient
from .utils import clear_directory, decode_value, find_open_port, format_hex_address, ynprompt
from . import ganache
from . import geth
from . import logger
from . import parity
from . import truffle
try:
    from .manticoreclient import ManticoreClient
    from . import manticoreutils
    MANTICORE_INSTALLED = True
except ModuleNotFoundError:
    MANTICORE_INSTALLED = False

def main--- This code section failed: ---

 L.  31         0  LOAD_GLOBAL              argparse
                2  LOAD_ATTR                ArgumentParser
                4  LOAD_STR                 'An Ethereum JSON RPC multiplexer and Manticore wrapper'
                6  LOAD_CONST               ('description',)
                8  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               10  STORE_FAST               'parser'

 L.  32        12  LOAD_FAST                'parser'
               14  LOAD_ATTR                add_argument
               16  LOAD_STR                 '--debug'
               18  LOAD_STR                 'store_true'
               20  LOAD_CONST               False
               22  LOAD_STR                 'Enable debugging from within the web server'
               24  LOAD_CONST               ('action', 'default', 'help')
               26  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
               28  POP_TOP          

 L.  33        30  LOAD_FAST                'parser'
               32  LOAD_ATTR                add_argument
               34  LOAD_STR                 '--run-publicly'
               36  LOAD_STR                 'store_true'
               38  LOAD_CONST               False
               40  LOAD_STR                 'Allow the web server to accept external connections'
               42  LOAD_CONST               ('action', 'default', 'help')
               44  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
               46  POP_TOP          

 L.  34        48  LOAD_FAST                'parser'
               50  LOAD_ATTR                add_argument
               52  LOAD_STR                 '-p'
               54  LOAD_STR                 '--port'
               56  LOAD_GLOBAL              int
               58  LOAD_GLOBAL              GETH_DEFAULT_RPC_PORT
               60  LOAD_STR                 'Port on which to run the JSON RPC webserver (default=%d)'
               62  LOAD_GLOBAL              GETH_DEFAULT_RPC_PORT
               64  BINARY_MODULO    
               66  LOAD_CONST               ('type', 'default', 'help')
               68  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
               70  POP_TOP          

 L.  35        72  LOAD_FAST                'parser'
               74  LOAD_ATTR                add_argument
               76  LOAD_STR                 '-a'
               78  LOAD_STR                 '--accounts'
               80  LOAD_GLOBAL              int
               82  LOAD_CONST               None
               84  LOAD_STR                 'Number of accounts to create in the client (default=10)'
               86  LOAD_CONST               ('type', 'default', 'help')
               88  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
               90  POP_TOP          

 L.  36        92  LOAD_FAST                'parser'
               94  LOAD_ATTR                add_argument
               96  LOAD_STR                 '-b'
               98  LOAD_STR                 '--balance'
              100  LOAD_GLOBAL              float
              102  LOAD_CONST               100.0
              104  LOAD_STR                 'Default balance (in Ether) to seed to each account (default=100.0)'
              106  LOAD_CONST               ('type', 'default', 'help')
              108  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              110  POP_TOP          

 L.  37       112  LOAD_FAST                'parser'
              114  LOAD_ATTR                add_argument
              116  LOAD_STR                 '-c'
              118  LOAD_STR                 '--gas-price'
              120  LOAD_GLOBAL              int
              122  LOAD_CONST               None
              124  LOAD_STR                 'Default gas price (default=20000000000)'
              126  LOAD_CONST               ('type', 'default', 'help')
              128  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              130  POP_TOP          

 L.  38       132  LOAD_FAST                'parser'
              134  LOAD_ATTR                add_argument
              136  LOAD_STR                 '-i'
              138  LOAD_STR                 '--network-id'
              140  LOAD_GLOBAL              int
              142  LOAD_CONST               None
              144  LOAD_STR                 'Specify a network ID (default is the network ID of the master client)'
              146  LOAD_CONST               ('type', 'default', 'help')
              148  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              150  POP_TOP          

 L.  39       152  LOAD_FAST                'parser'
              154  LOAD_ATTR                add_argument
              156  LOAD_STR                 '-m'
              158  LOAD_STR                 '--manticore'
              160  LOAD_STR                 'store_true'
              162  LOAD_CONST               False
              164  LOAD_STR                 'Run all transactions through manticore'
              166  LOAD_CONST               ('action', 'default', 'help')
              168  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              170  POP_TOP          

 L.  40       172  LOAD_FAST                'parser'
              174  LOAD_ATTR                add_argument
              176  LOAD_STR                 '-r'
              178  LOAD_STR                 '--manticore-script'
              180  LOAD_GLOBAL              argparse
              182  LOAD_METHOD              FileType
              184  LOAD_STR                 'rb'
              186  CALL_METHOD_1         1  '1 positional argument'
              188  LOAD_CONST               None
              190  LOAD_STR                 'Instead of running automated detectors and analyses, run this Manticore script'
              192  LOAD_CONST               ('type', 'default', 'help')
              194  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              196  POP_TOP          

 L.  41       198  LOAD_FAST                'parser'
              200  LOAD_ATTR                add_argument
              202  LOAD_STR                 '--manticore-max-depth'
              204  LOAD_GLOBAL              int
              206  LOAD_CONST               None
              208  LOAD_STR                 'Maximum state depth for Manticore to explore'
              210  LOAD_CONST               ('type', 'default', 'help')
              212  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              214  POP_TOP          

 L.  42       216  LOAD_FAST                'parser'
              218  LOAD_ATTR                add_argument
              220  LOAD_STR                 '-e'
              222  LOAD_STR                 '--echidna'
              224  LOAD_STR                 'store_true'
              226  LOAD_CONST               False
              228  LOAD_STR                 'Fuzz the clients using transactions generated by Echidna'
              230  LOAD_CONST               ('action', 'default', 'help')
              232  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              234  POP_TOP          

 L.  43       236  LOAD_FAST                'parser'
              238  LOAD_ATTR                add_argument
              240  LOAD_STR                 '--fuzz-limit'
              242  LOAD_GLOBAL              int
              244  LOAD_CONST               None
              246  LOAD_STR                 'The maximum number of transactions for Echidna to generate (default=unlimited)'
              248  LOAD_CONST               ('type', 'default', 'help')
              250  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              252  POP_TOP          

 L.  44       254  LOAD_FAST                'parser'
              256  LOAD_ATTR                add_argument
              258  LOAD_STR                 '--fuzz-contract'
              260  LOAD_GLOBAL              str
              262  LOAD_CONST               None
              264  LOAD_STR                 'Path to a Solidity contract to have Echidna use for fuzzing (default is to use a builtin generic Echidna fuzzing contract)'
              266  LOAD_CONST               ('type', 'default', 'help')
              268  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              270  POP_TOP          

 L.  45       272  LOAD_FAST                'parser'
              274  LOAD_ATTR                add_argument
              276  LOAD_STR                 '-t'
              278  LOAD_STR                 '--truffle'
              280  LOAD_STR                 'store_true'
              282  LOAD_CONST               False
              284  LOAD_STR                 'Run the truffle migrations in the current directory and exit'
              286  LOAD_CONST               ('action', 'default', 'help')
              288  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              290  POP_TOP          

 L.  46       292  LOAD_FAST                'parser'
              294  LOAD_ATTR                add_argument
              296  LOAD_STR                 '--truffle-cmd'
              298  LOAD_GLOBAL              str
              300  LOAD_STR                 'truffle'
              302  LOAD_STR                 'Command to run truffle (default=truffle)'
              304  LOAD_CONST               ('type', 'default', 'help')
              306  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              308  POP_TOP          

 L.  47       310  LOAD_FAST                'parser'
              312  LOAD_ATTR                add_argument
              314  LOAD_STR                 '--truffle-args'
              316  LOAD_GLOBAL              str
              318  LOAD_STR                 'migrate'
              320  LOAD_STR                 'Arguments to pass to truffle (default=migrate)'
              322  LOAD_CONST               ('type', 'default', 'help')
              324  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              326  POP_TOP          

 L.  48       328  LOAD_FAST                'parser'
              330  LOAD_ATTR                add_argument
              332  LOAD_STR                 '-g'
              334  LOAD_STR                 '--ganache'
              336  LOAD_STR                 'store_true'
              338  LOAD_CONST               False
              340  LOAD_STR                 'Run Ganache as a master JSON RPC client (cannot be used in conjunction with --master)'
              342  LOAD_CONST               ('action', 'default', 'help')
              344  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              346  POP_TOP          

 L.  49       348  LOAD_FAST                'parser'
              350  LOAD_ATTR                add_argument
              352  LOAD_STR                 '--ganache-args'
              354  LOAD_GLOBAL              str
              356  LOAD_CONST               None
              358  LOAD_STR                 'Additional arguments to pass to Ganache'
              360  LOAD_CONST               ('type', 'default', 'help')
              362  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              364  POP_TOP          

 L.  50       366  LOAD_FAST                'parser'
              368  LOAD_ATTR                add_argument
              370  LOAD_STR                 '--ganache-port'
              372  LOAD_GLOBAL              int
              374  LOAD_CONST               None
              376  LOAD_STR                 'Port on which to run Ganache (defaults to the closest available port to the port specified with --port plus one)'
              378  LOAD_CONST               ('type', 'default', 'help')
              380  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              382  POP_TOP          

 L.  51       384  LOAD_FAST                'parser'
              386  LOAD_ATTR                add_argument
              388  LOAD_STR                 '-go'
              390  LOAD_STR                 '--geth'
              392  LOAD_STR                 'store_true'
              394  LOAD_CONST               False
              396  LOAD_STR                 'Run Geth as a JSON RPC client'
              398  LOAD_CONST               ('action', 'default', 'help')
              400  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              402  POP_TOP          

 L.  52       404  LOAD_FAST                'parser'
              406  LOAD_ATTR                add_argument
              408  LOAD_STR                 '--geth-port'
              410  LOAD_GLOBAL              int
              412  LOAD_CONST               None
              414  LOAD_STR                 'Port on which to run Geth (defaults to the closest available port to the port specified with --port plus one)'
              416  LOAD_CONST               ('type', 'default', 'help')
              418  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              420  POP_TOP          

 L.  53       422  LOAD_FAST                'parser'
              424  LOAD_ATTR                add_argument
              426  LOAD_STR                 '-pa'
              428  LOAD_STR                 '--parity'
              430  LOAD_STR                 'store_true'
              432  LOAD_CONST               False
              434  LOAD_STR                 'Run Parity as a JSON RPC client'
              436  LOAD_CONST               ('action', 'default', 'help')
              438  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              440  POP_TOP          

 L.  54       442  LOAD_FAST                'parser'
              444  LOAD_ATTR                add_argument
              446  LOAD_STR                 '--parity-port'
              448  LOAD_GLOBAL              int
              450  LOAD_CONST               None
              452  LOAD_STR                 'Port on which to run Parity (defaults to the closest available port to the port specified with --port plus one)'
              454  LOAD_CONST               ('type', 'default', 'help')
              456  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              458  POP_TOP          

 L.  55       460  LOAD_FAST                'parser'
              462  LOAD_ATTR                add_argument
              464  LOAD_STR                 '-j'
              466  LOAD_STR                 '--genesis'
              468  LOAD_GLOBAL              str
              470  LOAD_CONST               None
              472  LOAD_STR                 'Path to a genesis.json file to use for initializing clients. Any genesis-related options like --network-id will override the values in this file. If --accounts is greater than zero, that many new accounts will be appended to the accounts in the genesis file.'
              474  LOAD_CONST               ('type', 'default', 'help')
              476  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              478  POP_TOP          

 L.  56       480  LOAD_FAST                'parser'
              482  LOAD_ATTR                add_argument
              484  LOAD_STR                 '--save-genesis'
              486  LOAD_GLOBAL              str
              488  LOAD_CONST               None
              490  LOAD_STR                 'Save a genesis.json file to reproduce the state of this run. Note that this genesis file will include all known private keys for the genesis accounts, so use this with caution.'
              492  LOAD_CONST               ('type', 'default', 'help')
              494  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              496  POP_TOP          

 L.  57       498  LOAD_FAST                'parser'
              500  LOAD_ATTR                add_argument
              502  LOAD_STR                 '--constantinople-block'
              504  LOAD_GLOBAL              int
              506  LOAD_CONST               None
              508  LOAD_STR                 'The block in which to enable Constantinople EIPs (default=do not enable Constantinople)'
              510  LOAD_CONST               ('type', 'default', 'help')
              512  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              514  POP_TOP          

 L.  58       516  LOAD_FAST                'parser'
              518  LOAD_ATTR                add_argument
              520  LOAD_STR                 '--constantinople'
              522  LOAD_STR                 'store_true'
              524  LOAD_CONST               False
              526  LOAD_STR                 'Enables Constantinople EIPs; equivalent to `--constantinople-block 0`'
              528  LOAD_CONST               ('action', 'default', 'help')
              530  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              532  POP_TOP          

 L.  59       534  LOAD_FAST                'parser'
              536  LOAD_ATTR                add_argument
              538  LOAD_STR                 '--no-differential-testing'
              540  LOAD_STR                 'store_false'
              542  LOAD_STR                 'run_differential'
              544  LOAD_CONST               True
              546  LOAD_STR                 'Do not run differential testing, which is run by default'
              548  LOAD_CONST               ('action', 'dest', 'default', 'help')
              550  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              552  POP_TOP          

 L.  60       554  LOAD_FAST                'parser'
              556  LOAD_ATTR                add_argument
              558  LOAD_STR                 '-l'
              560  LOAD_STR                 '--log-level'
              562  LOAD_GLOBAL              str
              564  LOAD_ATTR                upper
              566  LOAD_STR                 'CRITICAL'
              568  LOAD_STR                 'ERROR'
              570  LOAD_STR                 'WARNING'
              572  LOAD_STR                 'INFO'
              574  LOAD_STR                 'DEBUG'
              576  BUILD_SET_5           5 
              578  LOAD_STR                 'INFO'
              580  LOAD_STR                 "Set Etheno's log level (default=INFO)"
              582  LOAD_CONST               ('type', 'choices', 'default', 'help')
              584  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
              586  POP_TOP          

 L.  61       588  LOAD_FAST                'parser'
              590  LOAD_ATTR                add_argument
              592  LOAD_STR                 '--log-file'
              594  LOAD_GLOBAL              str
              596  LOAD_CONST               None
              598  LOAD_STR                 'Path to save all log output to a single file'
              600  LOAD_CONST               ('type', 'default', 'help')
              602  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              604  POP_TOP          

 L.  62       606  LOAD_FAST                'parser'
              608  LOAD_ATTR                add_argument
              610  LOAD_STR                 '--log-dir'
              612  LOAD_GLOBAL              str
              614  LOAD_CONST               None
              616  LOAD_STR                 'Path to a directory in which to save all log output, divided by logging source'
              618  LOAD_CONST               ('type', 'default', 'help')
              620  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              622  POP_TOP          

 L.  63       624  LOAD_FAST                'parser'
              626  LOAD_ATTR                add_argument
              628  LOAD_STR                 '-d'
              630  LOAD_STR                 '--dump-jsonrpc'
              632  LOAD_GLOBAL              str
              634  LOAD_CONST               None
              636  LOAD_STR                 'Path to a JSON file in which to dump all raw JSON RPC calls; if `--log-dir` is provided, the raw JSON RPC calls will additionally be dumped to `rpc.json` in the log directory.'
              638  LOAD_CONST               ('type', 'default', 'help')
              640  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              642  POP_TOP          

 L.  64       644  LOAD_FAST                'parser'
              646  LOAD_ATTR                add_argument
              648  LOAD_STR                 '-x'
              650  LOAD_STR                 '--export-summary'
              652  LOAD_GLOBAL              str
              654  LOAD_CONST               None
              656  LOAD_STR                 'Path to a JSON file in which to export an event summary'
              658  LOAD_CONST               ('type', 'default', 'help')
              660  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              662  POP_TOP          

 L.  65       664  LOAD_FAST                'parser'
              666  LOAD_ATTR                add_argument
              668  LOAD_STR                 '-v'
              670  LOAD_STR                 '--version'
              672  LOAD_STR                 'store_true'
              674  LOAD_CONST               False
              676  LOAD_STR                 'Print version information and exit'
              678  LOAD_CONST               ('action', 'default', 'help')
              680  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              682  POP_TOP          

 L.  66       684  LOAD_FAST                'parser'
              686  LOAD_ATTR                add_argument
              688  LOAD_STR                 'client'
              690  LOAD_GLOBAL              str
              692  LOAD_STR                 '*'
              694  LOAD_STR                 'JSON RPC client URLs to multiplex; if no client is specified for --master, the first client in this list will default to the master (format="http://foo.com:8545/")'
              696  LOAD_CONST               ('type', 'nargs', 'help')
              698  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              700  POP_TOP          

 L.  67       702  LOAD_FAST                'parser'
              704  LOAD_ATTR                add_argument
              706  LOAD_STR                 '-s'
              708  LOAD_STR                 '--master'
              710  LOAD_GLOBAL              str
              712  LOAD_CONST               None
              714  LOAD_STR                 'A JSON RPC client to use as the master (format="http://foo.com:8545/")'
              716  LOAD_CONST               ('type', 'default', 'help')
              718  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              720  POP_TOP          

 L.  68       722  LOAD_FAST                'parser'
              724  LOAD_ATTR                add_argument
              726  LOAD_STR                 '--raw'
              728  LOAD_GLOBAL              str
              730  LOAD_STR                 '*'
              732  LOAD_STR                 'append'
              734  LOAD_STR                 'JSON RPC client URLs to multiplex that do not have any local accounts; Etheno will automatically use auto-generated accounts with known private keys, pre-sign all transactions, and only use eth_sendRawTransaction'
              736  LOAD_CONST               ('type', 'nargs', 'action', 'help')
              738  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              740  POP_TOP          

 L.  70       742  LOAD_FAST                'argv'
              744  LOAD_CONST               None
              746  COMPARE_OP               is
          748_750  POP_JUMP_IF_FALSE   758  'to 758'

 L.  71       752  LOAD_GLOBAL              sys
              754  LOAD_ATTR                argv
              756  STORE_FAST               'argv'
            758_0  COME_FROM           748  '748'

 L.  73       758  LOAD_FAST                'parser'
              760  LOAD_METHOD              parse_args
              762  LOAD_FAST                'argv'
              764  LOAD_CONST               1
              766  LOAD_CONST               None
              768  BUILD_SLICE_2         2 
              770  BINARY_SUBSCR    
              772  CALL_METHOD_1         1  '1 positional argument'
              774  STORE_DEREF              'args'

 L.  75       776  LOAD_DEREF               'args'
              778  LOAD_ATTR                version
          780_782  POP_JUMP_IF_FALSE   802  'to 802'

 L.  76       784  LOAD_GLOBAL              print
              786  LOAD_GLOBAL              VERSION_NAME
              788  CALL_FUNCTION_1       1  '1 positional argument'
              790  POP_TOP          

 L.  77       792  LOAD_GLOBAL              sys
              794  LOAD_METHOD              exit
              796  LOAD_CONST               0
              798  CALL_METHOD_1         1  '1 positional argument'
              800  POP_TOP          
            802_0  COME_FROM           780  '780'

 L.  79       802  LOAD_DEREF               'args'
              804  LOAD_ATTR                constantinople
          806_808  POP_JUMP_IF_FALSE   828  'to 828'
              810  LOAD_DEREF               'args'
              812  LOAD_ATTR                constantinople_block
              814  LOAD_CONST               None
              816  COMPARE_OP               is
          818_820  POP_JUMP_IF_FALSE   828  'to 828'

 L.  80       822  LOAD_CONST               0
              824  LOAD_DEREF               'args'
              826  STORE_ATTR               constantinople_block
            828_0  COME_FROM           818  '818'
            828_1  COME_FROM           806  '806'

 L.  82       828  LOAD_DEREF               'args'
              830  LOAD_ATTR                log_level
              832  LOAD_GLOBAL              ETHENO
              834  STORE_ATTR               log_level

 L.  84       836  LOAD_DEREF               'args'
              838  LOAD_ATTR                log_file
          840_842  POP_JUMP_IF_FALSE   858  'to 858'

 L.  85       844  LOAD_GLOBAL              ETHENO
              846  LOAD_ATTR                logger
              848  LOAD_METHOD              save_to_file
              850  LOAD_DEREF               'args'
              852  LOAD_ATTR                log_file
              854  CALL_METHOD_1         1  '1 positional argument'
              856  POP_TOP          
            858_0  COME_FROM           840  '840'

 L.  87       858  LOAD_DEREF               'args'
              860  LOAD_ATTR                log_dir
          862_864  POP_JUMP_IF_FALSE  1128  'to 1128'

 L.  88       866  LOAD_GLOBAL              os
              868  LOAD_ATTR                path
              870  LOAD_METHOD              exists
              872  LOAD_DEREF               'args'
              874  LOAD_ATTR                log_dir
              876  CALL_METHOD_1         1  '1 positional argument'
          878_880  POP_JUMP_IF_FALSE  1056  'to 1056'

 L.  89       882  LOAD_GLOBAL              ynprompt
              884  LOAD_STR                 'Logging path `%s` already exists! Would you like to overwrite it? [yN] '
              886  LOAD_DEREF               'args'
              888  LOAD_ATTR                log_dir
              890  BINARY_MODULO    
              892  CALL_FUNCTION_1       1  '1 positional argument'
          894_896  POP_JUMP_IF_TRUE    910  'to 910'

 L.  90       898  LOAD_GLOBAL              sys
              900  LOAD_METHOD              exit
              902  LOAD_CONST               1
              904  CALL_METHOD_1         1  '1 positional argument'
              906  POP_TOP          
              908  JUMP_FORWARD       1056  'to 1056'
            910_0  COME_FROM           894  '894'

 L.  91       910  LOAD_GLOBAL              os
              912  LOAD_ATTR                path
              914  LOAD_METHOD              isfile
              916  LOAD_DEREF               'args'
              918  LOAD_ATTR                log_dir
              920  CALL_METHOD_1         1  '1 positional argument'
          922_924  POP_JUMP_IF_FALSE   940  'to 940'

 L.  92       926  LOAD_GLOBAL              os
              928  LOAD_METHOD              remove
              930  LOAD_DEREF               'args'
              932  LOAD_ATTR                log_dir
              934  CALL_METHOD_1         1  '1 positional argument'
              936  POP_TOP          
              938  JUMP_FORWARD       1056  'to 1056'
            940_0  COME_FROM           922  '922'

 L.  96       940  LOAD_GLOBAL              ynprompt
              942  LOAD_STR                 'We are about to delete the contents of `%s`. Are you sure? [yN] '
              944  LOAD_DEREF               'args'
              946  LOAD_ATTR                log_dir
              948  BINARY_MODULO    
              950  CALL_FUNCTION_1       1  '1 positional argument'
          952_954  POP_JUMP_IF_TRUE    966  'to 966'

 L.  97       956  LOAD_GLOBAL              sys
              958  LOAD_METHOD              exit
              960  LOAD_CONST               1
              962  CALL_METHOD_1         1  '1 positional argument'
              964  POP_TOP          
            966_0  COME_FROM           952  '952'

 L.  98       966  LOAD_GLOBAL              os
              968  LOAD_ATTR                path
              970  LOAD_METHOD              abspath
              972  LOAD_DEREF               'args'
              974  LOAD_ATTR                log_dir
              976  CALL_METHOD_1         1  '1 positional argument'
              978  STORE_FAST               'abspath'

 L.  99       980  LOAD_FAST                'abspath'
              982  LOAD_STR                 ''
              984  COMPARE_OP               ==
          986_988  POP_JUMP_IF_TRUE   1024  'to 1024'
              990  LOAD_FAST                'abspath'
              992  LOAD_STR                 '/'
              994  COMPARE_OP               ==
          996_998  POP_JUMP_IF_TRUE   1024  'to 1024'
             1000  LOAD_FAST                'abspath'
             1002  LOAD_METHOD              endswith
             1004  LOAD_STR                 '://'
             1006  CALL_METHOD_1         1  '1 positional argument'
         1008_1010  POP_JUMP_IF_TRUE   1024  'to 1024'
             1012  LOAD_FAST                'abspath'
             1014  LOAD_METHOD              endswith
             1016  LOAD_STR                 ':\\\\'
             1018  CALL_METHOD_1         1  '1 positional argument'
         1020_1022  POP_JUMP_IF_FALSE  1046  'to 1046'
           1024_0  COME_FROM          1008  '1008'
           1024_1  COME_FROM           996  '996'
           1024_2  COME_FROM           986  '986'

 L. 100      1024  LOAD_GLOBAL              print
             1026  LOAD_STR                 "Wait a sec, you want me to delete `%s`?!\nThat looks too dangerous.\nIf I were to do that, you'd file an angry GitHub issue complaining that I deleted your hard drive.\nYou're on your own deleting this directory!"
             1028  LOAD_FAST                'abspath'
             1030  BINARY_MODULO    
             1032  CALL_FUNCTION_1       1  '1 positional argument'
             1034  POP_TOP          

 L. 101      1036  LOAD_GLOBAL              sys
             1038  LOAD_METHOD              exit
             1040  LOAD_CONST               1
             1042  CALL_METHOD_1         1  '1 positional argument'
             1044  POP_TOP          
           1046_0  COME_FROM          1020  '1020'

 L. 102      1046  LOAD_GLOBAL              clear_directory
             1048  LOAD_DEREF               'args'
             1050  LOAD_ATTR                log_dir
             1052  CALL_FUNCTION_1       1  '1 positional argument'
             1054  POP_TOP          
           1056_0  COME_FROM           938  '938'
           1056_1  COME_FROM           908  '908'
           1056_2  COME_FROM           878  '878'

 L. 104      1056  LOAD_GLOBAL              ETHENO
             1058  LOAD_ATTR                logger
             1060  LOAD_METHOD              save_to_directory
             1062  LOAD_DEREF               'args'
             1064  LOAD_ATTR                log_dir
             1066  CALL_METHOD_1         1  '1 positional argument'
             1068  POP_TOP          

 L. 105      1070  LOAD_DEREF               'args'
             1072  LOAD_ATTR                log_file
         1074_1076  POP_JUMP_IF_TRUE   1102  'to 1102'

 L. 107      1078  LOAD_GLOBAL              ETHENO
             1080  LOAD_ATTR                logger
             1082  LOAD_METHOD              save_to_file
             1084  LOAD_GLOBAL              os
             1086  LOAD_ATTR                path
             1088  LOAD_METHOD              join
             1090  LOAD_DEREF               'args'
             1092  LOAD_ATTR                log_dir
             1094  LOAD_STR                 'Complete.log'
             1096  CALL_METHOD_2         2  '2 positional arguments'
             1098  CALL_METHOD_1         1  '1 positional argument'
             1100  POP_TOP          
           1102_0  COME_FROM          1074  '1074'

 L. 109      1102  LOAD_GLOBAL              ETHENO
             1104  LOAD_METHOD              add_plugin
             1106  LOAD_GLOBAL              JSONRPCExportPlugin
             1108  LOAD_GLOBAL              os
             1110  LOAD_ATTR                path
             1112  LOAD_METHOD              join
             1114  LOAD_DEREF               'args'
             1116  LOAD_ATTR                log_dir
             1118  LOAD_STR                 'rpc.json'
             1120  CALL_METHOD_2         2  '2 positional arguments'
             1122  CALL_FUNCTION_1       1  '1 positional argument'
             1124  CALL_METHOD_1         1  '1 positional argument'
             1126  POP_TOP          
           1128_0  COME_FROM           862  '862'

 L. 111      1128  LOAD_DEREF               'args'
             1130  LOAD_ATTR                dump_jsonrpc
             1132  LOAD_CONST               None
             1134  COMPARE_OP               is-not
         1136_1138  POP_JUMP_IF_FALSE  1156  'to 1156'

 L. 112      1140  LOAD_GLOBAL              ETHENO
             1142  LOAD_METHOD              add_plugin
             1144  LOAD_GLOBAL              JSONRPCExportPlugin
             1146  LOAD_DEREF               'args'
             1148  LOAD_ATTR                dump_jsonrpc
             1150  CALL_FUNCTION_1       1  '1 positional argument'
             1152  CALL_METHOD_1         1  '1 positional argument'
             1154  POP_TOP          
           1156_0  COME_FROM          1136  '1136'

 L. 114      1156  LOAD_DEREF               'args'
             1158  LOAD_ATTR                export_summary
             1160  LOAD_CONST               None
             1162  COMPARE_OP               is-not
         1164_1166  POP_JUMP_IF_FALSE  1184  'to 1184'

 L. 115      1168  LOAD_GLOBAL              ETHENO
             1170  LOAD_METHOD              add_plugin
             1172  LOAD_GLOBAL              EventSummaryExportPlugin
             1174  LOAD_DEREF               'args'
             1176  LOAD_ATTR                export_summary
             1178  CALL_FUNCTION_1       1  '1 positional argument'
             1180  CALL_METHOD_1         1  '1 positional argument'
             1182  POP_TOP          
           1184_0  COME_FROM          1164  '1164'

 L. 118      1184  LOAD_DEREF               'args'
             1186  LOAD_ATTR                echidna
         1188_1190  POP_JUMP_IF_FALSE  1256  'to 1256'

 L. 119      1192  LOAD_GLOBAL              echidna_exists
             1194  CALL_FUNCTION_0       0  '0 positional arguments'
         1196_1198  POP_JUMP_IF_TRUE   1256  'to 1256'

 L. 120      1200  LOAD_GLOBAL              ynprompt
             1202  LOAD_STR                 'Echidna does not appear to be installed.\nWould you like to have Etheno attempt to install it now? [yN] '
             1204  CALL_FUNCTION_1       1  '1 positional argument'
         1206_1208  POP_JUMP_IF_TRUE   1220  'to 1220'

 L. 121      1210  LOAD_GLOBAL              sys
             1212  LOAD_METHOD              exit
             1214  LOAD_CONST               1
             1216  CALL_METHOD_1         1  '1 positional argument'
             1218  POP_TOP          
           1220_0  COME_FROM          1206  '1206'

 L. 122      1220  LOAD_GLOBAL              install_echidna
             1222  CALL_FUNCTION_0       0  '0 positional arguments'
             1224  POP_TOP          

 L. 123      1226  LOAD_GLOBAL              echidna_exists
             1228  CALL_FUNCTION_0       0  '0 positional arguments'
         1230_1232  POP_JUMP_IF_TRUE   1256  'to 1256'

 L. 124      1234  LOAD_GLOBAL              ETHENO
             1236  LOAD_ATTR                logger
             1238  LOAD_METHOD              error
             1240  LOAD_STR                 'Etheno failed to install Echidna. Please install it manually https://github.com/trailofbits/echidna'
             1242  CALL_METHOD_1         1  '1 positional argument'
             1244  POP_TOP          

 L. 125      1246  LOAD_GLOBAL              sys
             1248  LOAD_METHOD              exit
             1250  LOAD_CONST               1
             1252  CALL_METHOD_1         1  '1 positional argument'
             1254  POP_TOP          
           1256_0  COME_FROM          1230  '1230'
           1256_1  COME_FROM          1196  '1196'
           1256_2  COME_FROM          1188  '1188'

 L. 127      1256  LOAD_DEREF               'args'
             1258  LOAD_ATTR                genesis
             1260  LOAD_CONST               None
             1262  COMPARE_OP               is
         1264_1266  POP_JUMP_IF_FALSE  1304  'to 1304'

 L. 129      1268  LOAD_DEREF               'args'
             1270  LOAD_ATTR                accounts
             1272  LOAD_CONST               None
             1274  COMPARE_OP               is
         1276_1278  POP_JUMP_IF_FALSE  1286  'to 1286'

 L. 130      1280  LOAD_CONST               10
             1282  LOAD_DEREF               'args'
             1284  STORE_ATTR               accounts
           1286_0  COME_FROM          1276  '1276'

 L. 131      1286  LOAD_DEREF               'args'
             1288  LOAD_ATTR                gas_price
             1290  LOAD_CONST               None
             1292  COMPARE_OP               is
         1294_1296  POP_JUMP_IF_FALSE  1304  'to 1304'

 L. 132      1298  LOAD_CONST               20000000000
             1300  LOAD_DEREF               'args'
             1302  STORE_ATTR               gas_price
           1304_0  COME_FROM          1294  '1294'
           1304_1  COME_FROM          1264  '1264'

 L. 134      1304  BUILD_LIST_0          0 
             1306  STORE_FAST               'accounts'

 L. 136      1308  LOAD_DEREF               'args'
             1310  LOAD_ATTR                genesis
         1312_1314  POP_JUMP_IF_FALSE  1548  'to 1548'

 L. 137      1316  LOAD_GLOBAL              open
             1318  LOAD_DEREF               'args'
             1320  LOAD_ATTR                genesis
             1322  LOAD_STR                 'rb'
             1324  CALL_FUNCTION_2       2  '2 positional arguments'
             1326  SETUP_WITH         1540  'to 1540'
             1328  STORE_FAST               'f'

 L. 138      1330  LOAD_GLOBAL              json
             1332  LOAD_METHOD              load
             1334  LOAD_FAST                'f'
             1336  CALL_METHOD_1         1  '1 positional argument'
             1338  STORE_FAST               'genesis'

 L. 139      1340  LOAD_STR                 'config'
             1342  LOAD_FAST                'genesis'
             1344  COMPARE_OP               not-in
         1346_1348  POP_JUMP_IF_FALSE  1358  'to 1358'

 L. 140      1350  BUILD_MAP_0           0 
             1352  LOAD_FAST                'genesis'
             1354  LOAD_STR                 'config'
             1356  STORE_SUBSCR     
           1358_0  COME_FROM          1346  '1346'

 L. 141      1358  LOAD_STR                 'alloc'
             1360  LOAD_FAST                'genesis'
             1362  COMPARE_OP               not-in
         1364_1366  POP_JUMP_IF_FALSE  1376  'to 1376'

 L. 142      1368  BUILD_MAP_0           0 
             1370  LOAD_FAST                'genesis'
             1372  LOAD_STR                 'alloc'
             1374  STORE_SUBSCR     
           1376_0  COME_FROM          1364  '1364'

 L. 143      1376  LOAD_DEREF               'args'
             1378  LOAD_ATTR                network_id
             1380  LOAD_CONST               None
             1382  COMPARE_OP               is
         1384_1386  POP_JUMP_IF_FALSE  1406  'to 1406'

 L. 144      1388  LOAD_FAST                'genesis'
             1390  LOAD_STR                 'config'
             1392  BINARY_SUBSCR    
             1394  LOAD_METHOD              get
             1396  LOAD_STR                 'chainId'
             1398  LOAD_CONST               None
             1400  CALL_METHOD_2         2  '2 positional arguments'
             1402  LOAD_DEREF               'args'
             1404  STORE_ATTR               network_id
           1406_0  COME_FROM          1384  '1384'

 L. 145      1406  LOAD_DEREF               'args'
             1408  LOAD_ATTR                constantinople_block
             1410  LOAD_CONST               None
             1412  COMPARE_OP               is
         1414_1416  POP_JUMP_IF_FALSE  1448  'to 1448'

 L. 146      1418  LOAD_FAST                'genesis'
             1420  LOAD_STR                 'config'
             1422  BINARY_SUBSCR    
             1424  LOAD_METHOD              get
             1426  LOAD_STR                 'constantinopleBlock'
             1428  LOAD_CONST               None
             1430  CALL_METHOD_2         2  '2 positional arguments'
             1432  LOAD_DEREF               'args'
             1434  STORE_ATTR               constantinople_block

 L. 147      1436  LOAD_DEREF               'args'
             1438  LOAD_ATTR                constantinople_block
             1440  LOAD_CONST               None
             1442  COMPARE_OP               is-not
             1444  LOAD_DEREF               'args'
             1446  STORE_ATTR               constantinople
           1448_0  COME_FROM          1414  '1414'

 L. 148      1448  SETUP_LOOP         1536  'to 1536'
             1450  LOAD_FAST                'genesis'
             1452  LOAD_STR                 'alloc'
             1454  BINARY_SUBSCR    
             1456  LOAD_METHOD              items
             1458  CALL_METHOD_0         0  '0 positional arguments'
             1460  GET_ITER         
             1462  FOR_ITER           1534  'to 1534'
             1464  UNPACK_SEQUENCE_2     2 
             1466  STORE_FAST               'addr'
             1468  STORE_FAST               'bal'

 L. 149      1470  LOAD_CONST               None
             1472  STORE_FAST               'pkey'

 L. 150      1474  LOAD_STR                 'privateKey'
             1476  LOAD_FAST                'bal'
             1478  COMPARE_OP               in
         1480_1482  POP_JUMP_IF_FALSE  1492  'to 1492'

 L. 151      1484  LOAD_FAST                'bal'
             1486  LOAD_STR                 'privateKey'
             1488  BINARY_SUBSCR    
             1490  STORE_FAST               'pkey'
           1492_0  COME_FROM          1480  '1480'

 L. 152      1492  LOAD_FAST                'accounts'
             1494  LOAD_METHOD              append
             1496  LOAD_GLOBAL              Account
             1498  LOAD_GLOBAL              int
             1500  LOAD_FAST                'addr'
             1502  LOAD_CONST               16
             1504  CALL_FUNCTION_2       2  '2 positional arguments'
             1506  LOAD_GLOBAL              decode_value
             1508  LOAD_FAST                'bal'
             1510  LOAD_STR                 'balance'
             1512  BINARY_SUBSCR    
             1514  CALL_FUNCTION_1       1  '1 positional argument'
             1516  LOAD_GLOBAL              decode_value
             1518  LOAD_FAST                'pkey'
             1520  CALL_FUNCTION_1       1  '1 positional argument'
             1522  LOAD_CONST               ('address', 'balance', 'private_key')
             1524  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
             1526  CALL_METHOD_1         1  '1 positional argument'
             1528  POP_TOP          
         1530_1532  JUMP_BACK          1462  'to 1462'
             1534  POP_BLOCK        
           1536_0  COME_FROM_LOOP     1448  '1448'
             1536  POP_BLOCK        
             1538  LOAD_CONST               None
           1540_0  COME_FROM_WITH     1326  '1326'
             1540  WITH_CLEANUP_START
             1542  WITH_CLEANUP_FINISH
             1544  END_FINALLY      
             1546  JUMP_FORWARD       1552  'to 1552'
           1548_0  COME_FROM          1312  '1312'

 L. 155      1548  LOAD_CONST               None
             1550  STORE_FAST               'genesis'
           1552_0  COME_FROM          1546  '1546'

 L. 157      1552  LOAD_FAST                'accounts'
             1554  LOAD_GLOBAL              make_accounts
             1556  LOAD_DEREF               'args'
             1558  LOAD_ATTR                accounts
             1560  LOAD_GLOBAL              int
             1562  LOAD_DEREF               'args'
             1564  LOAD_ATTR                balance
             1566  LOAD_CONST               1000000000000000000
             1568  BINARY_MULTIPLY  
             1570  CALL_FUNCTION_1       1  '1 positional argument'
             1572  LOAD_CONST               ('default_balance',)
             1574  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1576  INPLACE_ADD      
             1578  STORE_FAST               'accounts'

 L. 159      1580  LOAD_FAST                'genesis'
             1582  LOAD_CONST               None
             1584  COMPARE_OP               is-not
         1586_1588  POP_JUMP_IF_FALSE  1660  'to 1660'

 L. 161      1590  SETUP_LOOP         1660  'to 1660'
             1592  LOAD_FAST                'accounts'
             1594  LOAD_GLOBAL              len
             1596  LOAD_FAST                'genesis'
             1598  LOAD_STR                 'alloc'
             1600  BINARY_SUBSCR    
             1602  CALL_FUNCTION_1       1  '1 positional argument'
             1604  LOAD_CONST               None
             1606  BUILD_SLICE_2         2 
             1608  BINARY_SUBSCR    
             1610  GET_ITER         
             1612  FOR_ITER           1658  'to 1658'
             1614  STORE_FAST               'account'

 L. 162      1616  LOAD_STR                 '%d'
             1618  LOAD_FAST                'account'
             1620  LOAD_ATTR                balance
             1622  BINARY_MODULO    
             1624  LOAD_GLOBAL              format_hex_address
             1626  LOAD_FAST                'account'
             1628  LOAD_ATTR                private_key
             1630  CALL_FUNCTION_1       1  '1 positional argument'
             1632  LOAD_STR                 '`privateKey` and `comment` are ignored.  In a real chain, the private key should _not_ be stored!'
             1634  LOAD_CONST               ('balance', 'privateKey', 'comment')
             1636  BUILD_CONST_KEY_MAP_3     3 
             1638  LOAD_FAST                'genesis'
             1640  LOAD_STR                 'alloc'
             1642  BINARY_SUBSCR    
             1644  LOAD_GLOBAL              format_hex_address
             1646  LOAD_FAST                'account'
             1648  LOAD_ATTR                address
             1650  CALL_FUNCTION_1       1  '1 positional argument'
             1652  STORE_SUBSCR     
         1654_1656  JUMP_BACK          1612  'to 1612'
             1658  POP_BLOCK        
           1660_0  COME_FROM_LOOP     1590  '1590'
           1660_1  COME_FROM          1586  '1586'

 L. 164      1660  LOAD_DEREF               'args'
             1662  LOAD_ATTR                raw
             1664  LOAD_CONST               None
             1666  COMPARE_OP               is
         1668_1670  POP_JUMP_IF_FALSE  1680  'to 1680'

 L. 165      1672  BUILD_LIST_0          0 
             1674  LOAD_DEREF               'args'
             1676  STORE_ATTR               raw
             1678  JUMP_FORWARD       1698  'to 1698'
           1680_0  COME_FROM          1668  '1668'

 L. 167      1680  LOAD_LISTCOMP            '<code_object <listcomp>>'
             1682  LOAD_STR                 'main.<locals>.<listcomp>'
             1684  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
             1686  LOAD_DEREF               'args'
             1688  LOAD_ATTR                raw
             1690  GET_ITER         
             1692  CALL_FUNCTION_1       1  '1 positional argument'
             1694  LOAD_DEREF               'args'
             1696  STORE_ATTR               raw
           1698_0  COME_FROM          1678  '1678'

 L. 169      1698  LOAD_DEREF               'args'
             1700  LOAD_ATTR                ganache
         1702_1704  POP_JUMP_IF_FALSE  1748  'to 1748'
             1706  LOAD_DEREF               'args'
             1708  LOAD_ATTR                master
         1710_1712  POP_JUMP_IF_FALSE  1748  'to 1748'

 L. 170      1714  LOAD_FAST                'parser'
             1716  LOAD_METHOD              print_help
             1718  CALL_METHOD_0         0  '0 positional arguments'
             1720  POP_TOP          

 L. 171      1722  LOAD_GLOBAL              sys
             1724  LOAD_ATTR                stderr
             1726  LOAD_METHOD              write
             1728  LOAD_STR                 '\nError: You cannot specify both --ganache and --master at the same time!\n'
             1730  CALL_METHOD_1         1  '1 positional argument'
             1732  POP_TOP          

 L. 172      1734  LOAD_GLOBAL              sys
             1736  LOAD_METHOD              exit
             1738  LOAD_CONST               1
             1740  CALL_METHOD_1         1  '1 positional argument'
             1742  POP_TOP          
         1744_1746  JUMP_FORWARD       2060  'to 2060'
           1748_0  COME_FROM          1710  '1710'
           1748_1  COME_FROM          1702  '1702'

 L. 173      1748  LOAD_DEREF               'args'
             1750  LOAD_ATTR                ganache
         1752_1754  POP_JUMP_IF_FALSE  1910  'to 1910'

 L. 174      1756  LOAD_DEREF               'args'
             1758  LOAD_ATTR                ganache_port
             1760  LOAD_CONST               None
             1762  COMPARE_OP               is
         1764_1766  POP_JUMP_IF_FALSE  1784  'to 1784'

 L. 175      1768  LOAD_GLOBAL              find_open_port
             1770  LOAD_DEREF               'args'
             1772  LOAD_ATTR                port
             1774  LOAD_CONST               1
             1776  BINARY_ADD       
             1778  CALL_FUNCTION_1       1  '1 positional argument'
             1780  LOAD_DEREF               'args'
             1782  STORE_ATTR               ganache_port
           1784_0  COME_FROM          1764  '1764'

 L. 177      1784  LOAD_DEREF               'args'
             1786  LOAD_ATTR                network_id
             1788  LOAD_CONST               None
             1790  COMPARE_OP               is
         1792_1794  POP_JUMP_IF_FALSE  1802  'to 1802'

 L. 178      1796  LOAD_CONST               111550642089583
             1798  LOAD_DEREF               'args'
             1800  STORE_ATTR               network_id
           1802_0  COME_FROM          1792  '1792'

 L. 180      1802  LOAD_LISTCOMP            '<code_object <listcomp>>'
             1804  LOAD_STR                 'main.<locals>.<listcomp>'
             1806  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
             1808  LOAD_FAST                'accounts'
             1810  GET_ITER         
             1812  CALL_FUNCTION_1       1  '1 positional argument'
             1814  STORE_FAST               'ganache_accounts'

 L. 182      1816  LOAD_FAST                'ganache_accounts'
             1818  LOAD_STR                 '-g'
             1820  LOAD_GLOBAL              str
             1822  LOAD_DEREF               'args'
             1824  LOAD_ATTR                gas_price
             1826  CALL_FUNCTION_1       1  '1 positional argument'
             1828  LOAD_STR                 '-i'
             1830  LOAD_GLOBAL              str
             1832  LOAD_DEREF               'args'
             1834  LOAD_ATTR                network_id
             1836  CALL_FUNCTION_1       1  '1 positional argument'
             1838  BUILD_LIST_4          4 
             1840  BINARY_ADD       
             1842  STORE_FAST               'ganache_args'

 L. 184      1844  LOAD_DEREF               'args'
             1846  LOAD_ATTR                ganache_args
             1848  LOAD_CONST               None
             1850  COMPARE_OP               is-not
         1852_1854  POP_JUMP_IF_FALSE  1872  'to 1872'

 L. 185      1856  LOAD_FAST                'ganache_args'
             1858  LOAD_GLOBAL              shlex
             1860  LOAD_METHOD              split
             1862  LOAD_DEREF               'args'
             1864  LOAD_ATTR                ganache_args
             1866  CALL_METHOD_1         1  '1 positional argument'
             1868  INPLACE_ADD      
             1870  STORE_FAST               'ganache_args'
           1872_0  COME_FROM          1852  '1852'

 L. 187      1872  LOAD_GLOBAL              ganache
             1874  LOAD_ATTR                Ganache
             1876  LOAD_FAST                'ganache_args'
             1878  LOAD_DEREF               'args'
             1880  LOAD_ATTR                ganache_port
             1882  LOAD_CONST               ('args', 'port')
             1884  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1886  STORE_FAST               'ganache_instance'

 L. 189      1888  LOAD_GLOBAL              ganache
             1890  LOAD_METHOD              GanacheClient
             1892  LOAD_FAST                'ganache_instance'
             1894  CALL_METHOD_1         1  '1 positional argument'
             1896  LOAD_GLOBAL              ETHENO
             1898  STORE_ATTR               master_client

 L. 191      1900  LOAD_FAST                'ganache_instance'
             1902  LOAD_METHOD              start
             1904  CALL_METHOD_0         0  '0 positional arguments'
             1906  POP_TOP          
             1908  JUMP_FORWARD       2060  'to 2060'
           1910_0  COME_FROM          1752  '1752'

 L. 192      1910  LOAD_DEREF               'args'
             1912  LOAD_ATTR                master
         1914_1916  POP_JUMP_IF_FALSE  1936  'to 1936'

 L. 193      1918  LOAD_GLOBAL              AddressSynchronizingClient
             1920  LOAD_GLOBAL              RpcProxyClient
             1922  LOAD_DEREF               'args'
             1924  LOAD_ATTR                master
             1926  CALL_FUNCTION_1       1  '1 positional argument'
             1928  CALL_FUNCTION_1       1  '1 positional argument'
             1930  LOAD_GLOBAL              ETHENO
             1932  STORE_ATTR               master_client
             1934  JUMP_FORWARD       2060  'to 2060'
           1936_0  COME_FROM          1914  '1914'

 L. 194      1936  LOAD_DEREF               'args'
             1938  LOAD_ATTR                client
         1940_1942  POP_JUMP_IF_FALSE  1998  'to 1998'
             1944  LOAD_DEREF               'args'
             1946  LOAD_ATTR                geth
         1948_1950  POP_JUMP_IF_TRUE   1998  'to 1998'
             1952  LOAD_DEREF               'args'
             1954  LOAD_ATTR                parity
         1956_1958  POP_JUMP_IF_TRUE   1998  'to 1998'

 L. 195      1960  LOAD_GLOBAL              AddressSynchronizingClient
             1962  LOAD_GLOBAL              RpcProxyClient
             1964  LOAD_DEREF               'args'
             1966  LOAD_ATTR                client
             1968  LOAD_CONST               0
             1970  BINARY_SUBSCR    
             1972  CALL_FUNCTION_1       1  '1 positional argument'
             1974  CALL_FUNCTION_1       1  '1 positional argument'
             1976  LOAD_GLOBAL              ETHENO
             1978  STORE_ATTR               master_client

 L. 196      1980  LOAD_DEREF               'args'
             1982  LOAD_ATTR                client
             1984  LOAD_CONST               1
             1986  LOAD_CONST               None
             1988  BUILD_SLICE_2         2 
             1990  BINARY_SUBSCR    
             1992  LOAD_DEREF               'args'
             1994  STORE_ATTR               client
             1996  JUMP_FORWARD       2060  'to 2060'
           1998_0  COME_FROM          1956  '1956'
           1998_1  COME_FROM          1948  '1948'
           1998_2  COME_FROM          1940  '1940'

 L. 197      1998  LOAD_DEREF               'args'
             2000  LOAD_ATTR                raw
         2002_2004  POP_JUMP_IF_FALSE  2060  'to 2060'
             2006  LOAD_DEREF               'args'
             2008  LOAD_ATTR                geth
         2010_2012  POP_JUMP_IF_TRUE   2060  'to 2060'
             2014  LOAD_DEREF               'args'
             2016  LOAD_ATTR                parity
         2018_2020  POP_JUMP_IF_TRUE   2060  'to 2060'

 L. 198      2022  LOAD_GLOBAL              RawTransactionClient
             2024  LOAD_GLOBAL              RpcProxyClient
             2026  LOAD_DEREF               'args'
             2028  LOAD_ATTR                raw
             2030  LOAD_CONST               0
             2032  BINARY_SUBSCR    
             2034  CALL_FUNCTION_1       1  '1 positional argument'
             2036  LOAD_FAST                'accounts'
             2038  CALL_FUNCTION_2       2  '2 positional arguments'
             2040  LOAD_GLOBAL              ETHENO
             2042  STORE_ATTR               master_client

 L. 199      2044  LOAD_DEREF               'args'
             2046  LOAD_ATTR                raw
             2048  LOAD_CONST               1
             2050  LOAD_CONST               None
             2052  BUILD_SLICE_2         2 
             2054  BINARY_SUBSCR    
             2056  LOAD_DEREF               'args'
             2058  STORE_ATTR               raw
           2060_0  COME_FROM          2018  '2018'
           2060_1  COME_FROM          2010  '2010'
           2060_2  COME_FROM          2002  '2002'
           2060_3  COME_FROM          1996  '1996'
           2060_4  COME_FROM          1934  '1934'
           2060_5  COME_FROM          1908  '1908'
           2060_6  COME_FROM          1744  '1744'

 L. 201      2060  LOAD_DEREF               'args'
             2062  LOAD_ATTR                network_id
             2064  LOAD_CONST               None
             2066  COMPARE_OP               is
         2068_2070  POP_JUMP_IF_FALSE  2120  'to 2120'

 L. 202      2072  LOAD_GLOBAL              ETHENO
             2074  LOAD_ATTR                master_client
         2076_2078  POP_JUMP_IF_FALSE  2114  'to 2114'

 L. 203      2080  LOAD_GLOBAL              int
             2082  LOAD_GLOBAL              ETHENO
             2084  LOAD_ATTR                master_client
             2086  LOAD_METHOD              post

 L. 204      2088  LOAD_CONST               1

 L. 205      2090  LOAD_STR                 '2.0'

 L. 206      2092  LOAD_STR                 'net_version'
             2094  LOAD_CONST               ('id', 'jsonrpc', 'method')
             2096  BUILD_CONST_KEY_MAP_3     3 
             2098  CALL_METHOD_1         1  '1 positional argument'

 L. 207      2100  LOAD_STR                 'result'
             2102  BINARY_SUBSCR    
             2104  LOAD_CONST               16
             2106  CALL_FUNCTION_2       2  '2 positional arguments'
             2108  LOAD_DEREF               'args'
             2110  STORE_ATTR               network_id
             2112  JUMP_FORWARD       2120  'to 2120'
           2114_0  COME_FROM          2076  '2076'

 L. 209      2114  LOAD_CONST               111550642089583
             2116  LOAD_DEREF               'args'
             2118  STORE_ATTR               network_id
           2120_0  COME_FROM          2112  '2112'
           2120_1  COME_FROM          2068  '2068'

 L. 211      2120  LOAD_FAST                'genesis'
             2122  LOAD_CONST               None
             2124  COMPARE_OP               is
         2126_2128  POP_JUMP_IF_FALSE  2150  'to 2150'

 L. 212      2130  LOAD_GLOBAL              make_genesis
             2132  LOAD_DEREF               'args'
             2134  LOAD_ATTR                network_id
             2136  LOAD_FAST                'accounts'
             2138  LOAD_DEREF               'args'
             2140  LOAD_ATTR                constantinople_block
             2142  LOAD_CONST               ('network_id', 'accounts', 'constantinople_block')
             2144  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
             2146  STORE_FAST               'genesis'
             2148  JUMP_FORWARD       2164  'to 2164'
           2150_0  COME_FROM          2126  '2126'

 L. 215      2150  LOAD_DEREF               'args'
             2152  LOAD_ATTR                network_id
             2154  LOAD_FAST                'genesis'
             2156  LOAD_STR                 'config'
             2158  BINARY_SUBSCR    
             2160  LOAD_STR                 'chainId'
             2162  STORE_SUBSCR     
           2164_0  COME_FROM          2148  '2148'

 L. 217      2164  LOAD_DEREF               'args'
             2166  LOAD_ATTR                save_genesis
         2168_2170  POP_JUMP_IF_FALSE  2236  'to 2236'

 L. 218      2172  LOAD_GLOBAL              open
             2174  LOAD_DEREF               'args'
             2176  LOAD_ATTR                save_genesis
             2178  LOAD_STR                 'wb'
             2180  CALL_FUNCTION_2       2  '2 positional arguments'
             2182  SETUP_WITH         2230  'to 2230'
             2184  STORE_FAST               'f'

 L. 219      2186  LOAD_FAST                'f'
             2188  LOAD_METHOD              write
             2190  LOAD_GLOBAL              json
             2192  LOAD_METHOD              dumps
             2194  LOAD_FAST                'genesis'
             2196  CALL_METHOD_1         1  '1 positional argument'
             2198  LOAD_METHOD              encode
             2200  LOAD_STR                 'utf-8'
             2202  CALL_METHOD_1         1  '1 positional argument'
             2204  CALL_METHOD_1         1  '1 positional argument'
             2206  POP_TOP          

 L. 220      2208  LOAD_GLOBAL              ETHENO
             2210  LOAD_ATTR                logger
             2212  LOAD_METHOD              info
             2214  LOAD_STR                 'Saved genesis to %s'
             2216  LOAD_DEREF               'args'
             2218  LOAD_ATTR                save_genesis
             2220  BINARY_MODULO    
             2222  CALL_METHOD_1         1  '1 positional argument'
             2224  POP_TOP          
             2226  POP_BLOCK        
             2228  LOAD_CONST               None
           2230_0  COME_FROM_WITH     2182  '2182'
             2230  WITH_CLEANUP_START
             2232  WITH_CLEANUP_FINISH
             2234  END_FINALLY      
           2236_0  COME_FROM          2168  '2168'

 L. 222      2236  LOAD_DEREF               'args'
             2238  LOAD_ATTR                geth
         2240_2242  POP_JUMP_IF_FALSE  2392  'to 2392'

 L. 223      2244  LOAD_DEREF               'args'
             2246  LOAD_ATTR                geth_port
             2248  LOAD_CONST               None
             2250  COMPARE_OP               is
         2252_2254  POP_JUMP_IF_FALSE  2272  'to 2272'

 L. 224      2256  LOAD_GLOBAL              find_open_port
             2258  LOAD_DEREF               'args'
             2260  LOAD_ATTR                port
             2262  LOAD_CONST               1
             2264  BINARY_ADD       
             2266  CALL_FUNCTION_1       1  '1 positional argument'
             2268  LOAD_DEREF               'args'
             2270  STORE_ATTR               geth_port
           2272_0  COME_FROM          2252  '2252'

 L. 226      2272  LOAD_GLOBAL              geth
             2274  LOAD_ATTR                GethClient
             2276  LOAD_FAST                'genesis'
             2278  LOAD_DEREF               'args'
             2280  LOAD_ATTR                geth_port
             2282  LOAD_CONST               ('genesis', 'port')
             2284  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             2286  STORE_FAST               'geth_instance'

 L. 227      2288  LOAD_GLOBAL              ETHENO
             2290  LOAD_FAST                'geth_instance'
             2292  STORE_ATTR               etheno

 L. 228      2294  SETUP_LOOP         2346  'to 2346'
             2296  LOAD_FAST                'accounts'
             2298  GET_ITER         
             2300  FOR_ITER           2344  'to 2344'
             2302  STORE_FAST               'account'

 L. 230      2304  LOAD_FAST                'geth_instance'
             2306  LOAD_ATTR                logger
             2308  LOAD_METHOD              info
             2310  LOAD_STR                 'Unlocking Geth account %s'
             2312  LOAD_GLOBAL              format_hex_address
             2314  LOAD_FAST                'account'
             2316  LOAD_ATTR                address
             2318  LOAD_CONST               True
             2320  CALL_FUNCTION_2       2  '2 positional arguments'
             2322  BINARY_MODULO    
             2324  CALL_METHOD_1         1  '1 positional argument'
             2326  POP_TOP          

 L. 231      2328  LOAD_FAST                'geth_instance'
             2330  LOAD_METHOD              import_account
             2332  LOAD_FAST                'account'
             2334  LOAD_ATTR                private_key
             2336  CALL_METHOD_1         1  '1 positional argument'
             2338  POP_TOP          
         2340_2342  JUMP_BACK          2300  'to 2300'
             2344  POP_BLOCK        
           2346_0  COME_FROM_LOOP     2294  '2294'

 L. 232      2346  LOAD_FAST                'geth_instance'
             2348  LOAD_ATTR                start
             2350  LOAD_CONST               True
             2352  LOAD_CONST               ('unlock_accounts',)
             2354  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
             2356  POP_TOP          

 L. 233      2358  LOAD_GLOBAL              ETHENO
             2360  LOAD_ATTR                master_client
             2362  LOAD_CONST               None
             2364  COMPARE_OP               is
         2366_2368  POP_JUMP_IF_FALSE  2378  'to 2378'

 L. 234      2370  LOAD_FAST                'geth_instance'
             2372  LOAD_GLOBAL              ETHENO
             2374  STORE_ATTR               master_client
             2376  JUMP_FORWARD       2392  'to 2392'
           2378_0  COME_FROM          2366  '2366'

 L. 236      2378  LOAD_GLOBAL              ETHENO
             2380  LOAD_METHOD              add_client
             2382  LOAD_GLOBAL              AddressSynchronizingClient
             2384  LOAD_FAST                'geth_instance'
             2386  CALL_FUNCTION_1       1  '1 positional argument'
             2388  CALL_METHOD_1         1  '1 positional argument'
             2390  POP_TOP          
           2392_0  COME_FROM          2376  '2376'
           2392_1  COME_FROM          2240  '2240'

 L. 238      2392  LOAD_DEREF               'args'
             2394  LOAD_ATTR                parity
         2396_2398  POP_JUMP_IF_FALSE  2554  'to 2554'

 L. 239      2400  LOAD_DEREF               'args'
             2402  LOAD_ATTR                parity_port
             2404  LOAD_CONST               None
             2406  COMPARE_OP               is
         2408_2410  POP_JUMP_IF_FALSE  2458  'to 2458'

 L. 240      2412  LOAD_DEREF               'args'
             2414  LOAD_ATTR                geth_port
             2416  LOAD_CONST               None
             2418  COMPARE_OP               is-not
         2420_2422  POP_JUMP_IF_FALSE  2442  'to 2442'

 L. 241      2424  LOAD_GLOBAL              find_open_port
             2426  LOAD_DEREF               'args'
             2428  LOAD_ATTR                geth_port
             2430  LOAD_CONST               1
             2432  BINARY_ADD       
             2434  CALL_FUNCTION_1       1  '1 positional argument'
             2436  LOAD_DEREF               'args'
             2438  STORE_ATTR               parity_port
             2440  JUMP_FORWARD       2458  'to 2458'
           2442_0  COME_FROM          2420  '2420'

 L. 243      2442  LOAD_GLOBAL              find_open_port
             2444  LOAD_DEREF               'args'
             2446  LOAD_ATTR                port
             2448  LOAD_CONST               1
             2450  BINARY_ADD       
             2452  CALL_FUNCTION_1       1  '1 positional argument'
             2454  LOAD_DEREF               'args'
             2456  STORE_ATTR               parity_port
           2458_0  COME_FROM          2440  '2440'
           2458_1  COME_FROM          2408  '2408'

 L. 245      2458  LOAD_GLOBAL              parity
             2460  LOAD_ATTR                ParityClient
             2462  LOAD_FAST                'genesis'
             2464  LOAD_DEREF               'args'
             2466  LOAD_ATTR                parity_port
             2468  LOAD_CONST               ('genesis', 'port')
             2470  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             2472  STORE_FAST               'parity_instance'

 L. 246      2474  LOAD_GLOBAL              ETHENO
             2476  LOAD_FAST                'parity_instance'
             2478  STORE_ATTR               etheno

 L. 247      2480  SETUP_LOOP         2508  'to 2508'
             2482  LOAD_FAST                'accounts'
             2484  GET_ITER         
             2486  FOR_ITER           2506  'to 2506'
             2488  STORE_FAST               'account'

 L. 249      2490  LOAD_FAST                'parity_instance'
             2492  LOAD_METHOD              import_account
             2494  LOAD_FAST                'account'
             2496  LOAD_ATTR                private_key
             2498  CALL_METHOD_1         1  '1 positional argument'
             2500  POP_TOP          
         2502_2504  JUMP_BACK          2486  'to 2486'
             2506  POP_BLOCK        
           2508_0  COME_FROM_LOOP     2480  '2480'

 L. 250      2508  LOAD_FAST                'parity_instance'
             2510  LOAD_ATTR                start
             2512  LOAD_CONST               True
             2514  LOAD_CONST               ('unlock_accounts',)
             2516  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
             2518  POP_TOP          

 L. 251      2520  LOAD_GLOBAL              ETHENO
             2522  LOAD_ATTR                master_client
             2524  LOAD_CONST               None
             2526  COMPARE_OP               is
         2528_2530  POP_JUMP_IF_FALSE  2540  'to 2540'

 L. 252      2532  LOAD_FAST                'parity_instance'
             2534  LOAD_GLOBAL              ETHENO
             2536  STORE_ATTR               master_client
             2538  JUMP_FORWARD       2554  'to 2554'
           2540_0  COME_FROM          2528  '2528'

 L. 254      2540  LOAD_GLOBAL              ETHENO
             2542  LOAD_METHOD              add_client
             2544  LOAD_GLOBAL              AddressSynchronizingClient
             2546  LOAD_FAST                'parity_instance'
             2548  CALL_FUNCTION_1       1  '1 positional argument'
             2550  CALL_METHOD_1         1  '1 positional argument'
             2552  POP_TOP          
           2554_0  COME_FROM          2538  '2538'
           2554_1  COME_FROM          2396  '2396'

 L. 256      2554  SETUP_LOOP         2590  'to 2590'
             2556  LOAD_DEREF               'args'
             2558  LOAD_ATTR                client
             2560  GET_ITER         
             2562  FOR_ITER           2588  'to 2588'
             2564  STORE_FAST               'client'

 L. 257      2566  LOAD_GLOBAL              ETHENO
             2568  LOAD_METHOD              add_client
             2570  LOAD_GLOBAL              AddressSynchronizingClient
             2572  LOAD_GLOBAL              RpcProxyClient
             2574  LOAD_FAST                'client'
             2576  CALL_FUNCTION_1       1  '1 positional argument'
             2578  CALL_FUNCTION_1       1  '1 positional argument'
             2580  CALL_METHOD_1         1  '1 positional argument'
             2582  POP_TOP          
         2584_2586  JUMP_BACK          2562  'to 2562'
             2588  POP_BLOCK        
           2590_0  COME_FROM_LOOP     2554  '2554'

 L. 259      2590  SETUP_LOOP         2628  'to 2628'
             2592  LOAD_DEREF               'args'
             2594  LOAD_ATTR                raw
             2596  GET_ITER         
             2598  FOR_ITER           2626  'to 2626'
             2600  STORE_FAST               'client'

 L. 260      2602  LOAD_GLOBAL              ETHENO
             2604  LOAD_METHOD              add_client
             2606  LOAD_GLOBAL              RawTransactionClient
             2608  LOAD_GLOBAL              RpcProxyClient
             2610  LOAD_FAST                'client'
             2612  CALL_FUNCTION_1       1  '1 positional argument'
             2614  LOAD_FAST                'accounts'
             2616  CALL_FUNCTION_2       2  '2 positional arguments'
             2618  CALL_METHOD_1         1  '1 positional argument'
             2620  POP_TOP          
         2622_2624  JUMP_BACK          2598  'to 2598'
             2626  POP_BLOCK        
           2628_0  COME_FROM_LOOP     2590  '2590'

 L. 262      2628  LOAD_CONST               None
             2630  STORE_DEREF              'manticore_client'

 L. 263      2632  LOAD_DEREF               'args'
             2634  LOAD_ATTR                manticore
         2636_2638  POP_JUMP_IF_FALSE  2856  'to 2856'

 L. 264      2640  LOAD_GLOBAL              MANTICORE_INSTALLED
         2642_2644  POP_JUMP_IF_TRUE   2668  'to 2668'

 L. 265      2646  LOAD_GLOBAL              ETHENO
             2648  LOAD_ATTR                logger
             2650  LOAD_METHOD              error
             2652  LOAD_STR                 "Manticore is not installed! Running Etheno with Manticore requires Manticore version 0.2.2 or newer. Reinstall Etheno with Manticore support by running `pip3 install --user 'etheno[manticore]'`, or install Manticore separately with `pip3 install --user 'manticore'`"
             2654  CALL_METHOD_1         1  '1 positional argument'
             2656  POP_TOP          

 L. 266      2658  LOAD_GLOBAL              sys
             2660  LOAD_METHOD              exit
             2662  LOAD_CONST               1
             2664  CALL_METHOD_1         1  '1 positional argument'
             2666  POP_TOP          
           2668_0  COME_FROM          2642  '2642'

 L. 267      2668  LOAD_GLOBAL              manticoreutils
             2670  LOAD_METHOD              manticore_is_new_enough
             2672  CALL_METHOD_0         0  '0 positional arguments'
             2674  STORE_FAST               'new_enough'

 L. 268      2676  LOAD_FAST                'new_enough'
             2678  LOAD_CONST               None
             2680  COMPARE_OP               is
         2682_2684  POP_JUMP_IF_FALSE  2712  'to 2712'

 L. 269      2686  LOAD_GLOBAL              ETHENO
             2688  LOAD_ATTR                logger
             2690  LOAD_METHOD              warning
             2692  LOAD_STR                 'Unknown Manticore version '
             2694  LOAD_GLOBAL              manticoreutils
             2696  LOAD_METHOD              manticore_version
             2698  CALL_METHOD_0         0  '0 positional arguments'
             2700  FORMAT_VALUE          0  ''
             2702  LOAD_STR                 '; it may not be new enough to have Etheno support!'
             2704  BUILD_STRING_3        3 
             2706  CALL_METHOD_1         1  '1 positional argument'
             2708  POP_TOP          
             2710  JUMP_FORWARD       2742  'to 2742'
           2712_0  COME_FROM          2682  '2682'

 L. 270      2712  LOAD_FAST                'new_enough'
         2714_2716  POP_JUMP_IF_TRUE   2742  'to 2742'

 L. 271      2718  LOAD_GLOBAL              ETHENO
             2720  LOAD_ATTR                logger
             2722  LOAD_METHOD              error
             2724  LOAD_STR                 'The version of Manticore installed is '
             2726  LOAD_GLOBAL              manticoreutils
             2728  LOAD_METHOD              manticore_version
             2730  CALL_METHOD_0         0  '0 positional arguments'
             2732  FORMAT_VALUE          0  ''
             2734  LOAD_STR                 ', but the minimum required version with Etheno support is 0.2.2. We will try to proceed, but things might not work correctly! Please upgrade Manticore.'
             2736  BUILD_STRING_3        3 
             2738  CALL_METHOD_1         1  '1 positional argument'
             2740  POP_TOP          
           2742_0  COME_FROM          2714  '2714'
           2742_1  COME_FROM          2710  '2710'

 L. 272      2742  LOAD_GLOBAL              ManticoreClient
             2744  CALL_FUNCTION_0       0  '0 positional arguments'
             2746  STORE_DEREF              'manticore_client'

 L. 273      2748  LOAD_GLOBAL              ETHENO
             2750  LOAD_METHOD              add_client
             2752  LOAD_DEREF               'manticore_client'
             2754  CALL_METHOD_1         1  '1 positional argument'
             2756  POP_TOP          

 L. 274      2758  LOAD_DEREF               'args'
             2760  LOAD_ATTR                manticore_max_depth
             2762  LOAD_CONST               None
             2764  COMPARE_OP               is-not
         2766_2768  POP_JUMP_IF_FALSE  2790  'to 2790'

 L. 275      2770  LOAD_DEREF               'manticore_client'
             2772  LOAD_ATTR                manticore
             2774  LOAD_METHOD              register_detector
             2776  LOAD_GLOBAL              manticoreutils
             2778  LOAD_METHOD              StopAtDepth
             2780  LOAD_DEREF               'args'
             2782  LOAD_ATTR                manticore_max_depth
             2784  CALL_METHOD_1         1  '1 positional argument'
             2786  CALL_METHOD_1         1  '1 positional argument'
             2788  POP_TOP          
           2790_0  COME_FROM          2766  '2766'

 L. 276      2790  LOAD_GLOBAL              manticoreutils
             2792  LOAD_METHOD              manticore_is_new_enough
             2794  LOAD_CONST               0
             2796  LOAD_CONST               2
             2798  LOAD_CONST               4
             2800  CALL_METHOD_3         3  '3 positional arguments'
         2802_2804  POP_JUMP_IF_FALSE  2836  'to 2836'

 L. 278      2806  LOAD_CONST               0
             2808  LOAD_CONST               ('set_verbosity',)
             2810  IMPORT_NAME_ATTR         manticore.utils.log
             2812  IMPORT_FROM              set_verbosity
             2814  STORE_FAST               'set_verbosity'
             2816  POP_TOP          

 L. 279      2818  LOAD_FAST                'set_verbosity'
             2820  LOAD_GLOBAL              getattr
             2822  LOAD_GLOBAL              logger
             2824  LOAD_DEREF               'args'
             2826  LOAD_ATTR                log_level
             2828  CALL_FUNCTION_2       2  '2 positional arguments'
             2830  CALL_FUNCTION_1       1  '1 positional argument'
             2832  POP_TOP          
             2834  JUMP_FORWARD       2856  'to 2856'
           2836_0  COME_FROM          2802  '2802'

 L. 281      2836  LOAD_DEREF               'manticore_client'
             2838  LOAD_ATTR                manticore
             2840  LOAD_METHOD              verbosity
             2842  LOAD_GLOBAL              getattr
             2844  LOAD_GLOBAL              logger
             2846  LOAD_DEREF               'args'
             2848  LOAD_ATTR                log_level
             2850  CALL_FUNCTION_2       2  '2 positional arguments'
             2852  CALL_METHOD_1         1  '1 positional argument'
             2854  POP_TOP          
           2856_0  COME_FROM          2834  '2834'
           2856_1  COME_FROM          2636  '2636'

 L. 283      2856  LOAD_DEREF               'args'
             2858  LOAD_ATTR                truffle
         2860_2862  POP_JUMP_IF_FALSE  2916  'to 2916'

 L. 284      2864  LOAD_GLOBAL              truffle
             2866  LOAD_ATTR                Truffle
             2868  LOAD_DEREF               'args'
             2870  LOAD_ATTR                truffle_cmd
             2872  LOAD_GLOBAL              ETHENO
             2874  LOAD_ATTR                logger
             2876  LOAD_CONST               ('truffle_cmd', 'parent_logger')
             2878  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             2880  STORE_DEREF              'truffle_controller'

 L. 286      2882  LOAD_CLOSURE             'args'
             2884  LOAD_CLOSURE             'manticore_client'
             2886  LOAD_CLOSURE             'truffle_controller'
             2888  BUILD_TUPLE_3         3 
             2890  LOAD_CODE                <code_object truffle_thread>
             2892  LOAD_STR                 'main.<locals>.truffle_thread'
             2894  MAKE_FUNCTION_8          'closure'
             2896  STORE_FAST               'truffle_thread'

 L. 318      2898  LOAD_GLOBAL              Thread
             2900  LOAD_FAST                'truffle_thread'
             2902  LOAD_CONST               ('target',)
             2904  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
             2906  STORE_FAST               'thread'

 L. 319      2908  LOAD_FAST                'thread'
             2910  LOAD_METHOD              start
             2912  CALL_METHOD_0         0  '0 positional arguments'
             2914  POP_TOP          
           2916_0  COME_FROM          2860  '2860'

 L. 321      2916  LOAD_DEREF               'args'
             2918  LOAD_ATTR                run_differential
         2920_2922  POP_JUMP_IF_FALSE  3010  'to 3010'
             2924  LOAD_GLOBAL              ETHENO
             2926  LOAD_ATTR                master_client
             2928  LOAD_CONST               None
             2930  COMPARE_OP               is-not
         2932_2934  POP_JUMP_IF_FALSE  3010  'to 3010'
             2936  LOAD_GLOBAL              next
             2938  LOAD_GLOBAL              filter
             2940  LOAD_LAMBDA              '<code_object <lambda>>'
             2942  LOAD_STR                 'main.<locals>.<lambda>'
             2944  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
             2946  LOAD_GLOBAL              ETHENO
             2948  LOAD_ATTR                clients
             2950  CALL_FUNCTION_2       2  '2 positional arguments'
             2952  LOAD_CONST               False
             2954  CALL_FUNCTION_2       2  '2 positional arguments'
         2956_2958  POP_JUMP_IF_FALSE  3010  'to 3010'

 L. 323      2960  LOAD_GLOBAL              ETHENO
             2962  LOAD_ATTR                logger
             2964  LOAD_METHOD              info
             2966  LOAD_STR                 'Initializing differential tests to compare clients %s'
             2968  LOAD_STR                 ', '
             2970  LOAD_METHOD              join
             2972  LOAD_GLOBAL              map
             2974  LOAD_GLOBAL              str
             2976  LOAD_GLOBAL              ETHENO
             2978  LOAD_ATTR                master_client
             2980  BUILD_LIST_1          1 
             2982  LOAD_GLOBAL              ETHENO
             2984  LOAD_ATTR                clients
             2986  BINARY_ADD       
             2988  CALL_FUNCTION_2       2  '2 positional arguments'
             2990  CALL_METHOD_1         1  '1 positional argument'
             2992  BINARY_MODULO    
             2994  CALL_METHOD_1         1  '1 positional argument'
             2996  POP_TOP          

 L. 324      2998  LOAD_GLOBAL              ETHENO
             3000  LOAD_METHOD              add_plugin
             3002  LOAD_GLOBAL              DifferentialTester
             3004  CALL_FUNCTION_0       0  '0 positional arguments'
             3006  CALL_METHOD_1         1  '1 positional argument'
             3008  POP_TOP          
           3010_0  COME_FROM          2956  '2956'
           3010_1  COME_FROM          2932  '2932'
           3010_2  COME_FROM          2920  '2920'

 L. 326      3010  LOAD_DEREF               'args'
             3012  LOAD_ATTR                echidna
         3014_3016  POP_JUMP_IF_FALSE  3086  'to 3086'

 L. 327      3018  LOAD_CONST               None
             3020  STORE_FAST               'contract_source'

 L. 328      3022  LOAD_DEREF               'args'
             3024  LOAD_ATTR                fuzz_contract
             3026  LOAD_CONST               None
             3028  COMPARE_OP               is-not
         3030_3032  POP_JUMP_IF_FALSE  3066  'to 3066'

 L. 329      3034  LOAD_GLOBAL              open
             3036  LOAD_DEREF               'args'
             3038  LOAD_ATTR                fuzz_contract
             3040  LOAD_STR                 'rb'
             3042  CALL_FUNCTION_2       2  '2 positional arguments'
             3044  SETUP_WITH         3060  'to 3060'
             3046  STORE_FAST               'c'

 L. 330      3048  LOAD_FAST                'c'
             3050  LOAD_METHOD              read
             3052  CALL_METHOD_0         0  '0 positional arguments'
             3054  STORE_FAST               'contract_source'
             3056  POP_BLOCK        
             3058  LOAD_CONST               None
           3060_0  COME_FROM_WITH     3044  '3044'
             3060  WITH_CLEANUP_START
             3062  WITH_CLEANUP_FINISH
             3064  END_FINALLY      
           3066_0  COME_FROM          3030  '3030'

 L. 331      3066  LOAD_GLOBAL              ETHENO
             3068  LOAD_METHOD              add_plugin
             3070  LOAD_GLOBAL              EchidnaPlugin
             3072  LOAD_DEREF               'args'
             3074  LOAD_ATTR                fuzz_limit
             3076  LOAD_FAST                'contract_source'
             3078  LOAD_CONST               ('transaction_limit', 'contract_source')
             3080  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             3082  CALL_METHOD_1         1  '1 positional argument'
             3084  POP_TOP          
           3086_0  COME_FROM          3014  '3014'

 L. 333      3086  LOAD_GLOBAL              len
             3088  LOAD_GLOBAL              ETHENO
             3090  LOAD_ATTR                plugins
             3092  CALL_FUNCTION_1       1  '1 positional argument'
             3094  LOAD_CONST               0
             3096  COMPARE_OP               >
             3098  STORE_FAST               'had_plugins'

 L. 335      3100  LOAD_GLOBAL              ETHENO
             3102  LOAD_ATTR                master_client
             3104  LOAD_CONST               None
             3106  COMPARE_OP               is
         3108_3110  POP_JUMP_IF_FALSE  3150  'to 3150'
             3112  LOAD_GLOBAL              ETHENO
             3114  LOAD_ATTR                clients
         3116_3118  POP_JUMP_IF_TRUE   3150  'to 3150'
             3120  LOAD_GLOBAL              ETHENO
             3122  LOAD_ATTR                plugins
         3124_3126  POP_JUMP_IF_TRUE   3150  'to 3150'

 L. 336      3128  LOAD_FAST                'had_plugins'
         3130_3132  POP_JUMP_IF_TRUE   3146  'to 3146'

 L. 337      3134  LOAD_GLOBAL              ETHENO
             3136  LOAD_ATTR                logger
             3138  LOAD_METHOD              info
             3140  LOAD_STR                 'No clients or plugins provided; exiting...'
             3142  CALL_METHOD_1         1  '1 positional argument'
             3144  POP_TOP          
           3146_0  COME_FROM          3130  '3130'

 L. 339      3146  LOAD_CONST               None
             3148  RETURN_VALUE     
           3150_0  COME_FROM          3124  '3124'
           3150_1  COME_FROM          3116  '3116'
           3150_2  COME_FROM          3108  '3108'

 L. 341      3150  LOAD_GLOBAL              EthenoView
             3152  CALL_FUNCTION_0       0  '0 positional arguments'
             3154  STORE_FAST               'etheno'

 L. 342      3156  LOAD_GLOBAL              app
             3158  LOAD_ATTR                add_url_rule
             3160  LOAD_STR                 '/'
             3162  LOAD_FAST                'etheno'
             3164  LOAD_METHOD              as_view
             3166  LOAD_STR                 'etheno'
             3168  CALL_METHOD_1         1  '1 positional argument'
             3170  LOAD_CONST               ('view_func',)
             3172  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             3174  POP_TOP          

 L. 344      3176  LOAD_GLOBAL              ETHENO
             3178  LOAD_ATTR                run
             3180  LOAD_DEREF               'args'
             3182  LOAD_ATTR                debug
             3184  LOAD_DEREF               'args'
             3186  LOAD_ATTR                run_publicly
             3188  LOAD_DEREF               'args'
             3190  LOAD_ATTR                port
             3192  LOAD_CONST               ('debug', 'run_publicly', 'port')
             3194  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
             3196  STORE_FAST               'etheno_thread'

 L. 345      3198  LOAD_DEREF               'args'
             3200  LOAD_ATTR                truffle
         3202_3204  POP_JUMP_IF_FALSE  3214  'to 3214'

 L. 346      3206  LOAD_DEREF               'truffle_controller'
             3208  LOAD_METHOD              terminate
             3210  CALL_METHOD_0         0  '0 positional arguments'
             3212  POP_TOP          
           3214_0  COME_FROM          3202  '3202'

 L. 348      3214  LOAD_DEREF               'args'
             3216  LOAD_ATTR                log_file
             3218  LOAD_CONST               None
             3220  COMPARE_OP               is-not
         3222_3224  POP_JUMP_IF_FALSE  3248  'to 3248'

 L. 349      3226  LOAD_GLOBAL              print
             3228  LOAD_STR                 'Log file saved to: %s'
             3230  LOAD_GLOBAL              os
             3232  LOAD_ATTR                path
             3234  LOAD_METHOD              realpath
             3236  LOAD_DEREF               'args'
             3238  LOAD_ATTR                log_file
             3240  CALL_METHOD_1         1  '1 positional argument'
             3242  BINARY_MODULO    
             3244  CALL_FUNCTION_1       1  '1 positional argument'
             3246  POP_TOP          
           3248_0  COME_FROM          3222  '3222'

 L. 350      3248  LOAD_DEREF               'args'
             3250  LOAD_ATTR                log_dir
             3252  LOAD_CONST               None
             3254  COMPARE_OP               is-not
         3256_3258  POP_JUMP_IF_FALSE  3300  'to 3300'

 L. 351      3260  LOAD_GLOBAL              print
             3262  LOAD_STR                 'Logs %ssaved to: %s'
             3264  LOAD_STR                 ''
             3266  LOAD_STR                 'also '
             3268  BUILD_LIST_2          2 
             3270  LOAD_DEREF               'args'
             3272  LOAD_ATTR                log_file
             3274  LOAD_CONST               None
             3276  COMPARE_OP               is-not
             3278  BINARY_SUBSCR    
             3280  LOAD_GLOBAL              os
             3282  LOAD_ATTR                path
             3284  LOAD_METHOD              realpath
             3286  LOAD_DEREF               'args'
             3288  LOAD_ATTR                log_dir
             3290  CALL_METHOD_1         1  '1 positional argument'
             3292  BUILD_TUPLE_2         2 
             3294  BINARY_MODULO    
             3296  CALL_FUNCTION_1       1  '1 positional argument'
             3298  POP_TOP          
           3300_0  COME_FROM          3256  '3256'

Parse error at or near `COME_FROM' instruction at offset 1046_0


if __name__ == '__main__':
    main()