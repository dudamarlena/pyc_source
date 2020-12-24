# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/dame/cli_methods.py
# Compiled at: 2020-05-04 14:59:45
# Size of source mod 2**32: 9792 bytes
import os, stat, uuid
from pathlib import Path
import click, texttable as tt
from modelcatalog import ApiException, SampleResource
from dame._utils import log
from dame.executor import prepare_execution, get_engine, DOCKER_ENGINE, SINGULARITY_ENGINE, get_singularity_cmd, run_singularity, run_docker, get_docker_cmd
from dame.local_file_manager import find_file_directory
from dame.utils import create_yaml_from_resource, obtain_id
from dame.utils import url_validation
SCRIPT_FILENAME = 'run'
data_set_property = [
 'id', 'label']
parameter_set_property = ['id', 'label', 'has_default_value']

def show_model_configuration_details(model_configuration):
    click.echo(click.style('Information about the model configuration', bold=True))
    if model_configuration:
        if hasattr(model_configuration, 'has_input'):
            click.echo(click.style('Inputs', bold=True))
            for _input in model_configuration.has_input:
                if hasattr(_input, 'has_fixed_resource') and hasattr(_input.has_fixed_resource[0], 'value'):
                    click.echo('- {}: {}'.format(_input.label[0], _input.has_fixed_resource[0].value[0]))
                else:
                    label = getattr(_input, 'label') if hasattr(_input, 'label') else getattr(_input, 'id')
                    click.echo('- {}: {}'.format(label[0], 'No information'))

    if model_configuration:
        if hasattr(model_configuration, 'has_parameter'):
            click.echo(click.style('Parameters', bold=True))
            for _parameter in model_configuration.has_parameter:
                short_value(_parameter, 'has_default_value')

    else:
        if hasattr(model_configuration, 'has_software_image'):
            try:
                click.echo(click.style('Docker Image', bold=True))
                image = getattr(model_configuration, 'has_software_image')[0].label[0]
                click.echo('- {}: {} - https://hub.docker.com/r/{} '.format('Name', image, image.split(':')[0]))
            except AttributeError as e:
                try:
                    raise AttributeError('No information available about the Docker Image.')
                finally:
                    e = None
                    del e

        else:
            raise AttributeError('No information available about the Docker Image.')
        if hasattr(model_configuration, 'has_component_location'):
            try:
                click.echo(click.style('Component Location', bold=True))
                image = getattr(model_configuration, 'has_component_location')[0]
                click.echo('- {}: {}'.format('Link', image))
            except AttributeError as e:
                try:
                    raise AttributeError('No information available about the executable component Location')
                finally:
                    e = None
                    del e

        else:
            raise AttributeError('No information available about the executable component Location')


def short_value(resource, prop):
    if hasattr(resource, prop):
        value = getattr(resource, prop)
        click.echo('- {}: {}'.format(getattr(resource, 'label')[0], value[0]))


def verify_input_parameters(model_configuration, interactive, data_dir):
    for _input in model_configuration.has_input:
        uri = None
        if not hasattr(_input, 'has_fixed_resource'):
            if interactive:
                if hasattr(_input, 'label') and hasattr(_input, 'has_format'):
                    click.secho(('To run this model configuration,a {} file (.{} file) is required.'.format(_input.label[0], _input.has_format[0])),
                      fg='yellow')
                else:
                    if hasattr(_input, 'label'):
                        click.secho(('To run this model configuration, a {} file is required.'.format(_input.label[0])), fg='yellow')
                    else:
                        click.secho(('To run this model configuration, a {} file is required.'.format(_input.id)),
                          fg='yellow')
                if data_dir:
                    if hasattr(_input, 'has_format'):
                        if click.confirm(('Do you want to search the file in the directory {}'.format(data_dir)),
                          default=True):
                            uri = find_file_directory(data_dir, _input.has_format[0])
                if uri is None:
                    uri = click.prompt('Please enter a url')
                    uri = uri.replace(' ', '')
                    while not url_validation(uri):
                        uri = click.prompt('Please enter a url')

                create_sample_resource(_input, uri)
        if not hasattr(_input, 'has_fixed_resource') or interactive:
            raise ValueError('Missing information')

    click.secho('The information needed to run the model is complete, and I can execute the model as follows:', fg='green')
    return model_configuration


def create_sample_resource(_input, uri):
    s = SampleResource(id=('https://w3id.org/okn/i/mint/'.format(str(uuid.uuid4()))), data_catalog_identifier='FFF-3s5c112e-c7ae-4cda-ba23-2e4f2286a18o',
      value=[
     uri])
    _input.has_fixed_resource = [s.to_dict()]


def print_data_property_table(resource, property_selected={}):
    resource_dict = resource.to_dict()
    tab = tt.Texttable(max_width=100)
    headings = ['Property', 'Value']
    tab.header(headings)
    for key, value in resource_dict.items():
        if not isinstance(value, dict):
            if key == 'type' or key == 'has_presentation':
                continue
            if property_selected:
                if key not in property_selected:
                    continue
            tab.add_row([key, value])

    print(tab.draw())


def run_method_setup(setup, interactive, data_dir):
    """
    Call download_setup(): Download the setup(s) as yaml file
    Call execute_setup(): Read the yaml file and execute
    """
    try:
        name = obtain_id(setup.id)
        file_path = create_yaml_from_resource(resource=setup, name=name, output=(Path('.')))
        component_src_dir, execution_dir, setup_cmd_line, setup_name, image = prepare_execution(file_path)
    except ApiException as e:
        try:
            click.secho(('Unable to download the setup {}'.format(e)), fg='red')
            exit(1)
        finally:
            e = None
            del e

    try:
        execute_setups(component_src_dir, execution_dir, setup_cmd_line, setup_name, image, interactive)
        click.secho(('[{}] The execution has been successful'.format(setup_name)), fg='green')
        click.secho(('[{}] Results available at: {} '.format(setup_name, component_src_dir)), fg='green')
    except Exception as e:
        try:
            log.error(e, exc_info=True)
            click.secho(('[{}] The execution has failed'.format(setup_name)), fg='red')
            exit(1)
        finally:
            e = None
            del e


def execute_setups(component_src_dir, execution_dir, setup_cmd_line, setup_name, image, interactive):
    """
    Find the setup files if the path is a directory and execute it
    """
    try:
        engine = get_engine()
    except FileNotFoundError:
        click.secho('Singularity is not installed', fg='red')
        exit(1)
    except Exception as e:
        try:
            click.secho(('Docker is not running or installed'.format(e)), fg='red')
            exit(1)
        finally:
            e = None
            del e

    os.chmod(component_src_dir / SCRIPT_FILENAME, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
    if engine == DOCKER_ENGINE:
        try:
            mint_volumes = {str(Path(component_src_dir).absolute()): {'bind':'/tmp/mint',  'mode':'rw'}}
            docker_cmd_pretty = get_docker_cmd(image, setup_cmd_line, mint_volumes)
            show_execution_info(component_src_dir, interactive, docker_cmd_pretty)
            run_docker(setup_cmd_line, execution_dir, component_src_dir, setup_name, image, mint_volumes)
        except Exception as e:
            try:
                raise e
            finally:
                e = None
                del e

    else:
        if engine == SINGULARITY_ENGINE:
            try:
                singularity_cmd = get_singularity_cmd(image, setup_cmd_line)
                singularity_cmd_pretty = ' '.join(singularity_cmd)
                show_execution_info(component_src_dir, interactive, singularity_cmd_pretty)
                run_singularity(singularity_cmd, execution_dir, component_src_dir, setup_name)
            except Exception as e:
                try:
                    raise e
                finally:
                    e = None
                    del e


def show_execution_info(component_src_dir, interactive, singularity_cmd_pretty):
    click.echo('Invocation command \ncd {}\n{}'.format(component_src_dir, singularity_cmd_pretty))
    if interactive:
        if not click.confirm('Do you want to proceed and submit it for execution?', default=True):
            exit(0)


def find_setup_files--- This code section failed: ---

 L. 201         0  BUILD_LIST_0          0 
                2  STORE_FAST               'setup_files'

 L. 202         4  LOAD_GLOBAL              os
                6  LOAD_ATTR                path
                8  LOAD_METHOD              isdir
               10  LOAD_FAST                'path'
               12  CALL_METHOD_1         1  '1 positional argument'
               14  POP_JUMP_IF_FALSE    80  'to 80'

 L. 203        16  LOAD_GLOBAL              Path
               18  LOAD_FAST                'path'
               20  CALL_FUNCTION_1       1  '1 positional argument'
               22  STORE_FAST               'path'

 L. 204        24  SETUP_LOOP          114  'to 114'
               26  LOAD_GLOBAL              os
               28  LOAD_METHOD              listdir
               30  LOAD_FAST                'path'
               32  CALL_METHOD_1         1  '1 positional argument'
               34  GET_ITER         
             36_0  COME_FROM            58  '58'
               36  FOR_ITER             76  'to 76'
               38  STORE_FAST               'file'

 L. 205        40  LOAD_FAST                'file'
               42  LOAD_METHOD              endswith
               44  LOAD_STR                 '.yaml'
               46  CALL_METHOD_1         1  '1 positional argument'
               48  POP_JUMP_IF_TRUE     60  'to 60'
               50  LOAD_FAST                'file'
               52  LOAD_METHOD              endswith
               54  LOAD_STR                 '.yml'
               56  CALL_METHOD_1         1  '1 positional argument'
               58  POP_JUMP_IF_FALSE    36  'to 36'
             60_0  COME_FROM            48  '48'

 L. 206        60  LOAD_FAST                'setup_files'
               62  LOAD_METHOD              append
               64  LOAD_FAST                'path'
               66  LOAD_FAST                'file'
               68  BINARY_TRUE_DIVIDE
               70  CALL_METHOD_1         1  '1 positional argument'
               72  POP_TOP          
               74  JUMP_BACK            36  'to 36'
               76  POP_BLOCK        
               78  JUMP_FORWARD        114  'to 114'
             80_0  COME_FROM            14  '14'

 L. 207        80  LOAD_GLOBAL              os
               82  LOAD_ATTR                path
               84  LOAD_METHOD              isfile
               86  LOAD_FAST                'path'
               88  CALL_METHOD_1         1  '1 positional argument'
               90  POP_JUMP_IF_FALSE   114  'to 114'

 L. 208        92  LOAD_GLOBAL              Path
               94  LOAD_STR                 '.'
               96  CALL_FUNCTION_1       1  '1 positional argument'
               98  STORE_FAST               'default_path'

 L. 209       100  LOAD_FAST                'setup_files'
              102  LOAD_METHOD              append
              104  LOAD_FAST                'default_path'
              106  LOAD_FAST                'path'
              108  BINARY_TRUE_DIVIDE
              110  CALL_METHOD_1         1  '1 positional argument'
              112  POP_TOP          
            114_0  COME_FROM            90  '90'
            114_1  COME_FROM            78  '78'
            114_2  COME_FROM_LOOP       24  '24'

 L. 210       114  LOAD_FAST                'setup_files'
              116  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM_LOOP' instruction at offset 114_2


def print_table_list(items):
    headings = [
     'Id', 'Description']
    tab = tt.Texttable()
    tab.header(headings)
    for item in items:
        _id = obtain_id(item.id)
        _description = ''.join(item.description) if hasattr(item, 'description') else 'No information'
        tab.add_row([_id, _description])

    print(tab.draw())