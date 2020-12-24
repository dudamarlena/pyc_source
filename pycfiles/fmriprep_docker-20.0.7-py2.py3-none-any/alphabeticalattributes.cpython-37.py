# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-aejasjrz/pip/pip/_vendor/html5lib/filters/alphabeticalattributes.py
# Compiled at: 2020-05-05 12:41:47
# Size of source mod 2**32: 919 bytes
from __future__ import absolute_import, division, unicode_literals
from . import base
from collections import OrderedDict

def _attr_key(attr):
    """Return an appropriate key for an attribute for sorting

    Attributes have a namespace that can be either ``None`` or a string. We
    can't compare the two because they're different types, so we convert
    ``None`` to an empty string first.

    """
    return (
     attr[0][0] or '', attr[0][1])


class Filter(base.Filter):
    __doc__ = 'Alphabetizes attributes for elements'

    def __iter__(self):
        for token in base.Filter.__iter__(self):
            if token['type'] in ('StartTag', 'EmptyTag'):
                attrs = OrderedDict()
                for name, value in sorted((token['data'].items()), key=_attr_key):
                    attrs[name] = value

                token['data'] = attrs
            yield token