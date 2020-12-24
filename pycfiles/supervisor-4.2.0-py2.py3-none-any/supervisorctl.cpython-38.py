# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./build/lib/supervisor/supervisorctl.py
# Compiled at: 2019-06-16 14:41:06
# Size of source mod 2**32: 54678 bytes
"""supervisorctl -- control applications run by supervisord from the cmd line.

Usage: %s [options] [action [arguments]]

Options:
-c/--configuration FILENAME -- configuration file path (searches if not given)
-h/--help -- print usage message and exit
-i/--interactive -- start an interactive shell after executing commands
-s/--serverurl URL -- URL on which supervisord server is listening
     (default "http://localhost:9001").
-u/--username USERNAME -- username to use for authentication with server
-p/--password PASSWORD -- password to use for authentication with server
-r/--history-file -- keep a readline history (if readline is available)

action [arguments] -- see below

Actions are commands like "tail" or "stop".  If -i is specified or no action is
specified on the command line, a "shell" interpreting actions typed
interactively is started.  Use the action "help" to find out about available
actions.
"""
import cmd, errno, getpass, socket, sys, threading
from supervisor.compat import xmlrpclib
from supervisor.compat import urlparse
from supervisor.compat import unicode
from supervisor.compat import raw_input
from supervisor.compat import as_string
import supervisor.medusa as asyncore
from supervisor.options import ClientOptions
from supervisor.options import make_namespec
from supervisor.options import split_namespec
from supervisor import xmlrpc
from supervisor import states
from supervisor import http_client

class LSBInitExitStatuses:
    SUCCESS = 0
    GENERIC = 1
    INVALID_ARGS = 2
    UNIMPLEMENTED_FEATURE = 3
    INSUFFICIENT_PRIVILEGES = 4
    NOT_INSTALLED = 5
    NOT_RUNNING = 7


class LSBStatusExitStatuses:
    NOT_RUNNING = 3
    UNKNOWN = 4


DEAD_PROGRAM_FAULTS = (
 xmlrpc.Faults.SPAWN_ERROR,
 xmlrpc.Faults.ABNORMAL_TERMINATION,
 xmlrpc.Faults.NOT_RUNNING)

class fgthread(threading.Thread):
    __doc__ = ' A subclass of threading.Thread, with a kill() method.\n    To be used for foreground output/error streaming.\n    http://mail.python.org/pipermail/python-list/2004-May/260937.html\n    '

    def __init__(self, program, ctl):
        threading.Thread.__init__(self)
        self.killed = False
        self.program = program
        self.ctl = ctl
        self.listener = http_client.Listener()
        self.output_handler = http_client.HTTPHandler(self.listener, self.ctl.options.username, self.ctl.options.password)
        self.error_handler = http_client.HTTPHandler(self.listener, self.ctl.options.username, self.ctl.options.password)

    def start(self):
        self._fgthread__run_backup = self.run
        self.run = self._fgthread__run
        threading.Thread.start(self)

    def run(self):
        self.output_handler.get(self.ctl.options.serverurl, '/logtail/%s/stdout' % self.program)
        self.error_handler.get(self.ctl.options.serverurl, '/logtail/%s/stderr' % self.program)
        asyncore.loop()

    def __run(self):
        sys.settrace(self.globaltrace)
        self._fgthread__run_backup()
        self.run = self._fgthread__run_backup

    def globaltrace(self, frame, why, arg):
        if why == 'call':
            return self.localtrace
        return

    def localtrace(self, frame, why, arg):
        if self.killed:
            if why == 'line':
                raise SystemExit()
        return self.localtrace

    def kill(self):
        self.output_handler.close()
        self.error_handler.close()
        self.killed = True


class Controller(cmd.Cmd):

    def __init__(self, options, completekey='tab', stdin=None, stdout=None):
        self.options = options
        self.prompt = self.options.prompt + '> '
        self.options.plugins = []
        self.vocab = ['help']
        self._complete_info = None
        self.exitstatus = LSBInitExitStatuses.SUCCESS
        cmd.Cmd.__init__(self, completekey, stdin, stdout)
        for name, factory, kwargs in self.options.plugin_factories:
            plugin = factory(self, **kwargs)
            for a in dir(plugin):
                if a.startswith('do_'):
                    if callable(getattr(plugin, a)):
                        self.vocab.append(a[3:])
                    self.options.plugins.append(plugin)
                    plugin.name = name

    def emptyline(self):
        pass

    def default(self, line):
        self.output('*** Unknown syntax: %s' % line)
        self.exitstatus = LSBInitExitStatuses.GENERIC

    def exec_cmdloop(self, args, options):
        try:
            import readline
            delims = readline.get_completer_delims()
            delims = delims.replace(':', '')
            delims = delims.replace('*', '')
            delims = delims.replace('-', '')
            readline.set_completer_delims(delims)
            if options.history_file:
                try:
                    readline.read_history_file(options.history_file)
                except IOError:
                    pass
                else:

                    def save():
                        try:
                            readline.write_history_file(options.history_file)
                        except IOError:
                            pass

                    import atexit
                    atexit.register(save)
        except ImportError:
            pass

        try:
            self.cmdqueue.append('status')
            self.cmdloop()
        except KeyboardInterrupt:
            self.output('')

    def set_exitstatus_from_xmlrpc_fault(self, faultcode, ignored_faultcode=None):
        if faultcode in (ignored_faultcode, xmlrpc.Faults.SUCCESS):
            pass
        elif faultcode in DEAD_PROGRAM_FAULTS:
            self.exitstatus = LSBInitExitStatuses.NOT_RUNNING
        else:
            self.exitstatus = LSBInitExitStatuses.GENERIC

    def onecmd--- This code section failed: ---

 L. 191         0  LOAD_FAST                'self'
                2  LOAD_METHOD              parseline
                4  LOAD_FAST                'line'
                6  CALL_METHOD_1         1  ''
                8  UNPACK_SEQUENCE_3     3 
               10  STORE_FAST               'cmd'
               12  STORE_FAST               'arg'
               14  STORE_FAST               'line'

 L. 192        16  LOAD_FAST                'line'
               18  POP_JUMP_IF_TRUE     28  'to 28'

 L. 193        20  LOAD_FAST                'self'
               22  LOAD_METHOD              emptyline
               24  CALL_METHOD_0         0  ''
               26  RETURN_VALUE     
             28_0  COME_FROM            18  '18'

 L. 194        28  LOAD_FAST                'cmd'
               30  LOAD_CONST               None
               32  COMPARE_OP               is
               34  POP_JUMP_IF_FALSE    46  'to 46'

 L. 195        36  LOAD_FAST                'self'
               38  LOAD_METHOD              default
               40  LOAD_FAST                'line'
               42  CALL_METHOD_1         1  ''
               44  RETURN_VALUE     
             46_0  COME_FROM            34  '34'

 L. 196        46  LOAD_CONST               None
               48  LOAD_FAST                'self'
               50  STORE_ATTR               _complete_info

 L. 197        52  LOAD_FAST                'line'
               54  LOAD_FAST                'self'
               56  STORE_ATTR               lastcmd

 L. 199        58  LOAD_FAST                'cmd'
               60  LOAD_STR                 ''
               62  COMPARE_OP               ==
               64  POP_JUMP_IF_FALSE    76  'to 76'

 L. 200        66  LOAD_FAST                'self'
               68  LOAD_METHOD              default
               70  LOAD_FAST                'line'
               72  CALL_METHOD_1         1  ''
               74  RETURN_VALUE     
             76_0  COME_FROM            64  '64'

 L. 202        76  LOAD_FAST                'self'
               78  LOAD_METHOD              _get_do_func
               80  LOAD_FAST                'cmd'
               82  CALL_METHOD_1         1  ''
               84  STORE_FAST               'do_func'

 L. 203        86  LOAD_FAST                'do_func'
               88  LOAD_CONST               None
               90  COMPARE_OP               is
               92  POP_JUMP_IF_FALSE   104  'to 104'

 L. 204        94  LOAD_FAST                'self'
               96  LOAD_METHOD              default
               98  LOAD_FAST                'line'
              100  CALL_METHOD_1         1  ''
              102  RETURN_VALUE     
            104_0  COME_FROM            92  '92'

 L. 205       104  SETUP_FINALLY       296  'to 296'

 L. 206       106  SETUP_FINALLY       120  'to 120'

 L. 207       108  LOAD_FAST                'do_func'
              110  LOAD_FAST                'arg'
              112  CALL_FUNCTION_1       1  ''
              114  POP_BLOCK        
              116  POP_BLOCK        
              118  RETURN_VALUE     
            120_0  COME_FROM_FINALLY   106  '106'

 L. 208       120  DUP_TOP          
              122  LOAD_GLOBAL              xmlrpclib
              124  LOAD_ATTR                ProtocolError
              126  COMPARE_OP               exception-match
          128_130  POP_JUMP_IF_FALSE   282  'to 282'
              132  POP_TOP          
              134  STORE_FAST               'e'
              136  POP_TOP          
              138  SETUP_FINALLY       270  'to 270'

 L. 209       140  LOAD_FAST                'e'
              142  LOAD_ATTR                errcode
              144  LOAD_CONST               401
              146  COMPARE_OP               ==
          148_150  POP_JUMP_IF_FALSE   256  'to 256'

 L. 210       152  LOAD_FAST                'self'
              154  LOAD_ATTR                options
              156  LOAD_ATTR                interactive
              158  POP_JUMP_IF_FALSE   236  'to 236'

 L. 211       160  LOAD_FAST                'self'
              162  LOAD_METHOD              output
              164  LOAD_STR                 'Server requires authentication'
              166  CALL_METHOD_1         1  ''
              168  POP_TOP          

 L. 212       170  LOAD_GLOBAL              raw_input
              172  LOAD_STR                 'Username:'
              174  CALL_FUNCTION_1       1  ''
              176  STORE_FAST               'username'

 L. 213       178  LOAD_GLOBAL              getpass
              180  LOAD_ATTR                getpass
              182  LOAD_STR                 'Password:'
              184  LOAD_CONST               ('prompt',)
              186  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              188  STORE_FAST               'password'

 L. 214       190  LOAD_FAST                'self'
              192  LOAD_METHOD              output
              194  LOAD_STR                 ''
              196  CALL_METHOD_1         1  ''
              198  POP_TOP          

 L. 215       200  LOAD_FAST                'username'
              202  LOAD_FAST                'self'
              204  LOAD_ATTR                options
              206  STORE_ATTR               username

 L. 216       208  LOAD_FAST                'password'
              210  LOAD_FAST                'self'
              212  LOAD_ATTR                options
              214  STORE_ATTR               password

 L. 217       216  LOAD_FAST                'self'
              218  LOAD_METHOD              onecmd
              220  LOAD_FAST                'line'
              222  CALL_METHOD_1         1  ''
              224  ROT_FOUR         
              226  POP_BLOCK        
              228  POP_EXCEPT       
              230  CALL_FINALLY        270  'to 270'
              232  POP_BLOCK        
              234  RETURN_VALUE     
            236_0  COME_FROM           158  '158'

 L. 219       236  LOAD_FAST                'self'
              238  LOAD_METHOD              output
              240  LOAD_STR                 'Server requires authentication'
              242  CALL_METHOD_1         1  ''
              244  POP_TOP          

 L. 220       246  LOAD_GLOBAL              LSBInitExitStatuses
              248  LOAD_ATTR                GENERIC
              250  LOAD_FAST                'self'
              252  STORE_ATTR               exitstatus
              254  JUMP_FORWARD        266  'to 266'
            256_0  COME_FROM           148  '148'

 L. 222       256  LOAD_GLOBAL              LSBInitExitStatuses
              258  LOAD_ATTR                GENERIC
              260  LOAD_FAST                'self'
              262  STORE_ATTR               exitstatus

 L. 223       264  RAISE_VARARGS_0       0  'reraise'
            266_0  COME_FROM           254  '254'
              266  POP_BLOCK        
              268  BEGIN_FINALLY    
            270_0  COME_FROM           230  '230'
            270_1  COME_FROM_FINALLY   138  '138'
              270  LOAD_CONST               None
              272  STORE_FAST               'e'
              274  DELETE_FAST              'e'
              276  END_FINALLY      
              278  POP_EXCEPT       
              280  JUMP_FORWARD        284  'to 284'
            282_0  COME_FROM           128  '128'
              282  END_FINALLY      
            284_0  COME_FROM           280  '280'

 L. 224       284  LOAD_FAST                'do_func'
              286  LOAD_FAST                'arg'
              288  CALL_FUNCTION_1       1  ''
              290  POP_TOP          
              292  POP_BLOCK        
              294  JUMP_FORWARD        374  'to 374'
            296_0  COME_FROM_FINALLY   104  '104'

 L. 225       296  DUP_TOP          
              298  LOAD_GLOBAL              Exception
              300  COMPARE_OP               exception-match
          302_304  POP_JUMP_IF_FALSE   372  'to 372'
              306  POP_TOP          
              308  POP_TOP          
              310  POP_TOP          

 L. 226       312  LOAD_GLOBAL              asyncore
              314  LOAD_METHOD              compact_traceback
              316  CALL_METHOD_0         0  ''
              318  UNPACK_SEQUENCE_4     4 
              320  UNPACK_SEQUENCE_3     3 
              322  STORE_FAST               'file'
              324  STORE_FAST               'fun'
              326  STORE_FAST               'line'
              328  STORE_FAST               't'
              330  STORE_FAST               'v'
              332  STORE_FAST               'tbinfo'

 L. 227       334  LOAD_STR                 'error: %s, %s: file: %s line: %s'
              336  LOAD_FAST                't'
              338  LOAD_FAST                'v'
              340  LOAD_FAST                'file'
              342  LOAD_FAST                'line'
              344  BUILD_TUPLE_4         4 
              346  BINARY_MODULO    
              348  STORE_FAST               'error'

 L. 228       350  LOAD_FAST                'self'
              352  LOAD_METHOD              output
              354  LOAD_FAST                'error'
              356  CALL_METHOD_1         1  ''
              358  POP_TOP          

 L. 229       360  LOAD_GLOBAL              LSBInitExitStatuses
              362  LOAD_ATTR                GENERIC
              364  LOAD_FAST                'self'
              366  STORE_ATTR               exitstatus
              368  POP_EXCEPT       
              370  JUMP_FORWARD        374  'to 374'
            372_0  COME_FROM           302  '302'
              372  END_FINALLY      
            374_0  COME_FROM           370  '370'
            374_1  COME_FROM           294  '294'

Parse error at or near `POP_BLOCK' instruction at offset 116

    def _get_do_func(self, cmd):
        func_name = 'do_' + cmd
        func = getattr(self, func_name, None)
        for plugin in func or self.options.plugins:
            func = getattr(plugin, func_name, None)
            if func is not None:
                break
            else:
                return func

    def output(self, message):
        if isinstance(message, unicode):
            message = message.encode('utf-8')
        self.stdout.write(message + '\n')

    def get_supervisor(self):
        return self.get_server_proxy('supervisor')

    def get_server_proxy(self, namespace=None):
        proxy = self.options.getServerProxy()
        if namespace is None:
            return proxy
        return getattr(proxy, namespace)

    def upcheck--- This code section failed: ---

 L. 257         0  SETUP_FINALLY        78  'to 78'

 L. 258         2  LOAD_FAST                'self'
                4  LOAD_METHOD              get_supervisor
                6  CALL_METHOD_0         0  ''
                8  STORE_FAST               'supervisor'

 L. 259        10  LOAD_FAST                'supervisor'
               12  LOAD_METHOD              getVersion
               14  CALL_METHOD_0         0  ''
               16  STORE_FAST               'api'

 L. 260        18  LOAD_CONST               0
               20  LOAD_CONST               ('rpcinterface',)
               22  IMPORT_NAME              supervisor
               24  IMPORT_FROM              rpcinterface
               26  STORE_FAST               'rpcinterface'
               28  POP_TOP          

 L. 261        30  LOAD_FAST                'api'
               32  LOAD_FAST                'rpcinterface'
               34  LOAD_ATTR                API_VERSION
               36  COMPARE_OP               !=
               38  POP_JUMP_IF_FALSE    74  'to 74'

 L. 262        40  LOAD_FAST                'self'
               42  LOAD_METHOD              output

 L. 263        44  LOAD_STR                 'Sorry, this version of supervisorctl expects to talk to a server with API version %s, but the remote version is %s.'

 L. 265        46  LOAD_FAST                'rpcinterface'
               48  LOAD_ATTR                API_VERSION
               50  LOAD_FAST                'api'
               52  BUILD_TUPLE_2         2 

 L. 263        54  BINARY_MODULO    

 L. 262        56  CALL_METHOD_1         1  ''
               58  POP_TOP          

 L. 266        60  LOAD_GLOBAL              LSBInitExitStatuses
               62  LOAD_ATTR                NOT_INSTALLED
               64  LOAD_FAST                'self'
               66  STORE_ATTR               exitstatus

 L. 267        68  POP_BLOCK        
               70  LOAD_CONST               False
               72  RETURN_VALUE     
             74_0  COME_FROM            38  '38'
               74  POP_BLOCK        
               76  JUMP_FORWARD        318  'to 318'
             78_0  COME_FROM_FINALLY     0  '0'

 L. 268        78  DUP_TOP          
               80  LOAD_GLOBAL              xmlrpclib
               82  LOAD_ATTR                Fault
               84  COMPARE_OP               exception-match
               86  POP_JUMP_IF_FALSE   164  'to 164'
               88  POP_TOP          
               90  STORE_FAST               'e'
               92  POP_TOP          
               94  SETUP_FINALLY       152  'to 152'

 L. 269        96  LOAD_FAST                'e'
               98  LOAD_ATTR                faultCode
              100  LOAD_GLOBAL              xmlrpc
              102  LOAD_ATTR                Faults
              104  LOAD_ATTR                UNKNOWN_METHOD
              106  COMPARE_OP               ==
              108  POP_JUMP_IF_FALSE   138  'to 138'

 L. 270       110  LOAD_FAST                'self'
              112  LOAD_METHOD              output

 L. 271       114  LOAD_STR                 'Sorry, supervisord responded but did not recognize the supervisor namespace commands that supervisorctl uses to control it.  Please check that the [rpcinterface:supervisor] section is enabled in the configuration file (see sample.conf).'

 L. 270       116  CALL_METHOD_1         1  ''
              118  POP_TOP          

 L. 276       120  LOAD_GLOBAL              LSBInitExitStatuses
              122  LOAD_ATTR                UNIMPLEMENTED_FEATURE
              124  LOAD_FAST                'self'
              126  STORE_ATTR               exitstatus

 L. 277       128  POP_BLOCK        
              130  POP_EXCEPT       
              132  CALL_FINALLY        152  'to 152'
              134  LOAD_CONST               False
              136  RETURN_VALUE     
            138_0  COME_FROM           108  '108'

 L. 278       138  LOAD_GLOBAL              LSBInitExitStatuses
              140  LOAD_ATTR                GENERIC
              142  LOAD_FAST                'self'
              144  STORE_ATTR               exitstatus

 L. 279       146  RAISE_VARARGS_0       0  'reraise'
              148  POP_BLOCK        
              150  BEGIN_FINALLY    
            152_0  COME_FROM           132  '132'
            152_1  COME_FROM_FINALLY    94  '94'
              152  LOAD_CONST               None
              154  STORE_FAST               'e'
              156  DELETE_FAST              'e'
              158  END_FINALLY      
              160  POP_EXCEPT       
              162  JUMP_FORWARD        318  'to 318'
            164_0  COME_FROM            86  '86'

 L. 280       164  DUP_TOP          
              166  LOAD_GLOBAL              socket
              168  LOAD_ATTR                error
              170  COMPARE_OP               exception-match
          172_174  POP_JUMP_IF_FALSE   316  'to 316'
              176  POP_TOP          
              178  STORE_FAST               'e'
              180  POP_TOP          
              182  SETUP_FINALLY       304  'to 304'

 L. 281       184  LOAD_FAST                'e'
              186  LOAD_ATTR                args
              188  LOAD_CONST               0
              190  BINARY_SUBSCR    
              192  LOAD_GLOBAL              errno
              194  LOAD_ATTR                ECONNREFUSED
              196  COMPARE_OP               ==
              198  POP_JUMP_IF_FALSE   236  'to 236'

 L. 282       200  LOAD_FAST                'self'
              202  LOAD_METHOD              output
              204  LOAD_STR                 '%s refused connection'
              206  LOAD_FAST                'self'
              208  LOAD_ATTR                options
              210  LOAD_ATTR                serverurl
              212  BINARY_MODULO    
              214  CALL_METHOD_1         1  ''
              216  POP_TOP          

 L. 283       218  LOAD_GLOBAL              LSBInitExitStatuses
              220  LOAD_ATTR                INSUFFICIENT_PRIVILEGES
              222  LOAD_FAST                'self'
              224  STORE_ATTR               exitstatus

 L. 284       226  POP_BLOCK        
              228  POP_EXCEPT       
              230  CALL_FINALLY        304  'to 304'
              232  LOAD_CONST               False
              234  RETURN_VALUE     
            236_0  COME_FROM           198  '198'

 L. 285       236  LOAD_FAST                'e'
              238  LOAD_ATTR                args
              240  LOAD_CONST               0
              242  BINARY_SUBSCR    
              244  LOAD_GLOBAL              errno
              246  LOAD_ATTR                ENOENT
              248  COMPARE_OP               ==
          250_252  POP_JUMP_IF_FALSE   290  'to 290'

 L. 286       254  LOAD_FAST                'self'
              256  LOAD_METHOD              output
              258  LOAD_STR                 '%s no such file'
              260  LOAD_FAST                'self'
              262  LOAD_ATTR                options
              264  LOAD_ATTR                serverurl
              266  BINARY_MODULO    
              268  CALL_METHOD_1         1  ''
              270  POP_TOP          

 L. 287       272  LOAD_GLOBAL              LSBInitExitStatuses
              274  LOAD_ATTR                NOT_RUNNING
              276  LOAD_FAST                'self'
              278  STORE_ATTR               exitstatus

 L. 288       280  POP_BLOCK        
              282  POP_EXCEPT       
              284  CALL_FINALLY        304  'to 304'
              286  LOAD_CONST               False
              288  RETURN_VALUE     
            290_0  COME_FROM           250  '250'

 L. 289       290  LOAD_GLOBAL              LSBInitExitStatuses
              292  LOAD_ATTR                GENERIC
              294  LOAD_FAST                'self'
              296  STORE_ATTR               exitstatus

 L. 290       298  RAISE_VARARGS_0       0  'reraise'
              300  POP_BLOCK        
              302  BEGIN_FINALLY    
            304_0  COME_FROM           284  '284'
            304_1  COME_FROM           230  '230'
            304_2  COME_FROM_FINALLY   182  '182'
              304  LOAD_CONST               None
              306  STORE_FAST               'e'
              308  DELETE_FAST              'e'
              310  END_FINALLY      
              312  POP_EXCEPT       
              314  JUMP_FORWARD        318  'to 318'
            316_0  COME_FROM           172  '172'
              316  END_FINALLY      
            318_0  COME_FROM           314  '314'
            318_1  COME_FROM           162  '162'
            318_2  COME_FROM            76  '76'

 L. 291       318  LOAD_CONST               True
              320  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_CONST' instruction at offset 70

    def complete(self, text, state, line=None):
        """Completer function that Cmd will register with readline using
        readline.set_completer().  This function will be called by readline
        as complete(text, state) where text is a fragment to complete and
        state is an integer (0..n).  Each call returns a string with a new
        completion.  When no more are available, None is returned."""
        if line is None:
            import readline
            line = readline.get_line_buffer()
        else:
            matches = []
            if not line.strip():
                matches = self._complete_actions(text)
            else:
                words = line.split()
            action = words[0]
            if len(words) == 1:
                matches = line.endswith(' ') or self._complete_actions(text)
            else:
                if action in 'help':
                    matches = self._complete_actions(text)
                else:
                    if action in ('add', 'remove', 'update'):
                        matches = self._complete_groups(text)
                    else:
                        if action in ('clear', 'fg', 'pid', 'restart', 'signal', 'start',
                                      'status', 'stop', 'tail'):
                            matches = self._complete_processes(text)
        if len(matches) > state:
            return matches[state]

    def _complete_actions(self, text):
        """Build a completion list of action names matching text"""
        return [a + ' ' for a in self.vocab if a.startswith(text)]

    def _complete_groups(self, text):
        """Build a completion list of group names matching text"""
        groups = []
        for info in self._get_complete_info():
            if info['group'] not in groups:
                groups.append(info['group'])
            return [g + ' ' for g in groups if g.startswith(text)]

    def _complete_processes(self, text):
        """Build a completion list of process names matching text"""
        processes = []
        for info in self._get_complete_info():
            if ':' in text or info['name'] != info['group']:
                processes.append('%s:%s' % (info['group'], info['name']))
                if '%s:*' % info['group'] not in processes:
                    processes.append('%s:*' % info['group'])
                else:
                    processes.append(info['name'])
            else:
                return [p + ' ' for p in processes if p.startswith(text)]

    def _get_complete_info(self):
        """Get all process info used for completion.  We cache this between
        commands to reduce XML-RPC calls because readline may call
        complete() many times if the user hits tab only once."""
        if self._complete_info is None:
            self._complete_info = self.get_supervisor().getAllProcessInfo()
        return self._complete_info

    def do_help(self, arg):
        if arg.strip() == 'help':
            self.help_help()
        else:
            for plugin in self.options.plugins:
                plugin.do_help(arg)

    def help_help(self):
        self.output('help\t\tPrint a list of available actions')
        self.output('help <action>\tPrint help for <action>')

    def do_EOF(self, arg):
        self.output('')
        return 1

    def help_EOF(self):
        self.output('To quit, type ^D or use the quit command')


def get_names(inst):
    names = []
    classes = [
     inst.__class__]
    while classes:
        aclass = classes.pop(0)
        if aclass.__bases__:
            classes = classes + list(aclass.__bases__)
        names = names + dir(aclass)

    return names


class ControllerPluginBase:
    name = 'unnamed'

    def __init__(self, controller):
        self.ctl = controller

    def _doc_header(self):
        return '%s commands (type help <topic>):' % self.name

    doc_header = property(_doc_header)

    def do_help--- This code section failed: ---

 L. 397         0  LOAD_FAST                'arg'
                2  POP_JUMP_IF_FALSE   142  'to 142'

 L. 399         4  SETUP_FINALLY        24  'to 24'

 L. 400         6  LOAD_GLOBAL              getattr
                8  LOAD_FAST                'self'
               10  LOAD_STR                 'help_'
               12  LOAD_FAST                'arg'
               14  BINARY_ADD       
               16  CALL_FUNCTION_2       2  ''
               18  STORE_FAST               'func'
               20  POP_BLOCK        
               22  JUMP_FORWARD        134  'to 134'
             24_0  COME_FROM_FINALLY     4  '4'

 L. 401        24  DUP_TOP          
               26  LOAD_GLOBAL              AttributeError
               28  COMPARE_OP               exception-match
               30  POP_JUMP_IF_FALSE   132  'to 132'
               32  POP_TOP          
               34  POP_TOP          
               36  POP_TOP          

 L. 402        38  SETUP_FINALLY        84  'to 84'

 L. 403        40  LOAD_GLOBAL              getattr
               42  LOAD_FAST                'self'
               44  LOAD_STR                 'do_'
               46  LOAD_FAST                'arg'
               48  BINARY_ADD       
               50  CALL_FUNCTION_2       2  ''
               52  LOAD_ATTR                __doc__
               54  STORE_FAST               'doc'

 L. 404        56  LOAD_FAST                'doc'
               58  POP_JUMP_IF_FALSE    80  'to 80'

 L. 405        60  LOAD_FAST                'self'
               62  LOAD_ATTR                ctl
               64  LOAD_METHOD              output
               66  LOAD_FAST                'doc'
               68  CALL_METHOD_1         1  ''
               70  POP_TOP          

 L. 406        72  POP_BLOCK        
               74  POP_EXCEPT       
               76  LOAD_CONST               None
               78  RETURN_VALUE     
             80_0  COME_FROM            58  '58'
               80  POP_BLOCK        
               82  JUMP_FORWARD        104  'to 104'
             84_0  COME_FROM_FINALLY    38  '38'

 L. 407        84  DUP_TOP          
               86  LOAD_GLOBAL              AttributeError
               88  COMPARE_OP               exception-match
               90  POP_JUMP_IF_FALSE   102  'to 102'
               92  POP_TOP          
               94  POP_TOP          
               96  POP_TOP          

 L. 408        98  POP_EXCEPT       
              100  JUMP_FORWARD        104  'to 104'
            102_0  COME_FROM            90  '90'
              102  END_FINALLY      
            104_0  COME_FROM           100  '100'
            104_1  COME_FROM            82  '82'

 L. 409       104  LOAD_FAST                'self'
              106  LOAD_ATTR                ctl
              108  LOAD_METHOD              output
              110  LOAD_FAST                'self'
              112  LOAD_ATTR                ctl
              114  LOAD_ATTR                nohelp
              116  LOAD_FAST                'arg'
              118  BUILD_TUPLE_1         1 
              120  BINARY_MODULO    
              122  CALL_METHOD_1         1  ''
              124  POP_TOP          

 L. 410       126  POP_EXCEPT       
              128  LOAD_CONST               None
              130  RETURN_VALUE     
            132_0  COME_FROM            30  '30'
              132  END_FINALLY      
            134_0  COME_FROM            22  '22'

 L. 411       134  LOAD_FAST                'func'
              136  CALL_FUNCTION_0       0  ''
              138  POP_TOP          
              140  JUMP_FORWARD        366  'to 366'
            142_0  COME_FROM             2  '2'

 L. 413       142  LOAD_GLOBAL              get_names
              144  LOAD_FAST                'self'
              146  CALL_FUNCTION_1       1  ''
              148  STORE_FAST               'names'

 L. 414       150  BUILD_LIST_0          0 
              152  STORE_FAST               'cmds_doc'

 L. 415       154  BUILD_LIST_0          0 
              156  STORE_FAST               'cmds_undoc'

 L. 416       158  BUILD_MAP_0           0 
              160  STORE_FAST               'help'

 L. 417       162  LOAD_FAST                'names'
              164  GET_ITER         
            166_0  COME_FROM           184  '184'
              166  FOR_ITER            204  'to 204'
              168  STORE_FAST               'name'

 L. 418       170  LOAD_FAST                'name'
              172  LOAD_CONST               None
              174  LOAD_CONST               5
              176  BUILD_SLICE_2         2 
              178  BINARY_SUBSCR    
              180  LOAD_STR                 'help_'
              182  COMPARE_OP               ==
              184  POP_JUMP_IF_FALSE   166  'to 166'

 L. 419       186  LOAD_CONST               1
              188  LOAD_FAST                'help'
              190  LOAD_FAST                'name'
              192  LOAD_CONST               5
              194  LOAD_CONST               None
              196  BUILD_SLICE_2         2 
              198  BINARY_SUBSCR    
              200  STORE_SUBSCR     
              202  JUMP_BACK           166  'to 166'

 L. 420       204  LOAD_FAST                'names'
              206  LOAD_METHOD              sort
              208  CALL_METHOD_0         0  ''
              210  POP_TOP          

 L. 422       212  LOAD_STR                 ''
              214  STORE_FAST               'prevname'

 L. 423       216  LOAD_FAST                'names'
              218  GET_ITER         
            220_0  COME_FROM           238  '238'
              220  FOR_ITER            334  'to 334'
              222  STORE_FAST               'name'

 L. 424       224  LOAD_FAST                'name'
              226  LOAD_CONST               None
              228  LOAD_CONST               3
              230  BUILD_SLICE_2         2 
              232  BINARY_SUBSCR    
              234  LOAD_STR                 'do_'
              236  COMPARE_OP               ==
              238  POP_JUMP_IF_FALSE   220  'to 220'

 L. 425       240  LOAD_FAST                'name'
              242  LOAD_FAST                'prevname'
              244  COMPARE_OP               ==
          246_248  POP_JUMP_IF_FALSE   252  'to 252'

 L. 426       250  JUMP_BACK           220  'to 220'
            252_0  COME_FROM           246  '246'

 L. 427       252  LOAD_FAST                'name'
              254  STORE_FAST               'prevname'

 L. 428       256  LOAD_FAST                'name'
              258  LOAD_CONST               3
              260  LOAD_CONST               None
              262  BUILD_SLICE_2         2 
              264  BINARY_SUBSCR    
              266  STORE_FAST               'cmd'

 L. 429       268  LOAD_FAST                'cmd'
              270  LOAD_FAST                'help'
              272  COMPARE_OP               in
          274_276  POP_JUMP_IF_FALSE   296  'to 296'

 L. 430       278  LOAD_FAST                'cmds_doc'
              280  LOAD_METHOD              append
              282  LOAD_FAST                'cmd'
              284  CALL_METHOD_1         1  ''
              286  POP_TOP          

 L. 431       288  LOAD_FAST                'help'
              290  LOAD_FAST                'cmd'
              292  DELETE_SUBSCR    
              294  JUMP_BACK           220  'to 220'
            296_0  COME_FROM           274  '274'

 L. 432       296  LOAD_GLOBAL              getattr
              298  LOAD_FAST                'self'
              300  LOAD_FAST                'name'
              302  CALL_FUNCTION_2       2  ''
              304  LOAD_ATTR                __doc__
          306_308  POP_JUMP_IF_FALSE   322  'to 322'

 L. 433       310  LOAD_FAST                'cmds_doc'
              312  LOAD_METHOD              append
              314  LOAD_FAST                'cmd'
              316  CALL_METHOD_1         1  ''
              318  POP_TOP          
              320  JUMP_BACK           220  'to 220'
            322_0  COME_FROM           306  '306'

 L. 435       322  LOAD_FAST                'cmds_undoc'
              324  LOAD_METHOD              append
              326  LOAD_FAST                'cmd'
              328  CALL_METHOD_1         1  ''
              330  POP_TOP          
              332  JUMP_BACK           220  'to 220'

 L. 436       334  LOAD_FAST                'self'
              336  LOAD_ATTR                ctl
              338  LOAD_METHOD              output
              340  LOAD_STR                 ''
              342  CALL_METHOD_1         1  ''
              344  POP_TOP          

 L. 437       346  LOAD_FAST                'self'
              348  LOAD_ATTR                ctl
              350  LOAD_METHOD              print_topics
              352  LOAD_FAST                'self'
              354  LOAD_ATTR                doc_header
              356  LOAD_FAST                'cmds_doc'
              358  LOAD_CONST               15
              360  LOAD_CONST               80
              362  CALL_METHOD_4         4  ''
              364  POP_TOP          
            366_0  COME_FROM           140  '140'

Parse error at or near `POP_EXCEPT' instruction at offset 74


def not_all_langs():
    enc = getattr(sys.stdout, 'encoding', '').lower()
    if enc.startswith('utf'):
        return
    return sys.stdout.encoding


def check_encoding(ctl):
    problematic_enc = not_all_langs()
    if problematic_enc:
        ctl.output('Warning: sys.stdout.encoding is set to %s, so Unicode output may fail. Check your LANG and PYTHONIOENCODING environment settings.' % problematic_enc)


class DefaultControllerPlugin(ControllerPluginBase):
    name = 'default'
    listener = None

    def _tailf--- This code section failed: ---

 L. 454         0  LOAD_GLOBAL              check_encoding
                2  LOAD_FAST                'self'
                4  LOAD_ATTR                ctl
                6  CALL_FUNCTION_1       1  ''
                8  POP_TOP          

 L. 455        10  LOAD_FAST                'self'
               12  LOAD_ATTR                ctl
               14  LOAD_METHOD              output
               16  LOAD_STR                 '==> Press Ctrl-C to exit <=='
               18  CALL_METHOD_1         1  ''
               20  POP_TOP          

 L. 457        22  LOAD_FAST                'self'
               24  LOAD_ATTR                ctl
               26  LOAD_ATTR                options
               28  LOAD_ATTR                username
               30  STORE_FAST               'username'

 L. 458        32  LOAD_FAST                'self'
               34  LOAD_ATTR                ctl
               36  LOAD_ATTR                options
               38  LOAD_ATTR                password
               40  STORE_FAST               'password'

 L. 459        42  LOAD_CONST               None
               44  STORE_FAST               'handler'

 L. 460        46  SETUP_FINALLY       118  'to 118'

 L. 467        48  LOAD_FAST                'self'
               50  LOAD_ATTR                listener
               52  LOAD_CONST               None
               54  COMPARE_OP               is
               56  POP_JUMP_IF_FALSE    68  'to 68'

 L. 468        58  LOAD_GLOBAL              http_client
               60  LOAD_METHOD              Listener
               62  CALL_METHOD_0         0  ''
               64  STORE_FAST               'listener'
               66  JUMP_FORWARD         74  'to 74'
             68_0  COME_FROM            56  '56'

 L. 470        68  LOAD_FAST                'self'
               70  LOAD_ATTR                listener
               72  STORE_FAST               'listener'
             74_0  COME_FROM            66  '66'

 L. 471        74  LOAD_GLOBAL              http_client
               76  LOAD_METHOD              HTTPHandler
               78  LOAD_FAST                'listener'
               80  LOAD_FAST                'username'
               82  LOAD_FAST                'password'
               84  CALL_METHOD_3         3  ''
               86  STORE_FAST               'handler'

 L. 472        88  LOAD_FAST                'handler'
               90  LOAD_METHOD              get
               92  LOAD_FAST                'self'
               94  LOAD_ATTR                ctl
               96  LOAD_ATTR                options
               98  LOAD_ATTR                serverurl
              100  LOAD_FAST                'path'
              102  CALL_METHOD_2         2  ''
              104  POP_TOP          

 L. 473       106  LOAD_GLOBAL              asyncore
              108  LOAD_METHOD              loop
              110  CALL_METHOD_0         0  ''
              112  POP_TOP          
              114  POP_BLOCK        
              116  JUMP_FORWARD        164  'to 164'
            118_0  COME_FROM_FINALLY    46  '46'

 L. 474       118  DUP_TOP          
              120  LOAD_GLOBAL              KeyboardInterrupt
              122  COMPARE_OP               exception-match
              124  POP_JUMP_IF_FALSE   162  'to 162'
              126  POP_TOP          
              128  POP_TOP          
              130  POP_TOP          

 L. 475       132  LOAD_FAST                'handler'
              134  POP_JUMP_IF_FALSE   144  'to 144'

 L. 476       136  LOAD_FAST                'handler'
              138  LOAD_METHOD              close
              140  CALL_METHOD_0         0  ''
              142  POP_TOP          
            144_0  COME_FROM           134  '134'

 L. 477       144  LOAD_FAST                'self'
              146  LOAD_ATTR                ctl
              148  LOAD_METHOD              output
              150  LOAD_STR                 ''
              152  CALL_METHOD_1         1  ''
              154  POP_TOP          

 L. 478       156  POP_EXCEPT       
              158  LOAD_CONST               None
              160  RETURN_VALUE     
            162_0  COME_FROM           124  '124'
              162  END_FINALLY      
            164_0  COME_FROM           116  '116'

Parse error at or near `LOAD_CONST' instruction at offset 158

    def do_tail--- This code section failed: ---

 L. 481         0  LOAD_FAST                'self'
                2  LOAD_ATTR                ctl
                4  LOAD_METHOD              upcheck
                6  CALL_METHOD_0         0  ''
                8  POP_JUMP_IF_TRUE     14  'to 14'

 L. 482        10  LOAD_CONST               None
               12  RETURN_VALUE     
             14_0  COME_FROM             8  '8'

 L. 484        14  LOAD_FAST                'arg'
               16  LOAD_METHOD              split
               18  CALL_METHOD_0         0  ''
               20  STORE_FAST               'args'

 L. 486        22  LOAD_GLOBAL              len
               24  LOAD_FAST                'args'
               26  CALL_FUNCTION_1       1  ''
               28  LOAD_CONST               1
               30  COMPARE_OP               <
               32  POP_JUMP_IF_FALSE    68  'to 68'

 L. 487        34  LOAD_FAST                'self'
               36  LOAD_ATTR                ctl
               38  LOAD_METHOD              output
               40  LOAD_STR                 'Error: too few arguments'
               42  CALL_METHOD_1         1  ''
               44  POP_TOP          

 L. 488        46  LOAD_GLOBAL              LSBInitExitStatuses
               48  LOAD_ATTR                GENERIC
               50  LOAD_FAST                'self'
               52  LOAD_ATTR                ctl
               54  STORE_ATTR               exitstatus

 L. 489        56  LOAD_FAST                'self'
               58  LOAD_METHOD              help_tail
               60  CALL_METHOD_0         0  ''
               62  POP_TOP          

 L. 490        64  LOAD_CONST               None
               66  RETURN_VALUE     
             68_0  COME_FROM            32  '32'

 L. 492        68  LOAD_GLOBAL              len
               70  LOAD_FAST                'args'
               72  CALL_FUNCTION_1       1  ''
               74  LOAD_CONST               3
               76  COMPARE_OP               >
               78  POP_JUMP_IF_FALSE   114  'to 114'

 L. 493        80  LOAD_FAST                'self'
               82  LOAD_ATTR                ctl
               84  LOAD_METHOD              output
               86  LOAD_STR                 'Error: too many arguments'
               88  CALL_METHOD_1         1  ''
               90  POP_TOP          

 L. 494        92  LOAD_GLOBAL              LSBInitExitStatuses
               94  LOAD_ATTR                GENERIC
               96  LOAD_FAST                'self'
               98  LOAD_ATTR                ctl
              100  STORE_ATTR               exitstatus

 L. 495       102  LOAD_FAST                'self'
              104  LOAD_METHOD              help_tail
              106  CALL_METHOD_0         0  ''
              108  POP_TOP          

 L. 496       110  LOAD_CONST               None
              112  RETURN_VALUE     
            114_0  COME_FROM            78  '78'

 L. 498       114  LOAD_CONST               None
              116  STORE_FAST               'modifier'

 L. 500       118  LOAD_FAST                'args'
              120  LOAD_CONST               0
              122  BINARY_SUBSCR    
              124  LOAD_METHOD              startswith
              126  LOAD_STR                 '-'
              128  CALL_METHOD_1         1  ''
              130  POP_JUMP_IF_FALSE   142  'to 142'

 L. 501       132  LOAD_FAST                'args'
              134  LOAD_METHOD              pop
              136  LOAD_CONST               0
              138  CALL_METHOD_1         1  ''
              140  STORE_FAST               'modifier'
            142_0  COME_FROM           130  '130'

 L. 503       142  LOAD_GLOBAL              len
              144  LOAD_FAST                'args'
              146  CALL_FUNCTION_1       1  ''
              148  LOAD_CONST               1
              150  COMPARE_OP               ==
              152  POP_JUMP_IF_FALSE   168  'to 168'

 L. 504       154  LOAD_FAST                'args'
              156  LOAD_CONST               -1
              158  BINARY_SUBSCR    
              160  STORE_FAST               'name'

 L. 505       162  LOAD_STR                 'stdout'
              164  STORE_FAST               'channel'
              166  JUMP_FORWARD        258  'to 258'
            168_0  COME_FROM           152  '152'

 L. 507       168  LOAD_FAST                'args'
              170  POP_JUMP_IF_FALSE   232  'to 232'

 L. 508       172  LOAD_FAST                'args'
              174  LOAD_CONST               0
              176  BINARY_SUBSCR    
              178  STORE_FAST               'name'

 L. 509       180  LOAD_FAST                'args'
              182  LOAD_CONST               -1
              184  BINARY_SUBSCR    
              186  LOAD_METHOD              lower
              188  CALL_METHOD_0         0  ''
              190  STORE_FAST               'channel'

 L. 510       192  LOAD_FAST                'channel'
              194  LOAD_CONST               ('stderr', 'stdout')
              196  COMPARE_OP               not-in
              198  POP_JUMP_IF_FALSE   230  'to 230'

 L. 511       200  LOAD_FAST                'self'
              202  LOAD_ATTR                ctl
              204  LOAD_METHOD              output
              206  LOAD_STR                 'Error: bad channel %r'
              208  LOAD_FAST                'channel'
              210  BINARY_MODULO    
              212  CALL_METHOD_1         1  ''
              214  POP_TOP          

 L. 512       216  LOAD_GLOBAL              LSBInitExitStatuses
              218  LOAD_ATTR                GENERIC
              220  LOAD_FAST                'self'
              222  LOAD_ATTR                ctl
              224  STORE_ATTR               exitstatus

 L. 513       226  LOAD_CONST               None
              228  RETURN_VALUE     
            230_0  COME_FROM           198  '198'
              230  JUMP_FORWARD        258  'to 258'
            232_0  COME_FROM           170  '170'

 L. 515       232  LOAD_FAST                'self'
              234  LOAD_ATTR                ctl
              236  LOAD_METHOD              output
              238  LOAD_STR                 'Error: tail requires process name'
              240  CALL_METHOD_1         1  ''
              242  POP_TOP          

 L. 516       244  LOAD_GLOBAL              LSBInitExitStatuses
              246  LOAD_ATTR                GENERIC
              248  LOAD_FAST                'self'
              250  LOAD_ATTR                ctl
              252  STORE_ATTR               exitstatus

 L. 517       254  LOAD_CONST               None
              256  RETURN_VALUE     
            258_0  COME_FROM           230  '230'
            258_1  COME_FROM           166  '166'

 L. 519       258  LOAD_CONST               1600
              260  STORE_FAST               'bytes'

 L. 521       262  LOAD_FAST                'modifier'
              264  LOAD_CONST               None
              266  COMPARE_OP               is-not
          268_270  POP_JUMP_IF_FALSE   354  'to 354'

 L. 522       272  LOAD_FAST                'modifier'
              274  LOAD_CONST               1
              276  LOAD_CONST               None
              278  BUILD_SLICE_2         2 
              280  BINARY_SUBSCR    
              282  STORE_FAST               'what'

 L. 523       284  LOAD_FAST                'what'
              286  LOAD_STR                 'f'
              288  COMPARE_OP               ==
          290_292  POP_JUMP_IF_FALSE   300  'to 300'

 L. 524       294  LOAD_CONST               None
              296  STORE_FAST               'bytes'
              298  JUMP_FORWARD        354  'to 354'
            300_0  COME_FROM           290  '290'

 L. 526       300  SETUP_FINALLY       314  'to 314'

 L. 527       302  LOAD_GLOBAL              int
              304  LOAD_FAST                'what'
              306  CALL_FUNCTION_1       1  ''
              308  STORE_FAST               'bytes'
              310  POP_BLOCK        
              312  JUMP_FORWARD        354  'to 354'
            314_0  COME_FROM_FINALLY   300  '300'

 L. 528       314  POP_TOP          
              316  POP_TOP          
              318  POP_TOP          

 L. 529       320  LOAD_FAST                'self'
              322  LOAD_ATTR                ctl
              324  LOAD_METHOD              output
              326  LOAD_STR                 'Error: bad argument %s'
              328  LOAD_FAST                'modifier'
              330  BINARY_MODULO    
              332  CALL_METHOD_1         1  ''
              334  POP_TOP          

 L. 530       336  LOAD_GLOBAL              LSBInitExitStatuses
              338  LOAD_ATTR                GENERIC
              340  LOAD_FAST                'self'
              342  LOAD_ATTR                ctl
              344  STORE_ATTR               exitstatus

 L. 531       346  POP_EXCEPT       
              348  LOAD_CONST               None
              350  RETURN_VALUE     
              352  END_FINALLY      
            354_0  COME_FROM           312  '312'
            354_1  COME_FROM           298  '298'
            354_2  COME_FROM           268  '268'

 L. 533       354  LOAD_FAST                'self'
              356  LOAD_ATTR                ctl
              358  LOAD_METHOD              get_supervisor
              360  CALL_METHOD_0         0  ''
              362  STORE_FAST               'supervisor'

 L. 535       364  LOAD_FAST                'bytes'
              366  LOAD_CONST               None
              368  COMPARE_OP               is
          370_372  POP_JUMP_IF_FALSE   392  'to 392'

 L. 536       374  LOAD_FAST                'self'
              376  LOAD_METHOD              _tailf
              378  LOAD_STR                 '/logtail/%s/%s'
              380  LOAD_FAST                'name'
              382  LOAD_FAST                'channel'
              384  BUILD_TUPLE_2         2 
              386  BINARY_MODULO    
              388  CALL_METHOD_1         1  ''
              390  RETURN_VALUE     
            392_0  COME_FROM           370  '370'

 L. 539       392  LOAD_GLOBAL              check_encoding
              394  LOAD_FAST                'self'
              396  LOAD_ATTR                ctl
              398  CALL_FUNCTION_1       1  ''
              400  POP_TOP          

 L. 540       402  SETUP_FINALLY       452  'to 452'

 L. 541       404  LOAD_FAST                'channel'
              406  LOAD_STR                 'stdout'
              408  COMPARE_OP               ==
          410_412  POP_JUMP_IF_FALSE   432  'to 432'

 L. 542       414  LOAD_FAST                'supervisor'
              416  LOAD_METHOD              readProcessStdoutLog
              418  LOAD_FAST                'name'

 L. 543       420  LOAD_FAST                'bytes'
              422  UNARY_NEGATIVE   

 L. 543       424  LOAD_CONST               0

 L. 542       426  CALL_METHOD_3         3  ''
              428  STORE_FAST               'output'
              430  JUMP_FORWARD        448  'to 448'
            432_0  COME_FROM           410  '410'

 L. 545       432  LOAD_FAST                'supervisor'
              434  LOAD_METHOD              readProcessStderrLog
              436  LOAD_FAST                'name'

 L. 546       438  LOAD_FAST                'bytes'
              440  UNARY_NEGATIVE   

 L. 546       442  LOAD_CONST               0

 L. 545       444  CALL_METHOD_3         3  ''
              446  STORE_FAST               'output'
            448_0  COME_FROM           430  '430'
              448  POP_BLOCK        
              450  JUMP_FORWARD        620  'to 620'
            452_0  COME_FROM_FINALLY   402  '402'

 L. 547       452  DUP_TOP          
              454  LOAD_GLOBAL              xmlrpclib
              456  LOAD_ATTR                Fault
              458  COMPARE_OP               exception-match
          460_462  POP_JUMP_IF_FALSE   618  'to 618'
              464  POP_TOP          
              466  STORE_FAST               'e'
              468  POP_TOP          
              470  SETUP_FINALLY       606  'to 606'

 L. 548       472  LOAD_GLOBAL              LSBInitExitStatuses
              474  LOAD_ATTR                GENERIC
              476  LOAD_FAST                'self'
              478  LOAD_ATTR                ctl
              480  STORE_ATTR               exitstatus

 L. 549       482  LOAD_STR                 '%s: ERROR (%s)'
              484  STORE_FAST               'template'

 L. 550       486  LOAD_FAST                'e'
              488  LOAD_ATTR                faultCode
              490  LOAD_GLOBAL              xmlrpc
              492  LOAD_ATTR                Faults
              494  LOAD_ATTR                NO_FILE
              496  COMPARE_OP               ==
          498_500  POP_JUMP_IF_FALSE   524  'to 524'

 L. 551       502  LOAD_FAST                'self'
              504  LOAD_ATTR                ctl
              506  LOAD_METHOD              output
              508  LOAD_FAST                'template'
              510  LOAD_FAST                'name'
              512  LOAD_STR                 'no log file'
              514  BUILD_TUPLE_2         2 
              516  BINARY_MODULO    
              518  CALL_METHOD_1         1  ''
              520  POP_TOP          
              522  JUMP_FORWARD        602  'to 602'
            524_0  COME_FROM           498  '498'

 L. 552       524  LOAD_FAST                'e'
              526  LOAD_ATTR                faultCode
              528  LOAD_GLOBAL              xmlrpc
              530  LOAD_ATTR                Faults
              532  LOAD_ATTR                FAILED
              534  COMPARE_OP               ==
          536_538  POP_JUMP_IF_FALSE   562  'to 562'

 L. 553       540  LOAD_FAST                'self'
              542  LOAD_ATTR                ctl
              544  LOAD_METHOD              output
              546  LOAD_FAST                'template'
              548  LOAD_FAST                'name'

 L. 554       550  LOAD_STR                 'unknown error reading log'

 L. 553       552  BUILD_TUPLE_2         2 
              554  BINARY_MODULO    
              556  CALL_METHOD_1         1  ''
              558  POP_TOP          
              560  JUMP_FORWARD        602  'to 602'
            562_0  COME_FROM           536  '536'

 L. 555       562  LOAD_FAST                'e'
              564  LOAD_ATTR                faultCode
              566  LOAD_GLOBAL              xmlrpc
              568  LOAD_ATTR                Faults
              570  LOAD_ATTR                BAD_NAME
              572  COMPARE_OP               ==
          574_576  POP_JUMP_IF_FALSE   600  'to 600'

 L. 556       578  LOAD_FAST                'self'
              580  LOAD_ATTR                ctl
              582  LOAD_METHOD              output
              584  LOAD_FAST                'template'
              586  LOAD_FAST                'name'

 L. 557       588  LOAD_STR                 'no such process name'

 L. 556       590  BUILD_TUPLE_2         2 
              592  BINARY_MODULO    
              594  CALL_METHOD_1         1  ''
              596  POP_TOP          
              598  JUMP_FORWARD        602  'to 602'
            600_0  COME_FROM           574  '574'

 L. 559       600  RAISE_VARARGS_0       0  'reraise'
            602_0  COME_FROM           598  '598'
            602_1  COME_FROM           560  '560'
            602_2  COME_FROM           522  '522'
              602  POP_BLOCK        
              604  BEGIN_FINALLY    
            606_0  COME_FROM_FINALLY   470  '470'
              606  LOAD_CONST               None
              608  STORE_FAST               'e'
              610  DELETE_FAST              'e'
              612  END_FINALLY      
              614  POP_EXCEPT       
              616  JUMP_FORWARD        632  'to 632'
            618_0  COME_FROM           460  '460'
              618  END_FINALLY      
            620_0  COME_FROM           450  '450'

 L. 561       620  LOAD_FAST                'self'
              622  LOAD_ATTR                ctl
              624  LOAD_METHOD              output
              626  LOAD_FAST                'output'
              628  CALL_METHOD_1         1  ''
              630  POP_TOP          
            632_0  COME_FROM           616  '616'

Parse error at or near `LOAD_CONST' instruction at offset 348

    def help_tail(self):
        self.ctl.output('tail [-f] <name> [stdout|stderr] (default stdout)\nEx:\ntail -f <name>\t\tContinuous tail of named process stdout\n\t\t\tCtrl-C to exit.\ntail -100 <name>\tlast 100 *bytes* of process stdout\ntail <name> stderr\tlast 1600 *bytes* of process stderr')

    def do_maintail--- This code section failed: ---

 L. 574         0  LOAD_FAST                'self'
                2  LOAD_ATTR                ctl
                4  LOAD_METHOD              upcheck
                6  CALL_METHOD_0         0  ''
                8  POP_JUMP_IF_TRUE     14  'to 14'

 L. 575        10  LOAD_CONST               None
               12  RETURN_VALUE     
             14_0  COME_FROM             8  '8'

 L. 577        14  LOAD_FAST                'arg'
               16  LOAD_METHOD              split
               18  CALL_METHOD_0         0  ''
               20  STORE_FAST               'args'

 L. 579        22  LOAD_GLOBAL              len
               24  LOAD_FAST                'args'
               26  CALL_FUNCTION_1       1  ''
               28  LOAD_CONST               1
               30  COMPARE_OP               >
               32  POP_JUMP_IF_FALSE    68  'to 68'

 L. 580        34  LOAD_FAST                'self'
               36  LOAD_ATTR                ctl
               38  LOAD_METHOD              output
               40  LOAD_STR                 'Error: too many arguments'
               42  CALL_METHOD_1         1  ''
               44  POP_TOP          

 L. 581        46  LOAD_GLOBAL              LSBInitExitStatuses
               48  LOAD_ATTR                GENERIC
               50  LOAD_FAST                'self'
               52  LOAD_ATTR                ctl
               54  STORE_ATTR               exitstatus

 L. 582        56  LOAD_FAST                'self'
               58  LOAD_METHOD              help_maintail
               60  CALL_METHOD_0         0  ''
               62  POP_TOP          

 L. 583        64  LOAD_CONST               None
               66  RETURN_VALUE     
             68_0  COME_FROM            32  '32'

 L. 585        68  LOAD_GLOBAL              len
               70  LOAD_FAST                'args'
               72  CALL_FUNCTION_1       1  ''
               74  LOAD_CONST               1
               76  COMPARE_OP               ==
               78  POP_JUMP_IF_FALSE   232  'to 232'

 L. 586        80  LOAD_FAST                'args'
               82  LOAD_CONST               0
               84  BINARY_SUBSCR    
               86  LOAD_METHOD              startswith
               88  LOAD_STR                 '-'
               90  CALL_METHOD_1         1  ''
               92  POP_JUMP_IF_FALSE   196  'to 196'

 L. 587        94  LOAD_FAST                'args'
               96  LOAD_CONST               0
               98  BINARY_SUBSCR    
              100  LOAD_CONST               1
              102  LOAD_CONST               None
              104  BUILD_SLICE_2         2 
              106  BINARY_SUBSCR    
              108  STORE_FAST               'what'

 L. 588       110  LOAD_FAST                'what'
              112  LOAD_STR                 'f'
              114  COMPARE_OP               ==
              116  POP_JUMP_IF_FALSE   132  'to 132'

 L. 589       118  LOAD_STR                 '/mainlogtail'
              120  STORE_FAST               'path'

 L. 590       122  LOAD_FAST                'self'
              124  LOAD_METHOD              _tailf
              126  LOAD_FAST                'path'
              128  CALL_METHOD_1         1  ''
              130  RETURN_VALUE     
            132_0  COME_FROM           116  '116'

 L. 591       132  SETUP_FINALLY       146  'to 146'

 L. 592       134  LOAD_GLOBAL              int
              136  LOAD_FAST                'what'
              138  CALL_FUNCTION_1       1  ''
              140  STORE_FAST               'what'
              142  POP_BLOCK        
              144  JUMP_FORWARD        190  'to 190'
            146_0  COME_FROM_FINALLY   132  '132'

 L. 593       146  POP_TOP          
              148  POP_TOP          
              150  POP_TOP          

 L. 594       152  LOAD_FAST                'self'
              154  LOAD_ATTR                ctl
              156  LOAD_METHOD              output
              158  LOAD_STR                 'Error: bad argument %s'
              160  LOAD_FAST                'args'
              162  LOAD_CONST               0
              164  BINARY_SUBSCR    
              166  BINARY_MODULO    
              168  CALL_METHOD_1         1  ''
              170  POP_TOP          

 L. 595       172  LOAD_GLOBAL              LSBInitExitStatuses
              174  LOAD_ATTR                GENERIC
              176  LOAD_FAST                'self'
              178  LOAD_ATTR                ctl
              180  STORE_ATTR               exitstatus

 L. 596       182  POP_EXCEPT       
              184  LOAD_CONST               None
              186  RETURN_VALUE     
              188  END_FINALLY      
            190_0  COME_FROM           144  '144'

 L. 598       190  LOAD_FAST                'what'
              192  STORE_FAST               'bytes'
              194  JUMP_ABSOLUTE       236  'to 236'
            196_0  COME_FROM            92  '92'

 L. 600       196  LOAD_FAST                'self'
              198  LOAD_ATTR                ctl
              200  LOAD_METHOD              output
              202  LOAD_STR                 'Error: bad argument %s'
              204  LOAD_FAST                'args'
              206  LOAD_CONST               0
              208  BINARY_SUBSCR    
              210  BINARY_MODULO    
              212  CALL_METHOD_1         1  ''
              214  POP_TOP          

 L. 601       216  LOAD_GLOBAL              LSBInitExitStatuses
              218  LOAD_ATTR                GENERIC
              220  LOAD_FAST                'self'
              222  LOAD_ATTR                ctl
              224  STORE_ATTR               exitstatus

 L. 602       226  LOAD_CONST               None
              228  RETURN_VALUE     
              230  JUMP_FORWARD        236  'to 236'
            232_0  COME_FROM            78  '78'

 L. 605       232  LOAD_CONST               1600
              234  STORE_FAST               'bytes'
            236_0  COME_FROM           230  '230'

 L. 607       236  LOAD_FAST                'self'
              238  LOAD_ATTR                ctl
              240  LOAD_METHOD              get_supervisor
              242  CALL_METHOD_0         0  ''
              244  STORE_FAST               'supervisor'

 L. 609       246  SETUP_FINALLY       266  'to 266'

 L. 610       248  LOAD_FAST                'supervisor'
              250  LOAD_METHOD              readLog
              252  LOAD_FAST                'bytes'
              254  UNARY_NEGATIVE   
              256  LOAD_CONST               0
              258  CALL_METHOD_2         2  ''
              260  STORE_FAST               'output'
              262  POP_BLOCK        
              264  JUMP_FORWARD        388  'to 388'
            266_0  COME_FROM_FINALLY   246  '246'

 L. 611       266  DUP_TOP          
              268  LOAD_GLOBAL              xmlrpclib
              270  LOAD_ATTR                Fault
              272  COMPARE_OP               exception-match
          274_276  POP_JUMP_IF_FALSE   386  'to 386'
              278  POP_TOP          
              280  STORE_FAST               'e'
              282  POP_TOP          
              284  SETUP_FINALLY       374  'to 374'

 L. 612       286  LOAD_GLOBAL              LSBInitExitStatuses
              288  LOAD_ATTR                GENERIC
              290  LOAD_FAST                'self'
              292  LOAD_ATTR                ctl
              294  STORE_ATTR               exitstatus

 L. 613       296  LOAD_STR                 '%s: ERROR (%s)'
              298  STORE_FAST               'template'

 L. 614       300  LOAD_FAST                'e'
              302  LOAD_ATTR                faultCode
              304  LOAD_GLOBAL              xmlrpc
              306  LOAD_ATTR                Faults
              308  LOAD_ATTR                NO_FILE
              310  COMPARE_OP               ==
          312_314  POP_JUMP_IF_FALSE   334  'to 334'

 L. 615       316  LOAD_FAST                'self'
              318  LOAD_ATTR                ctl
              320  LOAD_METHOD              output
              322  LOAD_FAST                'template'
              324  LOAD_CONST               ('supervisord', 'no log file')
              326  BINARY_MODULO    
              328  CALL_METHOD_1         1  ''
              330  POP_TOP          
              332  JUMP_FORWARD        370  'to 370'
            334_0  COME_FROM           312  '312'

 L. 616       334  LOAD_FAST                'e'
              336  LOAD_ATTR                faultCode
              338  LOAD_GLOBAL              xmlrpc
              340  LOAD_ATTR                Faults
              342  LOAD_ATTR                FAILED
              344  COMPARE_OP               ==
          346_348  POP_JUMP_IF_FALSE   368  'to 368'

 L. 617       350  LOAD_FAST                'self'
              352  LOAD_ATTR                ctl
              354  LOAD_METHOD              output
              356  LOAD_FAST                'template'
              358  LOAD_CONST               ('supervisord', 'unknown error reading log')
              360  BINARY_MODULO    
              362  CALL_METHOD_1         1  ''
              364  POP_TOP          
              366  JUMP_FORWARD        370  'to 370'
            368_0  COME_FROM           346  '346'

 L. 620       368  RAISE_VARARGS_0       0  'reraise'
            370_0  COME_FROM           366  '366'
            370_1  COME_FROM           332  '332'
              370  POP_BLOCK        
              372  BEGIN_FINALLY    
            374_0  COME_FROM_FINALLY   284  '284'
              374  LOAD_CONST               None
              376  STORE_FAST               'e'
              378  DELETE_FAST              'e'
              380  END_FINALLY      
              382  POP_EXCEPT       
              384  JUMP_FORWARD        400  'to 400'
            386_0  COME_FROM           274  '274'
              386  END_FINALLY      
            388_0  COME_FROM           264  '264'

 L. 622       388  LOAD_FAST                'self'
              390  LOAD_ATTR                ctl
              392  LOAD_METHOD              output
              394  LOAD_FAST                'output'
              396  CALL_METHOD_1         1  ''
              398  POP_TOP          
            400_0  COME_FROM           384  '384'

Parse error at or near `LOAD_CONST' instruction at offset 184

    def help_maintail(self):
        self.ctl.output('maintail -f \tContinuous tail of supervisor main log file (Ctrl-C to exit)\nmaintail -100\tlast 100 *bytes* of supervisord main log file\nmaintail\tlast 1600 *bytes* of supervisor main log file\n')

    def do_quit(self, arg):
        return self.ctl.do_EOF(arg)

    def help_quit(self):
        self.ctl.output('quit\tExit the supervisor shell.')

    do_exit = do_quit

    def help_exit(self):
        self.ctl.output('exit\tExit the supervisor shell.')

    def _show_statuses(self, process_infos):
        namespecs, maxlen = [], 30
        for i, info in enumerate(process_infos):
            namespecs.append(make_namespec(info['group'], info['name']))
            if len(namespecs[i]) > maxlen:
                maxlen = len(namespecs[i])
        else:
            template = '%(namespec)-' + str(maxlen + 3) + 's%(state)-10s%(desc)s'
            for i, info in enumerate(process_infos):
                line = template % {'namespec':namespecs[i],  'state':info['statename'], 
                 'desc':info['description']}
                self.ctl.output(line)

    def do_status(self, arg):
        if not self.ctl.upcheck():
            self.ctl.exitstatus = LSBStatusExitStatuses.UNKNOWN
            return
        supervisor = self.ctl.get_supervisor()
        all_infos = supervisor.getAllProcessInfo()
        names = as_string(arg).split()
        if not names or 'all' in names:
            matching_infos = all_infos
        else:
            matching_infos = []
            for name in names:
                bad_name = True
                group_name, process_name = split_namespec(name)
                for info in all_infos:
                    matched = info['group'] == group_name
                    if process_name is not None:
                        matched = matched and info['name'] == process_name
                    if matched:
                        bad_name = False
                        matching_infos.append(info)

                if bad_name:
                    if process_name is None:
                        msg = '%s: ERROR (no such group)' % group_name
                    else:
                        msg = '%s: ERROR (no such process)' % name
                    self.ctl.output(msg)
                    self.ctl.exitstatus = LSBStatusExitStatuses.UNKNOWN
            else:
                self._show_statuses(matching_infos)
                for info in matching_infos:
                    if info['state'] in states.STOPPED_STATES:
                        self.ctl.exitstatus = LSBStatusExitStatuses.NOT_RUNNING

    def help_status(self):
        self.ctl.output('status <name>\t\tGet status for a single process')
        self.ctl.output('status <gname>:*\tGet status for all processes in a group')
        self.ctl.output('status <name> <name>\tGet status for multiple named processes')
        self.ctl.output('status\t\t\tGet all process status info')

    def do_pid(self, arg):
        supervisor = self.ctl.get_supervisor()
        if not self.ctl.upcheck():
            return
            names = arg.split()
            pid = names or supervisor.getPID()
            self.ctl.output(str(pid))
        else:
            pass
        if 'all' in names:
            for info in supervisor.getAllProcessInfo():
                self.ctl.output(str(info['pid']))

        else:
            for name in names:
                try:
                    info = supervisor.getProcessInfo(name)
                except xmlrpclib.Fault as e:
                    try:
                        self.ctl.exitstatus = LSBInitExitStatuses.GENERIC
                        if e.faultCode == xmlrpc.Faults.BAD_NAME:
                            self.ctl.output('No such process %s' % name)
                        else:
                            raise
                    finally:
                        e = None
                        del e

                else:
                    pid = info['pid']
                    self.ctl.output(str(pid))
                    if pid == 0:
                        self.ctl.exitstatus = LSBInitExitStatuses.NOT_RUNNING

    def help_pid(self):
        self.ctl.output('pid\t\t\tGet the PID of supervisord.')
        self.ctl.output('pid <name>\t\tGet the PID of a single child process by name.')
        self.ctl.output('pid all\t\t\tGet the PID of every child process, one per line.')

    def _startresult(self, result):
        name = make_namespec(result['group'], result['name'])
        code = result['status']
        template = '%s: ERROR (%s)'
        if code == xmlrpc.Faults.BAD_NAME:
            return template % (name, 'no such process')
        if code == xmlrpc.Faults.NO_FILE:
            return template % (name, 'no such file')
        if code == xmlrpc.Faults.NOT_EXECUTABLE:
            return template % (name, 'file is not executable')
        if code == xmlrpc.Faults.ALREADY_STARTED:
            return template % (name, 'already started')
        if code == xmlrpc.Faults.SPAWN_ERROR:
            return template % (name, 'spawn error')
        if code == xmlrpc.Faults.ABNORMAL_TERMINATION:
            return template % (name, 'abnormal termination')
        if code == xmlrpc.Faults.SUCCESS:
            return '%s: started' % name
        raise ValueError('Unknown result code %s for %s' % (code, name))

    def do_start(self, arg):
        if not self.ctl.upcheck():
            return
            names = arg.split()
            supervisor = self.ctl.get_supervisor()
            if not names:
                self.ctl.output('Error: start requires a process name')
                self.ctl.exitstatus = LSBInitExitStatuses.INVALID_ARGS
                self.help_start()
                return None
            if 'all' in names:
                results = supervisor.startAllProcesses()
                for result in results:
                    self.ctl.output(self._startresult(result))
                    self.ctl.set_exitstatus_from_xmlrpc_fault(result['status'], xmlrpc.Faults.ALREADY_STARTED)

        else:
            for name in names:
                group_name, process_name = split_namespec(name)
                if process_name is None:
                    try:
                        results = supervisor.startProcessGroup(group_name)
                        for result in results:
                            self.ctl.output(self._startresult(result))
                            self.ctl.set_exitstatus_from_xmlrpc_fault(result['status'], xmlrpc.Faults.ALREADY_STARTED)

                    except xmlrpclib.Fault as e:
                        try:
                            if e.faultCode == xmlrpc.Faults.BAD_NAME:
                                error = '%s: ERROR (no such group)' % group_name
                                self.ctl.output(error)
                                self.ctl.exitstatus = LSBInitExitStatuses.INVALID_ARGS
                            else:
                                self.ctl.exitstatus = LSBInitExitStatuses.GENERIC
                                raise
                        finally:
                            e = None
                            del e

                else:
                    try:
                        result = supervisor.startProcess(name)
                    except xmlrpclib.Fault as e:
                        try:
                            error = {'status':e.faultCode, 
                             'name':process_name, 
                             'group':group_name, 
                             'description':e.faultString}
                            self.ctl.output(self._startresult(error))
                            self.ctl.set_exitstatus_from_xmlrpc_fault(error['status'], xmlrpc.Faults.ALREADY_STARTED)
                        finally:
                            e = None
                            del e

                    else:
                        name = make_namespec(group_name, process_name)
                        self.ctl.output('%s: started' % name)

    def help_start(self):
        self.ctl.output('start <name>\t\tStart a process')
        self.ctl.output('start <gname>:*\t\tStart all processes in a group')
        self.ctl.output('start <name> <name>\tStart multiple processes or groups')
        self.ctl.output('start all\t\tStart all processes')

    def _signalresult(self, result, success='signalled'):
        name = make_namespec(result['group'], result['name'])
        code = result['status']
        fault_string = result['description']
        template = '%s: ERROR (%s)'
        if code == xmlrpc.Faults.BAD_NAME:
            return template % (name, 'no such process')
        if code == xmlrpc.Faults.BAD_SIGNAL:
            return template % (name, 'bad signal name')
        if code == xmlrpc.Faults.NOT_RUNNING:
            return template % (name, 'not running')
        if code == xmlrpc.Faults.SUCCESS:
            return '%s: %s' % (name, success)
        if code == xmlrpc.Faults.FAILED:
            return fault_string
        raise ValueError('Unknown result code %s for %s' % (code, name))

    def _stopresult(self, result):
        return self._signalresult(result, success='stopped')

    def do_stop(self, arg):
        if not self.ctl.upcheck():
            return
            names = arg.split()
            supervisor = self.ctl.get_supervisor()
            if not names:
                self.ctl.output('Error: stop requires a process name')
                self.ctl.exitstatus = LSBInitExitStatuses.GENERIC
                self.help_stop()
                return None
            if 'all' in names:
                results = supervisor.stopAllProcesses()
                for result in results:
                    self.ctl.output(self._stopresult(result))
                    self.ctl.set_exitstatus_from_xmlrpc_fault(result['status'], xmlrpc.Faults.NOT_RUNNING)

        else:
            for name in names:
                group_name, process_name = split_namespec(name)
                if process_name is None:
                    try:
                        results = supervisor.stopProcessGroup(group_name)
                        for result in results:
                            self.ctl.output(self._stopresult(result))
                            self.ctl.set_exitstatus_from_xmlrpc_fault(result['status'], xmlrpc.Faults.NOT_RUNNING)

                    except xmlrpclib.Fault as e:
                        try:
                            self.ctl.exitstatus = LSBInitExitStatuses.GENERIC
                            if e.faultCode == xmlrpc.Faults.BAD_NAME:
                                error = '%s: ERROR (no such group)' % group_name
                                self.ctl.output(error)
                            else:
                                raise
                        finally:
                            e = None
                            del e

                else:
                    try:
                        supervisor.stopProcess(name)
                    except xmlrpclib.Fault as e:
                        try:
                            error = {'status':e.faultCode, 
                             'name':process_name, 
                             'group':group_name, 
                             'description':e.faultString}
                            self.ctl.output(self._stopresult(error))
                            self.ctl.set_exitstatus_from_xmlrpc_fault(error['status'], xmlrpc.Faults.NOT_RUNNING)
                        finally:
                            e = None
                            del e

                    else:
                        name = make_namespec(group_name, process_name)
                        self.ctl.output('%s: stopped' % name)

    def help_stop(self):
        self.ctl.output('stop <name>\t\tStop a process')
        self.ctl.output('stop <gname>:*\t\tStop all processes in a group')
        self.ctl.output('stop <name> <name>\tStop multiple processes or groups')
        self.ctl.output('stop all\t\tStop all processes')

    def do_signal(self, arg):
        if not self.ctl.upcheck():
            return
            args = arg.split()
            if len(args) < 2:
                self.ctl.output('Error: signal requires a signal name and a process name')
                self.help_signal()
                self.ctl.exitstatus = LSBInitExitStatuses.GENERIC
                return
            sig = args[0]
            names = args[1:]
            supervisor = self.ctl.get_supervisor()
            if 'all' in names:
                results = supervisor.signalAllProcesses(sig)
                for result in results:
                    self.ctl.output(self._signalresult(result))
                    self.ctl.set_exitstatus_from_xmlrpc_fault(result['status'])

        else:
            for name in names:
                group_name, process_name = split_namespec(name)
                if process_name is None:
                    try:
                        results = supervisor.signalProcessGroup(group_name, sig)
                        for result in results:
                            self.ctl.output(self._signalresult(result))
                            self.ctl.set_exitstatus_from_xmlrpc_fault(result['status'])

                    except xmlrpclib.Fault as e:
                        try:
                            if e.faultCode == xmlrpc.Faults.BAD_NAME:
                                error = '%s: ERROR (no such group)' % group_name
                                self.ctl.output(error)
                                self.ctl.exitstatus = LSBInitExitStatuses.GENERIC
                            else:
                                raise
                        finally:
                            e = None
                            del e

                else:
                    try:
                        supervisor.signalProcess(name, sig)
                    except xmlrpclib.Fault as e:
                        try:
                            error = {'status':e.faultCode, 
                             'name':process_name, 
                             'group':group_name, 
                             'description':e.faultString}
                            self.ctl.output(self._signalresult(error))
                            self.ctl.set_exitstatus_from_xmlrpc_fault(error['status'])
                        finally:
                            e = None
                            del e

                    else:
                        name = make_namespec(group_name, process_name)
                        self.ctl.output('%s: signalled' % name)

    def help_signal(self):
        self.ctl.output('signal <signal name> <name>\t\tSignal a process')
        self.ctl.output('signal <signal name> <gname>:*\t\tSignal all processes in a group')
        self.ctl.output('signal <signal name> <name> <name>\tSignal multiple processes or groups')
        self.ctl.output('signal <signal name> all\t\tSignal all processes')

    def do_restart(self, arg):
        if not self.ctl.upcheck():
            return
        else:
            names = arg.split()
            names or self.ctl.output('Error: restart requires a process name')
            self.ctl.exitstatus = LSBInitExitStatuses.GENERIC
            self.help_restart()
            return None
        self.do_stop(arg)
        self.do_start(arg)

    def help_restart(self):
        self.ctl.output('restart <name>\t\tRestart a process')
        self.ctl.output('restart <gname>:*\tRestart all processes in a group')
        self.ctl.output('restart <name> <name>\tRestart multiple processes or groups')
        self.ctl.output('restart all\t\tRestart all processes')
        self.ctl.output('Note: restart does not reread config files. For that, see reread and update.')

    def do_shutdown(self, arg):
        if self.ctl.options.interactive:
            yesno = raw_input('Really shut the remote supervisord process down y/N? ')
            really = yesno.lower().startswith('y')
        else:
            really = 1
        if really:
            supervisor = self.ctl.get_supervisor()
            try:
                supervisor.shutdown()
            except xmlrpclib.Fault as e:
                try:
                    if e.faultCode == xmlrpc.Faults.SHUTDOWN_STATE:
                        self.ctl.output('ERROR: already shutting down')
                    else:
                        self.ctl.exitstatus = LSBInitExitStatuses.GENERIC
                        raise
                finally:
                    e = None
                    del e

            except socket.error as e:
                try:
                    self.ctl.exitstatus = LSBInitExitStatuses.GENERIC
                    if e.args[0] == errno.ECONNREFUSED:
                        msg = 'ERROR: %s refused connection (already shut down?)'
                        self.ctl.output(msg % self.ctl.options.serverurl)
                    else:
                        if e.args[0] == errno.ENOENT:
                            msg = 'ERROR: %s no such file (already shut down?)'
                            self.ctl.output(msg % self.ctl.options.serverurl)
                        else:
                            raise
                finally:
                    e = None
                    del e

            else:
                self.ctl.output('Shut down')

    def help_shutdown(self):
        self.ctl.output('shutdown \tShut the remote supervisord down.')

    def do_reload(self, arg):
        if arg:
            self.ctl.output('Error: reload accepts no arguments')
            self.ctl.exitstatus = LSBInitExitStatuses.GENERIC
            self.help_reload()
            return None
        else:
            if self.ctl.options.interactive:
                yesno = raw_input('Really restart the remote supervisord process y/N? ')
                really = yesno.lower().startswith('y')
            else:
                really = 1
            if really:
                supervisor = self.ctl.get_supervisor()
                try:
                    supervisor.restart()
                except xmlrpclib.Fault as e:
                    try:
                        self.ctl.exitstatus = LSBInitExitStatuses.GENERIC
                        if e.faultCode == xmlrpc.Faults.SHUTDOWN_STATE:
                            self.ctl.output('ERROR: already shutting down')
                        else:
                            raise
                    finally:
                        e = None
                        del e

                else:
                    self.ctl.output('Restarted supervisord')

    def help_reload(self):
        self.ctl.output('reload \t\tRestart the remote supervisord.')

    def _formatChanges(self, added_changed_dropped_tuple):
        added, changed, dropped = added_changed_dropped_tuple
        changedict = {}
        for n, t in ((added, 'available'),
         (
          changed, 'changed'),
         (
          dropped, 'disappeared')):
            changedict.update(dict(zip(n, [t] * len(n))))
        else:
            if changedict:
                names = list(changedict.keys())
                names.sort()
                for name in names:
                    self.ctl.output('%s: %s' % (name, changedict[name]))

            else:
                self.ctl.output('No config updates to processes')

    def _formatConfigInfo(self, configinfo):
        name = make_namespec(configinfo['group'], configinfo['name'])
        formatted = {'name': name}
        if configinfo['inuse']:
            formatted['inuse'] = 'in use'
        else:
            formatted['inuse'] = 'avail'
        if configinfo['autostart']:
            formatted['autostart'] = 'auto'
        else:
            formatted['autostart'] = 'manual'
        formatted['priority'] = '%s:%s' % (configinfo['group_prio'],
         configinfo['process_prio'])
        template = '%(name)-32s %(inuse)-9s %(autostart)-9s %(priority)s'
        return template % formatted

    def do_avail(self, arg):
        if arg:
            self.ctl.output('Error: avail accepts no arguments')
            self.ctl.exitstatus = LSBInitExitStatuses.GENERIC
            self.help_avail()
            return None
        supervisor = self.ctl.get_supervisor()
        try:
            configinfo = supervisor.getAllConfigInfo()
        except xmlrpclib.Fault as e:
            try:
                self.ctl.exitstatus = LSBInitExitStatuses.GENERIC
                if e.faultCode == xmlrpc.Faults.SHUTDOWN_STATE:
                    self.ctl.output('ERROR: supervisor shutting down')
                else:
                    raise
            finally:
                e = None
                del e

        else:
            for pinfo in configinfo:
                self.ctl.output(self._formatConfigInfo(pinfo))

    def help_avail(self):
        self.ctl.output('avail\t\t\tDisplay all configured processes')

    def do_reread(self, arg):
        if arg:
            self.ctl.output('Error: reread accepts no arguments')
            self.ctl.exitstatus = LSBInitExitStatuses.GENERIC
            self.help_reread()
            return None
        supervisor = self.ctl.get_supervisor()
        try:
            result = supervisor.reloadConfig()
        except xmlrpclib.Fault as e:
            try:
                self.ctl.exitstatus = LSBInitExitStatuses.GENERIC
                if e.faultCode == xmlrpc.Faults.SHUTDOWN_STATE:
                    self.ctl.output('ERROR: supervisor shutting down')
                else:
                    if e.faultCode == xmlrpc.Faults.CANT_REREAD:
                        self.ctl.output('ERROR: %s' % e.faultString)
                    else:
                        raise
            finally:
                e = None
                del e

        else:
            self._formatChanges(result[0])

    def help_reread(self):
        self.ctl.output("reread \t\t\tReload the daemon's configuration files without add/remove")

    def do_add(self, arg):
        names = arg.split()
        supervisor = self.ctl.get_supervisor()
        for name in names:
            try:
                supervisor.addProcessGroup(name)
            except xmlrpclib.Fault as e:
                try:
                    if e.faultCode == xmlrpc.Faults.SHUTDOWN_STATE:
                        self.ctl.output('ERROR: shutting down')
                        self.ctl.exitstatus = LSBInitExitStatuses.GENERIC
                    else:
                        if e.faultCode == xmlrpc.Faults.ALREADY_ADDED:
                            self.ctl.output('ERROR: process group already active')
                        else:
                            if e.faultCode == xmlrpc.Faults.BAD_NAME:
                                self.ctl.output('ERROR: no such process/group: %s' % name)
                                self.ctl.exitstatus = LSBInitExitStatuses.GENERIC
                            else:
                                self.ctl.exitstatus = LSBInitExitStatuses.GENERIC
                                raise
                finally:
                    e = None
                    del e

            else:
                self.ctl.output('%s: added process group' % name)

    def help_add(self):
        self.ctl.output('add <name> [...]\tActivates any updates in config for process/group')

    def do_remove(self, arg):
        names = arg.split()
        supervisor = self.ctl.get_supervisor()
        for name in names:
            try:
                supervisor.removeProcessGroup(name)
            except xmlrpclib.Fault as e:
                try:
                    self.ctl.exitstatus = LSBInitExitStatuses.GENERIC
                    if e.faultCode == xmlrpc.Faults.STILL_RUNNING:
                        self.ctl.output('ERROR: process/group still running: %s' % name)
                    else:
                        if e.faultCode == xmlrpc.Faults.BAD_NAME:
                            self.ctl.output('ERROR: no such process/group: %s' % name)
                        else:
                            raise
                finally:
                    e = None
                    del e

            else:
                self.ctl.output('%s: removed process group' % name)

    def help_remove(self):
        self.ctl.output('remove <name> [...]\tRemoves process/group from active config')

    def do_update--- This code section failed: ---

 L.1172         0  LOAD_CLOSURE             'self'
                2  BUILD_TUPLE_1         1 
                4  LOAD_CODE                <code_object log>
                6  LOAD_STR                 'DefaultControllerPlugin.do_update.<locals>.log'
                8  MAKE_FUNCTION_8          'closure'
               10  STORE_FAST               'log'

 L.1175        12  LOAD_DEREF               'self'
               14  LOAD_ATTR                ctl
               16  LOAD_METHOD              get_supervisor
               18  CALL_METHOD_0         0  ''
               20  STORE_FAST               'supervisor'

 L.1176        22  SETUP_FINALLY        36  'to 36'

 L.1177        24  LOAD_FAST                'supervisor'
               26  LOAD_METHOD              reloadConfig
               28  CALL_METHOD_0         0  ''
               30  STORE_FAST               'result'
               32  POP_BLOCK        
               34  JUMP_FORWARD        120  'to 120'
             36_0  COME_FROM_FINALLY    22  '22'

 L.1178        36  DUP_TOP          
               38  LOAD_GLOBAL              xmlrpclib
               40  LOAD_ATTR                Fault
               42  COMPARE_OP               exception-match
               44  POP_JUMP_IF_FALSE   118  'to 118'
               46  POP_TOP          
               48  STORE_FAST               'e'
               50  POP_TOP          
               52  SETUP_FINALLY       106  'to 106'

 L.1179        54  LOAD_GLOBAL              LSBInitExitStatuses
               56  LOAD_ATTR                GENERIC
               58  LOAD_DEREF               'self'
               60  LOAD_ATTR                ctl
               62  STORE_ATTR               exitstatus

 L.1180        64  LOAD_FAST                'e'
               66  LOAD_ATTR                faultCode
               68  LOAD_GLOBAL              xmlrpc
               70  LOAD_ATTR                Faults
               72  LOAD_ATTR                SHUTDOWN_STATE
               74  COMPARE_OP               ==
               76  POP_JUMP_IF_FALSE   100  'to 100'

 L.1181        78  LOAD_DEREF               'self'
               80  LOAD_ATTR                ctl
               82  LOAD_METHOD              output
               84  LOAD_STR                 'ERROR: already shutting down'
               86  CALL_METHOD_1         1  ''
               88  POP_TOP          

 L.1182        90  POP_BLOCK        
               92  POP_EXCEPT       
               94  CALL_FINALLY        106  'to 106'
               96  LOAD_CONST               None
               98  RETURN_VALUE     
            100_0  COME_FROM            76  '76'

 L.1184       100  RAISE_VARARGS_0       0  'reraise'
              102  POP_BLOCK        
              104  BEGIN_FINALLY    
            106_0  COME_FROM            94  '94'
            106_1  COME_FROM_FINALLY    52  '52'
              106  LOAD_CONST               None
              108  STORE_FAST               'e'
              110  DELETE_FAST              'e'
              112  END_FINALLY      
              114  POP_EXCEPT       
              116  JUMP_FORWARD        120  'to 120'
            118_0  COME_FROM            44  '44'
              118  END_FINALLY      
            120_0  COME_FROM           116  '116'
            120_1  COME_FROM            34  '34'

 L.1186       120  LOAD_FAST                'result'
              122  LOAD_CONST               0
              124  BINARY_SUBSCR    
              126  UNPACK_SEQUENCE_3     3 
              128  STORE_FAST               'added'
              130  STORE_FAST               'changed'
              132  STORE_FAST               'removed'

 L.1187       134  LOAD_GLOBAL              set
              136  LOAD_FAST                'arg'
              138  LOAD_METHOD              split
              140  CALL_METHOD_0         0  ''
              142  CALL_FUNCTION_1       1  ''
              144  STORE_FAST               'valid_gnames'

 L.1190       146  LOAD_STR                 'all'
              148  LOAD_FAST                'valid_gnames'
              150  COMPARE_OP               in
              152  POP_JUMP_IF_FALSE   160  'to 160'

 L.1191       154  LOAD_GLOBAL              set
              156  CALL_FUNCTION_0       0  ''
              158  STORE_FAST               'valid_gnames'
            160_0  COME_FROM           152  '152'

 L.1195       160  LOAD_FAST                'valid_gnames'
              162  POP_JUMP_IF_FALSE   252  'to 252'

 L.1196       164  LOAD_GLOBAL              set
              166  CALL_FUNCTION_0       0  ''
              168  STORE_FAST               'groups'

 L.1197       170  LOAD_FAST                'supervisor'
              172  LOAD_METHOD              getAllProcessInfo
              174  CALL_METHOD_0         0  ''
              176  GET_ITER         
              178  FOR_ITER            198  'to 198'
              180  STORE_FAST               'info'

 L.1198       182  LOAD_FAST                'groups'
              184  LOAD_METHOD              add
              186  LOAD_FAST                'info'
              188  LOAD_STR                 'group'
              190  BINARY_SUBSCR    
              192  CALL_METHOD_1         1  ''
              194  POP_TOP          
              196  JUMP_BACK           178  'to 178'

 L.1201       198  LOAD_FAST                'groups'
              200  LOAD_METHOD              update
              202  LOAD_FAST                'added'
              204  CALL_METHOD_1         1  ''
              206  POP_TOP          

 L.1203       208  LOAD_FAST                'valid_gnames'
              210  GET_ITER         
            212_0  COME_FROM           222  '222'
              212  FOR_ITER            252  'to 252'
              214  STORE_FAST               'gname'

 L.1204       216  LOAD_FAST                'gname'
              218  LOAD_FAST                'groups'
              220  COMPARE_OP               not-in
              222  POP_JUMP_IF_FALSE   212  'to 212'

 L.1205       224  LOAD_DEREF               'self'
              226  LOAD_ATTR                ctl
              228  LOAD_METHOD              output
              230  LOAD_STR                 'ERROR: no such group: %s'
              232  LOAD_FAST                'gname'
              234  BINARY_MODULO    
              236  CALL_METHOD_1         1  ''
              238  POP_TOP          

 L.1206       240  LOAD_GLOBAL              LSBInitExitStatuses
              242  LOAD_ATTR                GENERIC
              244  LOAD_DEREF               'self'
              246  LOAD_ATTR                ctl
              248  STORE_ATTR               exitstatus
              250  JUMP_BACK           212  'to 212'
            252_0  COME_FROM           162  '162'

 L.1208       252  LOAD_FAST                'removed'
              254  GET_ITER         
              256  FOR_ITER            378  'to 378'
              258  STORE_FAST               'gname'

 L.1209       260  LOAD_FAST                'valid_gnames'
          262_264  POP_JUMP_IF_FALSE   280  'to 280'
              266  LOAD_FAST                'gname'
              268  LOAD_FAST                'valid_gnames'
              270  COMPARE_OP               not-in
          272_274  POP_JUMP_IF_FALSE   280  'to 280'

 L.1210   276_278  JUMP_BACK           256  'to 256'
            280_0  COME_FROM           272  '272'
            280_1  COME_FROM           262  '262'

 L.1211       280  LOAD_FAST                'supervisor'
              282  LOAD_METHOD              stopProcessGroup
              284  LOAD_FAST                'gname'
              286  CALL_METHOD_1         1  ''
              288  STORE_FAST               'results'

 L.1212       290  LOAD_FAST                'log'
              292  LOAD_FAST                'gname'
              294  LOAD_STR                 'stopped'
              296  CALL_FUNCTION_2       2  ''
              298  POP_TOP          

 L.1214       300  LOAD_LISTCOMP            '<code_object <listcomp>>'
              302  LOAD_STR                 'DefaultControllerPlugin.do_update.<locals>.<listcomp>'
              304  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              306  LOAD_FAST                'results'
              308  GET_ITER         
              310  CALL_FUNCTION_1       1  ''
              312  STORE_FAST               'fails'

 L.1216       314  LOAD_FAST                'fails'
          316_318  POP_JUMP_IF_FALSE   354  'to 354'

 L.1217       320  LOAD_DEREF               'self'
              322  LOAD_ATTR                ctl
              324  LOAD_METHOD              output
              326  LOAD_STR                 '%s: %s'
              328  LOAD_FAST                'gname'
              330  LOAD_STR                 'has problems; not removing'
              332  BUILD_TUPLE_2         2 
              334  BINARY_MODULO    
              336  CALL_METHOD_1         1  ''
              338  POP_TOP          

 L.1218       340  LOAD_GLOBAL              LSBInitExitStatuses
              342  LOAD_ATTR                GENERIC
              344  LOAD_DEREF               'self'
              346  LOAD_ATTR                ctl
              348  STORE_ATTR               exitstatus

 L.1219   350_352  JUMP_BACK           256  'to 256'
            354_0  COME_FROM           316  '316'

 L.1220       354  LOAD_FAST                'supervisor'
              356  LOAD_METHOD              removeProcessGroup
              358  LOAD_FAST                'gname'
              360  CALL_METHOD_1         1  ''
              362  POP_TOP          

 L.1221       364  LOAD_FAST                'log'
              366  LOAD_FAST                'gname'
              368  LOAD_STR                 'removed process group'
              370  CALL_FUNCTION_2       2  ''
              372  POP_TOP          
          374_376  JUMP_BACK           256  'to 256'

 L.1223       378  LOAD_FAST                'changed'
              380  GET_ITER         
              382  FOR_ITER            460  'to 460'
              384  STORE_FAST               'gname'

 L.1224       386  LOAD_FAST                'valid_gnames'
          388_390  POP_JUMP_IF_FALSE   406  'to 406'
              392  LOAD_FAST                'gname'
              394  LOAD_FAST                'valid_gnames'
              396  COMPARE_OP               not-in
          398_400  POP_JUMP_IF_FALSE   406  'to 406'

 L.1225   402_404  JUMP_BACK           382  'to 382'
            406_0  COME_FROM           398  '398'
            406_1  COME_FROM           388  '388'

 L.1226       406  LOAD_FAST                'supervisor'
              408  LOAD_METHOD              stopProcessGroup
              410  LOAD_FAST                'gname'
              412  CALL_METHOD_1         1  ''
              414  POP_TOP          

 L.1227       416  LOAD_FAST                'log'
              418  LOAD_FAST                'gname'
              420  LOAD_STR                 'stopped'
              422  CALL_FUNCTION_2       2  ''
              424  POP_TOP          

 L.1229       426  LOAD_FAST                'supervisor'
              428  LOAD_METHOD              removeProcessGroup
              430  LOAD_FAST                'gname'
              432  CALL_METHOD_1         1  ''
              434  POP_TOP          

 L.1230       436  LOAD_FAST                'supervisor'
              438  LOAD_METHOD              addProcessGroup
              440  LOAD_FAST                'gname'
              442  CALL_METHOD_1         1  ''
              444  POP_TOP          

 L.1231       446  LOAD_FAST                'log'
              448  LOAD_FAST                'gname'
              450  LOAD_STR                 'updated process group'
              452  CALL_FUNCTION_2       2  ''
              454  POP_TOP          
          456_458  JUMP_BACK           382  'to 382'

 L.1233       460  LOAD_FAST                'added'
              462  GET_ITER         
              464  FOR_ITER            512  'to 512'
              466  STORE_FAST               'gname'

 L.1234       468  LOAD_FAST                'valid_gnames'
          470_472  POP_JUMP_IF_FALSE   488  'to 488'
              474  LOAD_FAST                'gname'
              476  LOAD_FAST                'valid_gnames'
              478  COMPARE_OP               not-in
          480_482  POP_JUMP_IF_FALSE   488  'to 488'

 L.1235   484_486  JUMP_BACK           464  'to 464'
            488_0  COME_FROM           480  '480'
            488_1  COME_FROM           470  '470'

 L.1236       488  LOAD_FAST                'supervisor'
              490  LOAD_METHOD              addProcessGroup
              492  LOAD_FAST                'gname'
              494  CALL_METHOD_1         1  ''
              496  POP_TOP          

 L.1237       498  LOAD_FAST                'log'
              500  LOAD_FAST                'gname'
              502  LOAD_STR                 'added process group'
              504  CALL_FUNCTION_2       2  ''
              506  POP_TOP          
          508_510  JUMP_BACK           464  'to 464'

Parse error at or near `POP_EXCEPT' instruction at offset 92

    def help_update(self):
        self.ctl.output('update\t\t\tReload config and add/remove as necessary, and will restart affected programs')
        self.ctl.output('update all\t\tReload config and add/remove as necessary, and will restart affected programs')
        self.ctl.output('update <gname> [...]\tUpdate specific groups')

    def _clearresult(self, result):
        name = make_namespec(result['group'], result['name'])
        code = result['status']
        template = '%s: ERROR (%s)'
        if code == xmlrpc.Faults.BAD_NAME:
            return template % (name, 'no such process')
        if code == xmlrpc.Faults.FAILED:
            return template % (name, 'failed')
        if code == xmlrpc.Faults.SUCCESS:
            return '%s: cleared' % name
        raise ValueError('Unknown result code %s for %s' % (code, name))

    def do_clear(self, arg):
        if not self.ctl.upcheck():
            return
            names = arg.split()
            if not names:
                self.ctl.output('Error: clear requires a process name')
                self.ctl.exitstatus = LSBInitExitStatuses.GENERIC
                self.help_clear()
                return None
            supervisor = self.ctl.get_supervisor()
            if 'all' in names:
                results = supervisor.clearAllProcessLogs()
                for result in results:
                    self.ctl.output(self._clearresult(result))
                    self.ctl.set_exitstatus_from_xmlrpc_fault(result['status'])

        else:
            for name in names:
                group_name, process_name = split_namespec(name)
                try:
                    supervisor.clearProcessLogs(name)
                except xmlrpclib.Fault as e:
                    try:
                        error = {'status':e.faultCode, 
                         'name':process_name, 
                         'group':group_name, 
                         'description':e.faultString}
                        self.ctl.output(self._clearresult(error))
                        self.ctl.set_exitstatus_from_xmlrpc_fault(error['status'])
                    finally:
                        e = None
                        del e

                else:
                    name = make_namespec(group_name, process_name)
                    self.ctl.output('%s: cleared' % name)

    def help_clear(self):
        self.ctl.output("clear <name>\t\tClear a process' log files.")
        self.ctl.output("clear <name> <name>\tClear multiple process' log files")
        self.ctl.output("clear all\t\tClear all process' log files")

    def do_open(self, arg):
        url = arg.strip()
        parts = urlparse.urlparse(url)
        if parts[0] not in ('unix', 'http'):
            self.ctl.output('ERROR: url must be http:// or unix://')
            self.ctl.exitstatus = LSBInitExitStatuses.GENERIC
            return
        self.ctl.options.serverurl = url
        old_exitstatus = self.ctl.exitstatus
        self.do_status('')
        self.ctl.exitstatus = old_exitstatus

    def help_open(self):
        self.ctl.output('open <url>\tConnect to a remote supervisord process.')
        self.ctl.output('\t\t(for UNIX domain socket, use unix:///socket/path)')

    def do_version(self, arg):
        if arg:
            self.ctl.output('Error: version accepts no arguments')
            self.ctl.exitstatus = LSBInitExitStatuses.GENERIC
            self.help_version()
            return None
        else:
            return self.ctl.upcheck() or None
        supervisor = self.ctl.get_supervisor()
        self.ctl.output(supervisor.getSupervisorVersion())

    def help_version(self):
        self.ctl.output('version\t\t\tShow the version of the remote supervisord process')

    def do_fg--- This code section failed: ---

 L.1332         0  LOAD_FAST                'self'
                2  LOAD_ATTR                ctl
                4  LOAD_METHOD              upcheck
                6  CALL_METHOD_0         0  ''
                8  POP_JUMP_IF_TRUE     14  'to 14'

 L.1333        10  LOAD_CONST               None
               12  RETURN_VALUE     
             14_0  COME_FROM             8  '8'

 L.1335        14  LOAD_FAST                'arg'
               16  LOAD_METHOD              split
               18  CALL_METHOD_0         0  ''
               20  STORE_FAST               'names'

 L.1336        22  LOAD_FAST                'names'
               24  POP_JUMP_IF_TRUE     60  'to 60'

 L.1337        26  LOAD_FAST                'self'
               28  LOAD_ATTR                ctl
               30  LOAD_METHOD              output
               32  LOAD_STR                 'ERROR: no process name supplied'
               34  CALL_METHOD_1         1  ''
               36  POP_TOP          

 L.1338        38  LOAD_GLOBAL              LSBInitExitStatuses
               40  LOAD_ATTR                GENERIC
               42  LOAD_FAST                'self'
               44  LOAD_ATTR                ctl
               46  STORE_ATTR               exitstatus

 L.1339        48  LOAD_FAST                'self'
               50  LOAD_METHOD              help_fg
               52  CALL_METHOD_0         0  ''
               54  POP_TOP          

 L.1340        56  LOAD_CONST               None
               58  RETURN_VALUE     
             60_0  COME_FROM            24  '24'

 L.1341        60  LOAD_GLOBAL              len
               62  LOAD_FAST                'names'
               64  CALL_FUNCTION_1       1  ''
               66  LOAD_CONST               1
               68  COMPARE_OP               >
               70  POP_JUMP_IF_FALSE    98  'to 98'

 L.1342        72  LOAD_FAST                'self'
               74  LOAD_ATTR                ctl
               76  LOAD_METHOD              output
               78  LOAD_STR                 'ERROR: too many process names supplied'
               80  CALL_METHOD_1         1  ''
               82  POP_TOP          

 L.1343        84  LOAD_GLOBAL              LSBInitExitStatuses
               86  LOAD_ATTR                GENERIC
               88  LOAD_FAST                'self'
               90  LOAD_ATTR                ctl
               92  STORE_ATTR               exitstatus

 L.1344        94  LOAD_CONST               None
               96  RETURN_VALUE     
             98_0  COME_FROM            70  '70'

 L.1346        98  LOAD_FAST                'names'
              100  LOAD_CONST               0
              102  BINARY_SUBSCR    
              104  STORE_FAST               'name'

 L.1347       106  LOAD_FAST                'self'
              108  LOAD_ATTR                ctl
              110  LOAD_METHOD              get_supervisor
              112  CALL_METHOD_0         0  ''
              114  STORE_FAST               'supervisor'

 L.1349       116  SETUP_FINALLY       132  'to 132'

 L.1350       118  LOAD_FAST                'supervisor'
              120  LOAD_METHOD              getProcessInfo
              122  LOAD_FAST                'name'
              124  CALL_METHOD_1         1  ''
              126  STORE_FAST               'info'
              128  POP_BLOCK        
              130  JUMP_FORWARD        232  'to 232'
            132_0  COME_FROM_FINALLY   116  '116'

 L.1351       132  DUP_TOP          
              134  LOAD_GLOBAL              xmlrpclib
              136  LOAD_ATTR                Fault
              138  COMPARE_OP               exception-match
              140  POP_JUMP_IF_FALSE   230  'to 230'
              142  POP_TOP          
              144  STORE_FAST               'e'
              146  POP_TOP          
              148  SETUP_FINALLY       218  'to 218'

 L.1352       150  LOAD_FAST                'e'
              152  LOAD_ATTR                faultCode
              154  LOAD_GLOBAL              xmlrpc
              156  LOAD_ATTR                Faults
              158  LOAD_ATTR                BAD_NAME
              160  COMPARE_OP               ==
              162  POP_JUMP_IF_FALSE   188  'to 188'

 L.1353       164  LOAD_FAST                'self'
              166  LOAD_ATTR                ctl
              168  LOAD_METHOD              output
              170  LOAD_STR                 'ERROR: bad process name supplied'
              172  CALL_METHOD_1         1  ''
              174  POP_TOP          

 L.1354       176  LOAD_GLOBAL              LSBInitExitStatuses
              178  LOAD_ATTR                GENERIC
              180  LOAD_FAST                'self'
              182  LOAD_ATTR                ctl
              184  STORE_ATTR               exitstatus
              186  JUMP_FORWARD        208  'to 208'
            188_0  COME_FROM           162  '162'

 L.1356       188  LOAD_FAST                'self'
              190  LOAD_ATTR                ctl
              192  LOAD_METHOD              output
              194  LOAD_STR                 'ERROR: '
              196  LOAD_GLOBAL              str
              198  LOAD_FAST                'e'
              200  CALL_FUNCTION_1       1  ''
              202  BINARY_ADD       
              204  CALL_METHOD_1         1  ''
              206  POP_TOP          
            208_0  COME_FROM           186  '186'

 L.1357       208  POP_BLOCK        
              210  POP_EXCEPT       
              212  CALL_FINALLY        218  'to 218'
              214  LOAD_CONST               None
              216  RETURN_VALUE     
            218_0  COME_FROM           212  '212'
            218_1  COME_FROM_FINALLY   148  '148'
              218  LOAD_CONST               None
              220  STORE_FAST               'e'
              222  DELETE_FAST              'e'
              224  END_FINALLY      
              226  POP_EXCEPT       
              228  JUMP_FORWARD        232  'to 232'
            230_0  COME_FROM           140  '140'
              230  END_FINALLY      
            232_0  COME_FROM           228  '228'
            232_1  COME_FROM           130  '130'

 L.1359       232  LOAD_FAST                'info'
              234  LOAD_STR                 'state'
              236  BINARY_SUBSCR    
              238  LOAD_GLOBAL              states
              240  LOAD_ATTR                ProcessStates
              242  LOAD_ATTR                RUNNING
              244  COMPARE_OP               !=
          246_248  POP_JUMP_IF_FALSE   276  'to 276'

 L.1360       250  LOAD_FAST                'self'
              252  LOAD_ATTR                ctl
              254  LOAD_METHOD              output
              256  LOAD_STR                 'ERROR: process not running'
              258  CALL_METHOD_1         1  ''
              260  POP_TOP          

 L.1361       262  LOAD_GLOBAL              LSBInitExitStatuses
              264  LOAD_ATTR                GENERIC
              266  LOAD_FAST                'self'
              268  LOAD_ATTR                ctl
              270  STORE_ATTR               exitstatus

 L.1362       272  LOAD_CONST               None
              274  RETURN_VALUE     
            276_0  COME_FROM           246  '246'

 L.1364       276  LOAD_FAST                'self'
              278  LOAD_ATTR                ctl
              280  LOAD_METHOD              output
              282  LOAD_STR                 '==> Press Ctrl-C to exit <=='
              284  CALL_METHOD_1         1  ''
              286  POP_TOP          

 L.1366       288  LOAD_CONST               None
              290  STORE_FAST               'a'

 L.1367       292  SETUP_FINALLY       532  'to 532'

 L.1369       294  LOAD_GLOBAL              fgthread
              296  LOAD_FAST                'name'
              298  LOAD_FAST                'self'
              300  LOAD_ATTR                ctl
              302  CALL_FUNCTION_2       2  ''
              304  STORE_FAST               'a'

 L.1370       306  LOAD_FAST                'a'
              308  LOAD_METHOD              start
              310  CALL_METHOD_0         0  ''
              312  POP_TOP          
            314_0  COME_FROM           482  '482'

 L.1374       314  LOAD_GLOBAL              raw_input
              316  CALL_FUNCTION_0       0  ''
              318  LOAD_STR                 '\n'
              320  BINARY_ADD       
              322  STORE_FAST               'inp'

 L.1375       324  SETUP_FINALLY       342  'to 342'

 L.1376       326  LOAD_FAST                'supervisor'
              328  LOAD_METHOD              sendProcessStdin
              330  LOAD_FAST                'name'
              332  LOAD_FAST                'inp'
              334  CALL_METHOD_2         2  ''
              336  POP_TOP          
              338  POP_BLOCK        
              340  JUMP_FORWARD        458  'to 458'
            342_0  COME_FROM_FINALLY   324  '324'

 L.1377       342  DUP_TOP          
              344  LOAD_GLOBAL              xmlrpclib
              346  LOAD_ATTR                Fault
              348  COMPARE_OP               exception-match
          350_352  POP_JUMP_IF_FALSE   456  'to 456'
              354  POP_TOP          
              356  STORE_FAST               'e'
              358  POP_TOP          
              360  SETUP_FINALLY       444  'to 444'

 L.1378       362  LOAD_FAST                'e'
              364  LOAD_ATTR                faultCode
              366  LOAD_GLOBAL              xmlrpc
              368  LOAD_ATTR                Faults
              370  LOAD_ATTR                NOT_RUNNING
              372  COMPARE_OP               ==
          374_376  POP_JUMP_IF_FALSE   392  'to 392'

 L.1379       378  LOAD_FAST                'self'
              380  LOAD_ATTR                ctl
              382  LOAD_METHOD              output
              384  LOAD_STR                 'Process got killed'
              386  CALL_METHOD_1         1  ''
              388  POP_TOP          
              390  JUMP_FORWARD        412  'to 412'
            392_0  COME_FROM           374  '374'

 L.1381       392  LOAD_FAST                'self'
              394  LOAD_ATTR                ctl
              396  LOAD_METHOD              output
              398  LOAD_STR                 'ERROR: '
              400  LOAD_GLOBAL              str
              402  LOAD_FAST                'e'
              404  CALL_FUNCTION_1       1  ''
              406  BINARY_ADD       
              408  CALL_METHOD_1         1  ''
              410  POP_TOP          
            412_0  COME_FROM           390  '390'

 L.1382       412  LOAD_FAST                'self'
              414  LOAD_ATTR                ctl
              416  LOAD_METHOD              output
              418  LOAD_STR                 'Exiting foreground'
              420  CALL_METHOD_1         1  ''
              422  POP_TOP          

 L.1383       424  LOAD_FAST                'a'
              426  LOAD_METHOD              kill
              428  CALL_METHOD_0         0  ''
              430  POP_TOP          

 L.1384       432  POP_BLOCK        
              434  POP_EXCEPT       
              436  CALL_FINALLY        444  'to 444'
              438  POP_BLOCK        
              440  LOAD_CONST               None
              442  RETURN_VALUE     
            444_0  COME_FROM           436  '436'
            444_1  COME_FROM_FINALLY   360  '360'
              444  LOAD_CONST               None
              446  STORE_FAST               'e'
              448  DELETE_FAST              'e'
              450  END_FINALLY      
              452  POP_EXCEPT       
              454  JUMP_FORWARD        458  'to 458'
            456_0  COME_FROM           350  '350'
              456  END_FINALLY      
            458_0  COME_FROM           454  '454'
            458_1  COME_FROM           340  '340'

 L.1386       458  LOAD_FAST                'supervisor'
              460  LOAD_METHOD              getProcessInfo
              462  LOAD_FAST                'name'
              464  CALL_METHOD_1         1  ''
              466  STORE_FAST               'info'

 L.1387       468  LOAD_FAST                'info'
              470  LOAD_STR                 'state'
              472  BINARY_SUBSCR    
              474  LOAD_GLOBAL              states
              476  LOAD_ATTR                ProcessStates
              478  LOAD_ATTR                RUNNING
              480  COMPARE_OP               !=
          482_484  POP_JUMP_IF_FALSE   314  'to 314'

 L.1388       486  LOAD_FAST                'self'
              488  LOAD_ATTR                ctl
              490  LOAD_METHOD              output
              492  LOAD_STR                 'Process got killed'
              494  CALL_METHOD_1         1  ''
              496  POP_TOP          

 L.1389       498  LOAD_FAST                'self'
              500  LOAD_ATTR                ctl
              502  LOAD_METHOD              output
              504  LOAD_STR                 'Exiting foreground'
              506  CALL_METHOD_1         1  ''
              508  POP_TOP          

 L.1390       510  LOAD_FAST                'a'
              512  LOAD_METHOD              kill
              514  CALL_METHOD_0         0  ''
              516  POP_TOP          

 L.1391       518  POP_BLOCK        
              520  LOAD_CONST               None
              522  RETURN_VALUE     
          524_526  JUMP_BACK           314  'to 314'
              528  POP_BLOCK        
              530  JUMP_FORWARD        584  'to 584'
            532_0  COME_FROM_FINALLY   292  '292'

 L.1392       532  DUP_TOP          
              534  LOAD_GLOBAL              KeyboardInterrupt
              536  LOAD_GLOBAL              EOFError
              538  BUILD_TUPLE_2         2 
              540  COMPARE_OP               exception-match
          542_544  POP_JUMP_IF_FALSE   582  'to 582'
              546  POP_TOP          
              548  POP_TOP          
              550  POP_TOP          

 L.1393       552  LOAD_FAST                'self'
              554  LOAD_ATTR                ctl
              556  LOAD_METHOD              output
              558  LOAD_STR                 'Exiting foreground'
              560  CALL_METHOD_1         1  ''
              562  POP_TOP          

 L.1394       564  LOAD_FAST                'a'
          566_568  POP_JUMP_IF_FALSE   578  'to 578'

 L.1395       570  LOAD_FAST                'a'
              572  LOAD_METHOD              kill
              574  CALL_METHOD_0         0  ''
              576  POP_TOP          
            578_0  COME_FROM           566  '566'
              578  POP_EXCEPT       
              580  JUMP_FORWARD        584  'to 584'
            582_0  COME_FROM           542  '542'
              582  END_FINALLY      
            584_0  COME_FROM           580  '580'
            584_1  COME_FROM           530  '530'

Parse error at or near `CALL_FINALLY' instruction at offset 212

    def help_fg(self, args=None):
        self.ctl.output('fg <process>\tConnect to a process in foreground mode')
        self.ctl.output('\t\tCtrl-C to exit')


def main(args=None, options=None):
    if options is None:
        options = ClientOptions()
    options.realize(args, doc=__doc__)
    c = Controller(options)
    if options.args:
        c.onecmd(' '.join(options.args))
        sys.exit(c.exitstatus)
    if options.interactive:
        c.exec_cmdloop(args, options)
        sys.exit(0)


if __name__ == '__main__':
    main()