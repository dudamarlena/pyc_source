# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/Editra/src/dev_tool.py
# Compiled at: 2012-12-22 13:45:18
""" Editra Development Tools
Tools and Utilities for debugging and helping with development of Editra.
@summary: Utility function for debugging the editor

"""
__author__ = 'Cody Precord <cprecord@editra.org>'
__svnid__ = '$Id: dev_tool.py 72623 2012-10-06 19:33:06Z CJP $'
__revision__ = '$Revision: 72623 $'
import os, sys, re, traceback, time, urllib2, webbrowser, codecs, locale, wx, ed_glob, ed_msg, eclib
from ebmlib import IsUnicode, LogFile
_ = wx.GetTranslation
RE_LOG_LBL = re.compile('\\[(.+?)\\]')
DEFAULT_ENCODING = locale.getpreferredencoding()
try:
    codecs.lookup(DEFAULT_ENCODING)
except (LookupError, TypeError):
    DEFAULT_ENCODING = 'utf-8'

PYTHONW = 'pythonw' in sys.executable.lower()

def DEBUGP(statement, *args):
    """Prints debug messages and broadcasts them on the log message channel.
    Subscribing a listener with any of the EDMSG_LOG_* types will recieve its
    messages from this method.

      1. Formatting
        - [object/module name][msg_type] message string

      2. Message Type:
        - [err]  : Notes an exception or error condition (high priority)
        - [warn] : Notes a error that is not severe (medium priority)
        - [info] : General information message (normal priority)
        - [evt]  : Event related message (normal priority)

    Example:
      >>> DEBUGP("[ed_main][err] File failed to open")

    @param statement: Should be a formatted string that starts with two
                      identifier blocks. The first is used to indicate the
                      source of the message and is used as the primary means
                      of filtering. The second block is the type of message,
                      this is used to indicate the priority of the message and
                      is used as the secondary means of filtering.

    """
    if len(args):
        try:
            statement = statement % args
        except:
            pass

    lbls = [ lbl.strip() for lbl in RE_LOG_LBL.findall(statement) ]
    info = RE_LOG_LBL.sub('', statement, 2).rstrip()
    if len(lbls) > 1:
        msg = LogMsg(info, lbls[0], lbls[1])
    elif len(lbls) == 1:
        msg = LogMsg(info, lbls[0])
    else:
        msg = LogMsg(info)
    msg_type = msg.Type
    if ed_glob.DEBUG:
        mstr = unicode(msg)
        mstr = mstr.encode('utf-8', 'replace')
        if not PYTHONW:
            print mstr
        logfile = EdLogFile()
        logfile.WriteMessage(mstr)
        if ed_glob.VDEBUG and msg_type in ('err', 'error'):
            traceback.print_exc()
            logfile.WriteMessage(traceback.format_exc())
    if msg_type in ('err', 'error'):
        mtype = ed_msg.EDMSG_LOG_ERROR
        if ed_glob.VDEBUG:
            msg = LogMsg(msg.Value + os.linesep + traceback.format_exc(), msg.Origin, msg.Type)
    elif msg_type in ('warn', 'warning'):
        mtype = ed_msg.EDMSG_LOG_WARN
    elif msg_type in ('evt', 'event'):
        mtype = ed_msg.EDMSG_LOG_EVENT
    elif msg.Type in ('info', 'information'):
        mtype = ed_msg.EDMSG_LOG_INFO
    else:
        mtype = ed_msg.EDMSG_LOG_ALL
    ed_msg.PostMessage(mtype, msg)


class LogMsg(object):
    """LogMsg is a container class for representing log messages. Converting
    it to a string will yield a formatted log message with timestamp. Once a
    message has been displayed once (converted to a string) it is marked as
    being expired.

    """

    def __init__(self, msg, msrc='unknown', level='info'):
        """Create a LogMsg object
        @param msg: the log message string
        @keyword msrc: Source of message
        @keyword level: Priority of the message

        """
        assert isinstance(msg, basestring)
        assert isinstance(msrc, basestring)
        assert isinstance(level, basestring)
        super(LogMsg, self).__init__()
        self._msg = dict(mstr=DecodeString(msg), msrc=DecodeString(msrc), lvl=DecodeString(level), tstamp=time.time())
        self._ok = True

    def __eq__(self, other):
        """Define the equal to operation"""
        return self.TimeStamp == other.TimeStamp

    def __ge__(self, other):
        """Define the greater than or equal to operation"""
        return self.TimeStamp >= other.TimeStamp

    def __gt__(self, other):
        """Define the greater than operation"""
        return self.TimeStamp > other.TimeStamp

    def __le__(self, other):
        """Define the less than or equal to operation"""
        return self.TimeStamp <= other.TimeStamp

    def __lt__(self, other):
        """Define the less than operation"""
        return self.TimeStamp < other.TimeStamp

    def __repr__(self):
        """String representation of the object"""
        return '<LogMsg %s:%d>' % (self._msg['lvl'], self._msg['tstamp'])

    def __str__(self):
        """Returns a nice formatted string version of the message"""
        s_lst = [ '[%s][%s][%s]%s' % (self.ClockTime, self.Origin, self.Type, msg.rstrip()) for msg in self.Value.split('\n') if len(msg.strip())
                ]
        try:
            sys_enc = sys.getfilesystemencoding()
            out = os.linesep.join([ val.encode(sys_enc, 'replace') for val in s_lst
                                  ])
        except UnicodeEncodeError:
            out = repr(self)

        self._ok = False
        return out

    def __unicode__(self):
        """Convert to unicode"""
        rval = ''
        try:
            sval = str(self)
            rval = sval.decode(sys.getfilesystemencoding(), 'replace')
        except UnicodeDecodeError, msg:
            pass

        return rval

    @property
    def ClockTime(self):
        """Formatted timestring of the messages timestamp"""
        ltime = time.localtime(self._msg['tstamp'])
        tstamp = '%s:%s:%s' % (str(ltime[3]).zfill(2),
         str(ltime[4]).zfill(2),
         str(ltime[5]).zfill(2))
        return tstamp

    @property
    def Expired(self):
        """Has this message already been retrieved"""
        return not self._ok

    @property
    def Origin(self):
        """Where the message came from"""
        return self._msg['msrc']

    @property
    def TimeStamp(self):
        """Property for accessing timestamp"""
        return self._msg['tstamp']

    @property
    def Type(self):
        """The messages level type"""
        return self._msg['lvl']

    @property
    def Value(self):
        """Returns the message part of the log string"""
        return self._msg['mstr']


class EdLogFile(LogFile):
    """Transient log file object"""

    def __init__(self):
        super(EdLogFile, self).__init__('editra')

    def PurgeOldLogs(self, days):
        try:
            super(EdLogFile, self).PurgeOldLogs(days)
        except OSError, msg:
            DEBUGP('[dev_tool][err] PurgeOldLogs: %s' % msg)


def DecodeString(string, encoding=None):
    """Decode the given string to Unicode using the provided
    encoding or the DEFAULT_ENCODING if None is provided.
    @param string: string to decode
    @keyword encoding: encoding to decode string with

    """
    if encoding is None:
        encoding = DEFAULT_ENCODING
    if not IsUnicode(string):
        try:
            rtxt = codecs.getdecoder(encoding)(string)[0]
        except Exception, msg:
            rtxt = string

        return rtxt
    else:
        return string
        return


class EdErrorDialog(eclib.ErrorDialog):
    """Error reporter dialog"""

    def __init__(self, msg):
        super(EdErrorDialog, self).__init__(None, title='Error Report', message=msg)
        self.SetDescriptionLabel(_('Error: Something unexpected hapend\nHelp improve Editra by clicking on Report Error\nto send the Error Traceback shown below.'))
        return

    def Abort(self):
        """Abort the application"""
        wx.CallLater(500, wx.GetApp().OnExit, wx.MenuEvent(wx.wxEVT_MENU_OPEN, ed_glob.ID_EXIT), True)

    def GetProgramName(self):
        """Get the program name to display in error report"""
        return '%s Version: %s' % (ed_glob.PROG_NAME, ed_glob.VERSION)

    def Send(self):
        """Send the error report"""
        msg = 'mailto:%s?subject=Error Report&body=%s'
        addr = 'bugs@%s' % ed_glob.HOME_PAGE.replace('http://', '', 1)
        if wx.Platform != '__WXMAC__':
            body = urllib2.quote(self.err_msg)
        else:
            body = self.err_msg
        msg = msg % (addr, body)
        msg = msg.replace("'", '')
        webbrowser.open(msg)


def ExceptionHook(exctype, value, trace):
    """Handler for all unhandled exceptions
    @param exctype: Exception Type
    @param value: Error Value
    @param trace: Trace back info

    """
    exc = traceback.format_exception(exctype, value, trace)
    exc.insert(0, '*** %s ***%s' % (eclib.TimeStamp(), os.linesep))
    ftrace = ('').join(exc)
    print ftrace
    if EdErrorDialog.ABORT:
        os._exit(1)
    if not EdErrorDialog.REPORTER_ACTIVE and not EdErrorDialog.ABORT:
        dlg = EdErrorDialog(ftrace)
        dlg.ShowModal()
        dlg.Destroy()