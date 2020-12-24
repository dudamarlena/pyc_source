# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/registration/__init__.py
# Compiled at: 2008-07-04 10:34:32
from paste.script import templates
import pkg_resources

class Registration(templates.Template):
    egg_plugins = [
     'Registration']
    _template_dir = pkg_resources.resource_filename('registration', 'template')
    summary = 'Provides a template for simple user registraton and verification.'
    required_templates = ['tgbase']
    use_cheetah = True