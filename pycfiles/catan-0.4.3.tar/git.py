# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/catalyze/git.py
# Compiled at: 2014-12-18 14:20:18
import subprocess

def remote_list():
    return subprocess.check_output(['git', 'remote']).split('\n')


def remote_add(name, url):
    subprocess.check_call(['git', 'remote', 'add', name, url])


def remote_remove(name):
    subprocess.check_call(['git', 'remote', 'remove', name])