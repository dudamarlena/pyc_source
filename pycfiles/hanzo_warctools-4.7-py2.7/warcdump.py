# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/hanzo/warcdump.py
# Compiled at: 2013-01-14 05:25:26
"""warcdump - dump warcs in a slightly more humane format"""
import os, sys, sys, os.path
from optparse import OptionParser
from .warctools import WarcRecord, expand_files
parser = OptionParser(usage='%prog [options] warc warc warc')
parser.add_option('-l', '--limit', dest='limit')
parser.add_option('-I', '--input', dest='input_format')
parser.add_option('-L', '--log-level', dest='log_level')
parser.set_defaults(output_directory=None, limit=None, log_level='info')

def main(argv):
    options, input_files = parser.parse_args(args=argv[1:])
    out = sys.stdout
    if len(input_files) < 1:
        dump_archive(WarcRecord.open_archive(file_handle=sys.stdin, gzip=None), name='-', offsets=False)
    else:
        for name in expand_files(input_files):
            fh = WarcRecord.open_archive(name, gzip='auto')
            dump_archive(fh, name)
            fh.close()

    return 0


def dump_archive(fh, name, offsets=True):
    for offset, record, errors in fh.read_records(limit=None, offsets=offsets):
        if record:
            print 'archive record at %s:%s' % (name, offset)
            record.dump(content=True)
        elif errors:
            print 'warc errors at %s:%d' % (name, offset if offset else 0)
            for e in errors:
                print '\t', e

        else:
            print
            print 'note: no errors encountered in tail of file'

    return


def run():
    sys.exit(main(sys.argv))


if __name__ == '__main__':
    run()