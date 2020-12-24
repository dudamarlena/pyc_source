# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/benchbase/main.py
# Compiled at: 2011-09-20 08:47:40
"""
Try to do something usefull with a jmeter output.
"""
import os, sys
from optparse import OptionParser, TitledHelpFormatter
from util import get_version, init_logging
from command import *
DEFAULT_DB = '~/benchbase.db'
DEFAULT_LOG = '~/benchbase.log'
USAGE = 'benchbase [--version] [--logfile=LOGFILE] [--database=DATABASE] COMMAND [OPTIONS] [ARGUMENT]\n\nCOMMANDS:\n\n  list\n     List the imported benchmark in the database.\n\n  info BID\n     Give more information about the benchmark with the bid number (benchmark identifier).\n\n  import [--jmeter|--funkload|--comment] FILE\n     Import the benchmark result into the database. Output the BID number.\n\n  addsar --host HOST [--comment COMMENT] BID SAR\n     Import the text sysstat sar output\n\n  report --output REPORT_DIR BID\n     Generate the report for the imported benchmark\n\nEXAMPLES\n\n   benchbase list\n      List of imported benchmarks.\n\n   benchbase import -m"Run 42" jmeter-2010.xml\n      Import a JMeter benchmark result file, this will output a BID number.\n.\n   benchbase addsar -H"localhost" -m"bencher host" 1 /tmp/sysstat-sar.log.gz\n      Attach a gzipped sysstat sar file for the bench BID 1.\n\n   benchbase report 1 -o /tmp/report-run42\n      Build the report of benchmark BID 1 into /tmp/report-run42 directory.\n\n'

def main(argv=sys.argv):
    """Main test"""
    global USAGE
    parser = OptionParser(USAGE, formatter=TitledHelpFormatter(), version='benchbase %s' % get_version())
    parser.add_option('-v', '--verbose', action='store_true', help='Verbose output')
    parser.add_option('-l', '--logfile', type='string', default=os.path.expanduser(DEFAULT_LOG), help='Log file path')
    parser.add_option('-d', '--database', type='string', default=os.path.expanduser(DEFAULT_DB), help='SQLite db path')
    parser.add_option('-m', '--comment', type='string', help='Add a comment')
    parser.add_option('-j', '--jmeter', action='store_true', default=True, help='JMeter input file')
    parser.add_option('-f', '--funkload', action='store_true', default=False, help='FunkLoad input file')
    parser.add_option('--rmdatabase', action='store_true', default=False, help='Remove existing database')
    parser.add_option('-o', '--output', type='string', help='Report output directory')
    parser.add_option('-H', '--host', type='string', help='Host name when adding sar report')
    parser.add_option('-r', '--runningavg', type='int', default=5, help='Number of second to compute the running average.')
    parser.add_option('--chart-width', type='int', default=800, help='Width of charts in report.')
    parser.add_option('--chart-height', type='int', default=768, help='Heigth of charts in report.')
    parser.add_option('--period', type='int', help='Resolution in second')
    (options, args) = parser.parse_args(argv)
    init_logging(options)
    if len(args) == 1:
        parser.error('Missing command')
    cmd = args[1]
    fn = globals()[('cmd_' + cmd)]
    ret = fn(args[2:], options)
    return ret


if __name__ == '__main__':
    ret = main()
    sys.exit(ret)