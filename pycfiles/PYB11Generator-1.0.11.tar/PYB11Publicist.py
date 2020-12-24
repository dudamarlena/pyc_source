# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/PYB11Generator/PYB11Publicist.py
# Compiled at: 2019-12-14 00:13:17
import inspect, sys, StringIO
from PYB11utils import *

def PYB11generateModulePublicists(modobj, ss):
    klasses = PYB11classes(modobj)
    known_publicists = []
    for kname, klass in klasses:
        klassattrs = PYB11attrs(klass)
        template_klass = len(klassattrs['template']) > 0
        mods = klassattrs['module']
        if PYB11protectedClass(klass) and (template_klass or not klassattrs['ignore']) and klassattrs['pyname'] not in known_publicists and (klass not in mods or mods[klass] == modobj.PYB11modulename):
            PYB11generatePublicist(klass, ss)


def PYB11generatePublicist(klass, ssout):
    klassattrs = PYB11attrs(klass)
    template_klass = len(klassattrs['template']) > 0
    if klassattrs['ignore'] and not template_klass:
        return
    fs = StringIO.StringIO()
    ss = fs.write
    Tdict = PYB11parseTemplates(klassattrs, inspect.getmro(klass))
    ss('//------------------------------------------------------------------------------\n// Publicist class for %(cppname)s\n//------------------------------------------------------------------------------\n#ifndef __publicist_%(pyname)s__\n#define __publicist_%(pyname)s__\n\n' % klassattrs)
    for ns in klassattrs['namespace'].split('::')[:-1]:
        ss('namespace ' + ns + ' {\n')

    if template_klass:
        ss('template<')
        for i, name in enumerate(klassattrs['template']):
            if i < len(klassattrs['template']) - 1:
                ss('%s, ' % name)
            else:
                ss('%s>\n' % name)

    ss('class PYB11Publicist%(cppname)s: public %(full_cppname)s {\npublic:\n' % klassattrs)
    if hasattr(klass, 'PYB11typedefs'):
        ss(klass.PYB11typedefs + '\n')
    methods = [ (mname, meth) for mname, meth in PYB11ClassMethods(klass) if PYB11attrs(meth)['protected'] and mname in klass.__dict__
              ]
    boundmeths = []
    for mname, meth in methods:
        methattrs = PYB11attrs(meth)
        if methattrs['cppname'] not in boundmeths:
            boundmeths.append(methattrs['cppname'])
            ss('  using %(full_cppname)s::' % klassattrs)
            ss('%(cppname)s;\n' % methattrs)

    ss('};\n\n')
    for ns in klassattrs['namespace'].split('::')[:-1]:
        ss('}\n')

    ss('\n#endif\n')
    ssout(fs.getvalue() % Tdict)