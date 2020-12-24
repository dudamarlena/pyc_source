# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pgpdump/__main__.py
# Compiled at: 2015-08-18 08:22:24
import sys
from . import AsciiData, BinaryData

def parsefile(name):
    with open(name, 'rb') as (infile):
        if name.endswith('.asc') or name.endswith('.txt'):
            data = AsciiData(infile.read())
        else:
            data = BinaryData(infile.read())
    for packet in data.packets():
        yield packet


def main():
    counter = length = 0
    for filename in sys.argv[1:]:
        for packet in parsefile(filename):
            counter += 1
            length += packet.length

    print('%d packets, length %d' % (counter, length))


if __name__ == '__main__':
    main()