# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/argonaut/model/initial_data/config_data.py
# Compiled at: 2011-02-22 13:32:19
from argonaut.model.meta import Session, Base
from argonaut.model import Config
values = [
 [
  'rss_title', 'Argonaut RSS'],
 [
  'site_url', 'http://127.0.0.1:5000'],
 [
  'site_title', 'Argonaut'],
 [
  'comments_enabled', 'true']]

def init_data():
    print 'Initing config data'
    query = Session.query(Config)
    for rec in values:
        if not query.get(unicode(rec[0])):
            config = Config()
            config.id = unicode(rec[0])
            config.value = unicode(rec[1])
            Session.add(config)
            Session.commit()