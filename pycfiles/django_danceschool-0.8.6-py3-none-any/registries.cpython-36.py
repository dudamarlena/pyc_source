# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /c/Users/Lee/Sync/projects/django-danceschool/currentmaster/django-danceschool/danceschool/core/registries.py
# Compiled at: 2019-04-03 22:56:26
# Size of source mod 2**32: 1381 bytes
from persisting_theory import Registry

class PluginTemplateBase(object):
    __doc__ = ' The base class for registering custom plugin templates. '
    template_name = ''
    plugin = None
    description = ''


class PluginTemplatesRegistry(Registry):
    __doc__ = "\n    Several plugins in this project allow the use of selectable templates\n    (e.g. for different types of statistics, different ways of displaying\n    instructors or upcoming series, etc.).  This registry keep track of the\n    list of template options that is presented when configuring each plugin.\n    While a user with the 'core.choose_custom_plugin_template' permission\n    can always set an entirely custom template file, it is recommended to\n    register your customer templates by defining a class in your app's\n    cms_plugins.py that inherits from\n    danceschool.core.registries.PluginTemplateBase, defining the\n    template_name and plugin properties, then registering your class by\n    decorating it with @plugin_templates_registry.register.\n    "
    look_into = 'cms_plugins'


plugin_templates_registry = PluginTemplatesRegistry()