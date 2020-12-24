# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_hammer_ping.py
# Compiled at: 2019-12-13 11:35:46
from insights.parsers.hammer_ping import HammerPing
from insights.tests import context_wrap
HAMMERPING_ERR_1 = '\nError: Connection refused - connect(2) for "localhost" port 443\n'
HAMMERPING_ERR_2 = "\nCould not load the API description from the server\n - is the server down?\n - was 'foreman-rake apipie:cache' run on the server when using apipie cache? (typical production settings)\nWarning: An error occured while loading module hammer_cli_csv\nCould not load the API description from the server\n - is the server down?\n - was 'foreman-rake apipie:cache' run on the server when using apipie cache? (typical production settings)\nWarning: An error occured while loading module hammer_cli_foreman\n"
HAMMERPING_OK_1 = '\ncandlepin:\n    Status:          ok\n    Server Response: Duration: 61ms\ncandlepin_auth:\n    Status:          ok\n'
HAMMERPING_OK = ('\ncandlepin:\n    Status:          ok\n    Server Response: Duration: 61ms\ncandlepin_auth:\n    Status:          ok\n    Server Response: Duration: 61ms\npulp:\n    Status:          ok\n    Server Response: Duration: 61ms\npulp_auth:\n    Status:          ok\n    Server Response: Duration: 61ms\nelasticsearch:\n    Status:          ok\n    Server Response: Duration: 35ms\nforeman_tasks:\n    Status:          ok\n    server Response: Duration: 1ms\n').strip()
HAMMERPING_COMMAND = ('\nCOMMAND> hammer ping\n\ncandlepin:\n    Status:          ok\n    Server Response: Duration: 20ms\ncandlepin_auth:\n    Status:          ok\n    Server Response: Duration: 14ms\npulp:\n    Status:          ok\n    Server Response: Duration: 101ms\npulp_auth:\n    Status:          ok\n    Server Response: Duration: 75ms\nforeman_tasks:\n    Status:          ok\n    Server Response: Duration: 3ms\n\n').strip()
HAMMERPING = ('\ncandlepin:\n    Status:          FAIL\n    Server Response:Message:404 Resource Not Found\ncandlepin_auth:\n    Status:          FAIL\n    Server Response: Message: Katello::Resources::Candlepin::CandlepinPing: 404 Resource Not Found\npulp:\n    Status:          ok\n    Server Response: Duration: 61ms\npulp_auth:\n    Status:\n    Server Response:\nelasticsearch:\n    Status:          ok\n    Server Response: Duration: 35ms\nforeman_tasks:\n    Status:          ok\n    server Response: Duration: 1ms\n').strip()
HAMMERPING_FAIL = ('\ncandlepin:\n    Status:          ok\n    Server Response:\ncandlepin_auth:\n    Status:          ok\n    Server Response:\npulp:\n    Status:          FAIL\n    Server Response:\npulp_auth:\n    Status: FAIL\nforeman_tasks:\n    Status:          ok\n    Server Response: Duration: 28ms\n').strip()

def test_hammer_ping_err_1():
    status = HammerPing(context_wrap(HAMMERPING_ERR_1))
    assert not status.are_all_ok
    assert status.errors != []


def test_hammer_ping_err_2():
    status = HammerPing(context_wrap(HAMMERPING_ERR_2))
    assert not status.are_all_ok
    assert status.errors != []


def test_hammer_ping_err_3():
    status = HammerPing(context_wrap(HAMMERPING_OK_1))
    assert status.are_all_ok
    assert status.errors == []


def test_hammer_ping_ok():
    status = HammerPing(context_wrap(HAMMERPING_OK))
    assert status.are_all_ok
    assert status.service_list == [
     'candlepin', 'candlepin_auth', 'elasticsearch', 'foreman_tasks', 'pulp', 'pulp_auth']
    assert status.services_of_status('FAIL') == []
    assert 'nonexistent' not in status.service_list


def test_hammer_ping_command():
    status = HammerPing(context_wrap(HAMMERPING_COMMAND))
    assert status.are_all_ok
    assert status.service_list == [
     'candlepin', 'candlepin_auth', 'foreman_tasks', 'pulp', 'pulp_auth']
    assert status.services_of_status('FAIL') == []
    assert 'nonexistent' not in status.service_list


def test_hammer_ping():
    status = HammerPing(context_wrap(HAMMERPING))
    assert not status.are_all_ok
    assert status.service_list == [
     'candlepin', 'candlepin_auth', 'elasticsearch', 'foreman_tasks',
     'pulp', 'pulp_auth']
    assert status.services_of_status('OK') == [
     'elasticsearch', 'foreman_tasks', 'pulp']
    assert status.services_of_status('FAIL') == [
     'candlepin', 'candlepin_auth']
    assert status['pulp_auth']['Status'] == ''
    assert status['candlepin']['Status'] == 'FAIL'
    assert status['elasticsearch']['Status'] == 'ok'
    assert status['pulp_auth']['Server Response'] == ''
    assert status['candlepin_auth']['Server Response'] == 'Message: Katello::Resources::Candlepin::CandlepinPing: 404 Resource Not Found'
    assert status['elasticsearch']['Server Response'] == 'Duration: 35ms'
    assert 'nonexistent' not in status.service_list
    assert 'nonexistent' not in status


def test_hammer_different_lines():
    status = HammerPing(context_wrap(HAMMERPING_FAIL))
    assert status.services_of_status('FAIL') == [
     'pulp', 'pulp_auth']
    assert status.services_of_status('ok') == [
     'candlepin', 'candlepin_auth', 'foreman_tasks']


def test_status_and_response():
    status = HammerPing(context_wrap(HAMMERPING_FAIL))
    assert status.status_of_service['pulp'] == 'fail'
    assert status.status_of_service['foreman_tasks'] == 'ok'
    assert status.response_of_service['pulp'] == ''
    assert status.response_of_service['foreman_tasks'] == 'Duration: 28ms'


def test_raw_content():
    status = HammerPing(context_wrap(HAMMERPING_COMMAND))
    for line in HAMMERPING_COMMAND.splitlines():
        assert line in status.raw_content