# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/roboticslanguage/RoboticsLanguage/RoboticsLanguage/Base/Outputs.py
# Compiled at: 2019-09-27 03:30:17
from . import Utilities

@Utilities.cache_in_disk
def prepareOutputs(parameters):
    outputs = parameters['manifesto']['Outputs']
    return [ {'data': outputs[x], 'name': x} for x in sorted(outputs, key=lambda k: outputs[k]['order'])
           ]


def Generate(code, parameters):
    """Generates the outputs"""
    outputs = parameters['globals']['output']
    sorted_outputs = prepareOutputs(parameters)
    for output in map(lambda k: k['name'], sorted_outputs):
        if output in outputs:
            if code is not None or code is None and 'requiresCode' in parameters['manifesto']['Outputs'][output].keys() and not parameters['manifesto']['Outputs'][output]['requiresCode']:
                parameters = Utilities.incrementCompilerStep(parameters, 'Outputs', output)
                output_function = Utilities.importModule(parameters['manifesto']['Outputs'][output]['type'], 'Outputs', output, 'Output')
                output_function.Output.output(code, parameters)
                Utilities.showDeveloperInformation(code, parameters)

    if parameters['developer']['progress']:
        Utilities.progressDone(parameters)
    return