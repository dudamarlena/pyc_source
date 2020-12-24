# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /MyWork/Projects/PyCK/pyck/mako_utils/template_lookup.py
# Compiled at: 2015-02-06 19:21:32
import os
from mako.lookup import TemplateLookup
here = os.path.dirname(__file__)
template_lookup = TemplateLookup(directories=[here + '/templates'], module_directory=here + '/cache', output_encoding='utf8', input_encoding='utf8', encoding_errors='ignore')