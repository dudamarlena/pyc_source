# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /MyWork/Projects/PyCK/pyck/mako_utils/template_lookup.py
# Compiled at: 2015-02-06 19:21:32
# Size of source mod 2**32: 387 bytes
import os
from mako.lookup import TemplateLookup
here = os.path.dirname(__file__)
template_lookup = TemplateLookup(directories=[here + '/templates'], module_directory=here + '/cache', output_encoding='utf8', input_encoding='utf8', encoding_errors='ignore')