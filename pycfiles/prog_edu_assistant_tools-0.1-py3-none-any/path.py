# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/progtools/path.py
# Compiled at: 2009-10-15 11:10:23
__doc__ = '\nPath/file functions\n\n:Variables:\n    STREAM_CODE : str\n        The special file name that designates standard input or output\n'
import os, re, sys
__author__ = 'Ross Light'
__date__ = 'December 7, 2008'
__docformat__ = 'reStructuredText'
__license__ = 'MIT'
__all__ = ['STREAM_CODE',
 'expandpath',
 'open_input_file',
 'open_output_file',
 'Path']
STREAM_CODE = '-'

def expandpath(path):
    """
    Expands a path so that it is usable by the program.
    
    At this time, it just expands the user and normalizes.
    
    :Parameters:
        path : str
            The path to expand
    :Returns: Expanded path
    :ReturnType: str
    """
    return os.path.normpath(os.path.expanduser(path))


def open_input_file(filename=STREAM_CODE, mode='r'):
    """
    Opens a file for input.
    
    :Parameters:
        filename : str
            File name to open.  If '-' is specified, stdin is returned.
        mode : str
            Mode to open the file as.  Default is 'r'.
    :Returns: The opened file
    :ReturnType: file
    """
    if filename == STREAM_CODE:
        return sys.stdin
    else:
        return open(expandpath(filename), mode)


def open_output_file(filename=STREAM_CODE, mode='w'):
    """
    Opens a file for output.
    
    :Parameters:
        filename : str
            File name to open.  If '-' is specified, stdout is returned.
        mode : str
            Mode to open the file as.  Default is 'w'.
    :Returns: The opened file
    :ReturnType: file
    """
    if filename == STREAM_CODE:
        return sys.stdout
    else:
        return open(expandpath(filename), mode)


class Path(object):
    """
    A POSIX path.
    
    Paths are split up into components and are automatically normalized.
    
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
    __slots__ = [
     'components', 'absolute', 'directory']
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
        self.components = tuple(components)
        self._normpath()

    def _normpath(self):
        """
        Normalize the path.
        
        This involves removing empty components and resolving immediately
        solvable parent references (e.g. "foo/../bar" turns into "bar", but
        "../foo/bar" remains the same).
        """
        result = []
        for component in self.components:
            if self.sep in component:
                raise ValueError('Separators are not allowed inside components')
            elif component and component != self.curdir:
                result.append(component)

        start_index = 0
        while True:
            try:
                parent_index = result.index(self.pardir, start_index)
            except ValueError:
                break
            else:
                previous_index = parent_index - 1
                if previous_index < start_index:
                    start_index += 1
                else:
                    del result[parent_index]
                    del result[previous_index]

        if self.absolute:
            while result and result[0] == self.pardir:
                del result[0]

            if self.directory and not result:
                self.directory = False
        self.components = tuple(result)

    def relative_path(self, other):
        """
        Evaluate a path as relative to the caller.
        
        >>> path1 = Path('/home/python/')
        >>> path2 = Path('spam/eggs')
        >>> path1.relative_path(path2)
        Path(['home', 'python', 'spam', 'eggs'], absolute=True)
        >>> path2.relative_path('hello')
        Path(['spam', 'hello'])
        
        :Parameters:
            other : `Path`
                The path to resolve, relative to self
        :Returns: The resolved path
        :ReturnType: `Path`
        """
        other_path = Path(other)
        if other_path.absolute:
            return other_path
        elif self.directory:
            return self + other_path
        else:
            return self[:-1] + other_path

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
        new_components = []
        for component in self.components:
            new_components.append(pattern.sub('', component))

        return Path(new_components, absolute=self.absolute, directory=self.directory)

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
            path_length = len(self.components)
            slice_range = xrange(*item.indices(path_length))
            absolute = bool(self.absolute and (len(slice_range) == 0 or slice_range[0] == 0))
            directory = bool(self.directory and len(slice_range) > 0 and slice_range[(-1)] == path_length - 1)
            return Path(self.components[item], absolute=absolute, directory=directory)
        elif isinstance(item, (int, long)) or hasattr(item, '__index__'):
            return self.components[item]
        else:
            type_name = type(item).__name__
            raise TypeError('Index or slice expected (got %s)' % type_name)

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