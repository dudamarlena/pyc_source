# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/zeta/ccore.py
# Compiled at: 2010-01-24 10:23:28
"""Everything can be a component.
  Component :

    * The ComponentMeta acts as the metaclass for all the Component derived
      classes.
    * Components with 'abstract' attribute set to True will not be registered
      for interface.
    * Components can only have no-argument initializers, like,
        def __init__( self ) 

    * implements. When a component implements an interface, it can declare so
      by calling the implements() api.
    * ExtensionPoint property can be instantiated to extend the functionality
      of a component through interfaces.

  Component Manager :

    * Normally ComponentManager class is instantiated as an environment object
      and binded to the Component objects as and when the Component objects are
      instantiated.
  
  Interfaces and Extension points :

    * Interfaces are used to extend the functionality of Zeta framework and
      currently it is used to implement view templates, plugins and more. 
"""
from zeta.lib.error import ZetaComponentError

class Interface(object):
    """Marker base class for extension point interfaces."""
    pass


class ExtensionPoint(property):
    """Marker class for extension points in components."""

    def __init__(self, interface):
        """Create the extension point.
        
        @param interface: the `Interface` subclass that defines the protocol
                          for the extension point
        """
        property.__init__(self, self.extensions)
        self.interface = interface
        self.__doc__ = 'List of components that implement `%s`' % self.interface.__name__

    def extensions(self, component):
        """Return a list of components that declare to implement the extension
        point interface.
        """
        extensions = ComponentMeta._registry.get(self.interface, [])
        return filter(None, [ component.compmgr[cls] for cls in extensions ])

    def __repr__(self):
        """Return a textual representation of the extension point."""
        return '<ExtensionPoint %s>' % self.interface.__name__


class ComponentMeta(type):
    """Meta class for components.
    
    Takes care of component and extension point registration.
    """
    _components = []
    _registry = {}
    _formcomps = {}

    def __new__(cls, name, bases, d):
        """Create the component class."""
        new_class = type.__new__(cls, name, bases, d)
        if name == 'Component':
            return new_class
        if True not in [ issubclass(x, ComponentManager) for x in bases ]:
            init = d.get('__init__')
            if not init:
                for init in [ b.__init__._original for b in new_class.mro() if issubclass(b, Component) if '__init__' in b.__dict__
                            ]:
                    break

            def maybe_init(self, compmgr, init=init, cls=new_class):
                """Component Init function hooked in by ComponentMeta."""
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

        if 'formname' in d:
            if isinstance(d.get('formname'), str):
                ComponentMeta._formcomps.setdefault(d.get('formname'), new_class)
            elif isinstance(d.get('formname'), list):
                [ ComponentMeta._formcomps.setdefault(f, new_class) for f in d.get('formname') ]
        return new_class


class Component(object):
    """Base class for components.

    Every component can declare what extension points it provides, as well as
    what extension points of other components it extends.
    """
    __metaclass__ = ComponentMeta

    def __new__(cls, *args, **kwargs):
        """Return an existing instance of the component if it has already been
        activated, otherwise create a new instance.
        """
        if issubclass(cls, ComponentManager):
            self = super(Component, cls).__new__(cls)
            self.compmgr = self
            return self
        else:
            compmgr = args[0]
            self = compmgr.components.get(cls)
            if self is None:
                self = super(Component, cls).__new__(cls)
                self.compmgr = compmgr
                compmgr.component_activated(self)
            return self

    @staticmethod
    def implements(*interfaces):
        """Can be used in the class definiton of `Component` subclasses to
        declare the extension points that are extended.
        """
        import sys
        frame = sys._getframe(1)
        locals_ = frame.f_locals
        assert locals_ is not frame.f_globals and '__module__' in locals_, 'implements() can only be used in a class definition'
        locals_.setdefault('_implements', []).extend(interfaces)


implements = Component.implements

class ComponentManager(object):
    """The component manager keeps a pool of active components."""

    def __init__(self):
        """Initialize the component manager."""
        self.components = {}
        self.enabled = {}
        if isinstance(self, Component):
            self.components[self.__class__] = self

    def __contains__(self, cls):
        """Return wether the given class is in the list of active components."""
        return cls in self.components

    def __getitem__(self, cls):
        """Activate the component instance for the given class, or return the
        existing the instance if the component has already been activated.
        """
        if cls not in self.enabled:
            self.enabled[cls] = self.is_component_enabled(cls)
        if not self.enabled[cls]:
            return None
        else:
            component = self.components.get(cls)
            if not component:
                if cls not in ComponentMeta._components:
                    raise ZetaComponentError('Component "%s" not registered' % cls.__name__)
                try:
                    component = cls(self)
                except TypeError, e:
                    raise ZetaComponentError('Unable to instantiate component %r (%s)' % (cls, e))

            return component

    def component_activated(self, component):
        """Can be overridden by sub-classes so that special initialization for
        components can be provided.
        """
        pass

    def is_component_enabled(self, cls):
        """Can be overridden by sub-classes to veto the activation of a
        component.

        If this method returns False, the component with the given class will
        not be available.
        """
        return True


def formcomponent(formname):
    """Get the component class implementing `formname` component"""
    return ComponentMeta._formcomps.get(formname, None)