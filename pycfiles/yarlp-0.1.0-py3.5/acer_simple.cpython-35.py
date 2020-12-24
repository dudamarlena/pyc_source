# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/yarlp/external/baselines/baselines/acer/acer_simple.py
# Compiled at: 2018-04-01 14:21:44
# Size of source mod 2**32: 16057 bytes
import time, joblib, numpy as np, tensorflow as tf
from baselines import logger
from baselines.common import set_global_seeds
from baselines.a2c.utils import batch_to_seq, seq_to_batch
from baselines.a2c.utils import Scheduler, make_path, find_trainable_variables
from baselines.a2c.utils import cat_entropy_softmax
from baselines.a2c.utils import EpisodeStats
from baselines.a2c.utils import get_by_index, check_shape, avg_norm, gradient_add, q_explained_variance
from baselines.acer.buffer import Buffer

def strip(var, nenvs, nsteps, flat=False):
    vars = batch_to_seq(var, nenvs, nsteps + 1, flat)
    return seq_to_batch(vars[:-1], flat)


def q_retrace(R, D, q_i, v, rho_i, nenvs, nsteps, gamma):
    """
    Calculates q_retrace targets

    :param R: Rewards
    :param D: Dones
    :param q_i: Q values for actions taken
    :param v: V values
    :param rho_i: Importance weight for each action
    :return: Q_retrace values
    """
    rho_bar = batch_to_seq(tf.minimum(1.0, rho_i), nenvs, nsteps, True)
    rs = batch_to_seq(R, nenvs, nsteps, True)
    ds = batch_to_seq(D, nenvs, nsteps, True)
    q_is = batch_to_seq(q_i, nenvs, nsteps, True)
    vs = batch_to_seq(v, nenvs, nsteps + 1, True)
    v_final = vs[(-1)]
    qret = v_final
    qrets = []
    for i in range(nsteps - 1, -1, -1):
        check_shape([qret, ds[i], rs[i], rho_bar[i], q_is[i], vs[i]], [[nenvs]] * 6)
        qret = rs[i] + gamma * qret * (1.0 - ds[i])
        qrets.append(qret)
        qret = rho_bar[i] * (qret - q_is[i]) + vs[i]

    qrets = qrets[::-1]
    qret = seq_to_batch(qrets, flat=True)
    return qret


class Model(object):

    def __init__(self, policy, ob_space, ac_space, nenvs, nsteps, nstack, num_procs, ent_coef, q_coef, gamma, max_grad_norm, lr, rprop_alpha, rprop_epsilon, total_timesteps, lrschedule, c, trust_region, alpha, delta):
        config = tf.ConfigProto(allow_soft_placement=True, intra_op_parallelism_threads=num_procs, inter_op_parallelism_threads=num_procs)
        sess = tf.Session(config=config)
        nact = ac_space.n
        nbatch = nenvs * nsteps
        A = tf.placeholder(tf.int32, [nbatch])
        D = tf.placeholder(tf.float32, [nbatch])
        R = tf.placeholder(tf.float32, [nbatch])
        MU = tf.placeholder(tf.float32, [nbatch, nact])
        LR = tf.placeholder(tf.float32, [])
        eps = 1e-06
        step_model = policy(sess, ob_space, ac_space, nenvs, 1, nstack, reuse=False)
        train_model = policy(sess, ob_space, ac_space, nenvs, nsteps + 1, nstack, reuse=True)
        params = find_trainable_variables('model')
        print('Params {}'.format(len(params)))
        for var in params:
            print(var)

        ema = tf.train.ExponentialMovingAverage(alpha)
        ema_apply_op = ema.apply(params)

        def custom_getter(getter, *args, **kwargs):
            v = ema.average(getter(*args, **kwargs))
            print(v.name)
            return v

        with tf.variable_scope('', custom_getter=custom_getter, reuse=True):
            polyak_model = policy(sess, ob_space, ac_space, nenvs, nsteps + 1, nstack, reuse=True)
        v = tf.reduce_sum(train_model.pi * train_model.q, axis=-1)
        f, f_pol, q = map(lambda var: strip(var, nenvs, nsteps), [train_model.pi, polyak_model.pi, train_model.q])
        f_i = get_by_index(f, A)
        q_i = get_by_index(q, A)
        rho = f / (MU + eps)
        rho_i = get_by_index(rho, A)
        qret = q_retrace(R, D, q_i, v, rho_i, nenvs, nsteps, gamma)
        entropy = tf.reduce_mean(cat_entropy_softmax(f))
        v = strip(v, nenvs, nsteps, True)
        check_shape([qret, v, rho_i, f_i], [[nenvs * nsteps]] * 4)
        check_shape([rho, f, q], [[nenvs * nsteps, nact]] * 2)
        adv = qret - v
        logf = tf.log(f_i + eps)
        gain_f = logf * tf.stop_gradient(adv * tf.minimum(c, rho_i))
        loss_f = -tf.reduce_mean(gain_f)
        adv_bc = q - tf.reshape(v, [nenvs * nsteps, 1])
        logf_bc = tf.log(f + eps)
        check_shape([adv_bc, logf_bc], [[nenvs * nsteps, nact]] * 2)
        gain_bc = tf.reduce_sum(logf_bc * tf.stop_gradient(adv_bc * tf.nn.relu(1.0 - c / (rho + eps)) * f), axis=1)
        loss_bc = -tf.reduce_mean(gain_bc)
        loss_policy = loss_f + loss_bc
        check_shape([qret, q_i], [[nenvs * nsteps]] * 2)
        ev = q_explained_variance(tf.reshape(q_i, [nenvs, nsteps]), tf.reshape(qret, [nenvs, nsteps]))
        loss_q = tf.reduce_mean(tf.square(tf.stop_gradient(qret) - q_i) * 0.5)
        check_shape([loss_policy, loss_q, entropy], [[]] * 3)
        loss = loss_policy + q_coef * loss_q - ent_coef * entropy
        if trust_region:
            g = tf.gradients(-(loss_policy - ent_coef * entropy) * nsteps * nenvs, f)
            k = -f_pol / (f + eps)
            k_dot_g = tf.reduce_sum(k * g, axis=-1)
            adj = tf.maximum(0.0, (tf.reduce_sum(k * g, axis=-1) - delta) / (tf.reduce_sum(tf.square(k), axis=-1) + eps))
            avg_norm_k = avg_norm(k)
            avg_norm_g = avg_norm(g)
            avg_norm_k_dot_g = tf.reduce_mean(tf.abs(k_dot_g))
            avg_norm_adj = tf.reduce_mean(tf.abs(adj))
            g = g - tf.reshape(adj, [nenvs * nsteps, 1]) * k
            grads_f = -g / (nenvs * nsteps)
            grads_policy = tf.gradients(f, params, grads_f)
            grads_q = tf.gradients(loss_q * q_coef, params)
            grads = [gradient_add(g1, g2, param) for g1, g2, param in zip(grads_policy, grads_q, params)]
            avg_norm_grads_f = avg_norm(grads_f) * (nsteps * nenvs)
            norm_grads_q = tf.global_norm(grads_q)
            norm_grads_policy = tf.global_norm(grads_policy)
        else:
            grads = tf.gradients(loss, params)
        if max_grad_norm is not None:
            grads, norm_grads = tf.clip_by_global_norm(grads, max_grad_norm)
        grads = list(zip(grads, params))
        trainer = tf.train.RMSPropOptimizer(learning_rate=LR, decay=rprop_alpha, epsilon=rprop_epsilon)
        _opt_op = trainer.apply_gradients(grads)
        with tf.control_dependencies([_opt_op]):
            _train = tf.group(ema_apply_op)
        lr = Scheduler(v=lr, nvalues=total_timesteps, schedule=lrschedule)
        run_ops = [
         _train, loss, loss_q, entropy, loss_policy, loss_f, loss_bc, ev, norm_grads]
        names_ops = ['loss', 'loss_q', 'entropy', 'loss_policy', 'loss_f', 'loss_bc', 'explained_variance',
         'norm_grads']
        if trust_region:
            run_ops = run_ops + [norm_grads_q, norm_grads_policy, avg_norm_grads_f, avg_norm_k, avg_norm_g, avg_norm_k_dot_g,
             avg_norm_adj]
            names_ops = names_ops + ['norm_grads_q', 'norm_grads_policy', 'avg_norm_grads_f', 'avg_norm_k', 'avg_norm_g',
             'avg_norm_k_dot_g', 'avg_norm_adj']

        def train(obs, actions, rewards, dones, mus, states, masks, steps):
            cur_lr = lr.value_steps(steps)
            td_map = {train_model.X: obs, polyak_model.X: obs, A: actions, R: rewards, D: dones, MU: mus, LR: cur_lr}
            if states != []:
                td_map[train_model.S] = states
                td_map[train_model.M] = masks
                td_map[polyak_model.S] = states
                td_map[polyak_model.M] = masks
            return (
             names_ops, sess.run(run_ops, td_map)[1:])

        def save(save_path):
            ps = sess.run(params)
            make_path(save_path)
            joblib.dump(ps, save_path)

        self.train = train
        self.save = save
        self.train_model = train_model
        self.step_model = step_model
        self.step = step_model.step
        self.initial_state = step_model.initial_state
        tf.global_variables_initializer().run(session=sess)


class Runner(object):

    def __init__(self, env, model, nsteps, nstack):
        self.env = env
        self.nstack = nstack
        self.model = model
        nh, nw, nc = env.observation_space.shape
        self.nc = nc
        self.nenv = nenv = env.num_envs
        self.nact = env.action_space.n
        self.nbatch = nenv * nsteps
        self.batch_ob_shape = (nenv * (nsteps + 1), nh, nw, nc * nstack)
        self.obs = np.zeros((nenv, nh, nw, nc * nstack), dtype=np.uint8)
        obs = env.reset()
        self.update_obs(obs)
        self.nsteps = nsteps
        self.states = model.initial_state
        self.dones = [False for _ in range(nenv)]

    def update_obs(self, obs, dones=None):
        if dones is not None:
            self.obs *= (1 - dones.astype(np.uint8))[:, None, None, None]
        self.obs = np.roll(self.obs, shift=-self.nc, axis=3)
        self.obs[:, :, :, -self.nc:] = obs[:, :, :, :]

    def run(self):
        enc_obs = np.split(self.obs, self.nstack, axis=3)
        mb_obs, mb_actions, mb_mus, mb_dones, mb_rewards = ([], [], [], [], [])
        for _ in range(self.nsteps):
            actions, mus, states = self.model.step(self.obs, state=self.states, mask=self.dones)
            mb_obs.append(np.copy(self.obs))
            mb_actions.append(actions)
            mb_mus.append(mus)
            mb_dones.append(self.dones)
            obs, rewards, dones, _ = self.env.step(actions)
            self.states = states
            self.dones = dones
            self.update_obs(obs, dones)
            mb_rewards.append(rewards)
            enc_obs.append(obs)

        mb_obs.append(np.copy(self.obs))
        mb_dones.append(self.dones)
        enc_obs = np.asarray(enc_obs, dtype=np.uint8).swapaxes(1, 0)
        mb_obs = np.asarray(mb_obs, dtype=np.uint8).swapaxes(1, 0)
        mb_actions = np.asarray(mb_actions, dtype=np.int32).swapaxes(1, 0)
        mb_rewards = np.asarray(mb_rewards, dtype=np.float32).swapaxes(1, 0)
        mb_mus = np.asarray(mb_mus, dtype=np.float32).swapaxes(1, 0)
        mb_dones = np.asarray(mb_dones, dtype=np.bool).swapaxes(1, 0)
        mb_masks = mb_dones
        mb_dones = mb_dones[:, 1:]
        return (
         enc_obs, mb_obs, mb_actions, mb_rewards, mb_mus, mb_dones, mb_masks)


class Acer:

    def __init__(self, runner, model, buffer, log_interval):
        self.runner = runner
        self.model = model
        self.buffer = buffer
        self.log_interval = log_interval
        self.tstart = None
        self.episode_stats = EpisodeStats(runner.nsteps, runner.nenv)
        self.steps = None

    def call(self, on_policy):
        runner, model, buffer, steps = (
         self.runner, self.model, self.buffer, self.steps)
        if on_policy:
            enc_obs, obs, actions, rewards, mus, dones, masks = runner.run()
            self.episode_stats.feed(rewards, dones)
            if buffer is not None:
                buffer.put(enc_obs, actions, rewards, mus, dones, masks)
        else:
            obs, actions, rewards, mus, dones, masks = buffer.get()
        obs = obs.reshape(runner.batch_ob_shape)
        actions = actions.reshape([runner.nbatch])
        rewards = rewards.reshape([runner.nbatch])
        mus = mus.reshape([runner.nbatch, runner.nact])
        dones = dones.reshape([runner.nbatch])
        masks = masks.reshape([runner.batch_ob_shape[0]])
        names_ops, values_ops = model.train(obs, actions, rewards, dones, mus, model.initial_state, masks, steps)
        if on_policy and int(steps / runner.nbatch) % self.log_interval == 0:
            logger.record_tabular('total_timesteps', steps)
            logger.record_tabular('fps', int(steps / (time.time() - self.tstart)))
            logger.record_tabular('mean_episode_length', self.episode_stats.mean_length())
            logger.record_tabular('mean_episode_reward', self.episode_stats.mean_reward())
            for name, val in zip(names_ops, values_ops):
                logger.record_tabular(name, float(val))

            logger.dump_tabular()


def learn(policy, env, seed, nsteps=20, nstack=4, total_timesteps=int(80000000.0), q_coef=0.5, ent_coef=0.01, max_grad_norm=10, lr=0.0007, lrschedule='linear', rprop_epsilon=1e-05, rprop_alpha=0.99, gamma=0.99, log_interval=100, buffer_size=50000, replay_ratio=4, replay_start=10000, c=10.0, trust_region=True, alpha=0.99, delta=1):
    print('Running Acer Simple')
    print(locals())
    tf.reset_default_graph()
    set_global_seeds(seed)
    nenvs = env.num_envs
    ob_space = env.observation_space
    ac_space = env.action_space
    num_procs = len(env.remotes)
    model = Model(policy=policy, ob_space=ob_space, ac_space=ac_space, nenvs=nenvs, nsteps=nsteps, nstack=nstack, num_procs=num_procs, ent_coef=ent_coef, q_coef=q_coef, gamma=gamma, max_grad_norm=max_grad_norm, lr=lr, rprop_alpha=rprop_alpha, rprop_epsilon=rprop_epsilon, total_timesteps=total_timesteps, lrschedule=lrschedule, c=c, trust_region=trust_region, alpha=alpha, delta=delta)
    runner = Runner(env=env, model=model, nsteps=nsteps, nstack=nstack)
    if replay_ratio > 0:
        buffer = Buffer(env=env, nsteps=nsteps, nstack=nstack, size=buffer_size)
    else:
        buffer = None
    nbatch = nenvs * nsteps
    acer = Acer(runner, model, buffer, log_interval)
    acer.tstart = time.time()
    for acer.steps in range(0, total_timesteps, nbatch):
        acer.call(on_policy=True)
        if replay_ratio > 0 and buffer.has_atleast(replay_start):
            n = np.random.poisson(replay_ratio)
            for _ in range(n):
                acer.call(on_policy=False)

    env.close()