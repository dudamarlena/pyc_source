# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/bill/py3/.virtualenvs/pytest/lib/python2.7/site-packages/Csys/deliver_post.py
# Compiled at: 2011-10-05 19:04:53
import Csys, os, os.path, sys, re
__doc__ = 'Celestial Software Main program prototype\n\nusage: %s username' % Csys.Config.progname
__doc__ += "\n\nThis is a deliver.post program for the deliver system that puts\nuser's messages into their $HOME/Maildir mailboxes, or may put\nthem in other mailboxes depending on patterns in their\n$HOME/Maildir.rules file, or another file specified in the\n/csoft/etc/csbase/Maildir.conf file using the ``mailrules''\noption in the DEFAULT section.\n\n$Id: deliver_post.py,v 1.4 2011/10/05 23:04:53 csoftmgr Exp $\n"
__version__ = '$Revision: 1.4 $'[11:-2]
parser = Csys.getopts(__doc__)
options, args = parser.parse_args()
if options.verbose:
    verbose = '-v'
Csys.getoptionsEnvironment(options)
import Csys, Csys.Maildir, Csys.MailInternet, Csys.Passwd
from cStringIO import StringIO
from Csys.Netparams import set_do_dnsname
set_do_dnsname(False)
import time
ctime = time.ctime(time.time())
localErrors = [
 ctime]
sys.stdout = stdout = StringIO()
try:
    user = args[0]
except:
    localErrors.append('User argument missing')
    raise

try:
    pw = Csys.Passwd.getpwnam(user)
except:
    localErrors.append('Password failed %s' % user)
    raise

maildir = Csys.Maildir.getMaildir(os.path.join(pw.home, 'Maildir'), None, user=pw)
if maildir.debug:
    maildir.pushDebug('User: %s' % pw.user)
envFields = ('HEADER', 'BODY')
msg = Csys.MailInternet.MailInternet(*Csys.getSlice(envFields, os.environ))
if not msg.get('X-Csys-Originating-IP'):
    received = msg.firstReceived()
    if received:
        msg.replace('X-Csys-Originating-IP', received.ip)
if len(localErrors) > 1:
    fh = open('/tmp/deliver.global', 'a')
    fh.write('%s\n' % ('\n\t').join(localErrors))
    fh.close()
try:
    maildir.checkRules(msg, True)
except Csys.Maildir.DropMessage as err:
    if maildir.debug:
        maildir.pushDebug('dropped mailbox %s %s' % (err.mailbox, err.msg))

stdout.seek(0)
stdoutlines = stdout.readlines()
if maildir.debug:
    debugfile = '/tmp/deliver.%s' % user
    debugOut = Csys.Maildir.Maildir.debugOut + stdoutlines
    if stdoutlines:
        stdoutlines.insert(0, 'standard output')
    fh = open(debugfile, 'a')
    fh.write('%s\n' % ('\n\t').join(debugOut))
    fh.close()
sys.stdout = sys.__stdout__
print 'DROP'