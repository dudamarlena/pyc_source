# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/eggspacker/command.py
# Compiled at: 2011-12-01 06:38:48
import optparse, sys, os
from eggspacker import EggsPacker
parser = optparse.OptionParser('%prog [options] pkgname [pkgname [pkgname...]]')
parser.add_option('-i', '--index', dest='index', default='http://pypi.python.org/simple/', help='A Pypi compatible index URL. Default to pypi')
parser.add_option('-t', '--targetdir', dest='targetdir', default='basket', help='Target directory. Default: "basket".')
parser.add_option('--python-version', dest='python_version', default='%s.%s' % sys.version_info[0:2], help='Target python version.')
parser.add_option('--platform', dest='platform', help='Target platform')
parser.add_option('--unzip', action='append', dest='unzip', default=[], help='Unzip the asked egg if present in the dependencies. The special value "auto" will guess what to do with with not-zip-safe flag, and "all" will force unzipping of all the eggs. Can be specified several times.')

def main():
    options, args = parser.parse_args()
    if len(args) < 1:
        parser.error('Missing arguments')
    if not os.path.exists(options.targetdir):
        os.mkdir(options.targetdir)
    packer = EggsPacker(index=options.index, basket=options.targetdir, python=options.python_version, platform=options.platform, unzip=options.unzip)
    for egg in args:
        packer.pack(egg)