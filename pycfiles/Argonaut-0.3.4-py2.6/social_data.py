# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/argonaut/model/initial_data/social_data.py
# Compiled at: 2011-02-21 15:06:08
from argonaut.model.meta import Session, Base
from argonaut.model import Social
values = [
 [
  1, 'dummy.mail@example.com', 1, 50, 'mailto:dummy.mail@example.com', 5],
 [
  2, 'Another social link', 1, 50, 'http://www.example.com', 10]]

def init_data():
    print 'Initing social data'
    query = Session.query(Social)
    for rec in values:
        if not query.get(rec[0]):
            social = Social()
            social.id = rec[0]
            social.name = unicode(rec[1])
            social.status = rec[2]
            social.priority = rec[3]
            social.url = unicode(rec[4])
            social.media_id = rec[5]
            Session.add(social)
            Session.commit()