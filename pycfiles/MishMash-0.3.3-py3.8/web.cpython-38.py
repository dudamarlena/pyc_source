# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mishmash/commands/web.py
# Compiled at: 2020-02-22 16:22:47
# Size of source mod 2**32: 1172 bytes
from ..web import MISHMASH_WEB
if MISHMASH_WEB:
    import tempfile
    from pathlib import Path
    from ..core import Command
    from pyramid.scripts.pserve import PServeCommand

    @Command.register
    class Web(Command):
        NAME = 'web'
        HELP = 'MishMash web interface.'

        def _initArgParser(self, parser):
            parser.add_argument('-p', '--port', type=int, default=None)

        def _run--- This code section failed: ---

 L.  18         0  LOAD_FAST                'self'
                2  LOAD_ATTR                args
                4  LOAD_ATTR                port
                6  POP_JUMP_IF_FALSE    30  'to 30'

 L.  19         8  LOAD_GLOBAL              str
               10  LOAD_FAST                'self'
               12  LOAD_ATTR                args
               14  LOAD_ATTR                port
               16  CALL_FUNCTION_1       1  ''
               18  LOAD_FAST                'self'
               20  LOAD_ATTR                config
               22  LOAD_STR                 'server:main'
               24  BINARY_SUBSCR    
               26  LOAD_STR                 'port'
               28  STORE_SUBSCR     
             30_0  COME_FROM             6  '6'

 L.  23        30  LOAD_GLOBAL              tempfile
               32  LOAD_ATTR                NamedTemporaryFile
               34  LOAD_STR                 'w'
               36  LOAD_STR                 '.ini'
               38  LOAD_CONST               False
               40  LOAD_CONST               ('mode', 'suffix', 'delete')
               42  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               44  SETUP_WITH          140  'to 140'
               46  STORE_FAST               'config_file'

 L.  24        48  LOAD_FAST                'self'
               50  LOAD_ATTR                config
               52  LOAD_METHOD              write
               54  LOAD_FAST                'config_file'
               56  CALL_METHOD_1         1  ''
               58  POP_TOP          

 L.  25        60  LOAD_FAST                'config_file'
               62  LOAD_METHOD              flush
               64  CALL_METHOD_0         0  ''
               66  POP_TOP          

 L.  26        68  LOAD_GLOBAL              PServeCommand
               70  LOAD_STR                 'mishmash'
               72  LOAD_FAST                'config_file'
               74  LOAD_ATTR                name
               76  BUILD_LIST_2          2 
               78  CALL_FUNCTION_1       1  ''
               80  STORE_FAST               'pserve'

 L.  27        82  SETUP_FINALLY       108  'to 108'

 L.  28        84  LOAD_FAST                'pserve'
               86  LOAD_METHOD              run
               88  CALL_METHOD_0         0  ''
               90  POP_BLOCK        
               92  CALL_FINALLY        108  'to 108'
               94  POP_BLOCK        
               96  ROT_TWO          
               98  BEGIN_FINALLY    
              100  WITH_CLEANUP_START
              102  WITH_CLEANUP_FINISH
              104  POP_FINALLY           0  ''
              106  RETURN_VALUE     
            108_0  COME_FROM            92  '92'
            108_1  COME_FROM_FINALLY    82  '82'

 L.  30       108  LOAD_GLOBAL              Path
              110  LOAD_FAST                'config_file'
              112  LOAD_ATTR                name
              114  CALL_FUNCTION_1       1  ''
              116  STORE_FAST               'tmp_cfg'

 L.  31       118  LOAD_FAST                'tmp_cfg'
              120  LOAD_METHOD              exists
              122  CALL_METHOD_0         0  ''
              124  POP_JUMP_IF_FALSE   134  'to 134'

 L.  33       126  LOAD_FAST                'tmp_cfg'
              128  LOAD_METHOD              unlink
              130  CALL_METHOD_0         0  ''
              132  POP_TOP          
            134_0  COME_FROM           124  '124'
              134  END_FINALLY      
              136  POP_BLOCK        
              138  BEGIN_FINALLY    
            140_0  COME_FROM_WITH       44  '44'
              140  WITH_CLEANUP_START
              142  WITH_CLEANUP_FINISH
              144  END_FINALLY      

Parse error at or near `POP_BLOCK' instruction at offset 94