# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_form/contentprovider.py
# Compiled at: 2020-02-23 12:53:51
# Size of source mod 2**32: 5457 bytes
"""PyAMS_form.contentprovider module

Base form content providers.
"""
from zope.contentprovider.interfaces import IContentProvider
from zope.interface import Interface, Invalid, implementer
from zope.location import locate
from pyams_form.error import MultipleErrors
from pyams_form.field import FieldWidgets
from pyams_form.interfaces import DISPLAY_MODE, IContentProviders, IDataConverter, IValidator
from pyams_form.interfaces.error import IErrorViewSnippet
from pyams_form.interfaces.form import IFieldsAndContentProvidersForm
from pyams_form.interfaces.widget import IWidgets
from pyams_layer.interfaces import IFormLayer
from pyams_utils.adapter import adapter_config
from pyams_utils.interfaces.form import NO_VALUE
__docformat__ = 'restructuredtext'

class BaseProvider:
    __doc__ = 'Base content provider'
    __slots__ = ('position', )


_LOOKUP = BaseProvider()

@implementer(IContentProviders)
class ContentProviders(dict):
    __doc__ = 'Content providers mapping'

    def __init__(self, names=None):
        super(ContentProviders, self).__init__()
        if names is not None:
            for position, name in enumerate(names):
                self[name] = _LOOKUP

    def __setitem__(self, key, value):
        factory = ContentProviderFactory(factory=value, name=key)
        super(ContentProviders, self).__setitem__(key, factory)


class ContentProviderFactory:
    __doc__ = 'Content provider factory'

    def __init__(self, factory, name):
        self.factory = factory
        self.name = name
        self.position = getattr(factory, 'position', None)

    def __call__(self, manager):
        if self.factory != _LOOKUP:
            content_provider = self.factory(manager.content, manager.request, manager.form)
        else:
            registry = manager.request.registry
            content_provider = registry.getMultiAdapter((manager.content, manager.request,
             manager.form), IContentProvider, self.name)
        return content_provider


@adapter_config(required=(IFieldsAndContentProvidersForm, IFormLayer, Interface), provides=IWidgets)
class FieldWidgetsAndProviders(FieldWidgets):
    __doc__ = 'Field widgets and providers adapter'

    def update(self):
        super(FieldWidgetsAndProviders, self).update()
        unique_ordered_keys = list(self.keys())
        data = {}
        data.update(self)
        for name in self.form.content_providers:
            factory = self.form.content_providers[name]
            if factory.position is None:
                raise ValueError("Position of the following content provider should be an integer: '%s'." % name)
            content_provider = factory(self)
            short_name = name
            content_provider.update()
            unique_ordered_keys.insert(factory.position, short_name)
            data[short_name] = content_provider
            locate(content_provider, self, short_name)

        self.create_according_to_list(data, unique_ordered_keys)

    def extract(self):
        """See interfaces.IWidgets"""
        data = {}
        errors = ()
        registry = self.request.registry
        for name, widget in self.items():
            if IContentProvider.providedBy(widget):
                pass
            else:
                if widget.mode == DISPLAY_MODE:
                    pass
                else:
                    value = widget.field.missing_value
                    try:
                        widget.set_errors = self.set_errors
                        raw = widget.extract()
                        if raw is not NO_VALUE:
                            value = IDataConverter(widget).to_field_value(raw)
                        registry.getMultiAdapter((self.content, self.request, self.form,
                         getattr(widget, 'field', None), widget), IValidator).validate(value)
                    except (Invalid, ValueError, MultipleErrors) as error:
                        view = registry.getMultiAdapter((error, self.request, widget, widget.field,
                         self.form, self.content), IErrorViewSnippet)
                        view.update()
                        if self.set_errors:
                            widget.error = view
                        errors += (view,)
                    else:
                        name = widget.__name__
                    data[name] = value

        for error in self.validate(data):
            view = registry.getMultiAdapter((error, self.request, None, None,
             self.form, self.content), IErrorViewSnippet)
            view.update()
            errors += (view,)

        if self.set_errors:
            self.errors = errors
        return (
         data, errors)