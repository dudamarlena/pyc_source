# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\Projects\Github\PKBReportBuilder\PKBReportBuilder\models\settings\config.py
# Compiled at: 2019-02-04 09:39:49
# Size of source mod 2**32: 4772 bytes
import os, sys, modules.logging.logging as logging_config, json, logging
root_dir = os.path.dirname(os.path.realpath(sys.argv[0]))
logs_dir_full_path = ''
logs_dir_name = 'logs'
configs_dir_full_path = ''
configs_dir_name = 'configs'
data_dir_full_path = ''
data_dir_name = 'data'
version_code = '0.4'
build_version_code = -1
engine_name = 'PKB Report Builder'
system_name = 'PKB Report Builder Engine'
show_system_info_on_start = False
logging_config_file_name = 'logging.yaml'
logging_config_file_full_path = ''
build_code_file_name = 'build_code.json'
build_code_file_full_path = ''
test_parse_file_name = '77873.xml'
test_parse_file_full_path = ''
exports_dir_full_path = ''
exports_dir_name = 'exports'
export_json_file_full_path = ''
export_json_file_name = 'data.json'
versions_container = [
 [
  '0.1', 'Leonardo'],
 [
  '0.2', 'Donatello'],
 [
  '0.3', 'Raphael'],
 [
  '0.4', 'Michelangelo'],
 [
  '0.5', 'Splinter']]

def load_build_version():
    global build_code_file_full_path
    global build_version_code
    try:
        with open(build_code_file_full_path) as (f):
            data = json.load(f)
            build_version_code = int(data['build_version_code'])
            build_version_code += 1
            data['build_version_code'] = build_version_code
        with open(build_code_file_full_path, 'w') as (jsonFile):
            json.dump(data, jsonFile)
    except Exception as e:
        logging.error('Error. ' + str(e))


def get_version_name():
    try:
        versions = versions_container
        current_version_code = version_code
        for version in versions:
            if version[0] == current_version_code:
                return version[1]

    except Exception as e:
        logging.error('Error. ' + str(e))
        return str(e)


def join_path(paths):
    try:
        path = (os.path.join)(*paths)
        path = os.path.normpath(path)
        return path
    except Exception as e:
        return str(e)


def show_system_info():
    try:
        print('Start init configuration')
        print('Root dir : ' + root_dir)
        print('System name : ' + system_name)
        print('Engine name : ' + engine_name)
        print('Engine version code: ' + version_code)
        print('Engine version name: ' + get_version_name())
        print('Build version code: ' + str(build_version_code))
    except Exception as e:
        pass


def config_paths():
    global build_code_file_full_path
    global configs_dir_full_path
    global data_dir_full_path
    global export_json_file_full_path
    global exports_dir_full_path
    global logging_config_file_full_path
    global logs_dir_full_path
    global test_parse_file_full_path
    try:
        configs_dir_full_path = join_path([root_dir, configs_dir_name])
        logging_config_file_full_path = join_path([configs_dir_full_path, logging_config_file_name])
        build_code_file_full_path = join_path([configs_dir_full_path, build_code_file_name])
        logs_dir_full_path = join_path([root_dir, logs_dir_name])
        data_dir_full_path = join_path([root_dir, data_dir_name])
        test_parse_file_full_path = join_path([data_dir_full_path, test_parse_file_name])
        exports_dir_full_path = join_path([root_dir, exports_dir_name])
        export_json_file_full_path = join_path([exports_dir_full_path, export_json_file_name])
        t = 0
    except Exception as e:
        pass


def init_config():
    try:
        config_paths()
        load_build_version()
        logging_config.setup_logging(default_path=logging_config_file_full_path)
        if show_system_info_on_start == True:
            show_system_info()
        logging.info('Config init successful')
    except Exception as e:
        logging.error(str(e))