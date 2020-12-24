# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dir2html/render_template.py
# Compiled at: 2018-11-21 04:57:05
# Size of source mod 2**32: 571 bytes
import sys
from pkg_resources import resource_string, resource_filename

def render_template(template_name, render_dict):
    template_names = {'image-template':'resources/image-template.html', 
     'album-template':'resources/album-template.html'}
    template_file = resource_filename(__name__, template_names.get(template_name, ''))
    with open(template_file) as (f):
        rendered_template = f.read()
        for k, v in render_dict.items():
            rendered_template = rendered_template.replace(k, v)

        return rendered_template