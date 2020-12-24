# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/PYB11Generator/__init__.py
# Compiled at: 2019-03-04 00:14:46
import inspect, sys
from PYB11utils import *
from PYB11Decorators import *
from PYB11STLmethods import *
from PYB11function import *
from PYB11class import *
from PYB11Publicist import *
from PYB11enum import *
from PYB11attr import *

def PYB11generateModule(modobj, name=None):
    if name is None:
        name = modobj.__name__
    modobj.PYB11modulename = name
    with open(name + '.cc', 'w') as (f):
        ss = f.write
        PYB11generateModuleStart(modobj, ss, name)
        PYB11generateModuleEnums(modobj, ss)
        PYB11generateModuleSTL(modobj, ss)
        PYB11generateModuleClasses(modobj, ss)
        PYB11generateModuleFunctions(modobj, ss)
        PYB11generateModuleAttrs(modobj, ss)
        ss('}\n')
        f.close()
    return


def PYB11generateModuleStart(modobj, ss, name):
    ss('//------------------------------------------------------------------------------\n// Module %(name)s\n//------------------------------------------------------------------------------\n// Put Python includes first to avoid compile warnings about redefining _POSIX_C_SOURCE\n#include "pybind11/pybind11.h"\n#include "pybind11/stl_bind.h"\n#include "pybind11/stl.h"\n#include "pybind11/functional.h"\n#include "pybind11/operators.h"\n\nnamespace py = pybind11;\nusing namespace pybind11::literals;\n\n#define PYB11COMMA ,\n\n' % {'name': name})
    if hasattr(modobj, 'PYB11includes'):
        for inc in modobj.PYB11includes:
            ss('#include %s\n' % inc)

        ss('\n')
    if hasattr(modobj, 'PYB11namespaces'):
        for ns in modobj.PYB11namespaces:
            ss('using namespace ' + ns + ';\n')

        ss('\n')
    if hasattr(modobj, 'PYB11scopenames'):
        for scopename in modobj.PYB11scopenames:
            ss('using ' + scopename + '\n')

        ss('\n')
    if hasattr(modobj, 'PYB11preamble'):
        ss(modobj.PYB11preamble + '\n')
        ss('\n')
    for objname, obj in PYB11STLobjs(modobj):
        obj.preamble(modobj, ss, objname)

    ss('\n')
    if hasattr(modobj, 'PYB11opaque'):
        for x in modobj.PYB11opaque:
            ss('PYBIND11_MAKE_OPAQUE(' + x.replace(',', ' PYB11COMMA ') + ')\n')

    PYB11generateModuleTrampolines(modobj, ss)
    PYB11generateModulePublicists(modobj, ss)
    ss('\n//------------------------------------------------------------------------------\n// Make the module\n//------------------------------------------------------------------------------\nPYBIND11_MODULE(%(name)s, m) {\n\n' % {'name': name})
    doc = inspect.getdoc(modobj)
    if doc:
        ss('  m.doc() = ')
        PYB11docstring(doc, ss)
        ss('  ;\n')
    ss('\n')
    if hasattr(modobj, 'PYB11modulepreamble'):
        ss(modobj.PYB11modulepreamble + '\n\n')
    othermods = PYB11othermods(modobj)
    for kname, klass in PYB11classes(modobj):
        klassattrs = PYB11attrs(klass)
        mods = klassattrs['module']
        for otherklass in mods:
            othermod = mods[otherklass]
            if othermod not in othermods:
                othermods.append(othermod)

    if othermods:
        ss('  // Import external modules\n')
        for othermod in othermods:
            if othermod != name:
                ss('  py::module::import("%s");\n' % othermod)

        ss('\n')