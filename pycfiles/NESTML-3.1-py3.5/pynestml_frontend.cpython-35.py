# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pynestml/frontend/pynestml_frontend.py
# Compiled at: 2020-03-05 05:49:41
# Size of source mod 2**32: 8006 bytes
import os, sys
from pynestml.cocos.co_cos_manager import CoCosManager
from pynestml.codegeneration.codegenerator import CodeGenerator
from pynestml.frontend.frontend_configuration import FrontendConfiguration, InvalidPathException, qualifier_store_log_arg, qualifier_module_name_arg, qualifier_logging_level_arg, qualifier_target_arg, qualifier_target_path_arg, qualifier_input_path_arg, qualifier_suffix_arg, qualifier_dev_arg
from pynestml.symbols.predefined_functions import PredefinedFunctions
from pynestml.symbols.predefined_types import PredefinedTypes
from pynestml.symbols.predefined_units import PredefinedUnits
from pynestml.symbols.predefined_variables import PredefinedVariables
from pynestml.utils.logger import Logger, LoggingLevel
from pynestml.utils.messages import Messages
from pynestml.utils.model_parser import ModelParser
from pynestml.utils.model_installer import install_nest as nest_installer

def to_nest(input_path, target_path=None, logging_level='ERROR', module_name=None, store_log=False, suffix='', dev=False):
    """Translate NESTML files into their equivalent C++ code for the NEST simulator.

    Parameters
    ----------
    input_path : str
        Path to the NESTML file or to a folder containing NESTML files to convert to NEST code.
    target_path : str, optional (default: append "target" to `input_path`)
        Path to the generated C++ code and install files.
    logging_level : str, optional (default: 'ERROR')
        Sets which level of information should be displayed duing code generation (among 'ERROR', 'WARNING', 'INFO', or 'NO').
    module_name : str, optional (default: "nestmlmodule")
        Name of the module, which will be used to import the model in NEST via `nest.Install(module_name)`.
    store_log : bool, optional (default: False)
        Whether the log should be saved to file.
    suffix : str, optional (default: "")
        Suffix which will be appended to the model's name (internal use to avoid naming conflicts with existing NEST models).
    dev : bool, optional (default: False)
        Enable development mode: code generation is attempted even for models that contain errors, and extra information is rendered in the generated code.
    """
    args = list()
    args.append(qualifier_input_path_arg)
    args.append(str(input_path))
    if target_path is not None:
        args.append(qualifier_target_path_arg)
        args.append(str(target_path))
    args.append(qualifier_target_arg)
    args.append(str('NEST'))
    args.append(qualifier_logging_level_arg)
    args.append(str(logging_level))
    if module_name is not None:
        args.append(qualifier_module_name_arg)
        args.append(str(module_name))
    if store_log:
        args.append(qualifier_store_log_arg)
    if suffix:
        args.append(qualifier_suffix_arg)
        args.append(suffix)
    if dev:
        args.append(qualifier_dev_arg)
    FrontendConfiguration.parse_config(args)
    if not process() == 0:
        raise Exception('Error(s) occurred while processing the model')


def install_nest(models_path, nest_path):
    """
    This procedure can be used to install generated models into the NEST
    simulator.

    Parameters
    ----------
    models_path : str
        Path to the generated models, which should contain the
        (automatically generated) CMake file.
    nest_path : str
        Path to the NEST installation, which should point to the main directory
        where NEST is installed. This folder contains the bin/, lib(64)/,
        include/, and share/ folders of the NEST install. Most importantly, the
        bin/ folder should contain the "nest-config" script. This path is
        passed through the -Dwith-nest argument of the CMake command during the
        installation of the generated NEST module. The suffix /bin/nest-config
        will be automatically attached to `nest_path`.
    """
    nest_installer(models_path, nest_path)


def main():
    """Returns the process exit code: 0 for success, > 0 for failure"""
    try:
        FrontendConfiguration.parse_config(sys.argv[1:])
    except InvalidPathException:
        print('Not a valid path to model or directory: "%s"!' % FrontendConfiguration.get_path())
        return 1

    return int(process())


def process():
    """
    Returns
    -------
    errors_occurred : bool
        Flag indicating whether errors occurred during processing
    """
    errors_occurred = False
    create_report_dir()
    init_predefined()
    compilation_units = list()
    nestml_files = FrontendConfiguration.get_files()
    if type(nestml_files) is not list:
        nestml_files = [
         nestml_files]
    for nestml_file in nestml_files:
        parsed_unit = ModelParser.parse_model(nestml_file)
        if parsed_unit is not None:
            compilation_units.append(parsed_unit)

    if len(compilation_units) > 0:
        neurons = list()
        for compilationUnit in compilation_units:
            neurons.extend(compilationUnit.get_neuron_list())

        CoCosManager.check_not_two_neurons_across_units(compilation_units)
        if not FrontendConfiguration.is_dev:
            for neuron in neurons:
                if Logger.has_errors(neuron):
                    code, message = Messages.get_neuron_contains_errors(neuron.get_name())
                    Logger.log_message(neuron=neuron, code=code, message=message, error_position=neuron.get_source_position(), log_level=LoggingLevel.INFO)
                    neurons.remove(neuron)
                    errors_occurred = True

        _codeGenerator = CodeGenerator(target=FrontendConfiguration.get_target())
        _codeGenerator.generate_code(neurons)
        for neuron in neurons:
            if Logger.has_errors(neuron):
                errors_occurred = True
                break

    if FrontendConfiguration.store_log:
        store_log_to_file()
    return errors_occurred


def init_predefined():
    PredefinedUnits.register_units()
    PredefinedTypes.register_types()
    PredefinedFunctions.register_functions()
    PredefinedVariables.register_variables()


def create_report_dir():
    if not os.path.isdir(os.path.join(FrontendConfiguration.get_target_path(), '..', 'report')):
        os.makedirs(os.path.join(FrontendConfiguration.get_target_path(), '..', 'report'))


def store_log_to_file():
    with open(str(os.path.join(FrontendConfiguration.get_target_path(), '..', 'report', 'log')) + '.txt', 'w+') as (f):
        f.write(str(Logger.get_json_format()))