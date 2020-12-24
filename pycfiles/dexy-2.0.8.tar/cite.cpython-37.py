# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ana/dev/dexy-clean/dexy/commands/cite.py
# Compiled at: 2020-03-18 15:12:33
# Size of source mod 2**32: 1004 bytes
from dexy.version import DEXY_VERSION
import datetime
citation_formats = ['bibtex']

def build_cite_parser(parser):
    parser.set_defaults(cmd=cite_command)
    parser.add_argument('-f', '--fmt', default=(citation_formats[0]), help='Desired format of citation.')


def cite_command(args):
    fmt = args.fmt
    if fmt == 'bibtex':
        cite_bibtex()
    else:
        msg = f"Don't know how to provide citation in '%{fmt}' format"
        print(msg)


def bibtex_text():
    args = {'version':DEXY_VERSION, 
     'year':datetime.date.today().year}
    return '@misc{Dexy,\n    title = {Dexy: Reproducible Data Analysis and Document Automation Software, Version~%(version)s},\n    author = {{Nelson, Ana}},\n    year = {%(year)s},\n    url = {http://www.dexy.it/},\n    note = {http://orcid.org/0000-0003-2561-1564}\n}' % args


def cite_bibtex():
    print(bibtex_text())