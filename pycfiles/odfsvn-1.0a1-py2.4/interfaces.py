# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/odfsvn/interfaces.py
# Compiled at: 2008-01-17 07:36:18
try:
    from zope.interface import Interface
except ImportError:

    class Interface:
        __module__ = __name__


class IODFPackage(Interface):
    """A ODF package abstraction.

    This provides a dict-like interface for a ODF package. This makes it
    possible to list, access and update all files in a ODF package without
    having to know if it is zipped, unpacked or in a repository.

    In order to optimise performance where possible generators are used
    instead of lists.
    """
    __module__ = __name__

    def close():
        """Commit all changes and close the package.

        It is an error to access the package after calling this method.
        """
        pass

    def values():
        """Return the contents of all files in the package."""
        pass

    def items():
        """Return an iterable over (path, contents) tuples."""
        pass

    def __len__():
        """Return the number of files in the package."""
        pass

    def __nonzero__():
        """Test if the package is empty."""
        pass

    def getRepositoryInfo():
        """Extract the repository metadata from a package.

        The information is returned as a dictionary.
        """
        pass

    def setRepositoryInfo(info):
        """Update the repository information in a package."""
        pass


class IRepository(Interface):
    __module__ = __name__

    def __init__(uri):
        """Initialize a repository located at URI."""
        pass

    def UUID():
        """Return the UUID for the repository."""
        pass

    def retrieve(path, odf):
        """Retrieve an ODF package from the path inside the repository
        and store it in an existing ODF package."""
        pass

    def store(path, odf, odf_update=True, message=None):
        """Store an ODF package in the repository.

        If odf_update is true the repository information in the ODF
        packge will be updated.
        """
        pass