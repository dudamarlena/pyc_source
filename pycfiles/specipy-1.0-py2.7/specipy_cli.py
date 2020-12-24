# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/bin/specipy_cli.py
# Compiled at: 2015-06-10 03:12:00
import specipy, argparse, os

def parse():
    global parser
    parser = argparse.ArgumentParser(description='Display the parsed Kiwi spec in formatted text.')
    parser.add_argument('file', type=str, help='kiwi file path')
    parsed_args = parser.parse_args()
    file = parsed_args.file
    if not os.path.exists(file):
        print 'The provided file does not exist %s' % file
        exit(0)
    with open(file, 'r') as (open_file):
        parsed = specipy.SpecParser(open_file.read())
        print parsed.root.elements_description()