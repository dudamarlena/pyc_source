# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/concurrent_tree_crawler/test/simple_dfs_crawler_test.py
# Compiled at: 2011-09-28 13:52:18
import unittest
from concurrent_tree_crawler.common.resources import Resources
from concurrent_tree_crawler.common.dir_tree_comparer import are_dir_trees_equal
from concurrent_tree_crawler.simple_dfs_crawler import SimpleDFSCrawler
from concurrent_tree_crawler.html_multipage_navigator.tree_navigator import HTMLMultipageNavigator
from concurrent_tree_crawler.html_multipage_navigator.sample_page_analyzer import LevelsCreator
from concurrent_tree_crawler.common.tempdir import TempDir

class SimpleDFSCrawlerTestCase(unittest.TestCase):

    def test_website_download(self):
        with TempDir() as (temp_dir):
            levels = LevelsCreator(temp_dir.get_path()).create()
            address = 'file:' + Resources.path(__file__, 'data/original_site-without_broken_links/issues_1.html', convert_to_url=True)
            navigator = HTMLMultipageNavigator(address, levels)
            crawler = SimpleDFSCrawler(navigator)
            crawler.run()
            expected_dir = Resources.path(__file__, 'data/expected_download-without_broken_links')
            actual_dir = temp_dir.get_path()
            self.assert_(are_dir_trees_equal(expected_dir, actual_dir, ignore=[
             '.gitignore']))