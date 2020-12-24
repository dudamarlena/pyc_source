# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: python_build/build.py
# Compiled at: 2015-07-06 03:33:33
from os import path, chdir
from sys import stdout, stderr, exit, argv
from subprocess import call
PYTHONBUILD_DIR = path.dirname(path.realpath(__file__))

def python_build(*args):
    pyenv_build_bin = path.join(PYTHONBUILD_DIR, 'bin', 'python-build')
    call([pyenv_build_bin] + list(args))


def run():
    python_build(*argv[1:])