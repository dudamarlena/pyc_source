# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-8.9.0-Power_Macintosh/egg/pudge/test/test_cli.py
# Compiled at: 2006-03-14 16:35:23
"""Pudge Command Line Interface Tests"""
import getopt, pudge.cli as cli
from pudge.generator import Generator

def test_bad_arguments():
    command = cli.PudgeCommand('pudge', ['-XX'])
    try:
        command.parse_arguments()
    except getopt.GetoptError, e:
        pass
    else:
        assert 0, 'PudgeCommand.parse_arguments() should have raised an exception.'


def test_usage():
    command = cli.PudgeCommand('pudge', ['-h'])
    call = command.parse_arguments()
    assert not isinstance(call, Generator)


def test_short_args():
    args = [
     '-f', '-x', '-d', '/test/dest', '-t', '/test/templates', '-m', 'pudge']
    command = cli.PudgeCommand('pudge', args)
    call = command.parse_arguments()
    assert isinstance(call, Generator)
    assert call.force
    assert call.xhtml
    assert call.dest == '/test/dest'
    assert call.template_dir == '/test/templates'
    assert call.modules == ['pudge']


def test_long_args():
    args = [
     '--force', '--xhtml', '--dest=/test/dest', '--templates=/test/templates', '--modules=pudge']
    command = cli.PudgeCommand('pudge', args)
    call = command.parse_arguments()
    assert isinstance(call, Generator)
    assert call.force
    assert call.xhtml
    assert call.dest == '/test/dest'
    assert call.template_dir == '/test/templates'
    assert call.modules == ['pudge']