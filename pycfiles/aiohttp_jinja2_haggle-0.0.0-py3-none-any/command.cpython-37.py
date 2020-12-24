# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\aiohttp_init\command.py
# Compiled at: 2019-10-11 05:22:07
# Size of source mod 2**32: 621 bytes
__doc__ = '\n@File    :   command.py\n@Time    :   2019/10/11 15:09:47\n@Author  :   lateautumn4lin\n@PythonVersion  :   3.7\n'
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