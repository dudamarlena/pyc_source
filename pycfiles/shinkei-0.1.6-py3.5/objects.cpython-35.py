# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/shinkei/objects.py
# Compiled at: 2019-12-14 12:45:46
# Size of source mod 2**32: 3076 bytes
import re

class Version:
    __doc__ = 'An object representing the API and singyeong version.\n\n    Attributes\n    ----------\n    api: :class:`str`\n        The API version, in ``vN`` format.\n    singyeong: :class:`str`\n        The singyeong version, in ``x.y.z`` format.\n    '
    __slots__ = ('api', 'singyeong')

    def __init__(self, data):
        self.api = data['api']
        self.singyeong = data['singyeong']

    def __repr__(self):
        return '<Version api={0.api} singyeong={0.singyeong}>'.format(self)


class MetadataPayload:
    __doc__ = 'An object representing a payload of data received from a client.\n\n    Attributes\n    ----------\n    nonce\n        A unique nonce used to identify the payload.\n    payload: Union[:class:`str`, :class:`int`, :class:`float`, :class:`list`, :class:`dict`]\n        The payload.\n    '
    __slots__ = ('nonce', 'payload')

    def __init__(self, data):
        self.nonce = data['nonce']
        self.payload = data['payload']

    def __repr__(self):
        return '<MetadataPayload nonce={0.nonce!r}>'.format(self)


class VersionMetadata:
    __doc__ = 'An object to represent a version object in :meth:`Client.update_metadata`.\n\n    This is *NOT* the same as :class:`Version`.\n\n    Parameters\n    ----------\n    fmt: :class:`str`\n        The version string.\n        Must be complient to the `elixir specification <https://hexdocs.pm/elixir/Version.html>`_.\n    '
    __slots__ = ('fmt', '_groups')
    VALIDATION_REGEX = re.compile('\n    ^(0|[1-9]\\d*)\\.(0|[1-9]\\d*)\\.(0|[1-9]\\d*)\n    (?:-((?:0|[1-9]\\d*|\\d*[a-zA-Z-][0-9a-zA-Z-]*)\n    (?:\\.(?:0|[1-9]\\d*|\\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?\n    (?:\\+([0-9a-zA-Z-]+(?:\\.[0-9a-zA-Z-]+)*))?$\n    ', re.VERBOSE)

    def __init__(self, fmt):
        match = self.VALIDATION_REGEX.match(fmt)
        if not match or not match.group(0):
            raise ValueError('Invalid version format.')
        self.fmt = fmt
        self._groups = match.groups(default='0')

    def __str__(self):
        return self.fmt

    def __repr__(self):
        return '<VersionMetadata fmt={0.fmt!r}>'.format(self)

    def __eq__(self, other):
        return isinstance(other, VersionMetadata) and self._groups == other._groups

    def __ne__(self, other):
        return not self.__eq__(other)

    def __le__(self, other):
        if isinstance(other, VersionMetadata):
            return self._groups <= other._groups
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, VersionMetadata):
            return self._groups < other._groups
        return NotImplemented

    def __ge__(self, other):
        if isinstance(other, VersionMetadata):
            return self._groups >= other._groups
        return NotImplemented

    def __gt__(self, other):
        if isinstance(other, VersionMetadata):
            return self._groups > other._groups
        return NotImplemented