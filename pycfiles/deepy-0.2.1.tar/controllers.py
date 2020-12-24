# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/shu/research/deepy/deepy/trainers/controllers.py
# Compiled at: 2016-04-20 00:05:45


class TrainingController(object):
    """
    Abstract class of training controllers.
    """

    def __init__(self, trainer):
        """
        :type trainer: deepy.trainers.base.NeuralTrainer
        """
        self._trainer = trainer

    def invoke(self):
        """
        Return True to exit training.
        """
        return False