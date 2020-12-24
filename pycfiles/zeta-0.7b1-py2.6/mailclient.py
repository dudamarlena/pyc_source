# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/zeta/lib/mailclient.py
# Compiled at: 2010-07-05 04:40:49
"""SMTP Client to send mails.

config parameters used,
    zeta.smtp_serverip,
    zeta.smtp_user,
    zeta.smtp_password,
from .ini file to login into SMTP server.

* Class methods provided to interface with mail server mysql tables.
  * Configuration for mail server mysql should be provided via,
        zeta.smtpmysql.*
  * For every virtual domains hosted by the server, an virtual domain entry
    should be present.
  * Every project will have mail account, as a virtual user of the format,
        projectname@hostname
    password will be same as what is given in `zeta.smtp_password` 

* Sender ID from each project will be construted using the domain name given
  in zeta.smtp_user as hostname.

Mails are sent for,
    * Inviting users
    * Sending urls for resetting forgotten password
    * Notifications on timeline logs

"""
from __future__ import with_statement
import time, email, smtplib, poplib
from os.path import basename
import datetime as dt, mimetypes, re
try:
    from email import encoders
    from email.header import make_header
    from email.message import Message
    from email.mime.audio import MIMEAudio
    from email.mime.base import MIMEBase
    from email.mime.image import MIMEImage
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
except ImportError:
    from email import Encoders as encoders
    from email.Header import make_header
    from email.MIMEMessage import Message
    from email.MIMEAudio import MIMEAudio
    from email.MIMEBase import MIMEBase
    from email.MIMEImage import MIMEImage
    from email.MIMEMultipart import MIMEMultipart
    from email.MIMEText import MIMEText

from pylons import config
from sqlalchemy import engine_from_config, Table, Column, MetaData, ForeignKey, select, Unicode
from sqlalchemy.orm import sessionmaker, mapper, scoped_session, relation, backref, deferred
import zeta.lib.helpers as h
from zeta.lib.error import *

def fetchconfig():
    serverip = h.fromconfig('zeta.smtp_serverip')
    login = h.fromconfig('zeta.smtp_user')
    password = h.fromconfig('zeta.smtp_password')
    return (serverip, login, password)


def projectemail(projectname):
    """Construct email-id for project"""
    (_d1, login, _d2) = fetchconfig()
    hostname = login.split('@')[(-1)]
    emailid = '%s@%s' % (projectname, hostname)
    return emailid


def mime_attachfname(header):
    """compose / retrieve attachment filename"""
    m = re.match('filename="(.*)"', header)
    tups = m.groups()
    return tups and tups[0] or ''


class OutMessage(object):
    """Represents an outgoing message via SMTP, attributes used to send a
    message are,
        to
        from
        subject
        body
    """

    def __init__(self, fromaddr=None, toaddrs=[], ccaddrs=[], subject='', body='', attachments=[], charset='utf8'):
        """Create an outgoing message"""
        if not isinstance(attachments, list):
            attachments = [
             attachments]
        if not isinstance(toaddrs, list):
            toaddrs = [
             toaddrs]
        if not isinstance(ccaddrs, list):
            ccaddrs = [
             ccaddrs]
        self.fromaddr = fromaddr
        self.toaddrs = toaddrs
        self.ccaddrs = ccaddrs
        self.subject = subject
        self.body = body
        self.attachments = [ (a, None) for a in attachments ]
        self.charset = charset
        return

    def as_string(self):
        """Format the message for sending"""
        return self.attachments and self._multiparts() or self._plaintext()

    def attach(self, filename):
        """Attach a file to the message object"""
        self.attachments.append((filename, None))
        return

    def _stuffmsg(self, msg):
        """Stuff message with message attributes,
            from, to, subject ...
        """
        subject = unicode(self.subject, self.charset)
        msg['Subject'] = str(make_header([(subject, self.charset)]))
        msg['From'] = self.fromaddr
        msg['To'] = (', ').join(self.toaddrs)
        msg['Cc'] = (', ').join(self.ccaddrs)
        return msg

    def _plaintext(self):
        """Convert the message into plain text"""
        msg = MIMEText(self.body, 'plain', self.charset)
        return self._stuffmsg(msg).as_string()

    def _multiparts(self):
        """Convert the message when message has attachments"""
        mainmsg = MIMEMultipart('related')
        mainmsg.attach(MIMEText(self.body, 'plain', self.charset))
        self._stuffmsg(mainmsg)
        mainmsg.preamble = self.subject
        for (fname, cid) in self.attachments:
            (ctype, encoding) = mimetypes.guess_type(fname)
            if ctype is None or encoding is not None:
                ctype = 'application/octet-stream'
            (maintype, subtype) = ctype.split('/', 1)
            fd = open(fname, 'rb')
            if maintype == 'text':
                msg = MIMEText(fd.read(), _subtype=subtype)
            elif maintype == 'image':
                msg = MIMEImage(fd.read(), _subtype=subtype)
            elif maintype == 'audio':
                msg = MIMEAudio(fd.read(), _subtype=subtype)
            else:
                msg = MIMEBase(maintype, subtype)
                msg.set_payload(fd.read())
                encoders.encode_base64(msg)
            fd.close()
            if cid:
                msg.add_header('Content-ID', '<%s>' % cid)
                msg.add_header('Content-Disposition', 'inline')
            else:
                msg.add_header('Content-Disposition', 'attachment', filename=basename(fname))
            mainmsg.attach(msg)

        return mainmsg.as_string()


class SMTPconn(object):
    """Create SMTP connection object based on application configuration"""

    def __init__(self, serverip=None, login=None, password=None):
        (c_serverip, c_login, c_password) = fetchconfig()
        self.serverip = serverip or c_serverip
        self.login = login or c_login
        self.password = password or c_password
        self.srvr = None
        return

    def connect(self):
        """Connect to the server. Don't forget to call quit() !"""
        if self.serverip and self.login and self.password:
            self.srvr = smtplib.SMTP(self.serverip)
            (rc, msg) = self.srvr.login(self.login, self.password)
            if rc != 235 or 'successful' not in msg:
                raise ZetaSMTPError('Unable to login to SMTP server `%s` \n %s ' % (
                 self.serverip, (rc, msg)))
        return self.srvr

    def sendmail(self, fromaddr, toaddrs, ccaddrs=[], subject='', body='', attachments=[]):
        """Send e-mail using OutMessage() instance"""
        if self.srvr == None:
            raise ZetaSMTPError('First, connect to the server')
        if isinstance(toaddrs, (str, unicode)):
            toaddrs = [
             toaddrs]
        if isinstance(ccaddrs, (str, unicode)):
            ccaddrs = [
             ccaddrs]
        fromaddr = fromaddr or self.login
        msg = OutMessage(fromaddr=fromaddr, toaddrs=toaddrs, ccaddrs=ccaddrs, subject=subject, body=body, attachments=attachments)
        rc = self.srvr.sendmail(fromaddr, toaddrs, msg.as_string())
        return rc

    def sendmsg(self, fromaddr, toaddrs, msg):
        """Send e-mail message"""
        if self.srvr == None:
            raise ZetaSMTPError('First, connect to the server')
        if isinstance(toaddrs, (str, unicode)):
            toaddrs = [
             toaddrs]
        fromaddr = fromaddr or self.login
        rc = self.srvr.sendmail(fromaddr, toaddrs, msg)
        return rc

    def quit(self):
        """Close connection"""
        if self.srvr == None:
            raise ZetaSMTPError('First, connect to the server')
        self.srvr.quit()
        self.srvr = None
        return


class InMessage(object):
    """Class to construct incoming messages, handles plain-text messages and
    plain-text messages with attachments,
        if self.multipart == True,
            self.rootpart, specifies the root part.
            self.messages, list of plain-text parts
            self.attachments, list of attachment parts"""

    def __init__(self, msg):
        self.m = email.message_from_string(('\n').join([ i for i in msg[1] ]))
        self.multipart = self.m.is_multipart()
        self.rootpart = None
        self.messages = []
        self.attachments = []
        if self.multipart:
            (self.rootpart, self.messages, self.attachments) = self._travelparts(self.m)
        return

    def _travelparts(self, m):
        rootpart = None
        messages = []
        attachments = []
        for part in m.walk():
            ctype = part.get_content_type()
            mtype = part.get_content_maintype()
            cdisp = part.get('Content-Disposition')
            if mtype == 'multipart' and rootpart == None:
                rootpart = part
                continue
            elif ctype == 'text/plain':
                messages.append(part)
            elif cdisp and 'attachment' in cdisp:
                attachments.append(part)

        return (
         rootpart, messages, attachments)


class POPconn(object):
    """Create POP3 connection object based on application configuration"""

    def __init__(self, serverip=None, login=None, password=None):
        (c_serverip, c_login, c_password) = fetchconfig()
        self.serverip = serverip or c_serverip
        self.login = login or c_login
        self.password = password or c_password
        self.srvr = None
        return

    def connect(self):
        """Connect to the server"""
        if self.serverip and self.login and self.password:
            self.srvr = poplib.POP3(self.serverip)
            try:
                self.srvr.user(self.login)
                self.srvr.pass_(self.password)
            except:
                raise
                raise ZetaPOP3Error('Unable to login to POP3 server `%s`' % self.serverip)

        return self.srvr

    def newm(self, offset):
        """Retrieve only new mails from the mail box,
        Returns, list of tuples,
            [ ( msgno, InMessage()), (..., ...), ... ]"""
        (n, size) = self.stat()
        inmails = []
        [ inmails.append((i, self.retr(i))) for i in range(offset + 1, n + 1) ]
        return inmails

    def allm(self):
        """Retrieve only new mails from the mail box,
        Returns, list of tuples,
            [ ( msgno, InMessage()), (..., ...), ... ]"""
        (n, size) = self.stat()
        inmails = []
        [ inmails.append(self.retr(i)) for i in range(1, n + 1) ]
        return inmails

    def stat(self):
        """Get mailbox status. The result is a tuple of 2 integers:
                (message count, mailbox size).
        """
        if self.srvr == None:
            raise ZetaPOP3Error('First, connect to the server')
        return self.srvr.stat()

    def list(self, which=[]):
        """Request message list, result is in the form 
                ( response, [ 'mesg_num octets', ...], octets ).
        If which is set, it is the message to list."""
        if self.srvr == None:
            raise ZetaPOP3Error('First, connect to the server')
        return which and self.srvr.list(which) or self.srvr.list()

    def retr(self, which):
        """Retrieve whole message number `which`, and set its seen flag.
        Result is in form,
            ( response, [ 'line', ...], octets )."""
        if self.srvr == None:
            raise ZetaPOP3Error('First, connect to the server')
        msg = self.srvr.retr(which)
        if msg[0][:3] != '+OK':
            raise ZetaPOP3Error(msg[0])
        im = InMessage(msg)
        return im

    def dele(self, which):
        """Flag message number `which` for deletion. On most servers deletions
        are not actually performed until QUIT"""
        if self.srvr == None:
            raise ZetaPOP3Error('First, connect to the server')
        return self.srvr.dele(which)

    def rset(self):
        """Remove any deletion marks for the mailbox."""
        if self.srvr == None:
            raise ZetaPOP3Error('First, connect to the server')
        return self.srvr.rset()

    def fetchmail(self, fromwhich=None, count=None, delete=None):
        """Recieve e-mail,
        fetch just the latest mail, or all the mails from `fromwhich` to
        latest mail"""
        if self.srvr == None:
            raise ZetaPOP3Error('First, connect to the server')
        inmails = []
        (mcount, size) = self.stat()
        start = fromwhich or count and mcount - count + 1 or mcount
        end = start + count if count and start + count < mcount else mcount + 1
        [ inmails.append(self.retr(i)) for i in range(start, end) if i > 0 ]
        delete and [ self.dele(i) for i in range(start, end) if i > 0 ]
        return inmails

    def quit(self):
        """Close connection"""
        if self.srvr == None:
            raise ZetaPOP3Error('First, connect to the server')
        self.srvr.quit()
        self.srvr = None
        return


class MailDB(object):
    """Class to manage mysql based configuration for mail server,
        * Add / Delete / List virtual domains
        * Add / Delete / List virtual users
    """

    def __init__(self, config, prefix='zeta.smtpmysql.'):
        """Instantiate a connection to DB"""
        try:
            self.metadata = MetaData()
            self.engine = engine_from_config(config, prefix)
            self.sm = sessionmaker(autoflush=True, autocommit=True, bind=self.engine)
            self.Session = scoped_session(self.sm)
            self.t_maildomains = Table('domains', self.metadata, Column('domain', Unicode(50), primary_key=True), mysql_engine='InnoDB')
            self.t_mailusers = Table('users', self.metadata, Column('email', Unicode(80), primary_key=True), Column('password', Unicode(20)), mysql_engine='InnoDB')
        except:
            self.Session = None

        return

    def adddomains(self, domainnames):
        """Add virtual mail domains `domainnames`"""
        if self.Session:
            if isinstance(domainnames, (str, unicode)):
                domainnames = [
                 domainnames]
            msession = self.Session()
            with msession.begin(subtransactions=True):
                for domain in domainnames:
                    stmt = self.t_maildomains.insert(bind=self.engine)
                    stmt.execute(domain=unicode(domain))

    def deldomains(self, domainnames):
        """Delete virtual mail domains `domainnames`"""
        if self.Session:
            if isinstance(domainnames, (str, unicode)):
                domainnames = [
                 domainnames]
            msession = self.Session()
            with msession.begin(subtransactions=True):
                for domain in domainnames:
                    stmt = self.t_maildomains.delete(bind=self.engine).where(self.t_maildomains.c.domain == unicode(domain))
                    stmt.execute()

    def listdomains(self):
        """List virtual mail domains"""
        if self.Session:
            q = select([self.t_maildomains.c.domain], bind=self.engine)
            return [ dom[0] for dom in q.execute().fetchall() ]
        else:
            return []

    def adduser(self, email, password):
        """Add virtual mail user (email, password)"""
        if self.Session:
            msession = self.Session()
            with msession.begin(subtransactions=True):
                stmt = self.t_mailusers.insert(bind=self.engine)
                stmt.execute(email=unicode(email), password=unicode(password))
            sconn = SMTPconn(login=email, password=password)
            sconn.connect()
            sconn.sendmail(sconn.login, email, subject='Test message', body='')
            sconn.quit()
            time.sleep(1)
            pconn = POPconn(login=email, password=password)
            pconn.connect()
            (mcount, size) = pconn.stat()
            [ pconn.dele(i) for i in range(1, mcount + 1) ]
            pconn.quit()

    def deluser(self, email):
        """Delete virtual mail user `email`"""
        if self.Session:
            msession = self.Session()
            with msession.begin(subtransactions=True):
                stmt = self.t_mailusers.delete(bind=self.engine).where(self.t_mailusers.c.email == unicode(email))
                stmt.execute()

    def listusers(self):
        """List virtual mail user `email`"""
        if self.Session:
            q = select([self.t_mailusers.c.email,
             self.t_mailusers.c.password], bind=self.engine)
            return q.execute().fetchall()
        else:
            return []


def pmailaccount(projectname, _config=None):
    """Generate email account for `projectname`"""
    mdb = MailDB(_config or config)
    if mdb.Session:
        emails = [ u[0] for u in mdb.listusers() ]
        plogin = projectemail(projectname)
        if plogin in emails:
            return ''
        (s, u, p) = fetchconfig()
        mdb.adduser(plogin, p)
        return plogin
    else:
        return ''


inv_subjecttmpl = 'Invitation to join `%s`'
inv_msgtmpl = '\nYou are being invited to join the project collobaration site `%s`.\nIf you are willing to accept it please click the below link and\nproceed with your registration, else, kindly ignore this mail\n    %s \n\n%s\n'

def inviteuser(toaddrs, url, byuser, sitename=''):
    """Send an invitation mail to user `toaddrs` (emailid) with `subject` and
    `body`. `byuser` is informational.
    E-mail is send via site's SMTP profile
    """
    if isinstance(toaddrs, (str, unicode)):
        toaddrs = [
         toaddrs]
    cname = h.user2canonical(byuser)
    conn = SMTPconn()
    conn.connect()
    subject = str(inv_subjecttmpl % sitename)
    body = str(inv_msgtmpl % (sitename, url, '- %s' % cname))
    msg = OutMessage(fromaddr=conn.login, toaddrs=toaddrs, subject=subject, body=body)
    rc = conn.sendmsg(conn.login, toaddrs, msg.as_string())
    conn.quit()
    return rc


rtp_subjecttmpl = 'Reset your password @ %s'
rtp_msgtmpl = '\nYou have made a request to reset you password, if so, please click the below\nlink and continue with the process, else, kindly ignore this mail\n    %s \n\n%s\n'

def resetpasswd(toaddrs, url, sitename=''):
    """Administrator sends email to user id, providing the person with `url`
    to reset their password.
    E-mail is send via site's SMTP profile"""
    if isinstance(toaddrs, (str, unicode)):
        toaddrs = [
         toaddrs]
    conn = SMTPconn()
    conn.connect()
    subject = str(rtp_subjecttmpl % sitename)
    body = str(rtp_msgtmpl % (url, '- Site Administrator'))
    msg = OutMessage(fromaddr=conn.login, toaddrs=toaddrs, subject=subject, body=body)
    rc = conn.sendmsg(conn.login, toaddrs, msg.as_string())
    conn.quit()
    return rc