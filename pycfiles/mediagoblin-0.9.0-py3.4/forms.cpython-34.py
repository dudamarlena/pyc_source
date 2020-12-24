# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mediagoblin/user_pages/forms.py
# Compiled at: 2016-02-04 13:34:40
# Size of source mod 2**32: 2652 bytes
import wtforms
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from mediagoblin.tools.translate import lazy_pass_to_ugettext as _

class MediaCommentForm(wtforms.Form):
    comment_content = wtforms.TextAreaField(_('Comment'), [
     wtforms.validators.InputRequired()], description=_('You can use <a href="http://daringfireball.net/projects/markdown/basics" target="_blank">Markdown</a> for formatting.'))


class ConfirmDeleteForm(wtforms.Form):
    confirm = wtforms.BooleanField(_('I am sure I want to delete this'))


class ConfirmCollectionItemRemoveForm(wtforms.Form):
    confirm = wtforms.BooleanField(_('I am sure I want to remove this item from the collection'))


class MediaCollectForm(wtforms.Form):
    collection = QuerySelectField(_('Collection'), allow_blank=True, blank_text=_('-- Select --'), get_label='title')
    note = wtforms.TextAreaField(_('Include a note'), [
     wtforms.validators.Optional()])
    collection_title = wtforms.StringField(_('Title'), [
     wtforms.validators.Length(min=0, max=500)])
    collection_description = wtforms.TextAreaField(_('Description of this collection'), description=_('You can use\n                      <a href="http://daringfireball.net/projects/markdown/basics" target="_blank">\n                      Markdown</a> for formatting.'))


class CommentReportForm(wtforms.Form):
    report_reason = wtforms.TextAreaField(_('Reason for Reporting'), [
     wtforms.validators.InputRequired()])
    reporter_id = wtforms.HiddenField('')


class MediaReportForm(wtforms.Form):
    report_reason = wtforms.TextAreaField(_('Reason for Reporting'), [
     wtforms.validators.InputRequired()])
    reporter_id = wtforms.HiddenField('')