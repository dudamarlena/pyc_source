# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/irk/util/proc.py
# Compiled at: 2018-06-20 22:05:50
# Size of source mod 2**32: 572 bytes
import subprocess, click, sys

def run(args, shell=False):
    proc = subprocess.Popen(args, shell=shell, stdout=(subprocess.PIPE), stderr=(subprocess.STDOUT), universal_newlines=True)
    all_stdout = ''
    while proc.poll() is None:
        new_content = proc.stdout.read(16)
        all_stdout += new_content
        print(new_content, end='')

    return (
     proc.returncode, all_stdout)


def elevate():
    arg_str = [
     '/usr/bin/env', 'sudo', *sys.argv]
    if click.confirm(f"Elevate with {' '.join(arg_str)}?"):
        exit(subprocess.run(arg_str).returncode)