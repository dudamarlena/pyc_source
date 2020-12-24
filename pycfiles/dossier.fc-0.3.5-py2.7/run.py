# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dossier/fc/tests/run.py
# Compiled at: 2015-09-05 21:22:50
"""Run all dossier.fc tests.

.. This software is released under an MIT/X11 open source license.
   Copyright 2012-2014 Diffeo, Inc.

"""
from __future__ import absolute_import, division, print_function
import argparse, os
try:
    import pytest
except ImportError:
    pytest = None

import dossier.fc.tests.performance as performance_tests

def main():
    parser = argparse.ArgumentParser(description='Run all dossier.fc tests.')
    if pytest:
        parser.add_argument('--unit', action='store_true', help='Run unit tests')
    parser.add_argument('--performance', '--perf', action='store_true', help='Run performance tests')
    args = parser.parse_args()
    if not args.unit and not args.performance:
        args.unit = pytest is not None
        args.performance = True
    if args.unit:
        pytest.main(os.path.dirname(__file__))
    if args.performance:
        performance_tests.main()
    return


if __name__ == '__main__':
    main()