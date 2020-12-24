# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/reddit2ebook/ebooklib_patched/plugins/booktype.py
# Compiled at: 2016-05-13 06:16:04
# Size of source mod 2**32: 4503 bytes
from ebooklib.plugins.base import BasePlugin
from ebooklib.utils import parse_html_string

class BooktypeLinks(BasePlugin):
    NAME = 'Booktype Links'

    def __init__(self, booktype_book):
        self.booktype_book = booktype_book

    def html_before_write(self, book, chapter):
        from lxml import etree
        try:
            from urlparse import urlparse, urljoin
        except ImportError:
            from urllib.parse import urlparse, urljoin

        try:
            tree = parse_html_string(chapter.content)
        except:
            return

        root = tree.getroottree()
        if len(root.find('body')) != 0:
            body = tree.find('body')
            for _link in body.xpath('//a'):
                if _link.get('href', '').find('InsertNoteID') != -1:
                    _ln = _link.get('href', '')
                    i = _ln.find('#')
                    _link.set('href', _ln[i:])
                else:
                    _u = urlparse(_link.get('href', ''))
                    if _u.scheme == '':
                        if _u.path != '':
                            _link.set('href', '%s.xhtml' % _u.path)
                        if _u.fragment != '':
                            _link.set('href', urljoin(_link.get('href'), '#%s' % _u.fragment))
                        if _link.get('name') != None:
                            _link.set('id', _link.get('name'))
                            etree.strip_attributes(_link, 'name')

        chapter.content = etree.tostring(tree, pretty_print=True, encoding='utf-8')


class BooktypeFootnotes(BasePlugin):
    NAME = 'Booktype Footnotes'

    def __init__(self, booktype_book):
        self.booktype_book = booktype_book

    def html_before_write(self, book, chapter):
        from lxml import etree
        from ebooklib import epub
        try:
            tree = parse_html_string(chapter.content)
        except:
            return

        root = tree.getroottree()
        if len(root.find('body')) != 0:
            body = tree.find('body')
            for footnote in body.xpath('//span[@class="InsertNoteMarker"]'):
                footnote_id = footnote.get('id')[:-8]
                a = footnote.getchildren()[0].getchildren()[0]
                footnote_text = body.xpath('//li[@id="%s"]' % footnote_id)[0]
                a.attrib['{%s}type' % epub.NAMESPACES['EPUB']] = 'noteref'
                ftn = etree.SubElement(body, 'aside', {'id': footnote_id})
                ftn.attrib['{%s}type' % epub.NAMESPACES['EPUB']] = 'footnote'
                ftn_p = etree.SubElement(ftn, 'p')
                ftn_p.text = footnote_text.text

            old_footnote = body.xpath('//ol[@id="InsertNote_NoteList"]')
            if len(old_footnote) > 0:
                body.remove(old_footnote[0])
        chapter.content = etree.tostring(tree, pretty_print=True, encoding='utf-8')