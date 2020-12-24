# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/devans/Documents/cirrus/src/cirrus/templates/__init__.py
# Compiled at: 2016-08-09 17:10:30
# Size of source mod 2**32: 373 bytes
"""
_templates_

"""
import os, inspect

def find_template_dir():
    """util to locate this directory"""
    this_init = inspect.getsourcefile(find_template)
    return os.path.dirname(this_init)


def find_template(template_name):
    """util to find the path to a template file"""
    return os.path.join(find_template_dir(), template_name)