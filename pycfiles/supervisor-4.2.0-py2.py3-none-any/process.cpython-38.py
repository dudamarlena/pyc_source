# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./build/lib/supervisor/process.py
# Compiled at: 2019-04-05 17:57:05
# Size of source mod 2**32: 38097 bytes
import os, time, errno, shlex, traceback, signal
from functools import total_ordering
from supervisor.compat import maxint
from supervisor.compat import as_bytes
from supervisor.compat import as_string
from supervisor.compat import PY2
import supervisor.medusa as asyncore
from supervisor.states import ProcessStates
from supervisor.states import SupervisorStates
from supervisor.states import getProcessStateDescription
from supervisor.states import STOPPED_STATES
from supervisor.options import decode_wait_status
from supervisor.options import signame
from supervisor.options import ProcessException, BadCommand
from supervisor.dispatchers import EventListenerStates
from supervisor import events
from supervisor.datatypes import RestartUnconditionally
from supervisor.socket_manager import SocketManager

@total_ordering
class Subprocess(object):
    __doc__ = 'A class to manage a subprocess.'
    pid = 0
    config = None
    state = None
    listener_state = None
    event = None
    laststart = 0
    laststop = 0
    laststopreport = 0
    delay = 0
    administrative_stop = False
    system_stop = False
    killing = False
    backoff = 0
    dispatchers = None
    pipes = None
    exitstatus = None
    spawnerr = None
    group = None

    def __init__(self, config):
        """Constructor.

        Argument is a ProcessConfig instance.
        """
        self.config = config
        self.dispatchers = {}
        self.pipes = {}
        self.state = ProcessStates.STOPPED

    def removelogs(self):
        for dispatcher in self.dispatchers.values():
            if hasattr(dispatcher, 'removelogs'):
                dispatcher.removelogs()

    def reopenlogs(self):
        for dispatcher in self.dispatchers.values():
            if hasattr(dispatcher, 'reopenlogs'):
                dispatcher.reopenlogs()

    def drain(self):
        for dispatcher in self.dispatchers.values():
            if dispatcher.readable():
                dispatcher.handle_read_event()
            if dispatcher.writable():
                dispatcher.handle_write_event()

    def write(self, chars):
        if not self.pid or self.killing:
            raise OSError(errno.EPIPE, 'Process already closed')
        stdin_fd = self.pipes['stdin']
        if stdin_fd is None:
            raise OSError(errno.EPIPE, 'Process has no stdin channel')
        dispatcher = self.dispatchers[stdin_fd]
        if dispatcher.closed:
            raise OSError(errno.EPIPE, "Process' stdin channel is closed")
        dispatcher.input_buffer += chars
        dispatcher.flush()

    def get_execv_args(self):
        """Internal: turn a program name into a file name, using $PATH,
        make sure it exists / is executable, raising a ProcessException
        if not """
        try:
            commandargs = shlex.split(self.config.command)
        except ValueError as e:
            try:
                raise BadCommand("can't parse command %r: %s" % (
                 self.config.command, str(e)))
            finally:
                e = None
                del e

        else:
            if commandargs:
                program = commandargs[0]
            else:
                raise BadCommand('command is empty')
            if '/' in program:
                filename = program
                try:
                    st = self.config.options.stat(filename)
                except OSError:
                    st = None

            else:
                path = self.config.get_path()
                found = None
                st = None
                for dir in path:
                    found = os.path.join(dir, program)
                    try:
                        st = self.config.options.stat(found)
                    except OSError:
                        pass
                    else:
                        break
                else:
                    if st is None:
                        filename = program
                    else:
                        filename = found

            self.config.options.check_execv_args(filename, commandargs, st)
            return (
             filename, commandargs)

    event_map = {ProcessStates.BACKOFF: events.ProcessStateBackoffEvent, 
     ProcessStates.FATAL: events.ProcessStateFatalEvent, 
     ProcessStates.UNKNOWN: events.ProcessStateUnknownEvent, 
     ProcessStates.STOPPED: events.ProcessStateStoppedEvent, 
     ProcessStates.EXITED: events.ProcessStateExitedEvent, 
     ProcessStates.RUNNING: events.ProcessStateRunningEvent, 
     ProcessStates.STARTING: events.ProcessStateStartingEvent, 
     ProcessStates.STOPPING: events.ProcessStateStoppingEvent}

    def change_state(self, new_state, expected=True):
        old_state = self.state
        if new_state is old_state:
            return False
        event_class = self.event_map.get(new_state)
        if event_class is not None:
            event = event_class(self, old_state, expected)
            events.notify(event)
        if new_state == ProcessStates.BACKOFF:
            now = time.time()
            self.backoff += 1
            self.delay = now + self.backoff
        self.state = new_state

    def _assertInState(self, *states):
        if self.state not in states:
            current_state = getProcessStateDescription(self.state)
            allowable_states = ' '.join(map(getProcessStateDescription, states))
            processname = as_string(self.config.name)
            raise AssertionError('Assertion failed for %s: %s not in %s' % (
             processname, current_state, allowable_states))

    def record_spawnerr(self, msg):
        self.spawnerr = msg
        self.config.options.logger.info('spawnerr: %s' % msg)

    def spawn--- This code section failed: ---

 L. 197         0  LOAD_FAST                'self'
                2  LOAD_ATTR                config
                4  LOAD_ATTR                options
                6  STORE_FAST               'options'

 L. 198         8  LOAD_GLOBAL              as_string
               10  LOAD_FAST                'self'
               12  LOAD_ATTR                config
               14  LOAD_ATTR                name
               16  CALL_FUNCTION_1       1  ''
               18  STORE_FAST               'processname'

 L. 200        20  LOAD_FAST                'self'
               22  LOAD_ATTR                pid
               24  POP_JUMP_IF_FALSE    50  'to 50'

 L. 201        26  LOAD_STR                 "process '%s' already running"
               28  LOAD_FAST                'processname'
               30  BINARY_MODULO    
               32  STORE_FAST               'msg'

 L. 202        34  LOAD_FAST                'options'
               36  LOAD_ATTR                logger
               38  LOAD_METHOD              warn
               40  LOAD_FAST                'msg'
               42  CALL_METHOD_1         1  ''
               44  POP_TOP          

 L. 203        46  LOAD_CONST               None
               48  RETURN_VALUE     
             50_0  COME_FROM            24  '24'

 L. 205        50  LOAD_CONST               False
               52  LOAD_FAST                'self'
               54  STORE_ATTR               killing

 L. 206        56  LOAD_CONST               None
               58  LOAD_FAST                'self'
               60  STORE_ATTR               spawnerr

 L. 207        62  LOAD_CONST               None
               64  LOAD_FAST                'self'
               66  STORE_ATTR               exitstatus

 L. 208        68  LOAD_CONST               False
               70  LOAD_FAST                'self'
               72  STORE_ATTR               system_stop

 L. 209        74  LOAD_CONST               False
               76  LOAD_FAST                'self'
               78  STORE_ATTR               administrative_stop

 L. 211        80  LOAD_GLOBAL              time
               82  LOAD_METHOD              time
               84  CALL_METHOD_0         0  ''
               86  LOAD_FAST                'self'
               88  STORE_ATTR               laststart

 L. 213        90  LOAD_FAST                'self'
               92  LOAD_METHOD              _assertInState
               94  LOAD_GLOBAL              ProcessStates
               96  LOAD_ATTR                EXITED
               98  LOAD_GLOBAL              ProcessStates
              100  LOAD_ATTR                FATAL

 L. 214       102  LOAD_GLOBAL              ProcessStates
              104  LOAD_ATTR                BACKOFF

 L. 214       106  LOAD_GLOBAL              ProcessStates
              108  LOAD_ATTR                STOPPED

 L. 213       110  CALL_METHOD_4         4  ''
              112  POP_TOP          

 L. 216       114  LOAD_FAST                'self'
              116  LOAD_METHOD              change_state
              118  LOAD_GLOBAL              ProcessStates
              120  LOAD_ATTR                STARTING
              122  CALL_METHOD_1         1  ''
              124  POP_TOP          

 L. 218       126  SETUP_FINALLY       144  'to 144'

 L. 219       128  LOAD_FAST                'self'
              130  LOAD_METHOD              get_execv_args
              132  CALL_METHOD_0         0  ''
              134  UNPACK_SEQUENCE_2     2 
              136  STORE_FAST               'filename'
              138  STORE_FAST               'argv'
              140  POP_BLOCK        
              142  JUMP_FORWARD        224  'to 224'
            144_0  COME_FROM_FINALLY   126  '126'

 L. 220       144  DUP_TOP          
              146  LOAD_GLOBAL              ProcessException
              148  COMPARE_OP               exception-match
              150  POP_JUMP_IF_FALSE   222  'to 222'
              152  POP_TOP          
              154  STORE_FAST               'what'
              156  POP_TOP          
              158  SETUP_FINALLY       210  'to 210'

 L. 221       160  LOAD_FAST                'self'
              162  LOAD_METHOD              record_spawnerr
              164  LOAD_FAST                'what'
              166  LOAD_ATTR                args
              168  LOAD_CONST               0
              170  BINARY_SUBSCR    
              172  CALL_METHOD_1         1  ''
              174  POP_TOP          

 L. 222       176  LOAD_FAST                'self'
              178  LOAD_METHOD              _assertInState
              180  LOAD_GLOBAL              ProcessStates
              182  LOAD_ATTR                STARTING
              184  CALL_METHOD_1         1  ''
              186  POP_TOP          

 L. 223       188  LOAD_FAST                'self'
              190  LOAD_METHOD              change_state
              192  LOAD_GLOBAL              ProcessStates
              194  LOAD_ATTR                BACKOFF
              196  CALL_METHOD_1         1  ''
              198  POP_TOP          

 L. 224       200  POP_BLOCK        
              202  POP_EXCEPT       
              204  CALL_FINALLY        210  'to 210'
              206  LOAD_CONST               None
              208  RETURN_VALUE     
            210_0  COME_FROM           204  '204'
            210_1  COME_FROM_FINALLY   158  '158'
              210  LOAD_CONST               None
              212  STORE_FAST               'what'
              214  DELETE_FAST              'what'
              216  END_FINALLY      
              218  POP_EXCEPT       
              220  JUMP_FORWARD        224  'to 224'
            222_0  COME_FROM           150  '150'
              222  END_FINALLY      
            224_0  COME_FROM           220  '220'
            224_1  COME_FROM           142  '142'

 L. 226       224  SETUP_FINALLY       250  'to 250'

 L. 227       226  LOAD_FAST                'self'
              228  LOAD_ATTR                config
              230  LOAD_METHOD              make_dispatchers
              232  LOAD_FAST                'self'
              234  CALL_METHOD_1         1  ''
              236  UNPACK_SEQUENCE_2     2 
              238  LOAD_FAST                'self'
              240  STORE_ATTR               dispatchers
              242  LOAD_FAST                'self'
              244  STORE_ATTR               pipes
              246  POP_BLOCK        
              248  JUMP_FORWARD        384  'to 384'
            250_0  COME_FROM_FINALLY   224  '224'

 L. 228       250  DUP_TOP          
              252  LOAD_GLOBAL              OSError
              254  LOAD_GLOBAL              IOError
              256  BUILD_TUPLE_2         2 
              258  COMPARE_OP               exception-match
          260_262  POP_JUMP_IF_FALSE   382  'to 382'
              264  POP_TOP          
              266  STORE_FAST               'why'
              268  POP_TOP          
              270  SETUP_FINALLY       370  'to 370'

 L. 229       272  LOAD_FAST                'why'
              274  LOAD_ATTR                args
              276  LOAD_CONST               0
              278  BINARY_SUBSCR    
              280  STORE_FAST               'code'

 L. 230       282  LOAD_FAST                'code'
              284  LOAD_GLOBAL              errno
              286  LOAD_ATTR                EMFILE
              288  COMPARE_OP               ==
          290_292  POP_JUMP_IF_FALSE   304  'to 304'

 L. 232       294  LOAD_STR                 "too many open files to spawn '%s'"
              296  LOAD_FAST                'processname'
              298  BINARY_MODULO    
              300  STORE_FAST               'msg'
              302  JUMP_FORWARD        326  'to 326'
            304_0  COME_FROM           290  '290'

 L. 234       304  LOAD_STR                 "unknown error making dispatchers for '%s': %s"

 L. 235       306  LOAD_FAST                'processname'

 L. 235       308  LOAD_GLOBAL              errno
              310  LOAD_ATTR                errorcode
              312  LOAD_METHOD              get
              314  LOAD_FAST                'code'
              316  LOAD_FAST                'code'
              318  CALL_METHOD_2         2  ''

 L. 234       320  BUILD_TUPLE_2         2 
              322  BINARY_MODULO    
              324  STORE_FAST               'msg'
            326_0  COME_FROM           302  '302'

 L. 236       326  LOAD_FAST                'self'
              328  LOAD_METHOD              record_spawnerr
              330  LOAD_FAST                'msg'
              332  CALL_METHOD_1         1  ''
              334  POP_TOP          

 L. 237       336  LOAD_FAST                'self'
              338  LOAD_METHOD              _assertInState
              340  LOAD_GLOBAL              ProcessStates
              342  LOAD_ATTR                STARTING
              344  CALL_METHOD_1         1  ''
              346  POP_TOP          

 L. 238       348  LOAD_FAST                'self'
              350  LOAD_METHOD              change_state
              352  LOAD_GLOBAL              ProcessStates
              354  LOAD_ATTR                BACKOFF
              356  CALL_METHOD_1         1  ''
              358  POP_TOP          

 L. 239       360  POP_BLOCK        
              362  POP_EXCEPT       
              364  CALL_FINALLY        370  'to 370'
              366  LOAD_CONST               None
              368  RETURN_VALUE     
            370_0  COME_FROM           364  '364'
            370_1  COME_FROM_FINALLY   270  '270'
              370  LOAD_CONST               None
              372  STORE_FAST               'why'
              374  DELETE_FAST              'why'
              376  END_FINALLY      
              378  POP_EXCEPT       
              380  JUMP_FORWARD        384  'to 384'
            382_0  COME_FROM           260  '260'
              382  END_FINALLY      
            384_0  COME_FROM           380  '380'
            384_1  COME_FROM           248  '248'

 L. 241       384  SETUP_FINALLY       398  'to 398'

 L. 242       386  LOAD_FAST                'options'
              388  LOAD_METHOD              fork
              390  CALL_METHOD_0         0  ''
              392  STORE_FAST               'pid'
              394  POP_BLOCK        
              396  JUMP_FORWARD        552  'to 552'
            398_0  COME_FROM_FINALLY   384  '384'

 L. 243       398  DUP_TOP          
              400  LOAD_GLOBAL              OSError
              402  COMPARE_OP               exception-match
          404_406  POP_JUMP_IF_FALSE   550  'to 550'
              408  POP_TOP          
              410  STORE_FAST               'why'
              412  POP_TOP          
              414  SETUP_FINALLY       538  'to 538'

 L. 244       416  LOAD_FAST                'why'
              418  LOAD_ATTR                args
              420  LOAD_CONST               0
              422  BINARY_SUBSCR    
              424  STORE_FAST               'code'

 L. 245       426  LOAD_FAST                'code'
              428  LOAD_GLOBAL              errno
              430  LOAD_ATTR                EAGAIN
              432  COMPARE_OP               ==
          434_436  POP_JUMP_IF_FALSE   448  'to 448'

 L. 247       438  LOAD_STR                 "Too many processes in process table to spawn '%s'"

 L. 248       440  LOAD_FAST                'processname'

 L. 247       442  BINARY_MODULO    
              444  STORE_FAST               'msg'
              446  JUMP_FORWARD        470  'to 470'
            448_0  COME_FROM           434  '434'

 L. 250       448  LOAD_STR                 "unknown error during fork for '%s': %s"

 L. 251       450  LOAD_FAST                'processname'

 L. 251       452  LOAD_GLOBAL              errno
              454  LOAD_ATTR                errorcode
              456  LOAD_METHOD              get
              458  LOAD_FAST                'code'
              460  LOAD_FAST                'code'
              462  CALL_METHOD_2         2  ''

 L. 250       464  BUILD_TUPLE_2         2 
              466  BINARY_MODULO    
              468  STORE_FAST               'msg'
            470_0  COME_FROM           446  '446'

 L. 252       470  LOAD_FAST                'self'
              472  LOAD_METHOD              record_spawnerr
              474  LOAD_FAST                'msg'
              476  CALL_METHOD_1         1  ''
              478  POP_TOP          

 L. 253       480  LOAD_FAST                'self'
              482  LOAD_METHOD              _assertInState
              484  LOAD_GLOBAL              ProcessStates
              486  LOAD_ATTR                STARTING
              488  CALL_METHOD_1         1  ''
              490  POP_TOP          

 L. 254       492  LOAD_FAST                'self'
              494  LOAD_METHOD              change_state
              496  LOAD_GLOBAL              ProcessStates
              498  LOAD_ATTR                BACKOFF
              500  CALL_METHOD_1         1  ''
              502  POP_TOP          

 L. 255       504  LOAD_FAST                'options'
              506  LOAD_METHOD              close_parent_pipes
              508  LOAD_FAST                'self'
              510  LOAD_ATTR                pipes
              512  CALL_METHOD_1         1  ''
              514  POP_TOP          

 L. 256       516  LOAD_FAST                'options'
              518  LOAD_METHOD              close_child_pipes
              520  LOAD_FAST                'self'
              522  LOAD_ATTR                pipes
              524  CALL_METHOD_1         1  ''
              526  POP_TOP          

 L. 257       528  POP_BLOCK        
              530  POP_EXCEPT       
              532  CALL_FINALLY        538  'to 538'
              534  LOAD_CONST               None
              536  RETURN_VALUE     
            538_0  COME_FROM           532  '532'
            538_1  COME_FROM_FINALLY   414  '414'
              538  LOAD_CONST               None
              540  STORE_FAST               'why'
              542  DELETE_FAST              'why'
              544  END_FINALLY      
              546  POP_EXCEPT       
              548  JUMP_FORWARD        552  'to 552'
            550_0  COME_FROM           404  '404'
              550  END_FINALLY      
            552_0  COME_FROM           548  '548'
            552_1  COME_FROM           396  '396'

 L. 259       552  LOAD_FAST                'pid'
              554  LOAD_CONST               0
              556  COMPARE_OP               !=
          558_560  POP_JUMP_IF_FALSE   572  'to 572'

 L. 260       562  LOAD_FAST                'self'
              564  LOAD_METHOD              _spawn_as_parent
              566  LOAD_FAST                'pid'
              568  CALL_METHOD_1         1  ''
              570  RETURN_VALUE     
            572_0  COME_FROM           558  '558'

 L. 263       572  LOAD_FAST                'self'
              574  LOAD_METHOD              _spawn_as_child
              576  LOAD_FAST                'filename'
              578  LOAD_FAST                'argv'
              580  CALL_METHOD_2         2  ''
              582  RETURN_VALUE     

Parse error at or near `CALL_FINALLY' instruction at offset 204

    def _spawn_as_parent(self, pid):
        self.pid = pid
        options = self.config.options
        options.close_child_pipes(self.pipes)
        options.logger.info("spawned: '%s' with pid %s" % (as_string(self.config.name), pid))
        self.spawnerr = None
        self.delay = time.time() + self.config.startsecs
        options.pidhistory[pid] = self
        return pid

    def _prepare_child_fds(self):
        options = self.config.options
        options.dup2(self.pipes['child_stdin'], 0)
        options.dup2(self.pipes['child_stdout'], 1)
        if self.config.redirect_stderr:
            options.dup2(self.pipes['child_stdout'], 2)
        else:
            options.dup2(self.pipes['child_stderr'], 2)
        for i in range(3, options.minfds):
            options.close_fd(i)

    def _spawn_as_child--- This code section failed: ---

 L. 288         0  LOAD_FAST                'self'
                2  LOAD_ATTR                config
                4  LOAD_ATTR                options
                6  STORE_FAST               'options'

 L. 289      8_10  SETUP_FINALLY       554  'to 554'

 L. 298        12  LOAD_FAST                'options'
               14  LOAD_METHOD              setpgrp
               16  CALL_METHOD_0         0  ''
               18  POP_TOP          

 L. 300        20  LOAD_FAST                'self'
               22  LOAD_METHOD              _prepare_child_fds
               24  CALL_METHOD_0         0  ''
               26  POP_TOP          

 L. 304        28  LOAD_FAST                'self'
               30  LOAD_METHOD              set_uid
               32  CALL_METHOD_0         0  ''
               34  STORE_FAST               'setuid_msg'

 L. 305        36  LOAD_FAST                'setuid_msg'
               38  POP_JUMP_IF_FALSE    86  'to 86'

 L. 306        40  LOAD_FAST                'self'
               42  LOAD_ATTR                config
               44  LOAD_ATTR                uid
               46  STORE_FAST               'uid'

 L. 307        48  LOAD_STR                 "couldn't setuid to %s: %s\n"
               50  LOAD_FAST                'uid'
               52  LOAD_FAST                'setuid_msg'
               54  BUILD_TUPLE_2         2 
               56  BINARY_MODULO    
               58  STORE_FAST               'msg'

 L. 308        60  LOAD_FAST                'options'
               62  LOAD_METHOD              write
               64  LOAD_CONST               2
               66  LOAD_STR                 'supervisor: '
               68  LOAD_FAST                'msg'
               70  BINARY_ADD       
               72  CALL_METHOD_2         2  ''
               74  POP_TOP          

 L. 309        76  POP_BLOCK        
            78_80  CALL_FINALLY        554  'to 554'
               82  LOAD_CONST               None
               84  RETURN_VALUE     
             86_0  COME_FROM            38  '38'

 L. 312        86  LOAD_GLOBAL              os
               88  LOAD_ATTR                environ
               90  LOAD_METHOD              copy
               92  CALL_METHOD_0         0  ''
               94  STORE_FAST               'env'

 L. 313        96  LOAD_STR                 '1'
               98  LOAD_FAST                'env'
              100  LOAD_STR                 'SUPERVISOR_ENABLED'
              102  STORE_SUBSCR     

 L. 314       104  LOAD_FAST                'self'
              106  LOAD_ATTR                config
              108  LOAD_ATTR                serverurl
              110  STORE_FAST               'serverurl'

 L. 315       112  LOAD_FAST                'serverurl'
              114  LOAD_CONST               None
              116  COMPARE_OP               is
              118  POP_JUMP_IF_FALSE   130  'to 130'

 L. 316       120  LOAD_FAST                'self'
              122  LOAD_ATTR                config
              124  LOAD_ATTR                options
              126  LOAD_ATTR                serverurl
              128  STORE_FAST               'serverurl'
            130_0  COME_FROM           118  '118'

 L. 317       130  LOAD_FAST                'serverurl'
              132  POP_JUMP_IF_FALSE   142  'to 142'

 L. 318       134  LOAD_FAST                'serverurl'
              136  LOAD_FAST                'env'
              138  LOAD_STR                 'SUPERVISOR_SERVER_URL'
              140  STORE_SUBSCR     
            142_0  COME_FROM           132  '132'

 L. 319       142  LOAD_FAST                'self'
              144  LOAD_ATTR                config
              146  LOAD_ATTR                name
              148  LOAD_FAST                'env'
              150  LOAD_STR                 'SUPERVISOR_PROCESS_NAME'
              152  STORE_SUBSCR     

 L. 320       154  LOAD_FAST                'self'
              156  LOAD_ATTR                group
              158  POP_JUMP_IF_FALSE   174  'to 174'

 L. 321       160  LOAD_FAST                'self'
              162  LOAD_ATTR                group
              164  LOAD_ATTR                config
              166  LOAD_ATTR                name
              168  LOAD_FAST                'env'
              170  LOAD_STR                 'SUPERVISOR_GROUP_NAME'
              172  STORE_SUBSCR     
            174_0  COME_FROM           158  '158'

 L. 322       174  LOAD_FAST                'self'
              176  LOAD_ATTR                config
              178  LOAD_ATTR                environment
              180  LOAD_CONST               None
              182  COMPARE_OP               is-not
              184  POP_JUMP_IF_FALSE   200  'to 200'

 L. 323       186  LOAD_FAST                'env'
              188  LOAD_METHOD              update
              190  LOAD_FAST                'self'
              192  LOAD_ATTR                config
              194  LOAD_ATTR                environment
              196  CALL_METHOD_1         1  ''
              198  POP_TOP          
            200_0  COME_FROM           184  '184'

 L. 326       200  LOAD_FAST                'self'
              202  LOAD_ATTR                config
              204  LOAD_ATTR                directory
              206  STORE_FAST               'cwd'

 L. 327       208  SETUP_FINALLY       232  'to 232'

 L. 328       210  LOAD_FAST                'cwd'
              212  LOAD_CONST               None
              214  COMPARE_OP               is-not
              216  POP_JUMP_IF_FALSE   228  'to 228'

 L. 329       218  LOAD_FAST                'options'
              220  LOAD_METHOD              chdir
              222  LOAD_FAST                'cwd'
              224  CALL_METHOD_1         1  ''
              226  POP_TOP          
            228_0  COME_FROM           216  '216'
              228  POP_BLOCK        
              230  JUMP_FORWARD        332  'to 332'
            232_0  COME_FROM_FINALLY   208  '208'

 L. 330       232  DUP_TOP          
              234  LOAD_GLOBAL              OSError
              236  COMPARE_OP               exception-match
          238_240  POP_JUMP_IF_FALSE   330  'to 330'
              242  POP_TOP          
              244  STORE_FAST               'why'
              246  POP_TOP          
              248  SETUP_FINALLY       318  'to 318'

 L. 331       250  LOAD_GLOBAL              errno
              252  LOAD_ATTR                errorcode
              254  LOAD_METHOD              get
              256  LOAD_FAST                'why'
              258  LOAD_ATTR                args
              260  LOAD_CONST               0
              262  BINARY_SUBSCR    
              264  LOAD_FAST                'why'
              266  LOAD_ATTR                args
              268  LOAD_CONST               0
              270  BINARY_SUBSCR    
              272  CALL_METHOD_2         2  ''
              274  STORE_FAST               'code'

 L. 332       276  LOAD_STR                 "couldn't chdir to %s: %s\n"
              278  LOAD_FAST                'cwd'
              280  LOAD_FAST                'code'
              282  BUILD_TUPLE_2         2 
              284  BINARY_MODULO    
              286  STORE_FAST               'msg'

 L. 333       288  LOAD_FAST                'options'
              290  LOAD_METHOD              write
              292  LOAD_CONST               2
              294  LOAD_STR                 'supervisor: '
              296  LOAD_FAST                'msg'
              298  BINARY_ADD       
              300  CALL_METHOD_2         2  ''
              302  POP_TOP          

 L. 334       304  POP_BLOCK        
              306  POP_EXCEPT       
              308  CALL_FINALLY        318  'to 318'
              310  POP_BLOCK        
              312  CALL_FINALLY        554  'to 554'
              314  LOAD_CONST               None
              316  RETURN_VALUE     
            318_0  COME_FROM           308  '308'
            318_1  COME_FROM_FINALLY   248  '248'
              318  LOAD_CONST               None
              320  STORE_FAST               'why'
              322  DELETE_FAST              'why'
              324  END_FINALLY      
              326  POP_EXCEPT       
              328  JUMP_FORWARD        332  'to 332'
            330_0  COME_FROM           238  '238'
              330  END_FINALLY      
            332_0  COME_FROM           328  '328'
            332_1  COME_FROM           230  '230'

 L. 337       332  SETUP_FINALLY       380  'to 380'

 L. 338       334  LOAD_FAST                'self'
              336  LOAD_ATTR                config
              338  LOAD_ATTR                umask
              340  LOAD_CONST               None
              342  COMPARE_OP               is-not
          344_346  POP_JUMP_IF_FALSE   362  'to 362'

 L. 339       348  LOAD_FAST                'options'
              350  LOAD_METHOD              setumask
              352  LOAD_FAST                'self'
              354  LOAD_ATTR                config
              356  LOAD_ATTR                umask
              358  CALL_METHOD_1         1  ''
              360  POP_TOP          
            362_0  COME_FROM           344  '344'

 L. 340       362  LOAD_FAST                'options'
              364  LOAD_METHOD              execve
              366  LOAD_FAST                'filename'
              368  LOAD_FAST                'argv'
              370  LOAD_FAST                'env'
              372  CALL_METHOD_3         3  ''
              374  POP_TOP          
              376  POP_BLOCK        
              378  JUMP_FORWARD        550  'to 550'
            380_0  COME_FROM_FINALLY   332  '332'

 L. 341       380  DUP_TOP          
              382  LOAD_GLOBAL              OSError
              384  COMPARE_OP               exception-match
          386_388  POP_JUMP_IF_FALSE   472  'to 472'
              390  POP_TOP          
              392  STORE_FAST               'why'
              394  POP_TOP          
              396  SETUP_FINALLY       460  'to 460'

 L. 342       398  LOAD_GLOBAL              errno
              400  LOAD_ATTR                errorcode
              402  LOAD_METHOD              get
              404  LOAD_FAST                'why'
              406  LOAD_ATTR                args
              408  LOAD_CONST               0
              410  BINARY_SUBSCR    
              412  LOAD_FAST                'why'
              414  LOAD_ATTR                args
              416  LOAD_CONST               0
              418  BINARY_SUBSCR    
              420  CALL_METHOD_2         2  ''
              422  STORE_FAST               'code'

 L. 343       424  LOAD_STR                 "couldn't exec %s: %s\n"
              426  LOAD_FAST                'argv'
              428  LOAD_CONST               0
              430  BINARY_SUBSCR    
              432  LOAD_FAST                'code'
              434  BUILD_TUPLE_2         2 
              436  BINARY_MODULO    
              438  STORE_FAST               'msg'

 L. 344       440  LOAD_FAST                'options'
              442  LOAD_METHOD              write
              444  LOAD_CONST               2
              446  LOAD_STR                 'supervisor: '
              448  LOAD_FAST                'msg'
              450  BINARY_ADD       
              452  CALL_METHOD_2         2  ''
              454  POP_TOP          
              456  POP_BLOCK        
              458  BEGIN_FINALLY    
            460_0  COME_FROM_FINALLY   396  '396'
              460  LOAD_CONST               None
              462  STORE_FAST               'why'
              464  DELETE_FAST              'why'
              466  END_FINALLY      
              468  POP_EXCEPT       
              470  JUMP_FORWARD        550  'to 550'
            472_0  COME_FROM           386  '386'

 L. 345       472  POP_TOP          
              474  POP_TOP          
              476  POP_TOP          

 L. 346       478  LOAD_GLOBAL              asyncore
              480  LOAD_METHOD              compact_traceback
              482  CALL_METHOD_0         0  ''
              484  UNPACK_SEQUENCE_4     4 
              486  UNPACK_SEQUENCE_3     3 
              488  STORE_FAST               'file'
              490  STORE_FAST               'fun'
              492  STORE_FAST               'line'
              494  STORE_FAST               't'
              496  STORE_FAST               'v'
              498  STORE_FAST               'tbinfo'

 L. 347       500  LOAD_STR                 '%s, %s: file: %s line: %s'
              502  LOAD_FAST                't'
              504  LOAD_FAST                'v'
              506  LOAD_FAST                'file'
              508  LOAD_FAST                'line'
              510  BUILD_TUPLE_4         4 
              512  BINARY_MODULO    
              514  STORE_FAST               'error'

 L. 348       516  LOAD_STR                 "couldn't exec %s: %s\n"
              518  LOAD_FAST                'filename'
              520  LOAD_FAST                'error'
              522  BUILD_TUPLE_2         2 
              524  BINARY_MODULO    
              526  STORE_FAST               'msg'

 L. 349       528  LOAD_FAST                'options'
              530  LOAD_METHOD              write
              532  LOAD_CONST               2
              534  LOAD_STR                 'supervisor: '
              536  LOAD_FAST                'msg'
              538  BINARY_ADD       
              540  CALL_METHOD_2         2  ''
              542  POP_TOP          
              544  POP_EXCEPT       
              546  JUMP_FORWARD        550  'to 550'
              548  END_FINALLY      
            550_0  COME_FROM           546  '546'
            550_1  COME_FROM           470  '470'
            550_2  COME_FROM           378  '378'
              550  POP_BLOCK        
              552  BEGIN_FINALLY    
            554_0  COME_FROM           312  '312'
            554_1  COME_FROM            78  '78'
            554_2  COME_FROM_FINALLY     8  '8'

 L. 355       554  LOAD_FAST                'options'
              556  LOAD_METHOD              write
              558  LOAD_CONST               2
              560  LOAD_STR                 'supervisor: child process was not spawned\n'
              562  CALL_METHOD_2         2  ''
              564  POP_TOP          

 L. 356       566  LOAD_FAST                'options'
              568  LOAD_METHOD              _exit
              570  LOAD_CONST               127
              572  CALL_METHOD_1         1  ''
              574  POP_TOP          
              576  END_FINALLY      

Parse error at or near `CALL_FINALLY' instruction at offset 78_80

    def _check_and_adjust_for_system_clock_rollback(self, test_time):
        """
        Check if system clock has rolled backward beyond test_time. If so, set
        affected timestamps to test_time.
        """
        if self.state == ProcessStates.STARTING:
            if test_time < self.laststart:
                self.laststart = test_time
            if self.delay > 0 and test_time < self.delay - self.config.startsecs:
                self.delay = test_time + self.config.startsecs
        elif self.state == ProcessStates.RUNNING:
            if test_time > self.laststart and test_time < self.laststart + self.config.startsecs:
                self.laststart = test_time - self.config.startsecs
        elif self.state == ProcessStates.STOPPING:
            if test_time < self.laststopreport:
                self.laststopreport = test_time
            if self.delay > 0 and test_time < self.delay - self.config.stopwaitsecs:
                self.delay = test_time + self.config.stopwaitsecs
        elif self.state == ProcessStates.BACKOFF and self.delay > 0 and test_time < self.delay - self.backoff:
            self.delay = test_time + self.backoff

    def stop(self):
        """ Administrative stop """
        self.administrative_stop = True
        self.laststopreport = 0
        return self.kill(self.config.stopsignal)

    def stop_report(self):
        """ Log a 'waiting for x to stop' message with throttling. """
        if self.state == ProcessStates.STOPPING:
            now = time.time()
            self._check_and_adjust_for_system_clock_rollback(now)
            if now > self.laststopreport + 2:
                self.config.options.logger.info('waiting for %s to stop' % as_string(self.config.name))
                self.laststopreport = now

    def give_up(self):
        self.delay = 0
        self.backoff = 0
        self.system_stop = True
        self._assertInState(ProcessStates.BACKOFF)
        self.change_state(ProcessStates.FATAL)

    def kill(self, sig):
        """Send a signal to the subprocess.  This may or may not kill it.

        Return None if the signal was sent, or an error message string
        if an error occurred or if the subprocess is not running.
        """
        now = time.time()
        options = self.config.options
        processname = as_string(self.config.name)
        if self.state == ProcessStates.BACKOFF:
            msg = 'Attempted to kill %s, which is in BACKOFF state.' % processname
            options.logger.debug(msg)
            self.change_state(ProcessStates.STOPPED)
            return None
        elif not self.pid:
            msg = "attempted to kill %s with sig %s but it wasn't running" % (
             processname, signame(sig))
            options.logger.debug(msg)
            return msg
            if self.state == ProcessStates.STOPPING:
                killasgroup = self.config.killasgroup
        else:
            killasgroup = self.config.stopasgroup
        as_group = ''
        if killasgroup:
            as_group = 'process group '
        options.logger.debug('killing %s (pid %s) %swith signal %s' % (
         processname,
         self.pid,
         as_group,
         signame(sig)))
        self.killing = True
        self.delay = now + self.config.stopwaitsecs
        self._assertInState(ProcessStates.RUNNING, ProcessStates.STARTING, ProcessStates.STOPPING)
        self.change_state(ProcessStates.STOPPING)
        pid = self.pid
        if killasgroup:
            pid = -self.pid
        try:
            options.kill(pid, sig)
        except:
            tb = traceback.format_exc()
            msg = 'unknown problem killing %s (%s):%s' % (processname,
             self.pid, tb)
            options.logger.critical(msg)
            self.change_state(ProcessStates.UNKNOWN)
            self.pid = 0
            self.killing = False
            self.delay = 0
            return msg

    def signal(self, sig):
        """Send a signal to the subprocess, without intending to kill it.

        Return None if the signal was sent, or an error message string
        if an error occurred or if the subprocess is not running.
        """
        options = self.config.options
        processname = as_string(self.config.name)
        if not self.pid:
            msg = "attempted to send %s sig %s but it wasn't running" % (
             processname, signame(sig))
            options.logger.debug(msg)
            return msg
        options.logger.debug('sending %s (pid %s) sig %s' % (
         processname,
         self.pid,
         signame(sig)))
        self._assertInState(ProcessStates.RUNNING, ProcessStates.STARTING, ProcessStates.STOPPING)
        try:
            options.kill(self.pid, sig)
        except:
            tb = traceback.format_exc()
            msg = 'unknown problem sending sig %s (%s):%s' % (
             processname, self.pid, tb)
            options.logger.critical(msg)
            self.change_state(ProcessStates.UNKNOWN)
            self.pid = 0
            return msg

    def finish(self, pid, sts):
        """ The process was reaped and we need to report and manage its state
        """
        self.drain()
        es, msg = decode_wait_status(sts)
        now = time.time()
        self._check_and_adjust_for_system_clock_rollback(now)
        self.laststop = now
        processname = as_string(self.config.name)
        if now > self.laststart:
            too_quickly = now - self.laststart < self.config.startsecs
        else:
            too_quickly = False
            self.config.options.logger.warn("process '%s' (%s) laststart time is in the future, don't know how long process was running so assuming it did not exit too quickly" % (
             processname, self.pid))
        exit_expected = es in self.config.exitcodes
        if self.killing:
            self.killing = False
            self.delay = 0
            self.exitstatus = es
            msg = 'stopped: %s (%s)' % (processname, msg)
            self._assertInState(ProcessStates.STOPPING)
            self.change_state(ProcessStates.STOPPED)
        else:
            if too_quickly:
                self.exitstatus = None
                self.spawnerr = 'Exited too quickly (process log may have details)'
                msg = 'exited: %s (%s)' % (processname, msg + '; not expected')
                self._assertInState(ProcessStates.STARTING)
                self.change_state(ProcessStates.BACKOFF)
            else:
                self.delay = 0
                self.backoff = 0
                self.exitstatus = es
                if self.state == ProcessStates.STARTING:
                    self.change_state(ProcessStates.RUNNING)
                else:
                    self._assertInState(ProcessStates.RUNNING)
                    if exit_expected:
                        msg = 'exited: %s (%s)' % (processname, msg + '; expected')
                        self.change_state((ProcessStates.EXITED), expected=True)
                    else:
                        self.spawnerr = 'Bad exit code %s' % es
                    msg = 'exited: %s (%s)' % (processname, msg + '; not expected')
                    self.change_state((ProcessStates.EXITED), expected=False)
        self.config.options.logger.info(msg)
        self.pid = 0
        self.config.options.close_parent_pipes(self.pipes)
        self.pipes = {}
        self.dispatchers = {}
        if self.event is not None:
            events.notify(events.EventRejectedEvent(self, self.event))
            self.event = None

    def set_uid(self):
        if self.config.uid is None:
            return
        msg = self.config.options.drop_privileges(self.config.uid)
        return msg

    def __lt__(self, other):
        return self.config.priority < other.config.priority

    def __eq__(self, other):
        return self.config.priority == other.config.priority

    def __repr__(self):
        name = self.config.name
        if PY2:
            name = as_string(name).encode('unicode-escape')
        return '<Subprocess at %s with name %s in state %s>' % (
         id(self),
         name,
         getProcessStateDescription(self.get_state()))

    def get_state(self):
        return self.state

    def transition(self):
        now = time.time()
        state = self.state
        self._check_and_adjust_for_system_clock_rollback(now)
        logger = self.config.options.logger
        if self.config.options.mood > SupervisorStates.RESTARTING:
            if state == ProcessStates.EXITED:
                if self.config.autorestart:
                    if self.config.autorestart is RestartUnconditionally:
                        self.spawn()
                    elif self.exitstatus not in self.config.exitcodes:
                        self.spawn()
            elif state == ProcessStates.STOPPED:
                if not self.laststart:
                    if self.config.autostart:
                        self.spawn()
            elif state == ProcessStates.BACKOFF and self.backoff <= self.config.startretries and now > self.delay:
                self.spawn()
        processname = as_string(self.config.name)
        if state == ProcessStates.STARTING:
            if now - self.laststart > self.config.startsecs:
                self.delay = 0
                self.backoff = 0
                self._assertInState(ProcessStates.STARTING)
                self.change_state(ProcessStates.RUNNING)
                msg = 'entered RUNNING state, process has stayed up for > than %s seconds (startsecs)' % self.config.startsecs
                logger.info('success: %s %s' % (processname, msg))
            if state == ProcessStates.BACKOFF:
                if self.backoff > self.config.startretries:
                    self.give_up()
                    msg = 'entered FATAL state, too many start retries too quickly'
                    logger.info('gave up: %s %s' % (processname, msg))
        elif state == ProcessStates.STOPPING:
            time_left = self.delay - now
            if time_left <= 0:
                self.config.options.logger.warn("killing '%s' (%s) with SIGKILL" % (processname,
                 self.pid))
                self.kill(signal.SIGKILL)


class FastCGISubprocess(Subprocess):
    __doc__ = 'Extends Subprocess class to handle FastCGI subprocesses'

    def __init__(self, config):
        Subprocess.__init__(self, config)
        self.fcgi_sock = None

    def before_spawn(self):
        """
        The FastCGI socket needs to be created by the parent before we fork
        """
        if self.group is None:
            raise NotImplementedError('No group set for FastCGISubprocess')
        if not hasattr(self.group, 'socket_manager'):
            raise NotImplementedError('No SocketManager set for %s:%s' % (
             self.group, dir(self.group)))
        self.fcgi_sock = self.group.socket_manager.get_socket()

    def spawn(self):
        """
        Overrides Subprocess.spawn() so we can hook in before it happens
        """
        self.before_spawn()
        pid = Subprocess.spawn(self)
        if pid is None:
            self.fcgi_sock = None
        return pid

    def after_finish(self):
        """
        Releases reference to FastCGI socket when process is reaped
        """
        self.fcgi_sock = None

    def finish(self, pid, sts):
        """
        Overrides Subprocess.finish() so we can hook in after it happens
        """
        retval = Subprocess.finish(self, pid, sts)
        self.after_finish()
        return retval

    def _prepare_child_fds(self):
        """
        Overrides Subprocess._prepare_child_fds()
        The FastCGI socket needs to be set to file descriptor 0 in the child
        """
        sock_fd = self.fcgi_sock.fileno()
        options = self.config.options
        options.dup2(sock_fd, 0)
        options.dup2(self.pipes['child_stdout'], 1)
        if self.config.redirect_stderr:
            options.dup2(self.pipes['child_stdout'], 2)
        else:
            options.dup2(self.pipes['child_stderr'], 2)
        for i in range(3, options.minfds):
            options.close_fd(i)


@total_ordering
class ProcessGroupBase(object):

    def __init__(self, config):
        self.config = config
        self.processes = {}
        for pconfig in self.config.process_configs:
            self.processes[pconfig.name] = pconfig.make_process(self)

    def __lt__(self, other):
        return self.config.priority < other.config.priority

    def __eq__(self, other):
        return self.config.priority == other.config.priority

    def __repr__(self):
        name = self.config.name
        if PY2:
            name = as_string(name).encode('unicode-escape')
        return '<%s instance at %s named %s>' % (self.__class__, id(self),
         name)

    def removelogs(self):
        for process in self.processes.values():
            process.removelogs()

    def reopenlogs(self):
        for process in self.processes.values():
            process.reopenlogs()

    def stop_all(self):
        processes = list(self.processes.values())
        processes.sort()
        processes.reverse()
        for proc in processes:
            state = proc.get_state()
            if state == ProcessStates.RUNNING:
                proc.stop()
            elif state == ProcessStates.STARTING:
                proc.stop()
            elif state == ProcessStates.BACKOFF:
                proc.give_up()

    def get_unstopped_processes(self):
        """ Processes which aren't in a state that is considered 'stopped' """
        return [x for x in self.processes.values() if x.get_state() not in STOPPED_STATES]

    def get_dispatchers(self):
        dispatchers = {}
        for process in self.processes.values():
            dispatchers.update(process.dispatchers)
        else:
            return dispatchers

    def before_remove(self):
        pass


class ProcessGroup(ProcessGroupBase):

    def transition(self):
        for proc in self.processes.values():
            proc.transition()


class FastCGIProcessGroup(ProcessGroup):

    def __init__(self, config, **kwargs):
        ProcessGroup.__init__(self, config)
        sockManagerKlass = kwargs.get('socketManager', SocketManager)
        self.socket_manager = sockManagerKlass((config.socket_config), logger=(config.options.logger))
        try:
            self.socket_manager.get_socket()
        except Exception as e:
            try:
                raise ValueError('Could not create FastCGI socket %s: %s' % (
                 self.socket_manager.config(), e))
            finally:
                e = None
                del e


class EventListenerPool(ProcessGroupBase):

    def __init__(self, config):
        ProcessGroupBase.__init__(self, config)
        self.event_buffer = []
        self.serial = -1
        self.last_dispatch = 0
        self.dispatch_throttle = 0
        self._subscribe()

    def handle_rejected(self, event):
        process = event.process
        procs = self.processes.values()
        if process in procs:
            self._acceptEvent((event.event), head=True)

    def transition(self):
        processes = self.processes.values()
        dispatch_capable = False
        for process in processes:
            process.transition()
            if process.state == ProcessStates.RUNNING and process.listener_state == EventListenerStates.READY:
                dispatch_capable = True
        else:
            if dispatch_capable:
                if self.dispatch_throttle:
                    now = time.time()
                    if now < self.last_dispatch:
                        self.last_dispatch = now
                    if now - self.last_dispatch < self.dispatch_throttle:
                        return
                self.dispatch()

    def before_remove(self):
        self._unsubscribe()

    def dispatch(self):
        while self.event_buffer:
            event = self.event_buffer.pop(0)
            ok = self._dispatchEvent(event)
            if not ok:
                self._acceptEvent(event, head=True)
                break

        self.last_dispatch = time.time()

    def _acceptEvent(self, event, head=False):
        processname = as_string(self.config.name)
        if not hasattr(event, 'serial'):
            event.serial = new_serial(GlobalSerial)
        if not hasattr(event, 'pool_serials'):
            event.pool_serials = {}
        else:
            if self.config.name not in event.pool_serials:
                event.pool_serials[self.config.name] = new_serial(self)
            else:
                self.config.options.logger.debug('rebuffering event %s for pool %s (buf size=%d, max=%d)' % (
                 event.serial, processname, len(self.event_buffer),
                 self.config.buffer_size))
            if len(self.event_buffer) >= self.config.buffer_size:
                if self.event_buffer:
                    discarded_event = self.event_buffer.pop(0)
                    self.config.options.logger.error('pool %s event buffer overflowed, discarding event %s' % (
                     processname, discarded_event.serial))
            if head:
                self.event_buffer.insert(0, event)
            else:
                self.event_buffer.append(event)

    def _dispatchEvent--- This code section failed: ---

 L. 925         0  LOAD_FAST                'event'
                2  LOAD_ATTR                pool_serials
                4  LOAD_FAST                'self'
                6  LOAD_ATTR                config
                8  LOAD_ATTR                name
               10  BINARY_SUBSCR    
               12  STORE_FAST               'pool_serial'

 L. 927        14  LOAD_FAST                'self'
               16  LOAD_ATTR                processes
               18  LOAD_METHOD              values
               20  CALL_METHOD_0         0  ''
               22  GET_ITER         
             24_0  COME_FROM            52  '52'
               24  FOR_ITER            256  'to 256'
               26  STORE_FAST               'process'

 L. 928        28  LOAD_FAST                'process'
               30  LOAD_ATTR                state
               32  LOAD_GLOBAL              ProcessStates
               34  LOAD_ATTR                RUNNING
               36  COMPARE_OP               !=
               38  POP_JUMP_IF_FALSE    42  'to 42'

 L. 929        40  JUMP_BACK            24  'to 24'
             42_0  COME_FROM            38  '38'

 L. 930        42  LOAD_FAST                'process'
               44  LOAD_ATTR                listener_state
               46  LOAD_GLOBAL              EventListenerStates
               48  LOAD_ATTR                READY
               50  COMPARE_OP               ==
               52  POP_JUMP_IF_FALSE    24  'to 24'

 L. 931        54  LOAD_GLOBAL              as_string
               56  LOAD_FAST                'process'
               58  LOAD_ATTR                config
               60  LOAD_ATTR                name
               62  CALL_FUNCTION_1       1  ''
               64  STORE_FAST               'processname'

 L. 932        66  LOAD_FAST                'event'
               68  LOAD_METHOD              payload
               70  CALL_METHOD_0         0  ''
               72  STORE_FAST               'payload'

 L. 933        74  SETUP_FINALLY       122  'to 122'

 L. 934        76  LOAD_FAST                'event'
               78  LOAD_ATTR                __class__
               80  STORE_FAST               'event_type'

 L. 935        82  LOAD_FAST                'event'
               84  LOAD_ATTR                serial
               86  STORE_FAST               'serial'

 L. 936        88  LOAD_FAST                'self'
               90  LOAD_METHOD              _eventEnvelope
               92  LOAD_FAST                'event_type'
               94  LOAD_FAST                'serial'

 L. 937        96  LOAD_FAST                'pool_serial'

 L. 937        98  LOAD_FAST                'payload'

 L. 936       100  CALL_METHOD_4         4  ''
              102  STORE_FAST               'envelope'

 L. 938       104  LOAD_FAST                'process'
              106  LOAD_METHOD              write
              108  LOAD_GLOBAL              as_bytes
              110  LOAD_FAST                'envelope'
              112  CALL_FUNCTION_1       1  ''
              114  CALL_METHOD_1         1  ''
              116  POP_TOP          
              118  POP_BLOCK        
              120  JUMP_FORWARD        208  'to 208'
            122_0  COME_FROM_FINALLY    74  '74'

 L. 939       122  DUP_TOP          
              124  LOAD_GLOBAL              OSError
              126  COMPARE_OP               exception-match
              128  POP_JUMP_IF_FALSE   206  'to 206'
              130  POP_TOP          
              132  STORE_FAST               'why'
              134  POP_TOP          
              136  SETUP_FINALLY       194  'to 194'

 L. 940       138  LOAD_FAST                'why'
              140  LOAD_ATTR                args
              142  LOAD_CONST               0
              144  BINARY_SUBSCR    
              146  LOAD_GLOBAL              errno
              148  LOAD_ATTR                EPIPE
              150  COMPARE_OP               !=
              152  POP_JUMP_IF_FALSE   156  'to 156'

 L. 941       154  RAISE_VARARGS_0       0  'reraise'
            156_0  COME_FROM           152  '152'

 L. 943       156  LOAD_FAST                'self'
              158  LOAD_ATTR                config
              160  LOAD_ATTR                options
              162  LOAD_ATTR                logger
              164  LOAD_METHOD              debug

 L. 944       166  LOAD_STR                 'epipe occurred while sending event %s to listener %s, listener state unchanged'

 L. 946       168  LOAD_FAST                'event'
              170  LOAD_ATTR                serial

 L. 946       172  LOAD_FAST                'processname'

 L. 945       174  BUILD_TUPLE_2         2 

 L. 944       176  BINARY_MODULO    

 L. 943       178  CALL_METHOD_1         1  ''
              180  POP_TOP          

 L. 947       182  POP_BLOCK        
              184  POP_EXCEPT       
              186  CALL_FINALLY        194  'to 194'
              188  JUMP_BACK            24  'to 24'
              190  POP_BLOCK        
              192  BEGIN_FINALLY    
            194_0  COME_FROM           186  '186'
            194_1  COME_FROM_FINALLY   136  '136'
              194  LOAD_CONST               None
              196  STORE_FAST               'why'
              198  DELETE_FAST              'why'
              200  END_FINALLY      
              202  POP_EXCEPT       
              204  JUMP_FORWARD        208  'to 208'
            206_0  COME_FROM           128  '128'
              206  END_FINALLY      
            208_0  COME_FROM           204  '204'
            208_1  COME_FROM           120  '120'

 L. 949       208  LOAD_GLOBAL              EventListenerStates
              210  LOAD_ATTR                BUSY
              212  LOAD_FAST                'process'
              214  STORE_ATTR               listener_state

 L. 950       216  LOAD_FAST                'event'
              218  LOAD_FAST                'process'
              220  STORE_ATTR               event

 L. 951       222  LOAD_FAST                'self'
              224  LOAD_ATTR                config
              226  LOAD_ATTR                options
              228  LOAD_ATTR                logger
              230  LOAD_METHOD              debug

 L. 952       232  LOAD_STR                 'event %s sent to listener %s'

 L. 953       234  LOAD_FAST                'event'
              236  LOAD_ATTR                serial

 L. 953       238  LOAD_FAST                'processname'

 L. 952       240  BUILD_TUPLE_2         2 
              242  BINARY_MODULO    

 L. 951       244  CALL_METHOD_1         1  ''
              246  POP_TOP          

 L. 954       248  POP_TOP          
              250  LOAD_CONST               True
              252  RETURN_VALUE     
              254  JUMP_BACK            24  'to 24'

 L. 956       256  LOAD_CONST               False
              258  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `CALL_FINALLY' instruction at offset 186

    def _eventEnvelope(self, event_type, serial, pool_serial, payload):
        event_name = events.getEventNameByType(event_type)
        payload_len = len(payload)
        D = {'ver':'3.0', 
         'sid':self.config.options.identifier, 
         'serial':serial, 
         'pool_name':self.config.name, 
         'pool_serial':pool_serial, 
         'event_name':event_name, 
         'len':payload_len, 
         'payload':payload}
        return 'ver:%(ver)s server:%(sid)s serial:%(serial)s pool:%(pool_name)s poolserial:%(pool_serial)s eventname:%(event_name)s len:%(len)s\n%(payload)s' % D

    def _subscribe(self):
        for event_type in self.config.pool_events:
            events.subscribe(event_type, self._acceptEvent)
        else:
            events.subscribe(events.EventRejectedEvent, self.handle_rejected)

    def _unsubscribe(self):
        for event_type in self.config.pool_events:
            events.unsubscribe(event_type, self._acceptEvent)
        else:
            events.unsubscribe(events.EventRejectedEvent, self.handle_rejected)


class GlobalSerial(object):

    def __init__(self):
        self.serial = -1


GlobalSerial = GlobalSerial()

def new_serial(inst):
    if inst.serial == maxint:
        inst.serial = -1
    inst.serial += 1
    return inst.serial