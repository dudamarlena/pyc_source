# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hachterberg/dev/fastr/fastr/fastr/resources/plugins/collectorplugins/jsoncollector.py
# Compiled at: 2019-06-04 03:03:06
__author__ = 'hachterberg'
import json, re, fastr
from fastr import exceptions
from fastr.plugins import FastrInterface

class JsonCollector(FastrInterface.collector_plugin_type):
    """
    The JsonCollector plugin allows a program to print out the result in a
    pre-defined JSON format. It is then used as values for fastr.

    The working is as follows:

    1. The location of the output is taken
    2. If the location is ``None``, go to step 5
    3. The substitutions are performed on the location field (see below)
    4. The location is used as a :ref:`regular expression <python:re-syntax>` and matched to the stdout line by line
    5. The matched string (or entire stdout if location is ``None``) is :py:func:`loaded as a json <python:json.loads>`
    6. The data is parsed by :py:meth:`set_result <fastr.core.node.NodeRun.set_result>`

    The structure of the JSON has to follow the a predefined format. For normal
    :py:class:`Nodes <fastr.core.node.NodeRun>` the format is in the form::

      [value1, value2, value3]

    where the multiple values represent the cardinality.

    For a :py:class:`FlowNodes <fastr.core.node.FlowNodeRun>` the format is the form::

      {
        'sample_id1': [value1, value2, value3],
        'sample_id2': [value4, value5, value6]
      }

    This allows the tool to create multiple output samples in a single run.
    """

    def __init__(self):
        super(JsonCollector, self).__init__()
        self.id = 'json'

    def _collect_results(self, interface, output, result):
        location = output.location
        stdout = result.log_data['stdout']
        if location is not None:
            cardinality = 0
            fastr.log.debug(('Searching for {}').format(location))
            specials, inputs, outputs = interface.get_specials(result.payload, output, cardinality)
            loc = location.format(input=inputs, output=outputs, special=specials, input_parts=inputs, output_parts=outputs)
            for line in stdout.splitlines():
                match = re.search(loc, line)
                if match is not None:
                    value = match.group(1)
                    break
            else:
                raise exceptions.FastrCollectorError(('[{}] Could not find {} in stdout').format(output.id, loc))

        else:
            value = stdout
        fastr.log.info(('Setting data for {} with {}').format(output.id, value))
        value = json.loads(value)
        if not isinstance(value, (list, dict)):
            value = [
             value]
        result.result_data[output.id] = value
        return