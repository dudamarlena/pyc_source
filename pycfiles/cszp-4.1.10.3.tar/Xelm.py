# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/bill/py3/.virtualenvs/pytest/lib/python2.7/site-packages/Csys/Xelm.py
# Compiled at: 2011-10-05 18:54:46
import Csys, os, os.path, sys, re
__doc__ = 'Celestial Software Main program prototype\n\nusage: %s [options] folder [folder...]' % Csys.Config.progname
__doc__ += "\n\n Options   Argument    Description\n   -c      integer     Column -- moves icon to left\n   -d      directory   cd directory before spawing process.\n   -m      maildir     Maildir (default ~/Maildir)\n   -r                  restart (don't raise flags on mailboxes initially.\n   -t      seconds     Timeout interval (default 60);\n   -w                  Wide screen\n   -x      position    x co-ordinate\n   -y      position    y co-ordinate\n   -v                  Verbose\n\n$Id: Xelm.py,v 1.7 2011/10/05 22:54:46 csoftmgr Exp $\n"
__version__ = '$Revision: 1.7 $'[11:-2]
import pwd
pw = Csys.Passwd.getpwnam(pwd.getpwuid(os.getuid())[0])
USER, HOME = pw.user, pw.home

def setOptions():
    """Set command line options"""
    global __doc__
    parser = Csys.getopts(__doc__)
    parser.add_option('-d', '--directory', action='store', type='string', dest='directory', default=None, help='Change to directory before starting process')
    parser.add_option('-m', '--maildir', action='store', type='string', dest='maildir', default=os.path.join(HOME, 'Maildir'), help='Mailbox file or Maildir directory')
    parser.add_option('-r', '--restart', action='store_true', dest='restart', default=False, help='restart without raising mailbox flags intially')
    parser.add_option('-t', '--timeout', action='store', type='int', dest='timeout', default=60, help='Time in seconds (default 60)')
    return parser


parser = setOptions()
options, args = parser.parse_args()
options.timeout *= 1000
if options.verbose:
    verbose = '-v'
Csys.getoptionsEnvironment(options)
from Csys.SysUtils import which
xterm = which('xterm')
mutt = which('mutt')
stty = which('stty')
xtermargs = [
 '-geometry 80x25+0+0', '-e', mutt, '-f']
import Csys.Maildir, Csys.Passwd, pkg_resources
imagedir = pkg_resources.resource_filename('Csys', 'images')
if not args:
    sys.stderr.write('%s\n' % __doc__)
    sys.stderr.write('No folders specified\n')
    sys.exit(1)
args.sort()
from Tkinter import *
image_new = PhotoImage(file=os.path.join(imagedir, 'mail_new.gif'))
image_old = PhotoImage(file=os.path.join(imagedir, 'mail_none.gif'))
image_use = PhotoImage(file=os.path.join(imagedir, 'mail_mutt.gif'))
top = Tk()
top.iconname('xelm')
top.title('Xelm')

def mycheck(obj):
    obj.chk_mailsize()


class Mailbox(Csys.CSClass):
    _attributes = {'maildir': None, 
       'folder': None, 
       'retryms': 60000, 
       'frame': None, 
       'image': image_old, 
       'button': None, 
       'hasnew': False, 
       'sizechkid': None, 
       'xtermargs': xtermargs[:], 
       'mailsize': 0, 
       'folderdir': None, 
       '_pid': 0}

    def chk_mailsize(self, newimage=None):
        pid = self._pid
        if pid:
            try:
                os.kill(pid, 0)
            except OSError:
                pid = 0

            if pid:
                self.sizechkid = self.button.after(self.retryms, mycheck, self)
            else:
                self._pid = 0
                self.chk_mailsize(image_old)
            return
        if not newimage:
            mailsize = self.mailsize
            newmailsize = self.maildir.newest(mailsize)
            if not newmailsize:
                newimage = image_old
            elif newmailsize > mailsize:
                if self.image != image_new:
                    top.bell()
                newimage = image_new
            self.mailsize = newmailsize
        elif newimage == image_old:
            self.mailsize = self.maildir.newest(self.mailsize)
        if newimage:
            self.image = newimage
        self.button.configure(image=self.image)
        self.sizechkid = self.button.after(self.retryms, mycheck, self)

    def read_email(self):
        """Read email turning off timer"""
        if self._pid:
            top.bell()
            return
        self.image = image_use
        self.button.configure(image=image_use)
        if self.sizechkid:
            self.button.after_cancel(self.sizechkid)
            self.sizechkid = False
        top.update()
        pid = os.fork()
        if not pid:
            os.execl(xterm, *self.xtermargs)
            sys.stderr.write('exec %s failed' % xterm + (' ').join(self.xtermargs))
            sys.exit(1)
        self._pid = pid
        pidMap[pid] = self
        self.sizechkid = self.button.after(self.retryms, mycheck, self)

    def checknew(self):
        """Check for files in new directory"""
        if os.listdir(os.path.join(self.folderdir, 'new')):
            self.hasnew = True
            self.image = image_new
        else:
            self.hasnew = False
            self.image = image_old

    def __init__(self, mailbox, folder, **kwargs):
        Csys.CSClass.__init__(self, **kwargs)
        self.folder = folder
        maildir = self.maildir = Csys.Maildir.getMaildir(mailbox, folder)
        self.folderdir = maildir.folderdir
        self.mailsize = maildir.newest(0)
        self.retryms = int(maildir.xelmretry) * 1000
        self.xtermargs.append(self.folderdir)
        f = self.frame = Frame(top)
        Label(f, text=folder).pack()
        self.checknew()
        button = self.button = Button(f, image=self.image, command=self.read_email)
        button.pack()
        f.pack()
        self.sizechkid = self.button.after(self.retryms, mycheck, self)


import signal
pidMap = {}

def catchSIGCHLD(signo, sigframe):
    if pidMap:
        try:
            pid = os.wait()[0]
        except:
            pid = 0

        if pid:
            for pid, mbox in pidMap.items():
                try:
                    p, s = os.waitpid(pid, os.WNOHANG)
                    exited = os.WIFEXITED(s) or os.WIFSIGNALED(s)
                except OSError:
                    exited = True

                if exited:
                    try:
                        os.kill(pid, 0)
                        pid = 0
                    except OSError:
                        pass

                    if pid:
                        del pidMap[pid]
                        mbox._pid = 0
                        mbox.chk_mailsize(image_old)

    signal.signal(signal.SIGCHLD, catchSIGCHLD)


signal.signal(signal.SIGCHLD, catchSIGCHLD)
for folder in args:
    f = Mailbox(options.maildir, folder)

top.mainloop()