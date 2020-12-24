# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./build/lib/supervisor/tests/fixtures/test_1231.py
# Compiled at: 2019-05-23 17:27:11
# Size of source mod 2**32: 489 bytes
import logging, random, sys, time

def main():
    logging.basicConfig(level=(logging.INFO), stream=(sys.stdout), format='%(levelname)s [%(asctime)s] %(message)s',
      datefmt='%m-%d|%H:%M:%S')
    i = 1
    while i < 500:
        delay = random.randint(400, 1200)
        time.sleep(delay / 1000.0)
        logging.info('%d - hash=57d94b…381088', i)
        i += 1


if __name__ == '__main__':
    main()