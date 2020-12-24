# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/inquant/tools/mkvimproject/project.py
# Compiled at: 2007-06-30 10:16:03
__author__ = 'Stefan Eletzhofer <stefan.eletzhofer@inquant.de>'
__docformat__ = 'plaintext'
__revision__ = '$Revision: 2382 $'
import sys, os
from mkvimproject import run
from mkvimproject import FILTERS

def create_project_file(filename, options):
    pattern = FILTERS['none']
    if options.filter:
        pattern = options.filter
    if options.filterset in FILTERS.keys():
        pattern = FILTERS[options.filterset]
    run('.', file(filename, 'w'), pattern)


def launch_vim(projectfile):
    import subprocess
    return subprocess.call(['gvim', '-c', 'Project %s' % projectfile])


def main():
    import optparse
    parser = optparse.OptionParser()
    parser.add_option('-U', '--update', action='store_true', dest='update', default=False, help='Update projectfile.')
    parser.add_option('-X', '--nolaunch', action='store_false', dest='launch', default=True, help='Do noit launch vim. Use with -U.')
    parser.add_option('-f', '--filter', dest='filter', action='append', help='The extensions to allow.')
    parser.add_option('-s', '--filterset', dest='filterset', action='store', help='The filterset to use: one of %s' % (',').join(FILTERS.keys()))
    (options, args) = parser.parse_args()
    if len(args):
        os.chdir(args[0])
    projectfile = '%s.vpj' % os.path.basename(os.getcwd())
    if not os.path.exists(projectfile) or options.update:
        create_project_file(projectfile, options)
        print 'Projectfile %s created.' % projectfile
    if options.launch:
        launch_vim(projectfile)


if __name__ == '__main__':
    main()