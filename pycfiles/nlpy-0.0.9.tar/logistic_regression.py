# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hadoop/nlpy/nlpy/classification/logistic_regression.py
# Compiled at: 2014-11-14 00:53:21
import numpy as np, theano.tensor as T, theano, time, sys, os, logging
logging = logging.getLogger(__name__)

class LogisticRegression(object):

    def __init__(self, input_n=0, output_n=0, batch_size=1000, learning_rate=0.13, improvement_threshold=0.995, max_epochs=1000, x=None, y=None):
        self._x = (x or T.matrix)('x') if 1 else x
        self._y = (y or T.ivector)('y') if 1 else y
        self.input_n = input_n
        self.output_n = output_n
        self._init_weights()
        self.batch_size = batch_size
        self.learning_rate = learning_rate
        self.improvement_threshold = improvement_threshold
        self.max_epochs = max_epochs

    def _init_weights(self):
        self._W = theano.shared(name='W', value=np.zeros((self.input_n, self.output_n), dtype=theano.config.floatX), borrow=True)
        self._B = theano.shared(name='B', value=np.zeros(self.output_n, dtype=theano.config.floatX), borrow=True)
        self._p_y_given_x = T.nnet.softmax(T.dot(self._x, self._W) + self._B)
        self._y_pred = T.argmax(self._p_y_given_x, axis=1)

    def _negative_log_likelihood(self):
        return -T.mean(T.log(self._p_y_given_x)[(T.arange(self._y.shape[0]), self._y)])

    def _errors(self):
        return T.mean(T.neq(self._y_pred, self._y))

    def _shared_dataset(self, data_xy, borrow=True):
        data_x, data_y = data_xy
        shared_x = theano.shared(np.asarray(data_x, dtype=theano.config.floatX), borrow=borrow)
        shared_y = theano.shared(np.asarray(data_y, dtype=theano.config.floatX), borrow=borrow)
        return (shared_x, T.cast(shared_y, 'int32'))

    def train(self, dataset):
        """
        Train the model
        :param data: dataset
        :type dataset: nlpy.dataset.AbstractDataset
        :param ys: target values
        """
        train_set = dataset.train_set()
        train_xs, train_ys = self._shared_dataset(train_set)
        valid_set = dataset.valid_set()
        valid_xs, valid_ys = self._shared_dataset(valid_set)
        test_set = dataset.test_set()
        test_set_given = bool(test_set)
        if test_set_given:
            test_xs, test_ys = self._shared_dataset(test_set)
        else:
            test_xs, test_ys = self._shared_dataset(valid_set)
        self.input_n = len(train_set[0][0])
        self.output_n = max(train_set[1]) + 1
        self._init_weights()
        n_train_batches = train_xs.get_value(borrow=True).shape[0] / self.batch_size
        n_valid_batches = valid_xs.get_value(borrow=True).shape[0] / self.batch_size
        n_test_batches = test_xs.get_value(borrow=True).shape[0] / self.batch_size
        index = T.lscalar()
        cost = self._negative_log_likelihood()
        validate_model = theano.function(inputs=[
         index], outputs=self._errors(), givens={self._x: valid_xs[index * self.batch_size:(index + 1) * self.batch_size], 
           self._y: valid_ys[index * self.batch_size:(index + 1) * self.batch_size]})
        g_W = T.grad(cost=cost, wrt=self._W)
        g_b = T.grad(cost=cost, wrt=self._B)
        updates = [
         (
          self._W, self._W - self.learning_rate * g_W),
         (
          self._B, self._B - self.learning_rate * g_b)]
        train_model = theano.function(inputs=[
         index], outputs=cost, updates=updates, givens={self._x: train_xs[index * self.batch_size:(index + 1) * self.batch_size], 
           self._y: train_ys[index * self.batch_size:(index + 1) * self.batch_size]})
        test_model = theano.function(inputs=[
         index], outputs=self._errors(), givens={self._x: test_xs[index * self.batch_size:(index + 1) * self.batch_size], 
           self._y: test_ys[index * self.batch_size:(index + 1) * self.batch_size]})
        patience = 5000
        patience_increase = 2
        validation_frequency = min(n_train_batches, patience / 2)
        best_validation_loss = np.inf
        test_score = 0.0
        start_time = time.clock()
        done_looping = False
        epoch = 0
        while epoch < self.max_epochs and not done_looping:
            epoch = epoch + 1
            for minibatch_index in xrange(n_train_batches):
                minibatch_avg_cost = train_model(minibatch_index)
                iter = (epoch - 1) * n_train_batches + minibatch_index
                if (iter + 1) % validation_frequency == 0:
                    validation_losses = [ validate_model(i) for i in xrange(n_valid_batches)
                                        ]
                    this_validation_loss = np.mean(validation_losses)
                    logging.info('epoch %i, minibatch %i/%i, validation error %f %%', epoch, minibatch_index + 1, n_train_batches, this_validation_loss * 100.0)
                    if this_validation_loss < best_validation_loss:
                        if this_validation_loss < best_validation_loss * self.improvement_threshold:
                            patience = max(patience, iter * patience_increase)
                        best_validation_loss = this_validation_loss
                        if test_set_given:
                            test_losses = [ test_model(i) for i in xrange(n_test_batches) ]
                            test_score = np.mean(test_losses)
                        logging.info('     epoch %i, minibatch %i/%i, test error of best model %f %%', epoch, minibatch_index + 1, n_train_batches, test_score * 100.0)
                if patience <= iter:
                    done_looping = True
                    break

        end_time = time.clock()
        logging.info('Optimization complete with best validation score of %f %%,with test performance %f %%', best_validation_loss * 100.0, test_score * 100.0)
        if end_time > start_time:
            logging.info('The code run for %d epochs, with %f epochs/sec', epoch, 1.0 * epoch / (end_time - start_time))
        logging.info('The code for file ' + os.path.split(__file__)[1] + ' ran for %.1fs' % (end_time - start_time))

    def predict(self, data):
        pass