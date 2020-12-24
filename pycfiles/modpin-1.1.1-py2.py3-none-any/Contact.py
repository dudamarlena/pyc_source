# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/patri/MODPIN/modpin/./src/SBI/structure/contacts/contact/Contact.py
# Compiled at: 2020-04-28 10:16:58
"""
Contact

author: jbonet
date:   03/2013

@oliva's lab
"""
import hashlib

class Contact(object):
    available_distance_types = set()
    atomic_types = set()
    description = ''

    def __init__(self, residue1, residue2):
        self._residue1 = residue1
        r1 = residue1.type + residue1.identifier
        self._residue2 = residue2
        r2 = residue2.type + residue2.identifier
        self._md5 = tuple(sorted([hashlib.sha224(r1 + r2).hexdigest()]))
        self._distance = {}
        self._underthreshold = False
        self._build()

    @property
    def md5s(self):
        return self._md5

    @property
    def description(self):
        return self.description

    @property
    def is_underthreshold(self):
        return self._underthreshold

    def reverse(self):
        self._residue1, self._residue2 = self._residue2, self._residue1
        for dist_type in self.available_distance_types:
            self._distance[dist_type] = (
             self._distance[dist_type][1], self._distance[dist_type][0], self._distance[dist_type][2])

    def _build(self):
        raise NotImplementedError

    def _check_type(self, requested_type):
        if requested_type not in self.available_distance_types:
            raise AttributeError(('Available distance types are {0}.\n').format(repr(self.available_distance_types)))

    def __eq__(self, other):
        return self.md5s == other.md5s

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return self.md5s.__hash__()