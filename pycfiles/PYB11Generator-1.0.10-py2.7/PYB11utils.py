# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/PYB11Generator/PYB11utils.py
# Compiled at: 2019-12-14 00:13:17
from PYB11Decorators import *
import inspect, StringIO, types, itertools

def PYB11copy_func(f, name=None):
    """
    return a function with same code, globals, defaults, closure, and 
    name (or provide a new name)
    """
    fn = types.FunctionType(f.__code__, f.__globals__, name or f.__name__, f.__defaults__, f.__closure__)
    fn.__dict__.update(f.__dict__)
    return fn


def PYB11inject(fromcls, tocls, virtual=None, pure_virtual=None):
    assert not (virtual and pure_virtual), 'PYB11inject: cannot specify both virtual and pure_virtual as True!'
    names = [ x for x in dir(fromcls) if inspect.ismethod(eval('fromcls.%s' % x)) ]
    for name in names:
        exec 'tocls.%(name)s = PYB11copy_func(fromcls.%(name)s)' % {'name': name}
        if virtual is not None:
            exec 'tocls.%s.__dict__["PYB11virtual"] = %s' % (name, virtual)
        if pure_virtual is not None:
            exec 'tocls.%s.__dict__["PYB11pure_virtual"] = %s' % (name, pure_virtual)

    from PYB11class import PYB11TemplateMethod
    names = [ x for x in dir(fromcls) if isinstance(eval('fromcls.%s' % x), PYB11TemplateMethod) ]
    for name in names:
        exec 'tocls.%(name)s = PYB11TemplateMethod(func_template = fromcls.%(name)s.func_template,\n                                                     template_parameters = [x[1] for x in fromcls.%(name)s.template_parameters],\n                                                     cppname = fromcls.%(name)s.cppname,\n                                                     pyname = fromcls.%(name)s.pyname,\n                                                     docext = fromcls.%(name)s.docext)' % {'name': name}

    from PYB11property import PYB11property
    names = [ x for x in dir(fromcls) if isinstance(eval('fromcls.%s' % x), PYB11property) ]
    for name in names:
        exec 'tocls.%(name)s = PYB11property(returnType = fromcls.%(name)s.returnType,\n                                               getter = fromcls.%(name)s.getter,\n                                               setter = fromcls.%(name)s.setter,\n                                               doc = fromcls.%(name)s.doc,\n                                               getterraw = fromcls.%(name)s.getterraw,\n                                               setterraw = fromcls.%(name)s.setterraw,\n                                               getterconst = fromcls.%(name)s.getterconst,\n                                               setterconst = fromcls.%(name)s.setterconst,\n                                               static = fromcls.%(name)s.static,\n                                               returnpolicy = fromcls.%(name)s.returnpolicy)' % {'name': name}

    from PYB11ClassAttribute import PYB11ClassAttribute
    names = [ x for x in dir(fromcls) if isinstance(eval('fromcls.%s' % x), PYB11ClassAttribute) ]
    for name in names:
        exec 'tocls.%(name)s = PYB11ClassAttribute(static = fromcls.%(name)s.static,\n                                                     pyname = fromcls.%(name)s.pyname,\n                                                     cppname = fromcls.%(name)s.cppname,\n                                                     returnpolicy = fromcls.%(name)s.returnpolicy,\n                                                     doc = fromcls.%(name)s.doc,\n                                                     deftype = fromcls.%(name)s.deftype)' % {'name': name}

    return


def PYB11getBaseClasses(klass):
    stuff = inspect.getclasstree(inspect.getmro(klass), unique=True)

    def flatten(s, result):
        if type(s) is list:
            for val in s:
                s = flatten(val, result)

        else:
            result.append(s)

    flatstuff = []
    flatten(stuff, flatstuff)
    result = {k[0]:k[1] for k in flatstuff}
    return result


def PYB11sort_by_line(stuff):
    from PYB11class import PYB11TemplateClass
    name, obj = stuff
    if isinstance(obj, PYB11TemplateClass):
        try:
            source, lineno = inspect.findsource(obj.klass_template)
        except:
            raise RuntimeError, 'Cannot find source for %s?' % name

        return lineno
    try:
        source, lineno = inspect.findsource(obj)
    except:
        raise RuntimeError, 'Cannot find source for %s?' % name

    return lineno


class PYB11sort_by_inheritance:

    def __init__(self, klasses):
        from PYB11class import PYB11TemplateClass
        self.keys = {}
        for name, obj in klasses:
            if isinstance(obj, PYB11TemplateClass):
                klass = obj.klass_template
            else:
                klass = obj
            self.keys[klass] = PYB11sort_by_line((name, klass))

        changed = True
        while changed:
            changed = False
            for name, obj in klasses:
                if isinstance(obj, PYB11TemplateClass):
                    klass = obj.klass_template
                else:
                    klass = obj
                for bklass in inspect.getmro(klass)[1:]:
                    if bklass in self.keys and self.keys[klass] <= self.keys[bklass]:
                        self.keys[klass] = self.keys[bklass] + 1
                        changed = True

    def __call__(self, stuff):
        from PYB11class import PYB11TemplateClass
        obj = stuff[1]
        if isinstance(obj, PYB11TemplateClass):
            klass = obj.klass_template
        else:
            klass = obj
        return self.keys[klass]


def PYB11classes(modobj):
    result = [ (name, cls) for name, cls in inspect.getmembers(modobj, predicate=inspect.isclass) if name[:5] != 'PYB11'
             ]
    return sorted(result, key=PYB11sort_by_line)


def PYB11othermods(modobj):
    if hasattr(modobj, 'import_modules'):
        return modobj.import_modules
    else:
        return []


def PYB11classTemplateInsts(modobj):
    from PYB11class import PYB11TemplateClass
    result = [ x for x in dir(modobj) if isinstance(eval('modobj.%s' % x), PYB11TemplateClass) ]
    result = [ (x, eval('modobj.%s' % x)) for x in result ]
    return sorted(result, key=PYB11sort_by_line)


def PYB11ClassMethods(obj):
    result = inspect.getmembers(obj, predicate=inspect.ismethod)
    try:
        result.sort(key=PYB11sort_by_line)
    except:
        pass

    return result


def PYB11ThisClassMethods(obj):
    result = PYB11ClassMethods(obj)
    return [ (name, meth) for name, meth in result if name in obj.__dict__ ]


def PYB11functions(modobj):
    result = [ (name, meth) for name, meth in inspect.getmembers(modobj, predicate=inspect.isfunction) if name[:5] != 'PYB11'
             ]
    try:
        result.sort(key=PYB11sort_by_line)
    except:
        pass

    return result


def PYB11parseArgs(meth):
    stuff = inspect.getargspec(meth)
    result = []
    if stuff.defaults:
        nargs = len(stuff.defaults)
        for argName, val in zip(stuff.args[-nargs:], stuff.defaults):
            if isinstance(val, tuple):
                assert len(val) == 2
                argType, default = val
            else:
                argType, default = val, None
            result.append((argType, argName, default))

    return result


def PYB11recurseTemplateDict(Tdict):
    done = False
    itcount = 0
    while not done and itcount < 100:
        done = True
        itcount += 1
        for key, val in Tdict.iteritems():
            if '%(' in val:
                done = False
                Tdict[key] = val % Tdict

    if itcount == 100:
        raise RuntimeError, 'PYB11recurseTemplate failed to resolve all values in %s' % Tdict
    return Tdict


def PYB11parseTemplates(attrs, bklasses=None):
    Tdict = {key.split()[1]:key.split()[1] for key in attrs['template']}
    if attrs['template_dict']:
        for key, value in attrs['template_dict'].items():
            if key not in Tdict:
                Tdict[key] = value

    if bklasses is not None:
        for bklass in bklasses:
            bklassattrs = PYB11attrs(bklass)
            if bklassattrs['template_dict']:
                for key, value in bklassattrs['template_dict'].items():
                    if key not in Tdict:
                        Tdict[key] = value

    Tdict = PYB11recurseTemplateDict(Tdict)
    return Tdict


def PYB11virtualClass(klass):
    klassattrs = PYB11attrs(klass)
    allmethods = PYB11ClassMethods(klass)
    virtual = False
    for mname, meth in allmethods:
        methattrs = PYB11attrs(meth)
        if methattrs['virtual'] or methattrs['pure_virtual']:
            virtual = True

    return virtual


def PYB11protectedClass(klass):
    klassattrs = PYB11attrs(klass)
    allmethods = PYB11ThisClassMethods(klass)
    protected = False
    for mname, meth in allmethods:
        methattrs = PYB11attrs(meth)
        if methattrs['protected']:
            protected = True

    return protected


def PYB11badchars(name):
    return any(c in ('<', '>', ',') for c in name)


def PYB11mangle(name):
    result = name.replace('<', '__').replace('>', '__').replace('::', '_').replace(', ', '_').replace(',', '_').replace('*', '_ptr_').replace('&', '_ampsnd_').replace(' ', '_')
    return result


def PYB11union_dict(*args):
    result = {}
    for d in args:
        for key in d:
            result[key] = d[key]

    return result


def PYB11CPPsafe(string):
    return string.replace(',', ' PYB11COMMA ')


def PYB11cppname_exts(templateargs):
    tt, mt = ('', '')
    if templateargs:
        tt = '<'
        for i, arg in enumerate(templateargs):
            arg = arg.split()[1]
            if i < len(templateargs) - 1:
                tt += '%s,' % arg
            else:
                tt += '%s>' % arg

        mt = PYB11mangle(tt)
    return (
     tt, mt)


class PYB11indentedIO:

    def __init__(self, prefix):
        self.prefix = prefix
        self.fs = StringIO.StringIO()

    def __call__(self, stuff):
        newstuff = stuff.replace('\n', '\n' + self.prefix)
        self.fs.write(newstuff)

    def getvalue(self):
        return self.fs.getvalue()

    def close(self):
        self.fs.close()


def PYB11docstring(doc, ss):
    if doc:
        stuff = doc.split('\n')
        if len(stuff) == 1:
            ss('"%s"' % doc.replace('"', '\\"'))
        else:
            ss('\n')
            for i, line in enumerate(doc.split('\n')):
                ss('            "%s\\n"' % line.replace('"', '\\"'))
                if i < len(stuff) - 1:
                    ss('\n')


def PYB11attrs(obj):
    d = {'pyname': obj.__name__, 'cppname': obj.__name__, 
       'ignore': False, 
       'namespace': '', 
       'singleton': False, 
       'holder': None, 
       'exposeBaseOverloads': True, 
       'dynamic_attr': None, 
       'virtual': False, 
       'pure_virtual': False, 
       'protected': False, 
       'const': False, 
       'static': False, 
       'noconvert': False, 
       'implementation': None, 
       'returnpolicy': None, 
       'keepalive': None, 
       'call_guard': None, 
       'template': (), 
       'template_dict': {}, 'module': {}}
    for key in d:
        if hasattr(obj, 'PYB11' + key):
            d[key] = eval('obj.PYB11%s' % key)

    safeexts = PYB11cppname_exts(d['template'])
    d['full_cppname'] = d['cppname'] + safeexts[0]
    d['mangle_cppname'] = d['cppname'] + safeexts[1]
    return d