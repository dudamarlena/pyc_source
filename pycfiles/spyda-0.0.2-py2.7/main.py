# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-x86_64/egg/tests/main.py
# Compiled at: 2013-11-18 22:39:53
import sys
from types import ModuleType
from os.path import abspath, dirname
from subprocess import Popen, STDOUT

def importable(module):
    try:
        m = __import__(module, globals(), locals())
        return type(m) is ModuleType
    except ImportError:
        return False


def main():
    cmd = [
     'py.test', '-s', '-r', 'fsxXE', '--ignore=tmp', '--durations=10']
    if importable('pytest_cov'):
        cmd.append('--cov=spyda')
        cmd.append('--cov-report=html')
    cmd.append(dirname(abspath(__file__)))
    raise SystemExit(Popen(cmd, stdout=sys.stdout, stderr=STDOUT).wait())


if __name__ == '__main__':
    main()