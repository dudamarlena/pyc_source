# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/accounts/tests/test_user_infobox_view.py
# Compiled at: 2020-02-11 04:03:56
"""Unit tests for reviewboard.accounts.views.UserInfoboxView."""
from __future__ import unicode_literals
from django.contrib.auth.models import User
from reviewboard.site.urlresolvers import local_site_reverse
from reviewboard.testing import TestCase

class UserInfoboxViewTests(TestCase):
    """Unit tests for reviewboard.accounts.views.UserInfoboxView."""

    def test_unicode(self):
        """Testing UserInfoboxView with a user with non-ascii characters"""
        user = User.objects.create_user(b'test', b'test@example.com')
        user.first_name = b'Test↹'
        user.last_name = b'User✩'
        user.save()
        self.client.get(local_site_reverse(b'user-infobox', args=[b'test']))