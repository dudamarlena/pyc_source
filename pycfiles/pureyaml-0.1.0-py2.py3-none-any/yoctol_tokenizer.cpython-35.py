# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/purewords/tokenizer/yoctol_tokenizer.py
# Compiled at: 2018-08-07 00:24:13
# Size of source mod 2**32: 1145 bytes
from .jieba_tokenizer import JiebaTokenizer
frequent_proper_nouns = [
 '有顆頭', '優拓', '優拓資訊', '機器學習', '人工智慧', '機器人',
 '客服', '推薦系統', '深度學習', '資料科學家', '資料科學',
 '自然語言處理']
common_proper_nouns = [
 '物連網', '溝通', '橋樑', '部落格', '粉專', '頁面']
frequent_eng_proper_nouns = [
 'Yoctol Info', 'YoctolInfo', 'yoctol', 'Yoctol',
 'aloha.ai', 'Aloha.AI',
 'machine learning', 'Machine Learning',
 'deep learning', 'Deep Learning',
 'Neural Network', 'Convolutional Neural Network', 'Deep Neural Network',
 'data scientist', 'Data Scientist', 'Natural Language Processing',
 'Computer Vision', 'Random Forest', 'Gradient Boosting']
proper_nouns = [
 '客群', '服務']

class YoctolTokenizer(JiebaTokenizer):

    def __init__(self):
        super(YoctolTokenizer, self).__init__()
        self.add_words(frequent_proper_nouns, None, 'nr')
        self.add_words(common_proper_nouns, None, 'nr')
        self.add_words(frequent_eng_proper_nouns, None, 'eng')
        self.add_words(proper_nouns, None, 'nr')