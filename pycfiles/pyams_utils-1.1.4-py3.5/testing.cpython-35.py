# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_utils/testing.py
# Compiled at: 2020-02-18 19:11:13
# Size of source mod 2**32: 2422 bytes
"""PyAMS_utils.testing module

This module provides small testing helpers.
"""
import lxml.etree, lxml.html
__docformat__ = 'restructuredtext'

def render_xpath(view, xpath='.'):
    r"""Render only an XPath selection of a full HTML code

    >>> from pyams_utils.testing import render_xpath
    >>> class View:
    ...     def __call__(self):
    ...         return '''<div><div class="row"><p>Row 1</p></div>                           <div class="row"><p>Row 2</p></div></div>'''
    >>> view = View()
    >>> render_xpath(view, './/div[2][@class="row"]')
    '<div class="row">\n  <p>Row 2</p>\n</div>\n'
    """
    method = getattr(view, 'render', None)
    if method is None:
        method = view.__call__
    string = method()
    if string == '':
        return string
    try:
        root = lxml.etree.fromstring(string)
    except lxml.etree.XMLSyntaxError:
        root = lxml.html.fromstring(string)

    output = ''
    for node in root.xpath(xpath, namespaces={'xmlns': 'http://www.w3.org/1999/xhtml'}):
        s = lxml.etree.tounicode(node, pretty_print=True)
        s = s.replace(' xmlns="http://www.w3.org/1999/xhtml"', ' ')
        output += s

    if not output:
        raise ValueError('No elements matched by %s.' % repr(xpath))
    output = output.replace('\n\n', '\n')
    output = output.replace('"/>', '" />')
    return output


def format_html(input):
    r"""Render formatted HTML code by removing empty lines and spaces ending lines

    >>> from pyams_utils.testing import format_html
    >>> format_html('''<div>      \n<b>This is a test</b>    \n\n</div>    ''')
    '<div>\n<b>This is a test</b>\n</div>'
    """
    return '\n'.join(filter(bool, map(str.rstrip, input.split('\n'))))