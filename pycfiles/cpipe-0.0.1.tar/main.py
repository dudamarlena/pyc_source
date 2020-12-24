# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/cpip/main.py
# Compiled at: 2017-10-03 13:07:16
__author__ = 'Paul Ross'
__date__ = '2011-07-10'
__rights__ = 'Copyright (c) 2008-2017 Paul Ross'
import os, sys, logging, time
from optparse import OptionParser
import multiprocessing
__version__ = '0.1.0'

def unitTest():
    pass


def main():
    usage = 'usage: %prog [options] ...'
    optParser = OptionParser(usage, version='%prog ' + __version__)
    optParser.add_option('-l', '--loglevel', type='int', dest='loglevel', default=30, help='Log Level (debug=10, info=20, warning=30, error=40, critical=50) [default: %default]')
    optParser.add_option('-j', '--jobs', type='int', dest='jobs', default=0, help='Max processes when multiprocessing. Zero uses number of native CPUs [%d]' % multiprocessing.cpu_count() + ' [default: %default]')
    optParser.add_option('-u', '--unittest', action='store_true', dest='unit_test', default=False, help='Execute unit tests. [default: %default]')
    optParser.add_option('-n', action='store_true', dest='nervous', default=False, help='Nervous mode (do no harm). [default: %default]')
    optParser.add_option('-I', '--usr', action='append', dest='incUsr', help='Add user include search path. [default: %default]')
    optParser.add_option('-J', '--sys', action='append', dest='incSys', help='Add system include search path. [default: %default]')
    optParser.add_option('-P', '--pre', action='append', dest='incPre', help='Add pre-include file path. [default: %default]')
    opts, args = optParser.parse_args()
    clkStart = time.clock()
    logging.basicConfig(level=opts.loglevel, format='%(asctime)s %(levelname)-8s %(message)s', stream=sys.stdout)
    logging.critical('Test logging message')
    logging.critical('opts: %s' % opts)
    logging.critical('args: %s' % args)
    if opts.unit_test:
        unitTest()
    if len(args) > 0:
        pass
    else:
        optParser.print_help()
        optParser.error('No arguments!')
        return 1
    clkExec = time.clock() - clkStart
    print 'CPU time = %8.3f (S)' % clkExec
    print 'Bye, bye!'
    return 0


if __name__ == '__main__':
    sys.exit(main())