# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/apydia/renderers/base.py
# Compiled at: 2007-11-28 07:42:03
"""
    Base Docstring-parsers
"""
from BeautifulSoup import BeautifulSoup

class Renderer(object):
    """
        Basic docstring-parser
        
        Just passes the text throught, without any formatting
    """
    __module__ = __name__
    name = 'null'

    def _render(self, source):
        return source

    def render_description(self, desc):
        """ render full description (without title)"""
        return self._render(desc.docstring)

    def render_short_desc(self, desc):
        """ render first paragraph (without title) """
        return self._render(desc.docstring)

    def render_title(self, desc):
        """ render title only """
        soup = BeautifulSoup(description)
        for tagname in ('h1', 'h2', 'h3'):
            title = soup.find(tagname)
            if title:
                return title.renderContents()

        return self._render(desc.docstring[0:1])

    @property
    def parser_id(self):
        if isinstance(self.name, basestring):
            return self.name.lower()
        else:
            return self.name[0].lower()

    @classmethod
    def matches(cls, name):
        name = name.lower()
        names = cls.name
        if isinstance(names, basestring):
            return name == names.lower()
        else:
            return name in (n.lower() for n in names)


class HTMLRenderer(Renderer):
    __module__ = __name__
    name = 'html'

    def render_title(self, desc):
        html = self._render(desc.docstring)
        soup = BeautifulSoup(html)
        heading = soup.find('h1') or soup.find('h2')
        if heading:
            return heading.renderContents().strip()
        else:
            return ''

    def render_short_desc(self, desc):
        """ render first paragraph (without title) """
        short_desc = BeautifulSoup(self.render_description(desc)).find('p')
        if short_desc:
            soup = BeautifulSoup(str(short_desc))
            if desc.href:
                href = desc.href
                for anchor in soup.findAll('a'):
                    if anchor['href'].startswith('#'):
                        anchor['href'] = href + anchor['href']

            return str(soup)
        else:
            return ''