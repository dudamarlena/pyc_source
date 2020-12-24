# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/benchline/timer.py
# Compiled at: 2014-04-25 18:53:17
"""
Script to time the execution of python code.
"""
import sys, time, benchline.args
if sys.platform == 'win32':
    timer_to_use = time.clock
else:
    timer_to_use = time.time

def start():
    return timer_to_use()


def stop(start_time):
    return timer_to_use() - start_time


def format_elapsed_time(elapsed_time):
    return '%s seconds' % elapsed_time


def main():
    benchline.args.go(__doc__)


if __name__ == '__main__':
    main()