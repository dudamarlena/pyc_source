# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/vohl/Documents/code/shwirl/shwirl/extern/vispy/visuals/shaders/shader_object.py
# Compiled at: 2018-10-01 14:58:41
# Size of source mod 2**32: 5772 bytes
from weakref import WeakKeyDictionary
from ext.ordereddict import OrderedDict
from ext.six import string_types
from .compiler import Compiler

class ShaderObject(object):
    __doc__ = ' Base class for all objects that may be included in a GLSL program\n    (Functions, Variables, Expressions).\n    \n    Shader objects have a *definition* that defines the object in GLSL, an \n    *expression* that is used to reference the object, and a set of \n    *dependencies* that must be declared before the object is used.\n    \n    Dependencies are tracked hierarchically such that changes to any object\n    will be propagated up the dependency hierarchy to trigger a recompile.\n    '

    @classmethod
    def create(self, obj, ref=None):
        """ Convert *obj* to a new ShaderObject. If the output is a Variable
        with no name, then set its name using *ref*. 
        """
        if isinstance(ref, Variable):
            ref = ref.name
        else:
            if isinstance(ref, string_types):
                if ref.startswith('gl_'):
                    ref = ref[3:].lower()
            elif hasattr(obj, '_shader_object'):
                obj = obj._shader_object()
            elif isinstance(obj, ShaderObject):
                if isinstance(obj, Variable) and obj.name is None:
                    obj.name = ref
            elif isinstance(obj, string_types):
                obj = TextExpression(obj)
            else:
                obj = Variable(ref, obj)
                if obj.vtype:
                    if obj.vtype[0] in 'auv':
                        obj.name = obj.vtype[0] + '_' + obj.name
            return obj

    def __init__(self):
        self._deps = OrderedDict()
        self._dependents = WeakKeyDictionary()

    @property
    def name(self):
        """ The name of this shader object.
        """
        pass

    def definition(self, obj_names):
        """ Return the GLSL definition for this object. Use *obj_names* to
        determine the names of dependencies.
        """
        pass

    def expression(self, obj_names):
        """ Return the GLSL expression used to reference this object inline.
        """
        return obj_names[self]

    def dependencies(self, sort=False):
        """ Return all dependencies required to use this object. The last item 
        in the list is *self*.
        """
        alldeps = []
        if sort:

            def key(obj):
                if not isinstance(obj, Variable):
                    return (0, 0)
                return (1, obj.vtype)

            deps = sorted((self._deps), key=key)
        else:
            deps = self._deps
        for dep in deps:
            alldeps.extend(dep.dependencies(sort=sort))

        alldeps.append(self)
        return alldeps

    def static_names(self):
        """ Return a list of names that are declared in this object's 
        definition (not including the name of the object itself).
        
        These names will be reserved by the compiler when automatically 
        determining object names.
        """
        return []

    def _add_dep(self, dep):
        """ Increment the reference count for *dep*. If this is a new 
        dependency, then connect to its *changed* event.
        """
        if dep in self._deps:
            self._deps[dep] += 1
        else:
            self._deps[dep] = 1
            dep._dependents[self] = None

    def _remove_dep(self, dep):
        """ Decrement the reference count for *dep*. If the reference count 
        reaches 0, then the dependency is removed and its *changed* event is
        disconnected.
        """
        refcount = self._deps[dep]
        if refcount == 1:
            self._deps.pop(dep)
            dep._dependents.pop(self)
        else:
            self._deps[dep] -= 1

    def _dep_changed(self, dep, code_changed=False, value_changed=False):
        """ Called when a dependency's expression has changed.
        """
        self.changed(code_changed, value_changed)

    def changed(self, code_changed=False, value_changed=False):
        """Inform dependents that this shaderobject has changed.
        """
        for d in self._dependents:
            d._dep_changed(self, code_changed=code_changed, value_changed=value_changed)

    def compile(self):
        """ Return a compilation of this object and its dependencies. 
        
        Note: this is mainly for debugging purposes; the names in this code
        are not guaranteed to match names in any other compilations. Use
        Compiler directly to ensure consistent naming across multiple objects. 
        """
        compiler = Compiler(obj=self)
        return compiler.compile()['obj']

    def __repr__(self):
        if self.name is not None:
            return '<%s "%s" at 0x%x>' % (self.__class__.__name__,
             self.name, id(self))
        return '<%s at 0x%x>' % (self.__class__.__name__, id(self))


from .variable import Variable
from .expression import TextExpression