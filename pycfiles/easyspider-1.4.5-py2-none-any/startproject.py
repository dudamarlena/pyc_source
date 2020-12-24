# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/zhanghang/Desktop/workspace/molbase/molbase_2017_7_3/release/easyspider/easyspider/commands/startproject.py
# Compiled at: 2017-08-03 10:12:10
import easyspider
from os.path import join, exists, abspath
from scrapy.commands.startproject import Command
from shutil import ignore_patterns, move, copy2, copystat

class easyCommand(Command):

    def run(self, args, opts):
        if len(args) not in (1, 2):
            raise UsageError()
        project_name = args[0]
        project_dir = args[0]
        if len(args) == 2:
            project_dir = args[1]
        if exists(join(project_dir, 'scrapy.cfg')):
            self.exitcode = 1
            print 'Error: scrapy.cfg already exists in %s' % abspath(project_dir)
            return
        if not self._is_valid_name(project_name):
            self.exitcode = 1
            return
        self._copytree(self.templates_dir, abspath(project_dir))

    @property
    def templates_dir(self):
        _templates_base_dir = join(easyspider.__path__[0], 'template_dir')
        return join(_templates_base_dir)