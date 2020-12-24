# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/concurrent_tree_crawler/abstract_cmdln_navigators_creator.py
# Compiled at: 2011-09-28 13:50:09
import argparse

class AbstractCmdLnNavigatorsCreator:

    def fill_parser(self, parser):
        """
                Fill the given parser object with command-line arguments needed to
                initialize navigators which are created in L{create} method.

                @type parser: L{argparse.ArgumentParser}
                """
        raise NotImplementedError()

    def create(self, args, navigators_count):
        """
                Create navigators based on arguments from command-line.
                
                @param args: result of calling the C{parser.parse_args()} function. 
                        Contains results of parsing of the arguments defined in 
                        L{fill_parser} method.
                @type args: L{argparse.Namespace}
                @param navigators_count: number of L{AbstractTreeNavigator}s to create
                @return: navigators that will be used by the crawler threads. 
                        Each navigator will be used by a single thread.
                @rtype: list of L{AbstractTreeNavigator}s
                """
        raise NotImplementedError()

    def on_exit(self):
        """
                This method is called before the program exit. 
                This is the place to do some cleanup.
                """
        raise NotImplementedError()