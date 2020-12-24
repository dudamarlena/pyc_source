# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/lib/python2.7/site-packages/crmsh/constants.py
# Compiled at: 2016-05-25 17:40:26
from .ordereddict import odict
keywords = {'node': 'element', 
   'primitive': 'element', 
   'resource': 'element', 
   'group': 'element', 
   'clone': 'element', 
   'ms': 'element', 
   'master': 'element', 
   'location': 'element', 
   'colocation': 'element', 
   'collocation': 'element', 
   'order': 'element', 
   'rsc_ticket': 'element', 
   'rsc_template': 'element', 
   'property': 'element', 
   'rsc_defaults': 'element', 
   'op_defaults': 'element', 
   'acl_target': 'element', 
   'acl_group': 'element', 
   'user': 'element', 
   'role': 'element', 
   'fencing_topology': 'element', 
   'fencing-topology': 'element', 
   'tag': 'element', 
   'monitor': 'element', 
   'params': 'subelement', 
   'meta': 'subelement', 
   'attributes': 'subelement', 
   'utilization': 'subelement', 
   'operations': 'subelement', 
   'op': 'subelement', 
   'rule': 'subelement', 
   'inf': 'value', 
   'INFINITY': 'value', 
   'and': 'op', 
   'or': 'op', 
   'lt': 'op', 
   'gt': 'op', 
   'lte': 'op', 
   'gte': 'op', 
   'eq': 'op', 
   'ne': 'op', 
   'defined': 'op', 
   'not_defined': 'op', 
   'in_range': 'op', 
   'in': 'op', 
   'date_spec': 'op', 
   'spec': 'op', 
   'date': 'value', 
   'yes': 'value', 
   'no': 'value', 
   'true': 'value', 
   'false': 'value', 
   'on': 'value', 
   'off': 'value', 
   'normal': 'value', 
   'member': 'value', 
   'ping': 'value', 
   'remote': 'value', 
   'start': 'value', 
   'stop': 'value', 
   'Mandatory': 'value', 
   'Optional': 'value', 
   'Serialize': 'value', 
   'ref': 'value', 
   'xpath': 'value', 
   'xml': 'element'}
cib_cli_map = {'node': 'node', 
   'primitive': 'primitive', 
   'group': 'group', 
   'clone': 'clone', 
   'master': 'ms', 
   'rsc_location': 'location', 
   'rsc_colocation': 'colocation', 
   'rsc_order': 'order', 
   'rsc_ticket': 'rsc_ticket', 
   'template': 'rsc_template', 
   'cluster_property_set': 'property', 
   'rsc_defaults': 'rsc_defaults', 
   'op_defaults': 'op_defaults', 
   'acl_target': 'acl_target', 
   'acl_group': 'acl_group', 
   'acl_user': 'user', 
   'acl_role': 'role', 
   'fencing-topology': 'fencing_topology', 
   'tag': 'tag'}
container_tags = ('group', 'clone', 'ms', 'master')
clonems_tags = ('clone', 'ms', 'master')
resource_tags = ('primitive', 'group', 'clone', 'ms', 'master', 'template')
constraint_tags = ('rsc_location', 'rsc_colocation', 'rsc_order', 'rsc_ticket')
constraint_rsc_refs = ('rsc', 'with-rsc', 'first', 'then')
children_tags = ('group', 'primitive')
nvpairs_tags = ('meta_attributes', 'instance_attributes', 'utilization')
defaults_tags = ('rsc_defaults', 'op_defaults')
resource_cli_names = ('primitive', 'group', 'clone', 'ms', 'master', 'rsc_template')
constraint_cli_names = ('location', 'colocation', 'collocation', 'order', 'rsc_ticket')
nvset_cli_names = ('property', 'rsc_defaults', 'op_defaults')
op_cli_names = ('monitor', 'start', 'stop', 'migrate_to', 'migrate_from', 'promote',
                'demote', 'notify', 'reload')
ra_operations = tuple(['probe'] + list(op_cli_names))
subpfx_list = {'instance_attributes': 'instance_attributes', 
   'meta_attributes': 'meta_attributes', 
   'utilization': 'utilization', 
   'operations': 'ops', 
   'rule': 'rule', 
   'expression': 'expression', 
   'date_expression': 'expression', 
   'duration': 'duration', 
   'date_spec': 'date_spec', 
   'read': 'read', 
   'write': 'write', 
   'deny': 'deny'}
acl_rule_names = ('read', 'write', 'deny')
acl_spec_map = odict({'xpath': 'xpath', 
   'ref': 'ref', 
   'tag': 'tag', 
   'attribute': 'attribute'})
acl_spec_map_2 = odict({'xpath': 'xpath', 
   'ref': 'reference', 
   'reference': 'reference', 
   'tag': 'object-type', 
   'type': 'object-type', 
   'attr': 'attribute', 
   'attribute': 'attribute'})
acl_spec_map_2_rev = (
 ('xpath', 'xpath'),
 ('reference', 'ref'),
 ('attribute', 'attr'),
 ('object-type', 'type'))
acl_shortcuts = {'meta': ("//primitive\\[@id='@@'\\]/meta_attributes", "/nvpair\\[@name='@@'\\]"), 
   'params': ("//primitive\\[@id='@@'\\]/instance_attributes", "/nvpair\\[@name='@@'\\]"), 
   'utilization': ("//primitive\\[@id='@@'\\]/utilization", ), 
   'location': ("//rsc_location\\[@id='cli-prefer-@@' and @rsc='@@'\\]", ), 
   'property': ('//crm_config/cluster_property_set', "/nvpair\\[@name='@@'\\]"), 
   'nodeattr': ('//nodes/node/instance_attributes', "/nvpair\\[@name='@@'\\]"), 
   'nodeutil': ('//nodes/node/utilization', "\\[@uname='@@'\\]"), 
   'node': ('//nodes/node', "\\[@uname='@@'\\]"), 
   'status': ('/cib/status', ), 
   'cib': ('/cib', )}
lrm_exit_codes = {'success': '0', 
   'unknown': '1', 
   'args': '2', 
   'unimplemented': '3', 
   'perm': '4', 
   'installed': '5', 
   'configured': '6', 
   'not_running': '7', 
   'master': '8', 
   'failed_master': '9'}
lrm_status_codes = {'pending': '-1', 
   'done': '0', 
   'cancelled': '1', 
   'timeout': '2', 
   'notsupported': '3', 
   'error': '4'}
cib_user_attrs = ('validate-with', )
node_states = ('online', 'offline', 'unclean')
precious_attrs = ('id-ref', )
op_extra_attrs = ('interval', )
rsc_meta_attributes = ('allow-migrate', 'maintenance', 'is-managed', 'interval-origin',
                       'migration-threshold', 'priority', 'multiple-active', 'failure-timeout',
                       'resource-stickiness', 'target-role', 'restart-type', 'description',
                       'remote-node', 'requires', 'provides', 'remote-port', 'remote-addr',
                       'remote-connect-timeout')
group_meta_attributes = ('container', )
clone_meta_attributes = ('ordered', 'notify', 'interleave', 'globally-unique', 'clone-max',
                         'clone-node-max', 'clone-state', 'description', 'clone-min')
ms_meta_attributes = ('master-max', 'master-node-max', 'description')
alert_meta_attributes = ('timeout', 'timestamp-format')
trace_ra_attr = 'trace_ra'
score_types = {'advisory': '0', 'mandatory': 'INFINITY'}
boolean_ops = ('or', 'and')
binary_ops = ('lt', 'gt', 'lte', 'gte', 'eq', 'ne')
binary_types = ('string', 'version', 'number')
unary_ops = ('defined', 'not_defined')
simple_date_ops = ('lt', 'gt')
date_ops = ('lt', 'gt', 'in_range', 'date_spec')
date_spec_names = ('hours monthdays weekdays yearsdays months weeks years weekyears moon').split()
in_range_attrs = ('start', 'end')
roles_names = ('Stopped', 'Started', 'Master', 'Slave')
actions_names = ('start', 'promote', 'demote', 'stop')
node_default_type = 'normal'
node_attributes_keyw = ('attributes', 'utilization')
shadow_envvar = 'CIB_shadow'
attr_defaults = {'node': {'type': 'normal'}, 'resource_set': {'sequential': 'true', 'require-all': 'true'}, 'rule': {'boolean-op': 'and'}}
cib_no_section_rc = 6
graph = {'.': {'compound': 'true'}, 
   '*': {'fontname': 'Helvetica', 
         'fontsize': '11'}, 
   'node': {'style': 'bold', 
            'shape': 'box', 
            'color': '#7ac142'}, 
   'primitive': {'fillcolor': '#e4e5e6', 
                 'color': '#b9b9b9', 
                 'shape': 'box', 
                 'style': 'rounded,filled'}, 
   'rsc_template': {'fillcolor': '#ffd457', 
                    'color': '#b9b9b9', 
                    'shape': 'box', 
                    'style': 'rounded,filled,dashed'}, 
   'class:stonith': {'shape': 'box', 
                     'style': 'dashed'}, 
   'location': {'style': 'dashed', 
                'dir': 'none'}, 
   'clone': {'color': '#ec008c'}, 
   'ms': {'color': '#f8981d'}, 
   'group': {'color': '#00aeef', 
             'group': '#00aeef', 
             'labelloc': 'b', 
             'labeljust': 'r', 
             'labelfontsize': '12'}, 
   'optional_set': {'style': 'dotted'}, 
   'template:edge': {'color': '#b9b9b9', 
                     'style': 'dotted', 
                     'arrowtail': 'open', 
                     'dir': 'back'}}
prompt = ''
tmp_cib = False
tmp_cib_prompt = '@tmp@'
live_cib_prompt = 'live'
simulate_programs = {'ptest': 'ptest', 
   'simulate': 'crm_simulate'}
meta_progs = ('crmd', 'pengine', 'stonithd', 'cib')
crmd_metadata_do_not_complete = ('dc-version', 'cluster-infrastructure', 'crmd-integration-timeout',
                                 'crmd-finalization-timeout', 'expected-quorum-votes')
extra_cluster_properties = ('dc-version', 'cluster-infrastructure', 'last-lrm-refresh',
                            'cluster-name')
pcmk_version = ''