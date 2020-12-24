# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\mad\__main__.py
# Compiled at: 2016-04-09 07:42:43
# Size of source mod 2**32: 1028 bytes
from sys import argv, stdout
from mad.parsing import Parser
from mad.datasource import Mad, InFilesDataSource
from mad.ui import Display, Arguments
source = InFilesDataSource()
mad = Mad(Parser(source), source)
cli = CommandLineInterface(Display(stdout), mad)
project = Arguments(argv[1:]).as_project
cli.simulate(project)