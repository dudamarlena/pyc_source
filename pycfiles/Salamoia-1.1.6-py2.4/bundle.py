# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/salamoia/h2o/bundle.py
# Compiled at: 2007-12-02 16:26:58
"""
Implementation of salamoia bundles
"""
__all__ = [
 'Bundle', 'Description', 'BundleDescription']
from pkg_resources import resource_filename
from salamoia.h2o.xmlparser import RootElement
from salamoia.utility.pathelp import path as Path
from cStringIO import StringIO

class Bundle(object):
    """
    A bundle is a group of python packages organized as the fundamental extension of salamoia

    TODO: offer a possibility to construct the egg for the module of the caller
    """
    __module__ = __name__

    def __init__(self, egg):
        """
        """
        from bundledescription import BundleDescription
        self.egg = egg
        self.description = BundleDescription(self.bundleMetadataWrapper())

    def filename(self, path):
        """
        Given a file path relative to this bundle this method will return an
        absolute path of the (eventually) unzipped resource.
        """
        return self.egg.get_resource_filename(resource_filename.im_self, path)

    def resourceWrapper(self, path):
        """
        Return a ResourceWrapper wrapper for the named resource file
        """
        return ResourceWrapper(path, self)

    def metadataWrapper(self, name):
        """
        Return a wrapper for the named metadata
        """
        return MetadataWrapper(name, self)

    def bundleMetadataWrapper(self):
        """
        return a wrapper for salamoia_bundle.xml
        """
        return self.metadataWrapper('salamoia_bundle.xml')

    def activate(self):
        self.egg.activate()
        self.description.activate()

    def __repr__(self):
        return '<Bundle %s: %s>' % (self.egg.key, self.egg.location)


class AbstractWrapper(object):
    __module__ = __name__

    def __init__(self, bundle):
        self.bundle = bundle


class StringWrapper(object):
    """
    The string wrapper is useful when you have to simulate a ResourceWrapper or MetadataWrapper
    in your doctests:

    >>> StringWrapper('hello').open().read()
    'hello'
    """
    __module__ = __name__

    def __init__(self, string):
        self.string = string

    def open(self):
        return StringIO(self.string)


class FileWrapper(object):
    """
    This object implement the resource wrapper interface and allows to use normal filesystem files
    like wrapped resources.
    """
    __module__ = __name__

    def __init__(self, path):
        self.path = path

    def open(self):
        return open(self.path)


class MetadataWrapper(AbstractWrapper):
    """
    Like ResourceWrapper but for egg metadata.

    Egg metadata are treated with a slightly different api at setuptools level.
    """
    __module__ = __name__

    def __init__(self, name, bundle=None):
        super(MetadataWrapper, self).__init__(bundle)
        self.name = name

    def open(self):
        return StringIO(self.bundle.egg.get_metadata(self.name))


class ResourceWrapper(AbstractWrapper):
    """
    A resource wrapper helps using resources (files) inside bundles.
    When bundles are packaged as egg (zip) files, it transparently decompress them.

    Wrappers keep a reference to the path and to the associated bundle, so that relative paths
    can be easly computed.

    The convenience `open` method is provided to abstract the need to access a filesystem path.
    In future a more direct way to get a stream to an archived file decompressed on fly (zlib for example)
    without the need of temporary storage. Using `open` will handle that transparently.

    You can use a ResourceWrapper without a bundle, in this case it simply passes the file through:
    >>> ResourceWrapper('test.txt').filename()
    'test.txt'

    """
    __module__ = __name__

    def __init__(self, path, bundle=None):
        super(ResourceWrapper, self).__init__(bundle)
        self.path = Path(path)

    def filename(self):
        """
        If a bundle is specified in the resource wrapper then the filename is resolved
        relative to it, otherwise the plain path is returned.

        Useful in order to use ResourceWrapper as a replacement of a filename
        """
        if self.bundle:
            return self.bundle.filename(self.path)
        return self.path

    def open(self):
        """
        Simply opens the file named `self.filename()`
        """
        return open(self.filename())


class Description(RootElement):
    """
    This is the abstract class for top level xml description files (like schema, service etc)
    """
    __module__ = __name__

    def activate(self):
        """
        This method will be called when the bundle is activated.
        Usually here the feature will be registered in the system
        """
        pass


from salamoia.tests import *
runDocTests()