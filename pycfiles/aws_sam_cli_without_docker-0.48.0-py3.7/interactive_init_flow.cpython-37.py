# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/samcli/commands/init/interactive_init_flow.py
# Compiled at: 2020-03-21 12:32:11
# Size of source mod 2**32: 6692 bytes
"""
Isolates interactive init prompt flow. Expected to call generator logic at end of flow.
"""
import tempfile, logging, click
from botocore.exceptions import ClientError, WaiterError
from samcli.commands.init.interactive_event_bridge_flow import get_schema_template_details, get_schemas_api_caller, get_schemas_template_parameter
from samcli.commands.exceptions import SchemasApiException
from samcli.lib.schemas.schemas_code_manager import do_download_source_code_binding, do_extract_and_merge_schemas_code
from samcli.local.common.runtime_template import INIT_RUNTIMES, RUNTIME_TO_DEPENDENCY_MANAGERS
from samcli.commands.init.init_generator import do_generate
from samcli.commands.init.init_templates import InitTemplates
from samcli.lib.utils.osutils import remove
LOG = logging.getLogger(__name__)

def do_interactive(location, runtime, dependency_manager, output_dir, name, app_template, no_input):
    if app_template:
        location_opt_choice = '1'
    else:
        click.echo('Which template source would you like to use?')
        click.echo('\t1 - AWS Quick Start Templates\n\t2 - Custom Template Location')
        location_opt_choice = click.prompt('Choice', type=(click.Choice(['1', '2'])), show_choices=False)
    if location_opt_choice == '2':
        _generate_from_location(location, runtime, dependency_manager, output_dir, name, app_template, no_input)
    else:
        _generate_from_app_template(location, runtime, dependency_manager, output_dir, name, app_template)


def _generate_from_location(location, runtime, dependency_manager, output_dir, name, app_template, no_input):
    location = click.prompt('\nTemplate location (git, mercurial, http(s), zip, path)', type=str)
    summary_msg = '\n-----------------------\nGenerating application:\n-----------------------\nLocation: {location}\nOutput Directory: {output_dir}\n    '.format(location=location,
      output_dir=output_dir)
    click.echo(summary_msg)
    do_generate(location, runtime, dependency_manager, output_dir, name, no_input, None)


def _generate_from_app_template(location, runtime, dependency_manager, output_dir, name, app_template):
    extra_context = None
    runtime = _get_runtime(runtime)
    dependency_manager = _get_dependency_manager(dependency_manager, runtime)
    if not name:
        name = click.prompt('\nProject name', type=str, default='sam-app')
    else:
        templates = InitTemplates()
        if app_template is not None:
            location = templates.location_from_app_template(runtime, dependency_manager, app_template)
            extra_context = {'project_name':name,  'runtime':runtime}
        else:
            location, app_template = templates.prompt_for_location(runtime, dependency_manager)
        extra_context = {'project_name':name, 
         'runtime':runtime}
    is_dynamic_schemas_template = templates.is_dynamic_schemas_template(app_template, runtime, dependency_manager)
    if is_dynamic_schemas_template:
        schemas_api_caller = get_schemas_api_caller()
        schema_template_details = _get_schema_template_details(schemas_api_caller)
        schemas_template_parameter = get_schemas_template_parameter(schema_template_details)
        extra_context = {**schemas_template_parameter, **extra_context}
    no_input = True
    summary_msg = '\n-----------------------\nGenerating application:\n-----------------------\nName: {name}\nRuntime: {runtime}\nDependency Manager: {dependency_manager}\nApplication Template: {app_template}\nOutput Directory: {output_dir}\n\nNext steps can be found in the README file at {output_dir}/{name}/README.md\n    '.format(name=name,
      runtime=runtime,
      dependency_manager=dependency_manager,
      app_template=app_template,
      output_dir=output_dir)
    click.echo(summary_msg)
    do_generate(location, runtime, dependency_manager, output_dir, name, no_input, extra_context)
    if is_dynamic_schemas_template:
        _package_schemas_code(runtime, schemas_api_caller, schema_template_details, output_dir, name, location)


def _get_runtime(runtime):
    if not runtime:
        choices = list(map(str, range(1, len(INIT_RUNTIMES) + 1)))
        choice_num = 1
        click.echo('\nWhich runtime would you like to use?')
        for r in INIT_RUNTIMES:
            msg = '\t' + str(choice_num) + ' - ' + r
            click.echo(msg)
            choice_num = choice_num + 1

        choice = click.prompt('Runtime', type=(click.Choice(choices)), show_choices=False)
        runtime = INIT_RUNTIMES[(int(choice) - 1)]
    return runtime


def _get_dependency_manager(dependency_manager, runtime):
    if not dependency_manager:
        valid_dep_managers = RUNTIME_TO_DEPENDENCY_MANAGERS.get(runtime)
        if valid_dep_managers is None:
            dependency_manager = None
        else:
            if len(valid_dep_managers) == 1:
                dependency_manager = valid_dep_managers[0]
            else:
                choices = list(map(str, range(1, len(valid_dep_managers) + 1)))
                choice_num = 1
                click.echo('\nWhich dependency manager would you like to use?')
                for dm in valid_dep_managers:
                    msg = '\t' + str(choice_num) + ' - ' + dm
                    click.echo(msg)
                    choice_num = choice_num + 1

                choice = click.prompt('Dependency manager', type=(click.Choice(choices)), show_choices=False)
                dependency_manager = valid_dep_managers[(int(choice) - 1)]
    return dependency_manager


def _get_schema_template_details(schemas_api_caller):
    try:
        return get_schema_template_details(schemas_api_caller)
    except ClientError as e:
        try:
            raise SchemasApiException('Exception occurs while getting Schemas template parameter. %s' % e.response['Error']['Message'])
        finally:
            e = None
            del e


def _package_schemas_code(runtime, schemas_api_caller, schema_template_details, output_dir, name, location):
    try:
        try:
            click.echo('Trying to get package schema code')
            download_location = tempfile.NamedTemporaryFile(delete=False)
            do_download_source_code_binding(runtime, schema_template_details, schemas_api_caller, download_location)
            do_extract_and_merge_schemas_code(download_location, output_dir, name, location)
            download_location.close()
        except (ClientError, WaiterError) as e:
            try:
                raise SchemasApiException('Exception occurs while packaging Schemas code. %s' % e.response['Error']['Message'])
            finally:
                e = None
                del e

    finally:
        remove(download_location.name)