# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/tests/test_formats.py
# Compiled at: 2019-12-13 11:35:35
from six import StringIO
from insights import dr, make_fail, rule
from insights.formats.text import HumanReadableFormat
from insights.formats._yaml import YamlFormat
from insights.formats._json import JsonFormat
from insights.formats._syslog import SysLogFormat
from insights.formats.html import HtmlFormat
from insights.formats.simple_html import SimpleHtmlFormat
SL_MSG = 'Running insights.tests.test_formats.report'
SL_CMD = 'Command Line - '
SL_ARCHIVE = 'Real Archive Path - '
SL_PATH = '/insights/core'

@rule()
def report():
    return make_fail('ERROR', foo='bar')


def test_human_readable():
    broker = dr.Broker()
    output = StringIO()
    with HumanReadableFormat(broker, stream=output):
        dr.run(report, broker=broker)
    output.seek(0)
    data = output.read()
    assert 'foo' in data
    assert 'bar' in data


def test_json_format():
    broker = dr.Broker()
    output = StringIO()
    with JsonFormat(broker, stream=output):
        dr.run(report, broker=broker)
    output.seek(0)
    data = output.read()
    assert 'foo' in data
    assert 'bar' in data


def test_syslog_format_no_archive():
    broker = dr.Broker()
    output = StringIO()
    with SysLogFormat(broker, stream=output):
        dr.run(report, broker=broker)
    output.seek(0)
    data = output.read()
    assert SL_MSG in data
    assert SL_CMD in data


def test_syslog_format_archive():
    broker = dr.Broker()
    output = StringIO()
    with SysLogFormat(broker, archive='../../insights/core', stream=output):
        dr.run(report, broker=broker)
    output.seek(0)
    data = output.read()
    assert SL_MSG in data
    assert SL_CMD in data
    assert SL_ARCHIVE in data
    assert SL_PATH in data


def test_yaml_format():
    broker = dr.Broker()
    output = StringIO()
    with YamlFormat(broker, stream=output):
        dr.run(report, broker=broker)
    output.seek(0)
    data = output.read()
    assert 'foo' in data
    assert 'bar' in data


def test_html_format():
    broker = dr.Broker()
    output = StringIO()
    with HtmlFormat(broker, stream=output):
        dr.run(report, broker=broker)
    output.seek(0)
    data = output.read()
    assert 'foo' in data
    assert 'bar' in data


def test_simple_html_format():
    broker = dr.Broker()
    output = StringIO()
    with SimpleHtmlFormat(broker, stream=output):
        dr.run(report, broker=broker)
    output.seek(0)
    data = output.read()
    assert 'foo' in data
    assert 'bar' in data