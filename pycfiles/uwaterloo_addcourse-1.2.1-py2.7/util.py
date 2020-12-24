# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/addcourse/util.py
# Compiled at: 2015-04-26 23:07:48
"""Utility functions used elsewhere in the package."""
import tempfile, os

def preview_page(html):
    """Preview the HTML code html in your browser."""
    with tempfile.NamedTemporaryFile(mode='w+t') as (f):
        f.write(str(html))
        f.flush()
        os.system(('firefox {}').format(f.name))
        os.sleep(10)