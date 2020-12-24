# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/oshane/Workspace/osoobe/packages/kotti/src/kotti_gsd/kotti_gsd/util.py
# Compiled at: 2017-05-31 17:48:39
import hashlib, time, urllib
from html2text import HTML2Text
from pyramid.renderers import render
from pyramid_mailer.mailer import Mailer
from pyramid_mailer.message import Message
from kotti.message import get_mailer

def send_email(request, recipients, template_name, template_vars=None, sender=None, cc=None, bcc=None):
    """ General email sender.

    :param request: current request.
    :type request: :class:`kotti.request.Request`

    :param recipients: list of email addresses. Each email should be a
                       string like: u'"John Doe" <joedoe@foo.com>'.
    :type recipients: list

    :param template_name: asset specification (e.g.
                          'mypackage:templates/email.pt')
    :type template_name: string

    :param template_vars: set of variables present on template.
    :type template_vars: dict
    :param sender: sender email address
    :type sender: string
    """
    if template_vars is None:
        template_vars = {}
    text = render(template_name, template_vars, request)
    subject, htmlbody = text.strip().split('\n', 1)
    subject = subject.replace('Subject:', '', 1).strip()
    html2text = HTML2Text()
    html2text.body_width = 0
    textbody = html2text.handle(htmlbody).strip()
    message = Message(recipients=recipients, subject=subject, body=textbody, html=htmlbody, sender=sender, cc=cc, bcc=bcc, attachments=None)
    mailer = get_mailer()
    mailer.send(message)
    return