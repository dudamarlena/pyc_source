# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/roboticslanguage/RoboticsLanguage/RoboticsLanguage/Base/Inputs.py
# Compiled at: 2019-09-27 03:30:17
from . import Utilities

def Parse(file_name, file_type, parameters):
    """Parses the robotics language and converts to XML"""
    if file_name is not None:
        with open(file_name) as (file):
            text = file.read()
        parameters['text'] = text
        for key, value in parameters['manifesto']['Inputs'].iteritems():
            if file_type.lower() == value['fileFormat'].lower() and parameters['globals']['input'] == '' or parameters['globals']['input'] == value['packageShortName']:
                parameters = Utilities.incrementCompilerStep(parameters, 'Inputs', value['packageShortName'])
                parsing_function = Utilities.importModule(value['type'], 'Inputs', value['packageShortName'], 'Parse')
                code, parameters = parsing_function.Parse.parse(text, parameters)
                Utilities.showDeveloperInformation(code, parameters)
                return (
                 code, parameters)

    else:
        parameters['developer']['step'] = 0
        Utilities.showDeveloperInformation(None, parameters)
    return (None, parameters)