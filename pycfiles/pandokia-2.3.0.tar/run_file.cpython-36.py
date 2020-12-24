# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jhunk/Downloads/pandokia/pandokia/run_file.py
# Compiled at: 2018-06-06 10:16:33
# Size of source mod 2**32: 17342 bytes
from tempfile import NamedTemporaryFile
import os, os.path, sys, fnmatch, datetime, signal, errno, pandokia, platform
windows = platform.system() == 'Windows'
import subprocess, pandokia.common as common
from pandokia.run_status import pdkrun_status
import pandokia.runners
runner_glob = pandokia.runners.runner_glob
try:
    runner_glob = pandokia.cfg.runner_glob + runner_glob
except AttributeError:
    pass

runner_glob_cache = {}

def read_runner_glob(dirname):
    dirname = os.path.abspath(dirname)
    if dirname in runner_glob_cache:
        return runner_glob_cache[dirname]
    else:
        parent = os.path.abspath(dirname + '/..')
        parent = parent.replace('//', '/')
        if parent == dirname:
            parent_list = runner_glob
        else:
            if os.path.exists(dirname + '/pandokia_top'):
                parent_list = runner_glob
            else:
                parent_list = read_runner_glob(parent)
            try:
                f = open(dirname + '/pdk_runners', 'r')
            except IOError as e:
                if e.errno == errno.ENOENT:
                    return parent_list
                raise

        here_list = []
        for line in f:
            line = line.strip()
            if line.startswith('#'):
                continue
            line = line.split()
            if len(line) == 2:
                here_list.append((line[0], line[1]))

        f.close()
        l = here_list + parent_list
        runner_glob_cache[dirname] = l
        return l


def select_runner(dirname, basename):
    runner_glob = read_runner_glob(dirname)
    for pat, runner in runner_glob:
        if fnmatch.fnmatch(basename, pat):
            if runner == 'none':
                return
            else:
                return runner


runner_modules = {}

def get_runner_mod(runner):
    if runner in runner_modules:
        runner_mod = runner_modules[runner]
    else:
        try:
            n = 'pandokia_runner_' + runner
            __import__(n)
        except ImportError:
            n = 'pandokia.runners.' + runner
            __import__(n)

        runner_mod = sys.modules[n]
        runner_modules[runner] = runner_mod
    return runner_mod


def get_prefix(envgetter, dirname):
    top = envgetter.gettop()
    assert dirname.startswith(top)
    prefix = dirname[len(top):] + '/'
    if prefix.startswith('/') or prefix.startswith('\\'):
        prefix = prefix[1:]
    if 'PDK_TESTPREFIX' in os.environ:
        e = os.environ['PDK_TESTPREFIX']
        if not (e.endswith('/') or e.endswith('.')):
            e += '/'
        prefix = e + prefix
    return prefix


def pdk_log_name(env):
    log = env['PDK_LOG']
    if 'PDK_PROCESS_SLOT' in env:
        log += '.' + env['PDK_PROCESS_SLOT']
    return log


def run(dirname, basename, envgetter, runner):
    global timeout_proc_kills
    cause = 'unknown'
    return_status = 0
    dirname = os.path.abspath(dirname)
    save_dir = os.getcwd()
    os.chdir(dirname)
    if runner is None:
        runner = select_runner(dirname, basename)
    else:
        if runner is not None:
            env = dict(envgetter.envdir(dirname))
            env['PDK_TESTPREFIX'] = get_prefix(envgetter, dirname)
            env['PDK_TOP'] = envgetter.gettop()
            runner_mod = get_runner_mod(runner)
            env['PDK_FILE'] = basename
            env['PDK_LOG'] = pdk_log_name(env)
            stat_summary = {}
            for x in pandokia.cfg.statuses:
                stat_summary[x] = 0

            if 'PDK_PROCESS_SLOT' in env:
                summary_file = env['PDK_LOG'] + '.summary'
                slot_id = env['PDK_PROCESS_SLOT']
            else:
                summary_file = None
                slot_id = '0'
            f = open(env['PDK_LOG'], 'a+')
            f.seek(0, 2)
            end_of_log = f.tell()
            f.close()
            env['PDK_DIRECTORY'] = dirname
            full_filename = dirname + '/' + env['PDK_FILE']
            f = open(env['PDK_LOG'], 'a')
            f.write('\n\nSTART\n')
            f.write('test_run=%s\n' % env['PDK_TESTRUN'])
            f.write('project=%s\n' % env['PDK_PROJECT'])
            f.write('host=%s\n' % env['PDK_HOST'])
            f.write('location=%s\n' % full_filename)
            f.write('test_runner=%s\n' % runner)
            f.write('context=%s\n' % env['PDK_CONTEXT'])
            f.write('SETDEFAULT\n')
            f.close()
            cmd = runner_mod.command(env)
            output_buffer = ''
            if cmd is not None:
                if not isinstance(cmd, list):
                    cmd = [
                     cmd]
                for thiscmd in cmd:
                    print('COMMAND : %s (for file %s) %s' % (
                     repr(thiscmd), full_filename, datetime.datetime.now()))
                    sys.stdout.flush()
                    sys.stderr.flush()
                    if windows:
                        f = open('stdout.%s.tmp' % slot_id, 'w')
                        p = subprocess.Popen(thiscmd,
                          stdout=f,
                          stderr=f,
                          shell=True,
                          env=env,
                          creationflags=(subprocess.CREATE_NEW_PROCESS_GROUP))
                        status = p.wait()
                        f.close()
                        f = open('stdout.%s.tmp' % slot_id, 'r')
                        output_buffer = f.read()
                        sys.stdout.write(output_buffer)
                        f.close()
                        os.unlink('stdout.%s.tmp' % slot_id)
                    else:
                        with NamedTemporaryFile(mode='r+b') as (f):
                            p = subprocess.Popen((thiscmd.split()),
                              stdout=f,
                              stderr=f,
                              shell=False,
                              env=env,
                              preexec_fn=unix_preexec)
                            if 'PDK_TIMEOUT' in env:
                                proc_timeout_start(env['PDK_TIMEOUT'], p)
                                status = p.wait()
                                print('return from wait, status=%d' % status)
                                proc_timeout_terminate()
                                if timeout_proc_kills > 0:
                                    status = -15
                            else:
                                status = p.wait()
                            f.seek(0)
                            output_buffer = f.read().decode()
                            sys.stdout.write(output_buffer)
                    if status >= 0:
                        cause = 'exit'
                        return_status = status
                    else:
                        if status < 0:
                            cause = 'signal'
                            return_status = -status
                    print('COMMAND EXIT: %s %s %s' % (
                     cause, return_status, datetime.datetime.now()))

            else:
                print('RUNNING INTERNALLY (for file %s)' % full_filename)
                runner_mod.run_internally(env)
                print('DONE RUNNING INTERNALLY')
            pdkrun_status(full_filename)
            if return_status > 1 or return_status < 0:
                f = open(env['PDK_LOG'], 'a')
                f.write('\n')
                f.write('test_name=%s\n' % full_filename)
                f.write('status=E\n')
                if output_buffer:
                    f.write('log:\n')
                    f.write('.[PANDOKIA]\n')
                    f.write('.FATAL: NON-STANDARD EXIT VALUE DETECTED! ({})\n'.format(return_status))
                    f.write('.\n')
                    f.write('.[STDOUT/STDERR STREAM]\n')
                    for line in output_buffer.splitlines():
                        f.write('.{}\n'.format(line))

                    f.write('\n')
                f.write('END\n')
                f.close()
            f = open(env['PDK_LOG'], 'r')
            f.seek(end_of_log, 0)
            while 1:
                l = f.readline()
                if l == '':
                    break
                l = l.strip()
                if l.startswith('status='):
                    l = l[7:].strip()
                    stat_summary[l] = stat_summary.get(l, 0) + 1

            f.close()
            common.print_stat_dict(stat_summary)
            print('')
            if summary_file:
                f = open(summary_file, 'a')
                for x in stat_summary:
                    f.write('%s=%s\n' % (x, stat_summary[x]))

                f.write('.file=%s\n' % full_filename)
                f.write('START\n\n')
                f.close()
        else:
            print('NO RUNNER FOR %s\n' % (dirname + '/' + basename))
    os.chdir(save_dir)
    pdkrun_status('')
    return (
     return_status, stat_summary)


if windows:
    pass
else:

    def unix_preexec():
        os.setpgrp()


    timeout_proc = None
    timeout_proc_kills = 0
    timeout_duration = None

    class timeout_not_going_away:
        pass


    def proc_timeout_start(timeout, p):
        global timeout_duration
        global timeout_proc
        global timeout_proc_kills
        timeout_proc = p
        timeout_proc_kills = 0
        timeout_duration = timeout
        signal.signal(signal.SIGALRM, proc_timeout_callback)
        signal.alarm(int(timeout))


    def killpg_maybe(pid, signal):
        print('killpg -%d %d' % (signal, pid))
        try:
            os.killpg(pid, signal)
        except OSError as e:
            print('killpg exception: %s' % e)
            if e.errno != errno.ESRCH:
                raise


    def proc_timeout_callback(sig, stack):
        global timeout_proc_kills
        platform_id = platform.system()

        def top():
            if platform_id == 'Linux':
                os.system('top -b -n 1')
            elif platform_id == 'Darwin':
                os.system('top -n 25 -l1 -ncols 13')

        if timeout_proc:
            pid = timeout_proc.pid
            print('PID=%d' % pid)
            sys.stdout.flush()
            if timeout_proc_kills == 0:
                os.system('ps -fp %s' % pid)
                sys.stdout.flush()
                print('timeout expired - terminate after %s' % str(timeout_duration))
                sys.stdout.flush()
                top()
                sys.stdout.flush()
                os.system('ps -efl')
                sys.stdout.flush()
                os.system('sleep 5')
                sys.stdout.flush()
                os.system('ps -efl')
                sys.stdout.flush()
                killpg_maybe(pid, signal.SIGTERM)
                top()
                sys.stdout.flush()
            else:
                if timeout_proc_kills == 1:
                    print('timeout expired again - kill')
                    killpg_maybe(pid, signal.SIGKILL)
                else:
                    if timeout_proc_kills == 2:
                        print('timeout expired yet again - now what?')
                        raise timeout_not_going_away()
            timeout_proc_kills += 1
            signal.alarm(10)


    def proc_timeout_terminate():
        signal.alarm(0)
        timeout_proc = None