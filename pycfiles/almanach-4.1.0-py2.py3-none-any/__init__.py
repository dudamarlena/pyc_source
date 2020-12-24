# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/alman/__init__.py
# Compiled at: 2015-08-31 22:18:13
API_KEY = None
API_BASE = 'http://almanapi.com/api/v0'
from .clients import DefaultClient
from .resources import Calendar, Vacancy, Booking
from .endpoints import CalendarsEndpoint, CalendarVacanciesEndpoint, VacanciesEndpoint, VacancyBookingsEndpoint, BookingsEndpoint

def default_client():
    return DefaultClient(API_KEY)