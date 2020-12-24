# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: c:\users\christian\documents\github\arduino_helpers\arduino_helpers\hardware\boards.py
# Compiled at: 2015-07-10 07:37:49
from path_helpers import path
from . import parse_config

def get_board_data_by_family(arduino_home_path):
    """
    Return a nested dictionary containing configuration from all boards
    supported by an Arduino installation home directory.
    """
    arduino_home_path = path(arduino_home_path).expand()
    pre_1_5_boards_path = arduino_home_path.joinpath('hardware', 'arduino', 'boards.txt')
    if pre_1_5_boards_path.isfile():
        boards_by_family = {'avr': parse_config(pre_1_5_boards_path)}
    else:
        hardware_family_directory = arduino_home_path.joinpath('hardware', 'arduino')
        boards_by_family = dict([ (str(d.name), parse_config(d.joinpath('boards.txt'))) for d in hardware_family_directory.dirs()
                                ])
    return boards_by_family