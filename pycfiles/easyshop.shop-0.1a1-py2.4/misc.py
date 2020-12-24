# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/shop/utilities/misc.py
# Compiled at: 2008-06-20 09:37:25
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import safe_unicode
from email.MIMEText import MIMEText
from email.MIMEMultipart import MIMEMultipart
from email.MIMENonMultipart import MIMENonMultipart

def getObjectByUID(context, uid):
    """
    """
    catalog = getToolByName(context, 'portal_catalog')
    brains = catalog.searchResults(uid=uid)
    try:
        return brains[0]
    except IndexError:
        return

    return


def sendMultipartMail(context, sender, receiver, cc=[], bcc=[], subject='', text='', charset='utf-8'):
    """
    """
    mail = MIMEMultipart('alternative')
    mail['From'] = sender
    mail['To'] = receiver
    mail['Cc'] = (', ').join(cc)
    mail['Bcc'] = (', ').join(bcc)
    mail['Subject'] = subject
    mail.epilogue = ''
    text = text.encode('utf-8')
    text_part = MIMEText(text, 'plain', charset)
    mail.attach(text_part)
    html_part = MIMEMultipart('related')
    html_code = MIMEText(text, 'html', charset)
    html_part.attach(html_code)
    mail.attach(html_part)
    context.MailHost.send(mail.as_string())


def sendNonMultipartMail(context, sender, receiver, cc=[], bcc=[], subject='', text='', charset='utf-8'):
    """
    """
    mail = MIMENonMultipart('text', 'plain')
    mail['From'] = sender
    mail['To'] = receiver
    mail['Cc'] = (', ').join(cc)
    mail['Bcc'] = (', ').join(bcc)
    mail['Subject'] = subject
    text = text.encode('utf-8')
    mail.set_payload(text)
    context.MailHost.send(mail.as_string())