# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/bill/py3/.virtualenvs/pytest/lib/python2.7/site-packages/Csys/tw.djbdns_files.py
# Compiled at: 2009-11-24 20:44:53
import Csys, os, os.path, sys, re
__doc__ = 'Create ignore files for daemontools variables.\n\nusage: %s' % Csys.Config.progname
__doc__ += '\n\n$Id: tw.djbdns_files.py,v 1.1 2009/11/25 01:44:53 csoftmgr Exp $\n'
__version__ = '$Revision: 1.1 $'[11:-2]
if __name__ == '__main__':

    def setOptions():
        """Set command line options"""
        global __doc__
        parser = Csys.getopts(__doc__)
        return parser


    parser = setOptions()
    options, args = parser.parse_args()
    verbose = ''
    if options.verbose:
        verbose = '-v'
        sys.stdout = sys.stderr
    Csys.getoptionsEnvironment(options)
    from glob import glob
    file = os.path.join(Csys.prefix, 'var/tripwire', os.path.splitext(Csys.Config.progname)[0])
    paths = (
     ('/service/*/log', '=%s R'),
     ('/service/*/supervise', '=%s R'),
     ('/service/*/root/data*', '%s L'),
     ('/service/*/root/servers/*', '%s R'))
    output = []
    for pat, fmt in paths:
        output.extend([ fmt % os.path.realpath(p) for p in glob(pat) ])

    open(file, 'w').write('%s\n' % ('\n').join(output))