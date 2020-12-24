# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/gitversionbuilder/__main__.py
# Compiled at: 2015-09-21 10:52:48
import argparse, importlib
from gitversionbuilder import main
try:
    Version = importlib.import_module('.Version', package='gitversionbuilder')
except ImportError:
    Version = importlib.import_module('.DummyVersion', package='gitversionbuilder')

def run_main():
    parser = argparse.ArgumentParser(description='Create a source file containing git version information.')
    parser.add_argument('--version', action='version', version=Version.VERSION_STRING)
    parser.add_argument('--lang', choices=['cpp', 'python'], required=True)
    parser.add_argument('--dir', default='.')
    parser.add_argument('file')
    args = parser.parse_args()
    print 'Creating git version information from %s' % args.dir
    main.create_version_file(git_directory=args.dir, output_file=args.file, lang=args.lang)


if __name__ == '__main__':
    run_main()