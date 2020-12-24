# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/alman/__init__.py
# Compiled at: 2015-08-31 22:18:13
API_KEY = None
API_BASE = 'http://almanapi.com/api/v0'
from .clients import DefaultClient
from .resources import Calendar, Vacancy, Booking
from .endpoints import CalendarsEndpoint, CalendarVacanciesEndpoint, VacanciesEndpoint, VacancyBookingsEndpoint, BookingsEndpoint

def default_client():
    return DefaultClient(API_KEY)