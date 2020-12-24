# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-8.10.1-i386/egg/iqpp/plone/commenting/subscribers.py
# Compiled at: 2007-10-07 08:01:45
from iqpp.plone.commenting.interfaces import ICommentingOptions
from iqpp.plone.commenting.config import MESSAGES, ENCODING
from Products.CMFCore.utils import getToolByName

def sendCommentAddedMail(event):
    """
    """
    context = event.context
    options = ICommentingOptions(context)
    if options.getEffectiveOption('send_comment_added_mail') == False:
        return
    comment = event.comment
    utool = getToolByName(context, 'portal_url')
    portal = utool.getPortalObject()
    mail_from = options.getEffectiveOption('mail_from') or portal.getProperty('email_from_address')
    mail_to = options.getEffectiveOption('mail_to') or portal.getProperty('email_from_address')
    if (mail_from and mail_to) == False:
        return
    mail = 'from: %s\n' % options.mail_from
    mail += 'to: %s\n' % options.mail_to
    mail += 'subject: [%s] %s\n\n' % (context.context.title_or_id(), MESSAGES['comment-added-subject'])
    mail += 'Name:\n%s\n' % comment.name
    mail += 'E-Mail:\n%s\n' % comment.email
    mail += 'Subject:\n%s\n' % comment.subject
    mail += 'Message:\n%s\n' % comment.message
    mail = mail.encode(ENCODING)
    try:
        context.MailHost.send(mail)
    except:
        return False
    else:
        return True