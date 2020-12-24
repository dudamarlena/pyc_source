# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\supervisor\scripts\sample_eventlistener.py
# Compiled at: 2015-07-18 10:13:56
import sys

def write_stdout(s):
    sys.stdout.write(s)
    sys.stdout.flush()


def write_stderr(s):
    sys.stderr.write(s)
    sys.stderr.flush()


def main():
    while 1:
        write_stdout('READY\n')
        line = sys.stdin.readline()
        write_stderr(line)
        headers = dict([ x.split(':') for x in line.split() ])
        data = sys.stdin.read(int(headers['len']))
        write_stderr(data)
        write_stdout('RESULT 2\nOK')


if __name__ == '__main__':
    main()