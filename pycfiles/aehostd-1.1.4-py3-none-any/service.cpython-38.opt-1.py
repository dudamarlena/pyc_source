# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /aehostd/service.py
# Compiled at: 2020-05-10 12:27:18
# Size of source mod 2**32: 11052 bytes
"""
aehostd.service - Unix domain socket server
"""
import sys, os, socket, socketserver, time, logging, logging.handlers, struct, argparse, signal
from lockfile.pidlockfile import PIDLockFile
import daemon
from .__about__ import __version__
from .cfg import CFG
from . import req
from .tiostream import TIOStream
from .req import PROTO_VERSION
SO_PEERCRED_DICT = {'linux': (17, '3i')}
UMASK_DEFAULT = 18
SYS_LOG_FORMAT = '%(levelname)s %(message)s'
CONSOLE_LOG_FORMAT = '%(asctime)s %(levelname)s %(message)s'

def cli_args(script_name, service_desc):
    """
    CLI arguments
    """
    parser = argparse.ArgumentParser(prog=script_name,
      formatter_class=(argparse.ArgumentDefaultsHelpFormatter),
      description=service_desc)
    parser.add_argument('-f',
      '--config', dest='cfg_filename',
      default='/etc/aehostd.conf',
      help='configuration file name',
      required=False)
    parser.add_argument('-p',
      '--pid', dest='pidfile',
      default=(os.path.join('/', 'var', 'run', 'aehostd', script_name) + '.pid'),
      help='PID file name',
      required=False)
    parser.add_argument('-l',
      '--log-level', dest='log_level',
      default=None,
      help='log level',
      type=int,
      required=False)
    parser.add_argument('-n',
      '--no-fork', dest='no_fork',
      default=False,
      help='Do not fork or daemonise, run in the foreground.',
      action='store_true',
      required=False)
    parser.add_argument('-c',
      '--check', dest='check_only',
      default=False,
      help='Check whether demon is running.',
      action='store_true',
      required=False)
    return parser.parse_args()


def init_logger(log_name, log_level, no_fork):
    """
    Returns a combined SysLogHandler/StreamHandler logging instance
    with formatters
    """
    if CFG.logsocket is None and no_fork:
        log_format = CONSOLE_LOG_FORMAT
        log_handler = logging.StreamHandler()
    else:
        log_format = '{name}[{pid}] {fmt}'.format(name=log_name,
          pid=(os.getpid()),
          fmt=SYS_LOG_FORMAT)
        log_handler = logging.handlers.SysLogHandler(address=(CFG.logsocket or '/dev/log'),
          facility=(logging.handlers.SysLogHandler.LOG_DAEMON))
    log_handler.setFormatter(logging.Formatter(fmt=log_format))
    the_logger = logging.getLogger()
    the_logger.addHandler(log_handler)
    if log_level is None:
        log_level = logging.INFO
    the_logger.setLevel(log_level)


def init_runtimedir(runtime_dir):
    """
    create run-time directory and set ownership and permissions
    """
    if os.getuid() != 0:
        logging.debug('Started as non-root user, leave run-time directory %r as is', runtime_dir)
        return None
    try:
        if not os.path.exists(runtime_dir):
            logging.debug('Creating run-time directory %r', runtime_dir)
            os.mkdir(runtime_dir)
        logging.debug('Set permissions and ownership of run-time directory %r', runtime_dir)
        os.chown(runtime_dir, CFG.uid, CFG.gid)
        os.chmod(runtime_dir, 493)
    except (IOError, OSError) as err:
        try:
            logging.warning('Failed setting permissions and ownership of run-time directory %r: %s', runtime_dir, err)
        finally:
            err = None
            del err


def init_service(log_name, service_desc, service_uid=None, service_gid=None):
    """
    initialize the service instance
    """
    script_name = os.path.basename(sys.argv[0])
    args = cli_args(script_name, service_desc)
    CFG.read_config(args.cfg_filename)
    init_logger(log_name, args.log_level, args.no_fork)
    logging.info('Starting %s %s [%d] reading config %s', script_name, __version__, os.getpid(), args.cfg_filename)
    for key, val in sorted(CFG.__dict__.items()):
        logging.debug('%s = %r', key, val)
    else:
        os.environ.clear()
        os.environ['HOME'] = '/'
        os.environ['TMPDIR'] = os.environ['TMP'] = '/tmp'
        os.environ['LDAPNOINIT'] = '1'
        if args.log_level is None:
            logging.getLogger().setLevel(CFG.loglevel)
        else:
            os.umask(UMASK_DEFAULT)
            pidfile = PIDLockFile(args.pidfile)
            runtime_dir = os.path.dirname(CFG.socketpath)
            init_runtimedir(runtime_dir)
            if args.check_only:
                if pidfile.is_locked():
                    logging.debug('pidfile (%s) is locked', args.pidfile)
                    sys.exit(0)
                else:
                    logging.debug('pidfile (%s) is not locked', args.pidfile)
                    sys.exit(1)
            else:
                if pidfile.is_locked():
                    logging.error('daemon may already be active, cannot acquire lock (%s)', args.pidfile)
                    sys.exit(1)
                if args.no_fork:
                    ctx = pidfile
                else:
                    if service_uid is None:
                        demon_uid = CFG.uid
                    else:
                        demon_uid = service_uid
                    if service_gid is None:
                        demon_gid = CFG.gid
                    else:
                        demon_gid = service_gid
            ctx = daemon.DaemonContext(pidfile=pidfile,
              umask=UMASK_DEFAULT,
              uid=demon_uid,
              gid=demon_gid,
              signal_map={signal.SIGTERM: 'terminate', 
             signal.SIGINT: 'terminate', 
             signal.SIGPIPE: None})
        return (
         script_name, ctx)


class TIOStreamRequestHandler(socketserver.BaseRequestHandler):
    __doc__ = '\n    handling a TIO stream request for NSS/PAM\n    '

    def _get_peer_cred(self):
        try:
            so_num, struct_fmt = SO_PEERCRED_DICT[sys.platform]
        except KeyError:
            return (None, None, None)
        else:
            peer_creds_struct = self.request.getsockopt(socket.SOL_SOCKET, so_num, struct.calcsize(struct_fmt))
            pid, uid, gid = struct.unpack(struct_fmt, peer_creds_struct)
            return (pid, uid, gid)

    def handle--- This code section failed: ---

 L. 240         0  LOAD_GLOBAL              time
                2  LOAD_METHOD              time
                4  CALL_METHOD_0         0  ''
                6  STORE_FAST               'start_time'

 L. 241         8  LOAD_FAST                'self'
               10  LOAD_ATTR                server
               12  DUP_TOP          
               14  LOAD_ATTR                _req_counter_all
               16  LOAD_CONST               1
               18  INPLACE_ADD      
               20  ROT_TWO          
               22  STORE_ATTR               _req_counter_all

 L. 242        24  LOAD_FAST                'self'
               26  LOAD_ATTR                request
               28  LOAD_ATTR                makefile
               30  LOAD_STR                 'rwb'
               32  LOAD_CONST               ('mode',)
               34  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               36  STORE_FAST               'req_file'

 L. 244        38  LOAD_GLOBAL              TIOStream
               40  LOAD_FAST                'req_file'
               42  CALL_FUNCTION_1       1  ''
               44  STORE_FAST               'tios'

 L. 246        46  LOAD_FAST                'tios'
               48  LOAD_METHOD              read_int32
               50  CALL_METHOD_0         0  ''
               52  STORE_FAST               'nslcd_version'

 L. 247        54  LOAD_FAST                'nslcd_version'
               56  LOAD_GLOBAL              req
               58  LOAD_ATTR                PROTO_VERSION
               60  COMPARE_OP               !=
               62  POP_JUMP_IF_FALSE    84  'to 84'

 L. 248        64  LOAD_GLOBAL              logging
               66  LOAD_METHOD              error

 L. 249        68  LOAD_STR                 'Wrong protocol version: Expected %r but got %r'

 L. 250        70  LOAD_GLOBAL              req
               72  LOAD_ATTR                PROTO_VERSION

 L. 251        74  LOAD_FAST                'nslcd_version'

 L. 248        76  CALL_METHOD_3         3  ''
               78  POP_TOP          

 L. 253        80  LOAD_CONST               None
               82  RETURN_VALUE     
             84_0  COME_FROM            62  '62'

 L. 254        84  LOAD_FAST                'tios'
               86  LOAD_METHOD              read_int32
               88  CALL_METHOD_0         0  ''
               90  STORE_FAST               'req_type'

 L. 255        92  LOAD_GLOBAL              logging
               94  LOAD_METHOD              debug
               96  LOAD_STR                 'Incoming request on %s'
               98  LOAD_FAST                'self'
              100  LOAD_ATTR                request
              102  LOAD_METHOD              getsockname
              104  CALL_METHOD_0         0  ''
              106  CALL_METHOD_2         2  ''
              108  POP_TOP          

 L. 256       110  SETUP_FINALLY       128  'to 128'

 L. 257       112  LOAD_FAST                'self'
              114  LOAD_ATTR                server
              116  LOAD_ATTR                _reqh
              118  LOAD_FAST                'req_type'
              120  BINARY_SUBSCR    
              122  STORE_FAST               'handler_class'
              124  POP_BLOCK        
              126  JUMP_FORWARD        178  'to 178'
            128_0  COME_FROM_FINALLY   110  '110'

 L. 258       128  DUP_TOP          
              130  LOAD_GLOBAL              KeyError
              132  COMPARE_OP               exception-match
              134  POP_JUMP_IF_FALSE   176  'to 176'
              136  POP_TOP          
              138  POP_TOP          
              140  POP_TOP          

 L. 259       142  LOAD_GLOBAL              logging
              144  LOAD_METHOD              error
              146  LOAD_STR                 'No handler for req_type 0x%08x'
              148  LOAD_FAST                'req_type'
              150  CALL_METHOD_2         2  ''
              152  POP_TOP          

 L. 260       154  LOAD_FAST                'self'
              156  LOAD_ATTR                server
              158  DUP_TOP          
              160  LOAD_ATTR                _invalid_requests
              162  LOAD_CONST               1
              164  INPLACE_ADD      
              166  ROT_TWO          
              168  STORE_ATTR               _invalid_requests

 L. 261       170  POP_EXCEPT       
              172  LOAD_CONST               None
              174  RETURN_VALUE     
            176_0  COME_FROM           134  '134'
              176  END_FINALLY      
            178_0  COME_FROM           126  '126'

 L. 262       178  LOAD_FAST                'self'
              180  LOAD_ATTR                server
              182  LOAD_ATTR                _req_counter
              184  LOAD_FAST                'req_type'
              186  DUP_TOP_TWO      
              188  BINARY_SUBSCR    
              190  LOAD_CONST               1
              192  INPLACE_ADD      
              194  ROT_THREE        
              196  STORE_SUBSCR     

 L. 263       198  LOAD_CONST               None
              200  STORE_FAST               'handler'

 L. 264       202  SETUP_FINALLY       272  'to 272'

 L. 265       204  LOAD_FAST                'handler_class'

 L. 266       206  LOAD_FAST                'tios'

 L. 267       208  LOAD_FAST                'self'
              210  LOAD_ATTR                server

 L. 268       212  LOAD_FAST                'self'
              214  LOAD_METHOD              _get_peer_cred
              216  CALL_METHOD_0         0  ''

 L. 265       218  CALL_FUNCTION_3       3  ''
              220  STORE_FAST               'handler'

 L. 270       222  LOAD_FAST                'handler'
              224  LOAD_METHOD              log_params
              226  LOAD_GLOBAL              logging
              228  LOAD_ATTR                DEBUG
              230  CALL_METHOD_1         1  ''
              232  POP_TOP          

 L. 271       234  LOAD_FAST                'handler'
              236  LOAD_ATTR                tios
              238  LOAD_METHOD              write_int32
              240  LOAD_GLOBAL              PROTO_VERSION
              242  CALL_METHOD_1         1  ''
              244  POP_TOP          

 L. 272       246  LOAD_FAST                'handler'
              248  LOAD_ATTR                tios
              250  LOAD_METHOD              write_int32
              252  LOAD_FAST                'handler'
              254  LOAD_ATTR                rtype
              256  CALL_METHOD_1         1  ''
              258  POP_TOP          

 L. 273       260  LOAD_FAST                'handler'
              262  LOAD_METHOD              process
              264  CALL_METHOD_0         0  ''
              266  POP_TOP          
              268  POP_BLOCK        
              270  JUMP_FORWARD        388  'to 388'
            272_0  COME_FROM_FINALLY   202  '202'

 L. 274       272  DUP_TOP          
              274  LOAD_GLOBAL              KeyboardInterrupt
              276  LOAD_GLOBAL              SystemExit
              278  BUILD_TUPLE_2         2 
              280  COMPARE_OP               exception-match
          282_284  POP_JUMP_IF_FALSE   330  'to 330'
              286  POP_TOP          
              288  STORE_FAST               'exit_err'
              290  POP_TOP          
              292  SETUP_FINALLY       318  'to 318'

 L. 275       294  LOAD_GLOBAL              logging
              296  LOAD_METHOD              debug

 L. 276       298  LOAD_STR                 'Received %s exception in %s => re-raise'

 L. 277       300  LOAD_FAST                'exit_err'

 L. 278       302  LOAD_FAST                'self'
              304  LOAD_ATTR                __class__
              306  LOAD_ATTR                __name__

 L. 275       308  CALL_METHOD_3         3  ''
              310  POP_TOP          

 L. 281       312  RAISE_VARARGS_0       0  'reraise'
              314  POP_BLOCK        
              316  BEGIN_FINALLY    
            318_0  COME_FROM_FINALLY   292  '292'
              318  LOAD_CONST               None
              320  STORE_FAST               'exit_err'
              322  DELETE_FAST              'exit_err'
              324  END_FINALLY      
              326  POP_EXCEPT       
              328  JUMP_FORWARD        388  'to 388'
            330_0  COME_FROM           282  '282'

 L. 282       330  DUP_TOP          
              332  LOAD_GLOBAL              Exception
              334  COMPARE_OP               exception-match
          336_338  POP_JUMP_IF_FALSE   386  'to 386'
              340  POP_TOP          
              342  POP_TOP          
              344  POP_TOP          

 L. 283       346  LOAD_FAST                'handler'
              348  LOAD_CONST               None
              350  COMPARE_OP               is-not
          352_354  POP_JUMP_IF_FALSE   368  'to 368'

 L. 284       356  LOAD_FAST                'handler'
              358  LOAD_METHOD              log_params
              360  LOAD_GLOBAL              logging
              362  LOAD_ATTR                ERROR
              364  CALL_METHOD_1         1  ''
              366  POP_TOP          
            368_0  COME_FROM           352  '352'

 L. 285       368  LOAD_GLOBAL              logging
              370  LOAD_ATTR                error
              372  LOAD_STR                 'Unhandled exception during processing request:'
              374  LOAD_CONST               True
              376  LOAD_CONST               ('exc_info',)
              378  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              380  POP_TOP          
              382  POP_EXCEPT       
              384  JUMP_FORWARD        388  'to 388'
            386_0  COME_FROM           336  '336'
              386  END_FINALLY      
            388_0  COME_FROM           384  '384'
            388_1  COME_FROM           328  '328'
            388_2  COME_FROM           270  '270'

 L. 286       388  LOAD_CONST               1000
              390  LOAD_GLOBAL              time
              392  LOAD_METHOD              time
              394  CALL_METHOD_0         0  ''
              396  LOAD_FAST                'start_time'
              398  BINARY_SUBTRACT  
              400  BINARY_MULTIPLY  
              402  STORE_FAST               'req_time'

 L. 287       404  LOAD_FAST                'self'
              406  LOAD_ATTR                server
              408  LOAD_ATTR                _avg_response_time
              410  LOAD_CONST               30
              412  BINARY_MULTIPLY  
              414  LOAD_FAST                'req_time'
              416  BINARY_ADD       
              418  LOAD_CONST               31
              420  BINARY_TRUE_DIVIDE
              422  LOAD_FAST                'self'
              424  LOAD_ATTR                server
              426  STORE_ATTR               _avg_response_time

 L. 288       428  LOAD_GLOBAL              max
              430  LOAD_FAST                'self'
              432  LOAD_ATTR                server
              434  LOAD_ATTR                _max_response_time
              436  LOAD_FAST                'req_time'
              438  CALL_FUNCTION_2       2  ''
              440  LOAD_FAST                'self'
              442  LOAD_ATTR                server
              444  STORE_ATTR               _max_response_time

Parse error at or near `LOAD_CONST' instruction at offset 172


class NSSPAMServer(socketserver.UnixStreamServer):
    __doc__ = '\n    the NSS/PAM socket server\n    '

    def __init__(self, server_address, bind_and_activate=True):
        socketserver.UnixStreamServer.__init__(self, server_address, TIOStreamRequestHandler, bind_and_activate)
        self._start_time = time.time()
        self._last_access_time = 0
        self._req_counter_all = 0
        self._invalid_requests = 0
        self._bytes_sent = 0
        self._bytes_received = 0
        self._avg_response_time = 0
        self._max_response_time = 0
        self._reqh = {}
        self._reqh.update(req.get_handlers('aehostd.config'))
        self._reqh.update(req.get_handlers('aehostd.group'))
        self._reqh.update(req.get_handlers('aehostd.hosts'))
        self._reqh.update(req.get_handlers('aehostd.passwd'))
        self._reqh.update(req.get_handlers('aehostd.pam'))
        self._req_counter = {}.fromkeys(self._reqh.keys(), 0)

    def get_monitor_data(self):
        """
        returns all monitoring data as
        """
        return dict(req_count=(self._req_counter_all),
          req_err=(self._invalid_requests),
          avg_response_time=(self._avg_response_time),
          max_response_time=(self._max_response_time))

    def server_bind(self):
        """Override server_bind to set socket options."""
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.settimeout(CFG.sockettimeout)
        try:
            os.unlink(self.server_address)
        except OSError:
            if os.path.exists(self.server_address):
                raise
        else:
            socketserver.UnixStreamServer.server_bind(self)
            os.chmod(self.server_address, int(CFG.socketperms, 8))
            logging.debug('%s now accepting connections on %r', self.__class__.__name__, self.server_address)