# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/xuming06/Codes/sentiment-classifier-zh/pysenti/__init__.py
# Compiled at: 2019-09-22 00:59:35
"""
@author:XuMing（xuming624@qq.com)
@description: 
"""
from . import config
from .compat import strdecode
from .model_classifier import ModelClassifier
from .rule_classfier import RuleClassifier
__version__ = '0.1.4'
rule_classifier = RuleClassifier()
classify = rule_classifier.classify
model_classifier = ModelClassifier(config.sentiment_model_path)