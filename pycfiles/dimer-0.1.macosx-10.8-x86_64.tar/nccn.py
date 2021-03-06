# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/dimer/nnet/nccn.py
# Compiled at: 2013-08-13 02:30:56
"""convolutional neural nets"""
import logging, numpy as np, theano.tensor as T
from theano.tensor.signal import downsample
from theano.tensor.nnet import sigmoid, softmax, conv
from . import Model, SpeedLayer
log = logging.getLogger(__name__)

class LogisticReg(SpeedLayer):
    """A logistic regression layer"""

    def __init__(self, X, n_in, n_out, rng, dtype):
        """A logistic regression layer

        the layer has a weight and a bias matrix as weights and parameters.
        """
        super(LogisticReg, self).__init__([(n_in, n_out), (n_out,)], [
         'llW', 'llb'], [rng, 0.0], [dtype, dtype])
        self.input = X
        self.p_y_given_x = self.activation()
        self.y_hat = T.argmax(self.p_y_given_x, axis=1)

    def activation(self):
        """softmax activation. XW + b (samples are rows)"""
        W, b = self.get_params()
        return softmax(T.dot(self.input, W) + b)

    def __str__(self):
        return '[(LOG_REG) %dx%d]' % self.get_weights()[0].shape


class HiddenLayer(SpeedLayer):
    """Hidden layer of a feed-forward net """

    def __init__(self, X, n_in, n_out, rng, dtype):
        super(HiddenLayer, self).__init__([(n_in, n_out), (n_out,)], [
         'hlW', 'hlb'], [0.0, 0.0], [dtype, dtype])
        if type(rng) == np.random.RandomState:
            thr = np.sqrt(6.0 / (n_in + n_out))
            self._weights_[0].set_value(np.asarray(rng.uniform(low=-thr, high=thr, size=(
             n_in, n_out)), dtype=dtype))
        self.input = X

    def activation(self):
        """softmax activation. XW + b (X is a row)"""
        W, b = self.get_params()
        return sigmoid(T.dot(self.input, W) + b)

    def __str__(self):
        return '[(HIDDEN) %dx%d]' % self.get_weights()[0].shape


class ConvPoolLayer(SpeedLayer):
    """LeNet  conv-pool layer"""

    def __init__(self, X, fshape, ishape, rng, poolsize, dtype):
        """Le Cun convolutional layer

        fshape: (# filters, # in_feature_maps, width, height)
        ishape: (batch_size, # feature_maps, width, height)
        """
        assert fshape[1] == ishape[1], 'nr. of feature maps should not change'
        super(ConvPoolLayer, self).__init__([fshape, (fshape[0],)], [
         'cpW', 'cpb'], [rng, 0.0], [dtype, dtype])
        if type(rng) == np.random.RandomState:
            thr = np.sqrt(3.0 / np.prod(fshape[1:]))
            self._weights_[0].set_value(np.asarray(rng.uniform(low=-thr, high=thr, size=fshape), dtype=dtype))
        self.input = X
        self.ishape = ishape
        self.fshape = fshape
        self.pshape = poolsize

    def activation(self):
        """activation function"""
        W, b = self.get_params()
        conved = conv.conv2d(self.input, W, filter_shape=self.fshape, image_shape=self.ishape)
        pooled = downsample.max_pool_2d(conved, self.pshape, ignore_border=True)
        return sigmoid(pooled + b.dimshuffle('x', 0, 'x', 'x'))

    def __str__(self):
        """in_fature_maps -> nr_of_kern (receprive_field_size (wXh) / pool_size(wXh)) -> """
        nk, ifm, fw, fh = self.fshape
        pw, ph = self.pshape
        weights = '[(CONV_POOL) %d -> @%d (%dx%d) / %dx%d]' % (ifm, nk, fw, fh, pw, ph)
        state = '[%d/batch  @%d (%dx%d) -> @%d (%dx%d)]' % (self.ishape + (self.fshape[0],
         (self.ishape[2] - self.fshape[2] + 1) / self.pshape[0],
         (self.ishape[3] - self.fshape[3] + 1) / self.pshape[1]))
        return weights + '  ' + state


class CnnModel(Model):

    def __init__(self, arch, lreg_size, inshape, nout, rng, xdtype, ydtype):
        self.X = T.dtensor4('X')
        self.Y = {'int32': T.ivector('Y'), 'int64': T.lvector('Y')}[ydtype]
        in_bs, in_fm, in_w, in_h = inshape
        layers = []
        this_input = self.X.reshape(inshape)
        img_sh = inshape
        for nkern, rf, ps in zip(*arch):
            layers.append(ConvPoolLayer(this_input, (
             nkern, img_sh[1], rf[0], rf[1]), img_sh, rng, ps, xdtype))
            this_input = layers[(-1)].activation()
            img_sh = (in_bs, nkern, (img_sh[2] - rf[0] + 1) / ps[0],
             (img_sh[3] - rf[1] + 1) / ps[1])

        layers.append(HiddenLayer(this_input.flatten(2), nkern * img_sh[2] * img_sh[3], lreg_size, rng, xdtype))
        layers.append(LogisticReg(layers[(-1)].activation(), lreg_size, nout, rng, xdtype))
        Model.__init__(self, layers)

    @property
    def top_cp_idx(self):
        return len(self) - 3

    def get_speeds(self):
        """
        @return: map(lambda l: l.get_speeds(), self)
        """
        return map(lambda l: l.get_speeds(), self)

    def set_speeds(self, vlst):
        for w, i in enumerate(vlst):
            self[i].set_speeds(w)

    def cost(self, l1, l2):
        """regularized cross entropy

        @param l1: L1 coefficient (float)
        @param l2: L2 coefficient (float)
        @return: cost function"""
        l1_term = l1 * self.weight_norm('l1')
        l2_term = l2 * self.weight_norm('l2')
        error = T.log(self[(-1)].p_y_given_x)[(T.arange(self.Y.shape[0]), self.Y)]
        return -T.mean(error) + l1_term + l2_term

    def update_params(self, train_batches, gradient_f, momentum, lrate):
        """step on the direction of gradient

        step on the direction of gradient
        for a whole epoch and update the model params in place.
        By definition speed is initialized to 0.
        new_speed = -rho * dE/dw + mu * speed
        new_weight = w + new_speed

        @param train_batches: indexes of batches (list)
        @param gradient_f: function that returns the list of gradients
                           from the batch index.
        @param momentum: mu
        @param lrate: rho
        @return: none
        """
        for batch_i in train_batches:
            all_grads = gradient_f(batch_i)
            for layer in self:
                l_grads = map(lambda i: all_grads.pop(0), range(len(layer.get_params())))
                layer.speed_update(l_grads, momentum, lrate)
                layer.weight_update()