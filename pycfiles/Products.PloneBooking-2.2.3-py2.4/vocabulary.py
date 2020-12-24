# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\Products\PloneBooking\content\vocabulary.py
# Compiled at: 2008-11-19 15:29:17
"""
    PloneBooking: Vocabulary
"""
__version__ = '$Revision: 1.4 $'
__author__ = ''
__docformat__ = 'restructuredtext'
from Products.Archetypes.utils import DisplayList
CALENDAR_REFRESH_MODES = DisplayList((('auto', 'Automatic', 'label_refresh_auto'), ('manual', 'Manual', 'label_refresh_manual')))
REQUIRED_FILTERS = DisplayList((('type', 'Type', 'label_type'), ('category', 'Category', 'label_category'), ('resource', 'Resource', 'label_resource')))
CALENDAR_VIEWS = DisplayList((('day', 'Day', 'label_day'), ('week', 'Week', 'label_week'), ('month', 'Month', 'label_month')))
LISTING_VIEWS = DisplayList((('day', 'Day', 'label_day'), ('week', 'Week', 'label_week'), ('month', 'Month', 'label_month'), ('year', 'Year', 'label_year')))
VIEW_MODES = DisplayList((('listing', 'Listing', 'label_listing'), ('calendar', 'Calendar', 'label_calendar')))
BOOKING_REVIEW_MODES = DisplayList((('default', 'Default (in booking center)', 'label_default_booking_review_mode'), ('review', 'Review bookings', 'label_review_bookings'), ('publish', 'Publish automatically bookings', 'label_publish_automatically_bookings')))
GLOBAL_BOOKING_REVIEW_MODES = DisplayList((('review', 'Review bookings', 'label_review_bookings'), ('publish', 'Publish automatically bookings', 'label_publish_automatically_bookings')))