# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-x86_64/egg/graphterm/bin/landslide/parser.py
# Compiled at: 2014-02-02 09:23:11
import re
SUPPORTED_FORMATS = {'markdown': [
              '.mdown', '.markdown', '.markdn', '.md', '.mdn'], 
   'restructuredtext': [
                      '.rst', '.rest'], 
   'textile': [
             '.textile']}

class Parser(object):
    """This class generates the HTML code depending on which syntax is used in
       the souce document.

       The Parser currently supports both Markdown and restructuredText
       syntaxes.
    """
    RST_REPLACEMENTS = [
     (
      '<div.*?>', '', re.UNICODE),
     (
      '</div>', '', re.UNICODE),
     (
      '<p class="system-message-\\w+">.*?</p>', '', re.UNICODE),
     (
      'Document or section may not begin with a transition\\.',
      '', re.UNICODE),
     (
      '<h(\\d+?).*?>', '<h\\1>', re.DOTALL | re.UNICODE),
     (
      '<hr.*?>\\n', '<hr />\\n', re.DOTALL | re.UNICODE)]
    md_extensions = ''

    def __init__(self, extension, encoding='utf8', md_extensions=''):
        """Configures this parser.
        """
        self.encoding = encoding
        self.format = None
        for supp_format, supp_extensions in SUPPORTED_FORMATS.items():
            for supp_extension in supp_extensions:
                if supp_extension == extension:
                    self.format = supp_format

        if not self.format:
            raise NotImplementedError('Unsupported format %s' % extension)
        if md_extensions:
            exts = (value.strip() for value in md_extensions.split(','))
            self.md_extensions = filter(None, exts)
        return

    def parse(self, text):
        """Parses and renders a text as HTML regarding current format.
        """
        if self.format == 'markdown':
            try:
                import markdown
            except ImportError:
                raise RuntimeError('Looks like markdown is not installed')

            if text.startswith('\ufeff'):
                text = text[1:]
            return markdown.markdown(text, self.md_extensions)
        if self.format == 'restructuredtext':
            try:
                from rst import html_body
            except ImportError:
                raise RuntimeError('Looks like docutils are not installed')

            html = html_body(text, input_encoding=self.encoding)
            for pattern, replacement, mode in self.RST_REPLACEMENTS:
                html = re.sub(re.compile(pattern, mode), replacement, html, 0)

            return html.strip()
        if self.format == 'textile':
            try:
                import textile
            except ImportError:
                raise RuntimeError('Looks like textile is not installed')

            return textile.textile(text, encoding=self.encoding)
        raise NotImplementedError('Unsupported format %s, cannot parse' % self.format)