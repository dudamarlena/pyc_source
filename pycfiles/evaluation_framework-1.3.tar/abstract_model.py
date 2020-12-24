# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/marpel/Scrivania/github/Evaluation-Framework/evaluation_framework/abstract_model.py
# Compiled at: 2020-01-21 09:44:15
from abc import abstractmethod

class AbstractModel:

    def __init__(self):
        super().__init__()

    @abstractmethod
    def train(self):
        pass