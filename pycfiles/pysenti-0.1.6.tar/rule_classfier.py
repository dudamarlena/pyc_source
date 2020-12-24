# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/xuming06/Codes/sentiment-classifier-zh/pysenti/rule_classfier.py
# Compiled at: 2019-09-22 00:56:53
"""
@author:XuMing（xuming624@qq.com)
@description: 
"""
from codecs import open
from collections import OrderedDict
from pysenti import config
from pysenti import tokenizer
from pysenti.compat import strdecode
from pysenti.utils import split_sentence

class RuleClassifier(object):

    def __init__(self):
        self.name = 'rule_classifier'
        self.sentiment_dict = {}
        self.conjunction_dict = {}
        self.adverb_dict = {}
        self.denial_dict = {}
        self.user_sentiment_dict = {}
        self.inited = False

    def init(self, sentiment_dict_path=config.sentiment_dict_path):
        self.sentiment_dict = self._get_dict(sentiment_dict_path)
        self.conjunction_dict = self._get_dict(config.conjunction_dict_path)
        self.adverb_dict = self._get_dict(config.adverb_dict_path)
        self.denial_dict = self._get_dict(config.denial_dict_path)
        self.inited = True

    def load_user_sentiment_dict(self, path):
        if not self.inited:
            self.init()
        self.user_sentiment_dict = self._get_dict(path)
        self.sentiment_dict.update(self.user_sentiment_dict)

    def classify(self, text):
        if not self.inited:
            self.init()
        result = OrderedDict(score=0)
        text = strdecode(text)
        clauses = split_sentence(text)
        for i in range(len(clauses)):
            sub_clause = self._analyse_clause(clauses[i])
            result['sub_clause' + str(i)] = sub_clause
            result['score'] += sub_clause['score']

        return result

    def _analyse_clause(self, clause):
        sub_clause = {'score': 0, 'sentiment': [], 'conjunction': []}
        seg_result = tokenizer.segment(clause, pos=False)
        for word in seg_result:
            r = self._is_word_conjunction(word)
            if r:
                sub_clause['conjunction'].append(r)
            r = self._is_word_sentiment(word, seg_result)
            if r:
                sub_clause['sentiment'].append(r)
                sub_clause['score'] += r['score']

        for a_conjunction in sub_clause['conjunction']:
            sub_clause['score'] *= a_conjunction['value']

        return sub_clause

    def _is_word_conjunction(self, the_word):
        r = {}
        if the_word in self.conjunction_dict:
            r = {'key': the_word, 'value': self.conjunction_dict[the_word]}
        return r

    def _is_word_sentiment(self, the_word, seg_result, index=-1):
        r = {}
        if the_word in self.sentiment_dict:
            r = self._emotional_word_analysis(the_word, self.sentiment_dict[the_word], seg_result, index)
        return r

    def _emotional_word_analysis(self, core_word, value, segments, index):
        orientation = {'key': core_word, 'adverb': [], 'denial': [], 'value': value}
        orientation_score = value
        view_window = index - 1
        if view_window > -1:
            if segments[view_window] in self.sentiment_dict:
                orientation['score'] = orientation_score
                return orientation
            if segments[view_window] in self.adverb_dict:
                adverb = {'key': segments[view_window], 'sentiment': 1, 'value': self.adverb_dict[segments[view_window]]}
                orientation['adverb'].append(adverb)
                orientation_score *= self.adverb_dict[segments[view_window]]
            elif segments[view_window] in self.denial_dict:
                denial = {'key': segments[view_window], 'sentiment': 1, 'value': self.denial_dict[segments[view_window]]}
                orientation['denial'].append(denial)
                orientation_score *= -1
        view_window = index - 2
        if view_window > -1:
            if segments[view_window] in self.sentiment_dict:
                orientation['score'] = orientation_score
                return orientation
            if segments[view_window] in self.adverb_dict:
                adverb = {'key': segments[view_window], 'sentiment': 2, 'value': self.adverb_dict[segments[view_window]]}
                orientation_score *= self.adverb_dict[segments[view_window]]
                orientation['adverb'].insert(0, adverb)
            elif segments[view_window] in self.denial_dict:
                denial = {'key': segments[view_window], 'sentiment': 2, 'value': self.denial_dict[segments[view_window]]}
                orientation['denial'].insert(0, denial)
                orientation_score *= -1
                if len(orientation['adverb']) > 0:
                    orientation_score *= 0.3
        view_window = index - 3
        if view_window > -1:
            if segments[view_window] in self.sentiment_dict:
                orientation['score'] = orientation_score
                return orientation
            if segments[view_window] in self.adverb_dict:
                adverb = {'key': segments[view_window], 'sentiment': 3, 'value': self.adverb_dict[segments[view_window]]}
                orientation_score *= self.adverb_dict[segments[view_window]]
                orientation['adverb'].insert(0, adverb)
            elif segments[view_window] in self.denial_dict:
                denial = {'key': segments[view_window], 'sentiment': 3, 'value': self.denial_dict[segments[view_window]]}
                orientation['denial'].insert(0, denial)
                orientation_score *= -1
                if len(orientation['adverb']) > 0 and len(orientation['denial']) == 0:
                    orientation_score *= 0.3
        orientation['score'] = orientation_score
        return orientation

    @staticmethod
    def _get_dict(path, encoding='utf-8'):
        u"""
        情感词典的构建
        :param path:
        :param encoding:
        :return:
        """
        sentiment_dict = {}
        with open(path, 'r', encoding=encoding) as (f):
            c = 0
            for line in f:
                parts = line.strip().split()
                c += 1
                if len(parts) == 2:
                    sentiment_dict[parts[0]] = float(parts[1])
                else:
                    print (
                     'error', c, line)

        return sentiment_dict


if __name__ == '__main__':
    d = RuleClassifier()
    d.load_user_sentiment_dict('../extra_dict/user_sentiment_dict.txt')
    print d.user_sentiment_dict
    a_sentence = [
     '剁椒鸡蛋好难吃。绝对没人受得了',
     '土豆丝很好吃', '土豆丝很难吃',
     '这笔钱是个天文数字',
     '我一会儿出去玩了，你吃啥？给你带,然而你不知道']
    for i in a_sentence:
        r = d.classify(i)
        print (i, r)