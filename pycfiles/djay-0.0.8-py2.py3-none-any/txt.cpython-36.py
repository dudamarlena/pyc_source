# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-m_4qh6p6/readme-renderer/readme_renderer/txt.py
# Compiled at: 2019-07-30 18:47:11
# Size of source mod 2**32: 990 bytes
from __future__ import absolute_import, division, print_function
import sys
from .clean import clean
if sys.version_info >= (3, ):
    from html import escape as html_escape
else:
    from cgi import escape

    def html_escape(s):
        return escape(s, quote=True).replace("'", '&#x27;')


def render(raw, **kwargs):
    rendered = html_escape(raw).replace('\n', '<br>')
    return clean(rendered, tags=['br'])