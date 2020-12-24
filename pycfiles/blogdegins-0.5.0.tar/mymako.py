# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/gines/midesarrollo/hg-projects/blogdegins-data/www.artgins.es/htmlrendercode/mymako.py
# Compiled at: 2012-08-20 03:55:04
import os
from mako.lookup import TemplateLookup

def get_mako_lookup(code_path, output_path):
    cache_dir = os.path.join(output_path, '.cache')
    if not os.path.exists(cache_dir):
        os.mkdir(cache_dir)
    lookup = TemplateLookup(directories=[
     code_path], module_directory=cache_dir)
    return lookup