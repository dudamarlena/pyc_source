# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/hugo/.virtualenvs/gitinspector/lib/python2.7/site-packages/gitinspector/basedir.py
# Compiled at: 2015-08-05 12:31:15
import os, subprocess, sys

def get_basedir():
    if hasattr(sys, 'frozen'):
        return sys.prefix
    else:
        return os.path.dirname(os.path.realpath(__file__))


__git_basedir__ = None

def get_basedir_git():
    global __git_basedir__
    if not __git_basedir__:
        sp = subprocess.Popen('git rev-parse --is-bare-repository', shell=True, bufsize=1, stdout=subprocess.PIPE, stderr=open(os.devnull, 'w'))
        isbare = sp.stdout.readlines()
        sp.wait()
        if sp.returncode != 0:
            sys.exit(_('Error processing git repository at "%s".' % os.getcwd()))
        isbare = isbare[0].decode('utf-8', 'replace').strip() == 'true'
        absolute_path = ''
        if isbare:
            absolute_path = subprocess.Popen('git rev-parse --git-dir', shell=True, bufsize=1, stdout=subprocess.PIPE).stdout
        else:
            absolute_path = subprocess.Popen('git rev-parse --show-toplevel', shell=True, bufsize=1, stdout=subprocess.PIPE).stdout
        absolute_path = absolute_path.readlines()
        if len(absolute_path) == 0:
            sys.exit(_('Unable to determine absolute path of git repository.'))
        __git_basedir__ = absolute_path[0].decode('utf-8', 'replace').strip()
    return __git_basedir__