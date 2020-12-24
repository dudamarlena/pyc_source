# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/PYB11Generator/PYB11Trampoline.py
# Compiled at: 2019-12-14 00:48:57
import inspect, sys, StringIO
from PYB11utils import *

def PYB11generateModuleTrampolines(modobj, ss):
    klasses = PYB11classes(modobj)
    klasses = [ (name, klass) for name, klass in klasses if PYB11virtualClass(klass) ]
    newklasses = []
    known_trampolines = []
    for name, klass in klasses:
        klassattrs = PYB11attrs(klass)
        template_klass = len(klassattrs['template']) > 0
        mods = klassattrs['module']
        if (template_klass or not klassattrs['ignore']) and klassattrs['pyname'] not in known_trampolines and (klass not in mods or mods[klass] == modobj.PYB11modulename):
            newklasses.append((name, klass))
            known_trampolines.append(klassattrs['pyname'])

    klasses = newklasses
    for kname, klass in klasses:
        PYB11generateTrampoline(klass, ss)


def PYB11generateTrampoline(klass, ssout):
    klassattrs = PYB11attrs(klass)
    template_klass = len(klassattrs['template']) > 0
    fs = StringIO.StringIO()
    ss = fs.write
    Tdict = PYB11parseTemplates(klassattrs, inspect.getmro(klass))
    ss('//------------------------------------------------------------------------------\n// Trampoline class for %(cppname)s\n//------------------------------------------------------------------------------\n#ifndef __trampoline_%(pyname)s__\n#define __trampoline_%(pyname)s__\n\n' % klassattrs)
    for ns in klassattrs['namespace'].split('::')[:-1]:
        ss('namespace ' + ns + ' {\n')

    if template_klass:
        ss('template<')
        for i, name in enumerate(klassattrs['template']):
            if i < len(klassattrs['template']) - 1:
                ss('%s, ' % name)
            else:
                ss('%s>\n' % name)

    bklassnames = []
    for bklass in inspect.getmro(klass):
        bklassattrs = PYB11attrs(bklass)
        bklassname = '%(namespace)s%(cppname)s' % bklassattrs
        if len(bklassattrs['template']) > 0:
            bklassname += '<'
            for i, name in enumerate(bklassattrs['template']):
                assert len(name.split()) == 2
                nameval = name.split()[1]
                if name in klassattrs['template']:
                    bklassname += nameval
                else:
                    if nameval not in Tdict:
                        raise RuntimeError, 'Trampoline template base class error: %s is missing from specified template parameters %s\n  (class, base) = (%s, %s)' % (nameval, Tdict, klass, bklass)
                    bklassname += Tdict[nameval]
                if i < len(bklassattrs['template']) - 1:
                    bklassname += ', '

            bklassname += '>'
        bklassnames.append(bklassname)

    assert len(bklassnames) == len(inspect.getmro(klass))
    bklassnames[0] = 'PYB11self'
    ss('class PYB11Trampoline%(cppname)s: public %(full_cppname)s {\npublic:\n  using %(full_cppname)s::%(cppname)s;   // inherit constructors\n  typedef %(full_cppname)s PYB11self;    // Necessary to protect macros below from names with commas in them\n' % klassattrs)
    for bklassname in bklassnames[1:]:
        if bklassname != PYB11mangle(bklassname):
            ss('  typedef %s %s;\n' % (bklassname, PYB11mangle(bklassname)))

    if hasattr(klass, 'PYB11typedefs'):
        typedefs = str(klass.PYB11typedefs)
    else:
        typedefs = ''
    methfms = StringIO.StringIO()
    boundMethods = []
    for bklass, bklassname in zip(inspect.getmro(klass), bklassnames):
        bklassinst = bklass()
        bklassattrs = PYB11attrs(bklass)
        methods = [ (mname, meth) for mname, meth in PYB11ClassMethods(bklass) if not PYB11attrs(meth)['ignore'] and (PYB11attrs(meth)['virtual'] or PYB11attrs(meth)['pure_virtual']) and mname in bklass.__dict__
                  ]
        bklasssubs = {}
        for name in bklassattrs['template']:
            if name not in klassattrs['template']:
                nameval = name.split()[1]
                assert nameval in Tdict
                bklasssubs[name] = Tdict[nameval]

        for mname, meth in methods:
            fms = StringIO.StringIO()
            methattrs = PYB11attrs(meth)
            methattrs['returnType'] = eval('bklassinst.' + mname + '()')
            assert methattrs['returnType']
            fms.write('  virtual %(returnType)s %(cppname)s(' % methattrs)
            args = PYB11parseArgs(meth)
            for i, (argType, argName, default) in enumerate(args):
                fms.write('%s %s' % (argType, argName))
                if i < len(args) - 1:
                    fms.write(', ')

            if methattrs['const']:
                fms.write(') const override { ')
            else:
                fms.write(') override { ')
            try:
                thpt = fms.getvalue() % Tdict
            except:
                raise RuntimeError, 'Unable to generate call descriptor for %s in %s->%s' % (mname, str(klass), bklassname)

            if thpt not in boundMethods:
                boundMethods.append(fms.getvalue() % Tdict)
                returnType = methattrs['returnType']
                if PYB11badchars(returnType):
                    returnType = PYB11mangle(returnType)
                    typedefstring = '    typedef %s %s;\n' % (methattrs['returnType'], returnType)
                    if typedefstring not in typedefs:
                        typedefs += typedefstring
                    methattrs['returnType'] = returnType
                altered = False
                for i, (argType, argName, default) in enumerate(args):
                    if '&' in argType:
                        altered = True
                        fms.write('\n    py::object dummy%i = py::cast(&%s);\n' % (i, argName))

                if altered:
                    fms.write('    ')
                if methattrs['pure_virtual']:
                    fms.write('PYBIND11_OVERLOAD_PURE(%(returnType)s, PYB11self, %(cppname)s, ' % methattrs)
                else:
                    fms.write('PYBIND11_OVERLOAD(%(returnType)s, ' % methattrs)
                    fms.write(PYB11mangle(bklassname) + ', ')
                    fms.write('%(cppname)s, ' % methattrs)
                for i, (argType, argName, default) in enumerate(args):
                    if i < len(args) - 1:
                        fms.write(argName + ', ')
                    else:
                        fms.write(argName)

                if altered:
                    fms.write(');\n  }\n')
                else:
                    fms.write('); }\n')
                methfms.write(fms.getvalue())
            fms.close()

    ss(typedefs + '\n')
    ss(methfms.getvalue())
    methfms.close()
    ss('};\n\n')
    for ns in klassattrs['namespace'].split('::')[:-1]:
        ss('}\n')

    ss('\n#endif\n')
    ssout(fs.getvalue() % Tdict)