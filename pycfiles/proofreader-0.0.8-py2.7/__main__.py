# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/proofreader/__main__.py
# Compiled at: 2018-03-13 09:30:54
import argparse, os
from proofreader.runner import run
DIRECTORY = os.getcwd()
PARSER = argparse.ArgumentParser(description='proofreader')
PARSER.add_argument('--check-licenses', type=bool, help='Check for supported licenses .e.g. true')
PARSER.add_argument('--targets', default=[], nargs='*', help='Target files and directories .e.g. dir1/* file1.py file2.py')
ARGS = PARSER.parse_args()

def main():
    run(targets=ARGS.targets, config_dir=DIRECTORY, check_licenses=ARGS.check_licenses)