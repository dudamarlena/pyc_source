# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/wmpy_util/sys_util.py
# Compiled at: 2019-01-03 00:44:36
# Size of source mod 2**32: 1492 bytes
import subprocess

def excute(cmd, cwd=None, verbose=False):
    if isinstance(cmd, str):
        if verbose:
            print(cmd)
        run = subprocess.Popen(cmd, shell=True, stdout=(subprocess.PIPE), stderr=(subprocess.PIPE), cwd=cwd)
    else:
        if isinstance(cmd, list):
            cmd = [str(unit) for unit in cmd]
            if verbose:
                print(' '.join(cmd))
            run = subprocess.Popen(cmd, stdout=(subprocess.PIPE), stderr=(subprocess.PIPE), cwd=cwd)
        else:
            return
    out = get_output_1(run, verbose)
    return out


def get_output(run, verbose):
    """ Display the output/error of a subprocess.Popen object
        if 'verbose' is True.
    """
    out = list()
    while run.poll() == None:
        line = run.stdout.readline().decode('UTF-8', 'ignore').strip()
        error_line = run.stderr.readline().decode('UTF-8', 'ignore').strip()
        if line:
            out.append(line)
            if verbose:
                print(line)
        if error_line and verbose:
            print(error_line)

    if run.returncode == 0:
        print('Subprogram success')
    else:
        print('Subprogram failed')
    return ''.join(out)


def get_output_1(run, verbose):
    out, err = run.communicate()
    out = out.decode('utf8', 'ignore')
    if verbose:
        print(out)
        if err:
            print(err.decode('utf8', 'ignore'))
    return out