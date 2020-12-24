# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/tests/test_regressions.py
# Compiled at: 2007-06-10 18:57:30
from mkcode import *
from mkcode.console import mk_withexc
trivial_mk = path('tests/trivialmkfile.py')
assert trivial_mk.exists()

def test_run_default_command():
    run_mk('egg_info')


def test_run_setup_command_by_namespace():
    run_mk('setup.egg_info')


def test_run_setup_command_with_args():
    run_mk('egg_info', '--help')


def test_run_setup_command_with_bad_args():
    try:
        run_mk('egg_info', '--blah')
    except SystemExit:
        pass


def test_run_mkfile_from_cli():
    mk_withexc('-f', trivial_mk.abspath(), 'hello')


def test_list_all_tasks():
    try:
        mk_withexc('-f', trivial_mk.abspath(), '-T')
    except SystemExit:
        pass


def test_shell_command():
    assert shell('echo') == 0
    assert shell('echo', '1', '2', '3') == 0