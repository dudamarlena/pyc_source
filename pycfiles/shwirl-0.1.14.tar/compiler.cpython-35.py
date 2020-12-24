# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/danyvohl/code/shwirl/extern/vispy/visuals/shaders/compiler.py
# Compiled at: 2017-04-05 22:13:00
# Size of source mod 2**32: 7684 bytes
from __future__ import division
import re
from ... import gloo

class Compiler(object):
    __doc__ = "\n    Compiler is used to convert Function and Variable instances into\n    ready-to-use GLSL code. This class handles name mangling to ensure that\n    there are no name collisions amongst global objects. The final name of\n    each object may be retrieved using ``Compiler.__getitem__(obj)``.\n\n    Accepts multiple root Functions as keyword arguments. ``compile()`` then\n    returns a dict of GLSL strings with the same keys.\n\n    Example::\n\n        # initialize with two main functions\n        compiler = Compiler(vert=v_func, frag=f_func)\n\n        # compile and extract shaders\n        code = compiler.compile()\n        v_code = code['vert']\n        f_code = code['frag']\n\n        # look up name of some object\n        name = compiler[obj]\n\n    "

    def __init__(self, namespace=None, **shaders):
        if namespace is None:
            namespace = {}
        self._object_names = namespace
        self.shaders = shaders

    def __getitem__(self, item):
        """
        Return the name of the specified object, if it has been assigned one.
        """
        return self._object_names[item]

    def compile(self, pretty=True):
        """ Compile all code and return a dict {name: code} where the keys
        are determined by the keyword arguments passed to __init__().

        Parameters
        ----------
        pretty : bool
            If True, use a slower method to mangle object names. This produces
            GLSL that is more readable.
            If False, then the output is mostly unreadable GLSL, but is about
            10x faster to compile.

        """
        self._object_names = {}
        self._shader_deps = {}
        for shader_name, shader in self.shaders.items():
            this_shader_deps = []
            self._shader_deps[shader_name] = this_shader_deps
            dep_set = set()
            for dep in shader.dependencies(sort=True):
                if not dep.name is None:
                    if dep in dep_set:
                        pass
                    else:
                        this_shader_deps.append(dep)
                        dep_set.add(dep)

        if pretty:
            self._rename_objects_pretty()
        else:
            self._rename_objects_fast()
        compiled = {}
        obj_names = self._object_names
        for shader_name, shader in self.shaders.items():
            code = []
            for dep in self._shader_deps[shader_name]:
                dep_code = dep.definition(obj_names)
                if dep_code is not None:
                    regex = '#version (\\d+)'
                    m = re.search(regex, dep_code)
                    if m is not None:
                        if m.group(1) != '120':
                            raise RuntimeError('Currently only GLSL #version 120 is supported.')
                        dep_code = re.sub(regex, '', dep_code)
                    code.append(dep_code)

            compiled[shader_name] = '\n'.join(code)

        self.code = compiled
        return compiled

    def _rename_objects_fast(self):
        """ Rename all objects quickly to guaranteed-unique names using the
        id() of each object.

        This produces mostly unreadable GLSL, but is about 10x faster to
        compile.
        """
        for shader_name, deps in self._shader_deps.items():
            for dep in deps:
                name = dep.name
                if name != 'main':
                    ext = '_%x' % id(dep)
                    name = name[:32 - len(ext)] + ext
                self._object_names[dep] = name

    def _rename_objects_pretty(self):
        """ Rename all objects like "name_1" to avoid conflicts. Objects are
        only renamed if necessary.

        This method produces more readable GLSL, but is rather slow.
        """
        self._global_ns = dict([(kwd, None) for kwd in gloo.util.KEYWORDS])
        self._shader_ns = dict([(shader, {}) for shader in self.shaders])
        obj_shaders = {}
        for shader_name, deps in self._shader_deps.items():
            for dep in deps:
                for name in dep.static_names():
                    self._global_ns[name] = None

                obj_shaders.setdefault(dep, []).append(shader_name)

        name_index = {}
        for obj, shaders in obj_shaders.items():
            name = obj.name
            if self._name_available(obj, name, shaders):
                self._assign_name(obj, name, shaders)
            else:
                while True:
                    index = name_index.get(name, 0) + 1
                    name_index[name] = index
                    ext = '_%d' % index
                    new_name = name[:32 - len(ext)] + ext
                    if self._name_available(obj, new_name, shaders):
                        self._assign_name(obj, new_name, shaders)
                        break

    def _is_global(self, obj):
        """ Return True if *obj* should be declared in the global namespace.

        Some objects need to be declared only in per-shader namespaces:
        functions, static variables, and const variables may all be given
        different definitions in each shader.
        """
        from .variable import Variable
        return isinstance(obj, Variable)

    def _name_available(self, obj, name, shaders):
        """ Return True if *name* is available for *obj* in *shaders*.
        """
        if name in self._global_ns:
            return False
        shaders = self.shaders if self._is_global(obj) else shaders
        for shader in shaders:
            if name in self._shader_ns[shader]:
                return False

        return True

    def _assign_name(self, obj, name, shaders):
        """ Assign *name* to *obj* in *shaders*.
        """
        if self._is_global(obj):
            assert name not in self._global_ns
            self._global_ns[name] = obj
        else:
            for shader in shaders:
                ns = self._shader_ns[shader]
                assert name not in ns
                ns[name] = obj

        self._object_names[obj] = name