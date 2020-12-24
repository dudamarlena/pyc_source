# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\test\test_socketsays.py
# Compiled at: 2020-04-19 23:40:10
# Size of source mod 2**32: 978 bytes
import pytest
from socket_says.socket_says import SocketSays

@pytest.fixture()
def test_socket():
    simon = SocketSays('127.0.0.1', 7357)
    yield simon


def test_says(test_socket: SocketSays, capsys):
    errors = None
    try:
        test_socket.says('Test\n        test\n        test ')
    except ConnectionRefusedError:
        errors = True
    else:
        assert errors is None


def test_change_address(test_socket: SocketSays):
    assert str(test_socket.address) == '127.0.0.1'
    test_socket.address = '10.10.2.20'
    assert str(test_socket.address) == '10.10.2.20'


def test_change_port(test_socket: SocketSays):
    assert test_socket.port == 7357
    test_socket.port = 80
    assert test_socket.port == 80


@pytest.mark.xfail
def test_bad_changes(test_socket: SocketSays):
    test_socket.address = '192,43:etc'
    test_socket.port = 'gatsby'