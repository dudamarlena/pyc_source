# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/mvc/adapters/adapter_registry.py
# Compiled at: 2020-03-07 03:51:48
# Size of source mod 2**32: 5068 bytes
import importlib, logging
logger = logging.getLogger(__name__)
from ..settings import TOOLKIT
from ..support import gui_loop

class ToolkitRegistry(dict):
    __doc__ = "\n        Dict subclass used to store all AdapterRegistry's.\n        Keys are toolkit names, values are AdapterRegistry instances\n    "
    toolkit_modules = [
     '.gtk_support']
    selected_toolkit = None

    def get_or_create_registry(self, toolkit_name):
        if toolkit_name not in self:
            adapter_registry = AdapterRegistry()
            self.register(toolkit_name, adapter_registry)
        return self[toolkit_name]

    def register(self, toolkit_name, adapter_registry):
        self[toolkit_name] = adapter_registry

    def select_toolkit(self, toolkit_name):
        if toolkit_name not in self:
            raise ValueError("Cannot select unknown toolkit '%s'" % toolkit_name)
        else:
            self.selected_toolkit = toolkit_name
            tkar = self.get_selected_adapter_registry()
            tkar.load_toolkit_functions()

    def get_selected_adapter_registry(self):
        if self.selected_toolkit is None:
            raise ValueError('No toolkit has been selected!')
        else:
            return self[self.selected_toolkit]


class AdapterRegistry(dict):
    __doc__ = "\n        A dict which maps Adapter class types to the widget types they\n        can handle. This relies on these classes being registered using\n        the 'register' decorator also provided by this class.\n    "
    toolkit_registry = ToolkitRegistry()

    @classmethod
    def get_selected_adapter_registry(cls):
        return cls.toolkit_registry.get_selected_adapter_registry()

    @classmethod
    def get_adapter_for_widget_type(cls, widget_type):
        return cls.toolkit_registry.get_selected_adapter_registry()[widget_type]

    def set_toolkit_functions(self, *args, **kwargs):
        setattr(self, '_toolkit_functions', (args, kwargs))

    def load_toolkit_functions(self):
        """
            This function loads the toolkit functions passed to 
            set_toolkit_functions with the support module.
        """
        args, kwargs = getattr(self, '_toolkit_functions', ([], {}))
        (gui_loop.load_toolkit_functions)(*args, **kwargs)

    @classmethod
    def register(cls, adapter_cls):
        """
            This is called from metaclasses or used as a decorator.
            An example metaclass is at mvc.adapters.metaclasses and a model
            implementing it at adapters.gtk_support.basic
        """
        if hasattr(adapter_cls, 'widget_types'):
            if hasattr(adapter_cls, 'toolkit'):
                adapter_registry = cls.toolkit_registry.get_or_create_registry(adapter_cls.toolkit)
                logger.debug("Registering %s as handler for widget types '%s' in toolkit '%s'" % (adapter_cls, adapter_cls.widget_types, adapter_cls.toolkit))
                for widget_type in adapter_cls.widget_types:
                    adapter_registry[widget_type] = adapter_cls

        else:
            logger.debug("Ignoring '%s' as handler: no 'toolkit' or 'widget_types' defined" % adapter_cls)
        return adapter_cls


for toolkit_module in ToolkitRegistry.toolkit_modules:
    if toolkit_module.startswith('.'):
        package = __name__.rpartition('.')[0]
        try:
            tk_mod = importlib.import_module(toolkit_module, package=package)
            tkreg = AdapterRegistry.toolkit_registry.get_or_create_registry(tk_mod.toolkit)
            tk_mod.load(tkreg)
        except ImportError:
            logger.warning("Could not load toolkit support module '%s'" % (toolkit_module,))

AdapterRegistry.toolkit_registry.select_toolkit(TOOLKIT)