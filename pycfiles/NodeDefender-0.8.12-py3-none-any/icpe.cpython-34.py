# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/develop/NodeDefender/NodeDefender/manage/icpe.py
# Compiled at: 2018-01-09 06:06:44
# Size of source mod 2**32: 1485 bytes
from flask_script import Manager, prompt
import NodeDefender
manager = Manager(usage='Manage iCPE Devices')

@manager.option('-m', '--mac', dest='mac', default=None)
def delete(mac):
    """Delete iCPE"""
    if mac is None:
        mac = prompt('Mac')
    try:
        NodeDefender.db.icpe.delete(mac)
    except LookupError as e:
        print('Error: ', str(e))
        return

    print('Successfully Deleted: ', mac)


@manager.command
def list():
    """List iCPEs"""
    icpes = NodeDefender.db.icpe.list()
    if not icpes:
        print('No icpes')
        return False
    for icpe in icpes:
        print('ID: {}, MAC: {}'.format(icpe.id, icpe.mac_address))

    return True


@manager.command
def unassigned():
    icpes = NodeDefender.db.icpe.unassigned()
    if not icpes:
        print('No Unassigned iCPEs')
        return False
    for icpe in icpes:
        print('ID: {}, MAC: {}'.format(icpe.id, icpe.mac_address))

    return True


@manager.option('-mac', '--mac', dest='mac', default=None)
def info(mac):
    """Info about a specific iCPE"""
    if mac is None:
        mac = prompt('Mac')
    icpe = NodeDefender.db.icpe.get_sql(mac)
    if icpe is None:
        print('Unable to find iCPE {}'.format(mac))
    print('ID: {}, MAC: {}'.format(icpe.id, icpe.mac_address))
    print('Alias {}, Node: {}'.format(icpe.alias, icpe.node.name))
    print('ZWave Sensors: ')
    for sensor in icpe.sensors:
        print('Alias: {}, Type: {}'.format(sensor.alias, sensor.type))