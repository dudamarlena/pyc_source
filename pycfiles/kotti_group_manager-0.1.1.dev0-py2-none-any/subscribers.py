# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ubuntu/workspace/src/kotti_group_manager/kotti_group_manager/subscribers.py
# Compiled at: 2018-09-19 03:14:50
from kotti import DBSession
from kotti.events import subscribe
from kotti.events import ObjectInsert
from kotti.security import Principal
from sqlalchemy.exc import IntegrityError
from kotti_group_manager.resources import GroupPage
from kotti_group_manager.security import create_group_from_user_email_domain, set_group_page_permission

@subscribe(ObjectInsert, Principal)
def new_user_handler(event):
    user = event.object
    create_group_from_user_email_domain(user)


@subscribe(ObjectInsert, GroupPage)
def update_group_page_permission_handler(event):
    group_page = event.object
    set_group_page_permission(group_page, group_page.group_name)