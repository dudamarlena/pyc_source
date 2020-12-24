# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/shu/research/deepy/deepy/trainers/delayed_trainers.py
# Compiled at: 2016-04-20 00:05:45
import logging as loggers, numpy as np, theano, theano.tensor as T
from theano.ifelse import ifelse
from deepy.utils import FLOATX
from deepy.trainers.base import NeuralTrainer
logging = loggers.getLogger(__name__)
THEANO_LINKER = 'cvm'

class DelayedBatchSGDTrainer(NeuralTrainer):
    """
    DEPRECATED
    Delayed batch SGD trainer.
    Update parameters after N iterations.
    """

    def __init__(self, network, config=None, batch_size=20):
        """
        Create a SGD trainer.
        :type network:
        :type config: deepy.conf.TrainerConfig
        :return:
        """
        super(DelayedBatchSGDTrainer, self).__init__(network, config)
        self.learning_rate = self.config.learning_rate
        self.batch_size = batch_size
        logging.info('compiling %s learning function', self.__class__.__name__)
        network_updates = list(network.updates) + list(network._learning_updates)
        learning_updates = list(self.learning_updates())
        update_list = network_updates + learning_updates
        logging.info('network updates: %s' % (' ').join(map(str, [ x[0] for x in network_updates ])))
        logging.info('learning updates: %s' % (' ').join(map(str, [ x[0] for x in learning_updates ])))
        self.learning_func = theano.function(network.inputs, self.training_variables, updates=update_list, allow_input_downcast=True, mode=theano.Mode(linker=THEANO_LINKER))

    def learning_updates(self):
        batch_counter = theano.shared(np.array(0, dtype='int32'), 'batch_counter')
        batch_size = self.batch_size
        to_update = batch_counter >= batch_size
        for param in self.network.parameters:
            gsum = theano.shared(np.zeros(param.get_value().shape, dtype=FLOATX), 'batch_gsum_%s' % param.name)
            yield (gsum, ifelse(to_update, T.zeros_like(gsum), gsum + T.grad(self.cost, param)))
            delta = self.learning_rate * gsum / batch_size
            yield (param, ifelse(to_update, param - delta, param))

        yield (batch_counter, ifelse(to_update, T.constant(0, dtype='int32'), batch_counter + 1))