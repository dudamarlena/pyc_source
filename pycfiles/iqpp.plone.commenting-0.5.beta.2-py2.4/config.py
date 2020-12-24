# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-8.10.1-i386/egg/iqpp/plone/commenting/config.py
# Compiled at: 2007-10-06 06:19:54
from zope.i18nmessageid import MessageFactory
_ = MessageFactory('iqpp.plone.commenting')
GLOBALS = globals()
MESSAGES = {'comment-added': _('Your comment has been added.'), 'comment-added-moderated': _('Your entry has been received. However, it will not be published until it has been reviewed by the site owner.'), 'comment-published': _('Comment has been published.'), 'comment-not-published': _('Comment has not been published.'), 'comment-rejected': _('Comment has been rejected.'), 'comment-not-rejected': _('Comment has not been rejected.'), 'comments-deleted': _('All comments have been deleted.'), 'comment-deleted': _('Your comment has been deleted.'), 'comment-not-deleted': _("Your comment wasn't able to be deleted."), 'comment-modified': _('Your comment has been modified.'), 'comment-not-modified': _("Your comment wasn't able to be modified."), 'comment-added-subject': _('A new comment has been added'), 'options-saved': _('Your options has been saved')}
REVIEW_STATES = ('private', 'pending', 'published')
REVIEW_STATES_CHOICES = (
 (
  _('Default'), 'default'), (_('Private'), 'private'), (_('Pending'), 'pending'), (_('Published'), 'published'))
DEFAULT_CHOICES = (
 (
  _('Default'), 'default'), (_('Enabled'), True), (_('Disabled'), False))
ENCODING = 'utf-8'