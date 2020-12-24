# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Library/Frameworks/Python.framework/Versions/2.6/lib/python2.6/site-packages/ponyexpress/core.py
# Compiled at: 2011-06-02 17:21:29
__doc__ = '\nCore PonyExpress Class\n'
import smtplib
from string import Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime, couch, json

class PonyExpressException(Exception):
    """
        Handle exceptions, log the error and
        message to couchdb so it can be reported
        and resent later
        """

    def __init__(self, pony, type, error):
        log = couch.PonyExpressError(date=datetime.datetime.now(), type=type, exception=str(error), template_id=pony._id, pony_json=pony.to_dict())
        log.save()


class PonyExpress(object):
    """fallback language to use when the requested language is unavailable"""
    _lang = 'en'
    _sender_name = 'nobody'
    _sender_address = 'nobody@localhost'
    _recipient_name = None
    _recipient_address = None
    _smpt_connection = None
    _recipients = None
    _smtp_connection = None
    _id = None
    _template = None
    _tags = None
    _replacements = None
    _message_doc = None

    def __init__(self, id, recipient_name=None, recipient_address=None, sender_name=None, sender_address=None, tags=None, replacements=None, **kwargs):
        """get the template"""
        self._id = id
        self._recipient_name = recipient_name
        self._recipient_address = recipient_address
        assert self._id, 'No Template ID Passed'
        assert self._recipient_address, 'No Recipient Address Passed'
        assert self._recipient_name, 'No Recipient Name Passed'
        self._sender_name = sender_name or self._sender_name
        self._sender_address = sender_address or self._sender_address
        self._tags = tags or []
        self._replacements = replacements or {}

    def to_json(self):
        """
                Encode the JSON dict to be passed around
                """
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, encoded_json, **kwargs):
        """
                Setup a PonyExpress object usting encoded JSON 
                """
        decoded_json = json.loads(encoded_json)
        return cls.from_dict(decoded_json, **kwargs)

    def to_dict(self):
        """
                Encode the JSON dict to be passed around
                """
        params = dict(id=self._id, recipient_name=self._recipient_name, recipient_address=self._recipient_address)
        if self._sender_name:
            params.update(sender_name=self._sender_name)
        if self._sender_address:
            params.update(sender_address=self._sender_address)
        if self._tags:
            params.update(tags=self._tags)
        if self._replacements:
            params.update(replacements=self._replacements)
        return params

    @classmethod
    def from_dict(cls, decoded_json, **kwargs):
        """
                Setup a PonyExpress object using a dict of values
                """
        dict = {}
        for (k, v) in decoded_json.iteritems():
            dict[str(k)] = v

        return cls(**dict)

    def to_couchdb(self, status='queued', save=True, config=None):
        """
                Create a PonyExpressMessage document for couchdb logging or queue.
                """
        self._message_doc = couch.PonyExpressMessage(status=status, date=datetime.datetime.now(), template=self._id, lang=self._lang, sender_address=self._sender_address, recipient_address=self._recipient_address, sender_name=self._sender_name, recipient_name=self._recipient_name, replacements=self._replacements, tags=self._tags or [])
        if save:
            if not couch.couch_db:
                config = config or {}
                couch.init(config)
            self._message_doc.save()
        return self._message_doc

    @classmethod
    def from_couchdb(cls, doc_id=None, doc=None):
        """
                Setup a PonyExpress object using a queued or failed PonyExpressMessage couchdb doc
                """
        if not doc:
            doc = couch.PonyExpressMessage(doc_id)
        pony = PonyExpress(id=doc.template, sender_address=doc.sender_address, sender_name=doc.sender_name, recipient_name=doc.recipient_name, recipient_address=doc.recipient_address, tags=doc.tags, replacements=doc.replacements)
        pony._message_doc = doc
        return pony

    def smtp_connect(self, connection):
        """
                Setup the SMTP connection to use to send this message

                connection:
                        either a smtplib.SMTP() connection object
                        or pass string with this format: "host|port|user|pass"

                Example use for passing in an existing connection of type smtplib.SMTP:
                        >>> # create the connection
                        >>> connection = smtplib.SMTP('mail.gmail.com', port=25)
                        >>> # login with our SMPT user/pass
                        >>> connection.login('username', 'password')
                        >>> # pass it into the MailTpl() object
                        >>> smtp_connect(connection) 
                
                Example use for passing in a string:
                        >>> # connection string with no login info
                        >>> smtp_connect('mail.gmail.com|25')
                        >>> # connection string with login info
                        >>> smtp_connect('mail.gmail.com|25|user|pass')
                """
        if not isinstance(connection, smtplib.SMTP):
            conn_parts = str(connection).split('|')
            conn_len = len(conn_parts)
            conn_host = str('localhost' if not conn_len > 0 else conn_parts[0])
            conn_port = int(25 if not conn_len > 1 else conn_parts[1])
            conn_user = str('' if not conn_len > 2 else conn_parts[2])
            conn_pass = str('' if not conn_len > 3 else conn_parts[3])
            connection = smtplib.SMTP(conn_host, conn_port)
            if len(conn_user):
                connection.login(conn_user, conn_pass)
        self._smtp_connection = connection
        return self._smtp_connection

    def compile(self, lc):
        """
                Gets the values for replacement and performs string replacement
                """
        subject, body = lc.subject, lc.body
        (htm_body, txt_body) = (None, None)
        if self._replacements:
            kwds = {}
            for (k, v) in self._replacements.iteritems():
                kwds[str(k)] = v

            subject = unicode(Template(subject).safe_substitute(**kwds))
            body = unicode(Template(body).safe_substitute(**kwds))
        if self._template.format == 'text':
            txt_body = body
        elif self._template.format == 'html':
            htm_body = body
        return (subject, htm_body, txt_body)

    def send(self, config=None):
        """
                Send the current message.

                        * Make sure we have a valid smtp connection
                        * Connect to couchdb and get the template
                        * Get the language specific subject/body from couchdb
                        * Render the subject/body, with variable replacement
                        * Send the message

                If sending fails at any stage of the way, we will
                log the exception and current message details to
                couch so we can retry.
                """
        if not self._smtp_connection:
            try:
                self.smtp_connect((config or {}).get('SMTP_STRING', None))
            except Exception, e:
                raise PonyExpressException(self, 'SMTP', str(e))
                return dict(status=False, id=None, error='SMTP: %s' % str(e))

        if not couch.couch_db:
            couch.init(config=config)
        try:
            self._template = couch.PonyExpressTemplate.get(self._id)
        except Exception, e:
            raise PonyExpressException(self, 'COUCH', str(e))
            return dict(status=False, id=None, error='COUCH: %s' % str(e))
        else:
            lc_try = [ lc for lc in self._template.contents if lc.lang == self._lang ]
            if lc_try:
                lc = lc_try[0]
            elif self._lang != self._fallback_language:
                lc_try = [ lc for lc in self._template.contents if lc.lang == self._fallback_language ]
                if lc_try:
                    lc = lc_try[0]
                else:
                    e = 'Unable to load language selected (%s)' % self._fallback_language
                    raise PonyExpressException(self, 'LOCALE', str(e))
                    return dict(status=False, id=None, error='LOCALE: %s' % str(e))
            (subject, html_body, text_body) = self.compile(lc)
            if html_body and text_body:
                format = 'both'
                msg = MIMEMultipart('alternative')
                msg.attach(MIMEText(text_body, 'plain'))
                msg.attach(MIMEText(html_body, 'html'))
            elif html_body:
                format = 'html'
                msg = MIMEText(html_body.encode('utf-8', 'replace'), 'html', 'utf-8')
            elif text_body:
                format = 'text'
                msg = MIMEText(text_body.encode('utf-8', 'replace'), 'plain', 'utf-8')

        msg['Subject'] = subject
        msg['Return-Path'] = self._sender_address
        msg['From'] = '%s <%s>' % (self._sender_name, self._sender_address)
        msg['To'] = self._recipient_address
        try:
            self._smtp_connection.sendmail(msg['From'], self._recipient_address, msg.as_string())
            if not self._message_doc:
                self._message_doc = self.to_couchdb(status='sent', save=False)
            self._message_doc.date = datetime.datetime.now()
            self._message_doc.status = 'sent'
            self._message_doc.subject = subject
            self._message_doc.body = text_body or html_body
            self._message_doc.save()
            return dict(result=True, id=self._message_doc._id)
        except Exception, e:
            if self._message_doc:
                self._message_doc.status = 'failed'
                self._message_doc.save()
            raise PonyExpressException(self, 'SEND', str(e))
            return dict(result=False, id=None, error='SEND: %s' % str(e))

        return