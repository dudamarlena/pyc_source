# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/baselines/her/experiment/config.py
# Compiled at: 2019-07-10 12:45:57
# Size of source mod 2**32: 7789 bytes
import os, numpy as np, gym
from deephyper.search.nas.baselines import logger
from deephyper.search.nas.baselines.her.ddpg import DDPG
from deephyper.search.nas.baselines.her.her_sampler import make_sample_her_transitions
from deephyper.search.nas.baselines.bench.monitor import Monitor
DEFAULT_ENV_PARAMS = {'FetchReach-v1': {'n_cycles': 10}}
DEFAULT_PARAMS = {'max_u':1.0, 
 'layers':3, 
 'hidden':256, 
 'network_class':'baselines.her.actor_critic:ActorCritic', 
 'Q_lr':0.001, 
 'pi_lr':0.001, 
 'buffer_size':int(1000000.0), 
 'polyak':0.95, 
 'action_l2':1.0, 
 'clip_obs':200.0, 
 'scope':'ddpg', 
 'relative_goals':False, 
 'n_cycles':50, 
 'rollout_batch_size':2, 
 'n_batches':40, 
 'batch_size':256, 
 'n_test_rollouts':10, 
 'test_with_polyak':False, 
 'random_eps':0.3, 
 'noise_eps':0.2, 
 'replay_strategy':'future', 
 'replay_k':4, 
 'norm_eps':0.01, 
 'norm_clip':5, 
 'bc_loss':0, 
 'q_filter':0, 
 'num_demo':100, 
 'demo_batch_size':128, 
 'prm_loss_weight':0.001, 
 'aux_loss_weight':0.0078}
CACHED_ENVS = {}

def cached_make_env(make_env):
    """
    Only creates a new environment from the provided function if one has not yet already been
    created. This is useful here because we need to infer certain properties of the env, e.g.
    its observation and action spaces, without any intend of actually using it.
    """
    if make_env not in CACHED_ENVS:
        env = make_env()
        CACHED_ENVS[make_env] = env
    return CACHED_ENVS[make_env]


def prepare_params(kwargs):
    ddpg_params = dict()
    env_name = kwargs['env_name']

    def make_env(subrank=None):
        env = gym.make(env_name)
        if subrank is not None:
            if logger.get_dir() is not None:
                try:
                    from mpi4py import MPI
                    mpi_rank = MPI.COMM_WORLD.Get_rank()
                except ImportError:
                    MPI = None
                    mpi_rank = 0
                    logger.warn('Running with a single MPI process. This should work, but the results may differ from the ones publshed in Plappert et al.')

                max_episode_steps = env._max_episode_steps
                env = Monitor(env, (os.path.join(logger.get_dir(), str(mpi_rank) + '.' + str(subrank))),
                  allow_early_resets=True)
                env = gym.wrappers.TimeLimit(env, max_episode_steps=max_episode_steps)
        return env

    kwargs['make_env'] = make_env
    tmp_env = cached_make_env(kwargs['make_env'])
    assert hasattr(tmp_env, '_max_episode_steps')
    kwargs['T'] = tmp_env._max_episode_steps
    kwargs['max_u'] = np.array(kwargs['max_u']) if isinstance(kwargs['max_u'], list) else kwargs['max_u']
    kwargs['gamma'] = 1.0 - 1.0 / kwargs['T']
    if 'lr' in kwargs:
        kwargs['pi_lr'] = kwargs['lr']
        kwargs['Q_lr'] = kwargs['lr']
        del kwargs['lr']
    for name in ('buffer_size', 'hidden', 'layers', 'network_class', 'polyak', 'batch_size',
                 'Q_lr', 'pi_lr', 'norm_eps', 'norm_clip', 'max_u', 'action_l2',
                 'clip_obs', 'scope', 'relative_goals'):
        ddpg_params[name] = kwargs[name]
        kwargs['_' + name] = kwargs[name]
        del kwargs[name]

    kwargs['ddpg_params'] = ddpg_params
    return kwargs


def log_params(params, logger=logger):
    for key in sorted(params.keys()):
        logger.info('{}: {}'.format(key, params[key]))


def configure_her(params):
    env = cached_make_env(params['make_env'])
    env.reset()

    def reward_fun(ag_2, g, info):
        return env.compute_reward(achieved_goal=ag_2, desired_goal=g, info=info)

    her_params = {'reward_fun': reward_fun}
    for name in ('replay_strategy', 'replay_k'):
        her_params[name] = params[name]
        params['_' + name] = her_params[name]
        del params[name]

    sample_her_transitions = make_sample_her_transitions(**her_params)
    return sample_her_transitions


def simple_goal_subtract(a, b):
    assert a.shape == b.shape
    return a - b


def configure_ddpg(dims, params, reuse=False, use_mpi=True, clip_return=True):
    sample_her_transitions = configure_her(params)
    gamma = params['gamma']
    rollout_batch_size = params['rollout_batch_size']
    ddpg_params = params['ddpg_params']
    input_dims = dims.copy()
    env = cached_make_env(params['make_env'])
    env.reset()
    ddpg_params.update({'input_dims':input_dims,  'T':params['T'], 
     'clip_pos_returns':True, 
     'clip_return':1.0 / (1.0 - gamma) if clip_return else np.inf, 
     'rollout_batch_size':rollout_batch_size, 
     'subtract_goals':simple_goal_subtract, 
     'sample_transitions':sample_her_transitions, 
     'gamma':gamma, 
     'bc_loss':params['bc_loss'], 
     'q_filter':params['q_filter'], 
     'num_demo':params['num_demo'], 
     'demo_batch_size':params['demo_batch_size'], 
     'prm_loss_weight':params['prm_loss_weight'], 
     'aux_loss_weight':params['aux_loss_weight']})
    ddpg_params['info'] = {'env_name': params['env_name']}
    policy = DDPG(reuse=reuse, **ddpg_params, **{'use_mpi': use_mpi})
    return policy


def configure_dims(params):
    env = cached_make_env(params['make_env'])
    env.reset()
    obs, _, _, info = env.step(env.action_space.sample())
    dims = {'o':obs['observation'].shape[0], 
     'u':env.action_space.shape[0], 
     'g':obs['desired_goal'].shape[0]}
    for key, value in info.items():
        value = np.array(value)
        if value.ndim == 0:
            value = value.reshape(1)
        dims['info_{}'.format(key)] = value.shape[0]

    return dims