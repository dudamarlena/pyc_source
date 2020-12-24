# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/aam/reader/markdown.py
# Compiled at: 2014-06-05 07:01:35
import re, mistune
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name

class MyRenderer(mistune.Renderer):

    def block_code(self, code, language):
        if language:
            lexer = get_lexer_by_name(language, stripall=True)
        else:
            return '<pre><code>%s</code></pre>' % code.strip()
        formatter = HtmlFormatter(noclasses=False, linenos=False)
        return '<div class="highlight-pre">%s</div>' % highlight(code, lexer, formatter)

    def autolink(self, link, is_email):
        if is_email:
            mailto = ('').join([ '&#%d;' % ord(letter) for letter in 'mailto:' ])
            email = ('').join([ '&#%d;' % ord(letter) for letter in link ])
            url = mailto + email
            return '<a href="%(url)s">%(link)s</a>' % {'url': url, 'link': email}
        title = link.replace('http://', '').replace('https://', '')
        if len(title) > 30:
            title = title[:24] + '...'
        return '<a href="%s">%s</a>' % (link, title)