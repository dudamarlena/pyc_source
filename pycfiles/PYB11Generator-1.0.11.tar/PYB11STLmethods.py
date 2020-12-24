# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/PYB11Generator/PYB11STLmethods.py
# Compiled at: 2019-03-04 00:14:46
import inspect
from PYB11utils import *

class PYB11_bind_vector:

    def __init__(self, element, opaque=False, local=None):
        self.element = element
        self.opaque = opaque
        self.local = local

    def preamble(self, modobj, ss, name):
        if self.opaque:
            ss('PYBIND11_MAKE_OPAQUE(std::vector<' + PYB11CPPsafe(self.element) + '>)\n')

    def __call__(self, modobj, ss, name):
        ss('py::bind_vector<std::vector<' + self.element + '>>(m, "' + name + '"')
        if self.local is not None:
            ss(', py::module_local(')
            if self.local:
                ss('true)')
            else:
                ss('false)')
        ss(');\n')
        return


class PYB11_bind_map:

    def __init__(self, key, value, opaque=False, local=None):
        self.key = key
        self.value = value
        self.opaque = opaque
        self.local = local

    def preamble(self, modobj, ss, name):
        if self.opaque:
            cppname = 'std::map<' + self.key + ',' + self.value + '>'
            ss('PYBIND11_MAKE_OPAQUE(' + PYB11CPPsafe(cppname) + ');\n')

    def __call__(self, modobj, ss, name):
        ss('py::bind_map<std::map<' + self.key + ', ' + self.value + '>>(m, "' + name + '"')
        if self.local is not None:
            ss(', py::module_local(')
            if self.local:
                ss('true)')
            else:
                ss('false)')
        ss(');\n')
        return


def PYB11STLobjs(modobj):
    return [ (name, obj) for name, obj in inspect.getmembers(modobj) if name[:5] != 'PYB11' and (isinstance(obj, PYB11_bind_vector) or isinstance(obj, PYB11_bind_map))
           ]


def PYB11generateModuleSTL(modobj, ss):
    stuff = PYB11STLobjs(modobj)
    for name, obj in stuff:
        ss('  ')
        obj(modobj, ss, name)

    ss('\n')