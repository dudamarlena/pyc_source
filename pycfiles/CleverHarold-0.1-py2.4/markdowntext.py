# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/harold/publishers/markdowntext.py
# Compiled at: 2006-08-02 05:57:50
from harold.publishers.common import default_helper, make_view, TemplateMixin
try:
    from markdown import markdown
except (ImportError,):

    def markdown(value):
        return markdown_not_installed % (value,)


markdown_not_installed = '\n<div>\n<h1>Markdown Not Installed - Rendering Not Available</h1>\n<p>Install markdown.py from\n<a href="http://www.freewisdom.org/projects/python-markdown/">\nhttp://www.freewisdom.org/projects/python-markdown/\n</a>.\n</p>\n<h2>Raw File Contents</h2>\n<pre>%s</pre>\n</div>\n'

class MarkdownTemplate(TemplateMixin):
    """ Class to publish text files with Markdown markup

    """
    __module__ = __name__
    ext = '.txt'
    index = 'index.txt'

    def render(self, filename, args):
        """ renders contents of Markdown text file

        @param filename name of file as found by the publisher
        @param args trailing path arguments if any
        @return rendered file as html
        """
        app = self.app
        text = open(filename).read()
        markup = markdown(text)
        helper_template = self.kwds.get('helper_template', default_helper)
        source = helper_template % (markup,)
        module = make_view(source, layout=app.layout, defaults=app.defaults, cache=not app.debug)
        output = self.kwds.get('output', 'html')
        context = self.context()()
        return module.serialize(output=output, **context)