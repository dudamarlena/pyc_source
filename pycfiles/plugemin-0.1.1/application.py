# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/plugboard/application.py
# Compiled at: 2006-02-14 14:34:55
from zope import interface
from zope.interface import adapter
import pkg_resources, sys

class IApplication(interface.Interface):
    """
    Main application interface
    """
    __module__ = __name__
    plugins = interface.Attribute('A list of found PlugBoard plugins')

    def register(ofrom, oto, name=''):
        """
        Register adaption from ofrom object to oto object gaining automatically their interfaces
        """
        pass


class Application(object):
    __module__ = __name__
    interface.implements(IApplication)

    def __init__(self):
        self.registry = adapter.AdapterRegistry()
        interface.interface.adapter_hooks = [self._adapter_hook]

    def _adapter_hook(self, provided, obj):
        adapter = self.registry.lookup1(interface.providedBy(obj), provided, '')
        if callable(adapter):
            return adapter(obj)
        else:
            adapter.application = self
            return adapter

    def _get_interface(self, obj):
        try:
            if issubclass(obj, interface.Interface):
                return obj
        except:
            pass

        if callable(obj):
            return iter(interface.implementedBy(obj)).next()
        else:
            return iter(interface.providedBy(obj)).next()

    def register(self, ofrom, oto, name=''):
        self.registry.register([self._get_interface(ofrom)], self._get_interface(oto), name, oto)