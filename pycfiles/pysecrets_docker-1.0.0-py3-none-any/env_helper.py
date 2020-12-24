# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/sanhehu/Documents/GitHub/pysecret-project/pysecret/env_helper.py
# Compiled at: 2019-04-10 23:00:06
import os, re
export_pattern = re.compile('export [a-zA-Z0-9_]{1,128}="[a-zA-Z0-9_]{1,128}"')

def append_line_if_not_exists(path, line):
    """
    Append a line to a text file at `path` if the line not exists in its content.

    :type path: str
    :param path: text file absolute path

    :type path: str
    :param line: text string.

    :return: None
    """
    if not os.path.exists(path):
        with open(path, 'wb') as (f):
            f.write(('').encode('utf-8'))
    if '\n' in line:
        raise ValueError("'\\n' should not be in the line")
    striped_line = line.strip()
    with open(path, 'rb') as (f):
        content = f.read().decode('utf-8')
        flag_endswith_new_line = content.endswith('\n') or content.endswith('\n\r')
        for line_ in content.split('\n'):
            if striped_line in line_:
                return

    with open(path, 'ab') as (f):
        if flag_endswith_new_line:
            f.write((line + '\n').encode('utf-8'))
        else:
            f.write(('\n' + line + '\n').encode('utf-8'))


def load_var_value_from_shell_script_content(content):
    """
    Extract variable definition such as ``export var="value"`` from shell script
    content text.

    :type content: str
    :param content: text content of a shell script

    :rtype: dict
    :return:
    """
    candidate_line_list = list()
    for line in content.split('\n'):
        line_striped = line.strip()
        for item in re.findall(export_pattern, line_striped):
            if item == line:
                candidate_line_list.append(item)

    results = dict()
    for item in candidate_line_list:
        if item.startswith('export ') and '="' in item and item.endswith('"'):
            item = item[7:]
            key, value = item.split('=', 1)
            value = value[1:-1]
            results[key] = value

    return results


def load_var_value_from_shell_script(shell_scripts):
    if not os.path.exists(shell_scripts):
        return {}
    with open(shell_scripts, 'rb') as (f):
        content = f.read().decode('utf-8')
        return load_var_value_from_shell_script_content(content)