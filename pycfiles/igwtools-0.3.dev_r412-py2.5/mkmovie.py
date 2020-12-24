# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/igwtools/mkmovie.py
# Compiled at: 2007-07-23 16:02:20
import os, sys, tempfile, shutil
from optparse import OptionParser

def make_movie(filenames, moviefile, options=''):
    filenames.sort()
    tempd = tempfile.mkdtemp()
    for fname in filenames:
        pass

    cmd = 'ffmpeg -i ' + tempd + '/frame%04d.pgm' + options + moviefile
    os.system(cmd)
    shutil.rmtree(tempd)


def make_movie_entry():
    usage = ' %prog [options] FILE(s) '
    parser = OptionParser(usage=usage, version='%prog (igwtools) ' + str(__version__))
    parser.add_option('-v', '--verbose', action='store_true', help='be verbose')
    (options, args) = parser.parse_args()
    make_movie(args)