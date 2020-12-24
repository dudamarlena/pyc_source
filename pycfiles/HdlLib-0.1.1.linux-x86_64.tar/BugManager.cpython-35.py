# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.5/dist-packages/HdlLib/Utilities/BugManager.py
# Compiled at: 2017-07-08 08:29:58
# Size of source mod 2**32: 5056 bytes
try:
    from gi.repository import Gtk, GLib, Pango
except ImportError:
    import gtk as Gtk, glib as GLib, pango as Pango

import os, sys, tempfile, traceback, logging, smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
import datetime, getpass
sys.path.append(os.path.abspath('./Threads'))
import Threads
LogFile = os.path.expanduser(os.path.join('~/', '{0}.log'.format(sys.argv[0].split('.')[0])))
GUI = None
SendMail = False

def SetVersion(Version):
    """
        Activate mail sending according to version.
        """
    if Version.upper().startswith('RD') or Version.lower().startswith('test'):
        SendMail = True
    else:
        SendMail = False


def BugTracking(Function, Msg='\nRuntime error has been encountered.\nWe sincerely apologize. Please let us know.'):
    """
        Decorator for Runtime bug of generic functions.
        """

    def BugTrack(*args, **kwargs):
        global GUI
        try:
            Result = Function(*args, **kwargs)
            return Result
        except:
            Traceback = ''
            for Line in traceback.format_exc(12):
                Traceback += Line

            logging.critical(Traceback)
            print(Msg)
            if GUI:
                if SendMail and GUI.popup('RUNTIME ERROR', 'A runtime error has been encountered.\nWe sincerely apologize. Would you like to send us the bug report (screenshot+log)?', 'question') == Gtk.ResponseType.YES:
                    Threads.LaunchAsThread(Name='Send_bug_report', Function=SendBug, ArgList=[Traceback])
                    logging.debug("Thread launched: 'Send_bug_report'")
            else:
                GUI.popup('RUNTIME ERROR', 'A runtime error has been encountered.\nWe sincerely apologize. Please let us know.', 'error')

    return BugTrack


def ScreenShot(Title='Screenshot_a_gui', FolderPath='./'):
    format = 'png'
    width = gtk.gdk.screen_width()
    height = gtk.gdk.screen_height()
    print('Taking screenshot...')
    sys.stdout.flush()
    screenshot = gtk.gdk.Pixbuf.get_from_drawable(gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, True, 8, width, height), gtk.gdk.get_default_root_window(), gtk.gdk.colormap_get_system(), 0, 0, 0, 0, width, height)
    FileName = os.path.join(FolderPath, Title + '.' + format)
    screenshot.save(FileName, format, {})
    return FileName


def SendBug(Msg):
    JoinImg, JoinLog = CreateReport(Info=Msg)
    SERVER = 'core.adacsys.com'
    FROM = 'matthieu.payet@free.fr'
    TO = ['matthieu.payet@free.fr', 'redmine.internal@adacsys.com']
    SUBJECT = 'AUTOMATIC BUG REPORT: {0}'.format(Msg.split('\n')[(-2)])
    Message = MIMEMultipart()
    Message['Subject'] = SUBJECT
    Message['From'] = FROM
    Message['To'] = ', '.join(TO)
    Message.attach(MIMEText('Project: YANGO '))
    Message.attach(MIMEText('Tracker: Bug '))
    Message.attach(MIMEText('Status: New '))
    Message.attach(MIMEText('Priority: Normal \n'))
    if JoinImg:
        with open(JoinImg, 'rb') as (IMGFILE):
            Image = MIMEImage(IMGFILE.read())
        Image.add_header('Content-Disposition', 'attachment', filename=os.path.basename(JoinImg))
        Message.attach(Image)
    Message.preamble = 'This message was automaticaly generated.'
    if JoinLog:
        with open(JoinLog, 'rb') as (TRACEFILE):
            Log = MIMEApplication(TRACEFILE.read())
        Log.add_header('Content-Disposition', 'attachment', filename=os.path.basename(JoinLog))
        Message.attach(Log)
    if LogFile:
        with open(os.path.abspath(LogFile), 'rb') as (LOGFILE):
            Log = MIMEApplication(LOGFILE.read())
            Log.add_header('Content-Disposition', 'attachment', filename=os.path.basename(LogFile))
            Message.attach(Log)
    Message.attach(MIMEText(Msg))
    server = smtplib.SMTP(SERVER)
    server.sendmail(FROM, TO, Message.as_string())
    server.quit()


def CreateReport(Info):
    TempPath = tempfile.mkdtemp()
    FileName = 'bug_a_gui_{0}_{1}'.format(getpass.getuser(), datetime.datetime.now())
    FileName = FileName.replace(' ', '_')
    FileName = FileName.replace(':', '.')
    LogPath = os.path.join(TempPath, FileName + 'log.txt')
    with open(LogPath, 'w+') as (TEXTFILE):
        TEXTFILE.write(Info)
    ImgPath = ScreenShot(Title=FileName, FolderPath=TempPath)
    return (
     ImgPath, LogPath)