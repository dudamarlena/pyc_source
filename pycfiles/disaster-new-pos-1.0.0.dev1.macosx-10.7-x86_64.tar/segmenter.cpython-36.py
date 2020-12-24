# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bai/anaconda3/lib/python3.6/site-packages/segmenter.py
# Compiled at: 2018-03-25 21:13:09
# Size of source mod 2**32: 1778 bytes
import sys, os, CRFPP
pkg_path = os.path.dirname(os.path.abspath(__file__))
DEFAULT_MODEL = str(os.path.join(pkg_path, 'segment/data/crf_model2014'))

class Tokenizer(object):

    def __init__(self, model_path=DEFAULT_MODEL):
        self.model = CRFPP.Tagger('-m ' + model_path)

    def seg(self, text):
        """
        text: String, text to be segmented;
        crf_model: path of pretrained CRFPP crf_model,
        """
        segList = []
        model = self.model
        model.clear()
        for char in text.strip():
            char = char.strip()
            if char:
                model.add(char + '\to\tB')

        model.parse()
        size = model.size()
        xsize = model.xsize()
        word = ''
        for i in range(0, size):
            for j in range(0, xsize):
                char = model.x(i, j)
                tag = model.y2(i)
                if tag == 'B':
                    word = char
                elif tag == 'M':
                    word += char
                elif tag == 'E':
                    word += char
                    segList.append(word)
                    word = ''
                else:
                    word = char
                    segList.append(word)
                    word = ''

        return segList


tk = Tokenizer(DEFAULT_MODEL)
seg = tk.seg