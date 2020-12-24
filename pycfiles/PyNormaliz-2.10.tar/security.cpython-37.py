# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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