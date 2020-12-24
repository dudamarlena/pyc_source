# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-uunam8sj/pip/pip/_vendor/html5lib/filters/lint.py
# Compiled at: 2020-03-25 22:23:37
# Size of source mod 2**32: 3643 bytes
from __future__ import absolute_import, division, unicode_literals
from pip._vendor.six import text_type
from . import base
from ..constants import namespaces, voidElements
from ..constants import spaceCharacters
spaceCharacters = ''.join(spaceCharacters)

class Filter(base.Filter):
    __doc__ = "Lints the token stream for errors\n\n    If it finds any errors, it'll raise an ``AssertionError``.\n\n    "

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
            type = token['type']
            if type in ('StartTag', 'EmptyTag'):
                namespace = token['namespace']
                name = token['name']
                if not namespace is None:
                    if not isinstance(namespace, text_type):
                        raise AssertionError
                assert namespace != ''
                assert isinstance(name, text_type)
                assert name != ''
                assert isinstance(token['data'], dict)
                if (not namespace or namespace == namespaces['html']) and name in voidElements:
                    assert type == 'EmptyTag'
                else:
                    assert type == 'StartTag'
                if type == 'StartTag':
                    if self.require_matching_tags:
                        open_elements.append((namespace, name))
                for (namespace, name), value in token['data'].items():
                    if not namespace is None:
                        if not isinstance(namespace, text_type):
                            raise AssertionError
                        else:
                            if not namespace != '':
                                raise AssertionError
                            elif not isinstance(name, text_type):
                                raise AssertionError
                            assert name != ''
                        assert isinstance(value, text_type)

            else:
                if type == 'EndTag':
                    namespace = token['namespace']
                    name = token['name']
                    if not namespace is None:
                        if not isinstance(namespace, text_type):
                            raise AssertionError
                    assert namespace != ''
                    assert isinstance(name, text_type)
                    assert name != ''
                    if (not namespace or namespace == namespaces['html']) and name in voidElements:
                        assert False, 'Void element reported as EndTag token: %(tag)s' % {'tag': name}
                    else:
                        if self.require_matching_tags:
                            start = open_elements.pop()
                            assert start == (namespace, name)
                else:
                    if type == 'Comment':
                        data = token['data']
                        assert isinstance(data, text_type)
                    else:
                        if type in ('Characters', 'SpaceCharacters'):
                            data = token['data']
                            assert isinstance(data, text_type)
                            assert data != ''
                            if type == 'SpaceCharacters':
                                assert data.strip(spaceCharacters) == ''
                        else:
                            if type == 'Doctype':
                                name = token['name']
                                if not name is None:
                                    if not isinstance(name, text_type):
                                        raise AssertionError
                                if not token['publicId'] is None:
                                    if not isinstance(name, text_type):
                                        raise AssertionError
                                if not token['systemId'] is None:
                                    assert isinstance(name, text_type)
                            else:
                                if type == 'Entity':
                                    assert isinstance(token['name'], text_type)
                                else:
                                    if type == 'SerializerError':
                                        assert isinstance(token['data'], text_type)
                                    else:
                                        assert False, 'Unknown token type: %(type)s' % {'type': type}
            yield token