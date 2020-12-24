# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/bill/py3/.virtualenvs/pytest/lib/python2.7/site-packages/Csys/putty2sshpub.py
# Compiled at: 2009-11-25 02:52:38
import Csys, os, os.path, sys, re
__doc__ = "Convert putty public keys to openssh format\n\nusage: %s puttykeyfile [outputfile]\n\n Where: outputfile defaults to 'putty.pub'\n\n" % Csys.Config.progname
__doc__ += '\n\n$Id: putty2sshpub.py,v 1.2 2009/11/25 07:52:38 csoftmgr Exp $\n'
__version__ = '$Revision: 1.2 $'[11:-2]

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
excmds = '$d\n1d\ns/.*"\\(.*\\)"/\\1/\n1m$\n1\nj\nj\nj\ns/ //g\nj\ns/^/ssh-rsa /\nwq\n'
print excmds
if len(args) == 1:
    args.append('putty.pub')
infile, outfile = args[:2]
Csys.copyfile(infile, outfile, model=infile)
excmd = Csys.popen('/usr/bin/ex - %s' % outfile, 'w')
excmd.write(excmds)
excmd.close()
sys.stderr.write('public key is in >%s<\n' % outfile)