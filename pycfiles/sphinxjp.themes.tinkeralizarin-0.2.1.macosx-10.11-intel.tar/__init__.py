# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Python/2.7/site-packages/sphinxjp/themes/tinkeralizarin/__init__.py
# Compiled at: 2016-01-09 00:20:48
from os import path
package_dir = path.abspath(path.dirname(__file__))
template_path = path.join(package_dir, 'templates')

def get_path():
    """entry-point for sphinxjp.themecore theme."""
    return template_path