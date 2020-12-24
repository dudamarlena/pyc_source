# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.4/dist-packages/bass/markup.py
# Compiled at: 2015-09-13 04:04:37
# Size of source mod 2**32: 1609 bytes
"""
bass.markup
-----
Objects and functions related to markup of text pages.
"""
import re
from . import setting
converter = {}
try:
    import markdown2
    markdown_found = True

    def convert_md2(text):
        return markdown2.markdown(text, extras=['def_list', 'footnotes', 'tables'])


    converter['mkd'] = convert_md2
    setting.markdown = True
except ImportError:
    setting.markdown = False

if not setting.markdown:
    try:
        import markdown

        def convert_mkd(text):
            return markdown.markdown(text, extras=['markdown.extensions.def_list',
             'markdown.extensions.footnotes',
             'markdown.extensionstables'])


        converter['mkd'] = convert_mkd
        setting.markdown = True
    except ImportError:
        setting.markdown = False

try:
    import docutils.core
    from docutils.writers.html4css1 import Writer

    def convert_rst(text):
        return docutils.core.publish_parts(text, writer=Writer())['body']


    converter['rst'] = convert_rst
    setting.rest = True
except ImportError:
    setting.rest = False

try:
    import textile

    def convert_txi(text):
        return textile.textile(text)


    converter['txi'] = convert_txi
    setting.textile = True
except ImportError:
    setting.textile = False

def convert_html(text):
    return text


converter['html'] = convert_html

def convert_txt(text):
    return '<p>' + re.sub('\\n{2,}', '</p><p>', text) + '</p>'


converter['txt'] = convert_txt