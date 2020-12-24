# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\Ofek\Desktop\code\privy\build\lib\tests\test_privy.py
# Compiled at: 2017-02-14 13:19:53
# Size of source mod 2**32: 2001 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, time, pytest, privy

def test_default():
    secret = b'secret'
    password = b'password'
    hidden = privy.hide(secret, password)
    @py_assert1 = privy.peek
    @py_assert5 = @py_assert1(hidden, password)
    @py_assert7 = @py_assert5 == secret
    if not @py_assert7:
        @py_format9 = @pytest_ar._call_reprcompare(('==',), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.peek\n}(%(py3)s, %(py4)s)\n} == %(py8)s',), (@py_assert5, secret)) % {'py3': @pytest_ar._saferepr(hidden) if 'hidden' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(hidden) else 'hidden', 'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(privy) if 'privy' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(privy) else 'privy', 'py6': @pytest_ar._saferepr(@py_assert5), 'py4': @pytest_ar._saferepr(password) if 'password' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(password) else 'password', 'py8': @pytest_ar._saferepr(secret) if 'secret' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(secret) else 'secret'}
        @py_format11 = ('' + 'assert %(py10)s') % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert5 = @py_assert7 = None


def test_security():
    secret = b'secret'
    password = b'password'
    hidden = privy.hide(secret, password, security=3)
    @py_assert1 = privy.peek
    @py_assert5 = @py_assert1(hidden, password)
    @py_assert7 = @py_assert5 == secret
    if not @py_assert7:
        @py_format9 = @pytest_ar._call_reprcompare(('==',), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.peek\n}(%(py3)s, %(py4)s)\n} == %(py8)s',), (@py_assert5, secret)) % {'py3': @pytest_ar._saferepr(hidden) if 'hidden' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(hidden) else 'hidden', 'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(privy) if 'privy' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(privy) else 'privy', 'py6': @pytest_ar._saferepr(@py_assert5), 'py4': @pytest_ar._saferepr(password) if 'password' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(password) else 'password', 'py8': @pytest_ar._saferepr(secret) if 'secret' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(secret) else 'secret'}
        @py_format11 = ('' + 'assert %(py10)s') % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert5 = @py_assert7 = None


def test_invalid_security():
    secret = b'secret'
    password = b'password'
    with pytest.raises(KeyError):
        privy.hide(secret, password, security=99)


def test_salt():
    secret = b'secret'
    password = b'password'
    hidden = privy.hide(secret, password, salt=b'bad_form')
    @py_assert1 = privy.peek
    @py_assert5 = @py_assert1(hidden, password)
    @py_assert7 = @py_assert5 == secret
    if not @py_assert7:
        @py_format9 = @pytest_ar._call_reprcompare(('==',), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.peek\n}(%(py3)s, %(py4)s)\n} == %(py8)s',), (@py_assert5, secret)) % {'py3': @pytest_ar._saferepr(hidden) if 'hidden' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(hidden) else 'hidden', 'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(privy) if 'privy' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(privy) else 'privy', 'py6': @pytest_ar._saferepr(@py_assert5), 'py4': @pytest_ar._saferepr(password) if 'password' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(password) else 'password', 'py8': @pytest_ar._saferepr(secret) if 'secret' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(secret) else 'secret'}
        @py_format11 = ('' + 'assert %(py10)s') % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert5 = @py_assert7 = None


def test_no_server():
    secret = b'secret'
    password = b'password'
    hidden = privy.hide(secret, password, server=False)
    @py_assert1 = privy.peek
    @py_assert5 = @py_assert1(hidden, password)
    @py_assert7 = @py_assert5 == secret
    if not @py_assert7:
        @py_format9 = @pytest_ar._call_reprcompare(('==',), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.peek\n}(%(py3)s, %(py4)s)\n} == %(py8)s',), (@py_assert5, secret)) % {'py3': @pytest_ar._saferepr(hidden) if 'hidden' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(hidden) else 'hidden', 'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(privy) if 'privy' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(privy) else 'privy', 'py6': @pytest_ar._saferepr(@py_assert5), 'py4': @pytest_ar._saferepr(password) if 'password' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(password) else 'password', 'py8': @pytest_ar._saferepr(secret) if 'secret' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(secret) else 'secret'}
        @py_format11 = ('' + 'assert %(py10)s') % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert5 = @py_assert7 = None


def test_unicode_password():
    secret = b'secret'
    password = 'password'
    hidden = privy.hide(secret, password)
    @py_assert1 = privy.peek
    @py_assert5 = @py_assert1(hidden, password)
    @py_assert7 = @py_assert5 == secret
    if not @py_assert7:
        @py_format9 = @pytest_ar._call_reprcompare(('==',), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.peek\n}(%(py3)s, %(py4)s)\n} == %(py8)s',), (@py_assert5, secret)) % {'py3': @pytest_ar._saferepr(hidden) if 'hidden' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(hidden) else 'hidden', 'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(privy) if 'privy' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(privy) else 'privy', 'py6': @pytest_ar._saferepr(@py_assert5), 'py4': @pytest_ar._saferepr(password) if 'password' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(password) else 'password', 'py8': @pytest_ar._saferepr(secret) if 'secret' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(secret) else 'secret'}
        @py_format11 = ('' + 'assert %(py10)s') % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert5 = @py_assert7 = None


def test_peek_non_unicode_hidden():
    secret = b'secret'
    password = b'password'
    hidden = privy.hide(secret, password).encode('utf-8')
    @py_assert1 = privy.peek
    @py_assert5 = @py_assert1(hidden, password)
    @py_assert7 = @py_assert5 == secret
    if not @py_assert7:
        @py_format9 = @pytest_ar._call_reprcompare(('==',), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.peek\n}(%(py3)s, %(py4)s)\n} == %(py8)s',), (@py_assert5, secret)) % {'py3': @pytest_ar._saferepr(hidden) if 'hidden' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(hidden) else 'hidden', 'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(privy) if 'privy' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(privy) else 'privy', 'py6': @pytest_ar._saferepr(@py_assert5), 'py4': @pytest_ar._saferepr(password) if 'password' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(password) else 'password', 'py8': @pytest_ar._saferepr(secret) if 'secret' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(secret) else 'secret'}
        @py_format11 = ('' + 'assert %(py10)s') % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert5 = @py_assert7 = None


def test_wrong_password():
    secret = b'secret'
    password = b'password'
    hidden = privy.hide(secret, password)
    with pytest.raises(ValueError):
        privy.peek(hidden, b'wrong')


def test_wrong_hidden_secret():
    secret = b'secret'
    password = b'password'
    hidden = privy.hide(secret, b'wrong')
    with pytest.raises(ValueError):
        privy.peek(hidden, password)


def test_expires():
    secret = b'secret'
    password = b'password'
    hidden = privy.hide(secret, password)
    time.sleep(2)
    with pytest.raises(ValueError):
        privy.peek(hidden, password, expires=1)