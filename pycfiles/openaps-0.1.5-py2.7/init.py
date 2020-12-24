# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/openaps/init.py
# Compiled at: 2015-12-15 13:09:24
import os

def init(args):
    shell_cmd = [
     'git-openaps-init'] + args.args
    os.execvp(shell_cmd[0], shell_cmd)