# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/kipp3/runner/runner.py
# Compiled at: 2019-12-16 21:55:05
# Size of source mod 2**32: 5776 bytes
"""
-----------
Kipp Runner
-----------

Collect scripts' running status into MongoDB

Arguments:
    -t, --timeout (int): seconds to throw ``KippRunnerTimeoutException``
    -l, --lock: only allow single process running

Examples:
::
    cd code/postconvertor && TARS_ENV=www2 /opt/venv/bin/python -m kipp.runner -t 30 -l "/opt/venv/bin/python PostConvertor.py"
"""
from __future__ import unicode_literals
import argparse, subprocess, sys, inspect, time, os, signal, traceback
from datetime import timedelta
from random import randint
from textwrap import dedent
import kipp3.options as opt
opt.patch_utilities()
from kipp3.aio import Event, run_until_complete
from kipp3.libs.aio import KippAIOTimeoutError
from kipp3.utils import ThreadPoolExecutor, check_is_allow_to_running, generate_validate_fname, get_logger, EmailSender, utcnow
from .exceptions import KippRunnerTimeoutException, KippRunnerException, KippRunnerSIGTERMException
from .models import RunStatsMonitor
RECEIVERS = ('lcai@movoto.com', )

def is_need_to_clean_old_records():
    return randint(0, 1000) == 1


def clean_monitor_logs():
    dt_range = timedelta(days=(-30))
    if is_need_to_clean_old_records():
        opt.runner_monitor.clean_logs_by_timedelta(dt_range)


def _process_runner(process, evt):

    def _set_evt(futu):
        evt.set()

    f = opt.executor.submit(process.communicate)
    f.add_done_callback(_set_evt)
    return f


def kill_process(process):
    if not process:
        return
    try:
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)
    except OSError:
        pass


def send_alert_email(msg):
    get_logger().info('try to send runner alert email...')
    if opt.debug:
        receivers = 'lcai@movoto.com'
    else:
        receivers = ','.join(RECEIVERS)
    content = dedent('\n        time: {dt}\n        command: {command}\n        error: {err}\n        '.format(dt=(utcnow().strftime('%Y-%m-%dT%H:%M:%S')),
      command=(opt.command),
      err=msg))
    opt.sender.send_email(mail_from='data@movoto.com',
      mail_to=receivers,
      subject='DATA Monitoring: Runner got critical error',
      content=content)


def wait_process_done--- This code section failed: ---

 L. 115         0  LOAD_GLOBAL              Event
                2  CALL_FUNCTION_0       0  ''
                4  STORE_FAST               'evt'

 L. 116         6  LOAD_GLOBAL              _process_runner
                8  LOAD_FAST                'process'
               10  LOAD_FAST                'evt'
               12  CALL_FUNCTION_2       2  ''
               14  STORE_FAST               'f_p'

 L. 117        16  SETUP_FINALLY       154  'to 154'
               18  SETUP_FINALLY        54  'to 54'

 L. 118        20  LOAD_FAST                'evt'
               22  LOAD_ATTR                wait
               24  LOAD_GLOBAL              opt
               26  LOAD_ATTR                timeout
               28  LOAD_CONST               ('timeout',)
               30  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               32  STORE_FAST               'futu'

 L. 119        34  LOAD_GLOBAL              run_until_complete
               36  LOAD_FAST                'futu'
               38  CALL_FUNCTION_1       1  ''
               40  POP_TOP          

 L. 120        42  LOAD_FAST                'futu'
               44  LOAD_METHOD              result
               46  CALL_METHOD_0         0  ''
               48  POP_TOP          
               50  POP_BLOCK        
               52  JUMP_FORWARD        138  'to 138'
             54_0  COME_FROM_FINALLY    18  '18'

 L. 121        54  DUP_TOP          
               56  LOAD_GLOBAL              KippAIOTimeoutError
               58  COMPARE_OP               exception-match
               60  POP_JUMP_IF_FALSE   136  'to 136'
               62  POP_TOP          
               64  POP_TOP          
               66  POP_TOP          

 L. 122        68  SETUP_FINALLY        82  'to 82'

 L. 123        70  LOAD_GLOBAL              kill_process
               72  LOAD_FAST                'process'
               74  CALL_FUNCTION_1       1  ''
               76  POP_TOP          
               78  POP_BLOCK        
               80  JUMP_FORWARD        118  'to 118'
             82_0  COME_FROM_FINALLY    68  '68'

 L. 124        82  DUP_TOP          
               84  LOAD_GLOBAL              OSError
               86  COMPARE_OP               exception-match
               88  POP_JUMP_IF_FALSE   116  'to 116'
               90  POP_TOP          
               92  POP_TOP          
               94  POP_TOP          

 L. 125        96  LOAD_FAST                'f_p'
               98  LOAD_METHOD              result
              100  CALL_METHOD_0         0  ''
              102  ROT_FOUR         
              104  POP_EXCEPT       
              106  ROT_FOUR         
              108  POP_EXCEPT       
              110  POP_BLOCK        
              112  CALL_FINALLY        154  'to 154'
              114  RETURN_VALUE     
            116_0  COME_FROM            88  '88'
              116  END_FINALLY      
            118_0  COME_FROM            80  '80'

 L. 127       118  LOAD_GLOBAL              KippRunnerTimeoutException

 L. 128       120  LOAD_STR                 'process exceeds timeout {}s'
              122  LOAD_METHOD              format
              124  LOAD_FAST                'timeout'
              126  CALL_METHOD_1         1  ''

 L. 127       128  CALL_FUNCTION_1       1  ''
              130  RAISE_VARARGS_1       1  'exception instance'
              132  POP_EXCEPT       
              134  JUMP_FORWARD        150  'to 150'
            136_0  COME_FROM            60  '60'
              136  END_FINALLY      
            138_0  COME_FROM            52  '52'

 L. 131       138  LOAD_FAST                'f_p'
              140  LOAD_METHOD              result
              142  CALL_METHOD_0         0  ''
              144  POP_BLOCK        
              146  CALL_FINALLY        154  'to 154'
              148  RETURN_VALUE     
            150_0  COME_FROM           134  '134'
              150  POP_BLOCK        
              152  BEGIN_FINALLY    
            154_0  COME_FROM           146  '146'
            154_1  COME_FROM           112  '112'
            154_2  COME_FROM_FINALLY    16  '16'

 L. 133       154  LOAD_GLOBAL              opt
              156  LOAD_ATTR                executor
              158  LOAD_METHOD              shutdown
              160  CALL_METHOD_0         0  ''
              162  POP_TOP          
              164  END_FINALLY      

Parse error at or near `ROT_FOUR' instruction at offset 106


def handle_signal_quit(signal, frame):
    err_msg = 'quit by signal {}:\n{}'.format(signal, inspect.getframeinfo(frame))
    if signal:
        raise KippRunnerSIGTERMException(err_msg)


def catch_sys_quit_signal():
    signal.signal(signal.SIGTERM, handle_signal_quit)


def runner(command):
    process = err_msg = None
    opt.set_option('runner_command_start_at', time.time())
    try:
        try:
            opt.set_option('runner_monitor', RunStatsMonitor(command=command, args=(sys.argv[1:-1])))
            clean_monitor_logs()
            catch_sys_quit_signal()
            opt.runner_monitor.start()
            get_logger().info('kipp.runner for %s', command)
            opt.set_option('runner_command_start_at', time.time())
            process = subprocess.Popen([
             command],
              shell=True,
              stderr=(subprocess.PIPE),
              stdout=(subprocess.PIPE),
              preexec_fn=(os.setsid))
            if opt.timeout:
                r = wait_process_done(process, opt.timeout)
            else:
                r = process.communicate()
            if process.returncode != 0:
                err_msg = r[1]
                raise RuntimeError(err_msg)
        except BaseException as err:
            try:
                get_logger().exception(err)
                err_msg = traceback.format_exc()
                opt.runner_monitor.fail(err_msg)
                raise
            finally:
                err = None
                del err

        else:
            get_logger().info('successed: %s', command)
            opt.runner_monitor.success()
    finally:
        kill_process(process)


def setup_settings():
    opt.set_option('executor', ThreadPoolExecutor(2))
    opt.set_option('sender', EmailSender(host=(opt.SMTP_HOST)))


def setup_arguments():
    opt.add_argument('-t', '--timeout', type=int, default=0, help='seconds')
    opt.add_argument('-ms',
      '--minimal_running_seconds',
      type=int,
      default=30,
      help='minimal running seconds')
    opt.add_argument('-l',
      '--lock',
      action='store_true',
      default=False,
      help='only allow single running')
    opt.add_argument('--debug', action='store_true', default=False)
    opt.add_argument('command', nargs=(argparse.REMAINDER))
    opt.parse_args()
    if not opt.command:
        raise AttributeError('You should run like ``python -m runner <COMMAND>``')
    opt.set_option('command', ' '.join(opt.command))


def main():
    setup_arguments()
    setup_settings()
    if opt.lock:
        lock_fname = generate_validate_fname(opt.command)
        fp = check_is_allow_to_running(lock_fname)
        if not fp:
            raise KippRunnerException('another process is still running')
    runner(opt.command)