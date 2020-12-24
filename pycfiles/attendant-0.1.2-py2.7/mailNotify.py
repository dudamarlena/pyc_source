# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/attendant/mailnotify.py
# Compiled at: 2016-08-26 12:23:55
"""
Module that facilitates several ways to send email notifications with gmail.

It also supports ignoring mail notifications, info should be a dictionary
with "user", "password", "recipients"
"""
import smtplib, logging, os, traceback
from threading import Thread
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send(subject, body, info):
    """
    Basic synchronous email sending function given subject, body and information.
    """
    try:
        message = _createmessage(subject, body, info)
        server_ssl = _login(info)
        server_ssl.sendmail(info['user'], _recipients(info), message.as_string())
        logging.info('Notification "%s"', subject)
    except smtplib.SMTPException:
        logging.exception('Failed to send email %s', subject)
    except:
        logging.exception('Failed to send message %s', subject)


def asyncsend(subject, body, info):
    """
    Same as 'send', but performed in a background thread.

    The thread is automatically started, but not joined on.
    Still, the thread object is returned in case it is
    required.
    """
    thread = Thread(target=send, args=(subject, body, info))
    thread.start()
    return thread


def sendexception(exception, info, tracebacktxt=None, async=True, extra_subject=''):
    """
    Deliver an email with useful exception information.

    If no formatted traceback is specified, the current
    one is used. The async parameter is for calling asyncsend
    or send, respectively.

    You can add details to the subject with the variable extra_subject
    """
    subject = 'An exception occurred ' + extra_subject
    body = '\n    An exception has ocurred:\n    \n    %s\n\n    %s\n    ' % (exception.message,
     tracebacktxt or traceback.format_exc())
    if async:
        asyncsend(subject, body, info)
    else:
        send(subject, body, info)


def send500(exception, tracebacktxt, request, info, extra_subject=''):
    """
    Asynchronously deliver a message in case of a 500 error.

    It uses information from the request, the
    exception object and the non-optional fromatted
    traceback.
    You can add details to the subject with the variable extra_subject
    """
    subject = '500 error ' + extra_subject
    body = "\n    Internal server error at %s\n    \n    Arguments:\n    %s\n\n    Exception '%s':\n\n    %s\n    " % (request.path, repr(dict(request.args)),
     exception.message, tracebacktxt)
    asyncsend(subject, body, info)


def _loadcredentials(info):
    """ 
    Load the credentials of the mail account from a dictionary
    """
    return (
     info['user'], info['password'])


def _recipients(info):
    return info['recipients'].split(',')


def _recipientsstr(info):
    return (', ').join(_recipients(info))


def _createmessage(subject, body, info):
    """
    Create a message with the valid sintax
    """
    message = MIMEMultipart()
    message['Subject'] = subject
    message['From'] = info['user']
    message['To'] = _recipientsstr(info)
    message.attach(MIMEText(body, 'plain', 'utf-8'))
    return message


def _login(info):
    """
    Logs to the mail account given by the user
    """
    user, password = _loadcredentials(info)
    server_ssl = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server_ssl.ehlo()
    server_ssl.login(user, password)
    return server_ssl