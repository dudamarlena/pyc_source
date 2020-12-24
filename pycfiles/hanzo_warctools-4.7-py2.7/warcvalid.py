# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/hanzo/warcvalid.py
# Compiled at: 2013-01-14 05:25:26
"""warcvalid - check a warc is ok"""
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
        parser.error('no imput warc file(s)')
    correct = True
    fh = None
    try:
        try:
            for name in expand_files(input_files):
                fh = WarcRecord.open_archive(name, gzip='auto')
                for offset, record, errors in fh.read_records(limit=None):
                    if errors:
                        print >> sys.stderr, 'warc errors at %s:%d' % (name, offset)
                        print >> sys.stderr, errors
                        correct = False
                        break
                    elif record is not None and record.validate():
                        print >> sys.stderr, 'warc errors at %s:%d' % (name, offset)
                        print >> sys.stderr, record.validate()
                        correct = False
                        break

        except StandardError as e:
            correct = False

    finally:
        if fh:
            fh.close()

    if correct:
        return 0
    else:
        return -1
        return


def run():
    sys.exit(main(sys.argv))


if __name__ == '__main__':
    run()