# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/test_main.py
# Compiled at: 2013-12-08 17:19:04
import os, sys
from subprocess import Popen, PIPE
from mio.main import USAGE, VERSION
import main_wrapper
TEST_FILE = os.path.join(os.path.dirname(__file__), 'test.mio')

def test_help():
    p = Popen([sys.executable, main_wrapper.__file__, '--help'], stdout=PIPE)
    stdout = p.communicate()[0].strip()
    assert stdout == USAGE


def test_version():
    p = Popen([sys.executable, main_wrapper.__file__, '--version'], stdout=PIPE)
    stdout = p.communicate()[0].strip()
    assert stdout == VERSION


def test_eval():
    p = Popen([sys.executable, main_wrapper.__file__, '-e', 'print(1 + 2)'], stdout=PIPE)
    stdout = p.communicate()[0]
    assert stdout == '3\n'


def test_inspect():
    p = Popen([sys.executable, main_wrapper.__file__, '-i', TEST_FILE], stdin=PIPE, stdout=PIPE)
    stdout = p.communicate('exit()\n')[0]
    assert stdout.split()[0] == '3'


def test_repl():
    p = Popen([sys.executable, main_wrapper.__file__], stdin=PIPE, stdout=PIPE)
    stdout = p.communicate('print(1 + 2)\nexit()\n')[0]
    assert stdout.split()[3] == '3'


def test_repl_cont():
    p = Popen([sys.executable, main_wrapper.__file__], stdin=PIPE, stdout=PIPE)
    stdout = p.communicate('foo = block(\n    print("Hello World!")\n)')[0]
    lines = stdout.split()[3:]
    assert lines[0] == '....'
    assert lines[1] == '....'