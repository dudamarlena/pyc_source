# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/MyKings/Documents/github/clocwalk/clocwalk/libs/analyzer/ruby.py
# Compiled at: 2020-02-03 01:02:02
# Size of source mod 2**32: 3743 bytes
import glob, os
__product__ = 'Ruby'
__version__ = '0.3'
from clocwalk.libs.core.common import recursive_search_files

def _get_version(version_str):
    """
    get version
    :param version_str:
    :return:
    """
    name = ''
    version = ''
    if version_str.startswith('gem'):
        version_str = version_str.replace('gem', '').strip()
        if version_str:
            str_list = version_str.split(',')
            for i in range(0, len(str_list)):
                if i == 0:
                    name = str_list[i].strip().replace("'", '')
                else:
                    version += '{0},'.format(str_list[i].strip().replace("'", ''))

            if version.endswith(','):
                version = version[:-1]
    return (
     name, version)


def _get_gemspec(code_dir, file_ext='gemspec'):
    """

    :param code_dir:
    :param file_ext:
    :return:
    """
    result = []
    if not code_dir.endswith('/'):
        code_dir = '{0}/'.format(code_dir)
    conf_list = glob.glob('{0}*.{1}'.format(code_dir, file_ext))
    if conf_list:
        with open(conf_list[0], 'r') as (fp):
            for line in fp:
                name = ''
                version = ''
                if not 'add_development_dependency' in line.strip():
                    if 'add_runtime_dependency' in line.strip():
                        current_conf = line.strip().split('_dependency')[1]
                        str_list = current_conf.split(',')
                        for i in range(0, len(str_list)):
                            if i == 0:
                                name = str_list[i].strip().replace("'", '')
                            else:
                                version += '{0},'.format(str_list[i].strip().replace("'", ''))

                        if version.endswith(','):
                            version = version[:-1]
                    result.append({'vendor':'', 
                     'product':name, 
                     'version':version, 
                     'new_version':'', 
                     'parent_file':'', 
                     'cve':{},  'origin_file':conf_list[0]})

    return result


def _get_dependencies(code_dir, file_name, origin=None):
    """
    get dependencies
    :param code_dir:
    :param file_name:
    :param origin:
    :return:
    """
    result = []
    with open(file_name, 'r') as (fp):
        for line in fp:
            if not line.strip().startswith('#'):
                if not (line.strip().startswith('source') or line.strip().startswith('group') or line.strip().startswith('end') or line.strip()):
                    continue
                if line.startswith('gemspec'):
                    return _get_gemspec(code_dir)
                name, ver = _get_version(line.strip())
                result.append({'vendor':'', 
                 'product':name, 
                 'version':ver, 
                 'parent_file':'', 
                 'cve':{},  'origin_file':origin})

    return result


def start(**kwargs):
    """
    :param kwargs:
    :return:
    """
    code_dir = kwargs.get('code_dir', '')
    file_name = kwargs.get('file_name', 'Gemfile')
    skipNewVerCheck = kwargs.get('skipNewVerCheck', False)
    result_file_list = recursive_search_files(code_dir, '*/Gemfile')
    result = []
    for item in result_file_list:
        relative_path = item.replace('{0}/'.format(code_dir), '')
        relative_path = relative_path[1:] if relative_path.startswith('/') else relative_path
        c_dir, _ = os.path.split(item)
        result.extend(_get_dependencies(code_dir=c_dir, file_name=item, origin=relative_path))

    return result