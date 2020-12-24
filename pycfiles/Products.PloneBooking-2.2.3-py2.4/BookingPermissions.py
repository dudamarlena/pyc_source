# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\Products\PloneBooking\BookingPermissions.py
# Compiled at: 2008-12-03 10:54:37
"""
    PloneBooking Permissions
"""
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