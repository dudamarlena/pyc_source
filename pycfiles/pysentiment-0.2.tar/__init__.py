# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/xuming06/Codes/sentiment-classifier-zh/pysenti/__init__.py
# Compiled at: 2019-09-22 00:59:35
__doc__ = '\n@author:XuMing（xuming624@qq.com)\n@description: \n'
from . import config
from .compat import strdecode
from .model_classifier import ModelClassifier
from .rule_classfier import RuleClassifier
__version__ = '0.1.4'
rule_classifier = RuleClassifier()
classify = rule_classifier.classify
model_classifier = ModelClassifier(config.sentiment_model_path)