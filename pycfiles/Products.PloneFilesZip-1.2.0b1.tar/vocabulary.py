# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\Products\PloneBooking\content\vocabulary.py
# Compiled at: 2008-11-19 15:29:17
__doc__ = '\n    PloneBooking: Vocabulary\n'
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