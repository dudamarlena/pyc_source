# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /a/lib/python3.6/site-packages/bibtools/ads.py
# Compiled at: 2017-03-31 14:58:29
# Size of source mod 2**32: 6059 bytes
"""
Tools relating to working with NASA's ADS.
"""
from __future__ import absolute_import, division, print_function, unicode_literals
import json
from .util import *
from . import webutil as wu
from .bibcore import *
__all__ = 'autolearn_bibcode search_ads'.split()

def _translate_ads_name(name):
    pieces = [x.strip() for x in name.split(',', 1)]
    surname = pieces[0].replace(' ', '_')
    if len(pieces) > 1:
        return pieces[1] + ' ' + surname
    else:
        return surname


def _autolearn_bibcode_tag(info, tag, text):
    if tag == 'T':
        info['title'] = text
    else:
        if tag == 'D':
            info['year'] = int(text.split('/')[(-1)])
        else:
            if tag == 'B':
                info['abstract'] = text
            else:
                if tag == 'A':
                    info['authors'] = [_translate_ads_name(n) for n in text.split(';')]
                elif tag == 'Y':
                    subdata = dict(s.strip().split(': ', 1) for s in text.split(';'))
                    if 'DOI' in subdata:
                        info['doi'] = subdata['DOI']
                    if 'eprintid' in subdata:
                        value = subdata['eprintid']
                        if value.startswith('arXiv:'):
                            info['arxiv'] = value[6:]


def autolearn_bibcode(app, bibcode):
    url = 'http://adsabs.harvard.edu/cgi-bin/nph-abs_connect?data_type=PORTABLE&nocookieset=1&bibcode=' + wu.urlquote(bibcode)
    info = {'bibcode':bibcode, 
     'keep':0}
    curtag = curtext = None
    print('[Parsing', url, '...]')
    for line in wu.urlopen(url):
        line = line.decode('iso-8859-1').strip()
        if not len(line):
            if curtag is not None:
                _autolearn_bibcode_tag(info, curtag, curtext)
                curtag = curtext = None
                continue
                if curtag is None:
                    if line[0] == '%':
                        curtag = line[1]
                        curtext = line[3:]
                    elif line.startswith('Retrieved '):
                        line.endswith('selected: 1.') or die('matched more than one publication')
                else:
                    if line[0] == '%':
                        _autolearn_bibcode_tag(info, curtag, curtext)
                        curtag = line[1]
                        curtext = line[3:]
                    else:
                        curtext += ' ' + line

    if curtag is not None:
        _autolearn_bibcode_tag(info, curtag, curtext)
    return info


def _run_ads_search(app, searchterms, filterterms, nrows=50):
    apikey = app.cfg.get_or_die('api-keys', 'ads')
    q = [
     (
      'q', ' '.join(searchterms))]
    for ft in filterterms:
        q.append(('fq', ft))

    q.append(('fl', 'author,bibcode,title'))
    q.append(('rows', nrows))
    url = 'http://api.adsabs.harvard.edu/v1/search/query?' + wu.urlencode(q)
    opener = wu.build_opener()
    opener.addheaders = [('Authorization', 'Bearer:' + apikey)]
    return json.load(opener.open(url))


def search_ads(app, terms, raw=False, large=False):
    if len(terms) < 2:
        die('require at least two search terms for ADS')
    else:
        adsterms = []
        for info in terms:
            if info[0] == 'year':
                adsterms.append('year:%d' % info[1])
            else:
                if info[0] == 'surname':
                    adsterms.append('author:"%s"' % info[1])
                else:
                    if info[0] == 'refereed':
                        if info[1]:
                            adsterms.append('property:refereed')
                        else:
                            adsterms.append('property:notrefereed')
                    else:
                        die("don't know how to express search term %r to ADS", info)

        if large:
            nrows = 1000
        else:
            nrows = 50
        try:
            r = _run_ads_search(app, adsterms, ['database:astronomy'], nrows=nrows)
        except Exception as e:
            die('could not perform ADS search: %s', e)

        if raw:
            import sys
            json.dump(r, (sys.stdout), ensure_ascii=False, indent=2, separators=(',',
                                                                                 ': '))
            return
        query_row_limit = r.get('responseHeader', {}).get('params', {}).get('rows')
        if query_row_limit is not None:
            query_row_limit = int(query_row_limit)
        else:
            query_row_limit = 10
        maxbclen = 0
        info = []
        if large:
            ntrunc = 2147483647
        else:
            ntrunc = 20
        nresults = len(r['response']['docs'])
        for item in r['response']['docs'][:ntrunc]:
            if 'title' in item:
                title = item['title'][0]
            else:
                title = '(no title)'
            bibcode = item['bibcode']
            authors = ', '.join(parse_name(_translate_ads_name(n))[1] for n in item['author'])
            maxbclen = max(maxbclen, len(bibcode))
            info.append((bibcode, title, authors))

        ofs = maxbclen + 2
        red, reset = get_color_codes(None, 'red', 'reset')
        for bc, title, authors in info:
            print(('%s%*s%s  ' % (red, maxbclen, bc, reset)), end='')
            print_truncated(title, ofs, color='bold')
            print('    ', end='')
            print_truncated(authors, 4)

        if nresults >= ntrunc:
            print('')
            if nresults < query_row_limit:
                print('(showing %d of %d results)' % (ntrunc, nresults))
            else:
                print('(showing %d of at least %d results)' % (ntrunc, query_row_limit))