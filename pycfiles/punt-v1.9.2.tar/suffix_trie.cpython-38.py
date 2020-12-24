# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/punsy/structs/suffix_trie.py
# Compiled at: 2020-02-18 00:19:24
# Size of source mod 2**32: 2363 bytes
__doc__ = "\nA python implementation of the Trie data structure, specialising in searching by _suffix_.\n\n    https://en.wikipedia.org/wiki/Trie\n\nThis trie has the ability to store and search words in reverse\n\ne.g. to find words rhyming with '-at', the search is reversed to 'ta' and then\nthe child nodes 'b' (bat) and 'c' (cat) are returned.\n\nt - a - b\n      \\ c\n\nUsage:\n\nt = SuffixTrie()                    # create a suffix trie\n\nt.insert(['K1', 'AH1', 'T'], 'cat') # insert a pronunciation sequence and associated word metadata into the trie\nt[['K1', 'AH1', 'T']]               # retrieve a node from the trie\nt,              print(t)            # print the contents of the trie\nprint(t.json())                     # pretty-print the trie as a JSON object\nt.rhymes_for_suffix(['AH1', 'T'])   # return all data for words ending in 'at'\nt.rhymes_for_suffix(\n    ['K1', 'AH1', 'T'],\n    offset=1\n)                                   # return all data for words rhyming with 'kat' (i.e. ending in 'at')\n"
import json, os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from punsy.structs.trie import Trie

class SuffixTrie:

    def __init__(self):
        self.trie = Trie()

    def insert(self, word, data):
        self.trie.insert(list(reversed(word)), data)

    def __getitem__(self, word):
        return self.trie.__getitem__(list(reversed(word)))

    def json(self):
        return json.dumps((self.trie.asdict()), indent=2)

    def rhymes_for_suffix(self, word, offset=0, max_depth=10):
        """Return all rhymes for the word/suffix, skipping <offset> number of
        syllables, and returning matches of
        length=(<max_depth> + <length of word>)"""
        return SuffixTrie._collect_child_data((self.__getitem__(word[offset:])),
          max_depth=max_depth,
          results=(list()))

    @staticmethod
    def _collect_child_data(node, max_depth=10, results=list()):
        if node.final:
            results.extend(node.data)
        for key, child in node.children.items():
            if max_depth > 0:
                SuffixTrie._collect_child_data(child, max_depth - 1, results)
            return results


if __name__ == '__main__':
    from IPython import embed
    print(__doc__)
    embed()