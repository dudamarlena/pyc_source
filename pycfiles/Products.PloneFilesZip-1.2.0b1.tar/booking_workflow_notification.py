# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\Products\PloneBooking\skins\plonebooking_templates\booking_workflow_notification.py
# Compiled at: 2008-11-19 15:29:04
from Products.CMFCore.utils import getToolByName
wf_tool = getToolByName(context, 'portal_workflow')
obj_review_state = wf_tool.getInfoFor(notified_obj, 'review_state')
mship = context.portal_membership
try:
    mhost = context.MailHost
except:
    mhost = None

message_template = '\nFrom: %s\nTo: %s\nSubject: %s - %s\n\n%s\n\nURL: %s\n'
if mhost:
    if 'booked' == obj_review_state:
        receiver = notified_obj.getEmail()
        sender = context.email_from_address
        subject = 'Confirmation de reservation'
        body = 'Votre reservation du %s au %s a bien été enregistrée.'
        body = body % (notified_obj.startDate, notified_obj.endDate)
        url = notified_obj.absolute_url()
    if 'pending' == obj_review_state:
        receiver = context.email_from_address
        sender = notified_obj.getEmail()
        subject = 'Demande de reservation'
        body = 'Cet item a été réservé par %s ; à vous de le confirmer en le rendant "public".' % notified_obj.Creator()
        url = notified_obj.absolute_url()
    if 'canceled' == obj_review_state:
        receiver = notified_obj.getEmail()
        sender = context.email_from_address
        subject = 'Annulation de reservation '
        body = 'La reservation de cet item par %s a été annulée.' % notified_obj.Creator()
        url = ''
    msg = message_template % (sender, receiver, subject, notified_obj.TitleOrId(), body, url)
    try:
        mhost.send(msg)
    except:
        pass