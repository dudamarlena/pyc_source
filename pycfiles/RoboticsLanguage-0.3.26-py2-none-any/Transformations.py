# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/roboticslanguage/RoboticsLanguage/RoboticsLanguage/Base/Transformations.py
# Compiled at: 2019-09-27 03:30:17
import sys
from . import Utilities

@Utilities.cache_in_disk
def prepareTransformations(parameters):
    transformers = parameters['manifesto']['Transformers']
    return [ {'data': transformers[x], 'name': x} for x in sorted(transformers, key=lambda k: transformers[k]['order'])
           ]


def Apply(code, parameters):
    """Applies transformations to the XML structure"""
    ordered_transformations_list = prepareTransformations(parameters)
    transform_function_list = [ Utilities.importModule(t['data']['type'], 'Transformers', t['name'], 'Transform') for t in ordered_transformations_list
                              ]
    for transform_function, transform_name in zip(transform_function_list, [ x['name'] for x in ordered_transformations_list ]):
        if transform_name not in parameters['developer']['skip']:
            if code is not None or code is None and 'requiresCode' in parameters['manifesto']['Transformers'][transform_name].keys() and not parameters['manifesto']['Transformers'][transform_name]['requiresCode']:
                parameters = Utilities.incrementCompilerStep(parameters, 'Transformers', transform_name)
                code, parameters = transform_function.Transform.transform(code, parameters)
                Utilities.showDeveloperInformation(code, parameters)

    if len(parameters['errors']) > 0:
        Utilities.logging.error('Semantic errors found! Stopping.')
        sys.exit(1)
    return (code, parameters)