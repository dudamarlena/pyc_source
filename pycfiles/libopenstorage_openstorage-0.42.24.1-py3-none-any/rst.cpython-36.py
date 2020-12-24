# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/readme-renderer/readme_renderer/rst.py
# Compiled at: 2020-01-10 16:25:27
# Size of source mod 2**32: 3370 bytes
from __future__ import absolute_import, division, print_function
import io
from docutils.core import publish_parts
from docutils.writers.html4css1 import HTMLTranslator, Writer
from docutils.utils import SystemMessage
from .clean import clean

class ReadMeHTMLTranslator(HTMLTranslator):
    object_image_types = {}


SETTINGS = {'cloak_email_addresses':True, 
 'doctitle_xform':True, 
 'sectsubtitle_xform':True, 
 'initial_header_level':2, 
 'file_insertion_enabled':False, 
 'halt_level':2, 
 'math_output':'MathJax', 
 'raw_enabled':False, 
 'report_level':5, 
 'smart_quotes':True, 
 'strip_comments':True, 
 'syntax_highlight':'short'}

def render(raw, stream=None, **kwargs):
    if stream is None:
        stream = io.StringIO()
    settings = SETTINGS.copy()
    settings['warning_stream'] = stream
    writer = Writer()
    writer.translator_class = ReadMeHTMLTranslator
    try:
        parts = publish_parts(raw, writer=writer, settings_overrides=settings)
    except SystemMessage:
        rendered = None
    else:
        rendered = parts.get('docinfo', '') + parts.get('fragment', '')
    if rendered:
        return clean(rendered)
    else:
        return