# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/grmaster/tests/test_server.py
# Compiled at: 2015-05-28 11:03:40
# Size of source mod 2**32: 1699 bytes
"""Tests for `grmaster.http`."""
from grmaster import server, data, setting
import pytest

@pytest.fixture
def app():
    """Fixture for easy testing."""
    return server.APP.test_client()


def test_index(app):
    """Index must return static index html."""
    assert data.readbytes('index.' + setting.LANG + '.html') == app.get('/').data


def test_template(app):
    """Template must return static template csv."""
    assert data.readbytes('template.csv') == app.get('/template.csv').data


def test_result(app):
    """Result must return anything."""
    assert app.post('/result.csv').status_code == 400
    with data.openfile('students.csv', 'rb') as (studentfile):
        response = app.post('/result.csv', data=dict(studentfile=(studentfile, 'students.csv')))
        assert response.status_code == 200
        assert response.mimetype == 'text/csv'