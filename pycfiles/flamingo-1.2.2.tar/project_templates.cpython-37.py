# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/fsc/work/devel/flamingo/flamingo/core/project_templates.py
# Compiled at: 2020-04-28 06:33:53
# Size of source mod 2**32: 2138 bytes
from configparser import ConfigParser, NoSectionError
import os
from flamingo.core.utils.configparser import parse_config_string
from flamingo.core.packaging import find_project_template_dirs

def get_project_template_config(path):
    config = ConfigParser()
    config_path = os.path.join(path, 'project_template.config')
    config.read_file(open(config_path, 'r'))
    try:
        data = {option:config.get('config', option) for option in config.options('config')}
    except NoSectionError:
        data = {}

    if 'variables' in data:
        data['variables'] = parse_config_string(data['variables'])
    else:
        data['variables'] = {}
    if 'description' not in data:
        data['description'] = ''
    return (config_path, data)


def list_project_templates(package=''):
    templates = []
    for template_package, template_dir in find_project_template_dirs():
        if package:
            if package != template_package:
                continue
        for entry in os.listdir(template_dir):
            template_path = os.path.join(template_dir, entry)
            if os.path.exists(os.path.join(template_path, 'project_template.config')):
                templates.append((template_package, template_path))

    return templates


def get_template_path(template_name):
    template_paths = []
    package = ''
    if '.' in template_name:
        package, template_name = template_name.split('.', 1)
    for template_package, template_dir in find_project_template_dirs():
        if package:
            if package != template_package:
                continue
        template_path = os.path.join(template_dir, template_name)
        if not os.path.exists(os.path.join(template_path, 'project_template.config')):
            continue
        template_paths.append((template_package, template_path))

    if len(template_paths) < 1:
        raise ValueError('no such template')
    if len(template_paths) > 1:
        raise ValueError('ambiguous template name')
    return (template_paths[0][0], template_paths[0][1])