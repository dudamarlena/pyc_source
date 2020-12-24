# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/unno/.pyenv/versions/2.7.8/lib/python2.7/site-packages/mrep/morph.py
# Compiled at: 2014-10-10 01:33:07
import MeCab

class MeCabParser(object):

    def __init__(self, arg=''):
        model = MeCab.Model_create(arg)
        if model is None:
            raise Exception('Cannot initialize mecab')
        self.model = model
        return

    def parse(self, s):
        tagger = self.model.createTagger()
        lattice = self.model.createLattice()
        lattice.set_sentence(s)
        tagger.parse(lattice)
        node = lattice.bos_node()
        morphs = []
        while node:
            if node.surface != '':
                feature = node.feature
                morphs.append({'surface': node.surface, 
                   'pos': feature[0:feature.find(',')], 
                   'feature': feature})
            node = node.next

        return morphs