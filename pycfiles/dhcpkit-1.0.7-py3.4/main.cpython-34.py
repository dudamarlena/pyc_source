# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/dhcpkit/ipv6/server/main.py
# Compiled at: 2017-06-20 18:49:13
# Size of source mod 2**32: 20056 bytes
"""
The main server process
"""
import argparse, atexit, fcntl, json, logging.handlers, multiprocessing, multiprocessing.queues, os, pwd, selectors, signal, sys, time
from multiprocessing import forkserver
from multiprocessing.util import get_logger
from urllib.parse import urlparse
import dhcpkit
from ZConfig import ConfigurationSyntaxError, DataConversionError
from dhcpkit.common.privileges import drop_privileges, restore_privileges
from dhcpkit.common.server.logging.config_elements import set_verbosity_logger
from dhcpkit.ipv6.server import config_parser, queue_logger
from dhcpkit.ipv6.server.config_elements import MainConfig
from dhcpkit.ipv6.server.control_socket import ControlConnection, ControlSocket
from dhcpkit.ipv6.server.listeners import ClosedListener, IgnoreMessage, Listener, ListenerCreator
from dhcpkit.ipv6.server.nonblocking_pool import NonBlockingPool
from dhcpkit.ipv6.server.queue_logger import WorkerQueueHandler
from dhcpkit.ipv6.server.statistics import ServerStatistics
from dhcpkit.ipv6.server.worker import handle_message, setup_worker
from typing import Iterable, Optional
logger = logging.getLogger()
logging_thread = None

@atexit.register
def stop_logging_thread():
    """
    Stop the logging thread from the global
    """
    global logging_thread
    if logging_thread:
        logging_thread.stop()


def error_callback(exception):
    """
    Show exceptions that occur while handling messages

    :param exception: The exception that occurred
    """
    message = 'Unexpected exception while delegating handling to worker {}'.format(exception)
    if exception.__cause__:
        message += ':' + str(exception.__cause__)
    logger.error(message)


def handle_args(args: Iterable[str]):
    """
    Handle the command line arguments.

    :param args: Command line arguments
    :return: The arguments object
    """
    parser = argparse.ArgumentParser(description='A flexible IPv6 DHCP server written in Python.')
    parser.add_argument('config', help='the configuration file')
    parser.add_argument('-v', '--verbosity', action='count', default=0, help='increase output verbosity')
    parser.add_argument('-c', '--control-socket', action='store', metavar='FILENAME', help='location of domain socket for server control')
    parser.add_argument('-p', '--pidfile', action='store', help="save the server's PID to this file")
    args = parser.parse_args(args)
    return args


def create_pidfile(args, config: MainConfig) -> Optional[str]:
    """
    Create a PID file when configured to do so.

    :param args: The command line arguments
    :param config: The server configuration
    :return: The name of the created PID file
    """
    if args.pidfile:
        pid_filename = os.path.realpath(args.pidfile)
    else:
        if config.pid_file:
            pid_filename = os.path.realpath(config.pid_file)
        else:
            pid_filename = None
    if pid_filename:
        old_umask = os.umask(18)
        try:
            os.unlink(pid_filename)
        except OSError:
            pass

        with open(pid_filename, 'w') as (pidfile):
            logger.info('Writing PID-file {}'.format(pid_filename))
            pidfile.write('{}\n'.format(os.getpid()))
        os.umask(old_umask)
    return pid_filename


def create_control_socket(args, config: MainConfig) -> ControlSocket:
    """
    Create a control socket when configured to do so.

    :param args: The command line arguments
    :param config: The server configuration
    :return: The name of the created control socket
    """
    if args.control_socket:
        socket_filename = os.path.realpath(args.control_socket)
    else:
        if config.control_socket:
            socket_filename = os.path.realpath(config.control_socket)
        else:
            socket_filename = None
    if socket_filename:
        control_socket_user = config.control_socket_user if config.control_socket_user else pwd.getpwuid(os.getuid())
        uid = control_socket_user.pw_uid
        gid = config.control_socket_group.gr_gid if config.control_socket_group else control_socket_user.pw_gid
        old_umask = os.umask(79)
        control_socket = ControlSocket(socket_filename)
        if uid != os.geteuid() or gid != os.getegid():
            os.chown(socket_filename, uid, gid)
        os.umask(old_umask)
        return control_socket


def main--- This code section failed: ---

 L. 161         0  LOAD_GLOBAL              handle_args
                3  LOAD_FAST                'args'
                6  CALL_FUNCTION_1       1  '1 positional, 0 named'
                9  STORE_FAST               'args'

 L. 162        12  LOAD_GLOBAL              set_verbosity_logger
               15  LOAD_GLOBAL              logger
               18  LOAD_FAST                'args'
               21  LOAD_ATTR                verbosity
               24  CALL_FUNCTION_2       2  '2 positional, 0 named'
               27  POP_TOP          

 L. 165        28  LOAD_GLOBAL              os
               31  LOAD_ATTR                path
               34  LOAD_ATTR                realpath
               37  LOAD_FAST                'args'
               40  LOAD_ATTR                config
               43  CALL_FUNCTION_1       1  '1 positional, 0 named'
               46  STORE_FAST               'config_file'

 L. 166        49  LOAD_GLOBAL              os
               52  LOAD_ATTR                chdir
               55  LOAD_GLOBAL              os
               58  LOAD_ATTR                path
               61  LOAD_ATTR                dirname
               64  LOAD_FAST                'config_file'
               67  CALL_FUNCTION_1       1  '1 positional, 0 named'
               70  CALL_FUNCTION_1       1  '1 positional, 0 named'
               73  POP_TOP          

 L. 168        74  SETUP_EXCEPT         96  'to 96'

 L. 170        77  LOAD_GLOBAL              config_parser
               80  LOAD_ATTR                load_config
               83  LOAD_FAST                'config_file'
               86  CALL_FUNCTION_1       1  '1 positional, 0 named'
               89  STORE_FAST               'config'
               92  POP_BLOCK        
               93  JUMP_FORWARD        316  'to 316'
             96_0  COME_FROM_EXCEPT     74  '74'

 L. 171        96  DUP_TOP          
               97  LOAD_GLOBAL              ConfigurationSyntaxError
              100  LOAD_GLOBAL              DataConversionError
              103  BUILD_TUPLE_2         2 
              106  COMPARE_OP               exception-match
              109  POP_JUMP_IF_FALSE   262  'to 262'
              112  POP_TOP          
              113  STORE_FAST               'e'
              116  POP_TOP          
              117  SETUP_FINALLY       249  'to 249'

 L. 173       120  LOAD_FAST                'e'
              123  LOAD_ATTR                message
              126  STORE_FAST               'msg'

 L. 174       129  LOAD_FAST                'e'
              132  LOAD_ATTR                lineno
              135  POP_JUMP_IF_FALSE   178  'to 178'
              138  LOAD_FAST                'e'
              141  LOAD_ATTR                lineno
              144  LOAD_CONST               -1
              147  COMPARE_OP               !=
              150  POP_JUMP_IF_FALSE   178  'to 178'

 L. 175       153  LOAD_FAST                'msg'
              156  LOAD_STR                 ' on line {}'
              159  LOAD_ATTR                format
              162  LOAD_FAST                'e'
              165  LOAD_ATTR                lineno
              168  CALL_FUNCTION_1       1  '1 positional, 0 named'
              171  INPLACE_ADD      
              172  STORE_FAST               'msg'
            175_0  COME_FROM           150  '150'
              175  JUMP_FORWARD        178  'to 178'
            178_0  COME_FROM           175  '175'

 L. 176       178  LOAD_FAST                'e'
              181  LOAD_ATTR                url
              184  POP_JUMP_IF_FALSE   227  'to 227'

 L. 177       187  LOAD_GLOBAL              urlparse
              190  LOAD_FAST                'e'
              193  LOAD_ATTR                url
              196  CALL_FUNCTION_1       1  '1 positional, 0 named'
              199  STORE_FAST               'parts'

 L. 178       202  LOAD_FAST                'msg'
              205  LOAD_STR                 ' in {}'
              208  LOAD_ATTR                format
              211  LOAD_FAST                'parts'
              214  LOAD_ATTR                path
              217  CALL_FUNCTION_1       1  '1 positional, 0 named'
              220  INPLACE_ADD      
              221  STORE_FAST               'msg'
              224  JUMP_FORWARD        227  'to 227'
            227_0  COME_FROM           224  '224'

 L. 179       227  LOAD_GLOBAL              logger
              230  LOAD_ATTR                critical
              233  LOAD_FAST                'msg'
              236  CALL_FUNCTION_1       1  '1 positional, 0 named'
              239  POP_TOP          

 L. 180       240  LOAD_CONST               1
              243  RETURN_VALUE     
              244  POP_BLOCK        
              245  POP_EXCEPT       
              246  LOAD_CONST               None
            249_0  COME_FROM_FINALLY   117  '117'
              249  LOAD_CONST               None
              252  STORE_FAST               'e'
              255  DELETE_FAST              'e'
              258  END_FINALLY      
              259  JUMP_FORWARD        316  'to 316'

 L. 181       262  DUP_TOP          
              263  LOAD_GLOBAL              ValueError
              266  COMPARE_OP               exception-match
              269  POP_JUMP_IF_FALSE   315  'to 315'
              272  POP_TOP          
              273  STORE_FAST               'e'
              276  POP_TOP          
              277  SETUP_FINALLY       302  'to 302'

 L. 182       280  LOAD_GLOBAL              logger
              283  LOAD_ATTR                critical
              286  LOAD_FAST                'e'
              289  CALL_FUNCTION_1       1  '1 positional, 0 named'
              292  POP_TOP          

 L. 183       293  LOAD_CONST               1
              296  RETURN_VALUE     
              297  POP_BLOCK        
              298  POP_EXCEPT       
              299  LOAD_CONST               None
            302_0  COME_FROM_FINALLY   277  '277'
              302  LOAD_CONST               None
              305  STORE_FAST               'e'
              308  DELETE_FAST              'e'
              311  END_FINALLY      
              312  JUMP_FORWARD        316  'to 316'
              315  END_FINALLY      
            316_0  COME_FROM           312  '312'
            316_1  COME_FROM           259  '259'
            316_2  COME_FROM            93  '93'

 L. 186       316  LOAD_GLOBAL              drop_privileges
              319  LOAD_FAST                'config'
              322  LOAD_ATTR                user
              325  LOAD_FAST                'config'
              328  LOAD_ATTR                group
              331  LOAD_STR                 'permanent'
              334  LOAD_CONST               False
              337  CALL_FUNCTION_258   258  '2 positional, 1 named'
              340  POP_TOP          

 L. 189       341  LOAD_GLOBAL              signal
              344  LOAD_ATTR                signal
              347  LOAD_GLOBAL              signal
              350  LOAD_ATTR                SIGINT
              353  LOAD_GLOBAL              signal
              356  LOAD_ATTR                SIG_IGN
              359  CALL_FUNCTION_2       2  '2 positional, 0 named'
              362  POP_TOP          

 L. 190       363  LOAD_GLOBAL              multiprocessing
              366  LOAD_ATTR                set_start_method
              369  LOAD_STR                 'forkserver'
              372  CALL_FUNCTION_1       1  '1 positional, 0 named'
              375  POP_TOP          

 L. 191       376  LOAD_GLOBAL              forkserver
              379  LOAD_ATTR                ensure_running
              382  CALL_FUNCTION_0       0  '0 positional, 0 named'
              385  POP_TOP          

 L. 194       386  LOAD_FAST                'config'
              389  LOAD_ATTR                logging
              392  LOAD_ATTR                configure
              395  LOAD_GLOBAL              logger
              398  LOAD_STR                 'verbosity'
              401  LOAD_FAST                'args'
              404  LOAD_ATTR                verbosity
              407  CALL_FUNCTION_257   257  '1 positional, 1 named'
              410  POP_TOP          

 L. 195       411  LOAD_GLOBAL              logger
              414  LOAD_ATTR                info
              417  LOAD_STR                 'Starting Python DHCPv6 server v{}'
              420  LOAD_ATTR                format
              423  LOAD_GLOBAL              dhcpkit
              426  LOAD_ATTR                __version__
              429  CALL_FUNCTION_1       1  '1 positional, 0 named'
              432  CALL_FUNCTION_1       1  '1 positional, 0 named'
              435  POP_TOP          

 L. 198       436  LOAD_GLOBAL              selectors
              439  LOAD_ATTR                DefaultSelector
              442  CALL_FUNCTION_0       0  '0 positional, 0 named'
              445  STORE_FAST               'sel'

 L. 201       448  LOAD_GLOBAL              os
              451  LOAD_ATTR                pipe
              454  CALL_FUNCTION_0       0  '0 positional, 0 named'
              457  UNPACK_SEQUENCE_2     2 
              460  STORE_FAST               'signal_r'
              463  STORE_FAST               'signal_w'

 L. 202       466  LOAD_GLOBAL              fcntl
              469  LOAD_ATTR                fcntl
              472  LOAD_FAST                'signal_w'
              475  LOAD_GLOBAL              fcntl
              478  LOAD_ATTR                F_GETFL
              481  LOAD_CONST               0
              484  CALL_FUNCTION_3       3  '3 positional, 0 named'
              487  STORE_FAST               'flags'

 L. 203       490  LOAD_FAST                'flags'
              493  LOAD_GLOBAL              os
              496  LOAD_ATTR                O_NONBLOCK
              499  BINARY_OR        
              500  STORE_FAST               'flags'

 L. 204       503  LOAD_GLOBAL              fcntl
              506  LOAD_ATTR                fcntl
              509  LOAD_FAST                'signal_w'
              512  LOAD_GLOBAL              fcntl
              515  LOAD_ATTR                F_SETFL
              518  LOAD_FAST                'flags'
              521  CALL_FUNCTION_3       3  '3 positional, 0 named'
              524  POP_TOP          

 L. 205       525  LOAD_GLOBAL              signal
              528  LOAD_ATTR                set_wakeup_fd
              531  LOAD_FAST                'signal_w'
              534  CALL_FUNCTION_1       1  '1 positional, 0 named'
              537  POP_TOP          

 L. 206       538  LOAD_FAST                'sel'
              541  LOAD_ATTR                register
              544  LOAD_FAST                'signal_r'
              547  LOAD_GLOBAL              selectors
              550  LOAD_ATTR                EVENT_READ
              553  CALL_FUNCTION_2       2  '2 positional, 0 named'
              556  POP_TOP          

 L. 209       557  LOAD_GLOBAL              signal
              560  LOAD_ATTR                signal
              563  LOAD_GLOBAL              signal
              566  LOAD_ATTR                SIGINT
              569  LOAD_LAMBDA              '<code_object <lambda>>'
              572  LOAD_STR                 'main.<locals>.<lambda>'
              575  MAKE_FUNCTION_0          '0 positional, 0 keyword only, 0 annotated'
              578  CALL_FUNCTION_2       2  '2 positional, 0 named'
              581  POP_TOP          

 L. 210       582  LOAD_GLOBAL              signal
              585  LOAD_ATTR                signal
              588  LOAD_GLOBAL              signal
              591  LOAD_ATTR                SIGTERM
              594  LOAD_LAMBDA              '<code_object <lambda>>'
              597  LOAD_STR                 'main.<locals>.<lambda>'
              600  MAKE_FUNCTION_0          '0 positional, 0 keyword only, 0 annotated'
              603  CALL_FUNCTION_2       2  '2 positional, 0 named'
              606  POP_TOP          

 L. 211       607  LOAD_GLOBAL              signal
              610  LOAD_ATTR                signal
              613  LOAD_GLOBAL              signal
              616  LOAD_ATTR                SIGHUP
              619  LOAD_LAMBDA              '<code_object <lambda>>'
              622  LOAD_STR                 'main.<locals>.<lambda>'
              625  MAKE_FUNCTION_0          '0 positional, 0 keyword only, 0 annotated'
              628  CALL_FUNCTION_2       2  '2 positional, 0 named'
              631  POP_TOP          

 L. 212       632  LOAD_GLOBAL              signal
              635  LOAD_ATTR                signal
              638  LOAD_GLOBAL              signal
              641  LOAD_ATTR                SIGUSR1
              644  LOAD_LAMBDA              '<code_object <lambda>>'
              647  LOAD_STR                 'main.<locals>.<lambda>'
              650  MAKE_FUNCTION_0          '0 positional, 0 keyword only, 0 annotated'
              653  CALL_FUNCTION_2       2  '2 positional, 0 named'
              656  POP_TOP          

 L. 215       657  BUILD_LIST_0          0 
              660  STORE_FAST               'exception_history'

 L. 218       663  LOAD_CONST               0
              666  STORE_FAST               'message_count'

 L. 221       669  LOAD_GLOBAL              multiprocessing
              672  LOAD_ATTR                Queue
              675  CALL_FUNCTION_0       0  '0 positional, 0 named'
              678  STORE_FAST               'logging_queue'

 L. 223       681  LOAD_GLOBAL              ServerStatistics
              684  CALL_FUNCTION_0       0  '0 positional, 0 named'
              687  STORE_FAST               'statistics'

 L. 224       690  BUILD_LIST_0          0 
              693  STORE_FAST               'listeners'

 L. 225       696  LOAD_CONST               None
              699  STORE_FAST               'control_socket'

 L. 226       702  LOAD_CONST               False
              705  STORE_FAST               'stopping'

 L. 228       708  SETUP_LOOP         3220  'to 3220'
              711  LOAD_FAST                'stopping'
              714  POP_JUMP_IF_TRUE   3219  'to 3219'

 L. 230       717  LOAD_CONST               True
              720  STORE_FAST               'stopping'

 L. 233       723  LOAD_FAST                'config'
              726  LOAD_ATTR                logging
              729  LOAD_ATTR                configure
              732  LOAD_GLOBAL              logger
              735  LOAD_STR                 'verbosity'
              738  LOAD_FAST                'args'
              741  LOAD_ATTR                verbosity
              744  CALL_FUNCTION_257   257  '1 positional, 1 named'
              747  STORE_FAST               'lowest_log_level'

 L. 236       750  LOAD_GLOBAL              get_logger
              753  CALL_FUNCTION_0       0  '0 positional, 0 named'
              756  STORE_FAST               'mp_logger'

 L. 237       759  LOAD_FAST                'config'
              762  LOAD_ATTR                logging
              765  LOAD_ATTR                log_multiprocessing
              768  LOAD_FAST                'mp_logger'
              771  STORE_ATTR               propagate

 L. 240       774  LOAD_GLOBAL              logging_thread
              777  POP_JUMP_IF_FALSE   793  'to 793'

 L. 241       780  LOAD_GLOBAL              logging_thread
              783  LOAD_ATTR                stop
              786  CALL_FUNCTION_0       0  '0 positional, 0 named'
              789  POP_TOP          
              790  JUMP_FORWARD        793  'to 793'
            793_0  COME_FROM           790  '790'

 L. 243       793  LOAD_GLOBAL              queue_logger
              796  LOAD_ATTR                QueueLevelListener
              799  LOAD_FAST                'logging_queue'
              802  LOAD_GLOBAL              logger
              805  LOAD_ATTR                handlers
              808  CALL_FUNCTION_VAR_1     1  '1 positional, 0 named'
              811  STORE_GLOBAL             logging_thread

 L. 244       814  LOAD_GLOBAL              logging_thread
              817  LOAD_ATTR                start
              820  CALL_FUNCTION_0       0  '0 positional, 0 named'
              823  POP_TOP          

 L. 247       824  LOAD_GLOBAL              WorkerQueueHandler
              827  LOAD_FAST                'logging_queue'
              830  CALL_FUNCTION_1       1  '1 positional, 0 named'
              833  STORE_FAST               'logging_handler'

 L. 248       836  LOAD_FAST                'logging_handler'
              839  LOAD_ATTR                setLevel
              842  LOAD_FAST                'lowest_log_level'
              845  CALL_FUNCTION_1       1  '1 positional, 0 named'
              848  POP_TOP          

 L. 249       849  LOAD_FAST                'logging_handler'
              852  BUILD_LIST_1          1 
              855  LOAD_GLOBAL              logger
              858  STORE_ATTR               handlers

 L. 252       861  LOAD_GLOBAL              restore_privileges
              864  CALL_FUNCTION_0       0  '0 positional, 0 named'
              867  POP_TOP          

 L. 255       868  LOAD_FAST                'listeners'
              871  STORE_FAST               'old_listeners'

 L. 256       874  BUILD_LIST_0          0 
              877  STORE_FAST               'listeners'

 L. 257       880  SETUP_LOOP          923  'to 923'
              883  LOAD_FAST                'config'
              886  LOAD_ATTR                listener_factories
              889  GET_ITER         
              890  FOR_ITER            922  'to 922'
              893  STORE_FAST               'listener_factory'

 L. 259       896  LOAD_FAST                'listeners'
              899  LOAD_ATTR                append
              902  LOAD_FAST                'listener_factory'
              905  LOAD_FAST                'old_listeners'
              908  LOAD_FAST                'listeners'
              911  BINARY_ADD       
              912  CALL_FUNCTION_1       1  '1 positional, 0 named'
              915  CALL_FUNCTION_1       1  '1 positional, 0 named'
              918  POP_TOP          
              919  JUMP_BACK           890  'to 890'
              922  POP_BLOCK        
            923_0  COME_FROM_LOOP      880  '880'

 L. 262       923  DELETE_FAST              'old_listeners'

 L. 265       926  LOAD_GLOBAL              create_pidfile
              929  LOAD_STR                 'args'
              932  LOAD_FAST                'args'
              935  LOAD_STR                 'config'
              938  LOAD_FAST                'config'
              941  CALL_FUNCTION_512   512  '0 positional, 2 named'
              944  STORE_FAST               'pid_filename'

 L. 268       947  LOAD_FAST                'control_socket'
              950  POP_JUMP_IF_FALSE   979  'to 979'

 L. 269       953  LOAD_FAST                'sel'
              956  LOAD_ATTR                unregister
              959  LOAD_FAST                'control_socket'
              962  CALL_FUNCTION_1       1  '1 positional, 0 named'
              965  POP_TOP          

 L. 270       966  LOAD_FAST                'control_socket'
              969  LOAD_ATTR                close
              972  CALL_FUNCTION_0       0  '0 positional, 0 named'
              975  POP_TOP          
              976  JUMP_FORWARD        979  'to 979'
            979_0  COME_FROM           976  '976'

 L. 272       979  LOAD_GLOBAL              create_control_socket
              982  LOAD_STR                 'args'
              985  LOAD_FAST                'args'
              988  LOAD_STR                 'config'
              991  LOAD_FAST                'config'
              994  CALL_FUNCTION_512   512  '0 positional, 2 named'
              997  STORE_FAST               'control_socket'

 L. 273      1000  LOAD_FAST                'control_socket'
             1003  POP_JUMP_IF_FALSE  1028  'to 1028'

 L. 274      1006  LOAD_FAST                'sel'
             1009  LOAD_ATTR                register
             1012  LOAD_FAST                'control_socket'
             1015  LOAD_GLOBAL              selectors
             1018  LOAD_ATTR                EVENT_READ
             1021  CALL_FUNCTION_2       2  '2 positional, 0 named'
             1024  POP_TOP          
             1025  JUMP_FORWARD       1028  'to 1028'
           1028_0  COME_FROM          1025  '1025'

 L. 277      1028  LOAD_GLOBAL              drop_privileges
             1031  LOAD_FAST                'config'
             1034  LOAD_ATTR                user
             1037  LOAD_FAST                'config'
             1040  LOAD_ATTR                group
             1043  LOAD_STR                 'permanent'
             1046  LOAD_CONST               False
             1049  CALL_FUNCTION_258   258  '2 positional, 1 named'
             1052  POP_TOP          

 L. 280      1053  SETUP_LOOP         1185  'to 1185'
             1056  LOAD_GLOBAL              list
             1059  LOAD_FAST                'sel'
             1062  LOAD_ATTR                get_map
             1065  CALL_FUNCTION_0       0  '0 positional, 0 named'
             1068  LOAD_ATTR                items
             1071  CALL_FUNCTION_0       0  '0 positional, 0 named'
             1074  CALL_FUNCTION_1       1  '1 positional, 0 named'
             1077  GET_ITER         
             1078  FOR_ITER           1184  'to 1184'
             1081  UNPACK_SEQUENCE_2     2 
             1084  STORE_FAST               'fd'
             1087  STORE_FAST               'key'

 L. 282      1090  LOAD_FAST                'key'
             1093  LOAD_ATTR                fileobj
             1096  LOAD_FAST                'signal_r'
             1099  COMPARE_OP               is
             1102  POP_JUMP_IF_TRUE   1078  'to 1078'

 L. 283      1105  LOAD_FAST                'control_socket'
             1108  POP_JUMP_IF_FALSE  1126  'to 1126'
             1111  LOAD_FAST                'key'
             1114  LOAD_ATTR                fileobj
             1117  LOAD_FAST                'control_socket'
             1120  COMPARE_OP               is
           1123_0  COME_FROM          1108  '1108'
             1123  POP_JUMP_IF_TRUE   1078  'to 1078'

 L. 284      1126  LOAD_FAST                'key'
             1129  LOAD_ATTR                fileobj
             1132  LOAD_FAST                'listeners'
             1135  COMPARE_OP               in
             1138  POP_JUMP_IF_TRUE   1078  'to 1078'

 L. 285      1141  LOAD_GLOBAL              isinstance
             1144  LOAD_FAST                'key'
             1147  LOAD_ATTR                fileobj
             1150  LOAD_GLOBAL              ControlConnection
             1153  CALL_FUNCTION_2       2  '2 positional, 0 named'
             1156  POP_JUMP_IF_FALSE  1165  'to 1165'

 L. 286      1159  CONTINUE           1078  'to 1078'
             1162  JUMP_FORWARD       1165  'to 1165'
           1165_0  COME_FROM          1162  '1162'

 L. 289      1165  LOAD_FAST                'sel'
             1168  LOAD_ATTR                unregister
             1171  LOAD_FAST                'key'
             1174  LOAD_ATTR                fileobj
             1177  CALL_FUNCTION_1       1  '1 positional, 0 named'
             1180  POP_TOP          
           1181_0  COME_FROM          1138  '1138'
           1181_1  COME_FROM          1123  '1123'
           1181_2  COME_FROM          1102  '1102'
             1181  JUMP_BACK          1078  'to 1078'
             1184  POP_BLOCK        
           1185_0  COME_FROM_LOOP     1053  '1053'

 L. 292      1185  LOAD_LISTCOMP            '<code_object <listcomp>>'
             1188  LOAD_STR                 'main.<locals>.<listcomp>'
             1191  MAKE_FUNCTION_0          '0 positional, 0 keyword only, 0 annotated'
             1194  LOAD_FAST                'sel'
             1197  LOAD_ATTR                get_map
             1200  CALL_FUNCTION_0       0  '0 positional, 0 named'
             1203  LOAD_ATTR                values
             1206  CALL_FUNCTION_0       0  '0 positional, 0 named'
             1209  GET_ITER         
             1210  CALL_FUNCTION_1       1  '1 positional, 0 named'
             1213  STORE_FAST               'existing_listeners'

 L. 293      1216  SETUP_LOOP         1267  'to 1267'
             1219  LOAD_FAST                'listeners'
             1222  GET_ITER         
             1223  FOR_ITER           1266  'to 1266'
             1226  STORE_FAST               'listener'

 L. 294      1229  LOAD_FAST                'listener'
             1232  LOAD_FAST                'existing_listeners'
             1235  COMPARE_OP               not-in
             1238  POP_JUMP_IF_FALSE  1223  'to 1223'

 L. 295      1241  LOAD_FAST                'sel'
             1244  LOAD_ATTR                register
             1247  LOAD_FAST                'listener'
             1250  LOAD_GLOBAL              selectors
             1253  LOAD_ATTR                EVENT_READ
             1256  CALL_FUNCTION_2       2  '2 positional, 0 named'
             1259  POP_TOP          
             1260  CONTINUE           1223  'to 1223'
             1263  JUMP_BACK          1223  'to 1223'
             1266  POP_BLOCK        
           1267_0  COME_FROM_LOOP     1216  '1216'

 L. 298      1267  SETUP_EXCEPT       1286  'to 1286'

 L. 299      1270  LOAD_FAST                'config'
             1273  LOAD_ATTR                create_message_handler
             1276  CALL_FUNCTION_0       0  '0 positional, 0 named'
             1279  STORE_FAST               'message_handler'
             1282  POP_BLOCK        
             1283  JUMP_FORWARD       1380  'to 1380'
           1286_0  COME_FROM_EXCEPT   1267  '1267'

 L. 300      1286  DUP_TOP          
             1287  LOAD_GLOBAL              Exception
             1290  COMPARE_OP               exception-match
             1293  POP_JUMP_IF_FALSE  1379  'to 1379'
             1296  POP_TOP          
             1297  STORE_FAST               'e'
             1300  POP_TOP          
             1301  SETUP_FINALLY      1366  'to 1366'

 L. 301      1304  LOAD_FAST                'args'
             1307  LOAD_ATTR                verbosity
             1310  LOAD_CONST               3
             1313  COMPARE_OP               >=
             1316  POP_JUMP_IF_FALSE  1335  'to 1335'

 L. 302      1319  LOAD_GLOBAL              logger
             1322  LOAD_ATTR                exception
             1325  LOAD_STR                 'Error initialising DHCPv6 server'
             1328  CALL_FUNCTION_1       1  '1 positional, 0 named'
             1331  POP_TOP          
             1332  JUMP_FORWARD       1357  'to 1357'
             1335  ELSE                     '1357'

 L. 304      1335  LOAD_GLOBAL              logger
             1338  LOAD_ATTR                critical
             1341  LOAD_STR                 'Error initialising DHCPv6 server: {}'
             1344  LOAD_ATTR                format
             1347  LOAD_FAST                'e'
             1350  CALL_FUNCTION_1       1  '1 positional, 0 named'
             1353  CALL_FUNCTION_1       1  '1 positional, 0 named'
             1356  POP_TOP          
           1357_0  COME_FROM          1332  '1332'

 L. 305      1357  LOAD_CONST               1
             1360  RETURN_VALUE     
             1361  POP_BLOCK        
             1362  POP_EXCEPT       
             1363  LOAD_CONST               None
           1366_0  COME_FROM_FINALLY  1301  '1301'
             1366  LOAD_CONST               None
             1369  STORE_FAST               'e'
             1372  DELETE_FAST              'e'
             1375  END_FINALLY      
             1376  JUMP_FORWARD       1380  'to 1380'
             1379  END_FINALLY      
           1380_0  COME_FROM          1376  '1376'
           1380_1  COME_FROM          1283  '1283'

 L. 308      1380  LOAD_FAST                'statistics'
             1383  LOAD_ATTR                set_categories
             1386  LOAD_FAST                'config'
             1389  LOAD_ATTR                statistics
             1392  CALL_FUNCTION_1       1  '1 positional, 0 named'
             1395  POP_TOP          

 L. 311      1396  LOAD_GLOBAL              os
             1399  LOAD_ATTR                getpid
             1402  CALL_FUNCTION_0       0  '0 positional, 0 named'
             1405  STORE_FAST               'my_pid'

 L. 312      1408  LOAD_GLOBAL              NonBlockingPool
             1411  LOAD_STR                 'processes'
             1414  LOAD_FAST                'config'
             1417  LOAD_ATTR                workers
             1420  LOAD_STR                 'initializer'

 L. 313      1423  LOAD_GLOBAL              setup_worker
             1426  LOAD_STR                 'initargs'

 L. 314      1429  LOAD_FAST                'message_handler'
             1432  LOAD_FAST                'logging_queue'
             1435  LOAD_FAST                'lowest_log_level'
             1438  LOAD_FAST                'statistics'
             1441  LOAD_FAST                'my_pid'
             1444  BUILD_TUPLE_5         5 
             1447  CALL_FUNCTION_768   768  '0 positional, 3 named'
             1450  SETUP_WITH         3063  'to 3063'
             1453  STORE_FAST               'pool'

 L. 316      1456  LOAD_GLOBAL              logger
             1459  LOAD_ATTR                info
             1462  LOAD_STR                 'Python DHCPv6 server is ready to handle requests'
             1465  CALL_FUNCTION_1       1  '1 positional, 0 named'
             1468  POP_TOP          

 L. 318      1469  LOAD_CONST               True
             1472  STORE_FAST               'running'

 L. 319      1475  SETUP_LOOP         3039  'to 3039'
             1478  LOAD_FAST                'running'
             1481  POP_JUMP_IF_FALSE  3038  'to 3038'

 L. 320      1484  LOAD_CONST               False
             1487  STORE_FAST               'count_exception'

 L. 323      1490  SETUP_EXCEPT       2814  'to 2814'

 L. 324      1493  LOAD_FAST                'sel'
             1496  LOAD_ATTR                select
             1499  CALL_FUNCTION_0       0  '0 positional, 0 named'
             1502  STORE_FAST               'events'

 L. 325      1505  SETUP_LOOP         2810  'to 2810'
             1508  LOAD_FAST                'events'
             1511  GET_ITER         
             1512  FOR_ITER           2809  'to 2809'
             1515  UNPACK_SEQUENCE_2     2 
             1518  STORE_FAST               'key'
             1521  STORE_FAST               'mask'

 L. 326      1524  LOAD_GLOBAL              isinstance
             1527  LOAD_FAST                'key'
             1530  LOAD_ATTR                fileobj
             1533  LOAD_GLOBAL              Listener
             1536  CALL_FUNCTION_2       2  '2 positional, 0 named'
             1539  POP_JUMP_IF_FALSE  1681  'to 1681'

 L. 327      1542  SETUP_EXCEPT       1611  'to 1611'

 L. 328      1545  LOAD_FAST                'key'
             1548  LOAD_ATTR                fileobj
             1551  LOAD_ATTR                recv_request
             1554  CALL_FUNCTION_0       0  '0 positional, 0 named'
             1557  UNPACK_SEQUENCE_2     2 
             1560  STORE_FAST               'packet'
             1563  STORE_FAST               'replier'

 L. 331      1566  LOAD_FAST                'message_count'
             1569  LOAD_CONST               1
             1572  INPLACE_ADD      
             1573  STORE_FAST               'message_count'

 L. 334      1576  LOAD_FAST                'pool'
             1579  LOAD_ATTR                apply_async
             1582  LOAD_GLOBAL              handle_message
             1585  LOAD_STR                 'args'
             1588  LOAD_FAST                'packet'
             1591  LOAD_FAST                'replier'
             1594  BUILD_TUPLE_2         2 
             1597  LOAD_STR                 'error_callback'
             1600  LOAD_GLOBAL              error_callback
             1603  CALL_FUNCTION_513   513  '1 positional, 2 named'
             1606  POP_TOP          
             1607  POP_BLOCK        
             1608  JUMP_ABSOLUTE      2806  'to 2806'
           1611_0  COME_FROM_EXCEPT   1542  '1542'

 L. 335      1611  DUP_TOP          
             1612  LOAD_GLOBAL              IgnoreMessage
             1615  COMPARE_OP               exception-match
             1618  POP_JUMP_IF_FALSE  1628  'to 1628'
             1621  POP_TOP          
             1622  POP_TOP          
             1623  POP_TOP          

 L. 337      1624  POP_EXCEPT       
             1625  JUMP_ABSOLUTE      2806  'to 2806'

 L. 338      1628  DUP_TOP          
             1629  LOAD_GLOBAL              ClosedListener
             1632  COMPARE_OP               exception-match
             1635  POP_JUMP_IF_FALSE  1677  'to 1677'
             1638  POP_TOP          
             1639  POP_TOP          
             1640  POP_TOP          

 L. 340      1641  LOAD_FAST                'sel'
             1644  LOAD_ATTR                unregister
             1647  LOAD_FAST                'key'
             1650  LOAD_ATTR                fileobj
             1653  CALL_FUNCTION_1       1  '1 positional, 0 named'
             1656  POP_TOP          

 L. 341      1657  LOAD_FAST                'listeners'
             1660  LOAD_ATTR                remove
             1663  LOAD_FAST                'key'
             1666  LOAD_ATTR                fileobj
             1669  CALL_FUNCTION_1       1  '1 positional, 0 named'
             1672  POP_TOP          
             1673  POP_EXCEPT       
             1674  JUMP_ABSOLUTE      2806  'to 2806'
             1677  END_FINALLY      
             1678  JUMP_BACK          1512  'to 1512'

 L. 343      1681  LOAD_GLOBAL              isinstance
             1684  LOAD_FAST                'key'
             1687  LOAD_ATTR                fileobj
             1690  LOAD_GLOBAL              ListenerCreator
             1693  CALL_FUNCTION_2       2  '2 positional, 0 named'
             1696  POP_JUMP_IF_FALSE  1758  'to 1758'

 L. 345      1699  LOAD_FAST                'key'
             1702  LOAD_ATTR                fileobj
             1705  LOAD_ATTR                create_listener
             1708  CALL_FUNCTION_0       0  '0 positional, 0 named'
             1711  STORE_FAST               'new_listener'

 L. 346      1714  LOAD_FAST                'new_listener'
             1717  POP_JUMP_IF_FALSE  2806  'to 2806'

 L. 347      1720  LOAD_FAST                'sel'
             1723  LOAD_ATTR                register
             1726  LOAD_FAST                'new_listener'
             1729  LOAD_GLOBAL              selectors
             1732  LOAD_ATTR                EVENT_READ
             1735  CALL_FUNCTION_2       2  '2 positional, 0 named'
             1738  POP_TOP          

 L. 348      1739  LOAD_FAST                'listeners'
             1742  LOAD_ATTR                append
             1745  LOAD_FAST                'new_listener'
             1748  CALL_FUNCTION_1       1  '1 positional, 0 named'
             1751  POP_TOP          
             1752  JUMP_ABSOLUTE      2806  'to 2806'
             1755  JUMP_BACK          1512  'to 1512'

 L. 351      1758  LOAD_FAST                'key'
             1761  LOAD_ATTR                fileobj
             1764  LOAD_FAST                'signal_r'
             1767  COMPARE_OP               ==
             1770  POP_JUMP_IF_FALSE  2195  'to 2195'

 L. 352      1773  LOAD_GLOBAL              os
             1776  LOAD_ATTR                read
             1779  LOAD_FAST                'signal_r'
             1782  LOAD_CONST               1
             1785  CALL_FUNCTION_2       2  '2 positional, 0 named'
             1788  STORE_FAST               'signal_nr'

 L. 353      1791  LOAD_FAST                'signal_nr'
             1794  LOAD_CONST               0
             1797  BINARY_SUBSCR    
             1798  LOAD_GLOBAL              signal
             1801  LOAD_ATTR                SIGHUP
             1804  BUILD_TUPLE_1         1 
             1807  COMPARE_OP               in
             1810  POP_JUMP_IF_FALSE  2104  'to 2104'

 L. 355      1813  SETUP_EXCEPT       1835  'to 1835'

 L. 357      1816  LOAD_GLOBAL              config_parser
             1819  LOAD_ATTR                load_config
             1822  LOAD_FAST                'config_file'
             1825  CALL_FUNCTION_1       1  '1 positional, 0 named'
             1828  STORE_FAST               'config'
             1831  POP_BLOCK        
             1832  JUMP_FORWARD       2073  'to 2073'
           1835_0  COME_FROM_EXCEPT   1813  '1813'

 L. 358      1835  DUP_TOP          
             1836  LOAD_GLOBAL              ConfigurationSyntaxError
             1839  LOAD_GLOBAL              DataConversionError
             1842  BUILD_TUPLE_2         2 
             1845  COMPARE_OP               exception-match
             1848  POP_JUMP_IF_FALSE  2010  'to 2010'
             1851  POP_TOP          
             1852  STORE_FAST               'e'
             1855  POP_TOP          
             1856  SETUP_FINALLY      1997  'to 1997'

 L. 360      1859  LOAD_STR                 'Not reloading: '
             1862  LOAD_GLOBAL              str
             1865  LOAD_FAST                'e'
             1868  LOAD_ATTR                message
             1871  CALL_FUNCTION_1       1  '1 positional, 0 named'
             1874  BINARY_ADD       
             1875  STORE_FAST               'msg'

 L. 361      1878  LOAD_FAST                'e'
             1881  LOAD_ATTR                lineno
             1884  POP_JUMP_IF_FALSE  1927  'to 1927'
             1887  LOAD_FAST                'e'
             1890  LOAD_ATTR                lineno
             1893  LOAD_CONST               -1
             1896  COMPARE_OP               !=
             1899  POP_JUMP_IF_FALSE  1927  'to 1927'

 L. 362      1902  LOAD_FAST                'msg'
             1905  LOAD_STR                 ' on line {}'
             1908  LOAD_ATTR                format
             1911  LOAD_FAST                'e'
             1914  LOAD_ATTR                lineno
             1917  CALL_FUNCTION_1       1  '1 positional, 0 named'
             1920  INPLACE_ADD      
             1921  STORE_FAST               'msg'
           1924_0  COME_FROM          1899  '1899'
             1924  JUMP_FORWARD       1927  'to 1927'
           1927_0  COME_FROM          1924  '1924'

 L. 363      1927  LOAD_FAST                'e'
             1930  LOAD_ATTR                url
             1933  POP_JUMP_IF_FALSE  1976  'to 1976'

 L. 364      1936  LOAD_GLOBAL              urlparse
             1939  LOAD_FAST                'e'
             1942  LOAD_ATTR                url
             1945  CALL_FUNCTION_1       1  '1 positional, 0 named'
             1948  STORE_FAST               'parts'

 L. 365      1951  LOAD_FAST                'msg'
             1954  LOAD_STR                 ' in {}'
             1957  LOAD_ATTR                format
             1960  LOAD_FAST                'parts'
             1963  LOAD_ATTR                path
             1966  CALL_FUNCTION_1       1  '1 positional, 0 named'
             1969  INPLACE_ADD      
             1970  STORE_FAST               'msg'
             1973  JUMP_FORWARD       1976  'to 1976'
           1976_0  COME_FROM          1973  '1973'

 L. 366      1976  LOAD_GLOBAL              logger
             1979  LOAD_ATTR                critical
             1982  LOAD_FAST                'msg'
             1985  CALL_FUNCTION_1       1  '1 positional, 0 named'
             1988  POP_TOP          

 L. 367      1989  CONTINUE_LOOP      1512  'to 1512'
             1992  POP_BLOCK        
             1993  POP_EXCEPT       
             1994  LOAD_CONST               None
           1997_0  COME_FROM_FINALLY  1856  '1856'
             1997  LOAD_CONST               None
             2000  STORE_FAST               'e'
             2003  DELETE_FAST              'e'
             2006  END_FINALLY      
             2007  JUMP_FORWARD       2073  'to 2073'

 L. 369      2010  DUP_TOP          
             2011  LOAD_GLOBAL              ValueError
             2014  COMPARE_OP               exception-match
             2017  POP_JUMP_IF_FALSE  2072  'to 2072'
             2020  POP_TOP          
             2021  STORE_FAST               'e'
             2024  POP_TOP          
             2025  SETUP_FINALLY      2059  'to 2059'

 L. 370      2028  LOAD_GLOBAL              logger
             2031  LOAD_ATTR                critical
             2034  LOAD_STR                 'Not reloading: '
             2037  LOAD_GLOBAL              str
             2040  LOAD_FAST                'e'
             2043  CALL_FUNCTION_1       1  '1 positional, 0 named'
             2046  BINARY_ADD       
             2047  CALL_FUNCTION_1       1  '1 positional, 0 named'
             2050  POP_TOP          

 L. 371      2051  CONTINUE_LOOP      1512  'to 1512'
             2054  POP_BLOCK        
             2055  POP_EXCEPT       
             2056  LOAD_CONST               None
           2059_0  COME_FROM_FINALLY  2025  '2025'
             2059  LOAD_CONST               None
             2062  STORE_FAST               'e'
             2065  DELETE_FAST              'e'
             2068  END_FINALLY      
             2069  JUMP_FORWARD       2073  'to 2073'
             2072  END_FINALLY      
           2073_0  COME_FROM          2069  '2069'
           2073_1  COME_FROM          2007  '2007'
           2073_2  COME_FROM          1832  '1832'

 L. 373      2073  LOAD_GLOBAL              logger
             2076  LOAD_ATTR                info
             2079  LOAD_STR                 'DHCPv6 server restarting after configuration change'
             2082  CALL_FUNCTION_1       1  '1 positional, 0 named'
             2085  POP_TOP          

 L. 374      2086  LOAD_CONST               False
             2089  STORE_FAST               'running'

 L. 375      2092  LOAD_CONST               False
             2095  STORE_FAST               'stopping'

 L. 376      2098  CONTINUE           1512  'to 1512'
             2101  JUMP_ABSOLUTE      2806  'to 2806'
             2104  ELSE                     '2192'

 L. 378      2104  LOAD_FAST                'signal_nr'
             2107  LOAD_CONST               0
             2110  BINARY_SUBSCR    
             2111  LOAD_GLOBAL              signal
             2114  LOAD_ATTR                SIGINT
             2117  LOAD_GLOBAL              signal
             2120  LOAD_ATTR                SIGTERM
             2123  BUILD_TUPLE_2         2 
             2126  COMPARE_OP               in
             2129  POP_JUMP_IF_FALSE  2161  'to 2161'

 L. 379      2132  LOAD_GLOBAL              logger
             2135  LOAD_ATTR                debug
             2138  LOAD_STR                 'Received termination request'
             2141  CALL_FUNCTION_1       1  '1 positional, 0 named'
             2144  POP_TOP          

 L. 381      2145  LOAD_CONST               False
             2148  STORE_FAST               'running'

 L. 382      2151  LOAD_CONST               True
             2154  STORE_FAST               'stopping'

 L. 383      2157  BREAK_LOOP       
             2158  JUMP_ABSOLUTE      2806  'to 2806'
             2161  ELSE                     '2192'

 L. 385      2161  LOAD_FAST                'signal_nr'
             2164  LOAD_CONST               0
             2167  BINARY_SUBSCR    
             2168  LOAD_GLOBAL              signal
             2171  LOAD_ATTR                SIGUSR1
             2174  BUILD_TUPLE_1         1 
             2177  COMPARE_OP               in
             2180  POP_JUMP_IF_FALSE  2806  'to 2806'

 L. 387      2183  LOAD_CONST               True
             2186  STORE_FAST               'count_exception'
             2189  JUMP_ABSOLUTE      2806  'to 2806'
             2192  JUMP_BACK          1512  'to 1512'

 L. 389      2195  LOAD_GLOBAL              isinstance
             2198  LOAD_FAST                'key'
             2201  LOAD_ATTR                fileobj
             2204  LOAD_GLOBAL              ControlSocket
             2207  CALL_FUNCTION_2       2  '2 positional, 0 named'
             2210  POP_JUMP_IF_FALSE  2259  'to 2259'

 L. 391      2213  LOAD_FAST                'key'
             2216  LOAD_ATTR                fileobj
             2219  LOAD_ATTR                accept
             2222  CALL_FUNCTION_0       0  '0 positional, 0 named'
             2225  STORE_FAST               'control_connection'

 L. 392      2228  LOAD_FAST                'control_connection'
             2231  POP_JUMP_IF_FALSE  2806  'to 2806'

 L. 394      2234  LOAD_FAST                'sel'
             2237  LOAD_ATTR                register
             2240  LOAD_FAST                'control_connection'
             2243  LOAD_GLOBAL              selectors
             2246  LOAD_ATTR                EVENT_READ
             2249  CALL_FUNCTION_2       2  '2 positional, 0 named'
             2252  POP_TOP          
             2253  JUMP_ABSOLUTE      2806  'to 2806'
             2256  JUMP_BACK          1512  'to 1512'

 L. 396      2259  LOAD_GLOBAL              isinstance
             2262  LOAD_FAST                'key'
             2265  LOAD_ATTR                fileobj
             2268  LOAD_GLOBAL              ControlConnection
             2271  CALL_FUNCTION_2       2  '2 positional, 0 named'
             2274  POP_JUMP_IF_FALSE  1512  'to 1512'

 L. 398      2277  LOAD_FAST                'key'
             2280  LOAD_ATTR                fileobj
             2283  STORE_FAST               'control_connection'

 L. 399      2286  LOAD_FAST                'control_connection'
             2289  LOAD_ATTR                get_commands
             2292  CALL_FUNCTION_0       0  '0 positional, 0 named'
             2295  STORE_FAST               'commands'

 L. 400      2298  SETUP_LOOP         2806  'to 2806'
             2301  LOAD_FAST                'commands'
             2304  GET_ITER         
             2305  FOR_ITER           2802  'to 2802'
             2308  STORE_FAST               'command'

 L. 401      2311  LOAD_FAST                'command'
             2314  POP_JUMP_IF_FALSE  2342  'to 2342'

 L. 402      2317  LOAD_GLOBAL              logger
             2320  LOAD_ATTR                debug
             2323  LOAD_STR                 "Received control command '{}'"
             2326  LOAD_ATTR                format
             2329  LOAD_FAST                'command'
             2332  CALL_FUNCTION_1       1  '1 positional, 0 named'
             2335  CALL_FUNCTION_1       1  '1 positional, 0 named'
             2338  POP_TOP          
             2339  JUMP_FORWARD       2342  'to 2342'
           2342_0  COME_FROM          2339  '2339'

 L. 404      2342  LOAD_FAST                'command'
             2345  LOAD_STR                 'help'
             2348  COMPARE_OP               ==
             2351  POP_JUMP_IF_FALSE  2458  'to 2458'

 L. 405      2354  LOAD_FAST                'control_connection'
             2357  LOAD_ATTR                send
             2360  LOAD_STR                 'Recognised commands:'
             2363  CALL_FUNCTION_1       1  '1 positional, 0 named'
             2366  POP_TOP          

 L. 406      2367  LOAD_FAST                'control_connection'
             2370  LOAD_ATTR                send
             2373  LOAD_STR                 '  help'
             2376  CALL_FUNCTION_1       1  '1 positional, 0 named'
             2379  POP_TOP          

 L. 407      2380  LOAD_FAST                'control_connection'
             2383  LOAD_ATTR                send
             2386  LOAD_STR                 '  stats'
             2389  CALL_FUNCTION_1       1  '1 positional, 0 named'
             2392  POP_TOP          

 L. 408      2393  LOAD_FAST                'control_connection'
             2396  LOAD_ATTR                send
             2399  LOAD_STR                 '  stats-json'
             2402  CALL_FUNCTION_1       1  '1 positional, 0 named'
             2405  POP_TOP          

 L. 409      2406  LOAD_FAST                'control_connection'
             2409  LOAD_ATTR                send
             2412  LOAD_STR                 '  reload'
             2415  CALL_FUNCTION_1       1  '1 positional, 0 named'
             2418  POP_TOP          

 L. 410      2419  LOAD_FAST                'control_connection'
             2422  LOAD_ATTR                send
             2425  LOAD_STR                 '  shutdown'
             2428  CALL_FUNCTION_1       1  '1 positional, 0 named'
             2431  POP_TOP          

 L. 411      2432  LOAD_FAST                'control_connection'
             2435  LOAD_ATTR                send
             2438  LOAD_STR                 '  quit'
             2441  CALL_FUNCTION_1       1  '1 positional, 0 named'
             2444  POP_TOP          

 L. 412      2445  LOAD_FAST                'control_connection'
             2448  LOAD_ATTR                acknowledge
             2451  CALL_FUNCTION_0       0  '0 positional, 0 named'
             2454  POP_TOP          
             2455  JUMP_BACK          2305  'to 2305'

 L. 414      2458  LOAD_FAST                'command'
             2461  LOAD_STR                 'stats'
             2464  COMPARE_OP               ==
             2467  POP_JUMP_IF_FALSE  2502  'to 2502'

 L. 415      2470  LOAD_FAST                'control_connection'
             2473  LOAD_ATTR                send
             2476  LOAD_GLOBAL              str
             2479  LOAD_FAST                'statistics'
             2482  CALL_FUNCTION_1       1  '1 positional, 0 named'
             2485  CALL_FUNCTION_1       1  '1 positional, 0 named'
             2488  POP_TOP          

 L. 416      2489  LOAD_FAST                'control_connection'
             2492  LOAD_ATTR                acknowledge
             2495  CALL_FUNCTION_0       0  '0 positional, 0 named'
             2498  POP_TOP          
             2499  JUMP_BACK          2305  'to 2305'

 L. 418      2502  LOAD_FAST                'command'
             2505  LOAD_STR                 'stats-json'
             2508  COMPARE_OP               ==
             2511  POP_JUMP_IF_FALSE  2555  'to 2555'

 L. 419      2514  LOAD_FAST                'control_connection'
             2517  LOAD_ATTR                send
             2520  LOAD_GLOBAL              json
             2523  LOAD_ATTR                dumps
             2526  LOAD_FAST                'statistics'
             2529  LOAD_ATTR                export
             2532  CALL_FUNCTION_0       0  '0 positional, 0 named'
             2535  CALL_FUNCTION_1       1  '1 positional, 0 named'
             2538  CALL_FUNCTION_1       1  '1 positional, 0 named'
             2541  POP_TOP          

 L. 420      2542  LOAD_FAST                'control_connection'
             2545  LOAD_ATTR                acknowledge
             2548  CALL_FUNCTION_0       0  '0 positional, 0 named'
             2551  POP_TOP          
             2552  JUMP_BACK          2305  'to 2305'

 L. 422      2555  LOAD_FAST                'command'
             2558  LOAD_STR                 'reload'
             2561  COMPARE_OP               ==
             2564  POP_JUMP_IF_FALSE  2611  'to 2611'

 L. 424      2567  LOAD_GLOBAL              os
             2570  LOAD_ATTR                write
             2573  LOAD_FAST                'signal_w'
             2576  LOAD_GLOBAL              bytes
             2579  LOAD_GLOBAL              signal
             2582  LOAD_ATTR                SIGHUP
             2585  BUILD_LIST_1          1 
             2588  CALL_FUNCTION_1       1  '1 positional, 0 named'
             2591  CALL_FUNCTION_2       2  '2 positional, 0 named'
             2594  POP_TOP          

 L. 425      2595  LOAD_FAST                'control_connection'
             2598  LOAD_ATTR                acknowledge
             2601  LOAD_STR                 'Reloading'
             2604  CALL_FUNCTION_1       1  '1 positional, 0 named'
             2607  POP_TOP          
             2608  JUMP_BACK          2305  'to 2305'

 L. 427      2611  LOAD_FAST                'command'
             2614  LOAD_STR                 'shutdown'
             2617  COMPARE_OP               ==
             2620  POP_JUMP_IF_FALSE  2691  'to 2691'

 L. 429      2623  LOAD_FAST                'control_connection'
             2626  LOAD_ATTR                acknowledge
             2629  LOAD_STR                 'Shutting down'
             2632  CALL_FUNCTION_1       1  '1 positional, 0 named'
             2635  POP_TOP          

 L. 430      2636  LOAD_FAST                'control_connection'
             2639  LOAD_ATTR                close
             2642  CALL_FUNCTION_0       0  '0 positional, 0 named'
             2645  POP_TOP          

 L. 431      2646  LOAD_FAST                'sel'
             2649  LOAD_ATTR                unregister
             2652  LOAD_FAST                'control_connection'
             2655  CALL_FUNCTION_1       1  '1 positional, 0 named'
             2658  POP_TOP          

 L. 433      2659  LOAD_GLOBAL              os
             2662  LOAD_ATTR                write
             2665  LOAD_FAST                'signal_w'
             2668  LOAD_GLOBAL              bytes
             2671  LOAD_GLOBAL              signal
             2674  LOAD_ATTR                SIGTERM
             2677  BUILD_LIST_1          1 
             2680  CALL_FUNCTION_1       1  '1 positional, 0 named'
             2683  CALL_FUNCTION_2       2  '2 positional, 0 named'
             2686  POP_TOP          

 L. 434      2687  BREAK_LOOP       
             2688  JUMP_BACK          2305  'to 2305'

 L. 436      2691  LOAD_FAST                'command'
             2694  LOAD_STR                 'quit'
             2697  COMPARE_OP               ==
             2700  POP_JUMP_IF_TRUE   2715  'to 2715'
             2703  LOAD_FAST                'command'
             2706  LOAD_CONST               None
             2709  COMPARE_OP               is
           2712_0  COME_FROM          2700  '2700'
             2712  POP_JUMP_IF_FALSE  2767  'to 2767'

 L. 437      2715  LOAD_FAST                'command'
             2718  LOAD_STR                 'quit'
             2721  COMPARE_OP               ==
             2724  POP_JUMP_IF_FALSE  2740  'to 2740'

 L. 439      2727  LOAD_FAST                'control_connection'
             2730  LOAD_ATTR                acknowledge
             2733  CALL_FUNCTION_0       0  '0 positional, 0 named'
             2736  POP_TOP          
             2737  JUMP_FORWARD       2740  'to 2740'
           2740_0  COME_FROM          2737  '2737'

 L. 441      2740  LOAD_FAST                'control_connection'
             2743  LOAD_ATTR                close
             2746  CALL_FUNCTION_0       0  '0 positional, 0 named'
             2749  POP_TOP          

 L. 442      2750  LOAD_FAST                'sel'
             2753  LOAD_ATTR                unregister
             2756  LOAD_FAST                'control_connection'
             2759  CALL_FUNCTION_1       1  '1 positional, 0 named'
             2762  POP_TOP          

 L. 443      2763  BREAK_LOOP       
             2764  JUMP_BACK          2305  'to 2305'

 L. 446      2767  LOAD_GLOBAL              logger
             2770  LOAD_ATTR                warning
             2773  LOAD_STR                 "Rejecting unknown control command '{}'"
             2776  LOAD_ATTR                format
             2779  LOAD_FAST                'command'
             2782  CALL_FUNCTION_1       1  '1 positional, 0 named'
             2785  CALL_FUNCTION_1       1  '1 positional, 0 named'
             2788  POP_TOP          

 L. 447      2789  LOAD_FAST                'control_connection'
             2792  LOAD_ATTR                reject
             2795  CALL_FUNCTION_0       0  '0 positional, 0 named'
             2798  POP_TOP          
             2799  JUMP_BACK          2305  'to 2305'
             2802  POP_BLOCK        
           2803_0  COME_FROM_LOOP     2298  '2298'
             2803  JUMP_BACK          1512  'to 1512'
           2806_0  COME_FROM_EXCEPT_CLAUSE  1625  '1625'
             2806  JUMP_BACK          1512  'to 1512'
             2809  POP_BLOCK        
           2810_0  COME_FROM_LOOP     1505  '1505'
             2810  POP_BLOCK        
             2811  JUMP_FORWARD       2879  'to 2879'
           2814_0  COME_FROM_EXCEPT   1490  '1490'

 L. 449      2814  DUP_TOP          
             2815  LOAD_GLOBAL              Exception
             2818  COMPARE_OP               exception-match
             2821  POP_JUMP_IF_FALSE  2878  'to 2878'
             2824  POP_TOP          
             2825  STORE_FAST               'e'
             2828  POP_TOP          
             2829  SETUP_FINALLY      2865  'to 2865'

 L. 451      2832  LOAD_GLOBAL              logger
             2835  LOAD_ATTR                exception
             2838  LOAD_STR                 'Caught unexpected exception {!r}'
             2841  LOAD_ATTR                format
             2844  LOAD_FAST                'e'
             2847  CALL_FUNCTION_1       1  '1 positional, 0 named'
             2850  CALL_FUNCTION_1       1  '1 positional, 0 named'
             2853  POP_TOP          

 L. 452      2854  LOAD_CONST               True
             2857  STORE_FAST               'count_exception'
             2860  POP_BLOCK        
             2861  POP_EXCEPT       
             2862  LOAD_CONST               None
           2865_0  COME_FROM_FINALLY  2829  '2829'
             2865  LOAD_CONST               None
             2868  STORE_FAST               'e'
             2871  DELETE_FAST              'e'
             2874  END_FINALLY      
             2875  JUMP_FORWARD       2879  'to 2879'
             2878  END_FINALLY      
           2879_0  COME_FROM          2875  '2875'
           2879_1  COME_FROM          2811  '2811'

 L. 454      2879  LOAD_FAST                'count_exception'
             2882  POP_JUMP_IF_FALSE  1478  'to 1478'

 L. 455      2885  LOAD_GLOBAL              time
             2888  LOAD_ATTR                monotonic
             2891  CALL_FUNCTION_0       0  '0 positional, 0 named'
             2894  STORE_FAST               'now'

 L. 458      2897  LOAD_FAST                'exception_history'
             2900  LOAD_ATTR                append
             2903  LOAD_FAST                'now'
             2906  CALL_FUNCTION_1       1  '1 positional, 0 named'
             2909  POP_TOP          

 L. 461      2910  LOAD_FAST                'now'
             2913  LOAD_FAST                'config'
             2916  LOAD_ATTR                exception_window
             2919  BINARY_SUBTRACT  
             2920  STORE_FAST               'cutoff'

 L. 462      2923  SETUP_LOOP         2965  'to 2965'
             2926  LOAD_FAST                'exception_history'
             2929  POP_JUMP_IF_FALSE  2964  'to 2964'
             2932  LOAD_FAST                'exception_history'
             2935  LOAD_CONST               0
             2938  BINARY_SUBSCR    
             2939  LOAD_FAST                'cutoff'
             2942  COMPARE_OP               <
           2945_0  COME_FROM          2929  '2929'
             2945  POP_JUMP_IF_FALSE  2964  'to 2964'

 L. 463      2948  LOAD_FAST                'exception_history'
             2951  LOAD_ATTR                pop
             2954  LOAD_CONST               0
             2957  CALL_FUNCTION_1       1  '1 positional, 0 named'
             2960  POP_TOP          
             2961  JUMP_BACK          2926  'to 2926'
             2964  POP_BLOCK        
           2965_0  COME_FROM_LOOP     2923  '2923'

 L. 466      2965  LOAD_GLOBAL              len
             2968  LOAD_FAST                'exception_history'
             2971  CALL_FUNCTION_1       1  '1 positional, 0 named'
             2974  LOAD_FAST                'config'
             2977  LOAD_ATTR                max_exceptions
             2980  COMPARE_OP               >
             2983  POP_JUMP_IF_FALSE  3035  'to 3035'

 L. 467      2986  LOAD_GLOBAL              logger
             2989  LOAD_ATTR                critical
             2992  LOAD_STR                 'Received more than {} exceptions in {} seconds, exiting'
             2995  LOAD_ATTR                format

 L. 468      2998  LOAD_FAST                'config'
             3001  LOAD_ATTR                max_exceptions
             3004  LOAD_FAST                'config'
             3007  LOAD_ATTR                exception_window
             3010  CALL_FUNCTION_2       2  '2 positional, 0 named'
             3013  CALL_FUNCTION_1       1  '1 positional, 0 named'
             3016  POP_TOP          

 L. 469      3017  LOAD_CONST               False
             3020  STORE_FAST               'running'

 L. 470      3023  LOAD_CONST               True
             3026  STORE_FAST               'stopping'
             3029  JUMP_ABSOLUTE      3035  'to 3035'
             3032  CONTINUE           1478  'to 1478'
             3035  JUMP_BACK          1478  'to 1478'
             3038  POP_BLOCK        
           3039_0  COME_FROM_LOOP     1475  '1475'

 L. 472      3039  LOAD_FAST                'pool'
             3042  LOAD_ATTR                close
             3045  CALL_FUNCTION_0       0  '0 positional, 0 named'
             3048  POP_TOP          

 L. 473      3049  LOAD_FAST                'pool'
             3052  LOAD_ATTR                join
             3055  CALL_FUNCTION_0       0  '0 positional, 0 named'
             3058  POP_TOP          
             3059  POP_BLOCK        
             3060  LOAD_CONST               None
           3063_0  COME_FROM_WITH     1450  '1450'
             3063  WITH_CLEANUP     
             3064  END_FINALLY      

 L. 476      3065  LOAD_GLOBAL              restore_privileges
             3068  CALL_FUNCTION_0       0  '0 positional, 0 named'
             3071  POP_TOP          

 L. 477      3072  SETUP_EXCEPT       3123  'to 3123'

 L. 478      3075  LOAD_FAST                'pid_filename'
             3078  POP_JUMP_IF_FALSE  3119  'to 3119'

 L. 479      3081  LOAD_GLOBAL              os
             3084  LOAD_ATTR                unlink
             3087  LOAD_FAST                'pid_filename'
             3090  CALL_FUNCTION_1       1  '1 positional, 0 named'
             3093  POP_TOP          

 L. 480      3094  LOAD_GLOBAL              logger
             3097  LOAD_ATTR                info
             3100  LOAD_STR                 'Removing PID-file {}'
             3103  LOAD_ATTR                format
             3106  LOAD_FAST                'pid_filename'
             3109  CALL_FUNCTION_1       1  '1 positional, 0 named'
             3112  CALL_FUNCTION_1       1  '1 positional, 0 named'
             3115  POP_TOP          
             3116  JUMP_FORWARD       3119  'to 3119'
           3119_0  COME_FROM          3116  '3116'
             3119  POP_BLOCK        
             3120  JUMP_FORWARD       3141  'to 3141'
           3123_0  COME_FROM_EXCEPT   3072  '3072'

 L. 481      3123  DUP_TOP          
             3124  LOAD_GLOBAL              OSError
             3127  COMPARE_OP               exception-match
             3130  POP_JUMP_IF_FALSE  3140  'to 3140'
             3133  POP_TOP          
             3134  POP_TOP          
             3135  POP_TOP          

 L. 482      3136  POP_EXCEPT       
             3137  JUMP_FORWARD       3141  'to 3141'
             3140  END_FINALLY      
           3141_0  COME_FROM          3137  '3137'
           3141_1  COME_FROM          3120  '3120'

 L. 484      3141  SETUP_EXCEPT       3198  'to 3198'

 L. 485      3144  LOAD_FAST                'control_socket'
             3147  POP_JUMP_IF_FALSE  3194  'to 3194'

 L. 486      3150  LOAD_GLOBAL              os
             3153  LOAD_ATTR                unlink
             3156  LOAD_FAST                'control_socket'
             3159  LOAD_ATTR                socket_path
             3162  CALL_FUNCTION_1       1  '1 positional, 0 named'
             3165  POP_TOP          

 L. 487      3166  LOAD_GLOBAL              logger
             3169  LOAD_ATTR                info
             3172  LOAD_STR                 'Removing control socket {}'
             3175  LOAD_ATTR                format
             3178  LOAD_FAST                'control_socket'
             3181  LOAD_ATTR                socket_path
             3184  CALL_FUNCTION_1       1  '1 positional, 0 named'
             3187  CALL_FUNCTION_1       1  '1 positional, 0 named'
             3190  POP_TOP          
             3191  JUMP_FORWARD       3194  'to 3194'
           3194_0  COME_FROM          3191  '3191'
             3194  POP_BLOCK        
             3195  JUMP_BACK           711  'to 711'
           3198_0  COME_FROM_EXCEPT   3141  '3141'

 L. 488      3198  DUP_TOP          
             3199  LOAD_GLOBAL              OSError
             3202  COMPARE_OP               exception-match
             3205  POP_JUMP_IF_FALSE  3215  'to 3215'
             3208  POP_TOP          
             3209  POP_TOP          
             3210  POP_TOP          

 L. 489      3211  POP_EXCEPT       
             3212  JUMP_BACK           711  'to 711'
             3215  END_FINALLY      
             3216  JUMP_BACK           711  'to 711'
             3219  POP_BLOCK        
           3220_0  COME_FROM_LOOP      708  '708'

 L. 491      3220  LOAD_GLOBAL              logger
             3223  LOAD_ATTR                info
             3226  LOAD_STR                 'Shutting down Python DHCPv6 server v{}'
             3229  LOAD_ATTR                format
             3232  LOAD_GLOBAL              dhcpkit
             3235  LOAD_ATTR                __version__
             3238  CALL_FUNCTION_1       1  '1 positional, 0 named'
             3241  CALL_FUNCTION_1       1  '1 positional, 0 named'
             3244  POP_TOP          

 L. 493      3245  LOAD_CONST               0
             3248  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM_EXCEPT_CLAUSE' instruction at offset 2806_0


def run() -> int:
    """
    Run the main program and handle exceptions

    :return: The program exit code
    """
    try:
        return main(sys.argv[1:])
    except Exception as e:
        logger.exception('Error: {}'.format(e))
        return 1


if __name__ == '__main__':
    sys.exit(run())