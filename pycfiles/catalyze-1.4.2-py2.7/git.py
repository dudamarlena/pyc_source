# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/catalyze/git.py
# Compiled at: 2014-12-18 14:20:18
import subprocess

def remote_list():
    return subprocess.check_output(['git', 'remote']).split('\n')


def remote_add(name, url):
    subprocess.check_call(['git', 'remote', 'add', name, url])


def remote_remove(name):
    subprocess.check_call(['git', 'remote', 'remove', name])