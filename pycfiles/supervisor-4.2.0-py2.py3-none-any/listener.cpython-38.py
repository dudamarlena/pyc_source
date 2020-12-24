# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./build/lib/supervisor/tests/fixtures/listener.py
# Compiled at: 2019-04-05 17:19:18
# Size of source mod 2**32: 935 bytes
import sys

def write_and_flush(stream, s):
    stream.write(s)
    stream.flush()


def write_stdout(s):
    sys.stdout.write(s)
    sys.stdout.flush()


def write_stderr(s):
    sys.stderr.write(s)
    sys.stderr.flush()


def main():
    stdin = sys.stdin
    stdout = sys.stdout
    stderr = sys.stderr
    while True:
        write_and_flush(stdout, 'READY\n')
        line = stdin.readline()
        write_and_flush(stderr, line)
        headers = dict([x.split(':') for x in line.split()])
        data = stdin.read(int(headers['len']))
        write_and_flush(stderr, data)
        write_and_flush(stdout, 'RESULT 2\nOK')


if __name__ == '__main__':
    main()