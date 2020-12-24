# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/arf_tools/src/classifiers/classifier.py
# Compiled at: 2018-03-22 17:13:21
# Size of source mod 2**32: 467 bytes


class Classifier(object):
    __doc__ = " Classe generique d'un classifieur.\n    Dispose de 3 méthodes :\n        - `fit`, pour apprendre.\n        - `predict` pour predire.\n        - `score` pour évaluer la precision.\n    "

    def fit(self, data, y):
        raise NotImplementedError()

    def predict(self, data):
        raise NotImplementedError()

    def score(self, data, y):
        return (self.predict(data) == y).mean()


if __name__ == '__main__':
    pass