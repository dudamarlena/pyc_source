# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/bill/py3/.virtualenvs/pytest/lib/python2.7/site-packages/Csys/undelsend.py
# Compiled at: 2009-11-25 02:59:48
import Csys, os, os.path, sys, re
__doc__ = 'Celestial Software Main program prototype\n\nusage: %s' % Csys.Config.progname
__doc__ += '\n\n$Id: undelsend.py,v 1.2 2009/11/25 07:59:48 csoftmgr Exp $\n'
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
from Csys.MailInternet import MBOX
try:
    undelmail = args[0]
except IndexError:
    undelmail = '/root/Undel.mail'

try:
    size = os.path.getsize(undelmail)
except:
    size = 0

if not size:
    sys.stderr.write('%s is empty or nonexistent\n' % undelmail)
    sys.exit(0)
undelsave = undelmail + '.save'
os.rename(undelmail, undelsave)
mbox = MBOX(undelsave)
sendmail = Csys.Config.sendmail
while True:
    msg = mbox.nextMessage()
    if not msg:
        break
    to = msg.get('X-Original-To')
    msg.delete('X-Original-To')
    msg.delete('X-Delivered')
    msg.delete('Delivered-To')
    msg.delete('Status')
    cmd = '%s %s' % (sendmail, to)
    sys.stderr.write('%s\n' % cmd)
    fh = Csys.popen(cmd, 'w')
    fh.write(str(msg))
    fh.close()