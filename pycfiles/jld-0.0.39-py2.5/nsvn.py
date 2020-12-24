# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\jld\cmd\nsvn.py
# Compiled at: 2009-03-24 20:56:20
""" NukeSVN - deletes all SVN related directories from a path hierarchy

    @author: Jean-Lou Dupont
"""
__author__ = 'Jean-Lou Dupont'
__version__ = '$Id: nsvn.py 894 2009-03-25 00:56:18Z JeanLou.Dupont $'
import glob, os, sys
from optparse import OptionParser
from jld.tools.mos import nukedir
_options = [{'o1': '-F', 'var': 'force', 'action': 'store_true', 'default': False, 'help': 'Forces the delete action'}, {'o1': '-q', 'var': 'quiet', 'action': 'store_true', 'default': False, 'help': 'Quiet mode'}]
_usage = '%prog [options] [input_directory]\n\nNukeSVN - deletes all SVN related directories from a directory hierarchy\nversion $LastChangeRevision$ by Jean-Lou Dupont\n\nThe -F option must be used in order to actually perform the delete action or else only a list of the found targets is produced.\n'

def main():
    parser = OptionParser(usage=_usage)
    for o in _options:
        parser.add_option(o['o1'], dest=o['var'], action=o['action'], help=o['help'], default=o['default'])

    (options, args) = parser.parse_args()
    try:
        input = args[0]
    except:
        input = os.getcwd()

    if not os.path.isdir(input):
        print 'Error: invalid input_directory parameter'
        return 0
    if options.force:
        prepend = 'deleting: [%s]'
    else:
        prepend = 'target: [%s]'
    targets = []
    for (root, dirs, files) in os.walk(input, topdown=False):
        if os.path.basename(root) == '.svn':
            targets.append(root)

    try:
        for directory in targets:
            if not options.quiet:
                print prepend % directory
            if options.force:
                nukedir(directory)

    except Exception, e:
        print 'Error: [%s]' % e
        return 0

    return 1


if __name__ == '__main__':
    sys.exit(main())