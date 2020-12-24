# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/Products/Zpydoc/inspectors/ZopeInfo.py
# Compiled at: 2011-09-28 02:31:46
import Globals, logging, Products, inspect, os, sys, traceback
from Acquisition import Implicit
from pydoc import ispackage
from PythonInfo import structured_text, getmembers, FunctionInfo as FuncInfoBase, ModuleInfo as ModInfoBase, ClassInfo as ClassInfoBase, PackageInfo as PkgInfoBase
from Products.Zpydoc.utils import implementsMethod
from Acquisition import aq_base
import OFS.misc_
from Products.CMFCore.utils import getToolByName
LOG = logging.getLogger('ZpyDoc::ZopeInfo')
inspect.ismethod = implementsMethod

class FunctionInfo(FuncInfoBase):
    """
    We want to get Zope Permission info into the function info
    """

    def __init__(self, function, permission):
        FuncInfoBase.__init__(self, function)
        self._permission = permission

    def arguments(self, formatfn=lambda x: '<span style="color:grey; font-size:10pt">=%s</span>' % repr(x)):
        """
        return an html-formatted list of the function arguments
        """
        try:
            return FuncInfoBase.arguments(self, formatfn)
        except:
            return '(...)'

    def permission(self):
        """
        return access permission needed to invoke this function
        """
        return self._permission


class ClassInfo(ClassInfoBase):
    """
    We want to place additional functions to access 'Public' and 'Private'
    methods etc
    """

    def __init__(self, cls):
        ClassInfoBase.__init__(self, cls)
        if hasattr(cls, 'meta_type'):
            self.productinfo = ProductInfo(cls.meta_type)
        else:
            self.productinfo = None
        pm_syms = {}
        if hasattr(self._class, '__ac_permissions__'):
            for perms in getattr(self._class, '__ac_permissions__'):
                for fn in perms[1]:
                    pm_syms[fn] = perms[0]

        self._methods = []
        try:
            methods = getmembers(self._class, inspect.ismethod)
        except Exception, e:
            methods = []

        for (name, method) in methods:
            self._methods.append(FunctionInfo(method.im_func, pm_syms.get(name, '')))

        if hasattr(self._class, '_Interface__attrs'):
            self._methods.extend(map(lambda x, y=pm_syms, self=self: FunctionInfo(x[1], y.get(x[0], '')), self._class._Interface__attrs.items()))
        return

    def methods(self):
        return map(lambda x: x.__of__(self), self._methods)

    def public_methods(self):
        """
        methods not beginning with an underscore, and having a docstring and a permission
        assignment (otherwise requiring Manager role to access - which effectively makes
        it private)
        """
        return filter(lambda x: x.id[0] != '_' and hasattr(x, '__doc__') and x.permission, self.methods())

    def private_methods(self):
        """
        methods beginning with an underscore, or without a docstring (or requiring Manager role)
        """
        return filter(lambda x: x.id[0] == '_' or not hasattr(x, '__doc__') or not x.permission, self.methods())


class ModuleInfo(ModInfoBase):
    """
    """

    def classes(self):
        results = []
        for (k, v) in getmembers(self._object, inspect.isclass):
            if (inspect.getmodule(v) or self._object) is self._object:
                results.append((k, v))

        return map(lambda x, self=self: ClassInfo(x[1]).__of__(self), results)


class PackageInfo(PkgInfoBase):
    """
    """

    def __init__(self, object, name, onelevel=True):
        """
        This is the same as it's parent, but the scope of the Info's is different ...
        """
        self.id = object.__name__
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

    def getIcon(self):
        """
        dynamically figure out if we're a package or module and produce the
        correct icon path
        """
        portal_url = getToolByName(self, 'portal_url').getPortalObject().absolute_url()
        if self.packages():
            return '%s/package.png' % portal_url
        else:
            return '%s/file.png' % portal_url

    def classes(self):
        """
        return a list of class meta data objects in this module/package
        """
        if inspect.isclass(self._object):
            return [ClassInfo(self._object).__of__(self)]
        results = []
        for (k, v) in getmembers(self._object, inspect.isclass):
            if inspect.getmodule(v) == self._object:
                results.append(v)

        return map(lambda x, self=self: ClassInfo(x).__of__(self), results)

    def __getitem__(self, name):
        """
        check for python builtin's before 'normal' zope objects ...
        """
        return PkgInfoBase.__getitem__(self, name) or getattr(aq_base(self._object), name, '')


class ProductInfo(Implicit):
    """
    product={'visibility': 'Global',
             'interfaces': [<Interface webdav.EtagSupport.EtagBaseInterface at 83fa108>],
             'container_filter': None,
             'action': 'manage_addProduct/Zpydoc/manage_addZpydoc',
             'permission': 'Manage Zpydocs',
             'name': 'Zpydoc',
             'product': 'Zpydoc',
             'instance': <extension class Products.Zpydoc.Zpydoc.Zpydoc at 922f208>}

    instance={'icon': 'misc_/Zpydoc/renderer.gif',
            'id': 'PyDoc', '_renderer': <PyHTMLDoc at 0x965a288>,
            '__call__': <function __call__ at 0x965a0e4>,
            '__implements__': (<Interface Products.Zpydoc.ZpydocRenderer.IZpydocRenderer at 92576c0>,),
            'meta_type': 'pydocRenderer',
            'directory': <function directory at 0x9659c14>,
            '__getattr__': <function __getattr__ at 0x9659c4c>,
            'title': 'Vanilla pydoc',
            'builtins': <function builtins at 0x965a164>,
            '__doc__': '
    Render a standard pydoc page by delegating to pydoc

    We have to be very careful about not explicitly defining methods here because
    then they do not become overrideable via ObjectManager objects in derivations.
    This is why we have used containment of the pydoc object.
    ',
            '__module__': 'Products.Zpydoc.renderers.PyDoc'}

    """
    __allow_access_to_unprotected_subobjects__ = 1

    def __init__(self, meta_type):
        self.id = meta_type
        self._product = None
        for p in Products.meta_types:
            product = p.get('instance', None)
            if product and hasattr(product, 'meta_type') and product.meta_type == meta_type:
                self._product = p
                break

        if self._product and self._product.has_key('interfaces'):
            interfaces = []
            for interface in self._product['interfaces']:
                interfaces.append(InterfaceInfo(interface))

            self._interfaces = interfaces
        else:
            self._interfaces = []
        return

    def iconpath(self):
        try:
            return self._product['instance'].icon
        except:
            return

        return

    def icon(self):
        try:
            name = os.path.split(self.iconpath())[1]
            return getattr(OFS.misc_.misc_, self._product['product'])[name]
        except:
            return

        return

    def interfaces(self):
        """
        return list of interface classes
        """
        return map(lambda x, y=self: x.__of__(y), self._interfaces)

    def doc(self, structured=False):
        """
        return the document string
        """
        msg = getattr(self._product, '__doc__').strip()
        if msg:
            if structured:
                return structured_text(msg)
            return msg
        return ''

    def __getitem__(self, name):
        item = self._product.get(name, None)
        return item


class InterfaceInfo(ClassInfo):
    """
    a Zope Interface object
    '_Interface__attrs': {'http__etag': <Method instance at 8379c78>, 'http__refreshEtag': <Method instance at 8450790>},
    '__doc__': '    Basic Etag support interface, meaning the object supports generating

                    an Etag that can be used by certain HTTP and WebDAV Requests.
    ',
    '__bases__': (<Interface Interface._Interface.Interface at 82d5b70>,),
    '__module__': 'webdav.EtagSupport',
    '__name__': 'EtagBaseInterface'
    """

    def name(self):
        return self['name']

    def module(self):
        return self['module']

    def methods(self):
        return map(lambda x, self=self: FunctionInfo(x[1], '').__of__(self), self._class._Interface__attrs.items())