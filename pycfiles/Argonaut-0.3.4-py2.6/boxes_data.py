# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/argonaut/model/initial_data/boxes_data.py
# Compiled at: 2011-02-20 14:04:18
from argonaut.model.meta import Session, Base
from argonaut.model import Boxes
values = [
 [
  1, 1, 1, 1],
 [
  2, 2, 1, 10],
 [
  3, 3, 1, 30],
 [
  4, 4, 1, 20]]

def init_data():
    print 'Initing boxes data'
    query = Session.query(Boxes)
    for rec in values:
        if not query.get(rec[0]):
            item = Boxes()
            item.box_id = rec[1]
            item.status = rec[2]
            item.order = rec[3]
            Session.add(item)
            Session.commit()