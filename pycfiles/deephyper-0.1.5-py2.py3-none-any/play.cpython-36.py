# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/baselines/her/experiment/play.py
# Compiled at: 2019-07-10 12:45:57
# Size of source mod 2**32: 1875 bytes
import click, numpy as np, pickle
from deephyper.search.nas.baselines import logger
from deephyper.search.nas.baselines.common import set_global_seeds
import deephyper.search.nas.baselines.her.experiment.config as config
from deephyper.search.nas.baselines.her.rollout import RolloutWorker

@click.command()
@click.argument('policy_file', type=str)
@click.option('--seed', type=int, default=0)
@click.option('--n_test_rollouts', type=int, default=10)
@click.option('--render', type=int, default=1)
def main(policy_file, seed, n_test_rollouts, render):
    set_global_seeds(seed)
    with open(policy_file, 'rb') as (f):
        policy = pickle.load(f)
    env_name = policy.info['env_name']
    params = config.DEFAULT_PARAMS
    if env_name in config.DEFAULT_ENV_PARAMS:
        params.update(config.DEFAULT_ENV_PARAMS[env_name])
    params['env_name'] = env_name
    params = config.prepare_params(params)
    config.log_params(params, logger=logger)
    dims = config.configure_dims(params)
    eval_params = {'exploit':True, 
     'use_target_net':params['test_with_polyak'], 
     'compute_Q':True, 
     'rollout_batch_size':1, 
     'render':bool(render)}
    for name in ('T', 'gamma', 'noise_eps', 'random_eps'):
        eval_params[name] = params[name]

    evaluator = RolloutWorker(
     (params['make_env']), policy, dims, logger, **eval_params)
    evaluator.seed(seed)
    evaluator.clear_history()
    for _ in range(n_test_rollouts):
        evaluator.generate_rollouts()

    for key, val in evaluator.logs('test'):
        logger.record_tabular(key, np.mean(val))

    logger.dump_tabular()


if __name__ == '__main__':
    main()