# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/ecs/cart/rules/rules_config.py
# Compiled at: 2009-01-13 06:18:21
"""This script load dynamically rules in fonction of conf files"""
import os
from ConfigParser import SafeConfigParser
from standard_rules import ObjectReduction, ObjectAmount, CartReduction, CartAmount

class RulesInit(object):
    """This class will load rules chain from the conf file and initializing
    it"""

    def __init__(self, conf_file=None):
        if conf_file is not None:
            if not os.path.exists(conf_file):
                raise IOError('%s does not exists' % os.path.abspath(conf_file))
            confparser = SafeConfigParser()
            confparser.read(conf_file)
            self.connector = confparser.get('main', 'connector')
            rules_chains = confparser.items('rules')
            from paste.util.import_string import simple_import
            self.chain = {}
            for (chain_name, chain) in rules_chains:
                chain = chain.replace('\n', ' ')
                process = None
                for module in chain.split(' '):
                    rule = simple_import(module)
                    process = rule(process)

                self.chain[chain_name] = process

        else:
            self.connector = 'standard'
            amount_chain = [CartReduction, CartAmount, ObjectReduction,
             ObjectAmount]
            process = None
            for rule in amount_chain:
                process = rule(process)

            self.chain = {'amount': process}
        return

    def amount_chain(self, cart):
        return self.chain['amount'](cart)