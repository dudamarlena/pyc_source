# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/unit/test_social_view.py
# Compiled at: 2017-02-24 16:57:38
"""Unittest for social login view."""
import pytest, mock
from pyramid.compat import text_type
from pyramid_fullauth.views.social import SocialLoginViews

@pytest.mark.parametrize('profile, email', [
 (
  {'accounts': [{'domain': text_type('facebook.com'), 'userid': text_type('2343')}], 'displayName': text_type('teddy'), 
     'verifiedEmail': text_type('verified@email.co.uk'), 
     'preferredUsername': text_type('teddy'), 
     'emails': [{'value': text_type('aasd@bwwqwe.pl')}], 'name': text_type('ted')},
  'verified@email.co.uk'),
 (
  {'accounts': [{'domain': text_type('facebook.com'), 'userid': text_type('2343')}], 'displayName': text_type('teddy'), 
     'preferredUsername': text_type('teddy'), 
     'emails': [{'value': text_type('aasd@bwwqwe.pl')}], 'name': text_type('ted')},
  'aasd@bwwqwe.pl'),
 (
  {'accounts': [{'domain': text_type('facebook.com'), 'userid': text_type('2343')}], 'displayName': text_type('teddy'), 
     'preferredUsername': text_type('teddy'), 
     'emails': [{}], 'name': text_type('ted')},
  '2343@facebook.com'),
 (
  {'accounts': [{'domain': text_type('facebook.com'), 'userid': text_type('2343')}], 'displayName': text_type('teddy'), 
     'preferredUsername': text_type('teddy'), 
     'emails': [], 'name': text_type('ted')},
  '2343@facebook.com'),
 (
  {'accounts': [{'domain': text_type('facebook.com'), 'userid': text_type('2343')}], 'displayName': text_type('teddy'), 
     'preferredUsername': text_type('teddy'), 
     'name': text_type('ted')},
  '2343@facebook.com')])
def test_email_from_context(profile, email):
    """Test email_from_context email getting method."""
    from velruse import AuthenticationComplete
    context = AuthenticationComplete(profile, {'oauthAccessToken': '7897048593434'}, text_type('facebook'), text_type('facebook'))
    view = SocialLoginViews(mock.MagicMock())
    assert view._email_from_context(context) == email