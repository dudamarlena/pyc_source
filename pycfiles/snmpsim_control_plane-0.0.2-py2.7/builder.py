# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/snmpsim_control_plane/management/exporters/builder.py
# Compiled at: 2020-01-01 13:42:52
from sqlalchemy import and_
from sqlalchemy import inspect
from snmpsim_control_plane.management import models

def object_as_dict(obj):
    return {c.key:getattr(obj, c.key) for c in inspect(obj).mapper.column_attrs}


def to_dict():
    labs = []
    query = models.Lab.query.filter_by(power='on').all()
    for orm_lab in query:
        agents = []
        lab = object_as_dict(orm_lab)
        lab.update(agents=agents)
        labs.append(lab)
        query = models.Agent.query.join(models.LabAgent, and_(models.LabAgent.agent_id == models.Agent.id, models.LabAgent.lab_id == orm_lab.id)).all()
        for orm_agent in query:
            engines = []
            selectors = []
            agent = object_as_dict(orm_agent)
            agent.update(engines=engines, selectors=selectors)
            agents.append(agent)
            query = models.Engine.query.join(models.AgentEngine, and_(models.AgentEngine.engine_id == models.Engine.id, models.AgentEngine.agent_id == orm_agent.id)).all()
            for orm_engine in query:
                users = []
                endpoints = []
                engine = object_as_dict(orm_engine)
                engine.update(users=users, endpoints=endpoints)
                engines.append(engine)
                query = models.User.query.join(models.EngineUser, and_(models.EngineUser.user_id == models.User.id, models.EngineUser.engine_id == orm_engine.id)).all()
                for orm_user in query:
                    user = object_as_dict(orm_user)
                    users.append(user)

                query = models.Endpoint.query.join(models.EngineEndpoint, and_(models.EngineEndpoint.endpoint_id == models.Endpoint.id, models.EngineEndpoint.engine_id == orm_engine.id)).all()
                for orm_endpoint in query:
                    endpoint = object_as_dict(orm_endpoint)
                    endpoints.append(endpoint)

            query = models.Selector.query.join(models.AgentSelector, and_(models.AgentSelector.selector_id == models.Selector.id, models.AgentSelector.agent_id == orm_agent.id)).all()
            for orm_selector in query:
                selector = object_as_dict(orm_selector)
                selectors.append(selector)

    context = {}
    if labs:
        context.update(labs=labs)
    return context