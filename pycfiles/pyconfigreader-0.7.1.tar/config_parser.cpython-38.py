# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/config_parser/config_parser.py
# Compiled at: 2019-11-26 10:07:40
# Size of source mod 2**32: 6050 bytes
from collections import namedtuple
from typing import Dict, List, Type, Tuple, Optional
import argparse, yaml

def parse_from_file--- This code section failed: ---

 L.  13         0  LOAD_GLOBAL              open
                2  LOAD_FAST                'file_location'
                4  CALL_FUNCTION_1       1  ''
                6  SETUP_WITH           32  'to 32'
                8  STORE_FAST               'yaml_file'

 L.  14        10  LOAD_GLOBAL              yaml
               12  LOAD_METHOD              safe_load
               14  LOAD_FAST                'yaml_file'
               16  CALL_METHOD_1         1  ''
               18  POP_BLOCK        
               20  ROT_TWO          
               22  BEGIN_FINALLY    
               24  WITH_CLEANUP_START
               26  WITH_CLEANUP_FINISH
               28  POP_FINALLY           0  ''
               30  RETURN_VALUE     
             32_0  COME_FROM_WITH        6  '6'
               32  WITH_CLEANUP_START
               34  WITH_CLEANUP_FINISH
               36  END_FINALLY      

Parse error at or near `ROT_TWO' instruction at offset 20


def write_to_file--- This code section failed: ---

 L.  23         0  LOAD_GLOBAL              open
                2  LOAD_FAST                'file_location'
                4  LOAD_STR                 'w'
                6  CALL_FUNCTION_2       2  ''
                8  SETUP_WITH           32  'to 32'
               10  STORE_FAST               'outfile'

 L.  24        12  LOAD_GLOBAL              yaml
               14  LOAD_ATTR                dump
               16  LOAD_FAST                'data'
               18  LOAD_FAST                'outfile'
               20  LOAD_CONST               False
               22  LOAD_CONST               ('default_flow_style',)
               24  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               26  POP_TOP          
               28  POP_BLOCK        
               30  BEGIN_FINALLY    
             32_0  COME_FROM_WITH        8  '8'
               32  WITH_CLEANUP_START
               34  WITH_CLEANUP_FINISH
               36  END_FINALLY      

Parse error at or near `BEGIN_FINALLY' instruction at offset 30


class ConfigGenerator:
    """ConfigGenerator"""

    def __init__(self, yaml_file_location: str):
        """
        Initializes the config generator from a yml file location
        :param yaml_file_location: relative file location of the yaml config
        """
        self.config_dict = parse_from_file(yaml_file_location)
        self.tuple_templates = self.build_tuples()
        self.arg_parser = self.build_arg_parser()
        self.args = None

    def __call__(self, args: List):
        """
        Parses the arguments. Needs to be called with sys.argv[1:] in general
        :param args: the argument (normally sys.argv[1:])
        :return: a dictionary of namedtuples filled with the defaults and the passed arguments
        """
        self.args = vars(self.arg_parser.parse_argsargs)
        return self.build_config()

    def build_tuples(self):
        """
        Builds a dictionary of namedtuples for easier config access
        :return: a dictionary of namedtuples from the config dictionary, and a tuple to hold all
            config tuples
        """
        return self.build_tuples_rec('Config', self.config_dict)

    def build_tuples_rec(self, key, config_dict):
        all_tuples = {}
        for k in config_dict:
            if isinstance(config_dict[k], dict):
                all_tuples[k] = self.build_tuples_rec(k, config_dict[k])
            return (namedtuple(key, config_dict.keys()), all_tuples)

    def build_arg_parser(self) -> argparse.ArgumentParser:
        """
        Builds the argument parser with default values from the config file
        :return: the argument parser
        """
        parser = argparse.ArgumentParser(description='Process args for experiments',
          formatter_class=(argparse.ArgumentDefaultsHelpFormatter))
        self.build_arg_parser_rec(self.config_dict, parser)
        return parser

    def build_arg_parser_rec(self, config_dict, group):
        for k, v in config_dict.items():
            if isinstance(v, dict):
                sub_group = group.add_argument_groupk
                self.build_arg_parser_rec(v, sub_group)
            elif type(v) == bool:
                bool_group = group.add_mutually_exclusive_group(required=False)
                bool_group.add_argument(('--' + k.replace('_', '-')), dest=k, default=v, action='store_true', help=' ')
                bool_group.add_argument(('--no-' + k.replace('_', '-')), dest=k, default=v, action='store_false', help=' ')
            elif type(v) == list:
                try:
                    list_item_type = type(v[0])
                except IndexError as e:
                    try:
                        print('Cannot parse default type from list without items')
                    finally:
                        e = None
                        del e

                else:
                    group.add_argument(('--' + k.replace('_', '-')), nargs='+', default=v, type=list_item_type, help=' ')
            else:
                group.add_argument(('--' + k.replace('_', '-')), default=v, type=(type(v)), help=' ')

    def build_config(self):
        """
        Builds the config, iterating over the internal dict and replacing values from the dict with
        the parsed arguments as needed
        :return: a dictionary of namedtuples containing the generated config
        """
        if self.args is None:
            raise ValueError('ConfigGenerator has no parsed arguments')
        arg_dict = self.args
        tuple_config, dict_config = self.build_config_rec(arg_dict, self.config_dict, self.tuple_templates)
        self.config_dict = dict_config
        return tuple_config

    def build_config_rec(self, arg_dict, config_dict, templates):
        used_config = dict()
        dict_config = dict()
        for k, v in config_dict.items():
            if isinstance(v, dict):
                used_config[k], dict_config[k] = self.build_config_rec(arg_dict, v, templates[1][k])
            elif k in arg_dict:
                used_config[k] = dict_config[k] = arg_dict[k]
            else:
                used_config[k] = dict_config[k] = v

        return (
         (templates[0])(**used_config), dict_config)

    def append_argument_to_config(self, argument_path, default):
        d = self.config_dict
        for a in argument_path[:-1]:
            d = d[a]

        d[argument_path[(-1)]] = default

    def recompile(self):
        self.tuple_templates = self.build_tuples()
        self.arg_parser = self.build_arg_parser()
        self.args = None

    def dump_config(self, file_location: str):
        """
        Writes the config back to a file in yml format, which can be loaded again
        :param file_location: the relative file location
        """
        if self.args is None:
            raise ValueError('ConfigGenerator has no parsed arguments')
        arg_dict = self.args
        save_dict = dict()
        for c in self.config_dict:
            save_dict_section = {}
            for k, v in self.config_dict[c].items():
                if k in arg_dict:
                    save_dict_section[k] = arg_dict[k]
                else:
                    save_dict_section[k] = v

            save_dict[c] = save_dict_section

        write_to_file(save_dict, file_location)