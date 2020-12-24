# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/bill/py3/.virtualenvs/pytest/lib/python2.7/site-packages/Csys/Maildir/mbox2maildir.py
# Compiled at: 2009-11-24 21:03:48
import Csys, os, os.path, sys, re
__doc__ = 'Celestial Software Main program prototype\n\nusage: %s' % Csys.Config.progname
__doc__ += '\n\n$Id: mbox2maildir.py,v 1.4 2009/11/25 02:03:48 csoftmgr Exp $\n'
__version__ = '$Revision: 1.4 $'[11:-2]
from Csys.Passwd import getpwnam, read_passwd_shadow
import pwd
pw = getpwnam(pwd.getpwuid(os.getuid())[0])
USER, HOME = pw.user, pw.home
defmaildir = '/var/spool/mail'

def setOptions():
    """Set command line options"""
    global __doc__
    parser = Csys.getopts(__doc__)
    parser.add_option('-a', '--all', action='store_true', dest='all', default=False, help='Convert all non-admin users on system')
    parser.add_option('--hostname', action='store', type='string', dest='hostname', default=None, help='Get mailbox from hostname with ssh')
    parser.add_option('-d', '--dupsok', action='store_true', dest='dupsok', default=False, help='Duplicates OK')
    parser.add_option('-f', '--filename', action='store', type='string', dest='filename', default=None, help='Get mailbox from hostname with ssh')
    parser.add_option('-l', '--lastdupbody', action='store_true', dest='lastdupbody', default=False, help='Keep only last duplicate body')
    parser.add_option('-m', '--nodupbody', action='store_true', dest='nodupbody', default=False, help='Keep only last duplicate body')
    parser.add_option('-u', '--user', action='append', type='string', dest='user', default=[], help='Username to convert')
    parser.add_option('--folder', action='store', type='string', dest='folder', default=None, help='Store in Maildir folder')
    return parser


parser = setOptions()
options, args = parser.parse_args()
if options.verbose:
    verbose = '-v'
else:
    verbose = ''
Csys.getoptionsEnvironment(options)
kwargs = {'dupsok': options.dupsok, 
   'nodupbody': options.nodupbody, 
   'lastdupbody': options.lastdupbody}
if options.all:
    users = {}
    accts = read_passwd_shadow()
    for user, pw in accts.accts.items():
        if not pw.is_admin:
            users[user] = pw

    users = users.values()
    users.sort()
    options.user = users
    MAIL = ''
    Maildir = ''
else:
    if not options.user:
        options.user.append(USER)
    user = options.user[0] = getpwnam(options.user[0])
    MAIL = os.environ.get('MAIL')
import Csys.MailInternet, Csys.Maildir
from Csys.Netparams import set_do_dnsname
set_do_dnsname(False)
folder = options.folder
if verbose:
    sys.stderr.write('folder: %s\n' % folder)
for user in options.user:
    if verbose:
        sys.stderr.write('user >%s<\n' % user.user)
    HOME = user.home
    donefile = os.path.join(HOME, 'mdirconvertdone')
    if os.path.isfile(donefile):
        continue
    if options.filename:
        filename = options.filename
        options.filename = ''
    else:
        if MAIL:
            filename = MAIL
        else:
            filename = os.path.join(defmaildir, user.user)
        if args:
            Maildir = args.pop(0)
        else:
            Maildir = os.path.join(user.home, 'Maildir')
        kwargs['user'] = user
        if options.hostname:
            filename = Csys.popen('ssh -h %s cat %s' % (options.hostname, filename))
        mbox = Csys.MailInternet.MBOX(filename)
        NR = 0
        while True:
            msg = mbox.nextMessage()
            if msg is None:
                break
            if not NR % 500:
                if verbose:
                    sys.stderr.write('\nResetting %s\n' % Maildir)
                Csys.Maildir.clearMaildirs()
                maildir = Csys.Maildir.getMaildir(Maildir, folder, **kwargs)
            NR += 1
            if not NR % 10:
                sys.stderr.write('.')
            try:
                fileobj = maildir.checkRules(msg, True)
            except Csys.Maildir.DropMessage as err:
                sys.stderr.write('\ndropped mailbox %s %s\n' % (err.mailbox, err.msg))
            except:
                sys.stderr.write('\nunknown error -- probably truncated file\n')

    if NR >= 10:
        sys.stderr.write('\n')