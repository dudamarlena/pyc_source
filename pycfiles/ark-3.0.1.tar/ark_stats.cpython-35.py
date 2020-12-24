# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dmlhllnd/dev/src/ark/ark/ext/ark_stats.py
# Compiled at: 2016-09-05 18:24:48
# Size of source mod 2**32: 877 bytes
from ark import hooks, site

@hooks.register('exit_build')
def print_stats():
    rendered, written = site.rendered(), site.written()
    time = site.runtime()
    average = time / rendered if rendered else 0
    report = 'Rendered: %5d  |  Written: %5d  |  '
    report += 'Time: %5.2f sec  |  Avg: %.4f sec/page'
    print(report % (rendered, written, time, average))