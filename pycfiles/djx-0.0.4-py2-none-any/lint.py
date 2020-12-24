# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-HZd96S/pip/pip/_vendor/html5lib/filters/lint.py
# Compiled at: 2019-02-14 00:35:07
from __future__ import absolute_import, division, unicode_literals
from pip._vendor.six import text_type
from . import base
from ..constants import namespaces, voidElements
from ..constants import spaceCharacters
spaceCharacters = (b'').join(spaceCharacters)

class Filter(base.Filter):
    """Lints the token stream for errors

    If it finds any errors, it'll raise an ``AssertionError``.

    """

    def __init__(self, source, require_matching_tags=True):
        """Creates a Filter

        :arg source: the source token stream

        :arg require_matching_tags: whether or not to require matching tags

        """
        super(Filter, self).__init__(source)
        self.require_matching_tags = require_matching_tags

    def __iter__(self):
        open_elements = []
        for token in base.Filter.__iter__(self):
            type = token[b'type']
            if type in ('StartTag', 'EmptyTag'):
                namespace = token[b'namespace']
                name = token[b'name']
                assert namespace is None or isinstance(namespace, text_type)
                assert namespace != b''
                assert isinstance(name, text_type)
                assert name != b''
                assert isinstance(token[b'data'], dict)
                if (not namespace or namespace == namespaces[b'html']) and name in voidElements:
                    assert type == b'EmptyTag'
                else:
                    assert type == b'StartTag'
                if type == b'StartTag' and self.require_matching_tags:
                    open_elements.append((namespace, name))
                for (namespace, name), value in token[b'data'].items():
                    assert namespace is None or isinstance(namespace, text_type)
                    assert namespace != b''
                    assert isinstance(name, text_type)
                    assert name != b''
                    assert isinstance(value, text_type)

            elif type == b'EndTag':
                namespace = token[b'namespace']
                name = token[b'name']
                assert namespace is None or isinstance(namespace, text_type)
                assert namespace != b''
                assert isinstance(name, text_type)
                assert name != b''
                if (not namespace or namespace == namespaces[b'html']) and name in voidElements:
                    assert False, b'Void element reported as EndTag token: %(tag)s' % {b'tag': name}
                elif self.require_matching_tags:
                    start = open_elements.pop()
                    assert start == (namespace, name)
            elif type == b'Comment':
                data = token[b'data']
                assert isinstance(data, text_type)
            elif type in ('Characters', 'SpaceCharacters'):
                data = token[b'data']
                assert isinstance(data, text_type)
                assert data != b''
                if type == b'SpaceCharacters':
                    assert data.strip(spaceCharacters) == b''
            elif type == b'Doctype':
                name = token[b'name']
                assert name is None or isinstance(name, text_type)
                assert token[b'publicId'] is None or isinstance(name, text_type)
                assert token[b'systemId'] is None or isinstance(name, text_type)
            elif type == b'Entity':
                assert isinstance(token[b'name'], text_type)
            elif type == b'SerializerError':
                assert isinstance(token[b'data'], text_type)
            else:
                assert False, b'Unknown token type: %(type)s' % {b'type': type}
            yield token

        return