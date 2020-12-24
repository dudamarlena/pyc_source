# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/bill/py3/.virtualenvs/pytest/lib/python2.7/site-packages/Csys/Maildir/imap2maildir.py
# Compiled at: 2007-10-05 20:14:35
import Csys, os, os.path, sys, re
__doc__ = 'Celestial Software Main program prototype\n\nusage: %s' % Csys.Config.progname
__doc__ += '\n\n$Id: imap2maildir.py,v 1.1 2007/10/06 00:14:35 csoftmgr Exp $\n'
__version__ = '$Revision: 1.1 $'[11:-2]

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
import imaplib, Csys.Passwd
from Csys.MailInternet import MailInternet
import Csys.Maildir
_hasChildren = re.compile('HasChildren')
_reFunnyChars = re.compile('[^a-zA-Z0-9.]+')
_INBOX = re.compile('^INBOX\\.{0,1}')
CRLF = re.compile('\\r$', re.MULTILINE)
_namespaceRe = re.compile('\\({1,2}"([^"]*)"\\s+"([^"]*)"\\){1,2}')

class Namespace(Csys.CSClass):
    _attributes = {'prefix': 'INBOX.', 
       'delim': '.'}

    def __init__(self, R):
        Csys.CSClass.__init__(self)
        self.prefix = R.group(1)
        self.delim = R.group(2)


def getNamespaces(conn):
    """Get namespaces from a connection"""
    namespaces = []
    try:
        c, d = conn.namespace()
        print c, d
        if c != 'OK':
            return None
        d = d[0].replace(' NIL ', '')
        while d:
            R = _namespaceRe.search(d)
            if not R:
                break
            namespaces.append(Namespace(R))
            d = d[R.end():]

    except:
        raise

    namespaces = []
    return namespaces


_FolderRe = re.compile('^(\\([^)]+\\))\\s+"(.)"\\s+"(.*)"$')

class Folder(Csys.CSClass):
    """Folderish information"""
    _attributes = {'name': '', 
       'delim': '.', 
       'status': '', 
       'haschildren': False, 
       'name_courier': ''}

    def __init__(self, R):
        """Get parts from regex match"""
        Csys.CSClass.__init__(self)
        self.status = R.group(1)
        if _hasChildren.search(self.status):
            self.haschildren = True
        self.delim = R.group(2)
        self.name = R.group(3)
        name = self._INBOX.sub('', self.name)
        if name:
            parts = []
            for part in self.name.split(self.delim):
                parts.append(self._reFunnyChars.sub('_', part))

            name = ('.').join(parts)
        else:
            name = None
        self.name_courier = name
        return

    def __cmp__(self, other):
        return cmp(self.name, other.name)


def getFolders(conn):
    """Get folders from a connection"""
    c, data = conn.list()
    if c != 'OK':
        return None
    else:
        folders = []
        for d in data:
            R = _FolderRe.search(d)
            if R:
                folders.append(Folder(R))

        return folders


def imap2maildir(conn, user, password, localuser=None):
    """Copy all mail from IMAP server to Maildir
        
        conn is an open connection to the IMAP server.
        user and password are those on the IMAP server.
        localuser is the user on the local system.
        """
    if not localuser:
        localuser = user
    pw = Csys.Passwd.getpwnam(localuser)
    maildir = os.path.join(pw.home, 'Maildir')
    print maildir
    folders = getFolders(conn)
    folders.sort()
    for folder in folders:
        oldfolder = folder.name
        newfolder = folder.name_courier
        sys.stderr.write('oldfolder: %s\n' % oldfolder)
        c, set = conn.select(oldfolder)
        if c != 'OK':
            sys.stderr.write('cannot select %s\n' % oldfolder)
            continue
        c, set = conn.search(None, 'ALL')
        if c != 'OK':
            continue
        mbox = Csys.Maildir.getMaildir(maildir, newfolder, user=pw, dupsok=False)
        msgnumbers = set[0].split()
        for msgnmbr in msgnumbers:
            c, data = conn.fetch(msgnmbr, '(RFC822)')
            if c != 'OK':
                continue
            msg = CRLF.sub('', data[0][1])
            msg = MailInternet(msg)
            mbox.addmsg(msg)

    conn.logout()
    return


cfgFile = os.path.join(Csys.prefix, 'etc/csadmin', 'imap2maildir.conf')
cfg = Csys.ConfigParser(cfgFile)
sections = cfg.sections()
sections.sort()
for section in sections:
    userCfg = cfg.getDict(section, asClass=True)
    user = section + userCfg.suffix
    password = userCfg.password
    localuser = userCfg.localuser or section
    if verbose:
        print user, password, localuser
    server = userCfg.mailhost
    conn = imaplib.IMAP4(server)
    print conn
    curServer = server
    try:
        c, d = conn.login(user, password)
    except:
        c = 'FAIL'

    if c != 'OK':
        sys.stderr.write('imap2maildir: login failed user %s pw >%s<' % (
         user, password))
        continue
    namespaces = getNamespaces(conn)
    if namespaces:
        for namespace in namespaces:
            print namespace.prefix, namespace.delim

        inbox = namespaces[0].prefix
    else:
        inbox = ''
    print 'here'
    if verbose:
        sys.stderr.write('inbox: >%s<\n' % inbox)
    imap2maildir(conn, user, password, localuser)
    conn.logout()