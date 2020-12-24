# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\seishub\core\core.py
# Compiled at: 2010-12-23 17:42:43
from seishub.core.exceptions import SeisHubError
from zope.interface import Interface, Attribute
from zope.interface.declarations import _implements, classImplements
import sys
__all__ = [
 'Component', 'implements', 'Interface', 'ERROR', 'WARN', 'INFO',
 'DEBUG', 'ComponentMeta', 'ComponentManager', 'PackageManager',
 'DEBUGX']
ERROR = 1
WARN = 5
INFO = 10
DEBUG = 20

class ComponentMeta(type):
    """
    Meta class for components.
    
    Takes care of component and extension point registration.
    """
    _components = []
    _registry = {}

    def __new__(cls, name, bases, d):
        """
        Create the component class.
        """
        new_class = type.__new__(cls, name, bases, d)
        if name == 'Component':
            return new_class
        if True not in [ issubclass(x, ComponentManager) for x in bases ]:
            init = d.get('__init__')
            if not init:
                for init in [ b.__init__._original for b in new_class.mro() if issubclass(b, Component) and '__init__' in b.__dict__
                            ]:
                    break

            def maybe_init(self, compmgr, init=init, cls=new_class):
                if cls not in compmgr.components:
                    compmgr.components[cls] = self
                    if init:
                        try:
                            init(self)
                        except:
                            del compmgr.components[cls]
                            raise

            maybe_init._original = init
            new_class.__init__ = maybe_init
        if d.get('abstract'):
            return new_class
        ComponentMeta._components.append(new_class)
        registry = ComponentMeta._registry
        for interface in d.get('_implements', []):
            registry.setdefault(interface, []).append(new_class)

        for base in [ base for base in bases if hasattr(base, '_implements') ]:
            for interface in base._implements:
                registry.setdefault(interface, []).append(new_class)

        PackageManager._addClass(new_class)
        return new_class


class PackageManager(object):
    """
    Takes care of package registration.
    """
    _registry = {}

    @staticmethod
    def _addClass(cls):
        if not hasattr(cls, 'package_id'):
            return
        registry = PackageManager._registry
        registry.setdefault(cls.package_id, []).append(cls)

    @staticmethod
    def getClasses(interface, package_id=None):
        """
        Get classes implementing interface within specified package.
        """
        registry = PackageManager._registry
        classes = ComponentMeta._registry.get(interface, [])
        if package_id:
            classes = [ cls for cls in classes if cls in registry.get(package_id, []) ]
        return classes

    @staticmethod
    def getComponents(interface, package_id, component):
        """
        Get objects providing interface within specified package.
        """
        classes = PackageManager.getClasses(interface, package_id)
        return filter(None, [ component.compmgr[cls] for cls in classes ])

    @staticmethod
    def getPackageIds():
        """
        Get a list of ID's of all packages (enabled and disabled ones) 
        without activating any components.
        """
        return PackageManager._registry.keys()


class Component(object):
    """
    Base class for components.
    
    Every component can declare what extension points it provides, as well as
    what extension points of other components it extends.
    """
    __metaclass__ = ComponentMeta

    def __new__(cls, *args, **kwargs):
        """
        Return an existing instance of the component if it has already been
        activated, otherwise create a new instance.
        """
        if issubclass(cls, ComponentManager):
            self = super(Component, cls).__new__(cls)
            self.compmgr = self
            return self
        else:
            try:
                compmgr = args[0]
            except IndexError:
                raise TypeError('Component takes a component manager instance ' + 'as first argument.')

            self = compmgr.components.get(cls)
            if self is None:
                self = super(Component, cls).__new__(cls)
                self.compmgr = compmgr
                compmgr.initComponent(self)
            return self


def implements--- This code section failed: ---

 L. 177         0  LOAD_GLOBAL           0  'sys'
                3  LOAD_ATTR             1  '_getframe'
                6  LOAD_CONST               1
                9  CALL_FUNCTION_1       1  None
               12  STORE_FAST            1  'frame'

 L. 178        15  LOAD_FAST             1  'frame'
               18  LOAD_ATTR             2  'f_locals'
               21  STORE_FAST            2  'locals_'

 L. 180        24  LOAD_FAST             2  'locals_'
               27  LOAD_FAST             1  'frame'
               30  LOAD_ATTR             3  'f_globals'
               33  COMPARE_OP            9  is-not
               36  POP_JUMP_IF_FALSE    51  'to 51'
               39  LOAD_CONST               '__module__'
               42  LOAD_FAST             2  'locals_'
               45  COMPARE_OP            6  in
             48_0  COME_FROM            36  '36'
               48  POP_JUMP_IF_TRUE     60  'to 60'
               51  LOAD_ASSERT              AssertionError

 L. 181        54  LOAD_CONST               'implements() can only be used in a class definition'
               57  RAISE_VARARGS_2       2  None

 L. 182        60  LOAD_FAST             2  'locals_'
               63  LOAD_ATTR             5  'setdefault'
               66  LOAD_CONST               '_implements'
               69  BUILD_LIST_0          0 
               72  CALL_FUNCTION_2       2  None
               75  LOAD_ATTR             6  'extend'
               78  LOAD_FAST             0  'interfaces'
               81  CALL_FUNCTION_1       1  None
               84  POP_TOP          

 L. 184        85  LOAD_GLOBAL           7  '_implements'
               88  LOAD_CONST               'implements'
               91  LOAD_FAST             0  'interfaces'
               94  LOAD_GLOBAL           8  'classImplements'
               97  CALL_FUNCTION_3       3  None
              100  POP_TOP          

Parse error at or near `CALL_FUNCTION_3' instruction at offset 97


class ComponentManager(object):
    """
    The component manager keeps a pool of active components.
    """

    def __init__(self):
        """
        Initialize the component manager.
        """
        self.components = {}
        self.enabled = {}
        if isinstance(self, Component):
            self.components[self.__class__] = self

    def __contains__(self, cls):
        """
        Return if the given class is in the list of active components.
        """
        return cls in self.components

    def __getitem__(self, cls):
        """
        Activate the component instance for the given class, or return the
        existing the instance if the component has already been activated.
        """
        if cls not in self.enabled:
            self.enabled[cls] = self.isComponentEnabled(cls)
        if not self.enabled[cls]:
            return None
        else:
            component = self.components.get(cls)
            if not component:
                if cls not in ComponentMeta._components:
                    raise SeisHubError('Component "%s" not registered' % cls.__name__)
                try:
                    component = cls(self)
                except TypeError as e:
                    raise SeisHubError('Unable to instantiate component %r (%s)' % (
                     cls, e))

            return component

    def __delitem__(self, cls):
        del self.components[cls]

    def initComponent(self, component):
        """
        Can be overridden by sub-classes so that special initialization for
        components can be provided.
        """
        pass

    def isComponentEnabled(self, cls):
        """
        Can be overridden by sub-classes to veto the activation of a component.
        
        If this method returns False, the component with the given class will
        not be available.
        """
        return True