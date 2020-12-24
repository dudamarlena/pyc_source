# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/plim/extensions.py
# Compiled at: 2015-10-10 10:15:03
# Size of source mod 2**32: 761 bytes
from docutils.core import publish_parts
import coffeescript
from scss import Scss
from stylus import Stylus
from .util import u

def rst_to_html(source):
    html = publish_parts(source=source, writer_name='html')
    return html['html_body']


def coffee_to_js(source):
    return u('<script>{js}</script>').format(js=coffeescript.compile(source))


def scss_to_css(source):
    css = Scss().compile(source).strip()
    return u('<style>{css}</style>').format(css=css)


def stylus_to_css(source):
    compiler = Stylus()
    return u('<style>{css}</style>').format(css=compiler.compile(source).strip())