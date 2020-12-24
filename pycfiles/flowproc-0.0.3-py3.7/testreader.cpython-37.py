# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/flowproc/testreader.py
# Compiled at: 2019-07-10 06:00:27
# Size of source mod 2**32: 6756 bytes
"""
A helper program to read binary NetFlow V5, V9 and IPFIX export packets from
disk and feed these to collectors
"""
import argparse, logging, struct, sys
from datetime import datetime
import flowproc.netflow_v5 as Cv5
import flowproc.netflow_v9 as Cv9
from flowproc import __version__
unpack_hdr5 = Cv5.unpack_header
unpack_hdr9 = Cv9.unpack_header
__author__ = 'Tobias Frei'
__copyright__ = 'Tobias Frei'
__license__ = 'mit'
expected = None
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())

def feed_5(fp, stat=False, selection=None):
    """stat: print statistics only"""
    global expected
    C = Cv5('all')
    _read = 0
    start_date = None
    end_date = None
    packets = 0
    records = 0
    min_recs = 30
    max_recs = 0
    domains = set()
    seq_err = {}
    fmt = '!HHIIIIBBH'
    while True:
        bin_hdr = fp.read(24)
        if len(bin_hdr) < 24:
            break
        hdr = struct.unpack(fmt, bin_hdr)
        counter = hdr[1]
        data = fp.read(counter * 48)
        if selection:
            _read += 1
            if _read < selection[1]:
                continue
            if sum(selection) - 1 < _read:
                continue
        if not stat:
            C.collect('0.0.0.0', bin_hdr + data)
        else:
            records += counter
            packets += 1
            min_recs = min(counter, min_recs)
            max_recs = max(counter, max_recs)
            domains.add(hdr[7])
            if not start_date:
                start_date = hdr[3]
            if not end_date:
                end_date = hdr[3]
            if expected:
                if not hdr[5] == expected:
                    seq_err[packets] = {'actual':hdr[5], 
                     'expected':expected}
            expected = hdr[5] + counter

    if stat:
        sdt = datetime.fromtimestamp(start_date)
        edt = datetime.fromtimestamp(end_date)
        print('Start:     ', sdt)
        print('End:       ', edt)
        print('Observation domains:  ', domains)
        print('Packets: {} records: {}'.format(packets, records))
        print('avg records in packet:', round(records / packets, 1))
        print('min records in packet:', min_recs)
        print('max records in packet:', max_recs)
        print('Sequence errors:')
        for k, v in seq_err.items():
            print('{:6d} {}'.format(k, v))


def feed_9(fp):
    """This IS EXPERIMENTAL !!"""
    fmt = '!HHIIII'

    def _is_header(header):
        """Return True if this looks like a Netflow V9 header"""
        if header[0] == 9:
            if header[(-1)] in (0, 1, 2, 3, 4):
                return True
        return False

    def _find_header():
        WORD = 4
        pos = fp.tell()
        mod = pos % WORD
        if mod != 0:
            fp.read(WORD - mod)
        pos = fp.tell()
        while True:
            header = struct.unpack(fmt, fp.read(20))
            if _is_header(header):
                fp.seek(pos)
                return header
            fp.read(WORD)

    while 1:
        header = struct.unpack(fmt, fp.read(20))
        if not _is_header(header):
            header = _find_header()
        pos = fp.tell()
        print('{:5d} Found export packet header: {}'.format(pos, header))
        while True:
            pos = fp.tell()
            set_id, length = struct.unpack('!HH', fp.read(4))
            print('{:5d}   Flow Set id: {:3d} length: {:d}'.format(pos, set_id, length))
            try:
                fp.read(length - 4)
            except ValueError as e:
                try:
                    pos = fp.tell()
                    print('{:5d}   {} ...skipping'.format(pos, e))
                    _find_header()
                    break
                finally:
                    e = None
                    del e


def ipfeed(fp):
    print('10 notimpl')


def parse_args(args):
    """Parse command line parameters

    Args:
      args ([str]): command line parameters as list of strings

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    parser = argparse.ArgumentParser(description='A helper program to read binary NetFlow V5, V9 and\n        IPFIX export packets from disk and feed these to collectors',
      formatter_class=(argparse.ArgumentDefaultsHelpFormatter))
    parser.add_argument('-i', '--infile', required=True, metavar='path')
    parser.add_argument('-r',
      '--range',
      nargs=2,
      type=int,
      default=None,
      help='RANGE START_PACKET, when `None` read all')
    parser.add_argument('-s',
      '--summary',
      help='print file summary instead of calling collector',
      action='store_true')
    parser.add_argument('-V',
      '--version',
      help='print packet version and exit',
      action='version',
      version='flowproc {ver}'.format(ver=__version__))
    return parser.parse_args(args)


def main(args):
    """Main entry point allowing external calls

    Args:
      args ([str]): command line parameter list
    """
    args = parse_args(args)
    print('Args {}'.format(vars(args)))
    with open(args.infile, 'rb') as (fp):
        ver = struct.unpack('!H', fp.read(2))[0]
        if ver in (5, 9):
            print('{} looks like NetFlow V{}'.format(args.infile, ver))
        else:
            if ver == 10:
                print('{} looks like IPFIX'.format(args.infile))
            else:
                print('Fishy file format... ¯\\_(°.°)_/¯')
        fp.seek(0)
        if ver == 5:
            feed_5(fp, stat=(args.summary), selection=(args.range))
        else:
            if ver == 9:
                feed_9(fp)
            else:
                ipfeed(fp)


def run():
    """Entry point for console_scripts
    """
    main(sys.argv[1:])


if __name__ == '__main__':
    run()