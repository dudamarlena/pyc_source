# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/develop/NodeDefender/NodeDefender/manage/role.py
# Compiled at: 2018-01-09 06:06:44
# Size of source mod 2**32: 1915 bytes
from flask_script import Manager, prompt
import NodeDefender
manager = Manager(usage='Administrate Roles')

@manager.option('-n', '-e', '--email', dest='email', default=None)
def technician(email):
    """List users that are member of a group"""
    if email is None:
        email = prompt('Email of User')
    try:
        NodeDefender.db.user.set_role(email, 'technician')
    except AttributeError:
        return print('User {} not found'.format(email))

    return print('User {} Added as Technician'.format(email))


@manager.option('-n', '-e', '--email', dest='email', default=None)
def admin(email):
    """List users that are member of a group"""
    if email is None:
        email = prompt('Email of User')
    try:
        NodeDefender.db.user.set_role(email, 'administrator')
    except AttributeError:
        return print('User {} not found'.format(email))

    return print('User {} Added as Administrator'.format(email))


@manager.option('-n', '-e', '--email', dest='email', default=None)
def superuser(email):
    """List users that are member of a group"""
    if email is None:
        email = prompt('Email of User')
    try:
        NodeDefender.db.user.set_role(email, 'superuser')
    except AttributeError:
        return print('User {} not found'.format(email))

    return print('User {} Added as superuser'.format(email))


@manager.option('-n', '--name', dest='name', default=None)
@manager.option('-i', '--index', dest='index', default=None)
def get(name, index):
    if name is None:
        if index is None:
            name = prompt('Index or Name')
    r = NodeDefender.db.user.Get(name if name else index)
    if r is None:
        print('Unable to find Node')
        return
    print('ID: {}, Name: {}'.format(r.id, r.name))
    print('Description: {}'.format(r.description))
    print('Users: ')
    for u in r.users:
        print('ID: {}, Email: {}'.format(u.id, u.email))