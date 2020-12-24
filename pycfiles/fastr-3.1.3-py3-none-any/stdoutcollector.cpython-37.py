# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hachterberg/dev/fastr/fastr/fastr/resources/plugins/collectorplugins/stdoutcollector.py
# Compiled at: 2019-06-04 03:32:43
# Size of source mod 2**32: 3608 bytes
__author__ = 'hachterberg'
import re, fastr
from fastr.plugins import FastrInterface

class StdoutCollector(FastrInterface.collector_plugin_type):
    __doc__ = '\n    The StdoutCollector can collect data from the stdout stream of a program.\n    It filters the ``stdout`` line by line matching a predefined regular expression.\n\n    The general working is as follows:\n\n    1. The location field is taken from the output\n    2. The substitutions are performed on the location field (see below)\n    3. The updated location field will be used as a :ref:`regular expression <python:re-syntax>` filter\n    4. The ``stdout`` is scanned line by line and the :ref:`regular expression <python:re-syntax>` filter is applied\n\n    The special substitutions performed on the location use the\n    Format Specification Mini-Language :ref:`python:formatspec`.\n    The predefined fields that can be used are:\n\n    * ``inputs``, an objet with the input values (use like ``{inputs.image[0]}``)\n    * ``outputs``, an object with the output values (use like ``{outputs.result[0]}``)\n    * ``special`` which has two subfields:\n\n      * ``special.cardinality``, the index of the current cardinality\n      * ``special.extension``, is the extension for the output DataType\n\n    .. note:: because the plugin scans line by line, it is impossible to catch\n              multi-line output into a single value\n    '

    def __init__(self):
        super(StdoutCollector, self).__init__()
        self.id = 'stdout'

    def _collect_results(self, interface, output, result):
        output_data = []
        result.result_data[output.id] = output_data
        location = output.location
        stdout = result.target_result.stdout
        cardinality = 0
        fastr.log.debug('Searching for {}'.format(location))
        specials, inputs, outputs = interface.get_specials(result.payload, output, cardinality)
        loc = location.format(input=inputs, output=outputs,
          special=specials,
          input_parts=inputs,
          output_parts=outputs)
        for line in stdout.splitlines():
            match = re.search(loc, line)
            if match is not None:
                value = '{regexp[0]}'.format(input=inputs, output=outputs,
                  special=specials,
                  input_parts=inputs,
                  output_parts=outputs,
                  regexp=(match.groups()))
                if output.separator is not None:
                    value = value.split(output.separator)
                else:
                    value = [
                     value]
                for val in value:
                    fastr.log.info('Found value: {}'.format(val))
                    output_data.append(val)
                    cardinality += 1

                specials, inputs, outputs = interface.get_specials(result.payload, output, cardinality)
                loc = location.format(input=inputs, output=outputs,
                  special=specials,
                  input_parts=inputs,
                  output_parts=outputs)