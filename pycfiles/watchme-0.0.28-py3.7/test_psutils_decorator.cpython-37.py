# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/watchme/tests/test_psutils_decorator.py
# Compiled at: 2020-04-10 14:08:50
# Size of source mod 2**32: 1032 bytes
from watchme.watchers.psutils.decorators import monitor_resources
from time import sleep

@monitor_resources('system', seconds=3)
def myfunc(iters, pause):
    long_list = []
    print('Generating a long list, pause is %s and iters is %s' % (pause, iters))
    for i in range(iters):
        long_list = long_list + i * 10 * ['pancakes']
        print('i is %s, sleeping %s seconds' % (i, pause))
        sleep(pause)

    return len(long_list)


if __name__ == '__main__':
    print('Calling myfunc with 2 iters')
    result = myfunc(2, 2)
    print('Result list has length %s' % result)