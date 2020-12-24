# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/autolabel/classifier.py
# Compiled at: 2020-04-02 05:27:35
# Size of source mod 2**32: 238 bytes


class Classifier:
    NAME = None

    def __init__(self):
        self._model = None

    def predict(self, images, decode, top):
        raise NotImplementedError

    def decode(self, preds, top=3):
        raise NotImplementedError