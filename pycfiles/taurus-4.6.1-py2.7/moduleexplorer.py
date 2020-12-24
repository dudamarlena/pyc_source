# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/taurus/test/moduleexplorer.py
# Compiled at: 2019-08-19 15:09:30
"""Utility code for returning info about a module"""
from __future__ import print_function
from builtins import object
import os, inspect, glob, re

class ModuleExplorer(object):

    def __init__(self, exclude_patterns=(), verbose=True):
        """
        :param exclude_patterns: (seq<str>) sequence of strings containing regexp
                                 patterns. Each candidate to be explored will be
                                 matched against these patterns and will be excluded
                                 if it matches any of them.
        :param verbose: (bool) If True (default) status messages will be printed to stdout
        """
        self.exclude_patterns = [ re.compile(p) for p in exclude_patterns ]
        self.verbose = verbose

    def _matchesAnyPattern(self, name, paterns):
        for p in paterns:
            if re.match(p, name) is not None:
                if self.verbose:
                    print('excluding "%s" (matches %s)' % (name, p.pattern))
                return True

        return False

    def _getlocalmembernames(self, module, predicate=None):
        ret = []
        modulepath, _ = os.path.split(inspect.getabsfile(module))
        for n, v in inspect.getmembers(module, predicate):
            if inspect.isbuiltin(v):
                continue
            try:
                memberpath, _ = os.path.split(inspect.getabsfile(v))
            except TypeError:
                continue

            if memberpath == modulepath:
                ret.append(n)

        return ret

    def _getSubpackagesFromPath(self, modulepath):
        g = glob.glob(os.path.join(modulepath, '*', '__init__.py'))
        ret = [ re.findall('.+\\/(.*)\\/__init__.py', s)[0] for s in g ]
        return ret

    def _getSubmodulesFromPath(self, modulepath, module):
        _imp = [ n for n, m in inspect.getmembers(module, inspect.ismodule) ]
        ret = []
        for s in glob.glob(os.path.join(modulepath, '*.py')):
            f = os.path.split(s)[1][:-3]
            if not f.startswith('_') and f not in _imp:
                ret.append(f)

        return ret

    def _isclass_with_init(self, obj):
        return inspect.isclass(obj) and hasattr(obj, '__init__')

    def _isenumeration(self, obj):
        return False

    def exploreModule(self, modulename):
        """Recursive function that gathers info on a module and all its submodules.

        :param modulename: the name of the module to explore

        :return: (dict<str,object>) a dictionary containing submodulenames,
                 localclassnames, localfunctionnames, localenumerationnames,
                 externalmembernames, submodules, warnings
        """
        if self.verbose:
            print('Exploring %s...' % modulename)
        warnings = []
        try:
            module = __import__(modulename, fromlist=[''])
        except Exception as e:
            msg = 'exploreModule: WARNING: Cannot import %s. Reason: %s' % (
             modulename, repr(e))
            warnings.append(msg)
            if self.verbose:
                print(msg)
            return dict(modulename=modulename, basemodulename=modulename.split('.')[(-1)], modulepath=None, submodulenames=[], localclassnames=[], localfunctionnames=[], localenumerationnames=[], externalmembernames=[], submodules={}, warnings=warnings)

        if module.__name__ == module.__package__:
            modulepath, _ = os.path.split(inspect.getabsfile(module))
        else:
            modulepath = inspect.getabsfile(module)
        submodulenames = sorted(self._getSubpackagesFromPath(modulepath) + self._getSubmodulesFromPath(modulepath, module))
        localclassnames = sorted(self._getlocalmembernames(module, self._isclass_with_init))
        localfunctionnames = sorted(self._getlocalmembernames(module, inspect.isfunction))
        localenumerationnames = sorted([])
        externalmembernames = sorted([])
        submodulenames = [ n for n in submodulenames if not self._matchesAnyPattern(('.').join((modulename, n)), self.exclude_patterns)
                         ]
        localclassnames = [ n for n in localclassnames if not self._matchesAnyPattern(('.').join((modulename, n)), self.exclude_patterns)
                          ]
        localfunctionnames = [ n for n in localfunctionnames if not self._matchesAnyPattern(('.').join((modulename, n)), self.exclude_patterns)
                             ]
        localenumerationnames = [ n for n in localenumerationnames if not self._matchesAnyPattern(('.').join((modulename, n)), self.exclude_patterns)
                                ]
        externalmembernames = [ n for n in externalmembernames if not self._matchesAnyPattern(('.').join((modulename, n)), self.exclude_patterns)
                              ]
        submodules = {}
        for n in submodulenames:
            sm_name = ('.').join((modulename, n))
            submodules[n] = self.exploreModule(sm_name)

        return dict(modulename=modulename, basemodulename=modulename.split('.')[(-1)], modulepath=modulepath, submodulenames=submodulenames, localclassnames=localclassnames, localfunctionnames=localfunctionnames, localenumerationnames=localenumerationnames, externalmembernames=externalmembernames, submodules=submodules, warnings=warnings)

    @staticmethod
    def getAll(info, key):
        """
        append all values for a given key in a nested "moduleinfo" dictionary

        :param info: (dict) a moduleinfo dictionary like the one returned by :meth:`exploreModule`
        :param key: (str) a key of a moduleinfo dictionary

        :return: (list<tuple>) a list that concatenates tuples where the first element is  the (sub)module name
                 and the second element is the value for the given key.
                 If for a certain submodule, the value is empty, it is not included in the list at all.
        """
        mname = info['modulename']
        try:
            if not isinstance(info[key], list):
                ret = [
                 (
                  mname, info[key])]
            else:
                ret = [ (mname, el) for el in info[key] ]
        except KeyError:
            return []

        for sminfo in info['submodules'].values():
            ret += ModuleExplorer.getAll(sminfo, key)

        return ret

    @staticmethod
    def explore(modulename, exclude_patterns=(), verbose=True):
        """convenience to explore a module

        :param modulename: the name of the module to explore
        :param exclude_patterns: (seq<str>) sequence of strings containing regexp
                                 patterns. Each candidate to be explored will be
                                 matched against these patterns and will be excluded
                                 if it matches any of them.
        :param verbose: (bool) If True (default) status messages will be printed to stdout

        :return: (dict<str,object>, allwarnings) a tuple whose first member is a dictionary
                 containing submodulenames, localclassnames, localfunctionnames, localenumerationnames,
                 externalmembernames, submodules, warnings. The second member of the tuple is a list
                 containing all the warnings accummulated.
        """
        explorer = ModuleExplorer(exclude_patterns=exclude_patterns, verbose=verbose)
        minfo = explorer.exploreModule(modulename)
        return (minfo, ModuleExplorer.getAll(minfo, 'warnings'))


def main(modulename='taurus', exclude_patterns=('_[^\\.]*[^_]', '.*\\.test', 'taurus\\.external', 'taurus\\.qt\\.qtgui\\.extra_sardana',
 'taurus\\.qt\\.qtgui\\.extra_pool', 'taurus\\.qt\\.qtgui\\.extra_macroexecutor',
 'taurus\\.qt\\.qtgui\\.resource', 'taurus\\.qt\\.qtgui\\.taurusgui\\.conf')):
    moduleinfo, allw = ModuleExplorer.explore(modulename, exclude_patterns=exclude_patterns, verbose=True)
    print('\n\n' + '*' * 50)
    print('Exploration finished with %i warnings:' % len(allw))
    for m, w in allw:
        print(w)

    print('*' * 50 + '\n')
    print()
    print(len(allw))
    assert len(allw) == 0


if __name__ == '__main__':
    main()