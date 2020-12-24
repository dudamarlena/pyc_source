# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\responder3\tools\proxyfilereader.py
# Compiled at: 2019-04-29 07:33:30
# Size of source mod 2**32: 488 bytes
from responder3.core.commons import *

def print_packets(filename):
    with open(filename, 'r') as (f):
        for line in f:
            line = line.strip()
            pd = ProxyData.fromJSON(line)
            print(str(pd))


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Parse the prox log file and print each packet to stdout')
    parser.add_argument('filename', help='full path to the proxy log file')
    args = parser.parse_args()
    print_packets(args.filename)