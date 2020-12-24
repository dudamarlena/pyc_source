# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/genshicolumntemplate/__init__.py
# Compiled at: 2007-09-09 02:05:17
from paste.script import templates
import pkg_resources

class GenshiColumnTemplate(templates.Template):
    __module__ = __name__
    egg_plugins = [
     'GenshiColumnTemplate']
    required_templates = ['tggenshi']
    _template_dir = pkg_resources.resource_filename('genshicolumntemplate', 'template')
    use_cheetah = True
    summary = 'Adds a 3 column layout to the standard genshi quickstart.'