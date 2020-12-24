# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nushell/filter.py
# Compiled at: 2019-10-27 12:42:09
# Size of source mod 2**32: 5804 bytes
from nushell.plugin import PluginBase
import copy, fileinput, json

class FilterPlugin(PluginBase):
    __doc__ = 'A filter plugin is identified by is_filter set to true in the\n       configuration, and interacts with nushell by way of nushell\n       asking for the configuration upon discovery on the path (method "config")\n       and then returning responses to begin_filter, end_filter, and filter.\n    '
    args = {}
    params = {}
    is_filter = True

    def get_string_primitive(self):
        return self.get_primitive('String')

    def get_int_primitive(self):
        return self.get_primitive('Int')

    def get_primitive(self, primitive_type=None):
        """get a primitive from an item, expected to be of a type (String
           or Int typically). We get this from last passed params.
        """
        if primitive_type:
            return self.params['item']['Primitive'][primitive_type]
        return list(self.params['item']['Primitive'].values())[0]

    def print_primitive_response(self, value, primitive_type, return_response=False):
        """a base function to print a good response with an updated
           value for a primitive type.
           Parameters
           ==========
           value: The primitive value, expected to match the type
           primitive_type: one of Int or String
           return_response: if True, just return (don't print)
        """
        primitive_type = self._camel_case(primitive_type)
        item = {'Primitive': {primitive_type: value}}
        response = copy.deepcopy(self.params)
        response['item'] = item
        response = [{'Ok': {'Value': response}}]
        if return_response:
            return response
        self.print_good_response(response)

    def print_int_response(self, value):
        return self.print_primitive_response(value, 'Int')

    def print_string_response(self, value):
        return self.print_primitive_response(value, 'String')

    def test(self, runFilter, line):
        """given a line, test the response
        """
        method = line.get('method')
        if method != 'end_filter':
            self.params = line.get('params', {})
        if method == 'config':
            plugin_config = self.get_config()
            return self.get_good_response(plugin_config)
        if method == 'begin_filter':
            self.args = self.parse_params(self.params)
            return self.get_good_response([])
        if method == 'end_filter':
            if 'help' in self.args:
                self.params['tag'] = self.params.get('name_tag', self.getTag())
                return self.print_primitive_response(self.get_help(), 'String', True)
            return self.get_good_response([])
        if method == 'filter':
            return runFilter(self, self.args)

    def run(self, runFilter):
        """the main run function is required to take a user runFilter function.
        """
        for line in fileinput.input():
            x = json.loads(line)
            method = x.get('method')
            self.logger.info('REQUEST %s' % line)
            self.logger.info('METHOD %s' % method)
            if method != 'end_filter':
                self.params = x.get('params', {})
            if method == 'config':
                plugin_config = self.get_config()
                self.logger.info('plugin-config: %s' % json.dumps(plugin_config))
                self.print_good_response(plugin_config)
                break
            elif method == 'begin_filter':
                self.args = self.parse_params(self.params)
                self.logger.info('Begin Filter Args: %s' % self.args)
                self.print_good_response([])
            elif method == 'end_filter':
                if 'help' in self.args:
                    self.params['tag'] = self.params.get('name_tag', self.getTag())
                    self.logger.info('User requested --help')
                    self.print_string_response(self.get_help())
                else:
                    self.print_good_response([])
                break
            elif method == 'filter':
                self.logger.info('RAW PARAMS: %s' % self.params)
                runFilter(self, self.args)
            else:
                break