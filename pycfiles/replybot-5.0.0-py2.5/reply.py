# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/botlib/reply.py
# Compiled at: 2008-08-09 12:48:27
"""Do the actual reply."""
from __future__ import with_statement
__metaclass__ = type
__all__ = [
 'do_reply']
import os, sys, errno, logging, smtplib, urllib2, datetime, tempfile
from email import utils
from email.mime.message import MIMEMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from string import Template
from botlib.configuration import config
from botlib import version
log = logging.getLogger('replybot')

def retrieve_response(reply_url, cache_directory):
    """Download and cache the response text.

    :param reply_url: The url to the autoresponse text
    :type reply_url: string
    :param cache_directory: The path to the cache directory
    :type cache_directory: string
    :return: the retrieved data and the filename its cached in
    :rtype: 2-tuple
    """
    log.info('Retrieving url: %s', reply_url)
    fp = urllib2.urlopen(reply_url)
    try:
        data = fp.read()
    finally:
        fp.close()

    try:
        os.mkdir(cache_directory, 1472)
    except OSError, e:
        if e.errno != errno.EEXIST:
            raise

    (fd, filename) = tempfile.mkstemp('', '', cache_directory)
    log.info('Saving cache file: %s', filename)
    try:
        os.write(fd, data)
    finally:
        os.close(fd)

    return (
     data, filename)


def get_response():
    """Get the response text.

    :return: the response text
    :rtype: string
    """
    now = datetime.datetime.now()
    notice = config.db.get_notice(config.reply_url)
    if notice is None:
        log.info('Caching new response text for: %s', config.reply_url)
        (text, filename) = retrieve_response(config.reply_url, config.cache_directory)
        config.db.put_notice(filename, config.reply_url, now)
    elif now > notice.retrieved + config.cache_period:
        log.info('Cache expired for url: %s', config.reply_url)
        try:
            os.remove(notice.filename)
        except OSError, e:
            if e.errno != errno.ENOENT:
                raise
        else:
            (text, filename) = retrieve_response(config.reply_url, config.cache_directory)
            notice.filename = unicode(filename)
            notice.retrieved = now
            config.db.store.commit()
    else:
        log.debug('Cache for %s: %s', config.reply_url, notice.filename)
        with open(notice.filename) as (fp):
            text = fp.read()
    return text


def do_reply(msg, sender):
    """Do the actual reply.

    :param msg: the original message
    :type msg: email.message.Message
    ;param sender: the sender of the original message
    :type sender: string
    """
    msgid = msg.get('message-id')
    log.info('Sending response to %s:%s, triggered by: %s', config.reply_context, sender, '(no message id available)' if msgid is None else msgid)
    original_msg = MIMEMessage(msg)
    response_text = get_response()
    response_msg = MIMEText(response_text)
    response = MIMEMultipart(_subparts=(response_msg, original_msg))
    response['From'] = utils.formataddr((config.replybot_who,
     config.replybot_from))
    response['To'] = sender
    response['Subject'] = 'Re: ' + msg.get('subject', '(no subject)')
    if msgid is not None:
        response['In-Reply-To'] = msgid
    references = msg.get('references')
    if references is None:
        references = msg.get('in-reply-to')
    if references is not None:
        if msgid is not None:
            references += ', ' + msgid
        response['References'] = references
    response['Precedence'] = 'bulk'
    response['X-No-Archive'] = 'Yes'
    response['X-Mailer'] = config.replybot_who + ' ' + version.VERSION
    response['X-Ack'] = 'No'
    response['X-Bug-Tracker'] = 'https://bugs.launchpad.net/replybot'
    if config.options.debug:
        log.debug('Debugging.  Not sending email to %s:%s', config.reply_context, sender)
        print >> sys.stderr, response.as_string()
    else:
        log.debug('Connecting to: %s:%s', config.mail_server, config.mail_port)
        conn = smtplib.SMTP()
        conn.connect(config.mail_server, config.mail_port)
        if config.mail_user and config.mail_password:
            log.debug('Authenticating to SMTP server as: %s', config.mail_user)
            conn.login(config.mail_user, config.mail_password)
        substitutions = dict(msg.items())
        substitutions.update(config.keywords)
        template = Template(response.as_string())
        flatmsg = template.safe_substitute(substitutions)
        log.debug('Sending %s bytes to: %s', len(flatmsg), sender)
        try:
            conn.sendmail(config.replybot_mailfrom, [sender], flatmsg)
        except smtplib.SMTPException:
            log.exception('sendmail() exception to sender: %s', sender)

        conn.quit()
    entry = config.db.get_entry(sender, config.reply_context)
    now = datetime.datetime.now()
    if entry is None:
        log.debug('Adding new database entry for sender: %s:%s', config.reply_context, sender)
        entry = config.db.put_entry(sender, now, config.reply_context)
    else:
        log.debug('Setting last_sent for existing sender: %s:%s', config.reply_context, sender)
        entry.last_sent = now
    config.db.store.commit()
    return