# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-HZd96S/pip/pip/_vendor/html5lib/filters/optionaltags.py
# Compiled at: 2019-02-14 00:35:07
from __future__ import absolute_import, division, unicode_literals
from . import base

class Filter(base.Filter):
    """Removes optional tags from the token stream"""

    def slider(self):
        previous1 = previous2 = None
        for token in self.source:
            if previous1 is not None:
                yield (
                 previous2, previous1, token)
            previous2 = previous1
            previous1 = token

        if previous1 is not None:
            yield (
             previous2, previous1, None)
        return

    def __iter__(self):
        for previous, token, next in self.slider():
            type = token[b'type']
            if type == b'StartTag':
                if token[b'data'] or not self.is_optional_start(token[b'name'], previous, next):
                    yield token
            elif type == b'EndTag':
                if not self.is_optional_end(token[b'name'], next):
                    yield token
            else:
                yield token

    def is_optional_start(self, tagname, previous, next):
        type = next and next[b'type'] or None
        if tagname in b'html':
            return type not in ('Comment', 'SpaceCharacters')
        else:
            if tagname == b'head':
                if type in ('StartTag', 'EmptyTag'):
                    return True
                if type == b'EndTag':
                    return next[b'name'] == b'head'
            elif tagname == b'body':
                if type in ('Comment', 'SpaceCharacters'):
                    return False
                else:
                    if type == b'StartTag':
                        return next[b'name'] not in ('script', 'style')
                    return True

            elif tagname == b'colgroup':
                if type in ('StartTag', 'EmptyTag'):
                    return next[b'name'] == b'col'
                else:
                    return False

            elif tagname == b'tbody':
                if type == b'StartTag':
                    if previous and previous[b'type'] == b'EndTag' and previous[b'name'] in ('tbody',
                                                                                             'thead',
                                                                                             'tfoot'):
                        return False
                    return next[b'name'] == b'tr'
                else:
                    return False

            return False

    def is_optional_end(self, tagname, next):
        type = next and next[b'type'] or None
        if tagname in ('html', 'head', 'body'):
            return type not in ('Comment', 'SpaceCharacters')
        else:
            if tagname in ('li', 'optgroup', 'tr'):
                if type == b'StartTag':
                    return next[b'name'] == tagname
                else:
                    return type == b'EndTag' or type is None

            elif tagname in ('dt', 'dd'):
                if type == b'StartTag':
                    return next[b'name'] in ('dt', 'dd')
                else:
                    if tagname == b'dd':
                        return type == b'EndTag' or type is None
                    return False

            elif tagname == b'p':
                if type in ('StartTag', 'EmptyTag'):
                    return next[b'name'] in ('address', 'article', 'aside', 'blockquote',
                                             'datagrid', 'dialog', 'dir', 'div',
                                             'dl', 'fieldset', 'footer', 'form',
                                             'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
                                             'header', 'hr', 'menu', 'nav', 'ol',
                                             'p', 'pre', 'section', 'table', 'ul')
                else:
                    return type == b'EndTag' or type is None

            elif tagname == b'option':
                if type == b'StartTag':
                    return next[b'name'] in ('option', 'optgroup')
                else:
                    return type == b'EndTag' or type is None

            elif tagname in ('rt', 'rp'):
                if type == b'StartTag':
                    return next[b'name'] in ('rt', 'rp')
                else:
                    return type == b'EndTag' or type is None

            elif tagname == b'colgroup':
                if type in ('Comment', 'SpaceCharacters'):
                    return False
                else:
                    if type == b'StartTag':
                        return next[b'name'] != b'colgroup'
                    return True

            elif tagname in ('thead', 'tbody'):
                if type == b'StartTag':
                    return next[b'name'] in ('tbody', 'tfoot')
                else:
                    if tagname == b'tbody':
                        return type == b'EndTag' or type is None
                    return False

            elif tagname == b'tfoot':
                if type == b'StartTag':
                    return next[b'name'] == b'tbody'
                else:
                    return type == b'EndTag' or type is None

            elif tagname in ('td', 'th'):
                if type == b'StartTag':
                    return next[b'name'] in ('td', 'th')
                else:
                    return type == b'EndTag' or type is None

            return False