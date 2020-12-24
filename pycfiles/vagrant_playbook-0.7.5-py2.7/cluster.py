# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-intel/egg/vagrantplaybook/compose/cluster.py
# Compiled at: 2016-11-16 04:10:40
from __future__ import absolute_import, division, print_function
__metaclass__ = type
import os, sys
from functools import partial
from vagrantplaybook.compat import compat_string_types
from vagrantplaybook.ansible import ansible_tempar, ansible_unwrap
from vagrantplaybook.errors import ContextVarGeneratorError, GroupVarGeneratorError, HostVarGeneratorError
from vagrantplaybook.compose.nodegroup import NodeGroup

class Cluster:
    """
    This class defines a cluster, thas is a set of group of nodes, where nodes in each group has similar characteristics.
    Basically, a cluster is a data structure that can be used as a recipe for setting up and provisioning a
    vagrant cluster composed by several machines with different roles.
    """

    def __init__(self, name, loader):
        """Creates a new Cluster.

        Keyword arguments:
        name            -- The name of the cluster.
        loader          -- The ansible dataloader, that will be used for generating an ansible templar manager
        """
        self.name = name
        self.box = 'ubuntu/trusty64'
        self.domain = 'vagrant'
        self.node_prefix = ''
        self.ansible_playbook_path = os.path.join(os.getcwd(), 'provisioning')
        self.ansible_context_vars = {}
        self.ansible_group_vars = {}
        self.ansible_host_vars = {}
        self._node_groups = {}
        self._ansible_templar = ansible_tempar(loader)

    def add_node_group(self, name, instances):
        """Adds a group of nodes to the cluster.

        Keyword arguments:
        name            -- The name of the group of nodes.
        instances       -- The number of nodes - VM instances - in the group.
        """
        self._node_groups[name] = NodeGroup(index=len(self._node_groups), name=name, instances=instances, box=self.box, boxname='{% if cluster_node_prefix %}{{cluster_node_prefix}}-{% endif %}{{group_name}}{{node_index + 1}}', hostname='{{boxname}}', fqdn='{{hostname}}{% if cluster_domain %}.{{cluster_domain}}{% endif %}', aliases=[], ip='172.31.{{group_index}}.{{100 + node_index + 1}}', cpus=1, memory=256, ansible_groups=[], attributes={})
        return self._node_groups[name]

    def compose(self):
        """Composes the cluster by generating nodes - VM instances - in each group of nodes """
        nodes = self._get_nodes()
        ansible_groups, extended_ansible_groups = self._get_ansible_groups(nodes)
        context_vars = self._get_context_vars(extended_ansible_groups)
        ansible_group_vars = self._get_ansible_group_vars(extended_ansible_groups, context_vars)
        ansible_host_vars = self._get_ansible_host_vars(nodes, context_vars)
        inventory = self._get_ansible_inventory(ansible_groups)
        return (
         nodes, inventory, ansible_group_vars, ansible_host_vars)

    def __setattr__(self, name, value):
        if name in ('name', ):
            if not (isinstance(value, compat_string_types) or value is None):
                raise TypeError("Attribute '%s' accepts only string values or empty." % name)
        elif name in ('box', 'domain', 'node_prefix', 'ansible_playbook_path'):
            if not isinstance(value, compat_string_types):
                raise TypeError("Attribute '%s' accepts only string values." % name)
        elif name in ('ansible_context_vars', 'ansible_group_vars', 'ansible_host_vars'):
            if not isinstance(value, dict):
                raise TypeError("Attribute '%s' accepts only object values." % name)
            else:
                for k1, v1 in value.iteritems():
                    if not isinstance(k1, compat_string_types):
                        raise TypeError("Invalid value for attribute '%s'. Check documentation." % name)
                    if not isinstance(v1, dict):
                        raise TypeError("Invalid value for attribute '%s'. Check documentation." % name)
                    else:
                        for k2, v2 in v1.iteritems():
                            if not isinstance(k2, compat_string_types):
                                raise TypeError("Invalid value for attribute '%s'. Check documentation." % name)
                            if not isinstance(v1, dict):
                                raise TypeError("Invalid value for attribute '%s'. Check documentation." % name)

        else:
            if name.startswith('_'):
                self.__dict__[name] = value
                return
            raise AttributeError("Attribute '%s' does't exists" % name)
        self.__dict__[name] = value
        return

    def _get_nodes(self):
        """Gets the list of nodes by composing all the nodegroups."""
        nodes = []
        for key, group in self._node_groups.iteritems():
            nodes.extend(group.compose(self._ansible_templar, self.name, self.node_prefix, self.domain, len(nodes)))

        return nodes

    def _get_ansible_groups(self, nodes):
        """Gets the ansible groups, each with its own list of nodes.
        NB. A node can be in zero, one or more than one ansible groups

        Keyword arguments:
        nodes           -- The list of nodes.
        """
        ansible_groups = {}
        for node in nodes:
            for ansible_group in node.ansible_groups:
                if ansible_group not in ansible_groups:
                    ansible_groups[ansible_group] = []
                ansible_groups[ansible_group].append(node)

        extended_ansible_groups = ansible_groups.copy()
        extended_ansible_groups['all'] = nodes
        return (
         ansible_groups, extended_ansible_groups)

    def _get_ansible_inventory(self, ansible_groups):
        """Gets the ansible to be used when provisioning VMs with vagrant/ansible.

        Keyword arguments:
        ansible_groups  -- The list of ansible_groups, each one with its own list of nodes.
        """
        inventory = {}
        for ansible_group, ansible_group_nodes in ansible_groups.iteritems():
            if ansible_group not in inventory:
                inventory[ansible_group] = [ dict(boxname=node.boxname, hostname=node.hostname) for node in ansible_group_nodes ]

        return inventory

    def _get_context_vars(self, ansible_groups):
        """Gets the context_vars to be used when generating group_vars and host_vars.

        Keyword arguments:
        ansible_groups  -- The list of ansible_groups, each one with its own list of nodes.
        """
        context_vars = {}
        for ansible_group, ansible_group_nodes in ansible_groups.iteritems():
            if ansible_group in self.ansible_context_vars:
                provisioners = self.ansible_context_vars[ansible_group]
                provisioners = ansible_unwrap(provisioners)
                for var_name, var_generator in provisioners.iteritems():
                    self._ansible_templar.set_available_variables(dict(nodes=ansible_group_nodes))
                    try:
                        value = self._ansible_templar.template(var_generator)
                    except Exception as e:
                        raise ContextVarGeneratorError(ansible_group, var_name, e.message), None, sys.exc_info()[2]

                    context_vars[var_name] = ansible_unwrap(value)

        return context_vars

    def _get_ansible_group_vars(self, ansible_groups, context_vars):
        """Gets the ansible_group_vars for ansible provisioning.

        Keyword arguments:
        ansible_groups  -- The list of ansible_groups, each one with its own list of nodes.
        context_vars    -- The list of context_vars
        """
        ansible_group_vars = {}
        for ansible_group, ansible_group_nodes in ansible_groups.iteritems():
            if ansible_group in self.ansible_group_vars:
                ansible_group_vars[ansible_group] = {}
                provisioners = self.ansible_group_vars[ansible_group]
                provisioners = ansible_unwrap(provisioners)
                for var_name, var_generator in provisioners.iteritems():
                    self._ansible_templar.set_available_variables(dict(context=context_vars, nodes=ansible_group_nodes))
                    try:
                        value = self._ansible_templar.template(var_generator)
                    except Exception as e:
                        raise GroupVarGeneratorError(ansible_group, var_name, e.message), None, sys.exc_info()[2]

                    ansible_group_vars[ansible_group][var_name] = ansible_unwrap(value)

        return ansible_group_vars

    def _get_ansible_host_vars(self, nodes, context_vars):
        """Gets the ansible_host_vars for ansible provisioning.

        Keyword arguments:
        ansible_groups  -- The list of ansible_groups, each one with its own list of nodes.
        context_vars    -- The list of context_vars
        """
        ansible_host_vars = {}
        for node in nodes:
            ansible_host_vars[node.hostname] = {}
            for ansible_group in node.ansible_groups:
                if ansible_group in self.ansible_host_vars:
                    provisioners = self.ansible_host_vars[ansible_group]
                    provisioners = ansible_unwrap(provisioners)
                    for var_name, var_generator in provisioners.iteritems():
                        self._ansible_templar.set_available_variables(dict(context=context_vars, node=node))
                        try:
                            value = self._ansible_templar.template(var_generator)
                        except Exception as e:
                            raise HostVarGeneratorError(node.hostname, var_name, e.message), None, sys.exc_info()[2]

                        ansible_host_vars[node.hostname][var_name] = ansible_unwrap(value)

        return ansible_host_vars