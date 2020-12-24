# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/grmaster/tests/test_main.py
# Compiled at: 2015-05-28 11:03:40
# Size of source mod 2**32: 3123 bytes
"""Tests for `grmaster.__main__`."""
from grmaster import __main__
from grmaster import data
from pytest import raises

class FakeGrmasterHttpAPP:
    __doc__ = 'Do nothing.'

    def run(self, port=None):
        """We can except it."""
        raise NotImplementedError()


def test_printfile(tmpdir):
    """Test print from data dir."""
    output = tmpdir.join('template.csv')
    with open(str(output), 'w') as (output_file):
        __main__.printfile('template.csv', output_file)
    with open(str(output), 'r') as (output_file):
        result = output_file.readlines()
    with data.openfile('template.csv') as (template_file):
        template = template_file.readlines()
    assert result == template


def get_stdoutlines(tmpdir, *args):
    """Run main with fake output file."""
    output = tmpdir.join('usage.txt')
    with open(str(output), 'w') as (output_file):
        __main__.main(['grmaster'] + list(args), output_file, FakeGrmasterHttpAPP())
    with open(str(output), 'r') as (output_file):
        return output_file.readlines()


def test_usage(tmpdir):
    """Must print usage."""
    result = get_stdoutlines(tmpdir, 'usage')
    assert 'Usage' in result[0]
    assert 'grmaster' in result[0]
    assert len(result) > 1


def test_wrong_format(tmpdir):
    """Must print usage."""
    result = get_stdoutlines(tmpdir, 'wrong_format')
    assert 'Usage' in result[0]
    assert len(result) > 1


def test_license(tmpdir):
    """Must print license."""
    result = get_stdoutlines(tmpdir, 'license')
    license_txt = data.readlines('LICENSE.txt')
    assert result == license_txt


def test_template(tmpdir):
    """Main must print template."""
    result = get_stdoutlines(tmpdir, 'template')
    template_csv = data.readlines('template.csv')
    assert result == template_csv


def test_divide(tmpdir):
    """Main must divide."""
    students_file = tmpdir.join('students.csv')
    with open(str(students_file), 'w') as (students):
        students.writelines(data.readlines('students.csv'))
    result = get_stdoutlines(tmpdir, 'divide', str(students_file))
    assert result[0].strip('\n').split(',')[(-1)] == 'Group'
    assert len(result) > 10


def test_http(tmpdir):
    """Fake http module rase NotImplementedError."""
    with raises(NotImplementedError):
        get_stdoutlines(tmpdir, 'server')