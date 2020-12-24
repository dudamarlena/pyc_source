# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/shu/research/deepy/deepy/utils/fake_generator.py
# Compiled at: 2016-04-20 00:05:45


class FakeGenerator(object):

    def __init__(self, dataset, method_name):
        self.dataset = dataset
        self.method_name = method_name

    def __iter__(self):
        return getattr(self.dataset, self.method_name)()