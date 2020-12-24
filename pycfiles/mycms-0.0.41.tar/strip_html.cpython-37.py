# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jnvilo/Projects/web/mycms/mycms/creole/html_tools/strip_html.py
# Compiled at: 2019-02-05 11:01:21
# Size of source mod 2**32: 3015 bytes
"""
    python-creole utils
    ~~~~~~~~~~~~~~~~~~~    

    :copyleft: 2008-2011 by python-creole team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""
from __future__ import division, absolute_import, print_function, unicode_literals
import re
from mycms.creole.html_parser.config import BLOCK_TAGS
strip_html_regex = re.compile('\n        \\s*\n        <\n            (?P<end>/{0,1})       # end tag e.g.: </end>\n            (?P<tag>[^ >]+)       # tag name\n            .*?\n            (?P<startend>/{0,1})  # closed tag e.g.: <closed />\n        >\n        \\s*\n    ', re.VERBOSE | re.MULTILINE | re.UNICODE)

def strip_html(html_code):
    r"""
    Delete whitespace from html code. Doesn't recordnize preformatted blocks!

    >>> strip_html(' <p>  one  \n two  </p>')
    '<p>one two</p>'

    >>> strip_html('<p><strong><i>bold italics</i></strong></p>')
    '<p><strong><i>bold italics</i></strong></p>'

    >>> strip_html('<li>  Force  <br /> \n linebreak </li>')
    '<li>Force<br />linebreak</li>'

    >>> strip_html('one  <i>two \n <strong>   \n  three  \n  </strong></i>')
    'one <i>two <strong>three</strong> </i>'

    >>> strip_html('<p>a <unknown tag /> foobar  </p>')
    '<p>a <unknown tag /> foobar</p>'

    >>> strip_html('<p>a <pre> preformated area </pre> foo </p>')
    '<p>a<pre>preformated area</pre>foo</p>'

    >>> strip_html('<p>a <img src="/image.jpg" /> image.</p>')
    '<p>a <img src="/image.jpg" /> image.</p>'

    """

    def strip_tag(match):
        block = match.group(0)
        end_tag = match.group('end') in ('/', '/')
        startend_tag = match.group('startend') in ('/', '/')
        tag = match.group('tag')
        if tag in BLOCK_TAGS:
            return block.strip()
        space_start = block.startswith(' ')
        space_end = block.endswith(' ')
        result = block.strip()
        if not end_tag or space_start or space_end:
            result += ' '
        else:
            if startend_tag:
                if space_start:
                    result = ' ' + result
                if space_end:
                    result += ' '
            elif space_start or space_end:
                result = ' ' + result
        return result

    data = html_code.strip()
    clean_data = ' '.join([line.strip() for line in data.split('\n')])
    clean_data = strip_html_regex.sub(strip_tag, clean_data)
    return clean_data


if __name__ == '__main__':
    import doctest
    print(doctest.testmod())