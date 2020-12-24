# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fynance/dev/set_neuralnetwork_tools.py
# Compiled at: 2019-02-12 11:42:02
# Size of source mod 2**32: 4877 bytes
from keras.models import Model
from keras.layers import Input, Dense, Dropout
from keras.optimizers import Adam
from keras import regularizers, initializers, constraints
__all__ = [
 'incr_seed', 'set_layer', 'set_nn_model']

def incr_seed(SEED, incr=1):
    """ Increment seed """
    if SEED is None:
        return
    return SEED + incr


def set_layer(nn, n_neurons, layer=Dense, dropout=None, SEED_dropout=None, **kwargs):
    """ Set `Dense` layers 
    
    Parameters
    ----------
    :nn: keras.Model
        An initilized neural network (cf `Input` keras documation).
    :n_neurons: int
        Number of neurons to set in this layer.
    :layer: keras.layer
        Kind of layers to use.
    :dropout: float
        At each iteration an part of variables is dropout. cf keras doc.
    :SEED: int
        A number to set the random weights.
    :kwargs: any parameters of `Dense` 
        cf keras documentation.
        
    Returns
    -------
    :nn: keras.Model
        Neural network with one more layer.
    
    """
    if dropout is None:
        return layer(n_neurons, **kwargs)(nn)
    nn = layer(n_neurons, **kwargs)(nn)
    return Dropout(dropout, seed=SEED_dropout)(nn)


def set_nn_model(X, neurons_list=[], layer=Dense, SEED=None, SEED_dropout=None, l1=0.01, l2=0.01, dropout=None, lr=0.01, b_1=0.99, b_2=0.999, decay=0.0, name=None, loss='mse', metrics=['accuracy'], l1_bias=0.01, l2_bias=0.01, l1_acti=0.01, l2_acti=0.01, m=0.0, std=1.0, **kwargs):
    """ Set a very basic neural network with `Dense` layers.
    
    Parameters
    ----------
    :X: np.ndarray[ndim=2, dtype=np.float32]
        Matrix of features of shape (T, N) with T is the number of 
        observations and N the number of features.
    :neurons_list: list of int
        Each number correspond at the number of neurons in corrsponding layers.
    :layer: keras.layer
        Kind of layers to use.
    :dropout: float
        At each iteration an part of variables is dropout. cf keras doc.
    :SEED: int
        A number to set the random weights.
    For other parameters cf Keras documentation.
    
    Returns
    -------
    :model: Keras.model
         A Neural Network ready to be train !
    
    """
    T, N = X.shape
    KERN_REG = regularizers.l1_l2(l1=l1, l2=l2)
    BIAS_REG = regularizers.l1_l2(l1=l1_bias, l2=l2_bias)
    ACTIV_REG = regularizers.l1_l2(l1=l1_acti, l2=l2_acti)
    KERN_CONS = constraints.MinMaxNorm(min_value=(-2.0),
      max_value=2.0,
      rate=1.0,
      axis=0)
    BIAS_CONS = constraints.MinMaxNorm(min_value=(-2.0),
      max_value=2.0,
      rate=1.0,
      axis=0)
    inputs = Input(shape=(N,), sparse=False)
    kern_init = initializers.RandomNormal(mean=m, stddev=std, seed=SEED)
    SEED = incr_seed(SEED, incr=1)
    nn = set_layer(
 inputs, neurons_list[0], dropout=dropout, kernel_regularizer=KERN_REG, SEED_dropout=SEED_dropout, 
     bias_regularizer=BIAS_REG, activity_regularizer=ACTIV_REG, 
     kernel_initializer=kern_init, kernel_constraint=KERN_CONS, 
     bias_constraint=BIAS_CONS, **kwargs)
    SEED_dropout = incr_seed(SEED_dropout, incr=1)
    for n_neurons in neurons_list[1:]:
        kern_init = initializers.RandomNormal(mean=m, stddev=std, seed=SEED)
        SEED = incr_seed(SEED, incr=1)
        nn = set_layer(
 nn, n_neurons, layer=layer, dropout=dropout, SEED_dropout=SEED_dropout, 
         kernel_regularizer=KERN_REG, kernel_initializer=kern_init, 
         bias_regularizer=BIAS_REG, activity_regularizer=ACTIV_REG, 
         kernel_constraint=KERN_CONS, bias_constraint=BIAS_CONS, **kwargs)
        SEED_dropout = incr_seed(SEED_dropout, incr=1)

    kern_init = initializers.RandomNormal(mean=m, stddev=std, seed=SEED)
    SEED = incr_seed(SEED, incr=1)
    outputs = set_layer(
 nn, 1, dropout=dropout, SEED_dropout=SEED_dropout, kernel_regularizer=KERN_REG, 
     bias_regularizer=BIAS_REG, activity_regularizer=ACTIV_REG, 
     kernel_initializer=kern_init, kernel_constraint=KERN_CONS, 
     bias_constraint=BIAS_CONS, **kwargs)
    SEED_dropout = incr_seed(SEED_dropout, incr=1)
    model = Model(inputs=inputs, outputs=outputs)
    model.name = name
    model.compile(optimizer=Adam(lr=lr,
      beta_1=b_1,
      beta_2=b_2,
      decay=decay,
      amsgrad=True),
      loss=loss,
      metrics=metrics)
    return model