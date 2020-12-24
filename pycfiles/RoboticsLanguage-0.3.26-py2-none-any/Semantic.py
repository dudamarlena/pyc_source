# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/roboticslanguage/RoboticsLanguage/RoboticsLanguage/Tools/Semantic.py
# Compiled at: 2019-09-27 03:30:17
import sys
from RoboticsLanguage.Base import Utilities, Types
from RoboticsLanguage.Tools import Exceptions

def Checker(code, parameters):
    """Generic semantic checking function"""
    code, parameters = TypeChecker(code, parameters)
    code, parameters = DefiniteAssignment(code, parameters)
    return (
     code, parameters)


def TypeChecker(code, parameters):
    """Generic type checking function"""
    code, parameters = AtomsTypeChecker(code, parameters)
    code, parameters = TypesTypeChecker(code, parameters)
    code, parameters = VariablesTypeChecker(code, parameters)
    code, parameters = FunctionsTypeChecker(code, parameters)
    code, parameters = RecursiveTypeChecker(code, parameters)
    return (
     code, parameters)


def AtomsTypeChecker(code, parameters):
    [ x.set('type', type) for type in Types.type_atomic for x in code.xpath('//' + type)
    ]
    return (
     code, parameters)


def TypesTypeChecker(code, parameters):
    return (
     code, parameters)


def VariablesTypeChecker(code, parameters):
    for variable in code.xpath('/node/option[@name="definitions"]//element'):
        variable_name = variable.getchildren()[0].attrib['name']
        variable_definition = variable.getchildren()[1]
        variable_definition, parameters = RecursiveTypeChecker(variable_definition, parameters)
        for variable_used in code.xpath('//variable[@name="' + variable_name + '"]'):
            variable_used.attrib['type'] = variable_definition.attrib['type']

    for variable in code.xpath('/node/option[@name!="definitions"]//element'):
        variable_name = variable.getchildren()[0].attrib['name']
        variable_definition = variable.getchildren()[1]
        variable_definition, parameters = RecursiveTypeChecker(variable_definition, parameters)
        for variable_used in variable.getparent().xpath('//variable[@name="' + variable_name + '"]'):
            variable_used.attrib['type'] = variable_definition.attrib['type']

    return (
     code, parameters)


def FunctionsTypeChecker(code, parameters):
    functions = {}
    for function in code.xpath('//function_definition'):
        function_name = function.attrib['name']
        functions[function_name] = {'mandatory': [], 'optional': {}, 'returns': []}
        print '----------------------' + function_name + '-------------------'
        Utilities.printCode(function)
        print 'Function arguments ============'
        arguments = function.xpath('function_arguments')
        if len(arguments) > 0:
            for argument in arguments[0].getchildren():
                argument, parameters = RecursiveTypeChecker(argument, parameters)
                if argument.tag == 'element':
                    functions[function_name]['mandatory'].append(argument.xpath('variable')[0].attrib['type'])
                if argument.tag == 'assign':
                    functions[function_name]['optional'][argument.xpath('element/variable')[0].attrib['name']] = argument.xpath('element/variable')[0].attrib['type']

        Utilities.printParameters(functions)

    return (
     code, parameters)


def RecursiveTypeChecker(code, parameters):
    if 'type' in code.attrib.keys():
        return (code, parameters)
    else:
        if code.tag in parameters['language']:
            for element in code.getchildren():
                element, parameters = RecursiveTypeChecker(element, parameters)

            if code.tag == 'option':
                if len(code.getchildren()) > 0:
                    code.attrib['type'] = code.getchildren()[0].attrib['type']
                else:
                    code.attrib['type'] = 'none'
                return (
                 code, parameters)
            optional_names = code.xpath('option/@name')
            optional_types = code.xpath('option/@type')
            argument_types = code.xpath('*[not(self::option)]/@type')
            keys = parameters['language']
            try:
                if 'optional' in keys[code.tag]['definition']:
                    if all([ x in keys[code.tag]['definition']['optional'].keys() for x in optional_names ]):
                        if not all(map(lambda x, y: keys[code.tag]['definition']['optional'][x]['test']([y]), optional_names, optional_types)):
                            Utilities.errorOptionalArgumentTypes(code, parameters, optional_names, optional_types)
                    else:
                        Utilities.errorOptionalArgumentNotDefined(code, parameters, optional_names)
                if keys[code.tag]['definition']['arguments']['test'](argument_types):
                    code.attrib['type'] = keys[code.tag]['definition']['returns'](argument_types)
                else:
                    Utilities.errorArgumentTypes(code, parameters, argument_types)
            except:
                Utilities.errorLanguageDefinition(code, parameters)
                sys.exit(1)

            return (
             code, parameters)
        return (
         code, parameters)


def DefiniteAssignment(code, parameters):
    return (
     code, parameters)