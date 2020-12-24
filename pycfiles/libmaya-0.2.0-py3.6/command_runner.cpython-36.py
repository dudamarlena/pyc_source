# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/maya/exp_runner/command_runner.py
# Compiled at: 2019-06-13 05:22:46
# Size of source mod 2**32: 1341 bytes
"""
Created on Wed Dec 12 00:03:52 2018

"""
import subprocess, time, sys
from shutil import copyfile
import os, errno, shutil

def copy(src, dest):
    try:
        shutil.copytree(src, dest)
    except OSError as e:
        if e.errno == errno.ENOTDIR:
            shutil.copy(src, dest)
        else:
            print('Directory not copied. Error: %s' % e)


def run_command(command):
    result = []
    proc = subprocess.Popen(command, shell=True, stdout=(subprocess.PIPE))
    pid = proc.pid
    output = proc.stdout
    raw_report = output.readlines()
    for line in raw_report:
        result.append(line.decode('utf-8'))

    return result


def run_command_with_id(command_id, command):
    base_dir = os.path.abspath('./')
    dummy_path = '../' + str(command_id) + '/'
    if os.path.exists(dummy_path):
        shutil.rmtree(dummy_path)
    shutil.copytree('./', dummy_path)
    os.chdir(dummy_path)
    print('working in', dummy_path, command)
    result = run_command(command)
    os.chdir(base_dir)
    return result


if __name__ == '__main__':
    command = 'ls'
    result = run_command(command)