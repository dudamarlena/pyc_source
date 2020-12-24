# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/devans/Documents/cirrus/src/cirrus/templates/__init__.py
# Compiled at: 2016-08-09 17:10:30
__doc__ = '\n_templates_\n\n'
import os, inspect

def find_template_dir():
    """util to locate this directory"""
    this_init = inspect.getsourcefile(find_template)
    return os.path.dirname(this_init)


def find_template(template_name):
    """util to find the path to a template file"""
    return os.path.join(find_template_dir(), template_name)