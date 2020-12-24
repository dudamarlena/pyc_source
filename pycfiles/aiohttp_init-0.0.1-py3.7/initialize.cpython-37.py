# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\aiohttp_init\core\initialize.py
# Compiled at: 2019-10-11 04:45:48
# Size of source mod 2**32: 2030 bytes
"""
@File    :   initialize.py
@Time    :   2019/08/10 14:37:02
@Author  :   linhanqiu
@PythonVersion  :   3.7
"""
import os
from pprint import pprint as print
from pathlib import Path
from dataclasses import dataclass
from jinja2 import Environment, FileSystemLoader
from ..logger import logger

@dataclass
class Initialize:

    def get_config(self, user_custom):
        config = {'project_name': user_custom.get('project_name', 'normal')}
        return config

    def create(self, **kwargs):
        logger.info('Init project Begin.')
        logger.info('Init project End.')

    def get_all_tpl(self, path, parent=None):
        if not path.is_dir():
            return [
             f"{parent}/{path.name}" if parent else path.name]
        tpl_list = []
        for sub_path in path.iterdir():
            tpl_list.extend(self.get_all_tpl(sub_path, f"{parent}/{path.name}" if parent else path.name))

        return tpl_list