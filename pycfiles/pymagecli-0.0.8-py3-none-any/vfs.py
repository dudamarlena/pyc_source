# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/pymage/vfs.py
# Compiled at: 2007-09-07 22:12:50
__doc__ = '\nVirtual file system abstraction\n\nThe goal of this module is to allow game data that is contained in a Python egg,\nzip file, or any other medium be capable of loading.  This leads to more\ndistribution options for your game.\n'
import os, re
try:
    import pkg_resources
except ImportError:
    pass

import zope.interface
__author__ = 'Ross Light'
__date__ = 'August 30, 2007'
__docformat__ = 'reStructuredText'
__all__ = ['IFilesystem',
 'Path',
 'PhysicalFilesystem',
 'PackageResources']

class IFilesystem(zope.interface.Interface):
    """Interface for an abstracted filesystem."""

    def resolve(path):
        """
        Resolves the abstract path to a physical one.
        
        This method *should* be implemented, but may be ignored if impossible.
        
        :Parameters:
            path : `Path` or string
                The abstract path to resolve
        :Raises TypeError: If resolving is impossible
        :Returns: The physical file path
        :ReturnType: str
        """
        pass

    def open(path, mode='r', buffering=None):
        """
        Opens a file object to the abstract path.
        
        This method *must* work under valid input.
        
        :Parameters:
            path : `Path` or string
                The abstract path to open
            mode : str
                The mode flag (same as built-in ``open`` call)
            buffering : int
                The buffering mode (same as built-in ``open`` call)
        :Returns: A file or file-like object representing that file
        :ReturnType: file
        """
        pass

    def listdir(path):
        """
        Lists the children of a directory.
        
        :Parameters:
            path : `Path` or string
                The abstract path to the directory to list
        :Returns: A list of subpaths
        :ReturnType: list of `Path` objects
        """
        pass

    def exists(path):
        """
        Determines whether the path exists.
        
        :Parameters:
            path : `Path` or string
                The abstract path to check
        :ReturnType: bool
        """
        pass

    def isdir(path):
        """
        Determines whether the path is a directory.
        
        :Parameters:
            path : `Path` or string
                The abstract path to check
        :ReturnType: bool
        """
        pass

    def isfile(path):
        """
        Determines whether the path is a file.
        
        :Parameters:
            path : `Path` or string
                The abstract path to check
        :ReturnType: bool
        """
        pass


class Path(object):
    """
    A POSIX path conforming object.
    
    This is used to standardize paths across systems by using the POSIX path
    conventions.  Paths are split up into components, and are automatically
    normalized.
    
    :CVariables:
        sep : str
            Separator for string-based paths
        curdir : str
            Current directory indicator for string-based paths
        pardir : str
            Parent directory indicator for string-based paths
    :IVariables:
        components : tuple
            The components of the path
        absolute : bool
            Whether the path is absolute
        directory : bool
            Whether the path refers to a directory
    """
    sep = '/'
    curdir = '.'
    pardir = '..'

    def __init__(self, path=[], absolute=False, directory=False):
        """
        Create a path.
        
        :Parameters:
            path
                The method of creation is dependent on what type of object this
                is.  If it is a:
                * `Path` object, then a copy is created.
                * string, then the path is parsed from the string.
                * sequence, then the path's components are constructed from the
                  members of the sequence and the keywords specify what kind of
                  path it is.
        :Keywords:
            absolute : bool
                Whether the path is absolute (i.e. has a leading slash)
            directory : bool
                Whether the path is a directory (i.e. has a trailing slash)
        """
        if isinstance(path, Path):
            components = path.components
            self.absolute = path.absolute
            self.directory = path.directory
        elif isinstance(path, basestring):
            if path.startswith(self.sep):
                self.absolute = True
                path = path[len(self.sep):]
            else:
                self.absolute = False
            if path.endswith(self.sep):
                self.directory = True
                path = path[:-len(self.sep)]
            else:
                self.directory = False
            components = path.split(self.sep)
        else:
            components = path
            self.absolute = bool(absolute)
            self.directory = bool(directory)
        self.components = tuple(self._normpath(components, self.absolute))

    @classmethod
    def _normpath(cls, components, absolute):
        """
        Normalize the path.
        
        This involves removing empty components and resolving immediately
        solvable parent references (e.g. "foo/../bar" turns into "bar", but
        "../foo/bar" remains the same).
        """
        result = []
        for component in components:
            if cls.sep in component:
                raise ValueError('Separators are not allowed inside components')
            elif component and component != cls.curdir:
                result.append(component)

        startIndex = 0
        while True:
            try:
                parentIndex = result.index(cls.pardir, startIndex)
            except ValueError:
                break
            else:
                previousIndex = parentIndex - 1
                if previousIndex < startIndex:
                    startIndex += 1
                else:
                    del result[parentIndex]
                    del result[previousIndex]

        if absolute:
            while result and result[0] == cls.pardir:
                del result[0]

        return result

    def relativePath(self, other):
        """
        Evaluate a path as relative to the caller.
        
        >>> path1 = Path('/home/python/')
        >>> path2 = Path('spam/eggs')
        >>> path1.relativePath(path2)
        Path(['home', 'python', 'spam', 'eggs'], absolute=True)
        >>> path2.relativePath('hello')
        Path(['spam', 'hello'])
        
        :Parameters:
            other : `Path`
                The path to resolve, relative to self
        :Returns: The resolved path
        :ReturnType: `Path`
        """
        otherPath = Path(other)
        if otherPath.absolute:
            return otherPath
        elif self.directory:
            return self + otherPath
        else:
            return self[:-1] + otherPath

    def convert(self, **kw):
        """
        Convert path to a different type.
        
        This doesn't affect the components, only the type of path.
        
        :Keywords:
            absolute : bool
                Whether the new path should be absolute
            directory : bool
                Whether the new path should be a directory
        :Returns: The converted path
        :ReturnType: `Path`
        """
        parameters = {'absolute': self.absolute, 'directory': self.directory}
        parameters.update(kw)
        return Path(self.components, **parameters)

    def sanitize(self, chars):
        """
        Sanitize the path by removing characters.
        
        :Parameters:
            chars : str
                The set of characters to remove
        :Returns: The sanitized path
        :ReturnType: `Path`
        """
        pattern = ('|').join((re.escape(char) for char in chars))
        pattern = re.compile(pattern)
        newComponents = []
        for component in self.components:
            newComponents.append(pattern.sub('', component))

        return Path(newComponents, absolute=self.absolute, directory=self.directory)

    def __repr__(self):
        result = 'Path(%r' % list(self.components)
        if self.absolute:
            result += ', absolute=%r' % self.absolute
        if self.directory:
            result += ', directory=%r' % self.directory
        result += ')'
        return result

    def __str__(self):
        result = self.sep.join(self.components)
        if self.absolute:
            result = self.sep + result
        if self.directory:
            result += self.sep
        return result

    def __add__(self, other):
        if isinstance(other, Path):
            return Path(self.components + other.components, absolute=self.absolute, directory=other.directory)
        elif isinstance(other, basestring):
            return self + Path(other)
        elif isinstance(other, (tuple, list)):
            return Path(self.components + tuple(other), absolute=self.absolute)
        else:
            return NotImplemented

    def __radd__(self, other):
        if isinstance(other, basestring):
            return Path(other) + self
        elif isinstance(other, (tuple, list)):
            return Path(tuple(other) + self.components, directory=self.directory)
        else:
            return NotImplemented

    def __len__(self):
        return len(self.components)

    def __contains__(self, item):
        return item in self.components

    def __iter__(self):
        return iter(self.components)

    def __getitem__(self, item):
        if isinstance(item, slice):
            pathLength = len(self.components)
            sliceRange = xrange(*item.indices(pathLength))
            absolute = bool(self.absolute and sliceRange[0] == 0)
            directory = bool(self.directory and sliceRange[(-1)] == pathLength - 1)
            return Path(self.components[item], absolute=absolute, directory=directory)
        elif isinstance(item, (int, long)) or hasattr(item, '__index__'):
            return self.components[item]
        else:
            typeName = type(item).__name__
            raise TypeError('Index or slice expected (got %s)' % typeName)

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other):
        if isinstance(other, Path):
            return self.components == other.components and self.absolute == other.absolute and self.directory == other.directory
        elif isinstance(other, basestring):
            return str(self) == other
        elif isinstance(other, (list, tuple)):
            return self.components == tuple(other)
        else:
            return NotImplemented

    def __ne__(self, other):
        if isinstance(other, Path):
            return self.components != other.components or self.absolute != other.absolute or self.directory != other.directory
        elif isinstance(other, basestring):
            return str(self) != other
        elif isinstance(other, (list, tuple)):
            return self.components != tuple(other)
        else:
            return NotImplemented

    def __gt__(self, other):
        if isinstance(other, Path):
            if self.absolute and not other.absolute:
                return True
            result = cmp(self.components, other.components)
            if result == 1:
                return True
            elif result == 0:
                return bool(self.directory and not other.directory)
            else:
                return False
        elif isinstance(other, basestring):
            return bool(str(self) > other)
        elif isinstance(other, (list, tuple)):
            return self.components > tuple(other)
        else:
            return NotImplemented

    def __lt__(self, other):
        if isinstance(other, Path):
            if not self.absolute and other.absolute:
                return True
            result = cmp(self.components, other.components)
            if result == -1:
                return True
            elif result == 0:
                return bool(not self.directory and other.directory)
            else:
                return False
        elif isinstance(other, basestring):
            return bool(str(self) < other)
        elif isinstance(other, (list, tuple)):
            return self.components < tuple(other)
        else:
            return NotImplemented


class PhysicalFilesystem(object):
    """
    Uses the underlying filesystem of the running machine.
    
    The filesystem is determined by a root directory, and anything higher than
    that directory is disallowed.
    
    .. Warning:: Do not depend on this inability to go above the root; doing
                 so would be a security flaw, as this currently does not check
                 for symbolic links.
    
    :IVariables:
        root : str
            Root of the filesystem
    """
    zope.interface.implements(IFilesystem)

    def __init__(self, root):
        self.root = root

    @staticmethod
    def _abspath(path):
        if not isinstance(path, Path):
            path = Path(path)
        return path.convert(absolute=True).sanitize(os.path.sep)

    def resolve(self, path):
        return os.path.join(self.root, *self._abspath(path).components)

    def open(self, path, mode='r', buffering=None):
        if buffering is None:
            return open(self.resolve(path), mode)
        else:
            return open(self.resolve(path), mode, buffering)
        return

    def listdir(self, path):
        path = self._abspath(path).convert(directory=True)
        result = []
        for name in os.listdir(self.resolve(path)):
            subpath = path.relativePath(name)
            if self.isdir(subpath):
                subpath = subpath.convert(directory=True)
            result.append(subpath)

        result.sort()
        return result

    def exists(self, path):
        return os.path.exists(self.resolve(path))

    def isdir(self, path):
        return os.path.isdir(self.resolve(path))

    def isfile(self, path):
        return os.path.isfile(self.resolve(path))


class PackageResources(object):
    """
    Uses the pkg_resources_ module to obtain files.
    
    :IVariables:
        package : str
            Name of the package
    
    .. _pkg_resources: http://peak.telecommunity.com/DevCenter/PkgResources
    """
    zope.interface.implements(IFilesystem)

    def __init__(self, package):
        self.package = package

    @staticmethod
    def _abspath(path):
        if not isinstance(path, Path):
            path = Path(path)
        return path.convert(absolute=True)

    @classmethod
    def _strpath(cls, path):
        return str(cls._abspath(path))

    def resolve(self, path):
        return pkg_resources.resource_filename(self.package, self._strpath(path))

    def open(self, path, mode='r', buffering=None):
        if mode not in ('r', 'rb'):
            raise ValueError('File must be opened in read, not %r' % mode)
        return pkg_resources.resource_stream(self.package, self._strpath(path))

    def listdir(self, path):
        path = self._abspath(path).convert(directory=True)
        result = []
        for name in pkg_resources.resource_listdir(self.package, str(path)):
            subpath = path.relativePath(name)
            if self.isdir(subpath):
                subpath = subpath.convert(directory=True)
            result.append(subpath)

        result.sort()
        return result

    def exists(self, path):
        return pkg_resources.resource_exists(self.package, self._strpath(path))

    def isdir(self, path):
        return pkg_resources.resource_isdir(self.package, self._strpath(path))

    def isfile(self, path):
        path = self._strpath(path)
        return pkg_resources.resource_exists(self.package, path) and not pkg_resources.resource_isdir(self.package, path)