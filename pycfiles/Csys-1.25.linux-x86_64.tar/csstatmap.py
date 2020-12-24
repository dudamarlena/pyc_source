# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/bill/py3/.virtualenvs/pytest/lib/python2.7/site-packages/Csys/csstatmap.py
# Compiled at: 2005-10-02 14:00:23
import Csys, os, os.path, sys, re
__doc__ = 'Create pickle file per directory with stat info.\n\nusage: [options] %s\n' % Csys.Config.progname
__doc__ += '\n\n$Id: csstatmap.py,v 1.1 2005/10/02 18:00:23 csoftmgr Exp $\n'
__doc__ = Csys.detab(__doc__)
__version__ = '$Revision: 1.1 $'[11:-2]
parser = Csys.getopts(__doc__)
options, args = parser.parse_args()
if options.verbose:
    verbose = '-v'
Csys.getoptionsEnvironment(options)
import cPickle
pname = '.cs_stats'
skip_list = (
 '.cvsignore',
 'CVS',
 pname)

def mapstats(dir):
    """Get stat(2) info for everything in a directory"""
    stats = {}
    for name in os.listdir(dir):
        if name not in skip_list:
            path = os.path.join(dir, name)
            stats[name] = os.stat(path)
            if os.path.isdir(path):
                mapstats(path)

    pfile = os.path.join(dir, pname)
    fh = open(pfile, 'w')
    cPickle.dump(stats, fh)
    fh.close()


for dir in args:
    mapstats(dir)