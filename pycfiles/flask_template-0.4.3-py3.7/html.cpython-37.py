# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/flask_template/templates/mongo/proj/utils/html.py
# Compiled at: 2020-04-01 02:43:02
# Size of source mod 2**32: 1401 bytes
from html.parser import HTMLParser
acceptable_elements = {
 'a', 'abbr', 'acronym', 'address', 'area', 'article', 'aside', 'audio', 'b', 'big', 'blockquote',
 'br', 'button', 'canvas', 'caption', 'center', 'cite', 'code', 'col', 'colgroup', 'command',
 'datagrid', 'datalist', 'dd', 'del', 'details', 'dfn', 'dialog', 'dir', 'div', 'dl', 'dt', 'em',
 'event-source', 'fieldset', 'figcaption', 'figure', 'footer', 'font', 'form', 'header', 'h1',
 'h2', 'h3', 'h4', 'h5', 'h6', 'hr', 'i', 'img', 'input', 'ins', 'keygen', 'kbd', 'label',
 'legend', 'li', 'm', 'map', 'menu', 'meter', 'multicol', 'nav', 'nextid', 'ol', 'output',
 'optgroup', 'option', 'p', 'pre', 'progress', 'q', 's', 'samp', 'section', 'select', 'small',
 'sound', 'source', 'spacer', 'span', 'strike', 'strong', 'sub', 'sup', 'table', 'tbody', 'td',
 'textarea', 'time', 'tfoot', 'th', 'thead', 'tr', 'tt', 'u', 'ul', 'var', 'video'}

class MyHTMLParser(HTMLParser):

    def __init__(self, *args, **kwargs):
        (super(MyHTMLParser, self).__init__)(*args, **kwargs)
        self.elements = set()

    def handle_starttag(self, tag, attrs):
        self.elements.add(tag)

    def handle_endtag(self, tag):
        self.elements.add(tag)


def is_html(text):
    parser = MyHTMLParser()
    parser.feed(text)
    return bool(parser.elements.intersection(acceptable_elements))