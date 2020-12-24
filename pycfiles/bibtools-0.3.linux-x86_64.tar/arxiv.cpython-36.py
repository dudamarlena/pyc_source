# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /a/lib/python3.6/site-packages/bibtools/arxiv.py
# Compiled at: 2017-03-31 14:59:36
# Size of source mod 2**32: 1898 bytes
"""
Things having to do with arxiv.org.
"""
from __future__ import absolute_import, division, print_function, unicode_literals
import xml.etree.ElementTree as ET
from . import webutil as wu
from .bibcore import doi_to_maybe_bibcode
__all__ = 'autolearn_arxiv'.split()
_atom_ns = '{http://www.w3.org/2005/Atom}'
_arxiv_ns = '{http://arxiv.org/schemas/atom}'

def _translate_arxiv_name(auth):
    return auth.find(_atom_ns + 'name').text


def autolearn_arxiv(app, arxiv):
    url = 'http://export.arxiv.org/api/query?id_list=' + wu.urlquote(arxiv)
    info = {'arxiv':arxiv,  'keep':0}
    print('[Parsing', url, '...]')
    xmldoc = (b'').join(wu.urlopen(url))
    root = ET.fromstring(xmldoc)
    ent = root.find(_atom_ns + 'entry')
    try:
        info['abstract'] = ent.find(_atom_ns + 'summary').text
    except:
        pass

    try:
        info['authors'] = [_translate_arxiv_name(a) for a in ent.findall(_atom_ns + 'author')]
    except:
        pass

    try:
        info['doi'] = ent.find(_arxiv_ns + 'doi').text
    except:
        pass

    try:
        info['title'] = ent.find(_atom_ns + 'title').text
    except:
        pass

    try:
        info['year'] = int(ent.find(_atom_ns + 'published').text[:4])
    except:
        pass

    if 'doi' in info:
        info['bibcode'] = doi_to_maybe_bibcode(app, info['doi'])
    return info