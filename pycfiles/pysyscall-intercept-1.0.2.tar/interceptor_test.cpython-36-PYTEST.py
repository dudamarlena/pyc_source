# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/lukasz/projects/pysyscall_intercept/tests/package/pysyscall_intercept/interceptor_test.py
# Compiled at: 2018-11-10 11:01:42
# Size of source mod 2**32: 2584 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from hamcrest import *
from pysyscall_intercept import SysCallInterceptor, SYS_WRITE, SYS_OPEN

def test_intercept__no_return():

    class Handler(object):

        def __init__(self):
            self.count = 0

        def on_syscall(self):
            self.count += 1

    handler = Handler()
    with SysCallInterceptor(SYS_WRITE, handler.on_syscall):
        with open('/dev/null', 'w') as (f):
            f.write('test')
    assert_that(handler.count, is_(1))


def test_intercept__bool_return():

    class Handler(object):

        def __init__(self):
            self.count = 0

        def on_syscall(self):
            self.count += 1
            return False

    handler = Handler()
    with SysCallInterceptor(SYS_WRITE, handler.on_syscall):
        with open('/dev/null', 'w') as (f):
            f.write('test')
    assert_that(handler.count, is_(1))


def test_multiple_interceptors__same_syscall():
    with SysCallInterceptor(SYS_WRITE, lambda : _):
        interceptor2 = SysCallInterceptor(SYS_WRITE, lambda : _)
        assert_that(calling(interceptor2.__enter__), raises(RuntimeError))


def test_multiple_interceptors__different_syscalls():
    with SysCallInterceptor(SYS_WRITE, lambda : _):
        with SysCallInterceptor(SYS_OPEN, lambda : _):
            pass


def test_resuse_interceptor():

    class Handler(object):

        def __init__(self):
            self.count = 0

        def on_syscall(self):
            self.count += 1
            return False

    handler = Handler()
    with SysCallInterceptor(SYS_WRITE, handler.on_syscall):
        with open('/dev/null', 'w') as (f):
            f.write('test')
    with open('/dev/null', 'w') as (f):
        f.write('test')
    with SysCallInterceptor(SYS_WRITE, handler.on_syscall):
        with open('/dev/null', 'w') as (f):
            f.write('test')
    assert_that(handler.count, is_(2))


def test_modify_intercepted_return():

    class Handler(object):

        def __init__(self, error_code):
            self.error_code = error_code

        def on_syscall(self):
            if self.error_code:
                error_code = self.error_code
                self.error_code = None
                return error_code
            else:
                return 0

    handler = Handler(-255)
    with SysCallInterceptor(SYS_WRITE, handler.on_syscall):
        with open('/dev/null', 'w') as (f):
            assert_that(calling(f.write).with_args('test'), raises(OSError))