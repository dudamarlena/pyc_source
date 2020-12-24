# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyogp/lib/client/agentmanager.py
# Compiled at: 2010-02-09 00:00:15
"""
Contributors can be viewed at:
http://svn.secondlife.com/svn/linden/projects/2008/pyogp/lib/base/trunk/CONTRIBUTORS.txt 

$LicenseInfo:firstyear=2008&license=apachev2$

Copyright 2009, Linden Research, Inc.

Licensed under the Apache License, Version 2.0.
You may obtain a copy of the License at:
    http://www.apache.org/licenses/LICENSE-2.0
or in 
    http://svn.secondlife.com/svn/linden/projects/2008/pyogp/lib/base/LICENSE.txt

$/LicenseInfo$
"""
from logging import getLogger
import signal, sys
from eventlet import api
from pyogp.lib.base.datatypes import UUID
from pyogp.lib.client.exc import LoginError
from pyogp.lib.base.helpers import Wait
logger = getLogger('pyogp.lib.client.agentmanager')

class AgentManager(object):
    """ a simple class to track multiple agents

    This class can perhaps begin to manage sessions in time.
    """
    __module__ = __name__

    def __init__(self, settings=None):
        """ initialize the agent manager """
        if settings != None:
            self.settings = settings
        else:
            from pyogp.lib.client.settings import Settings
            self.settings = Settings()
        self.agents = {}
        self.signal_handler = signal.signal(signal.SIGINT, self.sigint_handler)
        if self.settings.LOG_VERBOSE:
            logger.debug('Initializing agent manager for %s agents' % len(self.agents))
        return

    def initialize(self, agents):
        """ accept a list of Agent() instances, and store them in the agents attribute """
        if type(agents) != list:
            logger.warning('The AgentManager requires a list of Agent instances to initialize. Stopping.')
            return False
        for agent in agents:
            self.store_agent(agent)

    def store_agent(self, agent):
        """ adds an agent to the store """
        if str(type(agent)) != "<class 'pyogp.lib.client.agent.Agent'>":
            logger.warning('The AgentManager stores only Agent instances to initialize. Stopping.')
            return False
        if self._is_stored(agent) == False:
            if agent.agent_id == None:
                key = UUID().random()
            else:
                key = agent.agent_id
            self.agents[key] = agent
            logger.info('Stored agent %s with a key of %s' % (agent.name, key))
        else:
            if agent.firstname != None and agent.lastname != None:
                uniq = ' named ' + agent.Name()
            logger.warning('The AgentManager is already storing an agent%s. Stopping.' % uniq)
        return

    def _is_stored(self, agent):
        """ returns True if an agent is already stored, False if not """
        if agent.Name() in self._stored_names():
            return True
        elif agent.agent_id in self._stored_agent_ids():
            return True
        else:
            return False

    def _stored_names(self):
        """ returns the stored agent's names in a list """
        names = []
        for key in self.agents:
            names.append(self.agents[key].Name())

        return names

    def _stored_agent_ids(self):
        """ returns the stored agent's names in a list """
        ids = []
        for key in self.agents:
            if self.agents[key].agent_id != None:
                ids.append(self.agents[key].agent_id)

        return ids

    def login(self, key, loginuri, start_location):
        """ spawns a new agent via an eventlet coroutine """
        if self.settings.LOG_COROUTINE_SPAWNS:
            logger.info('Spawning a coroutine for agent login for %s.' % self.agents[key].Name())
        try:
            api.spawn(self.agents[key].login, loginuri=loginuri, start_location=start_location)
        except LoginError, error:
            logger.error('Skipping agent with failed login: %s due to %s.' % (self.agents[key].Name(), error))

    def has_agents_running(self):
        """ returns true if there is a client who's running value = True """
        for key in self.agents:
            if self.agents[key].running:
                return True

        return False

    def get_active_agents(self):
        """ returns a list of agents that are connected to a grid """
        active = []
        for key in self.agents:
            active.append(self.agents[key])

        return active

    def sigint_handler(self, sigint, frame):
        """ handles signals from the command line (and others) and logs out all agents """
        logger.info('Caught signal... %d. Stopping' % sigint)
        for agent in self.get_active_agents():
            agent.logout()

        Wait(10)
        if self.has_agents_running():
            logger.warning('These agents have not yet shut down. Killing the process hard.\n\t\t%s' % self.get_active_agents())
            sys.exit(1)