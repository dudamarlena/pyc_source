# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/bill/py3/.virtualenvs/pytest/lib/python2.7/site-packages/Csys/stripcomments.py
# Compiled at: 2005-10-02 14:18:53
import Csys, os, os.path, sys, re
__doc__ = "Remove comments from input\n\nusage: [options] %s\n options:\n\t--nohash\t# don't strip comments starting with ``#''\n\t-C\t\t\t# strip C-style (/* ... */) comments\n\t--Cplusplus\t# strip C++ (//.*) comments\n\t-a|--all\t# strip all comments listed above\n" % Csys.Config.progname
__doc__ += '\n\n$Id: stripcomments.py,v 1.4 2005/10/02 18:18:53 csoftmgr Exp $\n'
__doc__ = Csys.detab(__doc__)
__version__ = '$Revision: 1.4 $'[11:-2]
parser = Csys.getopts(__doc__)
parser.add_option('--nohash', action='store_true', dest='nohash', default=False, help="Don't strip hash comments")
parser.add_option('-C', action='store_true', dest='C', default=False, help='strip C (/*...*/) comments')
parser.add_option('--Cplusplus', action='store_true', dest='Cplusplus', default=False, help='strip C++ (//.*) comments')
parser.add_option('--HTML', action='store_true', dest='HTML', default=False, help='strip HTML comments')
parser.add_option('--SQL', action='store_true', dest='SQL', default=False, help='strip SQL comments')
parser.add_option('-a', '--all', action='store_true', dest='all', default=False, help='strip hash, C, and Cplusplus comments')
options, args = parser.parse_args()
if options.verbose:
    verbose = '-v'
Csys.getoptionsEnvironment(options)
sys.argv[1:] = args
input = []
import fileinput
for line in fileinput.input():
    input.append(line)

print Csys.rmComments(input, hash=not options.nohash, C=options.C, Cplusplus=options.Cplusplus, HTML=options.HTML, SQL=options.SQL, all=options.all)