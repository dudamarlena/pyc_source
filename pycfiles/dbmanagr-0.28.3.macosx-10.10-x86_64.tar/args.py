# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/dbmanagr/command/navigator/args.py
# Compiled at: 2015-10-11 07:17:06
from dbmanagr.args import parent_parser, format_group, create_parser
from dbmanagr.writer import TestWriter
from .writer import SimplifiedWriter, SimpleWriter, JsonWriter
from .writer import AutocompleteWriter
parent = parent_parser(daemonable=True)
group = format_group(parent, TestWriter)
group.add_argument('-D', '--default', help='output format: default', dest='formatter', action='store_const', const=SimplifiedWriter)
group.add_argument('-S', '--simple', help='output format: simple', dest='formatter', action='store_const', const=SimpleWriter)
group.add_argument('-J', '--json', help='output format: JSON', dest='formatter', action='store_const', const=JsonWriter)
group.add_argument('-A', '--autocomplete', help='output format: autocomplete', dest='formatter', action='store_const', const=AutocompleteWriter)
parser = create_parser(prog='dbmanagr', description='A database navigation tool that shows database structure and content', parents=[
 parent])
parser.add_argument('uri', help='the URI to parse (format for PostgreSQL/MySQL: user@host/database/table?filter; for SQLite: databasefile.db/table?filter)', nargs='?')
parser.add_argument('-s', '--simplify', dest='simplify', default=True, help='simplify the output', action='store_true')
parser.add_argument('-N', '--no-simplify', dest='simplify', help="don't simplify the output", action='store_false')
parser.add_argument('-m', '--limit', type=int, default=50, help='limit the results of the main query to this amount of rows (default: %(default)s)')