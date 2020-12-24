# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/simpleavro/__main__.py
# Compiled at: 2011-05-29 11:27:36
from .commands import read, count
import json, csv
from sys import stdout
import re
from itertools import ifilter
from functools import partial

def do_count(avro, args):
    print count(avro)


def show_json(row):
    print json.dumps(row)


_write_row = csv.writer(stdout).writerow

def show_csv(row):
    _write_row([ row[key] for key in sorted(row) ])


def compile_filter_expr(expr):
    """"$age > 10" -> "__record['age'] > 10\""""
    return re.sub('\\$(\\w+)', "__record['\\1']", expr)


def record_match(expr, record):
    return eval(expr, None, {'__record': record})


def do_print(avro, args):
    if args.header and args.format != 'csv':
        raise ValueError('--header applies only to CSV format')
    avro = read(avro)
    if args.filter:
        expr = compile_filter_expr(args.filter)
        avro = ifilter(partial(record_match, expr), avro)
    for i in xrange(args.skip):
        try:
            next(avro)
        except StopIteration:
            return

    show = show_csv if args.format == 'csv' else show_json
    for i, record in enumerate(avro):
        if i == 0 and args.header:
            _write_row(sorted(record.keys()))
        if i >= args.count:
            break
        show(record)


def do_schema(avro, args):
    schema = str(read(avro).schema)
    print json.dumps(json.loads(schema), indent=4)


def main(argv=None):
    import sys
    from argparse import ArgumentParser
    argv = argv or sys.argv
    parser = ArgumentParser(description='Avro file tool box', prog='simpleavro')
    subparsers = parser.add_subparsers()
    pc = subparsers.add_parser('count', description='Print number of records')
    pc.add_argument('filename', help='avro file (- for stdin)')
    pc.set_defaults(func=do_count)
    pp = subparsers.add_parser('print', description='Print records')
    pp.add_argument('filename', help='avro file (- for stdin)')
    pp.add_argument('-n', '--count', default=float('Infinity'), help='number of records to print', type=int)
    pp.add_argument('-s', '--skip', help='number of records to skip', type=int, default=0)
    pp.add_argument('-f', '--format', help='record format', default='json', choices=[
     'json', 'csv'])
    pp.add_argument('--header', help='print CSV header', default=False, action='store_true')
    pp.add_argument('--filter', help='filter records (e.g. $age>1)', default=None)
    pp.set_defaults(func=do_print)
    ps = subparsers.add_parser('schema', description='Print schema')
    ps.add_argument('filename', help='avro file (- for stdin)')
    ps.set_defaults(func=do_schema)
    args = parser.parse_args(argv[1:])
    avro = sys.stdin if args.filename == '-' else args.filename
    try:
        args.func(avro, args)
    except Exception as e:
        raise SystemExit('error: %s' % e)

    return


if __name__ == '__main__':
    main()