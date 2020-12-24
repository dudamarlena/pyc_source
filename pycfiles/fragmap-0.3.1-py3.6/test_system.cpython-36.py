# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\tests\test_system.py
# Compiled at: 2019-09-05 14:04:48
# Size of source mod 2**32: 612 bytes
import pytest, mock

def run(args):
    with mock.patch('sys.argv', [
     'dummypath/main.py'] + args):
        import fragmap.main
        fragmap.main.main()


def test_invalid_arg():
    with pytest.raises(SystemExit):
        run(['--notvalidarg=45654'])


def test_empty_arg():
    run([])


def test_arg_n():
    run(['-n', '2'])


def test_arg_s():
    run(['-s', 'HEAD~4'])


def test_r15():
    run(['-s', 'HEAD~15', '-u', 'HEAD~13'])


def test_no_color():
    run(['--no-color'])


def test_full():
    run(['--full'])


def test_n_no_color_full():
    run(['-n', '2', '--no-color', '--full'])