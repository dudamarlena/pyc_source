# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/davidam/git/damenltk/source/test/test_corpus.py
# Compiled at: 2019-10-30 10:18:49
# Size of source mod 2**32: 4333 bytes
import unittest, nltk
from nltk.corpus import PlaintextCorpusReader
from nltk.corpus import inaugural
from nltk.corpus import gutenberg
from nltk.corpus import reuters
from nltk.corpus import cmudict
from nltk.corpus import twitter_samples
from nltk.corpus import verbnet
from nltk.corpus import wordnet

class TddInPythonExample(unittest.TestCase):

    def test_corpus_fileids_method_returns_correct_result(self):
        fileids = inaugural.fileids()
        self.assertEqual(['1789-Washington.txt', '1793-Washington.txt', '1797-Adams.txt'], fileids[0:3])

    def test_corpus_sents_method_returns_correct_result(self):
        sents1 = [
         [
          '[', 'Sense', 'and', 'Sensibility', 'by', 'Jane', 'Austen', '1811', ']'], ['CHAPTER', '1']]
        self.assertEqual(gutenberg.sents('austen-sense.txt')[0:2], sents1)

    def test_corpus_categories_method_returns_correct_result(self):
        cat = reuters.categories()[0:2]
        self.assertEqual(cat, ['acq', 'alum'])

    def test_corpus_cmudict_method_returns_correct_result(self):
        transcr = cmudict.dict()
        t = [transcr[w][0] for w in 'Natural Language Tool Kit'.lower().split()]
        self.assertEqual(t, [['N', 'AE1', 'CH', 'ER0', 'AH0', 'L'], ['L', 'AE1', 'NG', 'G', 'W', 'AH0', 'JH'], ['T', 'UW1', 'L'], ['K', 'IH1', 'T']])

    def test_corpus_twitter_method_returns_correct_result(self):
        self.assertEqual(twitter_samples.fileids(), ['negative_tweets.json', 'positive_tweets.json', 'tweets.20150430-223406.json'])
        self.assertEqual(twitter_samples.strings('negative_tweets.json')[0], 'hopeless for tmr :(')
        self.assertEqual(twitter_samples.strings('positive_tweets.json')[0], '#FollowFriday @France_Inte @PKuchly57 @Milipol_Paris for being top engaged members in my community this week :)')

    def test_corpus_verbnet_method_returns_correct_result(self):
        self.assertEqual(verbnet.classids('accept'), ['approve-77', 'characterize-29.2-1-1', 'obtain-13.5.2'])
        self.assertEqual(verbnet.longid('77'), 'approve-77')
        self.assertEqual(verbnet.lemmas()[0:10], ['December', 'FedEx', 'UPS', 'abandon', 'abase', 'abash', 'abate', 'abbreviate', 'abduct', 'abet'])

    def test_syn_returns_correct_result(self):
        syns = wordnet.synsets('program')
        self.assertEqual(syns[0].name(), 'plan.n.01')
        self.assertEqual(syns[0].lemmas()[0].name(), 'plan')
        self.assertEqual(syns[0].definition(), 'a series of steps to be carried out or goals to be accomplished')
        self.assertEqual(syns[0].examples(), ['they drew up a six-step plan', 'they discussed plans for a new bond issue'])

    def test_antonym_returns_correct_result(self):
        antonyms = []
        for syn in wordnet.synsets('good'):
            for l in syn.lemmas():
                if l.antonyms():
                    antonyms.append(l.antonyms()[0].name())

        self.assertEqual(['evil', 'evilness', 'bad', 'badness', 'bad', 'evil', 'ill'], antonyms)