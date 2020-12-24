# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ml_markdown/utils/default_renderer.py
# Compiled at: 2017-02-18 13:57:54
# Size of source mod 2**32: 2361 bytes
"""
    Default renderer module
"""
from django.utils.text import slugify
from misaka import HtmlRenderer
from pygments import highlight
from pygments.lexers import get_lexer_by_name, get_lexer_for_filename, ClassNotFound
from pygments.formatters.html import HtmlFormatter

class DefaultRenderer(HtmlRenderer):
    __doc__ = '\n        Default Html renderer.\n        Provides:\n            * id attribute to h* tags (for readable anchor links in tables of contents)\n            * syntax highlighting with extra syntax for fenced code\n    '

    def header(self, content, level):
        """
            Parse headers

            :params content: That will be detween <h*> and </h*>
            :params level: The title level

            :return: a <h*> tag with slugified content as id
        """
        return '<h{n} id="{id}">{title}</h{n}>'.format(n=level, title=content, id=slugify(content))

    def blockcode(self, text, lang=''):
        """
            Generate a syntax highlighted blockcode

            :param text: the code
            :param lang: the language, can be a language name, a filename, or
                an association of the two (ex: djangohtml:template.html)

            :return: the syntax highlighted block code
        """
        formatter = HtmlFormatter(nowrap=True)
        output_template = '<div class="blockcode">{tab}<pre><code>{code}</code></pre></div>'
        tab_template = '<div class="blockcode-tab">{name}</div>'
        language = 'text'
        tab_name = ''
        if not lang:
            pass
        else:
            if ':' in lang:
                tmp = lang.split(':')
                language, tab_name = tmp[0], ':'.join(tmp[1:])
            else:
                if '.' in lang:
                    tab_name = lang
                    language = lang
                else:
                    language = lang
        try:
            lexer = get_lexer_by_name(language, stripall=True)
        except ClassNotFound:
            try:
                lexer = get_lexer_for_filename(language, stripall=True)
            except ClassNotFound:
                lexer = get_lexer_by_name('text')

        return output_template.format(tab=tab_template.format(name=tab_name) if tab_name else '', code=highlight(text, lexer, formatter))