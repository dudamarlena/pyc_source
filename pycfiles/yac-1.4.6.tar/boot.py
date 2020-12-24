# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/x0ox/Dropbox/ActiveDev/yac/yac/lib/boot.py
# Compiled at: 2017-11-16 20:28:41
import json
from yac.lib.file import get_file_contents
from yac.lib.template import apply_stemplate
from yac.lib.variables import get_variable

def get_value(params):
    boot_script_list = []
    services_consumed = get_variable(params, 'services-consumed', [])
    servicefile_path = get_variable(params, 'servicefile-path')
    boot_file = get_variable(params, 'boot-file', '')
    if boot_file:
        boot_script_contents = get_file_contents(boot_file, servicefile_path)
        if boot_script_contents:
            boot_script_contents = apply_stemplate(boot_script_contents, params)
            boot_script_lines_list = boot_script_contents.split('\n')
            for i, line in enumerate(boot_script_lines_list):
                if '{' in line and '}' in line and 'Ref' in line:
                    prefix = line[:line.index('{')]
                    reference = line[line.index('{'):line.index('}') + 1]
                    reference_dict = json.loads(reference)
                    boot_script_list = boot_script_list + [prefix, {'Ref': reference_dict['Ref']}] + ['\n']
                else:
                    boot_script_list = boot_script_list + [line] + ['\n']

    else:
        boot_script_list = boot_script_list + ['# No boot script provided. See yac docs for more info.\n']
    return boot_script_list


def pp_script(boot_script_list):
    for line in boot_script_list:
        print str(line)