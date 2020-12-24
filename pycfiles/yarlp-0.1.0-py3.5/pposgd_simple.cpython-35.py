# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/yarlp/external/baselines/baselines/ppo1/pposgd_simple.py
# Compiled at: 2018-04-01 14:21:44
# Size of source mod 2**32: 9489 bytes
from baselines.common import Dataset, explained_variance, fmt_row, zipsame
from baselines import logger
import baselines.common.tf_util as U, tensorflow as tf, numpy as np, time
from baselines.common.mpi_adam import MpiAdam
from baselines.common.mpi_moments import mpi_moments
from mpi4py import MPI
from collections import deque

def traj_segment_generator(pi, env, horizon, stochastic):
    t = 0
    ac = env.action_space.sample()
    new = True
    ob = env.reset()
    cur_ep_ret = 0
    cur_ep_len = 0
    ep_rets = []
    ep_lens = []
    obs = np.array([ob for _ in range(horizon)])
    rews = np.zeros(horizon, 'float32')
    vpreds = np.zeros(horizon, 'float32')
    news = np.zeros(horizon, 'int32')
    acs = np.array([ac for _ in range(horizon)])
    prevacs = acs.copy()
    while True:
        prevac = ac
        ac, vpred = pi.act(stochastic, ob)
        if t > 0 and t % horizon == 0:
            yield {'ob': obs, 'rew': rews, 'vpred': vpreds, 'new': news, 
             'ac': acs, 'prevac': prevacs, 'nextvpred': vpred * (1 - new), 
             'ep_rets': ep_rets, 'ep_lens': ep_lens}
            ep_rets = []
            ep_lens = []
        i = t % horizon
        obs[i] = ob
        vpreds[i] = vpred
        news[i] = new
        acs[i] = ac
        prevacs[i] = prevac
        ob, rew, new, _ = env.step(ac)
        rews[i] = rew
        cur_ep_ret += rew
        cur_ep_len += 1
        if new:
            ep_rets.append(cur_ep_ret)
            ep_lens.append(cur_ep_len)
            cur_ep_ret = 0
            cur_ep_len = 0
            ob = env.reset()
        t += 1


def add_vtarg_and_adv(seg, gamma, lam):
    """
    Compute target value using TD(lambda) estimator, and advantage with GAE(lambda)
    """
    new = np.append(seg['new'], 0)
    vpred = np.append(seg['vpred'], seg['nextvpred'])
    T = len(seg['rew'])
    seg['adv'] = gaelam = np.empty(T, 'float32')
    rew = seg['rew']
    lastgaelam = 0
    for t in reversed(range(T)):
        nonterminal = 1 - new[(t + 1)]
        delta = rew[t] + gamma * vpred[(t + 1)] * nonterminal - vpred[t]
        gaelam[t] = lastgaelam = delta + gamma * lam * nonterminal * lastgaelam

    seg['tdlamret'] = seg['adv'] + seg['vpred']


def learn(env, policy_fn, *, timesteps_per_actorbatch, clip_param, entcoeff, optim_epochs, optim_stepsize, optim_batchsize, gamma, lam, max_timesteps=0, max_episodes=0, max_iters=0, max_seconds=0, callback=None, adam_epsilon=1e-05, schedule='constant'):
    ob_space = env.observation_space
    ac_space = env.action_space
    pi = policy_fn('pi', ob_space, ac_space)
    oldpi = policy_fn('oldpi', ob_space, ac_space)
    atarg = tf.placeholder(dtype=tf.float32, shape=[None])
    ret = tf.placeholder(dtype=tf.float32, shape=[None])
    lrmult = tf.placeholder(name='lrmult', dtype=tf.float32, shape=[])
    clip_param = clip_param * lrmult
    ob = U.get_placeholder_cached(name='ob')
    ac = pi.pdtype.sample_placeholder([None])
    kloldnew = oldpi.pd.kl(pi.pd)
    ent = pi.pd.entropy()
    meankl = tf.reduce_mean(kloldnew)
    meanent = tf.reduce_mean(ent)
    pol_entpen = -entcoeff * meanent
    ratio = tf.exp(pi.pd.logp(ac) - oldpi.pd.logp(ac))
    surr1 = ratio * atarg
    surr2 = tf.clip_by_value(ratio, 1.0 - clip_param, 1.0 + clip_param) * atarg
    pol_surr = -tf.reduce_mean(tf.minimum(surr1, surr2))
    vf_loss = tf.reduce_mean(tf.square(pi.vpred - ret))
    total_loss = pol_surr + pol_entpen + vf_loss
    losses = [pol_surr, pol_entpen, vf_loss, meankl, meanent]
    loss_names = ['pol_surr', 'pol_entpen', 'vf_loss', 'kl', 'ent']
    var_list = pi.get_trainable_variables()
    lossandgrad = U.function([ob, ac, atarg, ret, lrmult], losses + [U.flatgrad(total_loss, var_list)])
    adam = MpiAdam(var_list, epsilon=adam_epsilon)
    assign_old_eq_new = U.function([], [], updates=[tf.assign(oldv, newv) for oldv, newv in zipsame(oldpi.get_variables(), pi.get_variables())])
    compute_losses = U.function([ob, ac, atarg, ret, lrmult], losses)
    U.initialize()
    adam.sync()
    seg_gen = traj_segment_generator(pi, env, timesteps_per_actorbatch, stochastic=True)
    episodes_so_far = 0
    timesteps_so_far = 0
    iters_so_far = 0
    tstart = time.time()
    lenbuffer = deque(maxlen=100)
    rewbuffer = deque(maxlen=100)
    assert sum([max_iters > 0, max_timesteps > 0, max_episodes > 0, max_seconds > 0]) == 1, 'Only one time constraint permitted'
    while 1:
        if callback:
            callback(locals(), globals())
        if max_timesteps and timesteps_so_far >= max_timesteps:
            break
        else:
            if max_episodes and episodes_so_far >= max_episodes:
                break
            else:
                if max_iters and iters_so_far >= max_iters:
                    break
                else:
                    if max_seconds and time.time() - tstart >= max_seconds:
                        break
                    if schedule == 'constant':
                        cur_lrmult = 1.0
                    else:
                        if schedule == 'linear':
                            cur_lrmult = max(1.0 - float(timesteps_so_far) / max_timesteps, 0)
                        else:
                            raise NotImplementedError
            logger.log('********** Iteration %i ************' % iters_so_far)
            seg = seg_gen.__next__()
            add_vtarg_and_adv(seg, gamma, lam)
            ob, ac, atarg, tdlamret = (
             seg['ob'], seg['ac'], seg['adv'], seg['tdlamret'])
            vpredbefore = seg['vpred']
            atarg = (atarg - atarg.mean()) / atarg.std()
            d = Dataset(dict(ob=ob, ac=ac, atarg=atarg, vtarg=tdlamret), shuffle=not pi.recurrent)
            optim_batchsize = optim_batchsize or ob.shape[0]
            if hasattr(pi, 'ob_rms'):
                pi.ob_rms.update(ob)
        assign_old_eq_new()
        logger.log('Optimizing...')
        logger.log(fmt_row(13, loss_names))
        for _ in range(optim_epochs):
            losses = []
            for batch in d.iterate_once(optim_batchsize):
                *newlosses, g = lossandgrad(batch['ob'], batch['ac'], batch['atarg'], batch['vtarg'], cur_lrmult)
                adam.update(g, optim_stepsize * cur_lrmult)
                losses.append(newlosses)

            logger.log(fmt_row(13, np.mean(losses, axis=0)))

        logger.log('Evaluating losses...')
        losses = []
        for batch in d.iterate_once(optim_batchsize):
            newlosses = compute_losses(batch['ob'], batch['ac'], batch['atarg'], batch['vtarg'], cur_lrmult)
            losses.append(newlosses)

        meanlosses, _, _ = mpi_moments(losses, axis=0)
        logger.log(fmt_row(13, meanlosses))
        for lossval, name in zipsame(meanlosses, loss_names):
            logger.record_tabular('loss_' + name, lossval)

        logger.record_tabular('ev_tdlam_before', explained_variance(vpredbefore, tdlamret))
        lrlocal = (seg['ep_lens'], seg['ep_rets'])
        listoflrpairs = MPI.COMM_WORLD.allgather(lrlocal)
        lens, rews = map(flatten_lists, zip(*listoflrpairs))
        lenbuffer.extend(lens)
        rewbuffer.extend(rews)
        logger.record_tabular('EpLenMean', np.mean(lenbuffer))
        logger.record_tabular('EpRewMean', np.mean(rewbuffer))
        logger.record_tabular('EpThisIter', len(lens))
        episodes_so_far += len(lens)
        timesteps_so_far += sum(lens)
        iters_so_far += 1
        logger.record_tabular('EpisodesSoFar', episodes_so_far)
        logger.record_tabular('TimestepsSoFar', timesteps_so_far)
        logger.record_tabular('TimeElapsed', time.time() - tstart)
        if MPI.COMM_WORLD.Get_rank() == 0:
            logger.dump_tabular()


def flatten_lists(listoflists):
    return [el for list_ in listoflists for el in list_]