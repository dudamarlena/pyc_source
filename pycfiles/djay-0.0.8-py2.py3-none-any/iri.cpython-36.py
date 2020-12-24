# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-m_4qh6p6/urllib3/urllib3/packages/rfc3986/iri.py
# Compiled at: 2019-07-30 18:47:11
# Size of source mod 2**32: 5466 bytes
"""Module containing the implementation of the IRIReference class."""
from collections import namedtuple
from . import compat
from . import exceptions
from . import misc
from . import normalizers
from . import uri
try:
    import idna
except ImportError:
    idna = None

class IRIReference(namedtuple('IRIReference', misc.URI_COMPONENTS), uri.URIMixin):
    __doc__ = 'Immutable object representing a parsed IRI Reference.\n\n    Can be encoded into an URIReference object via the procedure\n    specified in RFC 3987 Section 3.1\n\n     .. note::\n        The IRI submodule is a new interface and may possibly change in\n        the future. Check for changes to the interface when upgrading.\n    '
    slots = ()

    def __new__(cls, scheme, authority, path, query, fragment, encoding='utf-8'):
        """Create a new IRIReference."""
        ref = super(IRIReference, cls).__new__(cls, scheme or None, authority or None, path or None, query, fragment)
        ref.encoding = encoding
        return ref

    def __eq__(self, other):
        """Compare this reference to another."""
        other_ref = other
        if isinstance(other, tuple):
            other_ref = (self.__class__)(*other)
        else:
            if not isinstance(other, IRIReference):
                try:
                    other_ref = self.__class__.from_string(other)
                except TypeError:
                    raise TypeError('Unable to compare {0}() to {1}()'.format(type(self).__name__, type(other).__name__))

        return tuple(self) == tuple(other_ref)

    def _match_subauthority(self):
        return misc.ISUBAUTHORITY_MATCHER.match(self.authority)

    @classmethod
    def from_string(cls, iri_string, encoding='utf-8'):
        """Parse a IRI reference from the given unicode IRI string.

        :param str iri_string: Unicode IRI to be parsed into a reference.
        :param str encoding: The encoding of the string provided
        :returns: :class:`IRIReference` or subclass thereof
        """
        iri_string = compat.to_str(iri_string, encoding)
        split_iri = misc.IRI_MATCHER.match(iri_string).groupdict()
        return cls(split_iri['scheme'], split_iri['authority'], normalizers.encode_component(split_iri['path'], encoding), normalizers.encode_component(split_iri['query'], encoding), normalizers.encode_component(split_iri['fragment'], encoding), encoding)

    def encode(self, idna_encoder=None):
        """Encode an IRIReference into a URIReference instance.

        If the ``idna`` module is installed or the ``rfc3986[idna]``
        extra is used then unicode characters in the IRI host
        component will be encoded with IDNA2008.

        :param idna_encoder:
            Function that encodes each part of the host component
            If not given will raise an exception if the IRI
            contains a host component.
        :rtype: uri.URIReference
        :returns: A URI reference
        """
        authority = self.authority
        if authority:
            if idna_encoder is None:
                if idna is None:
                    raise exceptions.MissingDependencyError("Could not import the 'idna' module and the IRI hostname requires encoding")

                def idna_encoder(name):
                    if any(ord(c) > 128 for c in name):
                        try:
                            return idna.encode((name.lower()), strict=True,
                              std3_rules=True)
                        except idna.IDNAError:
                            raise exceptions.InvalidAuthority(self.authority)

                    return name

            else:
                authority = ''
                if self.host:
                    authority = '.'.join([compat.to_str(idna_encoder(part)) for part in self.host.split('.')])
                if self.userinfo is not None:
                    authority = normalizers.encode_component(self.userinfo, self.encoding) + '@' + authority
                if self.port is not None:
                    authority += ':' + str(self.port)
        return uri.URIReference((self.scheme), authority,
          path=(self.path),
          query=(self.query),
          fragment=(self.fragment),
          encoding=(self.encoding))