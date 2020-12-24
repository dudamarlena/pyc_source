# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /a/lib/python3.6/site-packages/bibtools/bibtex.py
# Compiled at: 2017-07-26 12:12:04
# Size of source mod 2**32: 14135 bytes
"""
BibTeX-related stuff.

TODO: styles defined in a support file or something.

"""
from __future__ import absolute_import, division, print_function, unicode_literals
import json
from six import text_type
from .util import *
from . import webutil as wu
from .bibcore import *
from .unicode_to_latex import unicode_to_latex
__all__ = str('\nimport_stream\nbibtexify_one\nget_style_or_die\nexport_to_bibtex\nwrite_bibtexified\n').split()
_bibtex_replacements = ('\\&ap;', '~', '\\&#177;', '±', '\\&gt;~', '⪞', '\\&lt;~',
                        '⪝', '{', '', '}', '', '<SUP>', '^', '</SUP>', '', '<SUB>',
                        '_', '</SUB>', '', 'Delta', 'Δ', 'Omega', 'Ω', '( ', '(',
                        ' )', ')', '[ ', '[', ' ]', ']', ' ,', ',', ' .', '.', ' ;',
                        ';', '\t', ' ', '  ', ' ')

def _fix_bibtex(text):
    """Ugggghhh. So many problems."""
    if text is None:
        return
    else:
        text = text_type(text)
        for i in range(0, len(_bibtex_replacements), 2):
            text = text.replace(_bibtex_replacements[i], _bibtex_replacements[(i + 1)])

        return text


def _translate_bibtex_name(name):
    a = [i.strip() for i in name.split(',')]
    if len(a) == 0:
        warn('all last name, I think: %s', name)
        return a.replace(' ', '_')
    else:
        first = a[(-1)]
        surname = ',_'.join(a[:-1]).replace(' ', '_')
        if not len(first):
            warn('CiteULike mis-parsed name, I think: %s', name)
        return first + ' ' + surname


def _convert_bibtex_record(rec):
    abstract = rec.get('abstract')
    arxiv = rec.get('eprint')
    bibcode = rec.get('bibcode')
    doi = rec.get('doi')
    nickname = rec.get('id')
    title = rec.get('title')
    year = rec.get('year')
    if year is not None:
        year = int(year)
    else:
        if 'author' in rec:
            authors = [_translate_bibtex_name(_fix_bibtex(a)) for a in rec['author']]
        else:
            authors = None
        if 'editor' in rec:
            editors = [_translate_bibtex_name(_fix_bibtex(e['name'])) for e in rec['editor']]
        else:
            editors = None
    abstract = _fix_bibtex(abstract)
    title = _fix_bibtex(title)
    urlinfo = []
    if 'url' in rec:
        urlinfo.append(sniff_url(rec['url']))
    if 'adsurl' in rec:
        urlinfo.append(sniff_url(rec['adsurl']))
    for k, v in rec.items():
        if k.startswith('citeulike-linkout-'):
            urlinfo.append(sniff_url(v))
        if k.startswith('bdsk-url-'):
            urlinfo.append(sniff_url(v))

    for kind, info in urlinfo:
        if kind is None:
            pass
        else:
            if kind == 'bibcode':
                if bibcode is None:
                    bibcode = info
                if kind == 'doi':
                    if doi is None:
                        doi = info
                if kind == 'arxiv' and arxiv is None:
                    arxiv = info

    refdata = {'_type': rec['type']}
    for k, v in rec.items():
        if k in ('type', 'id', 'abstract', 'archiveprefix', 'author', 'bibcode', 'day',
                 'doi', 'editor', 'eprint', 'keyword', 'keywords', 'link', 'month',
                 'posted-at', 'pmid', 'priority', 'title', 'url', 'year'):
            pass
        else:
            if k.startswith('citeulike'):
                pass
            else:
                refdata[k] = v

    return dict(abstract=abstract, arxiv=arxiv, authors=authors, bibcode=bibcode,
      doi=doi,
      editors=editors,
      nicknames=[
     nickname],
      refdata=refdata,
      title=title,
      year=year)


def _convert_bibtex_stream(bibstream):
    from .hacked_bibtexparser.bparser import BibTexParser
    from .hacked_bibtexparser.customization import author, editor, type, convert_to_unicode
    custom = lambda r: editor(author(type(convert_to_unicode(r))))
    bp = BibTexParser(bibstream, customization=custom)
    for rec in bp.get_entry_list():
        yield _convert_bibtex_record(rec)


def import_stream(app, bibstream):
    for info in _convert_bibtex_stream(bibstream):
        app.db.learn_pub(info)


class BibtexStyleBase(object):
    include_doi = True
    include_title_all = False
    issn_name_map = None
    normalize_pages = False
    aggressive_url = True
    title_types = set((b'book', ))

    def render_name(self, name):
        given, family = parse_name(name)
        if len(given):
            givenbit = b', ' + unicode_to_latex(given)
        else:
            givenbit = b''
        fbits = family.rsplit(',', 1)
        if len(fbits) > 1:
            return b'{%s}, %s%s' % (unicode_to_latex(fbits[0]),
             unicode_to_latex(fbits[1]),
             givenbit)
        else:
            return b'{%s}%s' % (unicode_to_latex(fbits[0]), givenbit)

    def render_names(self, names):
        return (b' and ').join(self.render_name(n) for n in names)

    def _massage_info(self, info, rd):
        pass

    def render_info(self, info):
        """Returns a dict in which the values are already latex-encoded. '_type' is
        the bibtex type, '_ident' is the bibtex identifier.

        We process an 'info' dictionary so that we can process BibTeX records that
        haven't actually been ingested into the database.

        """
        rd = dict(info['refdata'])
        for k in list(rd.keys()):
            rd[k] = unicode_to_latex(rd[k])

        self._massage_info(info, rd)
        if len(info.get('authors') or []):
            rd['author'] = self.render_names(info['authors'])
        if len(info.get('editors') or []):
            rd['editor'] = self.render_names(info['editors'])
        if self.include_doi:
            if info.get('doi') is not None:
                rd['doi'] = unicode_to_latex(info['doi'])
        if self.issn_name_map is not None:
            if 'issn' in rd:
                ltxjname = self.issn_name_map.get(rd['issn'].decode('utf8'))
                if ltxjname is not None:
                    rd['journal'] = ltxjname
        if self.normalize_pages and 'pages' in rd:
            p = rd['pages'].split(b'--')[0]
            if p[(-1)] == b'+':
                p = p[:-1]
            rd['pages'] = p
        if self.include_title_all or rd['_type'] in self.title_types:
            if info.get('title') is not None:
                rd['title'] = unicode_to_latex(info['title'])
        if info.get('year') is not None:
            rd['year'] = b'%d' % info['year']
        if self.aggressive_url:
            if info.get('doi') is not None:
                rd['url'] = unicode_to_latex('http://dx.doi.org/' + wu.urlquote(info['doi']))
            else:
                if info.get('bibcode') is not None:
                    rd['url'] = unicode_to_latex('http://adsabs.harvard.edu/abs/' + wu.urlquote(info['bibcode']))
                elif info.get('arxiv') is not None:
                    rd['url'] = unicode_to_latex('http://arxiv.org/abs/' + info['arxiv'])
        url = rd.get('url')
        if url is not None:
            if b' ' in url:
                warn('spaces in output url "%s"', url)
                url = url.replace(b' ', b'\\%20')
            url = url.replace(b'{}', b' ')
            rd['url'] = url
        return rd


class ApjBibtexStyle(BibtexStyleBase):
    normalize_pages = True

    def __init__(self):
        inm = {}
        for line in datastream('apj-issnmap.txt'):
            line = line.split(b'#')[0].strip().decode('utf-8')
            if not len(line):
                continue
            issn, jname = line.split(None, 1)
            inm[issn] = unicode_to_latex(jname)

        self.issn_name_map = inm

    def _massage_info(self, info, rd):
        if rd.get('issn') == '1996-756X':
            rd['_type'] = 'article'
        if rd.get('_type') == '!arxiv':
            rd['_type'] = 'article'
            rd['journal'] = rd['note']
            del rd['note']
            rd['eprint'] = info['arxiv']
            rd['archivePrefix'] = 'arxiv'
        elif rd.get('_type') == '!preprint':
            rd['_type'] = 'article'
            rd['journal'] = rd['note']
            del rd['note']


class NsfBibtexStyle(BibtexStyleBase):
    normalize_pages = True
    include_title_all = True

    def _massage_info(self, info, rd):
        if rd.get('_type') == '!arxiv':
            rd['_type'] = 'article'
            rd['journal'] = rd['note']
            del rd['note']
            rd['eprint'] = info['arxiv']
            rd['archivePrefix'] = 'arxiv'
        elif rd.get('_type') == '!preprint':
            rd['_type'] = 'article'
            rd['journal'] = rd['note']
            del rd['note']


bibtex_styles = {'apj':ApjBibtexStyle, 
 'nsf':NsfBibtexStyle}

def get_style_or_die(name):
    factory = bibtex_styles.get(name)
    if factory is None:
        die('unrecognized BibTeX output style "%s"', name)
    return factory()


def write_bibtexified(write, btdata):
    """This will mutate `btdata`."""
    bttype = btdata.pop('_type')
    btid = btdata.pop('_ident')
    write(b'@')
    write(bttype)
    write(b'{')
    write(btid)
    for k in sorted(btdata.keys()):
        if btdata[k] is None:
            warn('expected to see BibTeX field "%s" in "%s", but it is empty', k, btid)
        else:
            write(b',\n  ')
            write(k.encode('utf8'))
            write(b' = {')
            write(btdata[k])
            write(b'}')

    write(b'\n}\n')


def export_to_bibtex(app, style, citednicks, write=None, ignore_missing=False):
    if write is None:
        from pwkit.io import get_stdout_bytes
        write = get_stdout_bytes().write
    seenids = {}
    first = True
    for nick in sorted(citednicks):
        curs = app.db.pub_fquery('SELECT p.* FROM pubs AS p, nicknames AS n WHERE p.id == n.pubid AND n.nickname == ?', nick)
        res = list(curs)
        if not len(res):
            if ignore_missing:
                continue
            else:
                die('citation to unrecognized nickname "%s"', nick)
        if len(res) != 1:
            die('cant-happen multiple matches for nickname "%s"', nick)
        pub = res[0]
        if pub.id in seenids:
            die('"%s" and "%s" refer to the same publication; this will cause duplicate entries', nick, seenids[pub.id])
        if pub.refdata is None:
            die('no reference data for "%s"', nick)
        seenids[pub.id] = nick
        if first:
            first = False
        else:
            write(b'\n')
        bt = style.render_info(app.db.jsonify_pub(pub.id))
        bt['_ident'] = nick.encode('utf8')
        write_bibtexified(write, bt)


def merge_with_bibtex(app, bibpath, style, citednicks, write=None):
    if write is None:
        from pwkit.io import get_stdout_bytes
        write = get_stdout_bytes().write
    existing = {}
    with open(bibpath, 'r') as (f):
        for info in _convert_bibtex_stream(f):
            existing[info['nicknames'][0]] = info

    seenids = {}
    recognized = {}
    first = True
    sorted_cited = sorted(citednicks)
    for nick in sorted_cited:
        curs = app.db.pub_fquery('SELECT p.* FROM pubs AS p, nicknames AS n WHERE p.id == n.pubid AND n.nickname == ?', nick)
        res = list(curs)
        if not len(res):
            continue
        if len(res) != 1:
            die('cant-happen multiple matches for nickname "%s"', nick)
        pub = res[0]
        if pub.id in seenids:
            die('"%s" and "%s" refer to the same publication; this will cause duplicate entries', nick, seenids[pub.id])
        if pub.refdata is None:
            die('no reference data for "%s"', nick)
        seenids[pub.id] = nick
        recognized[nick] = pub.id

    for nick in sorted_cited:
        if nick in recognized:
            info = app.db.jsonify_pub(recognized[nick])
        else:
            info = existing.get(nick)
        if info is None:
            warn('skipping "%s"', nick)
        else:
            if first:
                first = False
            else:
                write('\n')
            bt = style.render_info(info)
            bt['_ident'] = nick.encode('utf8')
            write_bibtexified(write, bt)