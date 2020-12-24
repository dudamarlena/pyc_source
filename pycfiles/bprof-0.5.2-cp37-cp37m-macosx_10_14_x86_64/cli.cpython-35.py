# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python3.5/dist-packages/bprc/cli.py
# Compiled at: 2016-08-21 09:43:12
# Size of source mod 2**32: 3016 bytes
__doc__ = '\nThis module takes care of capturing the cli options\n'
import os, sys
PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
import argparse, sys, logging
from bprc._version import __version__
parser = argparse.ArgumentParser(description='Batch Processing RESTful Client')
outputgroup = parser.add_argument_group(title='I/O arguments')
logtestgroup = parser.add_argument_group(title='Logging, testing and debugging arguments')
protocolgroup = parser.add_argument_group(title='Protocol arguments')
parser.add_argument('--version', action='version', version='{} {}'.format(sys.argv[0], __version__), help='shows version number and exits')
parser.add_argument('yamlfile', nargs='?', help='YAML recipe file, defaults to stdin', type=argparse.FileType('r'), default=sys.stdin)
parser.add_argument('outputfile', nargs='?', help=argparse.SUPPRESS, type=argparse.FileType('w'), default=sys.stdout)
outputgroup.add_argument('--output-format', dest='outputformat', action='store', choices={
 'raw-all', 'raw-response', 'json'}, default='raw-all', help='specifies output format, defaults to %(default)s')
outputgroup.add_argument('--no-color', dest='nocolor', action='store_true', default=False, help='turns off pretty printing for console output')
logtestgroup.add_argument('-v', '--verbose', dest='verbose', action='store_true', help='verbose mode', default=False)
logtestgroup.add_argument('--debug', dest='debug', action='store_true', default=False, help='turns on stacktrace dumps for exceptions')
logtestgroup.add_argument('--log-level', dest='loglevel', action='store', default='none', choices={
 'none', 'critical', 'error', 'warning', 'info', 'debug'}, help='sets logging level, defaults to %(default)s')
logtestgroup.add_argument('--log-file', dest='logfile', action='store', metavar='logfile', default='bprc.log', help='specifies logfile, defaults to %(default)s')
protocolgroup.add_argument('--skip-http-errors', dest='skiphttperrors', action='store_true', default=False, help='moves to the next step if an HTTP 4xx or 5xx response code is returned')
protocolgroup.add_argument('--ignore-ssl', dest='ignoressl', action='store_true', default=False, help='do not validate ssl certificates')
args = parser.parse_args()