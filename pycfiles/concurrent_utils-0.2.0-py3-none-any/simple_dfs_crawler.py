# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/concurrent_tree_crawler/simple_dfs_crawler.py
# Compiled at: 2011-09-28 13:50:09
from concurrent_tree_crawler.abstract_tree_navigator import AbstractTreeNavigator

class SimpleDFSCrawler:

    def __init__(self, navigator):
        """@type navigator: C{AbstractTreeNavigator}"""
        self.__navigator = navigator

    def run(self):
        self.__navigator.start_in_root()
        self.__process_current_node()

    def __process_current_node(self):
        is_leaf = None
        try:
            is_leaf = self.__navigator.process_node_and_check_if_is_leaf()
        except Exception as _:
            pass

        if not is_leaf:
            children = self.__navigator.get_children()
            for child in children:
                self.__navigator.move_to_child(child)
                self.__process_current_node()
                self.__navigator.move_to_parent()

        return