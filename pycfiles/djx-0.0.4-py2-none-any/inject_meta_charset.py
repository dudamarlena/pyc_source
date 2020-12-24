# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-HZd96S/pip/pip/_vendor/html5lib/filters/inject_meta_charset.py
# Compiled at: 2019-02-14 00:35:07
from __future__ import absolute_import, division, unicode_literals
from . import base

class Filter(base.Filter):
    """Injects ``<meta charset=ENCODING>`` tag into head of document"""

    def __init__(self, source, encoding):
        """Creates a Filter

        :arg source: the source token stream

        :arg encoding: the encoding to set

        """
        base.Filter.__init__(self, source)
        self.encoding = encoding

    def __iter__(self):
        state = b'pre_head'
        meta_found = self.encoding is None
        pending = []
        for token in base.Filter.__iter__(self):
            type = token[b'type']
            if type == b'StartTag':
                if token[b'name'].lower() == b'head':
                    state = b'in_head'
            elif type == b'EmptyTag':
                if token[b'name'].lower() == b'meta':
                    has_http_equiv_content_type = False
                    for (namespace, name), value in token[b'data'].items():
                        if namespace is not None:
                            continue
                        elif name.lower() == b'charset':
                            token[b'data'][(namespace, name)] = self.encoding
                            meta_found = True
                            break
                        elif name == b'http-equiv' and value.lower() == b'content-type':
                            has_http_equiv_content_type = True
                    else:
                        if has_http_equiv_content_type and (None, 'content') in token[b'data']:
                            token[b'data'][(None, 'content')] = b'text/html; charset=%s' % self.encoding
                            meta_found = True
                elif token[b'name'].lower() == b'head' and not meta_found:
                    yield {b'type': b'StartTag', b'name': b'head', b'data': token[b'data']}
                    yield {b'type': b'EmptyTag', b'name': b'meta', b'data': {(None, 'charset'): self.encoding}}
                    yield {b'type': b'EndTag', b'name': b'head'}
                    meta_found = True
                    continue
            elif type == b'EndTag':
                if token[b'name'].lower() == b'head' and pending:
                    yield pending.pop(0)
                    if not meta_found:
                        yield {b'type': b'EmptyTag', b'name': b'meta', b'data': {(None, 'charset'): self.encoding}}
                    while pending:
                        yield pending.pop(0)

                    meta_found = True
                    state = b'post_head'
            if state == b'in_head':
                pending.append(token)
            else:
                yield token

        return