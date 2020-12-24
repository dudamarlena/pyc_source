# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/rbnotefield/extension.py
# Compiled at: 2014-09-03 18:40:39
from django.utils.translation import ugettext_lazy as _
from reviewboard.extensions.base import Extension
from reviewboard.extensions.hooks import ReviewRequestFieldsHook
from reviewboard.reviews.fields import BaseTextAreaField

class NoteField(BaseTextAreaField):
    field_id = 'beanbag_notefield_notes'
    label = _('Note to Reviewers')
    enable_markdown = True

    def render_change_entry_html(self, info):
        if 'old' in info and info['old'][0] is None:
            info['old'] = [
             '']
        if 'new' in info and info['new'][0] is None:
            info['new'] = [
             '']
        return super(NoteField, self).render_change_entry_html(info)


class NoteFieldExtension(Extension):
    metadata = {'Name': _('Note to Reviewers'), 
       'Summary': _('Add a "Note to Reviewers" field to review requests, for any special instructions not suitable for the Description field.')}

    def initialize(self):
        ReviewRequestFieldsHook(self, 'main', [NoteField])