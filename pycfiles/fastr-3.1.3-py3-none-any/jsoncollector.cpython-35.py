# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hachterberg/dev/fastr/fastr/fastr/resources/plugins/collectorplugins/jsoncollector.py
# Compiled at: 2018-12-19 07:29:10
# Size of source mod 2**32: 3020 bytes
__author__ = 'hachterberg'
import json, re, fastr
from fastr import exceptions
from fastr.plugins import FastrInterface

class JsonCollector(FastrInterface.collector_plugin_type):
    __doc__ = "\n    The JsonCollector plugin allows a program to print out the result in a\n    pre-defined JSON format. It is then used as values for fastr.\n\n    The working is as follows:\n\n    1. The location of the output is taken\n    2. If the location is ``None``, go to step 5\n    3. The substitutions are performed on the location field (see below)\n    4. The location is used as a :ref:`regular expression <python:re-syntax>` and matched to the stdout line by line\n    5. The matched string (or entire stdout if location is ``None``) is :py:func:`loaded as a json <python:json.loads>`\n    6. The data is parsed by :py:meth:`set_result <fastr.planning.node.NodeRun.set_result>`\n\n    The structure of the JSON has to follow the a predefined format. For normal\n    :py:class:`Nodes <fastr.planning.node.NodeRun>` the format is in the form::\n\n      [value1, value2, value3]\n\n    where the multiple values represent the cardinality.\n\n    For a :py:class:`FlowNodes <fastr.planning.node.FlowNodeRun>` the format is the form::\n\n      {\n        'sample_id1': [value1, value2, value3],\n        'sample_id2': [value4, value5, value6]\n      }\n\n    This allows the tool to create multiple output samples in a single run.\n    "

    def __init__(self):
        super(JsonCollector, self).__init__()
        self.id = 'json'

    def _collect_results(self, interface, output, result):
        location = output.location
        stdout = result.target_result.stdout
        if location is not None:
            cardinality = 0
            fastr.log.debug('Searching for {}'.format(location))
            specials, inputs, outputs = interface.get_specials(result.payload, output, cardinality)
            loc = location.format(input=inputs, output=outputs, special=specials, input_parts=inputs, output_parts=outputs)
            for line in stdout.splitlines():
                match = re.search(loc, line)
                if match is not None:
                    value = match.group(1)
                    break
            else:
                raise exceptions.FastrCollectorError('[{}] Could not find {} in stdout'.format(output.id, loc))

        else:
            value = stdout
        fastr.log.info('Setting data for {} with {}'.format(output.id, value))
        value = json.loads(value)
        if not isinstance(value, (list, dict)):
            value = [
             value]
        result.result_data[output.id] = value