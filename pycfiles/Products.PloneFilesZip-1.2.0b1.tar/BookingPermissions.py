# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\Products\PloneBooking\BookingPermissions.py
# Compiled at: 2008-12-03 10:54:37
__doc__ = '\n    PloneBooking Permissions\n'
__version__ = '$Revision: 1.4 $'
__author__ = ''
__docformat__ = 'restructuredtext'
from Products.CMFCore.permissions import setDefaultRoles
AddBookingCenter = 'PloneBooking: Add booking center'
AddBooking = 'PloneBooking: Add booking'
AddBookableObject = 'PloneBooking: Add bookable object'
setDefaultRoles(AddBookingCenter, ('Manager', 'Owner', 'Editor'))
setDefaultRoles(AddBooking, ('Manager', 'Owner', 'Member', 'Editor', 'Contributor'))
setDefaultRoles(AddBookableObject, ('Manager', 'Owner', 'Editor', 'Contributor'))