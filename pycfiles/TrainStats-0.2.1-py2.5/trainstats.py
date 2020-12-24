# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/trainstats/trainstats.py
# Compiled at: 2009-02-25 09:53:23
import os, sys, datetime, locale
from optparse import OptionParser
from viaggiatreno.viaggiatreno import ViaggiaTreno
from graph import Graph
PROGRAM_VERSION = '0.2.1'

def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        locale.setlocale(locale.LC_ALL, 'it_IT.UTF-8')
    except Exception, e:
        print 'Cannot set locale: %s' % e.message

    cmdline_parser = OptionParser(usage='%prog -t <train_id> [-d <YYYYMMGG>|-T] [more_options]', description='Get train time data from viaggiatreno.it', version='%s' % PROGRAM_VERSION)
    cmdline_parser.add_option('-t', '--train', action='store', type='int', dest='trainId', help='Train ID', default=None)
    cmdline_parser.add_option('-d', '--date', action='store', type='string', dest='date', help='Train date', default=None)
    cmdline_parser.add_option('-T', '--today', action='store_true', dest='today', help="Use today's date", default=False)
    cmdline_parser.add_option('-g', '--graph', action='store', type='string', dest='graphfile', help='File to write the graph to (PNG)', default=None)
    cmdline_parser.add_option('-G', '--autograph', action='store_true', dest='autograph', help='Automatically generate output graph filename', default=False)
    (options, args) = cmdline_parser.parse_args(argv[1:])
    if options.trainId is None:
        cmdline_parser.print_help()
        ret = 1
    else:
        if options.today:
            date = datetime.date.today()
        elif options.date is not None:
            try:
                dt = datetime.datetime.strptime(options.date, '%Y%m%d')
                date = dt.date()
            except ValueError, e:
                print 'Cannot parse date, please use the YYYYMMDD format.'
                date = None
                ret = 2

        else:
            print 'No date specified'
            cmdline_parser.print_help()
            ret = 1
            date = None
        if date is not None:
            vt = ViaggiaTreno()
            data = vt.get(options.trainId, date)
            if options.graphfile is not None:
                graphfile = options.graphfile
            elif options.autograph:
                graphfile = '%d-%s.png' % (options.trainId, date.strftime('%Y%m%d'))
            else:
                graphfile = None
            if graphfile is not None:
                g = Graph()
                g.daily(options.trainId, date, data, graphfile)
            ret = 0
    return ret


if __name__ == '__main__':
    sys.exit(main())