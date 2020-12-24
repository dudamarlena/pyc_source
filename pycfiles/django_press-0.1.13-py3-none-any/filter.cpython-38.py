# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\yuuta\YCU-Programing\Code_Review\ura_1\django_press\templatetags\filter.py
# Compiled at: 2019-12-06 06:21:13
# Size of source mod 2**32: 1357 bytes
from django import template
from django.utils.safestring import mark_safe
import markdown
from markdownx.utils import markdownify
from markdownx.settings import MARKDOWNX_MARKDOWN_EXTENSIONS, MARKDOWNX_MARKDOWN_EXTENSION_CONFIGS
import re
from markdown.extensions import Extension
register = template.Library()

@register.inclusion_tag('django_press/filter/html.html', takes_context=True)
def markdown_to_html(context, core: dict, md):
    for key, value in core.items():
        md = re.sub('{{\\s*(core\\.' + key + ')\\s*}}', value, md)
    else:
        return {'content': mark_safe(markdownify(md))}


class EscapeHtml(Extension):

    def extendMarkdown(self, md):
        md.preprocessors.deregister('html_block')
        md.inlinePatterns.deregister('html')


@register.filter
def markdown_to_html_with_escape(text):
    """マークダウンをhtmlに変換する。

    生のHTMLやCSS、JavaScript等のコードをエスケープした上で、マークダウンをHTMLに変換します。
    公開しているコメント欄等には、こちらを使ってください。

    """
    extensions = MARKDOWNX_MARKDOWN_EXTENSIONS + [EscapeHtml()]
    html = markdown.markdown(text, extensions=extensions, extension_configs=MARKDOWNX_MARKDOWN_EXTENSION_CONFIGS)
    return mark_safe(html)