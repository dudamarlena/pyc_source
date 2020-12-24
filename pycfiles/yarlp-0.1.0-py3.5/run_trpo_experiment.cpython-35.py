# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/yarlp/external/baselines/baselines/trpo_mpi/run_trpo_experiment.py
# Compiled at: 2018-04-01 14:21:44
# Size of source mod 2**32: 3133 bytes
import os, sys, time, json, subprocess
from functools import partial
from concurrent.futures import ProcessPoolExecutor
from baselines.bench.monitor import load_results
from baselines.bench.benchmarks import _BENCHMARKS
SEEDS = list(range(1, 100))

def train_mujoco(env_id, num_timesteps, seed, logdir):
    env = os.environ.copy()
    env['PATH'] = '/usr/sbin:/sbin:' + env['PATH']
    env['OPENAI_LOGDIR'] = logdir
    python_path = sys.executable
    command = '{} -m baselines.trpo_mpi.run_mujoco --env {} --seed {} --num-timesteps {}'.format(python_path, env_id, seed, num_timesteps)
    p = subprocess.Popen(command, env=env, shell=True)
    out, err = p.communicate()


def train_atari(env_id, num_timesteps, seed):
    pass


def train(base_log_path, benchmark_name, task):
    results = []
    for trial in range(task['trials']):
        trial_logdir = os.path.join(base_log_path, '{}_{}_{}'.format(benchmark_name, task['env_id'], trial))
        os.makedirs(trial_logdir)
        if benchmark_name.lower().startswith('mujoco'):
            train_mujoco(task['env_id'], num_timesteps=task['num_timesteps'], seed=SEEDS[trial], logdir=trial_logdir)
        else:
            train_atari(task['env_id'], num_timesteps=task['num_timesteps'], seed=SEEDS[trial], logdir=trial_logdir)
        res = load_results(trial_logdir)
        res['trial'] = trial
        res['seed'] = SEEDS[trial]
        results.append(res)

    return results


def main():
    import argparse
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--benchmark', help='benchmark name', default='Mujoco1M')
    parser.add_argument('--logdir', help='logging directory')
    args = parser.parse_args()
    logdir = args.logdir
    assert logdir is not None
    benchmark_name = args.benchmark
    benchmark_dict = dict(map(lambda x: (x[1]['name'], x[0]), enumerate(_BENCHMARKS)))
    assert benchmark_name in benchmark_dict
    benchmark_idx = benchmark_dict[benchmark_name]
    benchmark = _BENCHMARKS[benchmark_idx]
    path = time.strftime('{}_%d-%m-%y-%H-%M-%S_baseline'.format(benchmark_name))
    base_log_path = os.path.join(os.path.expanduser(logdir), path)
    os.makedirs(base_log_path)
    with ProcessPoolExecutor() as (ex):
        train_func = partial(train, base_log_path, benchmark_name)
        for res in ex.map(train_func, benchmark['tasks']):
            for r in res:
                print(r)


if __name__ == '__main__':
    main()