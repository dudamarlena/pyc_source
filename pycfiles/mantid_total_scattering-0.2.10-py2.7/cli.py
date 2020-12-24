# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/total_scattering/cli.py
# Compiled at: 2019-10-03 13:30:51
from __future__ import absolute_import, division, print_function
import json
from total_scattering.reduction import TotalScatteringReduction

def main(config=None):
    if not config:
        import argparse
        parser = argparse.ArgumentParser(description='Absolute normalization PDF generation')
        parser.add_argument('json', help='Input json file')
        options = parser.parse_args()
        print("loading config from '%s'" % options.json)
        with open(options.json, 'r') as (handle):
            config = json.load(handle)
    TotalScatteringReduction(config)


if __name__ == '__main__':
    main()