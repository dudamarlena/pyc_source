# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/oplogutils/_core.py
# Compiled at: 2010-05-30 01:17:52
import calendar
from datetime import datetime
from pymongo.timestamp import Timestamp
from pymongo import Connection
import re, sys, tty, termios, os

def _num(n):
    return '([0-9]{%d,})' % n


_date_re = '%s-%s-%s %s:%s:%s' % tuple(map(_num, [4, 2, 2, 2, 2, 2]))

def timestamp(string_date):
    m = re.match(_date_re, string_date)
    if not m:
        msg = 'Invalid date: %s (use format: YYYY-MM-DD HH:MM:SS)' % string_date
        raise AssertionError(msg)
    d = datetime(*map(int, m.groups()))
    return Timestamp(calendar.timegm(d.timetuple()), 0)


class Command(object):

    def __init__(self):
        self.option_parser = self.get_options()
        self.common_options(self.option_parser)
        (self.opts, self.args) = self.option_parser.parse_args()
        if self.opts.version:
            self.show_version()
        if not self.opts.host:
            self.usage_error()
        self.validate_options()

    def usage_error(self):
        self.option_parser.print_help()
        sys.exit(-1)

    def show_version(self):
        print 'OPLOGUTILS version', sys.modules['oplogutils'].__version__
        sys.exit(0)

    def common_options(self, op):
        op.add_option('', '--host', action='store', dest='host', default=None, help='The hostname of the mongodb master instance.')
        op.add_option('', '--port', action='store', dest='port', type='int', default=27017, help='The port of the mongodb master instance. (Defaults to 27017.)')
        op.add_option('', '--version', action='store_true', dest='version', default=False, help='Display version information and exit.')
        return op

    def get_options(self):
        raise NotImplementedError()

    def validate_options(self):
        pass

    def connection(self):
        return Connection(self.opts.host, self.opts.port)

    def replication_enabled(self):
        stat = self.connection().admin.command({'serverStatus': 1})
        return 'repl' in stat

    def db_local(self):
        return self.connection().local

    def oplog(self):
        return self.db_local().oplog

    def run(self):
        raise NotImplementedError()

    def getch(self):
        fd = sys.stdin.fileno()
        if not os.isatty(fd):
            return sys.stdin.read(1)
        attr = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            return sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, attr)