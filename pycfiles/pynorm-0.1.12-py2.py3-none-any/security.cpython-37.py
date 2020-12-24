# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ax/Workspace/norm/norm/security.py
# Compiled at: 2019-05-04 12:20:08
# Size of source mod 2**32: 471 bytes
from norm.config import PUBLIC_USER, session

def login(usr=None):
    from norm.models.user import User
    if usr is None:
        usr = PUBLIC_USER
    u = session.query(User).filter(User.username == usr['username'], User.email == usr['email']).first()
    if u is None:
        u = User(**usr)
        session.add(u)
        session.commit()
    return u


try:
    user = login()
except:
    user = None