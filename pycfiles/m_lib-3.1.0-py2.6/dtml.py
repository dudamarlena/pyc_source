# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/lib.linux-i686-2.6/m_lib/net/www/dtml.py
# Compiled at: 2016-07-25 10:38:46
"""DTML utilities"""

class standard_html:

    def __init__(self, title):
        self.standard_html_header = '<HTML>\n   <HEAD>\n      <TITLE>\n         %s\n      </TITLE>\n   </HEAD>\n\n<BODY>' % title
        self.standard_html_footer = '</BODY>\n</HTML>'
        self.title = title