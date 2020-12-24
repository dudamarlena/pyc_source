# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/naiveBayesClassifier/ExceptionNotSeen.py
# Compiled at: 2014-05-12 12:44:20


class NotSeen(Exception):
    """
    Exception for tokens which are not indexed 
    because never seen in the trainin data
    """

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return ("Token '{}' is never seen in the training set.").format(self.value)