# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/users/cpt/cpt/esr/Projects/galaxy/galaxygetopt/env/lib/python2.7/site-packages/galaxygetopt/parameter/flag.py
# Compiled at: 2014-07-07 15:44:50
from parameter import Parameter
import xml.etree.cElementTree as ET

class Flag(Parameter):

    def galaxy_command(self):
        value = self.get_galaxy_command_identifier()
        if self.hidden and self._galaxy_specific:
            value = self.default
        string = self.handle_possible_galaxy_command_repeat_start()
        if self.required:
            string += '--%s\n' % (self.get_galaxy_cli_identifier(),)
        else:
            if not self.multiple:
                string += '#if $%s:\n' % (self.get_galaxy_cli_identifier(),)
            string += '--%s\n' % (self.get_galaxy_cli_identifier(),)
            if not self.multiple:
                string += '#end if\n'
        string += self.handle_possible_galaxy_command_repeat_end()
        return string

    def galaxy_input(self, xml_node):
        node_of_interest = None
        possible_repeat_node = self.handle_possible_galaxy_input_repeat_start(xml_node)
        if possible_repeat_node is not None:
            node_of_interest = ET.SubElement(possible_repeat_node, 'param')
        else:
            node_of_interest = ET.SubElement(xml_node, 'param')
        params = self.get_default_input_parameters('boolean')
        params['falsevalue'] = 'False'
        params['truevalue'] = 'True'
        if self.default:
            params['checked'] = 'True'
        else:
            params['checked'] = ''
        try:
            del params['value']
        except KeyError:
            pass

        for key in params:
            node_of_interest.set(key, params[key])

        return

    def galaxy_output(self, xml_node):
        return

    def validate_individual(self, value):
        return True