# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/hanzo/warcextract.py
# Compiled at: 2013-01-14 05:25:26
"""warcextract - dump warc record context to standard out"""
import os, sys, sys, os.path
from optparse import OptionParser
from contextlib import closing
from .warctools import WarcRecord
parser = OptionParser(usage='%prog [options] warc offset')
parser.add_option('-I', '--input', dest='input_format')
parser.add_option('-L', '--log-level', dest='log_level')
parser.set_defaults(output_directory=None, limit=None, log_level='info')

def main(argv):
    options, args = parser.parse_args(args=argv[1:])
    out = sys.stdout
    if len(args) < 1:
        with closing(WarcRecord.open_archive(file_handle=sys.stdin, gzip=None)) as (fh):
            dump_record(fh)
    else:
        filename = args[0]
        if len(args) > 1:
            offset = int(args[1])
        else:
            offset = 0
        with closing(WarcRecord.open_archive(filename=filename, gzip='auto')) as (fh):
            fh.seek(offset)
            dump_record(fh)
    return 0


def dump_record(fh):
    for offset, record, errors in fh.read_records(limit=1, offsets=False):
        if record:
            sys.stdout.write(record.content[1])
        elif errors:
            print >> sys.stderr, 'warc errors at %s:%d' % (name, offset if offset else 0)
            for e in errors:
                print '\t', e

        break


def run():
    sys.exit(main(sys.argv))


if __name__ == '__main__':
    run()