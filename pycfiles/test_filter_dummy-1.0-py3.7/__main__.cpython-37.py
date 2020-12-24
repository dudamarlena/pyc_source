# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/test_filter_dummy/__main__.py
# Compiled at: 2019-10-10 14:02:33
# Size of source mod 2**32: 416 bytes
import filter, argparse
print('in')
parser = argparse.ArgumentParser()
grp = parser.add_argument_group()
grp.add_argument('--a', default=10)
grp.add_argument('--b', default=10)
grp.add_argument('--c', default=10)
options = parser.parse_args()
print(options.a, options.b, options.c)
f = filter.filtermanager(options.a, options.b, options.c)
f.calc()
f.cald()