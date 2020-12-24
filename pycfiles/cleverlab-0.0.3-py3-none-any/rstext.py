# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/harold/publishers/rstext.py
# Compiled at: 2006-08-02 05:57:50
from harold.publishers.common import default_helper, make_view, TemplateMixin
try:
    from docutils.core import publish_parts
except (ImportError,):

    def publish_parts(value, **kwds):
        return {'body': docutils_not_installed % (value,)}


docutils_not_installed = '\n<div>\n<h1>Docutils Not Installed - Rendering Not Available</h1>\n<p>Install docutils from\n<a href="http://docutils.sourceforge.net"/>http://docutils.sourceforge.net</a>.\n</p>\n<h2>Raw File Contents</h2>\n<pre>%s</pre>\n</div>\n'

class ReStructuredTextTemplate(TemplateMixin):
    """ Class to publish reStructuredText files

    """
    __module__ = __name__
    ext = '.txt'
    index = 'index.txt'

    def render(self, filename, args):
        """ renders contents of restructured text file

        @param filename name of file as found by the publisher
        @param args trailing path arguments if any
        @return rendered file as html
        """
        app = self.app
        text = open(filename).read()
        markup = publish_parts(text, writer_name='html')['html_body']
        helper_template = self.kwds.get('helper_template', default_helper)
        source = helper_template % (markup,)
        module = make_view(source, layout=app.layout, defaults=app.defaults, cache=not app.debug)
        output = self.kwds.get('output', 'html')
        context = self.context()()
        return module.serialize(output=output, **context)