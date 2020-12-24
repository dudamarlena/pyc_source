# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/cyglass/f2c/__main__.py
# Compiled at: 2018-08-01 18:59:20
"""
cyglass.f2c.main -- shortdesc

cyglass.f2c.main is a description

It defines classes_and_methods

@author:     user_name

@copyright:  2018 organization_name. All rights reserved.

@license:    license

@contact:    user_email
@deffield    updated: Updated
"""
import sys, os
from optparse import OptionParser
__all__ = []
__version__ = 0.1
__date__ = '2018-08-01'
__updated__ = '2018-08-01'
DEBUG = 1
TESTRUN = 0
PROFILE = 0

def main(argv=None):
    """Command line options."""
    program_name = os.path.basename(sys.argv[0])
    program_version = 'v0.1'
    program_build_date = '%s' % __updated__
    program_version_string = '%%prog %s (%s)' % (program_version, program_build_date)
    program_longdesc = ''
    program_license = 'Copyright 2018 (CyGlass, Inc.)                                                            Licensed under the Apache License 2.0\nhttp://www.apache.org/licenses/LICENSE-2.0'
    if argv is None:
        argv = sys.argv[1:]
    try:
        parser = OptionParser(version=program_version_string, epilog=program_longdesc, description=program_license)
        parser.add_option('-i', '--in', dest='infile', help='set input path [default: %default]', metavar='FILE')
        parser.add_option('-o', '--out', dest='outfile', help='set output path [default: %default]', metavar='FILE')
        parser.add_option('-v', '--verbose', dest='verbose', action='count', help='set verbosity level [default: %default]')
        parser.set_defaults(outfile='./out.txt', infile='./in.txt')
        opts, args = parser.parse_args(argv)
        if opts.verbose > 0:
            print 'verbosity level = %d' % opts.verbose
        if opts.infile:
            print 'infile = %s' % opts.infile
        if opts.outfile:
            print 'outfile = %s' % opts.outfile
    except Exception as e:
        indent = len(program_name) * ' '
        sys.stderr.write(program_name + ': ' + repr(e) + '\n')
        sys.stderr.write(indent + '  for help use --help')
        return 2

    return


if __name__ == '__main__':
    if DEBUG:
        sys.argv.append('-h')
    if TESTRUN:
        import doctest
        doctest.testmod()
    if PROFILE:
        import cProfile, pstats
        profile_filename = 'cyglass.f2c.main_profile.txt'
        cProfile.run('main()', profile_filename)
        statsfile = open('profile_stats.txt', 'wb')
        p = pstats.Stats(profile_filename, stream=statsfile)
        stats = p.strip_dirs().sort_stats('cumulative')
        stats.print_stats()
        statsfile.close()
        sys.exit(0)
    sys.exit(main())