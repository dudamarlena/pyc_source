# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/cryptography/cryptography/hazmat/_oid.py
# Compiled at: 2020-01-10 16:25:37
# Size of source mod 2**32: 2178 bytes
from __future__ import absolute_import, division, print_function
from cryptography import utils

class ObjectIdentifier(object):

    def __init__(self, dotted_string):
        self._dotted_string = dotted_string
        nodes = self._dotted_string.split('.')
        intnodes = []
        for node in nodes:
            try:
                intnodes.append(int(node, 0))
            except ValueError:
                raise ValueError('Malformed OID: %s (non-integer nodes)' % self._dotted_string)

        if len(nodes) < 2:
            raise ValueError('Malformed OID: %s (insufficient number of nodes)' % self._dotted_string)
        if intnodes[0] > 2:
            raise ValueError('Malformed OID: %s (first node outside valid range)' % self._dotted_string)
        if intnodes[0] < 2:
            if intnodes[1] >= 40:
                raise ValueError('Malformed OID: %s (second node outside valid range)' % self._dotted_string)

    def __eq__(self, other):
        if not isinstance(other, ObjectIdentifier):
            return NotImplemented
        else:
            return self.dotted_string == other.dotted_string

    def __ne__(self, other):
        return not self == other

    def __repr__(self):
        return '<ObjectIdentifier(oid={}, name={})>'.format(self.dotted_string, self._name)

    def __hash__(self):
        return hash(self.dotted_string)

    @property
    def _name(self):
        from cryptography.x509.oid import _OID_NAMES
        return _OID_NAMES.get(self, 'Unknown OID')

    dotted_string = utils.read_only_property('_dotted_string')