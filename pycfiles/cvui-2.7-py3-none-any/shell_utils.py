# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/cvu/shell_utils.py
# Compiled at: 2014-06-27 13:46:31
from utils import CVUError

def sh_cmd(cmd):
    import subprocess, os
    with open(os.devnull, 'wb') as (devnull):
        try:
            subprocess.check_call(cmd, shell=True)
        except subprocess.CalledProcessError as e:
            raise CVUError(str(e))


def sh_cmd_grep(cmd, grep):
    import subprocess, os, random, time, tempfile
    t = random.randint(1, 10000000)
    try:
        os.mkdir(os.path.join(tempfile.gettempdir(), 'cvu'))
    except OSError:
        pass

    fname = os.path.join(tempfile.gettempdir(), 'out_fifo_%s' % str(t))
    try:
        os.unlink(fname)
    except:
        pass

    retln = []
    os.mkfifo(fname)
    try:
        fifo = os.fdopen(os.open(fname, os.O_RDONLY | os.O_NONBLOCK))
        newcmd = '( %s ) 1>%s' % (cmd, fname)
        process = subprocess.Popen(newcmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        while process.returncode == None:
            time.sleep(0.5)
            process.poll()
            try:
                ln = fifo.readline().strip()
            except:
                continue

            if ln and grep in ln:
                retln.append(ln)

        rem = fifo.read()
        if rem:
            for ln in [ ln for ln in rem.split('\n') if ln.strip() ]:
                if grep in ln:
                    retln.append(ln)

        if process.returncode:
            raise CVUError('%s failed with error code %s' % (
             cmd, process.returncode))
    finally:
        try:
            os.unlink(fname)
        except:
            pass

        return retln


def sh_cmd_retproc(cmd, debug=False):
    import subprocess, os
    with open(os.devnull, 'wb') as (devnull):
        outfd = None if debug else devnull
        process = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=outfd, stderr=outfd)
        if process.poll():
            process.kill()
            raise CVUError('% failed with error code %s' % (
             cmd, process.returncode))
        return process
    return


def tcsh_env_interpreter(source_fname):
    import subprocess, os
    cmd = [
     'tcsh', '-c', 'source %s && env' % source_fname]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=False)
    for ln in proc.stdout:
        ln = ln.strip()
        k, _, v = ln.partition('=')
        os.environ[k] = v