# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/bill/py3/.virtualenvs/pytest/lib/python2.7/site-packages/Csys/csmain.py
# Compiled at: 2009-11-25 02:49:41
import Csys, os, os.path, sys, re
__doc__ = 'Celestial Software Main program prototype\n\nusage: %s' % Csys.Config.progname
__doc__ += '\n\n$Id: csmain.py,v 1.4 2009/11/25 07:49:41 csoftmgr Exp $\n'
__version__ = '$Revision: 1.4 $'[11:-2]

def main():

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


if __name__ == '__main__':
    main()