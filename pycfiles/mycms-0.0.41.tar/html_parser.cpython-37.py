# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jnvilo/Projects/web/mycms/mycms/creole/shared/html_parser.py
# Compiled at: 2019-02-05 11:01:21
# Size of source mod 2**32: 1009 bytes
"""
    HTMLParser for Python 2.x and 3.x
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    The HTMLParser has problems with the correct handling of <script>...</script>
    and <style>...</style> areas.
       
    It was fixed with v2.7.3 and 3.2.3, see:
        http://www.python.org/download/releases/2.7.3/
        http://www.python.org/download/releases/3.2.3/
    see also:
        http://bugs.python.org/issue670664#msg146770
        
    :copyleft: 2011-2012 by python-creole team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""
try:
    import HTMLParser as OriginHTMLParser
except ImportError:
    from html import parser as OriginHTMLParser

if hasattr(OriginHTMLParser, 'cdata_elem'):
    HTMLParser = OriginHTMLParser
else:
    from mycms.creole.shared.HTMLParsercompat import HTMLParser