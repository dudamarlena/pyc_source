# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/ocfl/dispositor.py
# Compiled at: 2020-02-25 12:56:35
# Size of source mod 2**32: 1795 bytes
"""Base class for Dispositor objects."""
import os, os.path
try:
    from urllib.parse import quote_plus, unquote_plus
except ImportError:
    from urllib import quote_plus, unquote_plus

class Dispositor(object):
    __doc__ = "Base class for disposition handlers -- let's call them Dispositors."

    def __init__(self):
        """Initialize Dispositor."""
        pass

    def strip_root(self, path, root):
        """Remove root from path, throw exception on failure."""
        root = root.rstrip(os.sep)
        if os.path.commonprefix((path, root)) == root:
            return os.path.relpath(path, start=root)
        raise Exception('Path %s is not in root %s' % (path, root))

    def is_valid(self, identifier):
        """True if identifier is valid, always True in this base implementation."""
        return True

    def encode(self, identifier):
        """Encode identifier to get rid of unsafe chars."""
        return quote_plus(identifier)

    def decode(self, identifier):
        """Decode identifier to put back unsafe chars."""
        return unquote_plus(identifier)

    def identifier_to_path(self, identifier):
        """Convert identifier to path relative to some root."""
        raise Exeption('No yet implemented')

    def relative_path_to_identifier(self, path):
        """Convert relative path to identifier."""
        raise Exeption('No yet implemented')

    def path_to_identifier(self, path, root=None):
        """Convert path relative to root to identifier."""
        if root is not None:
            path = self.strip_root(path, root)
        return self.relative_path_to_identifier(path)