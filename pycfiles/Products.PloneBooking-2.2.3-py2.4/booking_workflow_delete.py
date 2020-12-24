# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\Products\PloneBooking\skins\plonebooking_scripts\booking_workflow_delete.py
# Compiled at: 2008-11-19 15:29:05
from Products.CMFPlone.utils import transaction_note
from DateTime import DateTime
booking = state_change.object
booking_id = booking.getId()
booking_center = booking.getBookingCenter()
booked_object = booking.getBookableObject()
transaction_note('Deleted %s from %s' % (booking_id, booking.absolute_url()))
from Products.CMFCore.utils import getToolByName
booking_tool = getToolByName(booking, 'portal_booking')
booking_tool.cancelBooking(booking)
raiseError = context.REQUEST.get_header('raiseError', True)
if raiseError == True:
    raise state_change.ObjectDeleted(booked_object)
request = context.REQUEST
response = request.RESPONSE
response.setStatus(200)
response.write('')