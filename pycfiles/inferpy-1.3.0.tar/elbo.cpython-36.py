# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rcabanas/GoogleDrive/UAL/inferpy/repo/InferPy/inferpy/inference/variational/loss_functions/elbo.py
# Compiled at: 2019-09-03 11:37:11
# Size of source mod 2**32: 1224 bytes
import tensorflow as tf

def ELBO(pvars, qvars, batch_weight=1, **kwargs):
    """ Compute the loss tensor from the expanded variables of p and q models.
        Args:
            pvars (`dict<inferpy.RandomVariable>`): The dict with the expanded p random variables
            qvars (`dict<inferpy.RandomVariable>`): The dict with the expanded q random variables
            batch_weight (`float`): Weight to assign less importance to the energy, used when processing data in batches

        Returns (`tf.Tensor`):
            The generated loss tensor
    """
    energy = tf.reduce_sum([(batch_weight if p.is_datamodel else 1) * tf.reduce_sum(p.log_prob(p.value)) for p in pvars.values()])
    q_mask = tf.stack([tf.math.logical_not(q.is_observed) for q in qvars.values()], name='q_mask')
    entropy = -tf.reduce_sum(tf.boolean_mask(tf.stack([(batch_weight if q.is_datamodel else 1) * tf.reduce_sum(q.log_prob(q.value)) for q in qvars.values()]), q_mask))
    ELBO = energy + entropy
    return -ELBO