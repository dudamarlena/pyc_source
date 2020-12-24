# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/concurrent_tree_crawler/bin/sample_download_crawler.py
# Compiled at: 2011-09-28 13:50:09
"""
This script initializes the crawler to downloade pages from a sample web site.
"""

def set_path_to_package_root():
    """
        Calling this function esures that: 1) if this script is placed inside
        the C{concurrent_tree_crawler} package files, when importing the 
        C{concurrent_tree_crawler} package it uses these package files, 
        2) otherwise, in situtation when the script is in some other place and
        we want to use the library C{concurrent_tree_crawler} installed in the
        system, it uses this library when importing the C{concurrent_tree_crawler}.
        """
    import sys, os.path
    sys.path[0] = os.path.join(sys.path[0], '../..')


set_path_to_package_root()
from concurrent_tree_crawler.cmdln_multithreaded_crawler import CmdLnMultithreadedCrawler
from concurrent_tree_crawler.html_multipage_navigator.cmdln.navigators_creator import CmdLnNavigatorsCreator
from concurrent_tree_crawler.html_multipage_navigator.cmdln.sample_levels_creator import SampleCmdLnLevelsCreator
navigators_creator = CmdLnNavigatorsCreator(SampleCmdLnLevelsCreator())
crawler = CmdLnMultithreadedCrawler(navigators_creator)
crawler.run()