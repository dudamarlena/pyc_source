# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/shuyucms/generic/defaults.py
# Compiled at: 2016-05-20 23:26:47
from __future__ import unicode_literals
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from shuyucms.conf import register_setting
generic_comments = getattr(settings, b'COMMENTS_APP', b'') == b'shuyucms.generic'
if generic_comments:
    register_setting(name=b'COMMENTS_ACCOUNT_REQUIRED', label=_(b'Accounts required for commenting'), description=_(b'If ``True``, users must log in to comment.'), editable=True, default=False)
    register_setting(name=b'COMMENTS_DEFAULT_APPROVED', label=_(b'Auto-approve comments'), description=_(b'If ``True``, built-in comments are approved by default.'), editable=True, default=True)
    register_setting(name=b'COMMENT_FILTER', description=_(b"Dotted path to the function to call on a comment's value before it is rendered to the template."), editable=False, default=None)
    register_setting(name=b'COMMENTS_NOTIFICATION_EMAILS', label=_(b'Comment notification email addresses'), description=_(b'A comma separated list of email addresses that will receive an email notification each time a new comment is posted on the site.'), editable=False, default=b'')
    register_setting(name=b'COMMENTS_NUM_LATEST', label=_(b'Admin comments'), description=_(b'Number of latest comments shown in the admin dashboard.'), editable=True, default=20)
    register_setting(name=b'COMMENTS_REMOVED_VISIBLE', label=_(b'Show removed comments'), description=_(b'If ``True``, comments that have ``removed`` checked will still be displayed, but replaced with a ``removed`` message.'), editable=True, default=False)