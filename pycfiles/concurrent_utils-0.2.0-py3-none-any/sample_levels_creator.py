# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/concurrent_tree_crawler/html_multipage_navigator/cmdln/sample_levels_creator.py
# Compiled at: 2011-09-28 13:50:09
from concurrent_tree_crawler.html_multipage_navigator.cmdln.abstract_levels_creator import AbstractCmdLnLevelsCreator
from concurrent_tree_crawler.html_multipage_navigator.sample_page_analyzer import LevelsCreator
from concurrent_tree_crawler.common.file_helper import lenient_makedir

class SampleCmdLnLevelsCreator(AbstractCmdLnLevelsCreator):

    def fill_parser(self, parser):
        parser.add_argument('destination_dir', help='directory where the downloaded pages will be saved.')

    def create(self, args):
        lenient_makedir(args.destination_dir)
        return LevelsCreator(args.destination_dir).create()