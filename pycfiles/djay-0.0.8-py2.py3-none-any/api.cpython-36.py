# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-m_4qh6p6/urllib3/urllib3/packages/rfc3986/api.py
# Compiled at: 2019-07-30 18:47:11
# Size of source mod 2**32: 3887 bytes
"""
Module containing the simple and functional API for rfc3986.

This module defines functions and provides access to the public attributes
and classes of rfc3986.
"""
from .iri import IRIReference
from .parseresult import ParseResult
from .uri import URIReference

def uri_reference(uri, encoding='utf-8'):
    """Parse a URI string into a URIReference.

    This is a convenience function. You could achieve the same end by using
    ``URIReference.from_string(uri)``.

    :param str uri: The URI which needs to be parsed into a reference.
    :param str encoding: The encoding of the string provided
    :returns: A parsed URI
    :rtype: :class:`URIReference`
    """
    return URIReference.from_string(uri, encoding)


def iri_reference(iri, encoding='utf-8'):
    """Parse a IRI string into an IRIReference.

    This is a convenience function. You could achieve the same end by using
    ``IRIReference.from_string(iri)``.

    :param str iri: The IRI which needs to be parsed into a reference.
    :param str encoding: The encoding of the string provided
    :returns: A parsed IRI
    :rtype: :class:`IRIReference`
    """
    return IRIReference.from_string(iri, encoding)


def is_valid_uri(uri, encoding='utf-8', **kwargs):
    """Determine if the URI given is valid.

    This is a convenience function. You could use either
    ``uri_reference(uri).is_valid()`` or
    ``URIReference.from_string(uri).is_valid()`` to achieve the same result.

    :param str uri: The URI to be validated.
    :param str encoding: The encoding of the string provided
    :param bool require_scheme: Set to ``True`` if you wish to require the
        presence of the scheme component.
    :param bool require_authority: Set to ``True`` if you wish to require the
        presence of the authority component.
    :param bool require_path: Set to ``True`` if you wish to require the
        presence of the path component.
    :param bool require_query: Set to ``True`` if you wish to require the
        presence of the query component.
    :param bool require_fragment: Set to ``True`` if you wish to require the
        presence of the fragment component.
    :returns: ``True`` if the URI is valid, ``False`` otherwise.
    :rtype: bool
    """
    return (URIReference.from_string(uri, encoding).is_valid)(**kwargs)


def normalize_uri(uri, encoding='utf-8'):
    """Normalize the given URI.

    This is a convenience function. You could use either
    ``uri_reference(uri).normalize().unsplit()`` or
    ``URIReference.from_string(uri).normalize().unsplit()`` instead.

    :param str uri: The URI to be normalized.
    :param str encoding: The encoding of the string provided
    :returns: The normalized URI.
    :rtype: str
    """
    normalized_reference = URIReference.from_string(uri, encoding).normalize()
    return normalized_reference.unsplit()


def urlparse(uri, encoding='utf-8'):
    """Parse a given URI and return a ParseResult.

    This is a partial replacement of the standard library's urlparse function.

    :param str uri: The URI to be parsed.
    :param str encoding: The encoding of the string provided.
    :returns: A parsed URI
    :rtype: :class:`~rfc3986.parseresult.ParseResult`
    """
    return ParseResult.from_string(uri, encoding, strict=False)