# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/forums/markup/markdown.py
# Compiled at: 2020-03-30 17:48:04
# Size of source mod 2**32: 1273 bytes
import tendenci.apps.theme.templatetags.static as static
from markdown import Markdown
import bleach
from django.forms import Textarea
from django.template.loader import get_template
from markup.base import smile_it, BaseParser

class MarkdownWidget(Textarea):

    class Media:
        css = {'all': (
                 static('markitup/skins/simple/style.css'),
                 static('markitup/sets/markdown/style.css'))}
        js = (
         static('markitup/ajax_csrf.js'),
         static('markitup/jquery.markitup.js'),
         static('markitup/sets/markdown/set.js'),
         static('pybb/js/markitup.js'))

    def render(self, *args, **kwargs):
        tpl = get_template('pybb/markup/markdown_widget.html')
        ctx = {'widget_output': (super(MarkdownWidget, self).render)(*args, **kwargs)}
        return tpl.render(context=ctx)


class MarkdownParser(BaseParser):
    widget_class = MarkdownWidget

    def __init__(self):
        self._parser = Markdown()

    def format(self, text):
        return smile_it(self._parser.convert(bleach.clean(text)))

    def quote(self, text, username=''):
        return '>' + text.replace('\n', '\n>').replace('\r', '\n>') + '\n'