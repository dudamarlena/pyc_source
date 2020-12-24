# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_form/ajax.py
# Compiled at: 2020-02-23 12:53:51
# Size of source mod 2**32: 15455 bytes
__doc__ = 'PyAMS_form.ajex module\n\nThis module is declaring forms which can be used in an AJAX context, where\nforms are submitted using an XMLHTTPRequest and where response is made of\nJSON messages.\n'
import logging, venusian
from pyramid.config import ConfigurationError
from pyramid.events import subscriber
from pyramid.interfaces import IRequest
from zope.interface import Interface, alsoProvides, implementer
from pyams_form.events import FormCreatedEvent
from pyams_form.interfaces import DISPLAY_MODE
from pyams_form.interfaces.error import IAJAXErrorsRenderer, IErrorViewSnippet, IMultipleErrors
from pyams_form.interfaces.form import IAJAXForm, IAJAXFormRenderer, IAddForm, IForm, IFormCreatedEvent
from pyams_layer.interfaces import IFormLayer
from pyams_pagelet.interfaces import IPagelet
from pyams_pagelet.pagelet import Pagelet
from pyams_utils.adapter import adapter_config
from pyams_utils.list import boolean_iter
__docformat__ = 'restructuredtext'
from pyams_form import _
LOGGER = logging.getLogger('PyAMS (form)')

@implementer(IAJAXForm)
class AJAXForm:
    """AJAXForm"""

    def __call__(self):
        registry = self.request.registry
        registry.notify(FormCreatedEvent(self))
        self.update()
        has_errors, errors = boolean_iter(self.get_errors())
        if has_errors:
            return self.get_ajax_errors(errors)
        return self.get_ajax_output(self._finished_obj)

    def get_ajax_errors(self, errors):
        """Get AJAX errors"""
        request = self.request
        registry = request.registry
        renderer = registry.getMultiAdapter((self.context, request, self), IAJAXErrorsRenderer)
        return renderer.render(errors)

    def get_ajax_output(self, changes):
        """Get AJAX status and changes output in JSON"""
        raise NotImplementedError


@subscriber(IFormCreatedEvent, context_selector=IAJAXForm)
def handle_new_ajax_form(event):
    """Handle new AJAX form"""
    form = event.object
    impl = getattr(form, '__ajax_interfaces__', None)
    if impl is not None:
        alsoProvides(form, *impl)


class AJAXAddForm(AJAXForm):
    """AJAXAddForm"""
    no_changes_message = _('No data was created.')

    def get_ajax_output(self, changes):
        request = self.request
        registry = request.registry
        renderer = registry.queryMultiAdapter((self.context, request, self), IAJAXFormRenderer)
        if renderer is not None:
            result = renderer.render(changes)
            if result:
                pass
            return result
        if changes is None:
            return {'status': 'info', 
             'message': request.localizer.translate(self.no_changes_message)}
        return {'status': 'reload', 
         'location': self.next_url()}


class AJAXEditForm(AJAXForm):
    """AJAXEditForm"""

    def get_ajax_output(self, changes):
        request = self.request
        registry = request.registry
        translate = request.localizer.translate
        renderer = registry.queryMultiAdapter((self.context, request, self), IAJAXFormRenderer)
        result = {}
        if renderer is not None:
            result = renderer.render(changes)
        status = ''
        message = ''
        if result:
            status = result.get('status')
            message = result.get('message')
        if not changes:
            if not status:
                result['status'] = 'info'
            if not message:
                result['message'] = translate(self.no_changes_message)
        elif not status:
            result['status'] = status = 'success'
        if not message:
            if status == 'success':
                result['message'] = translate(self.success_message)
        return result


@adapter_config(required=(None, IFormLayer, IAJAXForm), provides=IAJAXFormRenderer)
class AJAXFormRenderer:
    """AJAXFormRenderer"""

    def __init__(self, context, request, form):
        self.context = context
        self.request = request
        self.form = form

    def render(self, changes):
        """Render form status and changes in JSON format"""
        registry = self.request.registry
        result = {}
        for form in self.form.get_forms(include_self=False):
            if form.mode == DISPLAY_MODE:
                pass
            else:
                renderer = registry.queryMultiAdapter((form.context, form.request, form), IAJAXFormRenderer)
                if renderer is not None:
                    form_output = renderer.render(changes)
                    if form_output:
                        for key, value in form_output.items():
                            if isinstance(value, (list, tuple)) and key in result:
                                form_output[key] += result[key]

                        result.update(form_output)

        return result


@adapter_config(required=(Interface, IFormLayer, IForm), provides=IAJAXErrorsRenderer)
class AJAXErrorRenderer:
    """AJAXErrorRenderer"""

    def __init__(self, context, request, form):
        self.context = context
        self.request = request
        self.form = form

    @classmethod
    def get_widget_error(cls, error, status, translate):
        """Get widget for a given error"""
        if hasattr(error, 'widget'):
            widget = error.widget
            if widget is not None:
                status.setdefault('widgets', []).append({'id': widget.id, 
                 'name': widget.name, 
                 'label': translate(widget.label), 
                 'message': translate(error.message)})
            else:
                status.setdefault('messages', []).append({'message': translate(error.message)})
        else:
            status.setdefault('messages', []).append(translate(error.message))

    def render(self, errors):
        """Return status as JSON message"""
        registry = self.request.registry
        translate = self.request.localizer.translate
        result = {'status': 'error', 
         'error_message': translate(self.form.status)}
        for error in errors:
            if isinstance(error, Exception):
                error = registry.getMultiAdapter((
                 error, self.request, None, None, self, self.request), IErrorViewSnippet)
            error.update()
            if IMultipleErrors.providedBy(error.error):
                for inner_error in error.error.errors:
                    self.get_widget_error(inner_error, result, translate)

            else:
                self.get_widget_error(error, result, translate)

        return result


class ajax_form_config:
    """ajax_form_config"""
    venusian = venusian

    def __init__(self, **settings):
        if 'name' not in settings:
            raise ConfigurationError("Missing 'name' argument for form definition")
        if 'for_' in settings and settings.get('context') is None:
            settings['context'] = settings.pop('for_')
        if 'layer' in settings:
            settings['request_type'] = settings.pop('layer')
        settings['ajax'] = ajax_settings = {}
        if 'context' in settings:
            ajax_settings['context'] = settings.get('context')
        if 'ajax_name' in settings:
            ajax_settings['name'] = settings.pop('ajax_name')
        else:
            ajax_settings['name'] = settings['name'].replace('.html', '.json')
        if 'ajax_base' in settings:
            ajax_settings['base'] = settings.pop('ajax_base')
        if 'ajax_implements' in settings:
            ajax_settings['implements'] = settings.pop('ajax_implements')
        if 'ajax_method' in settings:
            method = settings.pop('ajax_method')
            if method is not None:
                ajax_settings['request_method'] = method
        else:
            ajax_settings['request_method'] = 'POST'
        if 'ajax_permission' in settings:
            ajax_settings['permission'] = settings.pop('ajax_permission')
        if 'ajax_renderer' in settings:
            renderer = settings.pop('ajax_renderer')
            if renderer is not None:
                ajax_settings['renderer'] = renderer
        else:
            ajax_settings['renderer'] = 'json'
        if 'ajax_xhr' in settings:
            xhr = settings.pop('ajax_xhr')
            if xhr is not None:
                ajax_settings['xhr'] = xhr
        else:
            ajax_settings['xhr'] = True
        self.__dict__.update(settings)

    def __call__(self, wrapped):
        form_settings = self.__dict__.copy()
        depth = form_settings.pop('_depth', 0)
        ajax_settings = form_settings.pop('ajax')

        def callback(context, name, obj):
            """Venusian decorator callback"""
            config = context.config.with_package(info.module)
            form_cdict = {'__module__': obj.__module__, 
             '__name__': form_settings.get('name'), 
             'permission': form_settings.get('permission'), 
             'ajax_form_handler': ajax_settings.get('name')}
            ajax_cdict = {'__module__': obj.__module__, 
             '__name__': ajax_settings.get('name')}
            permission = ajax_settings.get('permission') or getattr(obj, '_edit_permission')
            if permission is not None:
                ajax_cdict['permission'] = permission
            base = ajax_settings.get('base')
            if base is None:
                if IAddForm.implementedBy(obj):
                    base = AJAXAddForm
            else:
                base = AJAXEditForm
            if 'implements' in ajax_settings:
                impl = ajax_settings.pop('implements')
                if not isinstance(impl, (list, tuple, set)):
                    impl = (
                     impl,)
                obj.__ajax_interfaces__ = impl
            form_class = type(obj.__name__, (obj, Pagelet), form_cdict)
            LOGGER.debug('Registering pagelet view "{}" for {} ({})'.format(form_settings.get('name'), str(form_settings.get('context', Interface)), str(form_class)))
            registry = form_settings.get('registry') or config.registry
            registry.registerAdapter(form_class, (
             form_settings.get('context', Interface),
             form_settings.get('request_type', IRequest)), IPagelet, form_settings.get('name'))
            config.add_view(view=form_class, **form_settings)
            ajax_class = type('AJAX' + obj.__name__, (base, obj), ajax_cdict)
            LOGGER.debug('Registering AJAX view "{0}" for {1} ({2})'.format(ajax_settings.get('name'), str(ajax_settings.get('context', Interface)), str(ajax_class)))
            config.add_view(view=ajax_class, **ajax_settings)

        info = self.venusian.attach(wrapped, callback, category='pyams_form', depth=depth + 1)
        if info.scope == 'class':
            if form_settings.get('attr') is None:
                form_settings['attr'] = wrapped.__name__
            if ajax_settings.get('attr') is None:
                ajax_settings['attr'] = wrapped.__name__
        form_settings['_info'] = info.codeinfo
        ajax_settings['_info'] = info.codeinfo
        return wrapped