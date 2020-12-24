# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/samcli/commands/_utils/template.py
# Compiled at: 2020-03-21 12:32:11
# Size of source mod 2**32: 8937 bytes
"""
Utilities to manipulate template
"""
import os, pathlib, jmespath, yaml
from botocore.utils import set_value_from_jmespath
from samcli.commands.exceptions import UserException
from samcli.yamlhelper import yaml_parse, yaml_dump
from samcli.commands._utils.resources import METADATA_WITH_LOCAL_PATHS, RESOURCES_WITH_LOCAL_PATHS

class TemplateNotFoundException(UserException):
    pass


class TemplateFailedParsingException(UserException):
    pass


def get_template_data(template_file):
    """
    Read the template file, parse it as JSON/YAML and return the template as a dictionary.

    Parameters
    ----------
    template_file : string
        Path to the template to read

    Returns
    -------
    Template data as a dictionary
    """
    if not pathlib.Path(template_file).exists():
        raise TemplateNotFoundException('Template file not found at {}'.format(template_file))
    with open(template_file, 'r') as (fp):
        try:
            return yaml_parse(fp.read())
        except (ValueError, yaml.YAMLError) as ex:
            try:
                raise TemplateFailedParsingException('Failed to parse template: {}'.format(str(ex)))
            finally:
                ex = None
                del ex


def move_template(src_template_path, dest_template_path, template_dict):
    """
    Move the SAM/CloudFormation template from ``src_template_path`` to ``dest_template_path``. For convenience, this
    method accepts a dictionary of template data ``template_dict`` that will be written to the destination instead of
    reading from the source file.

    SAM/CloudFormation template can contain certain properties whose value is a relative path to a local file/folder.
    This path is always relative to the template's location. Before writing the template to ``dest_template_path`,
    we will update these paths to be relative to the new location.

    This methods updates resource properties supported by ``aws cloudformation package`` command:
    https://docs.aws.amazon.com/cli/latest/reference/cloudformation/package.html

    You must use this method if you are reading a template from one location, modifying it, and writing it back to a
    different location.

    Parameters
    ----------
    src_template_path : str
        Path to the original location of the template

    dest_template_path : str
        Path to the destination location where updated template should be written to

    template_dict : dict
        Dictionary containing template contents. This dictionary will be updated & written to ``dest`` location.
    """
    original_root = os.path.dirname(src_template_path)
    new_root = os.path.dirname(dest_template_path)
    modified_template = _update_relative_paths(template_dict, original_root, new_root)
    with open(dest_template_path, 'w') as (fp):
        fp.write(yaml_dump(modified_template))


def _update_relative_paths(template_dict, original_root, new_root):
    """
    SAM/CloudFormation template can contain certain properties whose value is a relative path to a local file/folder.
    This path is usually relative to the template's location. If the template is being moved from original location
    ``original_root`` to new location ``new_root``, use this method to update these paths to be
    relative to ``new_root``.

    After this method is complete, it is safe to write the template to ``new_root`` without
    breaking any relative paths.

    This methods updates resource properties supported by ``aws cloudformation package`` command:
    https://docs.aws.amazon.com/cli/latest/reference/cloudformation/package.html

    If a property is either an absolute path or a S3 URI, this method will not update them.

    Parameters
    ----------
    template_dict : dict
        Dictionary containing template contents. This dictionary will be updated & written to ``dest`` location.

    original_root : str
        Path to the directory where all paths were originally set relative to. This is usually the directory
        containing the template originally

    new_root : str
        Path to the new directory that all paths set relative to after this method completes.

    Returns
    -------
    Updated dictionary

    """
    for resource_type, properties in template_dict.get('Metadata', {}).items():
        if resource_type not in METADATA_WITH_LOCAL_PATHS:
            continue
        for path_prop_name in METADATA_WITH_LOCAL_PATHS[resource_type]:
            path = properties.get(path_prop_name)
            updated_path = _resolve_relative_to(path, original_root, new_root)
            if not updated_path:
                continue
            properties[path_prop_name] = updated_path

    for _, resource in template_dict.get('Resources', {}).items():
        resource_type = resource.get('Type')
        if resource_type not in RESOURCES_WITH_LOCAL_PATHS:
            continue
        for path_prop_name in RESOURCES_WITH_LOCAL_PATHS[resource_type]:
            properties = resource.get('Properties', {})
            path = jmespath.search(path_prop_name, properties)
            updated_path = _resolve_relative_to(path, original_root, new_root)
            if not updated_path:
                continue
            set_value_from_jmespath(properties, path_prop_name, updated_path)

    template_dict = _update_aws_include_relative_path(template_dict, original_root, new_root)
    return template_dict


def _update_aws_include_relative_path(template_dict, original_root, new_root):
    """
    Update relative paths in "AWS::Include" directive. This directive can be present at any part of the template,
    and not just within resources.
    """
    for key, val in template_dict.items():
        if key == 'Fn::Transform':
            if isinstance(val, dict):
                if val.get('Name') == 'AWS::Include':
                    path = val.get('Parameters', {}).get('Location', {})
                    updated_path = _resolve_relative_to(path, original_root, new_root)
                    if not updated_path:
                        continue
                    val['Parameters']['Location'] = updated_path
                elif isinstance(val, dict):
                    _update_aws_include_relative_path(val, original_root, new_root)
                elif isinstance(val, list):
                    for item in val:
                        if isinstance(item, dict):
                            _update_aws_include_relative_path(item, original_root, new_root)

    return template_dict


def _resolve_relative_to--- This code section failed: ---

 L. 213         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'path'
                4  LOAD_GLOBAL              str
                6  CALL_FUNCTION_2       2  '2 positional arguments'
                8  POP_JUMP_IF_FALSE    52  'to 52'

 L. 214        10  LOAD_FAST                'path'
               12  LOAD_METHOD              startswith
               14  LOAD_STR                 's3://'
               16  CALL_METHOD_1         1  '1 positional argument'
               18  POP_JUMP_IF_TRUE     52  'to 52'

 L. 215        20  LOAD_FAST                'path'
               22  LOAD_METHOD              startswith
               24  LOAD_STR                 'http://'
               26  CALL_METHOD_1         1  '1 positional argument'
               28  POP_JUMP_IF_TRUE     52  'to 52'

 L. 216        30  LOAD_FAST                'path'
               32  LOAD_METHOD              startswith
               34  LOAD_STR                 'https://'
               36  CALL_METHOD_1         1  '1 positional argument'
               38  POP_JUMP_IF_TRUE     52  'to 52'

 L. 217        40  LOAD_GLOBAL              os
               42  LOAD_ATTR                path
               44  LOAD_METHOD              isabs
               46  LOAD_FAST                'path'
               48  CALL_METHOD_1         1  '1 positional argument'
               50  POP_JUMP_IF_FALSE    56  'to 56'
             52_0  COME_FROM            38  '38'
             52_1  COME_FROM            28  '28'
             52_2  COME_FROM            18  '18'
             52_3  COME_FROM             8  '8'

 L. 220        52  LOAD_CONST               None
               54  RETURN_VALUE     
             56_0  COME_FROM            50  '50'

 L. 223        56  LOAD_GLOBAL              os
               58  LOAD_ATTR                path
               60  LOAD_METHOD              relpath

 L. 224        62  LOAD_GLOBAL              os
               64  LOAD_ATTR                path
               66  LOAD_METHOD              normpath
               68  LOAD_GLOBAL              os
               70  LOAD_ATTR                path
               72  LOAD_METHOD              join
               74  LOAD_FAST                'original_root'
               76  LOAD_FAST                'path'
               78  CALL_METHOD_2         2  '2 positional arguments'
               80  CALL_METHOD_1         1  '1 positional argument'
               82  LOAD_FAST                'new_root'
               84  CALL_METHOD_2         2  '2 positional arguments'
               86  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 86


def get_template_parameters(template_file):
    """
    Get Parameters from a template file.

    Parameters
    ----------
    template_file : string
        Path to the template to read

    Returns
    -------
    Template Parameters as a dictionary
    """
    template_dict = get_template_data(template_file=template_file)
    return template_dict.get('Parameters', dict())