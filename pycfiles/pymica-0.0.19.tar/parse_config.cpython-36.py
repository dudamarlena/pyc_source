# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pymic/util/parse_config.py
# Compiled at: 2019-12-07 03:31:59
# Size of source mod 2**32: 2877 bytes
from __future__ import absolute_import, print_function
import configparser

def is_int(val_str):
    start_digit = 0
    if val_str[0] == '-':
        start_digit = 1
    flag = True
    for i in range(start_digit, len(val_str)):
        if str(val_str[i]) < '0' or str(val_str[i]) > '9':
            flag = False
            break

    return flag


def is_float(val_str):
    flag = False
    if '.' in val_str:
        if len(val_str.split('.')) == 2:
            if './' not in val_str:
                if is_int(val_str.split('.')[0]):
                    if is_int(val_str.split('.')[1]):
                        flag = True
                flag = False
    elif 'e' in val_str:
        if val_str[0] != 'e':
            if len(val_str.split('e')) == 2:
                if is_int(val_str.split('e')[0]):
                    if is_int(val_str.split('e')[1]):
                        flag = True
                flag = False
    else:
        flag = False
    return flag


def is_bool(var_str):
    if var_str.lower() == 'true' or var_str.lower() == 'false':
        return True
    else:
        return False


def parse_bool(var_str):
    if var_str.lower() == 'true':
        return True
    else:
        return False


def is_list(val_str):
    if val_str[0] == '[':
        if val_str[(-1)] == ']':
            return True
    return False


def parse_list(val_str):
    sub_str = val_str[1:-1]
    splits = sub_str.split(',')
    output = []
    for item in splits:
        item = item.strip()
        if is_int(item):
            output.append(int(item))
        elif is_float(item):
            output.append(float(item))
        else:
            if is_bool(item):
                output.append(parse_bool(item))
            else:
                if item.lower() == 'none':
                    output.append(None)
                else:
                    output.append(item)

    return output


def parse_value_from_string(val_str):
    if is_int(val_str):
        val = int(val_str)
    else:
        if is_float(val_str):
            val = float(val_str)
        else:
            if is_list(val_str):
                val = parse_list(val_str)
            else:
                if is_bool(val_str):
                    val = parse_bool(val_str)
                else:
                    if val_str.lower() == 'none':
                        val = None
                    else:
                        val = val_str
    return val


def parse_config(filename):
    config = configparser.ConfigParser()
    config.read(filename)
    output = {}
    for section in config.sections():
        output[section] = {}
        for key in config[section]:
            val_str = str(config[section][key])
            if len(val_str) > 0:
                val = parse_value_from_string(val_str)
                output[section][key] = val
            else:
                val = None
            print(section, key, val_str, val)

    return output


if __name__ == '__main__':
    print(is_int('555'))
    print(is_float('555.10'))
    a = '[1 ,2 ,3 ]'
    print(a)
    print(parse_list(a))