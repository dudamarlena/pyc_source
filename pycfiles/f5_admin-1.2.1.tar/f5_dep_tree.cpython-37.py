# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sli/f5-admin/src/f5_dep_tree.py
# Compiled at: 2020-03-10 21:28:12
# Size of source mod 2**32: 16179 bytes
from f5_admin import F5Client
from .util import *
import os
from os import listdir, unlink, symlink, mkdir
from os.path import isfile, isdir, join, dirname, realpath, getsize
import datetime, re

class Node:

    def __init__(self, name):
        self.name = name
        self.edges = []

    def addEdge(self, node_name):
        if node_name not in self.edges:
            self.edges.append(node_name)


class F5DepTree(F5Client):

    def __init__(self, credential, timeout, verbose):
        F5Client.__init__(self, credential, timeout, verbose)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        file = self.cache_config_base

    def load(self, node):
        if not is_valid_hostname(node):
            exit(1)
        else:
            self.node = node.lower().split('.')[0]
            self.cache_config_dir = self.cache_config_base + self.node
            if not is_directory(self.cache_config_dir):
                mkdir(self.cache_config_dir)
            self.cache_config = self.cache_config_dir + '/' + self.node + '.txt'
            print('Loading cache_config: ', self.cache_config)
            isfile(self.cache_config) or self.fetch()
        if getsize(self.cache_config) == 0:
            self.fetch()
        self.top_objs = self.parse_conf_file(self.cache_config)
        self.dep_tree = self.build_dep_tree()
        print('Loading complete')

    def build_dep_tree(self):
        if self.verbose:
            print(list(self.top_objs.keys()))
            print('Total object count: ', len(list(self.top_objs.keys())))
        dep_tree = {key:Node(key) for key in list(self.top_objs.keys())}
        for node in list(dep_tree.values()):
            self.build_tree_branches(node)

        return dep_tree

    def build_tree_branches(self, node):
        if 'ltm virtual ' in node.name:
            self.build_tree_branches_vip(node)
        else:
            if 'security firewall policy ' in node.name:
                self.build_tree_branches_afm_policy(node)
            else:
                if 'security firewall rule-list ' in node.name:
                    self.build_tree_branches_afm_rules(node)

    def build_tree_branches_vip(self, node):
        for entry in self.top_objs[node.name]:
            if 'pool ' in entry:
                pool_node_name = 'ltm pool ' + entry.split(' ')[(-1)]
                node.addEdge(pool_node_name)
            if 'ip-intelligence-policy ' in entry:
                pool_node_name = 'security ip-intelligence policy ' + entry.split(' ')[(-1)]
                if pool_node_name in list(self.top_objs.keys()):
                    node.addEdge(pool_node_name)
                else:
                    if 'security-log-profiles {' in entry:
                        security_log_profiles = self.parse_obj_one_indention('security-log-profiles {', self.top_objs[node.name])
                        for entry in security_log_profiles:
                            pool_node_name = 'security log profile ' + entry.split(' ')[(-1)]
                            if pool_node_name in list(self.top_objs.keys()):
                                node.addEdge(pool_node_name)

                    if 'fw-enforced-policy ' in entry:
                        pool_node_name = 'security firewall policy ' + entry.split(' ')[(-1)]
                        if pool_node_name in list(self.top_objs.keys()):
                            node.addEdge(pool_node_name)
                if 'rules {' in entry:
                    irules = self.parse_obj_one_indention('rules {', self.top_objs[node.name])
                    for entry in irules:
                        pool_node_name = 'ltm rule ' + entry.split(' ')[(-1)]
                        if pool_node_name in list(self.top_objs.keys()):
                            node.addEdge(pool_node_name)

                if 'policies {' in entry:
                    policies = self.parse_obj_one_indention('policies {', self.top_objs[node.name])
                    for entry in policies:
                        pool_node_name = 'ltm policy ' + entry.strip().split(' ')[0]
                        if pool_node_name in list(self.top_objs.keys()):
                            node.addEdge(pool_node_name)

                if 'vlans {' in entry:
                    vlans = self.parse_obj_one_indention('vlans {', self.top_objs[node.name])
                    for entry in vlans:
                        pool_node_name = 'net vlan ' + entry.split(' ')[(-1)]
                        if pool_node_name in list(self.top_objs.keys()):
                            node.addEdge(pool_node_name)

                if 'profiles {' in entry:
                    profiles = self.parse_obj_two_indention('profiles {', self.top_objs[node.name])
                    if self.verbose:
                        print('Found dependendant ltm profiles: ', profiles)
                    for entry in profiles:
                        pool_node_name = self.ltm_profile_lookup(entry)
                        if pool_node_name in list(self.top_objs.keys()):
                            if self.verbose:
                                print('Add dependendant ltm profile: ', pool_node_name)
                            node.addEdge(pool_node_name)

    def build_tree_branches_afm_policy(self, node):
        for entry in self.top_objs[node.name]:
            if ' rule-list ' in entry:
                pool_node_name = 'security firewall rule-list ' + entry.split(' ')[(-1)]
                if pool_node_name in list(self.top_objs.keys()):
                    node.addEdge(pool_node_name)
            if 'address-lists {' in entry:
                addr_lists = self.parse_obj_one_indention('address-lists {', self.top_objs[node.name])
                for addr in addr_lists:
                    pool_node_name_1 = 'security firewall address-list ' + addr.split(' ')[(-1)]
                    pool_node_name_2 = 'security shared-objects address-list ' + addr.split(' ')[(-1)]
                    if pool_node_name_1 in list(self.top_objs.keys()):
                        node.addEdge(pool_node_name_1)
                    if pool_node_name_2 in list(self.top_objs.keys()):
                        node.addEdge(pool_node_name_2)

            if 'fqdns {' in entry:
                fqdns = self.parse_obj_one_indention('fqdns {', self.top_objs[node.name])
                for fqdn in fqdns:
                    pool_node_name = 'security firewall fqdn-entity ' + fqdn.split(' ')[(-3)]
                    if pool_node_name in list(self.top_objs.keys()):
                        node.addEdge(pool_node_name)

            if 'port-lists {' in entry:
                port_lists = self.parse_obj_one_indention('port-lists {', self.top_objs[node.name])
                for port in port_lists:
                    pool_node_name = 'security firewall port-list ' + port.split(' ')[(-1)]
                    if pool_node_name in list(self.top_objs.keys()):
                        node.addEdge(pool_node_name)

            if 'vlans {' in entry:
                vlan_lists = self.parse_obj_one_indention('vlans {', self.top_objs[node.name])
                for vlan in vlan_lists:
                    pool_node_name = 'net vlan ' + vlan.split(' ')[(-1)]
                    if pool_node_name in list(self.top_objs.keys()):
                        node.addEdge(pool_node_name)

    def build_tree_branches_afm_rules(self, node):
        for entry in self.top_objs[node.name]:
            if 'address-lists {' in entry:
                addr_lists = self.parse_obj_one_indention('address-lists {', self.top_objs[node.name])
                for addr in addr_lists:
                    pool_node_name_1 = 'security firewall address-list ' + addr.split(' ')[(-1)]
                    pool_node_name_2 = 'security shared-objects address-list ' + addr.split(' ')[(-1)]
                    if pool_node_name_1 in list(self.top_objs.keys()):
                        node.addEdge(pool_node_name_1)
                    if pool_node_name_2 in list(self.top_objs.keys()):
                        node.addEdge(pool_node_name_2)

            if 'port-lists {' in entry:
                port_lists = self.parse_obj_one_indention('port-lists {', self.top_objs[node.name])
                for port in port_lists:
                    pool_node_name = 'security firewall port-list ' + port.split(' ')[(-1)]
                    if pool_node_name in list(self.top_objs.keys()):
                        node.addEdge(pool_node_name)

    def parse_obj_one_indention(self, pattern_string, input_obj):
        p_empty = re.compile('^(\\w+\\s)+.*\\{\\s\\}$', re.M | re.I)
        p_end = re.compile('^\\s+}$', re.M | re.I)
        recording = False
        if self.verbose:
            print('Parsing the F5 Single Configuration Object within one indention: ', pattern_string, input_obj)
        output_obj = []
        for x in input_obj:
            if self.verbose:
                print('Parsing line:', x)
            else:
                if pattern_string in x:
                    recording = True
                    if p_empty.match(x):
                        break
                    else:
                        continue
                    if recording and p_end.match(x):
                        recording = False
                        if self.verbose:
                            print('Ending found: ', x)
                        break
            if recording:
                if self.verbose:
                    print('Adding object: ', x)
                output_obj.append(x)
                continue

        if self.verbose:
            print('My output objects: ', output_obj)
        return output_obj

    def parse_obj_two_indention(self, pattern_string, input_obj):
        p_empty = re.compile('^(\\w+\\s)+.*\\{\\s\\}$', re.M | re.I)
        p_end = re.compile('^\\s+}$', re.M | re.I)
        recording = False
        recording_obj = []
        if self.verbose:
            print('Parsing the F5 Single Configuration Object within two indention: ', input_obj)
        for x in input_obj:
            if self.verbose:
                print('Parsing line:', x)
            if pattern_string in x:
                recording = True
                recording_obj.append(x)
                continue
            if recording:
                recording_obj.append(x)
            if p_end.match(x):
                if self.count_bracket(recording_obj, '{') == 0:
                    continue
                if self.count_bracket(recording_obj, '{') > self.count_bracket(recording_obj, '}'):
                    continue
                else:
                    recording = False
                    break

        if self.verbose:
            print('Recording object within two indention: ', recording_obj)
        if len(recording_obj) > 0:
            output_obj = [a.strip().split(' ')[0] for a in recording_obj]
        if self.verbose:
            print('Parsing single configuration object within two indent output: ', output_obj)
        if len(output_obj) >= 2:
            output_obj.pop()
            return output_obj[1:]
        return []

    def ltm_profile_lookup(self, name):
        if self.verbose:
            print('ltm profile lookup for: ', name)
        for item in list(self.top_objs.keys()):
            if 'ltm profile' in item and name in item:
                return item

    def dep_resolve(self, node_name):
        try:
            try:
                if 'resolved' not in globals():
                    resolved = {}
                if self.verbose:
                    print('Walking through node name: ', node_name)
                for key in self.dep_tree[node_name].edges:
                    if key not in list(resolved.keys()):
                        resolved.update({key: True})
                        self.dep_resolve(key)
                    else:
                        raise Exception('Circular reference detected: %s -> %s' % (self.dep_tree[node_name], self.dep_tree[key]))

            except Exception as e:
                try:
                    print('F5 configuration dependency resolving failure:', e)
                    raise
                finally:
                    e = None
                    del e

            except:
                print('Unexpected error:', sys.exc_info()[0])
                raise
            else:
                if self.verbose:
                    print(list(resolved.keys()))
        finally:
            return

        return list(resolved.keys())