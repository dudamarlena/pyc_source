# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/roboticslanguage/RoboticsLanguage/RoboticsLanguage/Base/Initialise.py
# Compiled at: 2019-11-01 11:02:50
import os, sys, time, signal
from . import Utilities
from . import Parameters
sys.setrecursionlimit(99999)

def exit_gracefully(*arguments):
    sys.exit(1)


signal.signal(signal.SIGINT, exit_gracefully)
signal.signal(signal.SIGTERM, exit_gracefully)

@Utilities.cache_in_disk
def prepareParameters():
    """Collects parameters, language, messages, and error handling functions from all list_of_modules.
  This function is cached in `rol`. To refresh the cache run `rol --remove-cache`."""
    parameters = Parameters.parameters
    sys.path.append(parameters['globals']['plugins'] + '/../')
    manifesto = {'Inputs': {}, 'Outputs': {}, 'Transformers': {}}
    parameters['Inputs'] = {}
    parameters['Outputs'] = {}
    parameters['Transformers'] = {}
    command_line_flags = {}
    package_order = {}
    for element in Utilities.findFileName('Manifesto.py', [parameters['globals']['RoboticsLanguagePath'] + '/../', parameters['globals']['plugins']]):
        name_split = element.split('/')[-4:-1]
        module_name = ('.').join(name_split)
        if len(name_split) == 3 and name_split[1] in ('Inputs', 'Outputs', 'Transformers'):
            try:
                manifesto_module = __import__(module_name + '.Manifesto', globals(), locals(), ['Manifesto'])
                manifesto[name_split[1]][name_split[2]] = manifesto_module.manifesto
                manifesto[name_split[1]][name_split[2]]['path'] = os.path.realpath(os.path.dirname(element))
                manifesto[name_split[1]][name_split[2]]['type'] = name_split[0]
                if 'order' in manifesto_module.manifesto.keys():
                    package_order[module_name] = manifesto_module.manifesto['order']
                elif name_split[1] == 'Inputs':
                    package_order[module_name] = -1
                elif name_split[1] == 'Outputs':
                    package_order[module_name] = 100000000
            except Exception as e:
                Utilities.logging.debug(e.__repr__())

    parameters['manifesto'] = manifesto
    parameters['globals']['loadOrder'] = sorted(package_order, key=package_order.get, reverse=False)
    for module_name in parameters['globals']['loadOrder']:
        name_split = module_name.split('.')
        try:
            parameters_module = __import__(module_name + '.Parameters', globals(), locals(), ['Parameters'])
            parameters[name_split[1]][name_split[2]] = parameters_module.parameters
            command_line = parameters_module.command_line_flags
            for key, value in command_line.iteritems():
                command_line_flags[name_split[1] + ':' + name_split[2] + ':' + key] = value

        except Exception as e:
            Utilities.logging.debug(e.__repr__())

    parameters['command_line_flags'] = Utilities.mergeDictionaries(command_line_flags, Parameters.command_line_flags)
    return parameters


def Initialise(remove_cache):
    """The main initialisation file of `rol`. Grabs information from all modules to assemble a `parameters` dictionary."""
    if remove_cache:
        Utilities.removeCache()
    parameters = prepareParameters()
    sys.path.append(parameters['globals']['plugins'] + '/../')
    parameters['developer']['progressStartTime'] = time.time()
    return parameters