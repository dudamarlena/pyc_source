# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/daniel/code/textX/textx-gen-coloring/textx_gen_coloring/templates/__init__.py
# Compiled at: 2019-08-21 19:03:19
# Size of source mod 2**32: 311 bytes
from os.path import dirname, join
import jinja2
templates_path = dirname(__file__)
textmate_template_dir = join(templates_path, 'textmate')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(templates_path), autoescape=True, lstrip_blocks=True, trim_blocks=True)