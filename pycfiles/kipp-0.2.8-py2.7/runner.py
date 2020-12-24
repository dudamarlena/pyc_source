# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/kipp/runner/runner.py
# Compiled at: 2019-11-20 22:44:04
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
from kipp.options import options as opt
opt.patch_utilities()
from kipp.aio import Event, run_until_complete
from kipp.libs.aio import KippAIOTimeoutError
from kipp.utils import ThreadPoolExecutor, check_is_allow_to_running, generate_validate_fname, get_logger, EmailSender, utcnow
from .exceptions import KippRunnerTimeoutException, KippRunnerException, KippRunnerSIGTERMException
from .models import RunStatsMonitor
RECEIVERS = ('lcai@movoto.com', )

def is_need_to_clean_old_records():
    return randint(0, 1000) == 1


def clean_monitor_logs():
    dt_range = timedelta(days=-30)
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
    get_logger().info(b'try to send runner alert email...')
    if opt.debug:
        receivers = b'lcai@movoto.com'
    else:
        receivers = (b',').join(RECEIVERS)
    content = dedent((b'\n        time: {dt}\n        command: {command}\n        error: {err}\n        ').format(dt=utcnow().strftime(b'%Y-%m-%dT%H:%M:%S'), command=opt.command, err=msg))
    opt.sender.send_email(mail_from=b'data@movoto.com', mail_to=receivers, subject=b'DATA Monitoring: Runner got critical error', content=content)


def wait_process_done(process, timeout):
    evt = Event()
    f_p = _process_runner(process, evt)
    try:
        try:
            futu = evt.wait(timeout=opt.timeout)
            run_until_complete(futu)
            futu.result()
        except KippAIOTimeoutError:
            try:
                kill_process(process)
            except OSError:
                return f_p.result()

            raise KippRunnerTimeoutException((b'process exceeds timeout {}s').format(timeout))
        else:
            return f_p.result()

    finally:
        opt.executor.shutdown()


def handle_signal_quit(signal, frame):
    err_msg = (b'quit by signal {}:\n{}').format(signal, inspect.getframeinfo(frame))
    if signal:
        raise KippRunnerSIGTERMException(err_msg)


def catch_sys_quit_signal():
    signal.signal(signal.SIGTERM, handle_signal_quit)


def runner(command):
    process = err_msg = None
    opt.set_option(b'runner_command_start_at', time.time())
    try:
        try:
            opt.set_option(b'runner_monitor', RunStatsMonitor(command=command, args=sys.argv[1:-1]))
            clean_monitor_logs()
            catch_sys_quit_signal()
            opt.runner_monitor.start()
            get_logger().info(b'kipp.runner for %s', command)
            opt.set_option(b'runner_command_start_at', time.time())
            process = subprocess.Popen([
             command], shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE, preexec_fn=os.setsid)
            if opt.timeout:
                r = wait_process_done(process, opt.timeout)
            else:
                r = process.communicate()
            if process.returncode != 0:
                err_msg = r[1]
                raise RuntimeError(err_msg)
        except BaseException as err:
            get_logger().exception(err)
            err_msg = traceback.format_exc()
            opt.runner_monitor.fail(err_msg)
            raise
        else:
            get_logger().info(b'successed: %s', command)
            opt.runner_monitor.success()

    finally:
        kill_process(process)

    return


def setup_settings():
    opt.set_option(b'executor', ThreadPoolExecutor(2))
    opt.set_option(b'sender', EmailSender(host=opt.SMTP_HOST))


def setup_arguments():
    opt.add_argument(b'-t', b'--timeout', type=int, default=0, help=b'seconds')
    opt.add_argument(b'-ms', b'--minimal_running_seconds', type=int, default=30, help=b'minimal running seconds')
    opt.add_argument(b'-l', b'--lock', action=b'store_true', default=False, help=b'only allow single running')
    opt.add_argument(b'--debug', action=b'store_true', default=False)
    opt.add_argument(b'command', nargs=argparse.REMAINDER)
    opt.parse_args()
    if not opt.command:
        raise AttributeError(b'You should run like ``python -m runner <COMMAND>``')
    opt.set_option(b'command', (b' ').join(opt.command))


def main():
    setup_arguments()
    setup_settings()
    if opt.lock:
        lock_fname = generate_validate_fname(opt.command)
        fp = check_is_allow_to_running(lock_fname)
        if not fp:
            raise KippRunnerException(b'another process is still running')
    runner(opt.command)