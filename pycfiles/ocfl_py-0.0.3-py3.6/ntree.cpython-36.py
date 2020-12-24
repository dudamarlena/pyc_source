# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/ocfl/ntree.py
# Compiled at: 2019-03-15 08:50:27
# Size of source mod 2**32: 2174 bytes
"""Handle pairtree (n=2) and similar directory structures.

Note that saying Pairtree for a given n, default 2, is not sufficient
to define the object layout. The Pairtree specification
https://confluence.ucop.edu/display/Curation/PairTree
encourages the use of object encapsulation (section 3) but does
not prescribe a particular method. In this implementation the default
it to encapsulate in a directory with the complete encoded identifier
name.

Makes use of encoding and decoding functions from Ben O'Steen's
implementation in the pairtree module
(https://github.com/benosteen/pairtree).
"""
import os, os.path
from pairtree import id_encode, id_decode
from .dispositor import Dispositor

class Ntree(Dispositor):
    __doc__ = 'Class to support pairtree and related dispositions.'

    def __init__(self, n=2, encapsulate=True):
        """Initialize Dispositor."""
        super(Ntree, self).__init__()
        self.n = n
        self.encapsulate = encapsulate

    def encode(self, identifier):
        """Pairtree encode identifier."""
        return id_encode(identifier)

    def decode(self, identifier):
        """Pairtree decode identifier."""
        return id_decode(identifier)

    def identifier_to_path(self, identifier):
        """Convert identifier to path relative to root."""
        identifier = self.encode(identifier)
        path = ''
        id_remains = identifier
        segments = []
        while len(id_remains) > self.n:
            segments.append(id_remains[0:self.n])
            id_remains = id_remains[self.n:]

        segments.append(id_remains)
        if self.encapsulate:
            segments.append(identifier)
        return (os.path.join)(*segments)

    def relative_path_to_identifier(self, path):
        """Convert relative path to identifier."""
        if self.encapsulate:
            path, encap_id = os.path.split(path)
        identifier = ''.join(path.split(os.sep))
        if self.encapsulate:
            if identifier != encap_id:
                raise Exception('Bad ntree path: id from path (%s) does not match encapsulation id (%s)' % (identifier, encap_id))
        return identifier