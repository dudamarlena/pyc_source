# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/rejester/tests/run.py
# Compiled at: 2015-07-08 07:32:10
"""rejester self-tests.

-----

This software is released under an MIT/X11 open source license.

Copyright 2014 Diffeo, Inc.

"""
from __future__ import absolute_import
import argparse, os, sys, pytest

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('redis_address', metavar='HOST:PORT', help='location of a redis instance to use for testing')
    args = parser.parse_args()
    test_dir = os.path.dirname(__file__)
    response = pytest.main(['-v', '-v',
     '--redis-address', args.redis_address,
     test_dir])
    sys.exit(response)


if __name__ == '__main__':
    main()