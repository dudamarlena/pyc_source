# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: titantools/nix.py
# Compiled at: 2014-06-16 15:46:58
from subprocess import Popen, PIPE, STDOUT

def execute_command(command):
    ps = Popen(command, shell=True, stdout=PIPE, stderr=STDOUT)
    output = ps.communicate()[0]
    return output