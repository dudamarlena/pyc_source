# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/schevo/template.py
# Compiled at: 2007-03-21 14:34:41
"""Schevo templates for Python Paste.

For copyright, license, and warranty, see bottom of file.
"""
import pkg_resources
from paste.script import templates

class SchevoTemplate(templates.Template):
    __module__ = __name__
    egg_plugins = [
     'Schevo']
    _template_dir = pkg_resources.resource_filename(pkg_resources.Requirement.parse('Schevo'), 'schevo/templates/schevo')
    summary = 'Schevo application template.'