# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/cblog/widgets/commentform.py
# Compiled at: 2006-12-15 15:47:01
__all__ = [
 'comment_form', 'CommentForm']
from turbogears import validators, url
from turbogears.widgets import *
import cElementTree as ET
from cblog.widgets.validators import SpamFilter
from cblog.widgets.base import *
from cblog.widgets import jslibs
comment_css = [
 CSSLink('cblog', 'css/commentform.css', media='screen')]
comment_js = [jslibs.events, JSLink('cblog', 'javascript/commentform.js'), JSLink('cblog', 'javascript/forms.js'),
 JSSource("document.write('<style>#commentform_wrapper {display: none;}</style>');", js_location.head)]

class CommentForm(ListForm):
    __module__ = __name__
    template = '    <div xmlns:py="http://purl.org/kid/ns#" id="commentform_wrapper">\n      <div id="commentpreview" class="comment"></div>\n      <form\n        name="${name}"\n        action="${action}"\n        method="${method}"\n        class="fieldsetform"\n        py:attrs="form_attrs">\n        <div py:for="field in hidden_fields"\n          py:replace="field.display(value_for(field), **params_for(field))"\n        />\n\n        <fieldset>\n          <legend>Add new comment</legend>\n\n          <div py:for="i, field in enumerate(fields)"\n            class="${i%2 and \'odd\' or \'even\'}${error_for(field) and \' fielderror\' or \'\'}">\n            <label class="fieldlabel" for="${field.field_id}" py:content="callable(field.label) and field.label() or field.label" />\n            <span py:replace="field.display(value_for(field), **params_for(field))" />\n            <span py:if="error_for(field)" class="fielderror" py:content="error_for(field)" />\n            <div py:if="field.help_text" class="fieldhelp">\n              <div py:content="field.help_text" />\n            </div>\n          </div>\n\n        </fieldset>\n\n        <div class="buttonbox">\n          <p py:replace="submit.display(submit_text)" />\n        </div>\n      </form>\n    </div>\n    '
    submit = SubmitButton(attrs=dict(id='submit_comment'))
    javascript = comment_js
    css = comment_css


class CommentFormFields(WidgetsList):
    __module__ = __name__
    id = HiddenField('id')
    name = TextField('name', label=_('Name'), attrs=dict(maxlength=50), help_text=_('Your name - will be displayed with your comment. Required'))
    email = TextField('email', label=_('Email'), attrs=dict(maxlength=255), help_text=_('Your email address - will not be displayed. Required'))
    homepage = TextField('homepage', label=_('Website'), attrs=dict(maxlength=255), help_text=_('Your homepage URL - your name will link to this. Optional'))
    comment = TextArea('comment', label=HelplinkLabel(_('Comment'), linklabel=_('Formatting help'), url=lambda : url('/static/textile.html')), help_text=_('Your comment - textile syntax, 1000 chars max. Required'), rows=7)


class CommentFormSchema(validators.Schema):
    __module__ = __name__
    id = validators.Int(not_empty=True)
    name = validators.UnicodeString(not_empty=True, max=50, strip=True)
    email = validators.Email(not_empty=True, max=255, strip=True)
    homepage = validators.All(validators.UnicodeString(max=255, strip=True), validators.URL(add_http=True))
    comment = validators.UnicodeString(not_empty=True, max=1000)
    chained_validators = [SpamFilter()]


comment_form = CommentForm(name='commentform', fields=CommentFormFields(), validator=CommentFormSchema())