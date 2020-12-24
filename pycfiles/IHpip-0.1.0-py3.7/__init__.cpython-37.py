# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\IHpip\__init__.py
# Compiled at: 2019-03-29 23:31:44
# Size of source mod 2**32: 461 bytes
import yaml, sys
import pip._internal as pip

def run():
    try:
        requirements_name = sys.argv[1]
        install_list = sys.argv[2]
    except:
        print('invalid amount of arguments')
    else:
        for requirement in parse_file(requirements_name)[install_list]:
            pip(['install', requirement])


def parse_file(file_name):
    with open(file_name, 'r') as (stream):
        try:
            return yaml.load(stream)
        except yaml.YAMLError as e:
            try:
                print(e)
            finally:
                e = None
                del e