# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/unit/test_tools.py
# Compiled at: 2017-02-24 16:57:38
"""Test fullauth's tools."""
import pytest
from pyramid_fullauth.tools import validate_passsword, password_generator
from pyramid_fullauth.exceptions import EmptyError, ShortPasswordError, PasswordConfirmMismatchError

@pytest.mark.parametrize(('password', 'exception'), [
 (
  '', EmptyError),
 (
  '1234', ShortPasswordError),
 (
  '123456789', PasswordConfirmMismatchError)])
def test_raises_errors(web_request, password, exception):
    """Test validate_passsword possible exceptions."""
    with pytest.raises(exception):
        validate_passsword(web_request, password)


@pytest.mark.parametrize('length', [5, 6])
def test_password_generator(length):
    """Test password_generator generating proper length of a random password."""
    assert len(password_generator(length)) == length