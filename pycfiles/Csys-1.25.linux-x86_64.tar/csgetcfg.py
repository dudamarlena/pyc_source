# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/bill/py3/.virtualenvs/pytest/lib/python2.7/site-packages/Csys/csgetcfg.py
# Compiled at: 2009-11-25 02:49:11
import Csys, os, os.path, sys, re
__doc__ = 'Celestial Software Get options from INI style configuration files.\n\nusage: %s file section option [option...]' % Csys.Config.progname
__doc__ += '\n\n$Id: csgetcfg.py,v 1.2 2009/11/25 07:49:11 csoftmgr Exp $\n'
__version__ = '$Revision: 1.2 $'[11:-2]
parser = Csys.getopts(__doc__)
parser.add_option('-a', '--all', action='store_true', dest='all', default=False, help='Get all options')
parser.add_option('--eval', action='store_true', dest='eval', default=False, help='Output format for eval in scripts')
options, args = parser.parse_args()
if options.verbose:
    verbose = '-v'
Csys.getoptionsEnvironment(options)
cfgfile = args.pop(0)
cfg = Csys.ConfigParser(cfgfile)
section = args.pop(0)
rec = dict(cfg.items(section))
if options.all:
    args = rec.keys()
    options.eval = True
args.sort()
for arg in args:
    val = rec[arg].replace('\n', ' ').strip()
    if options.eval:
        print '%s=%s' % (arg, repr(val))
    else:
        print val