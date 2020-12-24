# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/main.py
# Compiled at: 2013-11-20 06:12:43
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
        cmd.append('--cov=pymills')
        cmd.append('--cov-report=html')
    cmd.append(dirname(abspath(__file__)))
    raise SystemExit(Popen(cmd, stdout=sys.stdout, stderr=STDOUT).wait())


if __name__ == '__main__':
    main()