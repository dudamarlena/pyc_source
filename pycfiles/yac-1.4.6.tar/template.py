# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: yac/lib/template.py
# Compiled at: 2017-11-16 20:28:41
import os, shutil, re, subprocess
from yac.lib.file import get_file_contents
from yac.lib.variables import get_variable, get_map_variable

def get_file_type(file_str):
    """ return a filetype given a file """
    process_list = [
     'file', '--mime-type', file_str]
    p = subprocess.Popen(process_list, stdout=subprocess.PIPE)
    file_type, err = p.communicate()
    return file_type


def apply_stemplate(string_w_variables, template_variables):
    for key in template_variables:
        lookup_param_spec = get_variable(template_variables, key, '', 'lookup')
        variable_value = get_variable(template_variables, key)
        if lookup_param_spec:
            if contains_map_mustache(key, string_w_variables):
                lookup_param_ref = get_map_key(key, string_w_variables)
                if lookup_param_spec == lookup_param_ref:
                    to_replace = '{{%s:%s}}' % (key, lookup_param_spec)
                    replace_with = get_map_variable(template_variables, key, lookup_param_spec)
                    if replace_with:
                        string_w_variables = string_w_variables.replace(to_replace, replace_with)
        elif isinstance(variable_value, str) or isinstance(variable_value, unicode):
            if contains_ref_mustache(key, string_w_variables):
                to_replace = '{{%s}}' % key
                replace_with = str(variable_value)
                string_w_variables = string_w_variables.replace(to_replace, replace_with)

    return string_w_variables


def contains_ref_mustache(param_key, string_w_variables):
    search_str = '{{%s}}' % param_key
    return re.search(search_str, string_w_variables)


def contains_map_mustache(param_key, string_w_variables):
    search_str = '{{(%s:)([a-zA-Z-_.]+)}}' % param_key
    return re.search(search_str, string_w_variables)


def get_map_key(param_key, string_w_variables):
    lookup_param = ''
    regex_result = contains_map_mustache(param_key, string_w_variables)
    if regex_result and regex_result.group(2):
        lookup_param = regex_result.group(2)
    return lookup_param


def apply_ftemplate(file_w_variables, template_variables):
    string_w_variables = get_file_contents(file_w_variables)
    return apply_stemplate(string_w_variables, template_variables)


def apply_templates_in_file(file_w_variables, template_variables, rendered_file_dest='tmp'):
    file_type = get_file_type(file_w_variables)
    if file_type and len(file_type) >= 1 and ('text' in file_type or 'json' in file_type or 'xml' in file_type or 'html' in file_type):
        file_contents = get_file_contents(file_w_variables)
        rendered_file_contents = apply_stemplate(file_contents, template_variables)
        if not os.path.exists(rendered_file_dest):
            os.makedirs(rendered_file_dest)
        file_name = os.path.basename(file_w_variables)
        rendered_file = os.path.join(rendered_file_dest, file_name)
        with open(rendered_file, 'w') as (outfile):
            outfile.write(rendered_file_contents)
    else:
        if not os.path.exists(rendered_file_dest):
            os.makedirs(rendered_file_dest)
        file_name = os.path.basename(file_w_variables)
        rendered_file = os.path.join(rendered_file_dest, file_name)
        shutil.copy(file_w_variables, rendered_file)
    return rendered_file


def apply_templates_in_dir(source_dir, template_variables, dest_dir='tmp'):
    dir_children = os.listdir(source_dir)
    for this_child in dir_children:
        if os.path.isfile(os.path.join(source_dir, this_child)):
            this_file = os.path.join(source_dir, this_child)
            apply_templates_in_file(this_file, template_variables, dest_dir)
        else:
            new_dest_dir = os.path.join(dest_dir, this_child)
            new_source_dir = os.path.join(source_dir, this_child)
            apply_templates_in_dir(new_source_dir, template_variables, new_dest_dir)