# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/luoxi/Project/yunify/qingcloud-cli/qingcloud/cli/iaas_client/actions/lb/add_loadbalancer_policy_rules.py
# Compiled at: 2017-09-21 02:37:46
import json
from qingcloud.cli.iaas_client.actions.base import BaseAction

class AddLoadBalancerPolicyRulesAction(BaseAction):
    action = 'AddLoadBalancerPolicyRules'
    command = 'add-loadbalancer-policy-rules'
    usage = '%(prog)s -p <loadbalancer_policy> -r <rules> [-f <conf_file>]'
    description = 'Add policy rules to loadbalancer'

    @classmethod
    def add_ext_arguments(cls, parser):
        parser.add_argument('-p', '--loadbalancer_policy', dest='loadbalancer_policy', action='store', type=str, default='', help='the ID of loadbalancer_policy whose rules you want to add. ')
        parser.add_argument('-r', '--rules', dest='rules', action='store', type=str, default='', help='a json string of rules list. \n                    e.g. \'[{"rule_type":"domain","val":"www.qingcloud.com"},{"rule_type":"url","val":"/scripts"}]\' ')

    @classmethod
    def build_directive(cls, options):
        required_params = {'loadbalancer_policy': options.loadbalancer_policy, 
           'rules': options.rules}
        for param in required_params:
            if required_params[param] is None or required_params[param] == '':
                print 'error: [%s] should be specified' % param
                return

        loadbalancer_policy = options.loadbalancer_policy
        rules = json.loads(options.rules)
        if rules is None or len(rules) == 0 or len(loadbalancer_policy) == 0:
            return
        return {'loadbalancer_policy': loadbalancer_policy, 'rules': rules}