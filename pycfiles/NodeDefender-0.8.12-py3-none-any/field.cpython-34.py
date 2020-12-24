# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/develop/NodeDefender/NodeDefender/db/field.py
# Compiled at: 2018-02-26 02:27:58
# Size of source mod 2**32: 2258 bytes
from NodeDefender.db import redis
from NodeDefender.db.sql import SQL, CommandClassModel, CommandClassTypeModel
import NodeDefender

def get_redis(mac_address, sensor_id, name):
    return redis.field.get(mac_address, sensor_id, name)


def update_redis(mac_address, sensor_id, name, **kwargs):
    return redis.field.save(mac_address, sensor_id, name, **kwargs)


def delete_redis(mac_address, sensor_id, name):
    return redis.field.flush(mac_address, sensor_id, name)


def get(mac_address, sensor_id, name):
    return get_redis(mac_address, sensor_id, name)


def update(mac_address, sensor_id, name, **kwargs):
    return update_redis(mac_address, sensor_id, name, **kwargs)


def list(mac_address, sensor_id):
    return redis.field.list(mac_address, sensor_id)


def load():
    commandclasses = SQL.session.query(CommandClassModel).filter(CommandClassModel.name.isnot(None)).all()
    if len(commandclasses):
        load_commandclass(*commandclasses)
    commandclasstypes = SQL.session.query(CommandClassTypeModel).filter(CommandClassTypeModel.name.isnot(None)).all()
    if len(commandclasstypes):
        load_commandclasstype(*commandclasstypes)
    return len(commandclasses) + len(commandclasstypes)


def load_from_icpe(icpe):
    for sensor in icpe.sensors:
        load_from_sensor(sensor)


def load_from_sensor(sensor):
    load_commandclass(*sensor.commandclasses)


def load_commandclass(*commandclasses):
    for commandclass in commandclasses:
        if not commandclass.name:
            continue
        field = eval('NodeDefender.icpe.zwave.commandclass.' + commandclass.name + '.fields')
        if field:
            redis.field.load(commandclass, **field)
        if commandclass.types:
            load_commandclasstype(*commandclass.types)
            continue

    return len(commandclasses)


def load_commandclasstype(*cctypes):
    for cctype in cctypes:
        field = eval('NodeDefender.icpe.zwave.commandclass.' + cctype.commandclass.name + '.' + cctype.name + '.fields')
        if field:
            redis.field.load(cctype.commandclass, **field)
            continue

    return len(cctypes)


def flush(mac_address, sensor_id, name):
    return delete_redis(mac_address, sensor_id, name)