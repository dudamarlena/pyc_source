# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\dev\PyCharm Projects\NCryptoClient\NCryptoClient\Utils\constants.py
# Compiled at: 2018-04-19 15:52:58
# Size of source mod 2**32: 574 bytes
"""
Module for client application constants.
"""
from pathlib import Path
path_tokens = Path(__file__).parts
project_pos = path_tokens.index('NCryptoClient')
project_path = path_tokens[0:project_pos + 2]
logo_rel_path = '\\Img\\NCryptoLogo_750x206.png'
add_rel_path = '\\Img\\add_24x24.png'
remove_rel_path = '\\Img\\remove_24x24.png'
NCRYPTOLOGO_IMG_PATH = '\\'.join(project_path) + logo_rel_path
ADD_CONTACT_IMG_PATH = '\\'.join(project_path) + add_rel_path
REMOVE_CONTACT_IMG_PATH = '\\'.join(project_path) + remove_rel_path