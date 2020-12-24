# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/schevo/script/opt.py
# Compiled at: 2007-03-21 14:34:41
"""General option parser.

For copyright, license, and warranty, see bottom of file.
"""
from optparse import OptionParser
from schevo import trace

def set_trace(option, opt, value, parser):
    trace.print_history(value)
    trace.monitor_level = value
    trace.log(1, 'Tracing level set to', value)


def parser(usage):
    p = OptionParser(usage)
    p.add_option('-T', '--trace', help='Set Schevo tracing level.', action='callback', callback=set_trace, type=int)
    return p