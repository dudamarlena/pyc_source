# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/oZip/cli.py
# Compiled at: 2014-09-02 10:16:34
from main import main
import argparse

def run():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', action='store', dest='path', help='Path to input file', required=True)
    parser.add_argument('-d', action='store_true', default=False, dest='should_decompress', help='Decompress a file')
    parser.add_argument('--version', action='version', version='oZip 1.0')
    results = parser.parse_args()
    path = results.path
    action = results.should_decompress
    res = main(path, action)
    if res:
        print 'Error while processing %s: \n%s' % res
        print 'Please Report this error (with a screenshot) in the following URL:'
        print 'http://github.com/OzTamir/oZip/issues'
    else:
        print 'Processing completed successfully.'


if __name__ == '__main__':
    run()