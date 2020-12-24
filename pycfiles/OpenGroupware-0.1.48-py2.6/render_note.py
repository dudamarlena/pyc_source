# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/core/icalendar/render_note.py
# Compiled at: 2012-10-12 07:02:39
import vobject
from dateutil.tz import gettz

def render_note(note, journal, ctx, **params):
    journal.add('uid').value = ('coils://Note/{0}').format(note.object_id)
    journal.add('summary').value = note.title
    journal.add('description').value = note.content
    journal.add('dtstart').value = note.created.astimezone(params['utc_tz'])
    if note.modified is None:
        journal.add('last-modified').value = note.created.astimezone(params['utc_tz'])
    else:
        journal.add('last-modified').value = note.modified.astimezone(params['utc_tz'])
    if note.categories is not None:
        journal.add('categories').value = note.categories.split(',')
    if note.appointment_id is not None:
        journal.add('x-coils-appointment-id').value = unicode(note.appointment_id)
    if note.project_id is not None:
        journal.add('x-coils-project-id').value = unicode(note.project_id)
    if note.company_id is not None:
        journal.add('x-coils-company-id').value = unicode(note.company_id)
    if note.version is None:
        journal.add('x-coils-object-version').value = '0'
    else:
        journal.add('x-coils-object-version').value = unicode(note.version)
    if note.abstract is not None:
        journal.add('x-coils-abstract').value = note.abstract
    return