# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mishmash/commands/server.py
# Compiled at: 2019-12-04 00:39:14
# Size of source mod 2**32: 2928 bytes
import time, subprocess
from multiprocessing import Process
from ..core import Command, CommandError

class MishMashProc(Process):

    def __init__(self, cmd, *args, config=None):
        self._cmd = cmd
        super().__init__(target=(MishMashProc._entryPoint), args=[config, cmd, *args])

    @staticmethod
    def _entryPoint(config, cmd, *args):
        from ..__main__ import MishMash
        return MishMash(config_obj=config).run(args_list=[cmd, *args])

    def __str__(self):
        if self.exitcode is None:
            return f"`mishmash {self._cmd}` <running>"
        return f"`mishmash {self._cmd}` <stopped[{self.exitcode}]>"

    def start(self):
        super().start()
        return self

    def join(self, timeout=None, check=False):
        super().join(timeout)
        if check:
            if self.exitcode:
                raise CommandError(self)


class UnsonicProc:

    def __init__(self, config):
        self._config = config
        self._unsonic = None
        self.exitcode = None

    def start(self):
        self._unsonic = subprocess.Popen([
         'unsonic', '--config', self._config, 'serve'])
        return self

    def join--- This code section failed: ---

 L.  48         0  LOAD_FAST                'self'
                2  LOAD_ATTR                exitcode
                4  LOAD_CONST               None
                6  COMPARE_OP               is-not
                8  POP_JUMP_IF_FALSE    14  'to 14'

 L.  49        10  LOAD_CONST               None
               12  RETURN_VALUE     
             14_0  COME_FROM             8  '8'

 L.  51        14  SETUP_FINALLY        34  'to 34'

 L.  52        16  LOAD_FAST                'self'
               18  LOAD_ATTR                _unsonic
               20  LOAD_ATTR                wait
               22  LOAD_FAST                'timeout'
               24  LOAD_CONST               ('timeout',)
               26  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               28  POP_TOP          
               30  POP_BLOCK        
               32  JUMP_FORWARD         64  'to 64'
             34_0  COME_FROM_FINALLY    14  '14'

 L.  53        34  DUP_TOP          
               36  LOAD_GLOBAL              subprocess
               38  LOAD_ATTR                TimeoutExpired
               40  COMPARE_OP               exception-match
               42  POP_JUMP_IF_FALSE    62  'to 62'
               44  POP_TOP          
               46  POP_TOP          
               48  POP_TOP          

 L.  54        50  LOAD_CONST               None
               52  LOAD_FAST                'self'
               54  STORE_ATTR               exitcode

 L.  55        56  POP_EXCEPT       
               58  LOAD_CONST               None
               60  RETURN_VALUE     
             62_0  COME_FROM            42  '42'
               62  END_FINALLY      
             64_0  COME_FROM            32  '32'

 L.  57        64  LOAD_FAST                'self'
               66  LOAD_ATTR                _unsonic
               68  LOAD_ATTR                returncode
               70  LOAD_FAST                'self'
               72  STORE_ATTR               exitcode

 L.  58        74  LOAD_FAST                'check'
               76  POP_JUMP_IF_FALSE   102  'to 102'
               78  LOAD_FAST                'self'
               80  LOAD_ATTR                exitcode
               82  LOAD_CONST               None
               84  COMPARE_OP               is-not
               86  POP_JUMP_IF_FALSE   102  'to 102'
               88  LOAD_FAST                'self'
               90  LOAD_ATTR                exitcode
               92  POP_JUMP_IF_FALSE   102  'to 102'

 L.  59        94  LOAD_GLOBAL              CommandError
               96  LOAD_FAST                'self'
               98  CALL_FUNCTION_1       1  ''
              100  RAISE_VARARGS_1       1  'exception instance'
            102_0  COME_FROM            92  '92'
            102_1  COME_FROM            86  '86'
            102_2  COME_FROM            76  '76'

Parse error at or near `LOAD_CONST' instruction at offset 58

    def kill(self):
        self._unsonic.kill()


@Command.register
class Server(Command):
    NAME = 'server'
    HELP = 'Sync, monitor, browse, etc.'

    def _run(self):
        """main"""
        all_procs = []
        MishMashProc('info', config=(self.args.config)).start().join(check=True)
        sync = MishMashProc('sync', '--no-prompt', '--monitor', config=(self.args.config)) if self.args.config.getboolean('server', 'sync', fallback=True) else None
        web = MishMashProc('web', config=(self.args.config)) if self.args.config.getboolean('server', 'web', fallback=True) else None
        unsonic = self._createUnsonic()
        for p in (
         sync, web, unsonic):
            if p:
                all_procs.append(p)
                p.start()
        else:
            try:
                while True:
                    for proc in all_procs:
                        proc.join(1, check=True)
                    else:
                        time.sleep(5)

            finally:
                for proc in all_procs:
                    proc.kill()

    def _createUnsonic(self):
        if self.args.config.getboolean('server', 'unsonic', fallback=False):
            cfg_file = self.args.config.get('unsonic', 'config')
            return UnsonicProc(cfg_file)