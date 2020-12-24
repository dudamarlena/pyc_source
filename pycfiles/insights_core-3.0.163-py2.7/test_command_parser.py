# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/tests/test_command_parser.py
# Compiled at: 2020-03-25 13:10:41
import sys
from insights import get_nvr
from insights.command_parser import InsightsCli
import pytest
from mock import patch
VERSION_OUT = get_nvr() + '\n'

def test_insights_cli_version(capsys):
    test_args_list = [
     [
      'insights', 'version'],
     [
      'insights', '--version'],
     [
      'insights', 'cat', '--version'],
     [
      'insights', 'collect', '--version'],
     [
      'insights', 'inspect', '--version'],
     [
      'insights', 'info', '--version'],
     [
      'insights', 'ocpshell', '--version'],
     [
      'insights', 'run', '--version']]
    for args in test_args_list:
        with patch.object(sys, 'argv', args):
            with pytest.raises(SystemExit):
                InsightsCli()
            out, err = capsys.readouterr()
            assert err == ''
            assert out == VERSION_OUT


def test_insights_cli_version_bad_arg(capsys):
    test_args = ['insights', '-v']
    with patch.object(sys, 'argv', test_args):
        with pytest.raises(SystemExit):
            InsightsCli()
        out, err = capsys.readouterr()
        assert len(err) > 0
        assert out == ''