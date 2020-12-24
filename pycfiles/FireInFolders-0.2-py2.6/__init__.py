# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fire_in_folders/__init__.py
# Compiled at: 2009-12-22 04:13:06
import os, sys
from subprocess import Popen
from optparse import OptionParser

def fire_in_folder(folder, args, options):
    for file in os.listdir(folder):
        path = os.path.join(folder, file)
        if os.path.isdir(path) and not file.startswith('.'):
            if options.verbose:
                print '--- running in folder %s ---' % path
            p = Popen(args=args, cwd=path)
            p.wait()
            if options.verbose:
                print '--- end --- '


def main(*a, **kw):
    parser = OptionParser(usage='fire_in_folders [options] command\n')
    parser.add_option('-s', '--src', action='store', dest='src', type='string', default='src', help='destination folder where to execute command in all subfolders')
    parser.add_option('-q', '--quiet', action='store_false', dest='verbose', default=True, help='do not display extra information')
    (options, args) = parser.parse_args()
    if not len(args):
        parser.parse_args(['-h'])
    target_path = os.path.join(os.getcwd(), options.src)
    if not os.path.exists(target_path):
        parser.error('Folder does not exist: %s' % target_path)
    fire_in_folder(target_path, args, options)


if __name__ == '__main__':
    main()