# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/cnsenti/emotion.py
# Compiled at: 2020-03-26 02:55:53
# Size of source mod 2**32: 2486 bytes
import jieba, pickle, pathlib, re

class Emotion(object):
    """Emotion"""

    def __init__(self):
        self.Haos = self.read_dict('好.pkl')
        self.Les = self.read_dict('乐.pkl')
        self.Ais = self.read_dict('哀.pkl')
        self.Nus = self.read_dict('怒.pkl')
        self.Jus = self.read_dict('惧.pkl')
        self.Wus = self.read_dict('恶.pkl')
        self.Jings = self.read_dict('惊.pkl')

    def read_dict(self, file):
        pathchain = [
         'dictionary', 'dutir', file]
        mood_dict_filepath = (pathlib.Path(__file__).parent.joinpath)(*pathchain)
        dict_f = open(mood_dict_filepath, 'rb')
        words = pickle.load(dict_f)
        return words

    def emotion_count(self, text):
        """
        简单情感分析，未考虑强度副词、否定词对情感的复杂影响。仅仅计算各个情绪词出现次数(占比)
        :param text:  中文文本字符串
        :return: 返回文本情感统计信息，类似于这样{'words': 22, 'sentences': 2, '好': 0, '乐': 4, '哀': 0, '怒': 0, '惧': 0, '恶': 0, '惊': 0}
        """
        wordnum, sentences, hao, le, ai, nu, ju, wu, jing = (0, 0, 0, 0, 0, 0, 0, 0,
                                                             0)
        sentences = len(re.split('[\\.。！!？\\?\n;；]+', text))
        words = jieba.lcut(text)
        wordnum = len(words)
        for w in words:
            if w in self.Haos:
                hao += 1
            elif w in self.Les:
                le += 1
            elif w in self.Ais:
                ai += 1
            elif w in self.Nus:
                nu += 1
            elif w in self.Jus:
                ju += 1
            else:
                if w in self.Wus:
                    wu += 1

        result = {'words':wordnum, 
         'sentences':sentences,  '好':hao,  '乐':le,  '哀':ai,  '怒':nu,  '惧':ju,  '恶':wu,  '惊':jing}
        return result