# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/nori/nori-test.py
# Compiled at: 2013-11-20 14:16:07
from pprint import pprint as pp
import sys, os, shlex, subprocess, time, socket
sys.path.insert(0, os.path.dirname(__file__) + os.path.sep + '..')
import nori

def run_mode_hook():
    pass


nori.core.task_article = 'a'
nori.core.task_name = 'test'
nori.core.tasks_name = 'tests'
nori.run_mode_hooks.append(run_mode_hook)
nori.process_command_line()