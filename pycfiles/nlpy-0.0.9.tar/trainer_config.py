# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hadoop/nlpy/nlpy/deep/conf/trainer_config.py
# Compiled at: 2015-01-21 01:51:09


class TrainerConfig(object):

    def __init__(self):
        self.validation_frequency = 10
        self.test_frequency = 50
        self.monitor_frequency = 50
        self.min_improvement = 0.0
        self.patience = 20
        self.momentum = 0.9
        self.learning_rate = 0.0001
        self.update_l1 = 0
        self.update_l2 = 0
        self.weight_l1 = 0
        self.weight_l2 = 0
        self.hidden_l1 = 0
        self.hidden_l2 = 0
        self.contractive_l2 = 0