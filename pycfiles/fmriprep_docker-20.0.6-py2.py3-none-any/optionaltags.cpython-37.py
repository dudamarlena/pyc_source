# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-hbx1i2h0/pip/pip/_vendor/html5lib/filters/optionaltags.py
# Compiled at: 2020-04-16 14:32:34
# Size of source mod 2**32: 10588 bytes
from __future__ import absolute_import, division, unicode_literals
from . import base

class Filter(base.Filter):
    __doc__ = 'Removes optional tags from the token stream'

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

    def __iter__(self):
        for previous, token, next in self.slider():
            type = token['type']
            if type == 'StartTag' and not token['data'] or self.is_optional_start(token['name'], previous, next):
                yield token
            elif type == 'EndTag':
                if not self.is_optional_end(token['name'], next):
                    yield token
            else:
                yield token

    def is_optional_start(self, tagname, previous, next):
        type = next and next['type'] or None
        if tagname in 'html':
            return type not in ('Comment', 'SpaceCharacters')
            if tagname == 'head':
                if type in ('StartTag', 'EmptyTag'):
                    return True
                if type == 'EndTag':
                    return next['name'] == 'head'
        elif tagname == 'body':
            if type in ('Comment', 'SpaceCharacters'):
                return False
            if type == 'StartTag':
                return next['name'] not in ('script', 'style')
            return True
        else:
            if tagname == 'colgroup':
                if type in ('StartTag', 'EmptyTag'):
                    return next['name'] == 'col'
                return False
            else:
                if tagname == 'tbody':
                    if type == 'StartTag':
                        if previous:
                            if previous['type'] == 'EndTag':
                                if previous['name'] in ('tbody', 'thead', 'tfoot'):
                                    return False
                        return next['name'] == 'tr'
                    return False
        return False

    def is_optional_end(self, tagname, next):
        type = next and next['type'] or None
        if tagname in ('html', 'head', 'body'):
            return type not in ('Comment', 'SpaceCharacters')
        if tagname in ('li', 'optgroup', 'tr'):
            if type == 'StartTag':
                return next['name'] == tagname
            return type == 'EndTag' or type is None
        else:
            if tagname in ('dt', 'dd'):
                if type == 'StartTag':
                    return next['name'] in ('dt', 'dd')
                if tagname == 'dd':
                    return type == 'EndTag' or type is None
                return False
            else:
                if tagname == 'p':
                    if type in ('StartTag', 'EmptyTag'):
                        return next['name'] in ('address', 'article', 'aside', 'blockquote',
                                                'datagrid', 'dialog', 'dir', 'div',
                                                'dl', 'fieldset', 'footer', 'form',
                                                'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
                                                'header', 'hr', 'menu', 'nav', 'ol',
                                                'p', 'pre', 'section', 'table', 'ul')
                    return type == 'EndTag' or type is None
                else:
                    if tagname == 'option':
                        if type == 'StartTag':
                            return next['name'] in ('option', 'optgroup')
                        return type == 'EndTag' or type is None
                    else:
                        if tagname in ('rt', 'rp'):
                            if type == 'StartTag':
                                return next['name'] in ('rt', 'rp')
                            return type == 'EndTag' or type is None
                        else:
                            if tagname == 'colgroup':
                                if type in ('Comment', 'SpaceCharacters'):
                                    return False
                                if type == 'StartTag':
                                    return next['name'] != 'colgroup'
                                return True
                            else:
                                if tagname in ('thead', 'tbody'):
                                    if type == 'StartTag':
                                        return next['name'] in ('tbody', 'tfoot')
                                    if tagname == 'tbody':
                                        return type == 'EndTag' or type is None
                                    return False
                                else:
                                    if tagname == 'tfoot':
                                        if type == 'StartTag':
                                            return next['name'] == 'tbody'
                                        return type == 'EndTag' or type is None
                                    else:
                                        if tagname in ('td', 'th'):
                                            if type == 'StartTag':
                                                return next['name'] in ('td', 'th')
                                            return type == 'EndTag' or type is None
                                        return False