# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/xuming06/Codes/parrots/parrots/pinyin2hanzi.py
# Compiled at: 2018-09-13 07:36:55
"""
@author: nl8590687
语音识别的语言模型

基于马尔可夫模型的语言模型
"""
import os
from parrots import config
from parrots.utils.io_util import get_logger
default_logger = get_logger(__file__)
pwd_path = os.path.abspath(os.path.dirname(__file__))
get_abs_path = lambda path: os.path.normpath(os.path.join(pwd_path, path))

class Pinyin2Hanzi(object):

    def __init__(self, model_dir=config.pinyin2hanzi_dir):
        model_dir = get_abs_path(model_dir)
        self.dict_pinyin = self.get_symbol_dict(os.path.join(model_dir, 'pinyin_hanzi_dict.txt'))
        self.model1 = self.get_model_file(os.path.join(model_dir, 'char_idx.txt'))
        self.model2 = self.get_model_file(os.path.join(model_dir, 'word_idx.txt'))
        self.pinyin = self.get_pinyin(os.path.join(model_dir, 'dic_pinyin.txt'))
        self.model = (self.dict_pinyin, self.model1, self.model2)

    def pinyin_2_hanzi(self, list_syllable):
        u"""
        语音拼音 => 文本
        :param list_syllable:
        :return:
        """
        r = ''
        length = len(list_syllable)
        if not length:
            return ''
        str_tmp = [
         list_syllable[0]]
        for i in range(0, length - 1):
            str_split = list_syllable[i] + ' ' + list_syllable[(i + 1)]
            if str_split in self.pinyin:
                str_tmp.append(list_syllable[(i + 1)])
            else:
                str_decode = self.decode(str_tmp, 0.0)
                if str_decode != []:
                    r += str_decode[0][0]
                str_tmp = [list_syllable[(i + 1)]]

        str_decode = self.decode(str_tmp, 0.0)
        if str_decode:
            r += str_decode[0][0]
        return r

    def decode(self, list_syllable, yuzhi=0.0001):
        u"""
        实现拼音向文本的转换
        基于马尔可夫链
        """
        list_words = []
        num_pinyin = len(list_syllable)
        for i in range(num_pinyin):
            ls = ''
            if list_syllable[i] in self.dict_pinyin:
                ls = self.dict_pinyin[list_syllable[i]]
            else:
                break
            if i == 0:
                num_ls = len(ls)
                for j in range(num_ls):
                    tuple_word = [
                     '', 0.0]
                    tuple_word = [
                     ls[j], 1.0]
                    list_words.append(tuple_word)

                continue
            else:
                list_words_2 = []
                num_ls_word = len(list_words)
                for j in range(0, num_ls_word):
                    num_ls = len(ls)
                    for k in range(0, num_ls):
                        tuple_word = [
                         '', 0.0]
                        tuple_word = list(list_words[j])
                        tuple_word[0] = tuple_word[0] + ls[k]
                        tmp_words = tuple_word[0][-2:]
                        if tmp_words in self.model2:
                            tuple_word[1] = tuple_word[1] * float(self.model2[tmp_words]) / float(self.model1[tmp_words[(-2)]])
                        else:
                            tuple_word[1] = 0.0
                            continue
                        if tuple_word[1] >= pow(yuzhi, i):
                            list_words_2.append(tuple_word)

                list_words = list_words_2

        for i in range(0, len(list_words)):
            for j in range(i + 1, len(list_words)):
                if list_words[i][1] < list_words[j][1]:
                    tmp = list_words[i]
                    list_words[i] = list_words[j]
                    list_words[j] = tmp

        return list_words

    def get_symbol_dict(self, file_path):
        u"""
        读取拼音汉字的字典文件
        :param file_path:
        :return: 读取后的字典
        """
        txt_obj = open(file_path, 'r', encoding='UTF-8')
        txt_text = txt_obj.read()
        txt_obj.close()
        txt_lines = txt_text.split('\n')
        dic_symbol = {}
        for i in txt_lines:
            list_symbol = []
            if i:
                txt_l = i.split('\t')
                pinyin = txt_l[0]
                for word in txt_l[1]:
                    list_symbol.append(word)

            dic_symbol[pinyin] = list_symbol

        default_logger.debug('Loaded: %s, size: %d' % (file_path, len(dic_symbol)))
        return dic_symbol

    def get_model_file(self, model_path):
        u"""
        读取语言模型的文件
        :param model_path:
        :return: 读取后的模型
        """
        txt_obj = open(model_path, 'r', encoding='UTF-8')
        txt_text = txt_obj.read()
        txt_obj.close()
        txt_lines = txt_text.split('\n')
        dic_model = {}
        for i in txt_lines:
            if i:
                txt_l = i.split('\t')
                if len(txt_l) == 1:
                    continue
                dic_model[txt_l[0]] = txt_l[1]

        default_logger.debug('Loaded: %s, size: %d' % (model_path, len(dic_model)))
        return dic_model

    def get_pinyin(self, filename):
        file_obj = open(filename, 'r', encoding='UTF-8')
        txt_all = file_obj.read()
        file_obj.close()
        txt_lines = txt_all.split('\n')
        dic = {}
        for line in txt_lines:
            if not line:
                continue
            pinyin_split = line.split('\t')
            list_pinyin = pinyin_split[0]
            if list_pinyin not in dic and int(pinyin_split[1]) > 1:
                dic[list_pinyin] = pinyin_split[1]

        default_logger.debug('Loaded: %s, size: %d' % (filename, len(dic)))
        return dic