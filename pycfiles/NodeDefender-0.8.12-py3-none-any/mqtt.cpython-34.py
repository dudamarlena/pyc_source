# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/develop/NodeDefender/NodeDefender/manage/mqtt.py
# Compiled at: 2018-01-09 06:06:44
# Size of source mod 2**32: 1574 bytes
from flask_script import Manager, prompt
import NodeDefender
manager = Manager(usage='Manage MQTT')

@manager.option('-h', '-host', '--host', dest='host', default=None)
@manager.option('-p', '-port', '--port', dest='port', default=None)
@manager.option('-u', '-username', '--username', dest='username', default=None)
@manager.option('-pw', '--password', dest='password', default=None)
def create(host, port, username, password):
    """Create Node and Assign to Group"""
    if host is None:
        host = prompt('Host Address')
    if port is None:
        port = prompt('Port Number')
    try:
        NodeDefender.db.mqtt.create(host, port)
    except ValueError as e:
        print('Error: ', e)
        return

    print('MQTT {}:{} Successfully created'.format(host, port))


@manager.option('-i', '--host', dest='host', default=None)
def delete(host):
    """Delete Node"""
    if host is None:
        host = prompt('Host Address')
    try:
        NodeDefender.db.mqtt.delete(host)
    except LookupError as e:
        print('Error: ', e)
        return

    print('MQTT {} Successfully deleted'.format(host))


@manager.command
def list():
    for mqtt in NodeDefender.db.mqtt.list():
        print('ID: {}, IP: {}:{}'.format(mqtt.id, mqtt.host, mqtt.port))