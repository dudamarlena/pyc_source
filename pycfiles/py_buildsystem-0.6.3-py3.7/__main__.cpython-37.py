# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\py_buildsystem\__main__.py
# Compiled at: 2019-06-15 04:36:32
# Size of source mod 2**32: 1262 bytes
import os, sys, argparse
from py_buildsystem.common import logger, levels, MAX_LOG_LEVEL
import py_buildsystem.Project.Project as Project
import py_buildsystem.Toolchain.Toolchain as Toolchain
sys.tracebacklimit = 0
parser = argparse.ArgumentParser(prog='py_buildsystem', description='Python based build system.', allow_abbrev=True)
parser.add_argument('-pcc', '--project_compiler_config', type=str, nargs=1, required=True, help='Project specific toolchain configuration file')
parser.add_argument('-pc', '--project_config', type=str, nargs=1, default=(os.getcwd()), required=True, help='Project configuration file')
parser.add_argument('compiler_path', metavar='compiler path', type=str, nargs='?', default='', help='Path to compiler')
parser.add_argument('-v', '--verbose', action='count', dest='verbose', default=0, help='verbose mode')
args = parser.parse_args()
logger.setLevel(levels[min(args.verbose, MAX_LOG_LEVEL)])
toolchain = Toolchain(args.project_compiler_config[0], args.compiler_path)
project = Project(args.project_config[0], toolchain)
if any(project.get_exit_codes()):
    exit(-1)
else:
    exit(0)