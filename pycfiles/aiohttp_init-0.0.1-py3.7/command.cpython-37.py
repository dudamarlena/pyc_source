# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\aiohttp_init\command.py
# Compiled at: 2019-10-11 05:22:07
# Size of source mod 2**32: 621 bytes
"""
@File    :   command.py
@Time    :   2019/10/11 15:09:47
@Author  :   lateautumn4lin
@PythonVersion  :   3.7
"""
import argparse
from core.initialize import Initialize
from .logger import logger
parser = argparse.ArgumentParser(description='Auto Create Robust Web Projects Of Python3 For Humans')
parser.add_argument('-N',
  '--name',
  default='test',
  help='Customize Project Name')
args = parser.parse_args()

def main():
    init = Initialize()
    init.create(project_name=(args.name))


main()