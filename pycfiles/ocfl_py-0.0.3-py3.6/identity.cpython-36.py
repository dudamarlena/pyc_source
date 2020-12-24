# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/ocfl/identity.py
# Compiled at: 2019-03-15 08:50:27
# Size of source mod 2**32: 841 bytes
"""Identity mapping of identifier to directory structure."""
import os
from .dispositor import Dispositor

class Identity(Dispositor):
    __doc__ = 'Class to support trivial identity disposition.'

    def __init__(self):
        super(Identity, self).__init__()

    def identifier_to_path(self, identifier):
        """Convert identifier to path relative to root."""
        return self.encode(identifier)

    def relative_path_to_identifier(self, path):
        """Convert relative path to identifier.

        It is an error to include more than one path segment so raise
        and exception if os.sep exists in the path.
        """
        if os.sep in path:
            raise Exception('Relative path in Identity dispositor must not have multiple path segments!')
        return self.decode(path)