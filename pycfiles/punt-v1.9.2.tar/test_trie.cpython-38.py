# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/test/structs/test_trie.py
# Compiled at: 2019-07-24 02:05:30
# Size of source mod 2**32: 2562 bytes
import unittest, os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from punsy.structs.trie import Trie
from punsy.structs.suffix_trie import SuffixTrie

class TestTrie(unittest.TestCase):

    def test_insert_suffixes(self):
        words = [
         'cat',
         'bat',
         'catinthehat',
         'rat']
        trie = Trie()
        for word in words:
            trie.insert(word)

        for word in words:
            self.assertTrue(trie[word].final)

    def test_insert(self):
        trie = Trie()
        words = {'NONE':[
          'N', 'AH1', 'N'], 
         'NAAN':[
          'N', 'AH1', 'N'], 
         'ONCE':[
          'W', 'AH1', 'N', 'S'], 
         'PUN':[
          'P', 'AH1', 'N']}
        for word, pronunciation in words.items():
            trie.insert(pronunciation, word)

        self.assertEqual(['NONE', 'NAAN'], trie[['N', 'AH1', 'N']].data)
        self.assertEqual(['ONCE'], trie[('W', 'AH1', 'N', 'S')].data)
        self.assertEqual(['PUN'], trie[('P', 'AH1', 'N')].data)

    def test_search_suffix(self):
        trie = SuffixTrie()
        words = {'NONE':[
          'N', 'AH1', 'N'], 
         'NAAN':[
          'N', 'AH1', 'N'], 
         'ONCE':[
          'W', 'AH1', 'N', 'S'], 
         'PUN':[
          'P', 'AH1', 'N'], 
         'ANSWER':[
          'AH1', 'N', 'S', 'ER']}
        for word, pronunciation in words.items():
            trie.insert(pronunciation, word)

        self.assertEqual([
         'NONE', 'NAAN', 'PUN'], trie.rhymes_for_suffix(['AH1', 'N']))

    def test_get_item(self):
        trie = SuffixTrie()
        trie.insert('A', 123)
        self.assertEqual([123], trie['A'].data)
        self.assertEqual('A', trie['A'].value)
        trie.insert('AB', 321)
        self.assertEqual([123], trie['A'].data)
        self.assertEqual('A', trie['A'].value)
        self.assertTrue(trie['A'].final)
        self.assertTrue('A' in trie['B'].children)
        self.assertEqual([321], trie['AB'].data)
        self.assertTrue(trie['AB'].final)
        trie.insert('CAB', 101)
        self.assertEqual(['A', 'B'], list(trie.trie.children.keys()))
        self.assertEqual([101], trie['CAB'].data)
        self.assertEqual('C', trie['CAB'].value)
        self.assertTrue(trie['CAB'].final)