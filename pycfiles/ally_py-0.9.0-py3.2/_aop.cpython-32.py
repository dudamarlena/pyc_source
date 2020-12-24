# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ally/container/_impl/_aop.py
# Compiled at: 2013-10-02 09:54:40
"""
Created on Jan 12, 2012

@package: ally base
@copyright: 2011 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Provides the AOP implementations.
"""
from ._assembly import Assembly
from inspect import isclass
import re, sys, logging
log = logging.getLogger(__name__)

class Matcher:
    """
    Provides the matching for paths based on patterns.
    * - place holder for a module/package name
    ** - place holder for a modules/packages names
    Path patterns examples:
        api.* - will match all paths from the 'api' path.
        *.api - will match the path that is found in the paths like 'ally.api', 'superdesk.api' but not
                'ally.superdesk.api'.
        *.api.* - will match all the paths that are found in the 'api' path.
        **.api.* - match all the paths for all paths that are found with the name 'api' regardless of the
                root path location.
        **.api.** - just like the previous example but matches all the paths and sub paths.
    """

    def __init__(self, patterns):
        """
        Constructs the filter based on the provided patterns.
        
        @param patterns: list[string]
            A list of string patterns.
        """
        self._Matcher__regex = []
        for pattern in patterns:
            assert isinstance(pattern, str), 'Invalid pattern %s' % pattern
            pattern = pattern.strip()
            elements = []
            for element in pattern.split('**'):
                elements.append('[a-zA-Z0-9_]*'.join([re.escape(e) for e in element.split('*')]))

            self._Matcher__regex.append(re.compile('[a-zA-Z0-9_\\.]*'.join(elements) + '$'))

    def match(self, path):
        """
        Matches the provided path.
        
        @param path: string
            The path to be matched.
        @return: boolean
            True if the path is a match for the matcher, False otherwise.
        """
        assert isinstance(path, str), 'Invalid path %s' % path
        for reg in self._Matcher__regex:
            if reg.match(path):
                return True

        return False


class AOP:
    """
    Provides the basic AOP container.
    """

    def __init__(self, paths):
        """
        Initialize the AOP paths container.
        
        @param paths: dictionary{string, object}
            The path mapping of this aop.
        """
        assert isinstance(paths, dict), 'Invalid paths %s' % paths
        for path in paths.keys():
            if not isinstance(path, str):
                raise AssertionError('Invalid path %s' % path)

        self._paths = paths

    def filter(self, *patterns):
        """
        Keep in the container only the paths that respect the patterns.
        
        @param patterns: arguments[string]
            The patterns to filter by.
        @return: self
            The same instance for chaining.
        """
        matcher = Matcher(patterns)
        self._paths = {path:value for path, value in  if matcher.match(path)}
        return self

    def exclude(self, *patterns):
        """
        Remove from the container the paths that respect the patterns.
        
        @param patterns: arguments[string]
            The patterns to remove by.
        @return: self
            The same instance for chaining.
        """
        matcher = Matcher(patterns)
        self._paths = {path:value for path, value in  if not matcher.match(path)}
        return self

    def asList(self):
        """
        Provides the path values as a list.
        
        @return: list[object]
            The list of path objects.
        """
        return list(self._paths.values())


class AOPModules(AOP):
    """
    Container for module paths.
    """

    def __init__(self, paths):
        """
        Initialize the module paths container.
        
        @param paths: dictionary{string, string}
            The path mapping of this aop.
        """
        assert isinstance(paths, dict), 'Invalid paths %s' % paths
        for path, value in paths.items():
            assert isinstance(path, str), 'Invalid path %s' % path
            if not value == path:
                raise AssertionError("Invalid value %s should be the same as path '%s'" % (value, path))

        super().__init__(paths)

    def load(self):
        """
        Loads all the modules from this AOP.
        
        @return: self
            The same instance for chaining.
        """
        broken = set()
        for path in self._paths:
            if path not in sys.modules:
                try:
                    __import__(path)
                except:
                    log.warning('Cannot import module %r' % path, exc_info=True)
                    broken.add(path)

                continue

        self._paths = {path:sys.modules[path] for path in  if path not in broken}
        return self

    def classes(self):
        """
        Provides all the classes from the container module.
        
        @return: AOPClasses
            The loaded module AOP classes.
        """
        self.load()
        classes = {}
        for path, module in self._paths.items():
            for clazz in module.__dict__.values():
                if isclass(clazz) and clazz.__module__ == module.__name__:
                    classes[path + '.' + clazz.__name__] = clazz
                    continue

        return AOPClasses(classes)


class AOPClasses(AOP):
    """
    Container for classes paths.
    """

    def __init__(self, paths):
        """
        Initialize the classes paths container.
        
        @param paths: dictionary{string, class}
            The path mapping of this aop.
        """
        assert isinstance(paths, dict), 'Invalid paths %s' % paths
        for path, clazz in paths.items():
            assert isinstance(path, str), 'Invalid path %s' % path
            if not isclass(clazz):
                raise AssertionError('Invalid class %s' % clazz)

        super().__init__(paths)


class AOPResources(AOP):
    """
    Container for setup entities.
    """

    def __init__(self, resources):
        """
        Initialize the setups paths container.
        
        @param resources: dictionary{string, Callable}
            The resources mapping of this aop.
        """
        assert isinstance(resources, dict), 'Invalid resources %s' % resources
        for path, value in resources.items():
            assert isinstance(path, str), 'Invalid path %s' % path
            if not isinstance(value, str):
                if not callable(value):
                    raise AssertionError('Invalid value %s' % value)

        super().__init__(resources)

    def load(self):
        """
        Loads all the resources from this AOP.
        
        @return: self
            The same instance for chaining.
        """
        self._paths = {path:Assembly.process(path) for path in self._paths}
        return self