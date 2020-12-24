# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-m_4qh6p6/urllib3/urllib3/packages/rfc3986/uri.py
# Compiled at: 2019-07-30 18:47:11
# Size of source mod 2**32: 5227 bytes
"""Module containing the implementation of the URIReference class."""
from collections import namedtuple
from . import compat
from . import misc
from . import normalizers
from ._mixin import URIMixin

class URIReference(namedtuple('URIReference', misc.URI_COMPONENTS), URIMixin):
    __doc__ = 'Immutable object representing a parsed URI Reference.\n\n    .. note::\n\n        This class is not intended to be directly instantiated by the user.\n\n    This object exposes attributes for the following components of a\n    URI:\n\n    - scheme\n    - authority\n    - path\n    - query\n    - fragment\n\n    .. attribute:: scheme\n\n        The scheme that was parsed for the URI Reference. For example,\n        ``http``, ``https``, ``smtp``, ``imap``, etc.\n\n    .. attribute:: authority\n\n        Component of the URI that contains the user information, host,\n        and port sub-components. For example,\n        ``google.com``, ``127.0.0.1:5000``, ``username@[::1]``,\n        ``username:password@example.com:443``, etc.\n\n    .. attribute:: path\n\n        The path that was parsed for the given URI Reference. For example,\n        ``/``, ``/index.php``, etc.\n\n    .. attribute:: query\n\n        The query component for a given URI Reference. For example, ``a=b``,\n        ``a=b%20c``, ``a=b+c``, ``a=b,c=d,e=%20f``, etc.\n\n    .. attribute:: fragment\n\n        The fragment component of a URI. For example, ``section-3.1``.\n\n    This class also provides extra attributes for easier access to information\n    like the subcomponents of the authority component.\n\n    .. attribute:: userinfo\n\n        The user information parsed from the authority.\n\n    .. attribute:: host\n\n        The hostname, IPv4, or IPv6 adddres parsed from the authority.\n\n    .. attribute:: port\n\n        The port parsed from the authority.\n    '
    slots = ()

    def __new__(cls, scheme, authority, path, query, fragment, encoding='utf-8'):
        """Create a new URIReference."""
        ref = super(URIReference, cls).__new__(cls, scheme or None, authority or None, path or None, query, fragment)
        ref.encoding = encoding
        return ref

    __hash__ = tuple.__hash__

    def __eq__(self, other):
        """Compare this reference to another."""
        other_ref = other
        if isinstance(other, tuple):
            other_ref = URIReference(*other)
        else:
            if not isinstance(other, URIReference):
                try:
                    other_ref = URIReference.from_string(other)
                except TypeError:
                    raise TypeError('Unable to compare URIReference() to {0}()'.format(type(other).__name__))

        naive_equality = tuple(self) == tuple(other_ref)
        return naive_equality or self.normalized_equality(other_ref)

    def normalize(self):
        """Normalize this reference as described in Section 6.2.2.

        This is not an in-place normalization. Instead this creates a new
        URIReference.

        :returns: A new reference object with normalized components.
        :rtype: URIReference
        """
        return URIReference(normalizers.normalize_scheme(self.scheme or ''), normalizers.normalize_authority((
         self.userinfo, self.host, self.port)), normalizers.normalize_path(self.path or ''), normalizers.normalize_query(self.query), normalizers.normalize_fragment(self.fragment), self.encoding)

    @classmethod
    def from_string(cls, uri_string, encoding='utf-8'):
        """Parse a URI reference from the given unicode URI string.

        :param str uri_string: Unicode URI to be parsed into a reference.
        :param str encoding: The encoding of the string provided
        :returns: :class:`URIReference` or subclass thereof
        """
        uri_string = compat.to_str(uri_string, encoding)
        split_uri = misc.URI_MATCHER.match(uri_string).groupdict()
        return cls(split_uri['scheme'], split_uri['authority'], normalizers.encode_component(split_uri['path'], encoding), normalizers.encode_component(split_uri['query'], encoding), normalizers.encode_component(split_uri['fragment'], encoding), encoding)