# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/users/cpt/cpt/esr/Projects/galaxy/galaxygetopt/env/lib/python2.7/site-packages/galaxygetopt/parameter/parameter.py
# Compiled at: 2014-07-07 15:44:50
import xml.etree.cElementTree as ET
from ..exceptions import RepeatRequestedFromNonMultiple

class Parameter(object):

    def __init__(self, name=None, short=None, multiple=False, description=None, default=None, required=False, hidden=False, errors=[], value=[], _galaxy_specific=False, _show_in_galaxy=True, _cheetah_var=False, **kwargs):
        self.name = name
        self.short = short
        self.multiple = multiple
        self.description = description
        if self.multiple:
            if default is not None:
                if isinstance(default, list):
                    self.default = default
                else:
                    self.default = [
                     default]
            else:
                self.default = []
        else:
            self.default = default
        self.required = required
        self.hidden = hidden
        self.errors = errors
        self.value = value
        self._galaxy_specific = _galaxy_specific
        self._show_in_galaxy = _show_in_galaxy
        self._cheetah_var = _cheetah_var
        self.child_params = {}
        for key in kwargs.keys():
            self.child_params[key] = kwargs[key]

        return

    def galaxy_command(self):
        value = self.get_galaxy_command_identifier()
        if self.hidden and self._galaxy_specific:
            if self._cheetah_var:
                value = '"${%s}"' % (self.get_default(),)
            else:
                value = '"' + str(self.get_default()) + '"'
        else:
            value = '"${%s}"' % (value,)
        string = self.handle_possible_galaxy_command_repeat_start()
        if self.required or self._galaxy_specific:
            string += '--%s %s\n' % (self.get_galaxy_cli_identifier(),
             value)
        else:
            if not self.multiple:
                string += '#if $%s and $%s is not "None":\n' % (
                 self.get_galaxy_cli_identifier(),
                 self.get_galaxy_cli_identifier())
            string += '--%s %s\n' % (self.get_galaxy_cli_identifier(),
             value)
            if not self.multiple:
                string += '#end if\n'
        string += self.handle_possible_galaxy_command_repeat_end()
        return string

    def get_galaxy_command_identifier(self):
        if self.multiple:
            return '%s.%s' % (self.get_repeat_idx_name(),
             self.get_galaxy_cli_identifier())
        else:
            return self.get_galaxy_cli_identifier()

    def get_galaxy_cli_identifier(self):
        return self.name

    def get_value(self):
        if self.value is not None:
            if self.multiple:
                if len(self.value) > 0:
                    return self.value[0]
                else:
                    return

            else:
                return self.value
        else:
            return
        return

    def get_default(self):
        if self.default is not None:
            if self.multiple:
                if len(self.default) > 0:
                    return self.default[0]
                else:
                    return

            else:
                return self.default
        else:
            return
        return

    def validate(self, possible_value):
        self.errors = []
        if self.multiple:
            if possible_value is not None and isinstance(possible_value, list):
                for val in possible_value:
                    self.validate_individual(val)

            elif possible_value is not None:
                self.validate_individual(possible_value)
            elif self.required:
                self.errors.append('Must specify a value')
        else:
            self.validate_individual(possible_value)
        if len(self.errors) == 0:
            return True
        else:
            for error in self.errors:
                print 'ERROR [%s] %s' % (self.get_galaxy_cli_identifier(), error)

            return False
            return

    def get_repeat_idx_name(self):
        return 'item'

    def get_repeat_name(self):
        if self.multiple:
            return 'repeat_%s' % (self.get_galaxy_cli_identifier(),)
        raise RepeatRequestedFromNonMultiple('Tried to get repeat name for non-multiple item')

    def handle_possible_galaxy_input_repeat_start(self, xml_node):
        if self.multiple:
            repeat_node = ET.SubElement(xml_node, 'repeat')
            repeat_node.set('name', self.get_repeat_name())
            repeat_node.set('title', self.get_galaxy_cli_identifier().title().replace('_', ' '))
            return repeat_node
        else:
            return
            return

    def handle_possible_galaxy_command_repeat_start(self):
        if self.multiple:
            return '#for $%s in $%s:\n' % (self.get_repeat_idx_name(),
             self.get_repeat_name())
        else:
            return ''

    def handle_possible_galaxy_command_repeat_end(self):
        if self.multiple:
            return '#end for\n'
        else:
            return ''

    def get_default_input_parameters(self, paramType):
        params = {'name': self.get_galaxy_cli_identifier(), 
           'optional': self.is_optional_galaxy(), 
           'label': self.get_galaxy_cli_identifier(), 
           'help': self.get_description(), 
           'type': paramType}
        if self.get_default() is not None:
            params['value'] = self.get_default()
            if params['value'] is None:
                params['value'] = ''
            if type(params['value']) is not str:
                params['value'] = str(params['value'])
        return params

    def get_description(self):
        if self.description is not None:
            return self.description
        else:
            return 'Author failed to supply a description'
            return

    def get_all_keys(self):
        kd = {}
        if self.name is not None:
            kd['name'] = self.name
        if self.short is not None:
            kd['short'] = self.short
        if self.multiple is not None:
            kd['multiple'] = self.multiple
        if self.description is not None:
            kd['description'] = self.description
        if self.default is not None:
            kd['default'] = self.default
        if self.required is not None:
            kd['required'] = self.required
        if self.hidden is not None:
            kd['hidden'] = self.hidden
        if self.errors is not None:
            kd['errors'] = self.errors
        if self.value is not None:
            kd['value'] = self.value
        for p in self.child_params:
            kd[p] = self.child_params[p]

        return kd

    def is_optional_galaxy(self):
        if self.required:
            return 'False'
        else:
            return 'True'

    def validate_individual(self, value):
        return True

    def galaxy_input(self):
        return

    def galaxy_output(self):
        return