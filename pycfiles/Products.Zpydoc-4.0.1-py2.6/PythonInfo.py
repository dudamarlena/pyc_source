# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/Products/Zpydoc/inspectors/PythonInfo.py
# Compiled at: 2011-09-28 02:31:46
"""$id$"""
__version__ = '$Revision: 106 $'[11:-2]
import Globals, inspect, os, sys, logging, re, string, types
from Acquisition import aq_base, Implicit
from pydoc import ispackage, classname
from Products.Zpydoc.utils import pydoc_encode
LOG = logging.getLogger('ZpyDoc::PythonInfo')

class Warnings:
    """
    throw these in the bin ...
    """

    def __init__(self):
        pass

    def write(self, message):
        pass


try:
    from Products.CMFDefault.utils import bodyfinder, html_headcheck
except ImportError:

    def html_headcheck(text):
        return False


def getmembers(object, predicate=None):
    """
    the method in the inspect module is decidedly dodgy because it relies
    upon the underlying *dir* function which is described with the following
    qualification:

    Note: Because dir() is supplied primarily as a convenience for use at an 
    interactive prompt, it tries to supply an interesting set of names more 
    than it tries to supply a rigorously or consistently defined set of names, 
    and its detailed behavior may change across releases.

    unfortunately, we're still having to use it here instead of providing
    a better implementation.  dir() has a lot of known warts and there have
    been mutterings regarding it on the Python Language list.
    """
    results = []
    for key in dir(object):
        try:
            value = getattr(object, key)
            if not predicate or predicate(value):
                results.append((key, value))
        except:
            pass

    results.sort()
    return results


try:
    import docutils.core, docutils.io

    def structured_text(str):
        """
        hacked from ZReST::render ...
        """
        if str:
            str = str.strip()
        if not str:
            return ''
        else:
            pub = docutils.core.Publisher()
            pub.set_reader('standalone', None, 'restructuredtext')
            pub.set_writer('html')
            pub.get_settings()
            pub.settings._destination = ''
            pub.settings.report_level = 4
            pub.settings.halt_level = 6
            pub.settings.stylesheet = 'stylesheet.css'
            pub.settings.warning_stream = Warnings()
            pub.source = docutils.io.StringInput(source=str, encoding='iso-8859-15')
            pub.destination = docutils.io.StringOutput(encoding='iso-8859-15')
            document = pub.reader.read(pub.source, pub.parser, pub.settings)
            pub.apply_transforms(document)
            try:
                text = pub.writer.write(document, pub.destination)
                if html_headcheck(text):
                    text = bodyfinder(text)
                return text
            except:
                return ''

            return


except:
    from Products.PythonScripts.standard import structured_text

builtin = re.compile('^__(.+)__$')

def classlink(object, modname):
    """Make a link for a class."""
    try:
        name, module = object.__name__, sys.modules.get(object.__module__)
    except AttributeError:
        name = module = None

    if hasattr(module, name) and getattr(module, name) is object:
        return '<a href="%s.html#%s">%s</a>' % (
         pydoc_encode(module.__name__), name, classname(object, modname))
    else:
        return classname(object, modname)


class FunctionInfo(Implicit):
    """
    returns function info from a module (global) or class (member)
    """
    __allow_access_to_unprotected_subobjects__ = 1

    def __init__(self, function):
        self._function = function
        self.id = function.__name__
        self.title = function.__name__

    def arguments(self, formatfn=lambda x: '<span style="color:grey; font-size:10pt">=%s</span>' % repr(x)):
        """
        formatvalue is a function name used to format value's - maybe a python script??
        """
        if inspect.isbuiltin(self._function):
            return '...'
        else:
            (args, varargs, varkw, defaults) = inspect.getargspec(self._function)
            return inspect.formatargspec(args, varargs, varkw, defaults, formatvalue=formatfn)

    def doc(self, structured=False):
        if structured:
            return structured_text(getattr(self._function, '__doc__'))
        d = getattr(self._function, '__doc__', '')
        if d:
            return d.strip()
        return ''

    def __cmp__(self, other):
        x = self.id
        y = other.id
        if x < y:
            return -1
        if x > y:
            return 1
        return 0


class ClassInfo(Implicit):
    """
    Return Class-Specific information
    """
    __allow_access_to_unprotected_subobjects__ = 1

    def __init__(self, cls):
        self._class = cls
        self.id = cls.__name__
        self.title = cls.__name__

    def getclasstree(self):
        return inspect.getclasstree([self._class], 1)

    def bases(self):
        return map(lambda x, self=self: ClassInfo(x).__of__(self), self._class.__bases__)

    def methods(self):
        if not hasattr(self, '_methods'):
            self._methods = map(lambda x, self=self: FunctionInfo(x[1].im_func).__of__(self), getmembers(self._class, inspect.ismethod))
        return self._methods

    def hasmethod(self, method):
        return self.methods().count(method)

    def doc(self, structured=False):
        if structured:
            return structured_text(getattr(self._class, '__doc__'))
        d = getattr(self._class, '__doc__', '')
        if d:
            return d.strip()
        return ''

    def getsourcefile(self):
        return self._class.__name__

    def module(self):
        return self['module']

    def name(self):
        return self['name']

    def __getitem__(self, name):
        return getattr(aq_base(self._class), '__%s__' % name, '')

    def getclass(self):
        return self._class


class ModuleInfo(Implicit):
    """
    an object returned from a PythonInspector that has attributes
    suitably defined for Zope access
    """
    __allow_access_to_unprotected_subobjects__ = 1

    def __init__(self, module, name):
        self.id = module.__name__
        self.title = name or module.__name__
        self._module = module

    def name(self):
        return self.id or self.title

    def shortname(self):
        """
        return the smallest import name for the module
        """
        name = self.name()
        parentname = self.aq_parent.name()
        if name.startswith(parentname):
            return name[len(parentname) + 1:]
        return name

    def functions(self):
        return map(lambda x, self=self: FunctionInfo(x[1]).__of__(self), getmembers(self._module, inspect.isfunction))

    def classes(self):
        results = []
        for (k, v) in getmembers(self._object, inspect.isclass):
            if (inspect.getmodule(v) or self._object) is self._object:
                results.append((k, v))

        return map(lambda x, self=self: ClassInfo(x[1]).__of__(self), results)

    def __getitem__(self, name):
        """
        this is where all the work happens ...

        just try throwing inspect function names, and private object attributes
        at the beast and see what returns ...
        """
        if name in ('getdoc', 'getcomments', 'getfile', 'getmodule', 'getsourcefile',
                    'getsourcelines', 'getsource'):
            return structured_text(apply(getattr(inspect, name), [self._module]))
        item = getattr(aq_base(self._module), '__%s__' % name, '')
        return item

    def __cmp__(self, other):
        x = self.id
        y = other.id
        if x < y:
            return -1
        if x > y:
            return 1
        return 0


class PackageInfo(Implicit):
    """
    An aggregation of all information gatherable via the standard Python
    inspect package.

    This is quite a light-weight implementation, with very little data
    actually stored in the object, and the information only gathered upon
    specfic function invokation.

    Should it prove necessary, there is the possibility of caching within
    this class.

    This class is Zope-derived to enjoy aspects of Acquisition - maybe this
    can be relaxed in the future.
    """
    __allow_access_to_unprotected_subobjects__ = 1

    def __init__(self, object, name, onelevel=True):
        """
        information about a package

        we need to be able to recursively place 'PackageInfo's inside PackageInfo
        and the onelevel flag permits us to stop infinite looping ...
        """
        self.id = object.__name__ or name
        self.title = name
        self._object = object
        self._modpkgs = []
        if onelevel:
            for (name, module) in getmembers(object, inspect.ismodule):
                if hasattr(module, '__path__'):
                    self._modpkgs.append(PackageInfo(module, name, onelevel=False).__of__(self))
                else:
                    self._modpkgs.append(ModuleInfo(module, name).__of__(self))

        self._modpkgs.sort()

    def name(self):
        return self.id

    def shortname(self):
        """
        return the smallest import name for the module
        """
        name = self.name()
        if name.find('.') == -1:
            return name
        return name.split('.')[(-1)]

    def functions(self):
        """
        return a list of function meta data objects
        """
        return map(lambda x, self=self: FunctionInfo(x[1]).__of__(self), getmembers(self._object, inspect.isfunction))

    def data(self):
        """
        this is sort of supposed to be a light-weight final parse ...
        """
        return filter(lambda k: not builtin.search(k[0]) and type(k[1]) in (types.IntType,
         types.LongType, types.FloatType,
         types.ComplexType, types.StringType,
         types.TupleType, types.ListType, types.DictType), self._object.__dict__.items())

    def modules(self):
        return filter(lambda x: isinstance(x, ModuleInfo), self._modpkgs)

    def packages(self):
        return filter(lambda x: isinstance(x, PackageInfo), self._modpkgs)

    def classes(self):
        if inspect.isclass(self._object):
            return [ClassInfo(self._object).__of__(self)]
        results = []
        for (k, v) in getmembers(self._object, inspect.isclass):
            if inspect.getmodule(v) == self._object:
                results.append(v)

        return map(lambda x, self=self: ClassInfo(x).__of__(self), results)

    def classtree(self, links=0):
        """
        Unfortunately, this stuff recurses to build it's structure, and is not really
        a candidate for ZPT's which only iterate (saying that, all recursive functions
        can be written iteratively - but it would be masochistical to use ZPT).

        Our best chance here would be to accept formatter functions as parameters to
        avoid any direct use of HTML here.

        if you want the classtree to appear as links, then set this ...
        """
        return self._formattree(inspect.getclasstree(map(lambda x: x._class, self.classes()), 1), self._object.__name__, None, links)

    def _formattree(self, tree, modname, parent=None, links=0):
        """Produce HTML for a class tree as given by inspect.getclasstree()."""
        result = ''
        for entry in tree:
            if type(entry) is type(()):
                (c, bases) = entry
                result = result + '<dt><font face="helvetica, arial"><small>'
                if links:
                    result = result + classlink(c, modname)
                else:
                    result = result + classname(c, modname)
                if bases and bases != (parent,):
                    parents = []
                    for base in bases:
                        if links:
                            parents.append(classlink(base, modname))
                        else:
                            parents.append(classname(base, modname))

                    result = result + '(' + string.join(parents, ', ') + ')'
                result = result + '\n</small></font></dt>'
            elif type(entry) is type([]):
                result = result + '<dd>\n%s</dd>\n' % self._formattree(entry, modname, c, links)

        return '<dl>\n%s</dl>\n' % result

    def doc(self, structured=False):
        """
        hmmm - sometimes when stepping thru objects, we are only viewing a subset
        of the translation unit and need to prime this only for modules/packages ...
        """
        if inspect.ismodule(self._object):
            if structured:
                return structured_text(getattr(self._object, '__doc__'))
            d = getattr(self._object, '__doc__', '')
            if d:
                return d.strip()
        return ''

    def version(self):
        """
        return version string
        """
        return self['version']

    def getsourcefile(self):
        """
        just returns the name of the source file
        """
        return self['getsourcefile']

    def __getitem__(self, name):
        """
        this is where all the work happens ...

        just try throwing inspect function names, and private object attributes
        at the beast and see what returns ...
        """
        if name in ('getdoc', 'getcomments', 'getfile', 'getmodule', 'getsourcefile',
                    'getsourcelines', 'getsource'):
            try:
                return apply(getattr(inspect, name), [self._object])
            except:
                return

        return getattr(self._object, '__%s__' % name, '')

    def __cmp__(self, other):
        x = self.id
        y = other.id
        if x < y:
            return -1
        if x > y:
            return 1
        return 0