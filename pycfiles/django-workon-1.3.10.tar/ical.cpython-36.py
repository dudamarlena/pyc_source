# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/dalou/www/DJANGO-WORKON/workon/utils/ical.py
# Compiled at: 2018-03-02 04:14:08
# Size of source mod 2**32: 2017 bytes
import re, datetime
from django.utils.dateformat import format
__all__ = [
 'ics']

def ics(start_at, end_at, summary, uid=None, method='REQUEST', prodid='-//Microsoft Corporation//Outlook 10.0 MIMEDIR//EN', organizer=None, location=None, description=None, emails=None, users=None):
    ics = 'BEGIN:VCALENDAR'
    ics += '\nPRODID:%s' % prodid
    ics += '\nVERSION:2.0'
    ics += '\nMETHOD:%s' % method
    ics += '\nBEGIN:VEVENT'
    attendees = []
    if users:
        for user in users:
            attendees.append('ATTENDEE;CN=%s;ROLE=REQ-PARTICIPANT;RSVP=TRUE:MAILTO:%s' % (user.get_full_name(), user.email))

    if attendees:
        ics += '\n' + '\n'.join(attendees)
    if organizer:
        ics += '\nORGANIZER:MAILTO:%s' % (organizer,)
    ics += '\nDTSTART:%sZ' % (format(start_at, 'Ymd\\THis'),)
    ics += '\nDTEND:%sZ' % (format(end_at, 'Ymd\\THis'),)
    ics += '\nDTSTAMP:%sZ' % (format(start_at, 'Ymd\\THis'),)
    if location:
        ics += '\nLOCATION:%s' % location
    ics += '\nTRANSP:OPAQUE'
    ics += '\nSEQUENCE:0'
    if uid:
        ics += '\nUID:%s' % uid
    if description:
        ics += '\nDESCRIPTION:%s' % description.replace('\n', '\\n').strip()
    ics += '\nSUMMARY:%s' % summary.replace('\n', '\\n').strip()
    ics += '\nPRIORITY:5'
    ics += '\nCLASS:PUBLIC'
    ics += '\nBEGIN:VALARM'
    ics += '\nTRIGGER:-PT15M'
    ics += '\nACTION:DISPLAY'
    ics += '\nDESCRIPTION:Reminder'
    ics += '\nEND:VALARM'
    ics += '\nEND:VEVENT'
    ics += '\nEND:VCALENDAR'
    return ics