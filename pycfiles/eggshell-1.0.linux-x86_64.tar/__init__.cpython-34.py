# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /xchip/cga_home/sfrazer/virtualenvs/redshirt2_test/lib/python3.4/site-packages/eggshell/__init__.py
# Compiled at: 2014-08-12 13:09:51
# Size of source mod 2**32: 377 bytes
import subprocess, io

def run(command, cwd=None):
    proc = subprocess.Popen(command, shell=True, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True, cwd=cwd)
    stdout, stderr = proc.communicate()
    return (proc.returncode, stdout.strip(' \n'), stderr.strip(' \n'))