# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/yarlp/external/baselines/baselines/acktr/acktr_cont.py
# Compiled at: 2018-04-01 14:21:44
# Size of source mod 2**32: 5446 bytes
import numpy as np, tensorflow as tf
from baselines import logger
import baselines.common as common
from baselines.common import tf_util as U
from baselines.acktr import kfac
from baselines.common.filters import ZFilter

def pathlength(path):
    return path['reward'].shape[0]


def rollout(env, policy, max_pathlength, animate=False, obfilter=None):
    """
    Simulate the env and policy for max_pathlength steps
    """
    ob = env.reset()
    prev_ob = np.float32(np.zeros(ob.shape))
    if obfilter:
        ob = obfilter(ob)
    terminated = False
    obs = []
    acs = []
    ac_dists = []
    logps = []
    rewards = []
    for _ in range(max_pathlength):
        if animate:
            env.render()
        state = np.concatenate([ob, prev_ob], -1)
        obs.append(state)
        ac, ac_dist, logp = policy.act(state)
        acs.append(ac)
        ac_dists.append(ac_dist)
        logps.append(logp)
        prev_ob = np.copy(ob)
        scaled_ac = env.action_space.low + (ac + 1.0) * 0.5 * (env.action_space.high - env.action_space.low)
        scaled_ac = np.clip(scaled_ac, env.action_space.low, env.action_space.high)
        ob, rew, done, _ = env.step(scaled_ac)
        if obfilter:
            ob = obfilter(ob)
        rewards.append(rew)
        if done:
            terminated = True
            break

    return {'observation': np.array(obs), 'terminated': terminated, 
     'reward': np.array(rewards), 'action': np.array(acs), 
     'action_dist': np.array(ac_dists), 'logp': np.array(logps)}


def learn(env, policy, vf, gamma, lam, timesteps_per_batch, num_timesteps, animate=False, callback=None, desired_kl=0.002):
    obfilter = ZFilter(env.observation_space.shape)
    max_pathlength = env.spec.timestep_limit
    stepsize = tf.Variable(initial_value=np.float32(np.array(0.03)), name='stepsize')
    inputs, loss, loss_sampled = policy.update_info
    optim = kfac.KfacOptimizer(learning_rate=stepsize, cold_lr=stepsize * 0.09999999999999998, momentum=0.9, kfac_update=2, epsilon=0.01, stats_decay=0.99, async=1, cold_iter=1, weight_decay_dict=policy.wd_dict, max_grad_norm=None)
    pi_var_list = []
    for var in tf.trainable_variables():
        if 'pi' in var.name:
            pi_var_list.append(var)

    update_op, q_runner = optim.minimize(loss, loss_sampled, var_list=pi_var_list)
    do_update = U.function(inputs, update_op)
    U.initialize()
    enqueue_threads = []
    coord = tf.train.Coordinator()
    for qr in [q_runner, vf.q_runner]:
        assert qr != None
        enqueue_threads.extend(qr.create_threads(tf.get_default_session(), coord=coord, start=True))

    i = 0
    timesteps_so_far = 0
    while True:
        if timesteps_so_far > num_timesteps:
            break
        logger.log('********** Iteration %i ************' % i)
        timesteps_this_batch = 0
        paths = []
        while 1:
            path = rollout(env, policy, max_pathlength, animate=len(paths) == 0 and i % 10 == 0 and animate, obfilter=obfilter)
            paths.append(path)
            n = pathlength(path)
            timesteps_this_batch += n
            timesteps_so_far += n
            if timesteps_this_batch > timesteps_per_batch:
                break

        vtargs = []
        advs = []
        for path in paths:
            rew_t = path['reward']
            return_t = common.discount(rew_t, gamma)
            vtargs.append(return_t)
            vpred_t = vf.predict(path)
            vpred_t = np.append(vpred_t, 0.0 if path['terminated'] else vpred_t[(-1)])
            delta_t = rew_t + gamma * vpred_t[1:] - vpred_t[:-1]
            adv_t = common.discount(delta_t, gamma * lam)
            advs.append(adv_t)

        vf.fit(paths, vtargs)
        ob_no = np.concatenate([path['observation'] for path in paths])
        action_na = np.concatenate([path['action'] for path in paths])
        oldac_dist = np.concatenate([path['action_dist'] for path in paths])
        adv_n = np.concatenate(advs)
        standardized_adv_n = (adv_n - adv_n.mean()) / (adv_n.std() + 1e-08)
        do_update(ob_no, action_na, standardized_adv_n)
        min_stepsize = np.float32(1e-08)
        max_stepsize = np.float32(1.0)
        kl = policy.compute_kl(ob_no, oldac_dist)
        if kl > desired_kl * 2:
            logger.log('kl too high')
            tf.assign(stepsize, tf.maximum(min_stepsize, stepsize / 1.5)).eval()
        else:
            if kl < desired_kl / 2:
                logger.log('kl too low')
                tf.assign(stepsize, tf.minimum(max_stepsize, stepsize * 1.5)).eval()
            else:
                logger.log('kl just right!')
            logger.record_tabular('EpRewMean', np.mean([path['reward'].sum() for path in paths]))
            logger.record_tabular('EpRewSEM', np.std([path['reward'].sum() / np.sqrt(len(paths)) for path in paths]))
            logger.record_tabular('EpLenMean', np.mean([pathlength(path) for path in paths]))
            logger.record_tabular('KL', kl)
            if callback:
                callback()
        logger.dump_tabular()
        i += 1

    coord.request_stop()
    coord.join(enqueue_threads)