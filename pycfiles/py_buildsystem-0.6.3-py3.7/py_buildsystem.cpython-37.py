# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\py_buildsystem\py_buildsystem.py
# Compiled at: 2019-01-14 14:07:24
# Size of source mod 2**32: 1105 bytes
import sys, argparse
from py_buildsystem.common import logger, levels
import py_buildsystem.Project.Project as Project
import py_buildsystem.Toolchain.Toolchain as Toolchain
sys.tracebacklimit = 0
parser = argparse.ArgumentParser(usage='python -m py_buildsystem [options]', description='Python based build system.')
parser.add_argument('compiler_config', metavar='CC', type=str, nargs=1, help='Compiler configuration file')
parser.add_argument('project_config', metavar='PC', type=str, nargs=1, help='Project configuration file')
parser.add_argument('compiler_path', metavar='path', type=str, nargs='?', default='', help='Path to compiler')
parser.add_argument('-v', '--verbose', action='store_true', help='verbose mode')
args = parser.parse_args()
if args.v is True:
    logger.setLevel(levels['DEBUG'])
else:
    logger.setLevel(levels['INFO'])
toolchain = Toolchain(args.compiler_config[0], args.compiler_path)
project = Project(args.project_config[0], toolchain)