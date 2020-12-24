# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/csams/git_repos/personal/rulz/lib/python3.7/site-packages/rulz/plugins/demo.py
# Compiled at: 2019-05-03 16:41:25
# Size of source mod 2**32: 233 bytes
from rulz import plugin, run_graph

@plugin()
def one():
    return 1


@plugin()
def two():
    return 2


@plugin(one, two)
def add(a, b):
    return a + b


if __name__ == '__main__':
    print(run_graph())