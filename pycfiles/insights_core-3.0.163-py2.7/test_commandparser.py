# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/tests/test_commandparser.py
# Compiled at: 2020-03-25 13:10:41
from insights.core import CommandParser
from insights.tests import context_wrap
from insights.core.plugins import ContentException
import pytest
CMF = 'blah: Command not found'
NO_FILES_FOUND = 'No files found for docker.service'
NO_SUCH_FILE = '/usr/bin/blah: No such file or directory'
MULTI_LINE = ('\nblah: Command not found\n/usr/bin/blah: No such file or directory\n').strip()
MULTI_LINE_BAD = ('\nMissing Dependencies:\n    At Least One Of:\n        insights.specs.default.DefaultSpecs.aws_instance_type\n        insights.specs.insights_archive.InsightsArchiveSpecs.aws_instance_type\n').strip()

class MockParser(CommandParser):

    def parse_content(self, content):
        self.data = content


def test_command_not_found():
    with pytest.raises(ContentException) as (e):
        MockParser(context_wrap(CMF))
    assert 'Command not found' in str(e.value)


def test_no_files_found():
    with pytest.raises(ContentException) as (e):
        MockParser(context_wrap(NO_FILES_FOUND))
    assert 'No files found for' in str(e.value)


def test_no_such_file_or_directory():
    with pytest.raises(ContentException) as (e):
        MockParser(context_wrap(NO_SUCH_FILE))
    assert 'No such file or directory' in str(e.value)


def test_multi_line():
    assert MULTI_LINE.split('\n') == MockParser(context_wrap(MULTI_LINE)).data


def test_multi_line_ng():
    with pytest.raises(ContentException) as (e):
        MockParser(context_wrap(MULTI_LINE_BAD))
    assert 'Missing Dependencies:' in str(e.value)