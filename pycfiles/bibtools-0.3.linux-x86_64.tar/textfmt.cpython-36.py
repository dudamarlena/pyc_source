# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /a/lib/python3.6/site-packages/bibtools/textfmt.py
# Compiled at: 2017-03-31 15:23:24
# Size of source mod 2**32: 5150 bytes
"""
Import/export from our text format.
"""
from __future__ import absolute_import, division, print_function, unicode_literals
from six import text_type
import json
from .util import *
from .bibcore import *
__all__ = 'export_one import_one'.split()

def export_one(app, pub, stream, width):
    write = stream.write
    if pub.title is None:
        write('--no title--\n')
    else:
        print_linewrapped((pub.title), width=width, stream=stream)
    if pub.year is None:
        write('--no year--\n')
    else:
        write(text_type(pub.year))
        write('\n')
    write('\n')
    write('arxiv = ')
    write(pub.arxiv or '')
    write('\n')
    write('bibcode = ')
    write(pub.bibcode or '')
    write('\n')
    write('doi = ')
    write(pub.doi or '')
    write('\n')
    for nick, in app.db.execute('SELECT nickname FROM nicknames WHERE pubid == ? ORDER BY nickname asc', (
     pub.id,)):
        write('nick = ')
        write(nick)
        write('\n')

    write('\n')
    anyauth = False
    for given, family in app.db.get_pub_authors(pub.id, 'author'):
        write(encode_name(given, family))
        write('\n')
        anyauth = True

    if not anyauth:
        write('--no authors--\n')
    else:
        firsteditor = True
        for given, family in app.db.get_pub_authors(pub.id, 'editor'):
            if firsteditor:
                write('--editors--\n')
                firsteditor = False
            write(encode_name(given, family))
            write('\n')

        write('\n')
        if pub.refdata is None:
            write('--no reference data--\n')
        else:
            rd = json.loads(pub.refdata)
            btype = rd.pop('_type')
            write('@')
            write(btype)
            write('\n')
            for k in sorted(rd.keys()):
                write(k)
                write(' = ')
                write(rd[k])
                write('\n')

        write('\n')
        if pub.abstract is None:
            write('--no abstract--\n')
        else:
            print_linewrapped((pub.abstract), width=width, stream=stream, maxwidth=72)
    write('\n')


def _import_get_chunk(stream, gotoend=False):
    lines = []
    for line in stream:
        line = line.strip()
        if not len(line):
            if not gotoend:
                return lines
        lines.append(line)

    while len(lines) and not len(lines[(-1)]):
        lines = lines[:-1]

    return lines


def import_one(stream):
    info = {}
    c = _import_get_chunk(stream)
    if len(c) < 2:
        die('title/year chunk must contain at least two lines')
    info['title'] = squish_spaces(' '.join(c[:-1]))
    if info['title'].startswith('--'):
        del info['title']
    if not c[(-1)].startswith('--'):
        try:
            info['year'] = int(c[(-1)])
        except Exception as e:
            die('publication year must be an integer or "--no year--"; got "%s"', c[(-1)])

    c = _import_get_chunk(stream)
    info['nicknames'] = []
    for line in c:
        if '=' not in line:
            die('identifier lines must contain "=" signs; got "%s"', line)
        k, v = line.split('=', 1)
        k = k.strip()
        v = v.strip()
        if not v:
            continue
        if k == 'arxiv':
            info['arxiv'] = v
        elif k == 'bibcode':
            info['bibcode'] = v
        else:
            if k == 'doi':
                info['doi'] = v
            else:
                if k == 'nick':
                    info['nicknames'].append(v)
                else:
                    die('unexpected identifier kind "%s"', k)

    c = _import_get_chunk(stream)
    namelist = info['authors'] = []
    for line in c:
        if line == '--no authors--':
            pass
        else:
            if line == '--editors--':
                namelist = info['editors'] = []
            else:
                namelist.append(line)

    c = _import_get_chunk(stream)
    if not c[0].startswith('--'):
        rd = info['refdata'] = {}
        if c[0][0] != '@':
            die('reference data chunk must begin with an "@"; got "%s"', c[0])
        rd['_type'] = c[0][1:]
        for line in c[1:]:
            if '=' not in line:
                die('ref data lines must contain "=" signs; got "%s"', line)
            k, v = line.split('=', 1)
            k = k.strip()
            v = v.strip()
            rd[k] = v

    c = _import_get_chunk(stream, gotoend=True)
    abs = ''
    spacer = ''
    for line in c:
        if not len(line):
            spacer = '\n'
        else:
            if line == '--no abstract--':
                pass
            else:
                abs += spacer + line
                spacer = ' '

    if len(abs):
        info['abstract'] = abs
    return info