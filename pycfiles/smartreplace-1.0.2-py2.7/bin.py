# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/smartreplace/bin.py
# Compiled at: 2019-01-16 08:10:55
from smartreplace import sreplace
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('regex', help='regex to find needle')
parser.add_argument('replacer', help='what to replace needle with')
parser.add_argument('file_query', help='which files to look in, example: "*.py"')
args = parser.parse_args()

def run():
    sreplace(regex=args.regex, replacer=args.replacer, file_query=args.file_query)