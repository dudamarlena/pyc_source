# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /a/lib/python3.6/site-packages/bibtools/crossref.py
# Compiled at: 2017-03-31 15:02:39
# Size of source mod 2**32: 2756 bytes
"""
Things related to the CrossRef/DOI/OpenURL system.
"""
from __future__ import absolute_import, division, print_function, unicode_literals
import xml.etree.ElementTree as ET
from .util import die
from . import webutil as wu
__all__ = 'autolearn_doi stream_doi'.split()

def _translate_unixref_name(personelem):
    given = personelem.find('given_name').text
    sur = personelem.find('surname').text
    return given + ' ' + sur.replace(' ', '_')


def stream_doi(app, doi):
    """Returns tuple of URL string and a urlopen() return value."""
    apikey = app.cfg.get_or_die('api-keys', 'crossref')
    url = 'http://crossref.org/openurl/?id=%s&noredirect=true&pid=%s&format=unixref' % (
     wu.urlquote(doi), wu.urlquote(apikey))
    return (url, wu.urlopen(url))


def autolearn_doi(app, doi):
    url, handle = stream_doi(app, doi)
    print('[Parsing', url, '...]')
    root = ET.fromstring((b'').join(handle))
    infotop = root.find('doi_record/crossref/journal')
    if infotop is not None:
        authpath = 'journal_article/contributors/person_name'
        titlepath = 'journal_article/titles/title'
        yearpath = 'journal_issue/publication_date/year'
    if infotop is None:
        infotop = root.find('doi_record/crossref/conference/conference_paper')
        if infotop is not None:
            authpath = 'contributors/person_name'
            titlepath = 'titles/title'
            yearpath = 'publication_date/year'
    if infotop is None:
        die("don't know how to interpret UnixRef XML for %s", doi)
    info = {'doi':doi, 
     'keep':0}
    try:
        info['authors'] = [_translate_unixref_name(p) for p in infotop.findall(authpath)]
    except:
        pass

    try:
        info['title'] = ' '.join(t.strip() for t in infotop.find(titlepath).itertext())
    except:
        pass

    try:
        info['year'] = int(infotop.find(yearpath).text)
    except:
        pass

    return info