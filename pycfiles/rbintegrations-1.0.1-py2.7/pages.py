# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/rbintegrations/idonethis/pages.py
# Compiled at: 2020-01-07 04:31:42
"""Pages for I Done This integration."""
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from reviewboard.accounts.pages import AccountPage
from rbintegrations.idonethis.forms import IDoneThisIntegrationAccountPageForm

class IDoneThisIntegrationAccountPage(AccountPage):
    """User account page for I Done This."""
    page_id = b'idonethis_account_page'
    page_title = _(b'I Done This')
    form_classes = [IDoneThisIntegrationAccountPageForm]