# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/argonaut/model/initial_data/box_data.py
# Compiled at: 2011-02-20 14:03:51
from argonaut.model.meta import Session, Base
from argonaut.model import Box
values = [
 [
  1, 'Tag cloud', '/boxes/tag_cloud.mako'],
 [
  2, 'Search', '/boxes/search.mako'],
 [
  3, 'Account', '/boxes/account.mako'],
 [
  4, 'Social', '/boxes/social.mako']]

def init_data():
    print 'Initing box data'
    query = Session.query(Box)
    for rec in values:
        if not query.get(rec[0]):
            item = Box()
            item.name = unicode(rec[1])
            item.template = unicode(rec[2])
            Session.add(item)
            Session.commit()