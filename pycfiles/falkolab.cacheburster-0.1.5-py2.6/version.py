# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/falkolab/cacheburster/version.py
# Compiled at: 2010-11-18 05:51:30
from zope.interface import implements
import zope.component
from zope.browserresource.interfaces import IResource
from falkolab.cacheburster.interfaces import IVersionManager
import falkolab.cacheburster.interfaces
from zope.app.appsetup import appsetup
from zope.browserresource.file import File
import binascii, os.path
try:
    from hashlib import md5
except ImportError:
    from md5 import new as md5

_resource_hash = {}

class VersionManager(object):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __str__(self):
        cc = appsetup.getConfigContext()
        devmode = False
        if cc != None:
            devmode = cc.hasFeature('devmode')
        name = self.context.__name__
        if not devmode:
            version = _resource_hash.get(name)
            if version:
                return version
        version = self.getVersion()
        if not version:
            raise Exception("Can't take resource version `%s`" % name)
        if not devmode:
            _resource_hash[name] = version
        return version

    def __call__(self):
        return self.__str__()

    def getData(self):
        chooseContext = getattr(self.context, 'chooseContext', None)
        resourceContext = chooseContext and chooseContext() or self.context.context
        if isinstance(resourceContext, File):
            path = resourceContext.path
            f = open(path, 'rb')
            data = f.read()
            f.close()
        else:
            data = self.context.browserDefault(self.request)[0]()
        return data

    def getVersion(self):
        raise NotImplemented()


class MD5VersionManager(VersionManager):
    implements(IVersionManager)
    zope.component.adapts(IResource, falkolab.cacheburster.interfaces.IVersionedResourceLayer)

    def getVersion(self):
        data = self.getData()
        if not data:
            raise Exception("Can't take version from empty resource `%s`" % self.context.__name__)
        m = md5()
        m.update(data)
        return m.hexdigest()


class CRC32VersionManager(VersionManager):
    implements(IVersionManager)
    zope.component.adapts(IResource, falkolab.cacheburster.interfaces.IVersionedResourceLayer)

    def getVersion(self):
        data = self.getData()
        if not data:
            raise Exception("Can't take version from empty resource `%s`" % self.context.__name__)
        crc = binascii.crc32(data) & 4294967295
        return '%08x' % crc


def _getPath(filename):
    filename = os.path.normpath(filename)
    if os.path.isabs(filename):
        return filename
    basepath = os.path.dirname(__file__)
    basepath = os.path.abspath(basepath)
    return os.path.join(basepath, filename)


def FileVersionManager(file):
    """Create a VersionManager that can simply read version from file."""
    path = _getPath(file)

    def _getVersion(self):
        f = open(self._path, 'r')
        data = f.read()
        f.close()
        return data.strip(' \n\r')

    klass = type('FileVersionManager', (
     VersionManager,), {'getVersion': _getVersion, '_path': path})
    return klass