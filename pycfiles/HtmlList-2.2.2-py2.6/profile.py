# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/htmllist/test/profile.py
# Compiled at: 2010-10-16 07:02:00
from cProfile import run
from pstats import Stats
from os import path
import glob
from regression_tests import run_test
LIMIT = 10
EXTRA = None
TEST = 'ebay'
SORT = 'time'
if EXTRA is None:
    modules = [ path.basename(module) for module in glob.glob('../*.py') if '__' not in module ]
    reg = '(' + ('|').join(modules) + '):'
else:
    reg = None
run("run_test('" + TEST + "', 0, for_profiling=True)", 'stats')
stats = Stats('stats')
stats.strip_dirs()
stats.sort_stats(SORT)
stats.print_stats(reg, EXTRA, LIMIT)
stats.print_callees(reg, EXTRA, LIMIT)
stats.print_callers(reg, EXTRA, LIMIT)