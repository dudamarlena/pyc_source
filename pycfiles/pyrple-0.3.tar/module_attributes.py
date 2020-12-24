# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyrpl/module_attributes.py
# Compiled at: 2017-08-29 09:44:06
from .attributes import *
from .modules import *

class ModuleProperty(ModuleAttribute):
    """
    A property for a submodule.

    The ModuleAttribute is declared with:
    ModuleAttribute(module_cls, default, doc)

    The module_cls is instantiated in the __init__ of the parent module

    For the moment, the following actions are supported:
       - module.sub = dict(...) : module.sub.set_setup_attributes(dict(...))
       - module.sub: returns the submodule.
    """
    default = {}

    def __init__(self, module_cls, default=None, doc='', ignore_errors=False, call_setup=False, **kwargs):
        self.module_cls = module_cls
        self.kwargs = kwargs
        ModuleAttribute.__init__(self, default=default, doc=doc, ignore_errors=ignore_errors, call_setup=call_setup)

    def set_value(self, obj, val):
        """
        Use the dictionnary val to set_setup_attributes
        :param obj:
        :param val:
        :return:
        """
        getattr(obj, self.name).setup_attributes = val
        return val

    def get_value(self, obj):
        if not hasattr(obj, '_' + self.name):
            setattr(obj, '_' + self.name, self._create_module(obj))
        return getattr(obj, '_' + self.name)

    def _create_module(self, obj):
        return self.module_cls(obj, name=self.name, **self.kwargs)


class ModuleList(Module, list):
    """ a list of modules"""

    def __init__(self, parent, name=None, element_cls=Module, default=[]):

        def element_name(element_self):
            """ function that is used to dynamically assign each
            ModuleListElement's name to the index in the list.
            This is needed for proper storage in the config file"""
            try:
                return element_self.parent.index(element_self)
            except ValueError:
                return element_self._initial_name

        def element_next(element_self):
            try:
                return element_self.parent[(element_self.parent.index(element_self) + 1)]
            except:
                return

            return

        def element_init(element_self, parent, initial_name=None, *args, **kwargs):
            element_self._initial_name = initial_name
            return element_cls.__init__(element_self, parent, *args, **kwargs)

        self.element_cls = type(element_cls.__name__ + 'ListElement', (
         element_cls,), {'name': property(fget=element_name), 'next': property(fget=element_next), 
           '__init__': element_init})
        self._signal_launcher = self.element_cls._signal_launcher
        super(ModuleList, self).__init__(parent, name=name)
        self.extend(default)
        return

    def __setitem__(self, index, value):
        self[index].setup_attributes = value

    def insert(self, index, new):
        super(ModuleList, self).insert(index, None)
        super(ModuleList, self).__setitem__(index, self.element_cls(self, initial_name=index))
        self[index]._initial_name = None
        self[index].setup_attributes = new
        self.save_state()
        return

    def append(self, new):
        self.insert(self.__len__(), new)

    def extend(self, iterable):
        for i in iterable:
            self.append(i)

    def __delitem__(self, index=-1):
        self[index]._initial_name = index
        to_delete = super(ModuleList, self).pop(index)
        to_delete._clear()
        self.c._pop(index)

    def pop(self, index=-1):
        setup_attributes = self[index].setup_attributes
        self.__delitem__(index)
        return setup_attributes

    def remove(self, value):
        self.__delitem__(self.index(value))

    def __repr__(self):
        return str(ModuleList.__name__) + '(' + list.__repr__(self) + ')'

    @property
    def setup_attributes(self):
        return [ item.setup_attributes for item in self ]

    @setup_attributes.setter
    def setup_attributes(self, val):
        for i, v in enumerate(val):
            try:
                self[i] = v
            except IndexError:
                self.append(v)

        while len(self) > len(val):
            self.__delitem__(-1)

    def _load_setup_attributes(self):
        """
         Load and sets all setup attributes from config file
        """
        if self.c is not None:
            self.setup_attributes = self.c._data
        return


class ModuleListProperty(ModuleProperty):
    """
    A property for a list of submodules.
    """
    default = []
    module_cls = ModuleList

    def __init__(self, element_cls, default=None, doc='', ignore_errors=False):
        self.element_cls = element_cls
        ModuleProperty.__init__(self, self.module_cls, default=default, doc=doc, ignore_errors=ignore_errors)

    def _create_module(self, obj):
        newmodule = self.module_cls(obj, name=self.name, element_cls=self.element_cls, default=self.default)
        try:
            newmodule._widget_class = self._widget_class
        except AttributeError:
            pass

        return newmodule

    def validate_and_normalize(self, obj, value):
        """ ensures that only list-like values are passed to the ModuleProperty """
        if not isinstance(value, list):
            try:
                value = value.values()
            except AttributeError:
                raise ValueError('ModuleProperty must be assigned a list. You have wrongly assigned an object of type %s. ', type(value))

        return value


class ModuleDict(Module):
    """
    container class that loosely resembles a dictionary which contains submodules
    """

    def __getitem__(self, key):
        return getattr(self, key)

    def keys(self):
        return self._module_attributes

    def values(self):
        return [ self[k] for k in self.keys() ]

    def items(self):
        return [ (k, self[k]) for k in self.keys() ]

    def __iter__(self):
        return iter(self.values())

    @property
    def setup_attributes(self):
        return super(ModuleDict, self).setup_attributes

    @setup_attributes.setter
    def setup_attributes(self, kwds):
        Module.setup_attributes.fset(self, {k:v for k, v in kwds.items() if k in self._setup_attributes})

    def __setitem__(self, key, value):
        mp = ModuleProperty(value)
        mp.name = key
        setattr(self.__class__, key, mp)
        self._module_attributes.append(key)
        self._setup_attributes.append(key)
        self[key].name = key
        self[key]._load_setup_attributes()

    def __delitem__(self, key):
        self._module_attributes.pop(key)
        self._setup_attributes.pop(key)
        getattr(self, key)._clear()
        delattr(self, key)

    def pop(self, key):
        """ same as __delattr__ (does not return a value) """
        module = self._setup_attributes.pop(key)
        delattr(self, key)
        return module


class ModuleDictProperty(ModuleProperty):
    default_module_cls = Module

    def __init__(self, module_cls=None, default=None, doc='', ignore_errors=False, **kwargs):
        """
        returns a descriptor for a module container, i.e. a class that contains submodules whose name and class are
        specified in kwargs. module_cls is the base class for the module container (typically SoftwareModule)
        """
        if module_cls is None:
            module_cls = self.default_module_cls
        ModuleDictClassInstance = type(module_cls.__name__ + 'DictPropertyInstance', (
         ModuleDict, module_cls), {key:ModuleProperty(value) for key, value in kwargs.items()})
        super(ModuleDictProperty, self).__init__(ModuleDictClassInstance, default=default, doc=doc, ignore_errors=ignore_errors)
        return