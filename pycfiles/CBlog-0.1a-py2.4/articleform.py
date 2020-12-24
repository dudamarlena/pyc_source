# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/cblog/widgets/articleform.py
# Compiled at: 2006-12-15 15:46:36
__all__ = [
 'article_form', 'ArticleForm']
from turbogears import validators, url
from turbogears.widgets import *
from cblog.widgets.base import *
from cblog.widgets import jslibs
article_css = [
 CSSLink('cblog', 'css/articleform.css', media='screen')]
article_js = [jslibs.events, JSLink('cblog', 'javascript/articleform.js'), JSLink('cblog', 'javascript/forms.js')]

class ArticleForm(Form):
    __module__ = __name__
    template = '    <div xmlns:py="http://purl.org/kid/ns#" id="articleform_wrapper">\n      <div id="articlepreview" class="article"></div>\n\n      <form\n        name="${name}"\n        action="${action}"\n        method="${method}"\n        class="fieldsetform"\n        py:attrs="form_attrs">\n        <div py:for="field in hidden_fields"\n          py:replace="field.display(value_for(field), **params_for(field))"\n        />\n        <fieldset>\n          <legend>Post new article</legend>\n\n          <div py:for="i, field in enumerate(fields)"\n            class="${i%2 and \'odd\' or \'even\'}${error_for(field) and \' fielderror\' or \'\'}">\n            <label class="fieldlabel" for="${field.field_id}" py:content="callable(field.label) and field.label() or field.label" />\n            <span py:replace="field.display(value_for(field), **params_for(field))" />\n            <span py:if="error_for(field)" class="fielderror" py:content="error_for(field)" />\n            <div py:if="field.help_text" class="fieldhelp">\n              <div py:content="field.help_text" />\n            </div>\n          </div>\n\n        </fieldset>\n\n        <fieldset>\n          <legend>Add from your tags</legend>\n\n          <div id="taglist">\n            <p py:strip="True" py:for="tag, rank in tags">\n              <a class="tag rank${rank}" href="#">${tag}</a>,\n            </p>\n            <div CLASS="fieldhelp">\n              <div>Click on a tag to add it to the article.</div>\n            </div>\n          </div>\n        </fieldset>\n\n        <div class="buttonbox">\n          <p py:replace="submit.display(submit_text)" />\n        </div>\n      </form>\n    </div>\n    '
    submit = SubmitButton(attrs=dict(id='submit_article'))
    javascript = article_js
    css = article_css


class ArticleFormFields(WidgetsList):
    __module__ = __name__
    id = HiddenField('id')
    title = TextField('title', label=_('Title'), attrs=dict(maxlength=255), help_text=_('The title of your blog article - no formatting. Required'))
    text = TextArea('text', label=HelplinkLabel(_('Text'), linklabel=_('Formatting help'), url=lambda : url('/static/rest.html')), attrs=dict(maxlength=50000), help_text=_('The text of your blog article in ReST format. Required'), rows=15)
    tags = TextField('tags', label=_('Tags'), attrs=dict(maxlength=1024), help_text=_("A comma-separated list of tags. e.g. 'Web Design' counts as one tag 'Web, Design' as two. Optional"))


class ArticleFormSchema(validators.Schema):
    __module__ = __name__
    id = validators.Int(default=None)
    title = validators.UnicodeString(not_empty=True, max=255, strip=True)
    text = validators.UnicodeString(not_empty=True, max=50000, strip=True)
    tags = validators.UnicodeString(max=1024, strip=True)


article_form = ArticleForm(name='articleform', fields=ArticleFormFields(), validator=ArticleFormSchema())