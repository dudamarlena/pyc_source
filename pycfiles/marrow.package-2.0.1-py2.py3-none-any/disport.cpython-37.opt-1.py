# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /marrow/package/disport.py
# Compiled at: 2019-01-22 13:34:55
# Size of source mod 2**32: 2894 bytes
"""Import redirector registry utility.

Disport; noun: diversion from work or serious matters; recreation or amusement.
"""
from collections import deque
from typeguard import check_argument_types
from typing import Sequence, Iterable
from .loader import load, nodefault

class Importer:
    __doc__ = 'A helper class to redirect imports and plugin loading.\n\t\n\tPredominantly useful when paired with a template importer such as web.template or import-based template engine\n\tlike cinje to allow for overriding of page components.\n\t\n\tLater overrides take precedence over earlier ones, and are evaluated using a prefix search to construct a list of\n\tcandidate import paths. Each is attempted until one succeeds, or none succeed, at which point the original import\n\tis attempted.\n\t\n\tPlugin names can be overridden as well, however, the destination should still be a module path. The object name\n\treferenced by the original entry_point will be attempted against the overridden path, with similar fallback to the\n\toriginal.\n\t'
    __slots__ = ('redirects', 'namespace', 'separators', 'executable', 'protect')

    def __init__(self, redirect=None, namespace=None, separators=('.', ':'), executable=False, protect=True):
        """Configure the disport Importer.
                
                The arguments are essentially the same as those for the load or lazyload utilities, with the addition of the
                ability to specify an initial iterable of overrides through the `redirect` argument. This should be an
                iterable of tuples (or tuple-alikes) in the form `(source, destination)`.
                """
        assert check_argument_types()
        super().__init__()
        self.redirects = deque()
        self.namespace = namespace
        self.separators = separators
        self.executable = executable
        self.protect = protect
        for source, destination in redirect:
            self.redirect(source, destination)

    def redirect(self, source: str, destination: str):
        assert check_argument_types()
        self.redirects.appendleft((source, destination))

    def __call__(self, target: str, default=nodefault):
        assert check_argument_types()
        for candidate, destination in self.redirects:
            if candidate == target:
                return
                if not target.startswith(candidate):
                    continue
                candidate = load((target.replace(candidate, destination, 1)),
                  namespace=(self.namespace),
                  default=None,
                  executable=(self.executable),
                  separators=(self.separators),
                  protect=(self.protect))
                if candidate is not None:
                    return candidate

        return load((target.replace(candidate, destination)),
          namespace=(self.namespace),
          default=default,
          executable=(self.executable),
          separators=(self.separators),
          protect=(self.protect))