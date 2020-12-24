# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-intel/egg/lust/server.py
# Compiled at: 2013-04-09 18:55:40
from . import unix, log, config
import sys, os

class Simple(object):
    name = None
    should_jail = True
    should_drop_priv = True

    def __init__--- This code section failed: ---

 L.  14         0  LOAD_FAST             0  'self'
                3  LOAD_ATTR             0  'name'
                6  POP_JUMP_IF_TRUE     18  'to 18'
                9  LOAD_ASSERT              AssertionError
               12  LOAD_CONST               "You must set the service's name."
               15  RAISE_VARARGS_2       2  None

 L.  16        18  LOAD_FAST             6  'config_file'
               21  JUMP_IF_TRUE_OR_POP    49  'to 49'
               24  LOAD_GLOBAL           2  'os'
               27  LOAD_ATTR             3  'path'
               30  LOAD_ATTR             4  'join'
               33  LOAD_CONST               '/etc'
               36  LOAD_FAST             0  'self'
               39  LOAD_ATTR             0  'name'
               42  LOAD_CONST               '.conf'
               45  BINARY_ADD       
               46  CALL_FUNCTION_2       2  None
             49_0  COME_FROM            21  '21'
               49  STORE_FAST            6  'config_file'

 L.  17        52  LOAD_FAST             0  'self'
               55  LOAD_ATTR             5  'load_config'
               58  LOAD_FAST             6  'config_file'
               61  CALL_FUNCTION_1       1  None
               64  POP_TOP          

 L.  18        65  LOAD_FAST             0  'self'
               68  LOAD_ATTR             6  'get'
               71  LOAD_CONST               'run_dir'
               74  CALL_FUNCTION_1       1  None
               77  JUMP_IF_TRUE_OR_POP   101  'to 101'
               80  LOAD_GLOBAL           2  'os'
               83  LOAD_ATTR             3  'path'
               86  LOAD_ATTR             4  'join'
               89  LOAD_FAST             1  'run_base'
               92  LOAD_FAST             0  'self'
               95  LOAD_ATTR             0  'name'
               98  CALL_FUNCTION_2       2  None
            101_0  COME_FROM            77  '77'
              101  LOAD_FAST             0  'self'
              104  STORE_ATTR            7  'run_dir'

 L.  19       107  LOAD_FAST             0  'self'
              110  LOAD_ATTR             6  'get'
              113  LOAD_CONST               'pid_path'
              116  CALL_FUNCTION_1       1  None
              119  JUMP_IF_TRUE_OR_POP   125  'to 125'
              122  LOAD_FAST             3  'pid_file_path'
            125_0  COME_FROM           119  '119'
              125  LOAD_FAST             0  'self'
              128  STORE_ATTR            8  'pid_path'

 L.  20       131  LOAD_FAST             0  'self'
              134  LOAD_ATTR             6  'get'
              137  LOAD_CONST               'log_file'
              140  CALL_FUNCTION_1       1  None
              143  JUMP_IF_TRUE_OR_POP   171  'to 171'
              146  LOAD_GLOBAL           2  'os'
              149  LOAD_ATTR             3  'path'
              152  LOAD_ATTR             4  'join'
              155  LOAD_FAST             2  'log_dir'
              158  LOAD_FAST             0  'self'
              161  LOAD_ATTR             0  'name'
              164  LOAD_CONST               '.log'
              167  BINARY_ADD       
              168  CALL_FUNCTION_2       2  None
            171_0  COME_FROM           143  '143'
              171  LOAD_FAST             0  'self'
              174  STORE_ATTR            9  'log_file'

 L.  21       177  LOAD_FAST             0  'self'
              180  LOAD_ATTR             6  'get'
              183  LOAD_CONST               'uid'
              186  CALL_FUNCTION_1       1  None
              189  JUMP_IF_TRUE_OR_POP   195  'to 195'
              192  LOAD_FAST             4  'uid'
            195_0  COME_FROM           189  '189'
              195  LOAD_FAST             0  'self'
              198  STORE_ATTR           10  'uid'

 L.  22       201  LOAD_FAST             0  'self'
              204  LOAD_ATTR             6  'get'
              207  LOAD_CONST               'gid'
              210  CALL_FUNCTION_1       1  None
              213  JUMP_IF_TRUE_OR_POP   219  'to 219'
              216  LOAD_FAST             5  'gid'
            219_0  COME_FROM           213  '213'
              219  LOAD_FAST             0  'self'
              222  STORE_ATTR           11  'gid'

 L.  23       225  LOAD_FAST             0  'self'
              228  LOAD_ATTR             6  'get'
              231  LOAD_CONST               'run_dir_mode'
              234  CALL_FUNCTION_1       1  None
              237  JUMP_IF_TRUE_OR_POP   243  'to 243'
              240  LOAD_CONST               '0700'
            243_0  COME_FROM           237  '237'
              243  LOAD_FAST             0  'self'
              246  STORE_ATTR           12  'run_dir_mode'

 L.  24       249  LOAD_GLOBAL          13  'int'
              252  LOAD_FAST             0  'self'
              255  LOAD_ATTR            12  'run_dir_mode'
              258  LOAD_CONST               8
              261  CALL_FUNCTION_2       2  None
              264  LOAD_FAST             0  'self'
              267  STORE_ATTR           12  'run_dir_mode'

 L.  26       270  LOAD_GLOBAL          14  'log'
              273  LOAD_ATTR            15  'debug'
              276  LOAD_CONST               'UID and GID are %s:%s'
              279  LOAD_FAST             0  'self'
              282  LOAD_ATTR            10  'uid'
              285  LOAD_FAST             0  'self'
              288  LOAD_ATTR            11  'gid'
              291  BUILD_TUPLE_2         2 
              294  BINARY_MODULO    
              295  CALL_FUNCTION_1       1  None
              298  POP_TOP          

 L.  28       299  LOAD_GLOBAL          16  'unix'
              302  LOAD_ATTR            17  'get_user_info'
              305  LOAD_FAST             0  'self'
              308  LOAD_ATTR            10  'uid'
              311  LOAD_FAST             0  'self'
              314  LOAD_ATTR            11  'gid'
              317  CALL_FUNCTION_2       2  None
              320  UNPACK_SEQUENCE_2     2 
              323  LOAD_FAST             0  'self'
              326  STORE_ATTR           18  'unum'
              329  LOAD_FAST             0  'self'
              332  STORE_ATTR           19  'gnum'

 L.  29       335  LOAD_GLOBAL          14  'log'
              338  LOAD_ATTR            15  'debug'
              341  LOAD_CONST               'Numeric UID:GID are %d:%d'
              344  LOAD_FAST             0  'self'
              347  LOAD_ATTR            18  'unum'
              350  LOAD_FAST             0  'self'
              353  LOAD_ATTR            19  'gnum'
              356  BUILD_TUPLE_2         2 
              359  BINARY_MODULO    
              360  CALL_FUNCTION_1       1  None
              363  POP_TOP          

Parse error at or near `CALL_FUNCTION_1' instruction at offset 360

    def before_daemonize(self, args):
        pass

    def before_jail(self, args):
        pass

    def before_drop_privs(self, args):
        pass

    def start(self, args):
        pass

    def stop(self, args):
        log.info('Stopping server.')
        unix.kill_server(self.name, pid_file_path=self.pid_path)

    def status(self, args):
        print 'Server running at pid %d' % unix.pid_read(self.name, pid_file_path=self.pid_path)

    def shutdown(self, signal):
        pass

    def parse_cli(self, args):
        args.pop(0)
        if not args:
            log.error('Need a command like start, stop, status.')
            sys.exit(1)
        return (args[0], args[1:])

    def daemonize(self, args):
        log.setup(self.log_file)
        log.info('Daemonizing.')
        self.before_daemonize(args)
        if unix.still_running(self.name, pid_file_path=self.pid_path):
            log.error('%s still running. Aborting.' % self.name)
            sys.exit(1)
        else:
            unix.daemonize(self.name, pid_file_path=self.pid_path)

        def shutdown_handler(signal, frame):
            self.shutdown(signal)
            sys.exit(0)

        unix.register_shutdown(shutdown_handler)
        if not os.path.exists(self.run_dir):
            log.warn('Directory %s does not exist, attempting to create it.' % self.run_dir)
            os.mkdir(self.run_dir)
            log.info('Giving default permissions to %s, change them later if you need.' % self.run_dir)
            os.chown(self.run_dir, self.unum, self.gnum)
            os.chmod(self.run_dir, self.run_dir_mode)
        if self.should_jail:
            self.before_jail(args)
            log.info('Setting up the chroot jail to: %s' % self.run_dir)
            unix.chroot_jail(self.run_dir)
        else:
            log.warn('This daemon does not jail itself, chdir to %s instead' % self.run_dir)
            os.chdir(self.run_dir)
        if self.should_drop_priv:
            self.before_drop_privs(args)
            unix.drop_privileges(self.unum, self.gnum)
        else:
            log.warn('This daemon does not drop privileges.')
        log.info('Server %s running.' % self.name)
        self.start(args)

    def run(self, args):
        command, args = self.parse_cli(args)
        if command == 'start':
            self.daemonize(args)
        elif command == 'stop':
            self.stop(args)
        elif command == 'status':
            self.status(args)
        else:
            log.error('Invalid command: %s.  Commands are: start, stop, reload, status.')
            sys.exit(1)

    def get(self, name):
        """Simple convenience method that just uses the service's configured
        name to get a config value."""
        return self.config.get(self.name + '.' + name, None)

    def load_config(self, config_file):
        self.config_file = config_file
        log.debug('Config file at %s' % self.config_file)
        if os.path.exists(self.config_file):
            self.config = config.load_ini_file(self.config_file)
            log.debug('Loading config file %s contains %r' % (self.config_file,
             self.config))
        else:
            log.warn('No config file at %s, using defaults.' % self.config_file)
            self.config = {}