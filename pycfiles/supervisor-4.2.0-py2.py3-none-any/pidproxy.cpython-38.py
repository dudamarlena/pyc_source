# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./build/lib/supervisor/pidproxy.py
# Compiled at: 2019-04-10 17:22:04
# Size of source mod 2**32: 1892 bytes
""" An executable which proxies for a subprocess; upon a signal, it sends that
signal to the process identified by a pidfile. """
import os, sys, signal, time

class PidProxy:
    pid = None

    def __init__(self, args):
        self.setsignals()
        try:
            self.pidfile, cmdargs = args[1], args[2:]
            self.command = os.path.abspath(cmdargs[0])
            self.cmdargs = cmdargs
        except (ValueError, IndexError):
            self.usage()
            sys.exit(1)

    def go(self):
        self.pid = os.spawnv(os.P_NOWAIT, self.command, self.cmdargs)
        while True:
            time.sleep(5)
            try:
                pid = os.waitpid(-1, os.WNOHANG)[0]
            except OSError:
                pid = None
            else:
                if pid:
                    break

    def usage(self):
        print('pidproxy.py <pidfile name> <command> [<cmdarg1> ...]')

    def setsignals(self):
        signal.signal(signal.SIGTERM, self.passtochild)
        signal.signal(signal.SIGHUP, self.passtochild)
        signal.signal(signal.SIGINT, self.passtochild)
        signal.signal(signal.SIGUSR1, self.passtochild)
        signal.signal(signal.SIGUSR2, self.passtochild)
        signal.signal(signal.SIGQUIT, self.passtochild)
        signal.signal(signal.SIGCHLD, self.reap)

    def reap(self, sig, frame):
        pass

    def passtochild--- This code section failed: ---

 L.  51         0  SETUP_FINALLY        46  'to 46'

 L.  52         2  LOAD_GLOBAL              open
                4  LOAD_FAST                'self'
                6  LOAD_ATTR                pidfile
                8  LOAD_STR                 'r'
               10  CALL_FUNCTION_2       2  ''
               12  SETUP_WITH           36  'to 36'
               14  STORE_FAST               'f'

 L.  53        16  LOAD_GLOBAL              int
               18  LOAD_FAST                'f'
               20  LOAD_METHOD              read
               22  CALL_METHOD_0         0  ''
               24  LOAD_METHOD              strip
               26  CALL_METHOD_0         0  ''
               28  CALL_FUNCTION_1       1  ''
               30  STORE_FAST               'pid'
               32  POP_BLOCK        
               34  BEGIN_FINALLY    
             36_0  COME_FROM_WITH       12  '12'
               36  WITH_CLEANUP_START
               38  WITH_CLEANUP_FINISH
               40  END_FINALLY      
               42  POP_BLOCK        
               44  JUMP_FORWARD         74  'to 74'
             46_0  COME_FROM_FINALLY     0  '0'

 L.  54        46  POP_TOP          
               48  POP_TOP          
               50  POP_TOP          

 L.  55        52  LOAD_GLOBAL              print
               54  LOAD_STR                 "Can't read child pidfile %s!"
               56  LOAD_FAST                'self'
               58  LOAD_ATTR                pidfile
               60  BINARY_MODULO    
               62  CALL_FUNCTION_1       1  ''
               64  POP_TOP          

 L.  56        66  POP_EXCEPT       
               68  LOAD_CONST               None
               70  RETURN_VALUE     
               72  END_FINALLY      
             74_0  COME_FROM            44  '44'

 L.  57        74  LOAD_GLOBAL              os
               76  LOAD_METHOD              kill
               78  LOAD_FAST                'pid'
               80  LOAD_FAST                'sig'
               82  CALL_METHOD_2         2  ''
               84  POP_TOP          

 L.  58        86  LOAD_FAST                'sig'
               88  LOAD_GLOBAL              signal
               90  LOAD_ATTR                SIGTERM
               92  LOAD_GLOBAL              signal
               94  LOAD_ATTR                SIGINT
               96  LOAD_GLOBAL              signal
               98  LOAD_ATTR                SIGQUIT
              100  BUILD_TUPLE_3         3 
              102  COMPARE_OP               in
              104  POP_JUMP_IF_FALSE   116  'to 116'

 L.  59       106  LOAD_GLOBAL              sys
              108  LOAD_METHOD              exit
              110  LOAD_CONST               0
              112  CALL_METHOD_1         1  ''
              114  POP_TOP          
            116_0  COME_FROM           104  '104'

Parse error at or near `LOAD_CONST' instruction at offset 68


def main():
    pp = PidProxy(sys.argv)
    pp.go()


if __name__ == '__main__':
    main()