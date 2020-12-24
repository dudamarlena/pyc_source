# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dmulholl/dev/src/ivy/ivy/extensions/ivy_stats.py
# Compiled at: 2019-01-23 08:54:51
# Size of source mod 2**32: 1052 bytes
from ivy import hooks, site, utils

@hooks.register('exit_build')
def print_stats():
    rendered, written = site.rendered(), site.written()
    time = site.runtime()
    average = time / rendered if rendered else 0
    report = 'Rendered: %5d  ·  Written: %5d  ·  '
    report += 'Time: %5.2f sec  ·  Avg: %.4f sec/page'
    report = report.replace('·', '\x1b[90m·\x1b[0m')
    utils.safeprint(report % (rendered, written, time, average))