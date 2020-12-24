# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nushell/sink.py
# Compiled at: 2019-10-27 12:40:10
# Size of source mod 2**32: 4863 bytes
from nushell.plugin import PluginBase
import fileinput, json

class SinkPlugin(PluginBase):
    __doc__ = 'A sink plugin is identified by is_filter set to false in the\n       configuration, and interacts with nushell by way of nushell\n       asking for the configuration upon discovery on the path (method "config")\n       and then passing a temporary file as argument (method "sink")\n    '
    is_filter = False
    parse_pipe = True

    def get_sink_params(self, input_params):
        """The input params (under ["params"] is a list, with the first entry
           being the args dictionary (that we pass to self.parse_params) and
           the remaining being entries that are passed if the sink is used as 
           a pipe. If not, it looks like an empty list, like below:

          [{'args': {'positional': None,
             'named': {'switch': {'tag': {'anchor': None,
                'span': {'start': 58, 'end': 64}},
               'item': {'Primitive': {'Boolean': True}}},
              'mandatory': {'tag': {'anchor': None, 'span': {'start': 20, 'end': 32}},
               'item': {'Primitive': {'String': 'MANDATORYARG'}}},
              'optional': {'tag': {'anchor': None, 'span': {'start': 44, 'end': 55}},
               'item': {'Primitive': {'String': 'OPTIONALARG'}}}}},
            'name_tag': {'anchor': None, 'span': {'start': 0, 'end': 7}}},
           []]
        """
        if not input_params:
            return input_params
        args = input_params.pop(0)
        params = self.parse_params(args)
        params['_pipe'] = self._parse_pipe(input_params)
        return params

    def _parse_pipe(self, pipeList):
        """parse the list of piped input, typically this means string that
           have come from the terminal. To disable this, set the client
           parse_pipe to False.

           Parameters
           ==========
           pipeList: is the second index of the "params" dict from the request
        """
        return pipeList and self.parse_pipe or pipeList
        pipeList = pipeList.pop(0)
        return self.parse_primitives(pipeList)

    def test(self, sinkFunc, line):
        """test is akin to run, but instead of printing a result for the user,
           we return to the calling function. A line to parse is also required.
           since it's coming from Python, we also assume that we don't need to
           json.loads() the line from a string (it's a dictionary)
        """
        method = line.get('method')
        if method == 'config':
            plugin_config = self.get_config()
            return self.get_good_response(plugin_config)
        if method == 'sink':
            params = self.get_sink_params(line['params'])
            if params.get('help', False):
                return self.get_help()
            return sinkFunc(self, params)

    def run(self, sinkFunc):
        """the main run function is required to take a user sinkFunc.
        """
        for line in fileinput.input():
            x = json.loads(line)
            method = x.get('method')
            self.logger.info('REQUEST %s' % line)
            self.logger.info('METHOD %s' % method)
            if method == 'config':
                plugin_config = self.get_config()
                self.logger.info('plugin-config: %s' % json.dumps(plugin_config))
                self.print_good_response(plugin_config)
                break
            elif method == 'sink':
                params = self.get_sink_params(x['params'])
                self.logger.info('PARAMS %s' % params)
                if params.get('help', False):
                    print(self.get_help())
                else:
                    sinkFunc(self, params)
                break