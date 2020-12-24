# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/samcli/lib/schemas/schemas_code_manager.py
# Compiled at: 2020-03-21 12:32:11
# Size of source mod 2**32: 3169 bytes
""" Isolates code download and merge logic for dynamic Schemas template """
import os, json, click
from botocore.exceptions import ClientError
from samcli.local.lambdafn.zip import unzip
from samcli.local.common.runtime_template import SAM_RUNTIME_TO_SCHEMAS_CODE_LANG_MAPPING

def do_download_source_code_binding(runtime, schema_template_details, schemas_api_caller, download_location):
    """
    Downloads source code binding for given registry and schema version,
    generating the code bindings if they haven't been generated first
    :param runtime: Lambda runtime
    :param schema_template_details: e.g: registry_name, schema_name, schema_version
    :param schemas_api_caller:
    :param download_dir:
    :return: directory location where code is downloaded
    """
    registry_name = schema_template_details['registry_name']
    schema_name = schema_template_details['schema_full_name']
    schema_version = schema_template_details['schema_version']
    schemas_runtime = SAM_RUNTIME_TO_SCHEMAS_CODE_LANG_MAPPING.get(runtime)
    try:
        click.echo('Event code binding Registry: %s and Schema: %s' % (registry_name, schema_name))
        click.echo('Generating code bindings...')
        return schemas_api_caller.download_source_code_binding(schemas_runtime, registry_name, schema_name, schema_version, download_location)
    except ClientError as e:
        try:
            if e.response['Error']['Code'] == 'NotFoundException':
                schemas_api_caller.put_code_binding(schemas_runtime, registry_name, schema_name, schema_version)
                schemas_api_caller.poll_for_code_binding_status(schemas_runtime, registry_name, schema_name, schema_version)
                return schemas_api_caller.download_source_code_binding(schemas_runtime, registry_name, schema_name, schema_version, download_location)
            raise e
        finally:
            e = None
            del e


def do_extract_and_merge_schemas_code(download_location, output_dir, project_name, template_location):
    """
    Unzips schemas generated code and merge it with cookiecutter genertaed source.
    :param download_location:
    :param output_dir:
    :param project_name:
    :param template_location:
    :return:
    """
    click.echo('Merging code bindings...')
    cookiecutter_json_path = os.path.join(template_location, 'cookiecutter.json')
    with open(cookiecutter_json_path, 'r') as (cookiecutter_json):
        cookiecutter_json_data = cookiecutter_json.read()
        cookiecutter_json = json.loads(cookiecutter_json_data)
        function_name = cookiecutter_json['function_name']
        copy_location = os.path.join(output_dir, project_name, function_name)
        unzip(download_location, copy_location)