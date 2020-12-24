# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/WellDone/pymomo/pymomo/config/site_scons/utilities.py
# Compiled at: 2015-03-19 14:45:48
from SCons.Script import *
from SCons.Environment import Environment
import os, fnmatch, json, sys, os.path, pic12, StringIO
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from pymomo.utilities import build
from pymomo.mib.config12 import MIB12Processor

def find_files(dirname, pattern):
    """
        Recursively find all files matching pattern under path dirname
        """
    matches = []
    for root, dirnames, filenames in os.walk(dirname, followlinks=True):
        print dirnames, filenames
        for filename in fnmatch.filter(filenames, pattern):
            matches.append(os.path.join(root, filename))

    return matches


def build_includes(includes):
    if isinstance(includes, basestring):
        includes = [
         includes]
    return [ '-I"%s"' % x for x in includes ]


def build_libdirs(libdirs):
    if isinstance(libdirs, basestring):
        libdirs = [
         libdirs]
    return [ '-L"%s"' % x for x in libdirs ]


def build_staticlibs(libs, chip):
    if isinstance(libs, basestring):
        libs = [
         libs]
    processed = []
    for lib in libs:
        if lib[0] == '#':
            processed.append(lib[1:])
        else:
            proclib = '%s_%s' % (lib, chip.arch_name())
            processed.append(proclib)

    return [ '-l%s' % x for x in processed ]


def build_defines(defines):
    return [ '-D%s=%s' % (x, str(y)) for x, y in defines.iteritems() ]


def get_family(fam, modulefile=None):
    return build.ChipFamily(fam, modulefile=modulefile)


class BufferedSpawn:

    def __init__(self, env, logfile):
        self.env = env
        self.logfile = logfile
        self.stderr = StringIO.StringIO()
        self.stdout = StringIO.StringIO()

    def spawn(self, sh, escape, cmd, args, env):
        cmd_string = (' ').join(args)
        print cmd_string
        self.stdout.write(cmd_string)
        try:
            retval = self.env['PSPAWN'](sh, escape, cmd, args, env, sys.stdout, sys.stderr)
        except OSError as x:
            if x.errno != 10:
                raise x
            print 'OSError Ignored on command: %s' % cmd_string

        return retval