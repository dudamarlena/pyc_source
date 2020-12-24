# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/halicea/lib/dirtree.py
# Compiled at: 2011-12-25 05:31:43
from os import listdir, sep
from os.path import abspath, basename, isdir
from sys import argv

def tree(dir, padding, print_files=False, depth=3):
    print padding[:-1] + '+-' + basename(abspath(dir)) + '/'
    padding = padding + ' '
    files = []
    if print_files:
        files = listdir(dir)
    else:
        files = [ x for x in listdir(dir) if isdir(dir + sep + x) ]
    count = 0
    if depth != 0:
        for file in files:
            count += 1
            print padding + '|'
            path = dir + sep + file
            if isdir(path):
                if count == len(files):
                    tree(path, padding + ' ', print_files, depth - 1)
                else:
                    tree(path, padding + '|', print_files, depth - 1)
            else:
                print padding + '+-' + file


def usage():
    return 'Usage: %s [-f] <PATH>\nPrint tree structure of path specified.\nOptions:\n-f      Print files as well as directories\nPATH    Path to process' % basename(argv[0])


def main():
    if len(argv) == 1:
        print usage()
    elif len(argv) == 2:
        path = argv[1]
        if isdir(path):
            tree(path, ' ')
        else:
            print "ERROR: '" + path + "' is not a directory"
    elif len(argv) == 3 and argv[1] == '-f':
        path = argv[2]
        if isdir(path):
            tree(path, ' ', True)
        else:
            print "ERROR: '" + path + "' is not a directory"
    else:
        print usage()


if __name__ == '__main__':
    main()