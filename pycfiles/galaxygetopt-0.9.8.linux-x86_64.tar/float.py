# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/users/cpt/cpt/esr/Projects/galaxy/galaxygetopt/env/lib/python2.7/site-packages/galaxygetopt/parameter/float.py
# Compiled at: 2014-07-07 15:44:50
from parameter import Parameter
import xml.etree.cElementTree as ET

class Float(Parameter):

    def galaxy_input(self, xml_node):
        node_of_interest = None
        possible_repeat_node = self.handle_possible_galaxy_input_repeat_start(xml_node)
        if possible_repeat_node is not None:
            node_of_interest = ET.SubElement(possible_repeat_node, 'param')
        else:
            node_of_interest = ET.SubElement(xml_node, 'param')
        params = self.get_default_input_parameters('float')
        if 'min' in self.child_params and self.child_params['min'] is not None:
            params['min'] = str(self.child_params['min'])
        if 'max' in self.child_params and self.child_params['max'] is not None:
            params['max'] = str(self.child_params['max'])
        for key in params:
            node_of_interest.set(key, params[key])

        return

    def galaxy_output(self, xml_node):
        return

    def validate_individual(self, val):
        try:
            float(val)
            if 'max' in self.child_params and self.child_params['max'] is not None:
                if val > self.child_params['max']:
                    self.errors.append('Value passed with %s was greater than the allowable upper bound. [%s > %s]' % (
                     self.name, val,
                     self.child_params['max']))
                    return False
            if 'min' in self.child_params and self.child_params['min'] is not None:
                if val < self.child_params['min']:
                    self.errors.append('Value passed with %s was less than the allowable minimum bound. [%s > %s]' % (
                     self.name, val,
                     self.child_params['min']))
                    return False
        except ValueError:
            self.errors.append('Not a float')
            return False

        return True