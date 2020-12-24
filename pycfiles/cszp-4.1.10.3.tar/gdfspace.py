# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/bill/py3/.virtualenvs/pytest/lib/python2.7/site-packages/Csys/gdfspace.py
# Compiled at: 2009-11-24 20:44:53
import Csys, os, os.path, sys, re
__doc__ = 'Celestial Software Main program prototype\n\nusage: %s' % Csys.Config.progname
__doc__ += '\n\n$Id: gdfspace.py,v 1.1 2009/11/25 01:44:53 csoftmgr Exp $\n'
__version__ = '$Revision: 1.1 $'[11:-2]

def setOptions():
    """Set command line options"""
    global __doc__
    parser = Csys.getopts(__doc__)
    return parser


parser = setOptions()
options, args = parser.parse_args()
if options.verbose:
    verbose = '-v'
else:
    verbose = ''
Csys.getoptionsEnvironment(options)
if not args:
    from Csys.SysUtils import getMounted
    for dir, d in getMounted().items():
        if not (d.pseudo or d.tmpfs):
            args.append(d.dir)

    args.sort()
Blksize = 1024
Mbyte = 1048576.0
CONST = Blksize / Mbyte
cmd = 'gdf -P %s 2>/dev/null' % (' ').join(args)
if verbose:
    sys.stderr.write('%s\n' % cmd)
df = Csys.popen(cmd)
df.readline()
Cumfree = Cumalloc = 0
for line in df:
    line = line.strip()
    filesys, alloc, tmpalloc, free, cap, dir = line.split()
    alloc = int(alloc)
    tmpalloc = int(tmpalloc)
    free = int(free)
    tfree = max(0, free * CONST - 0.005)
    talloc = max(0, alloc * CONST - 0.005)
    try:
        pct = free * 100 / alloc
    except ZeroDivisionError:
        print line
        raise

    print '%-10s: Disk space: %#6.2f MB of %#7.2f MB available (%#5.2f%%)' % (
     dir, tfree, talloc, pct)
    Cumfree += free
    Cumalloc += alloc

if Cumalloc != 0:
    CumPct = Cumfree * 100 / Cumalloc
    Cumfree = Cumfree * CONST - 0.005
    Cumalloc = Cumalloc * CONST - 0.005
    print '\nTotal Free Space: %#6.2f MB Used %#6.2f MB of %#6.2f MB available (%#5.2f%%)' % (
     Cumfree, Cumalloc - Cumfree, Cumalloc, CumPct)