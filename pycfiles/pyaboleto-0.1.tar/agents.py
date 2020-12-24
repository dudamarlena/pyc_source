# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\pyabm\agents.py
# Compiled at: 2012-11-18 17:36:44
__doc__ = "\nContains classes to assist in making agents. 'Person' agents, for example, \nwould be subclasses of the Agent class, while Household, Neighborhood, and \nRegion agents would be represented as subclasses of the Agent_set object (as \nhouseholds, neighborhoods, and regions all contain lower-level agents).\n"
from __future__ import division
from pyabm import rc_params
rcParams = rc_params.get_params()

class Agent(object):
    """Class for agent objects."""

    def __init__(self, world, ID, initial_agent=False):
        self._world = world
        self._ID = ID
        self._initial_agent = initial_agent
        self._parent_agent = None
        return

    def get_ID(self):
        return self._ID

    def set_parent_agent(self, agent):
        self._parent_agent = agent

    def get_parent_agent(self):
        return self._parent_agent


class Agent_set(Agent):
    """
    Class for agents that contain a "set" of agents from a lower 
    hierarchical  level.
    """

    def __init__(self, world, ID, initial_agent):
        Agent.__init__(self, world, ID, initial_agent)
        self._members = {}

    def get_agents(self):
        return self._members.values()

    def get_agent(self, ID):
        """Returns an agent given the agent's ID"""
        return self._members[ID]

    def is_member(self, ID):
        """Returns true if agent is a member of this set"""
        return ID in self._members

    def add_agent(self, agent):
        """Adds a new agent to the set."""
        if agent.get_ID() in self._members:
            raise KeyError('agent %s is already a member of agent set %s' % (agent.get_ID(), self._ID))
        self._members[agent.get_ID()] = agent
        agent.set_parent_agent(self)

    def remove_agent(self, agent):
        """Removes agent from agent set."""
        try:
            self._members.pop(agent.get_ID())
        except KeyError:
            raise KeyError('agent %s is not a member of agent set %s' % (agent.get_ID(), self.get_ID()))

        assert agent.get_parent_agent().get_ID() == self.get_ID(), 'Removing agent from an Agent_set it does not appear to be assigned to.'
        agent.set_parent_agent(None)
        return

    def iter_agents(self):
        for agent in self.get_agents():
            yield agent

    def num_members(self):
        return len(self._members)


class Agent_Store(object):
    """
    Agent_Store is a class used to store agents who have left for various 
    reasons (such as migration) or are in school. It allows triggering their 
    return or graduation during a later timestep of the model.
    """

    def __init__(self):
        self._releases = {}
        self._parent_dict = {}
        self._stored_agents = []

    def add_agent(self, agent, release_time):
        """
        Adds a new agent to the agent store. Also remove the agent from it's 
        parent Agent_set instance.
        """
        if release_time in self._releases:
            self._releases[release_time].append(agent)
        else:
            self._releases[release_time] = [
             agent]
        self._parent_dict[agent] = agent.get_parent_agent()
        agent._store_list.append(self)
        agent.get_parent_agent().remove_agent(agent)
        self._stored_agents.append(agent)

    def release_agents(self, time):
        released_agents = []
        released_agents_dict = {}
        if time in self._releases:
            for agent in self._releases[time]:
                parent_agent = self._parent_dict.pop(agent)
                parent_agent.add_agent(agent)
                agent._store_list.remove(self)
                self._stored_agents.remove(agent)
                neighborhood = parent_agent.get_parent_agent()
                if neighborhood.get_ID() not in released_agents_dict:
                    released_agents_dict[neighborhood.get_ID()] = 0
                released_agents_dict[neighborhood.get_ID()] += 1
                released_agents.append(agent)

            self._releases.pop(time)
        return (released_agents_dict, released_agents)

    def in_store(self, agent):
        if agent in self._stored_agents:
            return True
        else:
            return False

    def remove_agent(self, agent):
        """
        Remove an agent from the store without releasing it to its original 
        location (useful for handling agents who die while away from home).
        """
        self._releases[agent._return_timestep].remove(agent)
        self._parent_dict.pop(agent)
        self._stored_agents.remove(agent)
        agent._store_list.remove(self)

    def __str__(self):
        return 'Agent_Store(%s)' % self._releases