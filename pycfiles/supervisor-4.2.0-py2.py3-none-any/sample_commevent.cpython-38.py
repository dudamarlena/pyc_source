# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./build/lib/supervisor/scripts/sample_commevent.py
# Compiled at: 2017-07-24 14:57:05
# Size of source mod 2**32: 562 bytes
import sys, time

def write_stdout(s):
    sys.stdout.write(s)
    sys.stdout.flush()


def main(sleep):
    while True:
        write_stdout('<!--XSUPERVISOR:BEGIN-->')
        write_stdout('the data')
        write_stdout('<!--XSUPERVISOR:END-->')
        time.sleep(sleep)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        main(float(sys.argv[1]))
    else:
        main(1)