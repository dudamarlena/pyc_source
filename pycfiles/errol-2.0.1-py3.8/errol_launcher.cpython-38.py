# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/errol/errol_launcher.py
# Compiled at: 2020-05-10 07:28:38
# Size of source mod 2**32: 3565 bytes
from errol import watcher
from errol import xmpp
from errol import config_parser
from configparser import NoSectionError, NoOptionError
import logging, argparse, asyncio
logging.getLogger('asyncio').setLevel(logging.INFO)
logger = logging.getLogger(__name__)

class ErrolLauncher:

    def __init__(self, conf):
        self.conf = conf

    def conf_getter(self):
        return self.conf

    async def launcher(self):
        if self.conf['command'] == 'xmpp':
            xmpp_handler = xmpp.XmppHandler()
            xmpp_handler.prepare(path=(self.conf['path']), filename='test.tmp', action='receive_file', forever=True,
              xmpp_conf=(self.conf['xmpp']))
            await xmpp_handler.update_xmpp_instance()
            xmpp_instance = xmpp_handler.ret_xmpp_instance()
            xmpp_instance.connect()
        else:
            if self.conf['command'] == 'watcher':
                await watcher.watch(path=(self.conf['path']), events=(self.conf['events']), debug=(self.conf['debug']), xmpp_conf=(self.conf['xmpp']))
            else:
                return


def config_retriever--- This code section failed: ---

 L.  41         0  LOAD_GLOBAL              argparse
                2  LOAD_ATTR                ArgumentParser
                4  LOAD_STR                 'Automatic XMPP file sender and directory watcher'
                6  LOAD_CONST               ('description',)
                8  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               10  STORE_FAST               'parser'

 L.  42        12  LOAD_FAST                'parser'
               14  LOAD_ATTR                add_argument
               16  LOAD_STR                 '-e'
               18  LOAD_STR                 '--events'

 L.  43        20  LOAD_GLOBAL              int

 L.  44        22  LOAD_CONST               10000

 L.  45        24  LOAD_STR                 'Number of events to watch (create modify) in the directory. Once reached, the programs stops.'

 L.  42        26  LOAD_CONST               ('type', 'default', 'help')
               28  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
               30  POP_TOP          

 L.  47        32  LOAD_FAST                'parser'
               34  LOAD_ATTR                add_argument
               36  LOAD_STR                 '-f'
               38  LOAD_STR                 '--file'

 L.  48        40  LOAD_STR                 'Config file containing XMPP parameters'

 L.  49        42  LOAD_CONST               False

 L.  49        44  LOAD_STR                 'config.ini'

 L.  47        46  LOAD_CONST               ('help', 'required', 'default')
               48  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
               50  POP_TOP          

 L.  50        52  LOAD_FAST                'parser'
               54  LOAD_ATTR                add_argument
               56  LOAD_STR                 '-d'
               58  LOAD_STR                 '--debug'
               60  LOAD_STR                 'set logging to DEBUG'

 L.  51        62  LOAD_STR                 'store_const'

 L.  51        64  LOAD_STR                 'loglevel'

 L.  52        66  LOAD_GLOBAL              logging
               68  LOAD_ATTR                DEBUG

 L.  52        70  LOAD_GLOBAL              logging
               72  LOAD_ATTR                INFO

 L.  50        74  LOAD_CONST               ('help', 'action', 'dest', 'const', 'default')
               76  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
               78  POP_TOP          

 L.  53        80  LOAD_FAST                'parser'
               82  LOAD_ATTR                add_argument
               84  LOAD_STR                 '-p'
               86  LOAD_STR                 '--path'

 L.  54        88  LOAD_STR                 'The path watched.'

 L.  55        90  LOAD_CONST               True

 L.  53        92  LOAD_CONST               ('help', 'required')
               94  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
               96  POP_TOP          

 L.  57        98  LOAD_FAST                'parser'
              100  LOAD_ATTR                add_argument
              102  LOAD_STR                 '-c'
              104  LOAD_STR                 '--command'

 L.  58       106  LOAD_STR                 'The executed command: xmpp or watcher'

 L.  59       108  LOAD_CONST               True

 L.  57       110  LOAD_CONST               ('help', 'required')
              112  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              114  POP_TOP          

 L.  60       116  BUILD_MAP_0           0 
              118  STORE_FAST               'conf'

 L.  61       120  LOAD_CONST               None
              122  STORE_FAST               'args'

 L.  62       124  SETUP_FINALLY       186  'to 186'

 L.  63       126  LOAD_FAST                'parser'
              128  LOAD_METHOD              parse_args
              130  CALL_METHOD_0         0  ''
              132  STORE_FAST               'args'

 L.  64       134  LOAD_GLOBAL              logging
              136  LOAD_ATTR                basicConfig
              138  LOAD_FAST                'args'
              140  LOAD_ATTR                loglevel
              142  LOAD_STR                 '%(levelname)-8s %(message)s'
              144  LOAD_CONST               ('level', 'format')
              146  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              148  POP_TOP          

 L.  65       150  LOAD_CONST               False
              152  STORE_FAST               'debug'

 L.  66       154  LOAD_FAST                'args'
              156  LOAD_ATTR                loglevel
              158  LOAD_GLOBAL              logging
              160  LOAD_ATTR                DEBUG
              162  COMPARE_OP               ==
              164  POP_JUMP_IF_FALSE   170  'to 170'

 L.  67       166  LOAD_CONST               True
              168  STORE_FAST               'debug'
            170_0  COME_FROM           164  '164'

 L.  68       170  LOAD_GLOBAL              config_parser
              172  LOAD_METHOD              read_config
              174  LOAD_FAST                'args'
              176  LOAD_ATTR                file
              178  CALL_METHOD_1         1  ''
              180  STORE_FAST               'conf'
              182  POP_BLOCK        
              184  JUMP_FORWARD        248  'to 248'
            186_0  COME_FROM_FINALLY   124  '124'

 L.  69       186  DUP_TOP          
              188  LOAD_GLOBAL              NoSectionError
              190  LOAD_GLOBAL              NoOptionError
              192  LOAD_GLOBAL              SystemExit
              194  BUILD_TUPLE_3         3 
              196  COMPARE_OP               exception-match
              198  POP_JUMP_IF_FALSE   246  'to 246'
              200  POP_TOP          
              202  STORE_FAST               'e'
              204  POP_TOP          
              206  SETUP_FINALLY       234  'to 234'

 L.  71       208  LOAD_GLOBAL              asyncio
              210  LOAD_METHOD              get_event_loop
              212  CALL_METHOD_0         0  ''
              214  STORE_FAST               'loop'

 L.  72       216  LOAD_FAST                'loop'
              218  LOAD_METHOD              stop
              220  CALL_METHOD_0         0  ''
              222  POP_TOP          

 L.  73       224  POP_BLOCK        
              226  POP_EXCEPT       
              228  CALL_FINALLY        234  'to 234'
              230  LOAD_CONST               None
              232  RETURN_VALUE     
            234_0  COME_FROM           228  '228'
            234_1  COME_FROM_FINALLY   206  '206'
              234  LOAD_CONST               None
              236  STORE_FAST               'e'
              238  DELETE_FAST              'e'
              240  END_FINALLY      
              242  POP_EXCEPT       
              244  JUMP_FORWARD        248  'to 248'
            246_0  COME_FROM           198  '198'
              246  END_FINALLY      
            248_0  COME_FROM           244  '244'
            248_1  COME_FROM           184  '184'

 L.  74       248  LOAD_FAST                'args'
              250  LOAD_ATTR                command
              252  LOAD_FAST                'conf'
              254  LOAD_STR                 'command'
              256  STORE_SUBSCR     

 L.  75       258  LOAD_FAST                'args'
              260  LOAD_ATTR                path
              262  LOAD_FAST                'conf'
              264  LOAD_STR                 'path'
              266  STORE_SUBSCR     

 L.  76       268  LOAD_FAST                'args'
              270  LOAD_ATTR                events
              272  LOAD_FAST                'conf'
              274  LOAD_STR                 'events'
              276  STORE_SUBSCR     

 L.  77       278  LOAD_FAST                'conf'
              280  LOAD_METHOD              setdefault
              282  LOAD_STR                 'debug'
              284  LOAD_CONST               False
              286  CALL_METHOD_2         2  ''
              288  POP_TOP          

 L.  78       290  LOAD_FAST                'debug'
          292_294  POP_JUMP_IF_FALSE   304  'to 304'

 L.  79       296  LOAD_CONST               True
              298  LOAD_FAST                'conf'
              300  LOAD_STR                 'debug'
              302  STORE_SUBSCR     
            304_0  COME_FROM           292  '292'

 L.  80       304  LOAD_FAST                'conf'
              306  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `CALL_FINALLY' instruction at offset 228


async def main():
    conf = config_retriever()
    if conf and conf.get('command'):
        errol_instance = ErrolLauncher(conf)
        await errol_instance.launcher()
    else:
        logger.info('No suitable config found.')


def launcher--- This code section failed: ---

 L.  93         0  LOAD_GLOBAL              asyncio
                2  LOAD_METHOD              get_event_loop
                4  CALL_METHOD_0         0  ''
                6  STORE_FAST               'loop'

 L.  94         8  LOAD_FAST                'loop'
               10  LOAD_METHOD              create_task
               12  LOAD_GLOBAL              main
               14  CALL_FUNCTION_0       0  ''
               16  CALL_METHOD_1         1  ''
               18  STORE_FAST               'future'

 L.  95        20  SETUP_FINALLY       124  'to 124'
               22  SETUP_FINALLY        36  'to 36'

 L.  96        24  LOAD_FAST                'loop'
               26  LOAD_METHOD              run_forever
               28  CALL_METHOD_0         0  ''
               30  POP_TOP          
               32  POP_BLOCK        
               34  JUMP_FORWARD        120  'to 120'
             36_0  COME_FROM_FINALLY    22  '22'

 L.  97        36  DUP_TOP          
               38  LOAD_GLOBAL              asyncio
               40  LOAD_ATTR                CancelledError
               42  COMPARE_OP               exception-match
               44  POP_JUMP_IF_FALSE    88  'to 88'
               46  POP_TOP          
               48  POP_TOP          
               50  POP_TOP          

 L.  98        52  LOAD_GLOBAL              logger
               54  LOAD_METHOD              info
               56  LOAD_STR                 'Tasks has been canceled'
               58  CALL_METHOD_1         1  ''
               60  POP_TOP          

 L.  99        62  LOAD_GLOBAL              asyncio
               64  LOAD_METHOD              all_tasks
               66  CALL_METHOD_0         0  ''
               68  GET_ITER         
               70  FOR_ITER             84  'to 84'
               72  STORE_FAST               'task'

 L. 100        74  LOAD_FAST                'task'
               76  LOAD_METHOD              cancel
               78  CALL_METHOD_0         0  ''
               80  POP_TOP          
               82  JUMP_BACK            70  'to 70'
               84  POP_EXCEPT       
               86  JUMP_FORWARD        120  'to 120'
             88_0  COME_FROM            44  '44'

 L. 101        88  DUP_TOP          
               90  LOAD_GLOBAL              RuntimeError
               92  LOAD_GLOBAL              KeyboardInterrupt
               94  LOAD_GLOBAL              SystemExit
               96  BUILD_TUPLE_3         3 
               98  COMPARE_OP               exception-match
              100  POP_JUMP_IF_FALSE   118  'to 118'
              102  POP_TOP          
              104  POP_TOP          
              106  POP_TOP          

 L. 102       108  POP_EXCEPT       
              110  POP_BLOCK        
              112  CALL_FINALLY        124  'to 124'
              114  LOAD_CONST               1
              116  RETURN_VALUE     
            118_0  COME_FROM           100  '100'
              118  END_FINALLY      
            120_0  COME_FROM            86  '86'
            120_1  COME_FROM            34  '34'
              120  POP_BLOCK        
              122  BEGIN_FINALLY    
            124_0  COME_FROM           112  '112'
            124_1  COME_FROM_FINALLY    20  '20'

 L. 104       124  LOAD_FAST                'loop'
              126  LOAD_METHOD              stop
              128  CALL_METHOD_0         0  ''
              130  POP_TOP          
              132  END_FINALLY      

Parse error at or near `CALL_FINALLY' instruction at offset 112


if __name__ == '__main__':
    launcher()