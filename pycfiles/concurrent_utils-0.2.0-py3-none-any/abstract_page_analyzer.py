# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/concurrent_tree_crawler/html_multipage_navigator/abstract_page_analyzer.py
# Compiled at: 2011-09-28 13:50:09
from concurrent_tree_crawler.html_multipage_navigator.web_browser import AbstractWebBrowser

class PageLinks:

    def __init__(self, children, next_page_link):
        """
                @param children: list of (name of child, link to the child) pairs.
                @param next_page_link: link to the next page corresponding to the
                        same node.
                """
        self.children = children
        self.next_page_link = next_page_link


class AbstractPageAnalyzer:

    def process(self, tree_path, page_file):
        """
                Process the node (normally, this method is called once for every node).

                @param tree_path: path to the tree node the navigator is currently in 
                        i.e. subsequent node names from the tree root to the current node.
                        This might be e.g. C{["root"]} for a path to the root node or
                        C{["root", "magazine-2011-09-18", "article_23"]} for some other
                        node inside the tree hierarchy.
                @type tree_path: list of strings
                @param page_file: file-like structure to be processed
                """
        pass

    def get_links(self, page_file, child_links_retrieved_so_far_count):
        """
                @param page_file: file-like structure to be analyzed
                @param child_links_retrieved_so_far_count: number of child links 
                        retrieved so far in current node (from previous pages)
                @return: information about links on the given page. 
                        The given default implementation is made for a leaf node 
                        (a page with no children).
                @rtype: L{PageLinks}
                """
        return PageLinks([], None)


class Level:

    def __init__(self, name, page_analyzer):
        """
                @type name: Name of the level. 
                        Example names: "books", "chapters", "sections".
                @type page_analyzer: L{AbstractPageAnalyzer}
                """
        self.name = name
        self.page_analyzer = page_analyzer


class AbstractLevelsCreator:
    """
        A class responsible for creating a list of C{Level}s which 
        describe structure of the explored web site.
        """

    def create(self):
        """
                Create list of L{Level}s. The first element is a level 
                corresponding to the root node, the last one corresponds to     a leaf.
                """
        raise NotImplementedError()