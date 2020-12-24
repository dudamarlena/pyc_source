# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\examples\directory_writer.py
# Compiled at: 2017-03-25 15:49:04
from evgen.core import SessionOwnerTemplate, SessionTemplate, GenericEventTemplate, EventGroup
from evgen.writers import DirectoryWriter
writer = DirectoryWriter('output')
eg = EventGroup()
eg.add_event(GenericEventTemplate(writer=writer), probability=1, delay=1000)
eg.set_repeat_policy(min=20, max=20)
session = SessionTemplate()
session.add_event_group(eg)
import datetime
start = datetime.datetime.strptime('2015-01-01 10:00:00', '%Y-%m-%d %H:%M:%S')
end = datetime.datetime.strptime('2015-10-31 23:59:00', '%Y-%m-%d %H:%M:%S')
user = SessionOwnerTemplate('michalz')
user.set_number_of_sessions(10)
user.set_start_date(start)
user.set_end_date(end)
user.add_session(session)
user.generate()