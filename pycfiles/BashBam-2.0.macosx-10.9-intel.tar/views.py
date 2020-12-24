# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/amay/.virtualenvs/bam/lib/python2.7/site-packages/bashbam/views.py
# Compiled at: 2014-02-23 18:24:43
from os import system
from optparse import OptionParser
from controllers import add_script, rm_script, run_script, ls_scripts

def main():
    usage = '\nbam <script>\nbam add <gist path (user/gist_name)>\nbam rm <script>\nbam ls'
    version = '2.0'
    parser = OptionParser(usage=usage, version='BashBam v%s' % version)
    options, args = parser.parse_args()
    if len(args) < 1:
        parser.print_version()
        print ''
        parser.print_usage()
        return 0
    if args[0] == 'add':
        if not args[1]:
            print 'Please provide a gist path (user/gist_name).'
            return -1
        return add_script(origin=args[1])
    if args[0] == 'rm':
        if not args[1]:
            print 'Please provide a script name.'
            return -1
        return rm_script(args[1])
    if args[0] == 'ls':
        return ls_scripts()
    return run_script(args[0])


if __name__ == '__main__':
    main()