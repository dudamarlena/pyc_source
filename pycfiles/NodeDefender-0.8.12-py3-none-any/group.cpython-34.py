# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/develop/NodeDefender/NodeDefender/manage/group.py
# Compiled at: 2018-01-09 06:06:44
# Size of source mod 2**32: 1509 bytes
from flask_script import Manager, prompt
import NodeDefender
manager = Manager(usage='Manage Groups')

@manager.option('-name', '--name', dest='name', default=None)
def create(name):
    """Create a Group"""
    if name is None:
        name = prompt('Group Name')
    try:
        NodeDefender.db.group.create(name)
    except ValueError as e:
        print('Error: ', e)

    print('Group {} successfully added'.format(name))


@manager.option('-name', '--name', dest='name', default=None)
def delete(name):
    """Delete a Group"""
    if name is None:
        name = prompt('Group Name')
    try:
        NodeDefender.db.group.delete(name)
    except ValueError as e:
        print('Error: ', e)

    print('Group {} successfully deleted'.format(name))


@manager.command
def list():
    """List Groups"""
    for group in NodeDefender.db.group.list():
        print('ID: {}, Name: {}'.format(group.id, group.name))


@manager.option('-n', '-g', '--group', '--name', dest='name', default=None)
def info(name):
    """Show information about a Group"""
    if name is None:
        name = prompt('Group Name')
    group = NodeDefender.db.group.get_sql(name)
    if group is None:
        print('Cant find group ', name)
        return
    print('ID: {}, Name: {}'.format(group.id, group.name))
    print('User Members:')
    for user in group.users:
        print('ID: {}, Mail: {}'.format(user.id, user.email))

    print('Nodes')
    for node in group.nodes:
        print('ID: {}, Name: {}'.format(node.id, node.name))