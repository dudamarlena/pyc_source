# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/symlinkator/symlinkator.py
# Compiled at: 2019-01-15 18:29:38
import os, sys

def get_dir_tuple(filename, directory):
    abspath = os.path.join(directory, filename)
    realpath = os.path.realpath(abspath)
    exists = os.path.exists(abspath)
    return (filename, realpath, exists)


def get_links(directory):
    file_list = [ get_dir_tuple(f, directory) for f in os.listdir(directory) if os.path.islink(os.path.join(directory, f))
                ]
    return file_list


def main():
    if not len(sys.argv) == 2:
        print 'USAGE: %s directory' % sys.argv[0]
        exit(1)
    directory = sys.argv[1]
    print get_links(directory)


if __name__ == '__main__':
    main()