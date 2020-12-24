# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/cnsenti/sentiment.py
# Compiled at: 2020-04-12 00:05:45
# Size of source mod 2**32: 9809 bytes
import jieba, numpy as np, pickle, pathlib, re

class Sentiment(object):
    __doc__ = '\n    文本情感计算类，支持导入自定义词典\n\n    默认使用知网Hownet词典进行情感分析\n        >>> from cnsenti import Sentiment\n        >>> senti = Sentiment()\n\n    统计文本中情感词个数，\n    返回的pos和neg是词语个数\n        >>>test_text= \'我好开心啊，非常非常非常高兴！今天我得了一百分，我很兴奋开心，愉快，开心\'\n        >>>senti.sentiment_count(test_text)\n        >>>{\'words\': 24, \'sentences\': 2, \'pos\': 4, \'neg\': 0}\n\n    考虑强度副词(如"非常"，"差不多")对情感形容词的修饰作用，\n    和否定词对情感意义的反转作用。\n    返回的pos和neg是得分\n        >>>senti.sentiment_calculate(test_text)\n        >>>{\'sentences\': 2, \'words\': 24, \'pos\': 46.0, \'neg\': 0.0}\n\n\n    使用自定义txt词典(建议utf-8编码)，\n    目前仅支持pos和neg两类词典，每行一个词语。\n    merge=True，cnsenti会融合自带的词典和用户导入的自定义词典；merge=False，cnsenti只使导入的自定义词典\n    其中pos和neg为txt词典文件路径，encoding为txt词典的编码方式\n    这里是utf-8编码的文件，初始化方式\n        >>>from cnsenti import Sentiment\n        >>>senti = Sentiment(pos=\'正面词典.txt\', neg=\'负面词典.txt\', merge=True, encoding=\'utf-8\')\n    '

    def __init__(self, merge=True, pos=None, neg=None, encoding='utf-8'):
        """
        :pos 正面词典的txt文件
        :neg 负面词典的txt文件
        :merge 默认merge=True,即融合自带情感词典和自定义词典。merge=False，只使用自定义词典。
        :encoding 词典txt文件的编码，默认为utf-8。如果是其他编码，该参数必须使用
        """
        self.Poss = self.load_dict('pos.pkl')
        self.Negs = self.load_dict('neg.pkl')
        if pos:
            if merge:
                del self.Poss
                self.Poss = self.load_diydict(file=pos, encoding=encoding) + self.load_dict('pos.pkl')
                jieba.load_userdict(pos)
            else:
                del self.Poss
                self.Poss = self.load_diydict(file=pos, encoding=encoding)
                jieba.load_userdict(pos)
        elif neg:
            if merge:
                del self.Negs
                self.Negs = self.load_diydict(file=neg, encoding=encoding) + self.load_dict('neg.pkl')
                jieba.load_userdict(pos)
            else:
                del self.Negs
                self.Negs = self.load_diydict(file=neg, encoding=encoding)
                jieba.load_userdict(pos)
        self.Denys = self.load_dict('deny.pkl')
        self.Extremes = self.load_dict('extreme.pkl')
        self.Verys = self.load_dict('very.pkl')
        self.Mores = self.load_dict('more.pkl')
        self.Ishs = self.load_dict('ish.pkl')

    def load_dict(self, file):
        """
        Sentiment内置的读取hownet自带pkl词典
        :param file:  词典pkl文件
        :return: 词语列表
        """
        pathchain = [
         'dictionary', 'hownet', file]
        mood_dict_filepath = (pathlib.Path(__file__).parent.joinpath)(*pathchain)
        dict_f = open(mood_dict_filepath, 'rb')
        words = pickle.load(dict_f)
        return words

    def load_diydict(self, file, encoding):
        """
        :param file:  自定义txt情感词典，其中txt文件每行只能放一个词
        :param encoding:  txt文件的编码方式
        :return:
        """
        text = open(file, encoding=encoding).read()
        words = text.split('\n')
        words = [w for w in words if w]
        return words

    def sentiment_count(self, text):
        """
        简单情感分析，未考虑强度副词、否定词对情感的复杂影响。仅仅计算各个情绪词出现次数(占比)
        :param text:  中文文本字符串
        :return: 返回情感信息，形如{'sentences': 2, 'words': 24, 'pos': 46.0, 'neg': 0.0}
        """
        length, sentences, pos, neg = (0, 0, 0, 0)
        sentences = [s for s in re.split('[\\.。！!？\\?\n;；]+', text) if s]
        sentences = len(sentences)
        words = jieba.lcut(text)
        length = len(words)
        for w in words:
            if w in self.Poss:
                pos += 1

        return {'words':length, 
         'sentences':sentences,  'pos':pos,  'neg':neg}

    def judgeodd(self, num):
        """
        判断奇数偶数。当情感词前方有偶数个否定词，情感极性方向不变。奇数会改变情感极性方向。
        """
        if num % 2 == 0:
            return 'even'
        return 'odd'

    def sentiment_calculate(self, text):
        """
        考虑副词对情绪形容词的修饰作用和否定词的反转作用，
        其中副词对情感形容词的情感赋以权重，
        否定词确定情感值正负。

        :param text:  文本字符串
        :return: 返回情感信息，刑如{'sentences': 2, 'words': 24, 'pos': 46.0, 'neg': 0.0}
        """
        sentences = [s for s in re.split('[\\.。！!？\\?\n;；]+', text) if s]
        wordnum = len(jieba.lcut(text))
        count1 = []
        count2 = []
        for sen in sentences:
            segtmp = jieba.lcut(sen)
            i = 0
            a = 0
            poscount = 0
            poscount2 = 0
            poscount3 = 0
            negcount = 0
            negcount2 = 0
            negcount3 = 0
            for word in segtmp:
                if word in self.Poss:
                    poscount += 1
                    c = 0
                    for w in segtmp[a:i]:
                        if w in self.Extremes:
                            poscount *= 4.0
                        elif w in self.Verys:
                            poscount *= 3.0
                        elif w in self.Mores:
                            poscount *= 2.0
                        else:
                            if w in self.Ishs:
                                poscount *= 0.5

                    if self.judgeodd(c) == 'odd':
                        poscount *= -1.0
                        poscount2 += poscount
                        poscount = 0
                        poscount3 = poscount + poscount2 + poscount3
                        poscount2 = 0
                    else:
                        poscount3 = poscount + poscount2 + poscount3
                        poscount = 0
                    a = i + 1
                elif word in self.Negs:
                    negcount += 1
                    d = 0
                    for w in segtmp[a:i]:
                        if w in self.Extremes:
                            negcount *= 4.0
                        elif w in self.Verys:
                            negcount *= 3.0
                        elif w in self.Mores:
                            negcount *= 2.0
                        else:
                            if w in self.Ishs:
                                negcount *= 0.5

                    if self.judgeodd(d) == 'odd':
                        negcount *= -1.0
                        negcount2 += negcount
                        negcount = 0
                        negcount3 = negcount + negcount2 + negcount3
                        negcount2 = 0
                    else:
                        negcount3 = negcount + negcount2 + negcount3
                        negcount = 0
                    a = i + 1

            count2.append(count1)
            count1 = []

        pos_result = []
        neg_result = []
        for sentence in count2:
            score_array = np.array(sentence)
            pos = np.sum(score_array[:, 0])
            neg = np.sum(score_array[:, 1])
            pos_result.append(pos)
            neg_result.append(neg)

        pos_score = np.sum(np.array(pos_result))
        neg_score = np.sum(np.array(neg_result))
        score = {'sentences':len(count2),  'words':wordnum, 
         'pos':pos_score, 
         'neg':neg_score}
        return score