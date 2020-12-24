# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/naiveBayesClassifier/trainer.py
# Compiled at: 2014-05-12 11:29:33
from naiveBayesClassifier.trainedData import TrainedData

class Trainer(object):
    """docstring for Trainer"""

    def __init__(self, tokenizer):
        super(Trainer, self).__init__()
        self.tokenizer = tokenizer
        self.data = TrainedData()

    def train(self, text, className):
        """
        enhances trained data using the given text and class
        """
        self.data.increaseClass(className)
        tokens = self.tokenizer.tokenize(text)
        for token in tokens:
            self.data.increaseToken(token, className)