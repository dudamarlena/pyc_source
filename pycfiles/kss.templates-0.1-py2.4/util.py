# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/kss/templates/util.py
# Compiled at: 2007-09-16 14:46:42
from paste.script.templates import Template, var

class KSSPluginTemplate(Template):
    __module__ = __name__
    _template_dir = 'plugin'
    summary = 'KSS plugin template'
    egg_plugins = []
    vars = [
     var('namespace', 'The namespace for your plugin (something like `my-namespace`)')]


class KSSZopePluginTemplate(Template):
    __module__ = __name__
    _template_dir = 'zope_plugin'
    summary = 'KSS Zope plugin template'
    required_templates = ['kss_plugin']