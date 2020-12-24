# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/concurrent_tree_crawler/html_multipage_navigator/cmdln/abstract_levels_creator.py
# Compiled at: 2011-09-28 13:50:09
import argparse
from concurrent_tree_crawler.html_multipage_navigator.sample_page_analyzer import LevelsCreator

class AbstractCmdLnLevelsCreator:

    def fill_parser(self, parser):
        """
                Fill the given parser object with command-line arguments needed to
                initialize levels creator returned in L{create} method.

                @type parser: L{argparse.ArgumentParser}
                """
        pass

    def create(self, args):
        """
                Create L{AbstractLevelsCreator} based on command line arguments.
                
                @param args: result of calling the C{parser.parse_args()} function. 
                        Contains result of parsing the arguments defined in L{fill_parser}
                        method.
                @type args: L{argparse.Namespace}
                @rtype: L{AbstractLevelsCreator}
                """
        raise NotImplementedError()

    def on_exit(self):
        """
                This method is called before the program exit. 
                This is the place to execute some cleanup actions.
                """
        pass