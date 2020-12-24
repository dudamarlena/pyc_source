# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/instatrace/commands.py
# Compiled at: 2010-05-17 21:22:05
from ConfigParser import SafeConfigParser
import logging, os, sys, time
from .stats import Accumulator, Statistic
log = logging.getLogger('instatrace')

class ExtractCommand:

    @classmethod
    def add_subparser(cls, parser):
        subparser = parser.add_parser('extract', help='Extract instatrace data from program log files')
        subparser.add_argument('--filter', action='store_true', help="Filter out any lines that don't contain INSTATRACE")
        subparser.add_argument('file', nargs='+')
        subparser.set_defaults(run=cls.run, filter_marker='INSTATRACE: ')

    @classmethod
    def run(cls, args):
        stats = Accumulator()
        marker = None
        if args.filter:
            marker = args.filter_marker
        for filename in args.file:
            stats.load(filename, None, marker)

        stats.dump(sys.stdout)
        return


class HistogramsCommand:

    @classmethod
    def add_subparser(cls, parser):
        subparser = parser.add_parser('histograms', help='Stat histograms')
        subparser.add_argument('-c', '--config', help='Statistics configuration file')
        subparser.add_argument('--filter', action='store_true', help="Filter out any lines that don't contain INSTATRACE")
        subparser.add_argument('-s', '--stat', action='append', dest='show_stats', metavar='STAT', help='Ignore stats not matching STAT')
        subparser.add_argument('file', nargs='+')
        subparser.set_defaults(run=cls.run, filter_marker='INSTATRACE: ')

    @classmethod
    def run(cls, args):
        stats = Accumulator()
        marker = None
        if args.filter:
            marker = args.filter_marker
        for filename in args.file:
            stats.load(filename, args.show_stats, marker)

        config = SafeConfigParser({'layout': 'exponential', 'scale': '1'})
        if args.config is not None:
            config.read(args.config)
        names = stats.statistics.keys()
        names.sort()
        for (i, name) in enumerate(names):
            samples = stats.statistics.get(name)
            stat = Statistic(name, samples, config)
            stat.write_text_histogram(sys.stdout)
            if i != len(names) - 1:
                sys.stdout.write('\n')

        return