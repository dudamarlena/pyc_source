# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/xbus/broker/model/setupmodel.py
# Compiled at: 2016-06-27 03:37:50
# Size of source mod 2**32: 5732 bytes
"""helper script to create an initial database
"""
from sqlalchemy import create_engine
from xbus.broker.model import metadata
from xbus.broker.model import user
from xbus.broker.model import group
from xbus.broker.model import permission
from xbus.broker.model import user_group_table
from xbus.broker.model import group_permission_table
from xbus.broker.model import gen_password
from xbus.broker.model.emission import emitter_profile
from xbus.broker.model import emitter
from xbus.broker.model.event import event_type
from xbus.broker.model.emission import emitter_profile_event_type_rel
from xbus.broker.model.service import service
from xbus.broker.model import role
from xbus.broker.model.event import event_node
from xbus.broker.model.event import event_node_rel

def setup_xbusdemo(engine):
    emitter_profile_id = engine.execute(emitter_profile.insert().returning(emitter_profile.c.id).values(name='test_profile')).first()[0]
    engine.execute(emitter.insert().returning(emitter.c.id).values(login='test_emitter', password=gen_password('password'), profile_id=emitter_profile_id))
    event_type_id = engine.execute(event_type.insert().returning(event_type.c.id).values(name='test_event')).first()[0]
    engine.execute(emitter_profile_event_type_rel.insert().values(profile_id=emitter_profile_id, event_id=event_type_id))
    consumer_service_id = engine.execute(service.insert().returning(service.c.id).values(name='consumer_service', is_consumer=True)).first()[0]
    worker_service_id = engine.execute(service.insert().returning(service.c.id).values(name='worker_service', is_consumer=False)).first()[0]
    engine.execute(role.insert().returning(role.c.id).values(login='consumer_role', password=gen_password('password'), service_id=consumer_service_id)).first()[0]
    engine.execute(role.insert().returning(role.c.id).values(login='worker_role', password=gen_password('password'), service_id=worker_service_id)).first()[0]
    engine.execute(event_node.insert().returning(event_node.c.id).values(service_id=consumer_service_id, type_id=event_type_id, is_start=True)).first()[0]
    parent_node_id = engine.execute(event_node.insert().returning(event_node.c.id).values(service_id=worker_service_id, type_id=event_type_id, is_start=True)).first()[0]
    child_node_id = engine.execute(event_node.insert().returning(event_node.c.id).values(service_id=consumer_service_id, type_id=event_type_id, is_start=False)).first()[0]
    engine.execute(event_node_rel.insert().values(parent_id=parent_node_id, child_id=child_node_id))


def setup_usergroupperms(engine):
    """default manager setup...
    """
    passw = gen_password('managepass')
    engine.execute(user.insert().values(user_name='manager', display_name='Example manager', email_address='manager@somedomain.com', password=passw))
    user_id = engine.execute(user.select().where(user.c.user_name == 'manager').limit(1)).fetchone()[user.c.user_id]
    engine.execute(group.insert().values(group_name='managers', display_name='Managers Group'))
    managers_group_id = engine.execute(group.select().where(group.c.group_name == 'managers').limit(1)).fetchone()[group.c.group_id]
    engine.execute(user_group_table.insert().values(user_id=user_id, group_id=managers_group_id))
    p = permission.insert()
    p = p.values(permission_name='xbus_manager', description='This permission gives full access to Xbus.')
    engine.execute(p)
    permission_id = engine.execute(permission.select().where(permission.c.permission_name == 'xbus_manager').limit(1)).fetchone()[permission.c.permission_id]
    engine.execute(group_permission_table.insert().values(group_id=managers_group_id, permission_id=permission_id))


def setup_app(config):
    """Place any commands to setup txMTA here

    config must be a config object as created by SafeConfigParser
    from the standard python lib and must contain a section
    database with an entry sqlalchemy.dburi"""
    print('Creating tables')
    dbengine = create_engine(config.get('database', 'sqlalchemy.dburi'), echo=True)
    metadata.create_all(bind=dbengine)
    setup_usergroupperms(dbengine)
    setup_xbusdemo(dbengine)