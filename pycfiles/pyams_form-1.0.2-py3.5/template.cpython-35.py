# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_form/template.py
# Compiled at: 2020-02-23 12:53:51
# Size of source mod 2**32: 6891 bytes
"""PyAMS_form.template module

Widgets templates management module.
"""
import inspect, os, venusian
from pyramid.config import ConfigurationError
from pyramid_chameleon.interfaces import IChameleonTranslate
from zope.component import getGlobalSiteManager
from zope.interface import Interface, directlyProvides
from pyams_form.interfaces import INPUT_MODE, IWidgetLayoutTemplate
from pyams_layer.interfaces import IFormLayer
from pyams_template.interfaces import IPageTemplate
from pyams_template.template import TemplateFactory, ViewTemplate
from pyams_utils.registry import query_utility
__docformat__ = 'restructuredtext'

class WidgetTemplateFactory(TemplateFactory):
    __doc__ = 'Widget template factory'

    def __call__(self, context, request, form, field, widget):
        return self.template


class WidgetTemplate(ViewTemplate):
    __doc__ = 'Widget template class'

    def __init__(self, provides):
        super(WidgetTemplate, self).__init__(provides)

    def __call__(self, instance, *args, **keywords):
        request = instance.request
        registry = request.registry
        template = registry.getMultiAdapter((
         request.context, request, instance.form, instance.field, instance), self.provides, name=instance.mode)
        keywords.update({'context': instance.context, 
         'request': instance.request, 
         'view': instance, 
         'translate': query_utility(IChameleonTranslate)})
        return template(*args, **keywords)


class GetWidgetTemplate(WidgetTemplate):
    __doc__ = 'Get widget template'

    def __init__(self):
        super(GetWidgetTemplate, self).__init__(IPageTemplate)


get_widget_template = GetWidgetTemplate

class GetWidgetLayout(WidgetTemplate):
    __doc__ = 'Layout template getter class'

    def __init__(self):
        super(GetWidgetLayout, self).__init__(IWidgetLayoutTemplate)


get_widget_layout = GetWidgetLayout

def register_widget_template(template, widget, settings, provides, registry=None):
    """Register new widget template"""
    if not os.path.isfile(template):
        raise ConfigurationError('No such file', template)
    content_type = settings.get('content_type', 'text/html')
    macro = settings.get('macro')
    factory = WidgetTemplateFactory(template, content_type, macro)
    provides = settings.get('provides', provides)
    directlyProvides(factory, provides)
    required = (
     settings.get('context', Interface),
     settings.get('layer', IFormLayer),
     settings.get('form', None),
     settings.get('field', None),
     widget)
    if registry is None:
        registry = settings.get('registry')
        if registry is None:
            registry = getGlobalSiteManager()
    registry.registerAdapter(factory, required, provides, settings.get('mode', INPUT_MODE))


class base_widget_template_config:
    __doc__ = 'Class decorator used to declare a widget template'
    venusian = venusian
    interface = IPageTemplate

    def __init__(self, **settings):
        if 'for_' in settings and settings.get('context') is None:
            settings['context'] = settings['for_']
        self.__dict__.update(settings)

    def __call__(self, wrapped):
        settings = self.__dict__.copy()

        def callback(context, name, widget):
            template = os.path.join(os.path.dirname(inspect.getfile(inspect.getmodule(widget))), settings.get('template'))
            if not os.path.isfile(template):
                raise ConfigurationError('No such file', template)
            registry = settings.get('registry')
            if registry is None:
                config = context.config.with_package(info.module)
                registry = config.registry
            register_widget_template(template, widget, settings, self.interface, registry)

        info = self.venusian.attach(wrapped, callback, category='pyams_form')
        if info.scope == 'class' and settings.get('attr') is None:
            settings['attr'] = wrapped.__name__
        settings['_info'] = info.codeinfo
        return wrapped


class widget_template_config(base_widget_template_config):
    __doc__ = 'Class decorator used to declare a widget template'


def override_widget_template(widget, **settings):
    """Override template for a given widget

    This function can be used to override a widget template without using ZCML.
    Settings are the same as for @widget_template_config decorator.
    """
    template = settings.get('template', '')
    if not template:
        raise ConfigurationError('No template specified')
    if not template.startswith('/'):
        stack = inspect.stack()[1]
        template = os.path.join(os.path.dirname(inspect.getfile(inspect.getmodule(stack[0]))), template)
    register_widget_template(template, widget, settings, IPageTemplate)


class widget_layout_config(base_widget_template_config):
    __doc__ = 'Class decorator used to declare a layout template'
    interface = IWidgetLayoutTemplate


def override_widget_layout(widget, **settings):
    """Override layout template for a given class

    This function can be used to override a class layout template without using ZCML.
    Settings are the same as for @layout_config decorator.
    """
    template = settings.get('template', '')
    if not template:
        raise ConfigurationError('No template specified')
    if not template.startswith('/'):
        stack = inspect.stack()[1]
        template = os.path.join(os.path.dirname(inspect.getfile(inspect.getmodule(stack[0]))), template)
    register_widget_template(template, widget, settings, IWidgetLayoutTemplate)