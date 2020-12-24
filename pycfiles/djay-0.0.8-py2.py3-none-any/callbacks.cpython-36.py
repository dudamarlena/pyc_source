# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-m_4qh6p6/bleach/bleach/callbacks.py
# Compiled at: 2019-07-30 18:47:12
# Size of source mod 2**32: 804 bytes
"""A set of basic callbacks for bleach.linkify."""
from __future__ import unicode_literals

def nofollow(attrs, new=False):
    href_key = (None, 'href')
    if href_key not in attrs:
        return attrs
    if attrs[href_key].startswith('mailto:'):
        return attrs
    else:
        rel_key = (None, 'rel')
        rel_values = [val for val in attrs.get(rel_key, '').split(' ') if val]
        if 'nofollow' not in [rel_val.lower() for rel_val in rel_values]:
            rel_values.append('nofollow')
        attrs[rel_key] = ' '.join(rel_values)
        return attrs


def target_blank(attrs, new=False):
    href_key = (None, 'href')
    if href_key not in attrs:
        return attrs
    else:
        if attrs[href_key].startswith('mailto:'):
            return attrs
        attrs[(None, 'target')] = '_blank'
        return attrs