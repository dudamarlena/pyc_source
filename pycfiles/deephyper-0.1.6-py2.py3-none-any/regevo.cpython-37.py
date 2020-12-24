# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/regevo.py
# Compiled at: 2019-09-05 10:20:47
# Size of source mod 2**32: 6220 bytes
import os, collections, numpy as np, json
from deephyper.search import util
from deephyper.search.nas import NeuralArchitectureSearch
from deephyper.core.parser import add_arguments_from_signature
import deephyper.core.logs.logging as jm
from deephyper.evaluator.evaluate import Encoder
dhlogger = util.conf_logger('deephyper.search.nas.regevo')

class RegularizedEvolution(NeuralArchitectureSearch):
    __doc__ = "Regularized evolution.\n\n    https://arxiv.org/abs/1802.01548\n\n    Args:\n        problem (str): Module path to the Problem instance you want to use for the search (e.g. deephyper.benchmark.nas.linearReg.Problem).\n        run (str): Module path to the run function you want to use for the search (e.g. deephyper.search.nas.model.run.quick).\n        evaluator (str): value in ['balsam', 'subprocess', 'processPool', 'threadPool'].\n        population_size (int, optional): the number of individuals to keep in the population. Defaults to 100.\n        sample_size (int, optional): the number of individuals that should participate in each tournament. Defaults to 10.\n    "

    def __init__(self, problem, run, evaluator, population_size=100, sample_size=10, **kwargs):
        if evaluator == 'balsam':
            balsam_launcher_nodes = int(os.environ.get('BALSAM_LAUNCHER_NODES', 1))
            deephyper_workers_per_node = int(os.environ.get('DEEPHYPER_WORKERS_PER_NODE', 1))
            n_free_nodes = balsam_launcher_nodes - 1
            self.free_workers = n_free_nodes * deephyper_workers_per_node
        else:
            self.free_workers = 1
        (super().__init__)(problem=problem, run=run, evaluator=evaluator, **kwargs)
        dhlogger.info(jm(type='start_infos',
          alg='aging-evolution',
          nworkers=(self.free_workers),
          encoded_space=json.dumps((self.problem.space), cls=Encoder)))
        self.pb_dict = self.problem.space
        cs_kwargs = self.pb_dict['create_search_space'].get('kwargs')
        if cs_kwargs is None:
            search_space = self.pb_dict['create_search_space']['func']()
        else:
            search_space = (self.pb_dict['create_search_space']['func'])(**cs_kwargs)
        self.space_list = [(0, vnode.num_ops - 1) for vnode in search_space.variable_nodes]
        self.population_size = population_size
        self.sample_size = sample_size

    @staticmethod
    def _extend_parser(parser):
        NeuralArchitectureSearch._extend_parser(parser)
        add_arguments_from_signature(parser, RegularizedEvolution)
        return parser

    def main(self):
        num_evals_done = 0
        population = collections.deque(maxlen=(self.population_size))
        self.evaluator.add_eval_batch(self.gen_random_batch(size=(self.free_workers)))
        while num_evals_done < self.max_evals:
            new_results = list(self.evaluator.get_finished_evals())
            if len(new_results) > 0:
                population.extend(new_results)
                stats = {'num_cache_used': self.evaluator.stats['num_cache_used']}
                dhlogger.info(jm(type='env_stats', **stats))
                self.evaluator.dump_evals(saved_key='arch_seq')
                num_received = len(new_results)
                num_evals_done += num_received
                if len(population) == self.population_size:
                    children_batch = []
                    for _ in range(len(new_results)):
                        indexes = np.random.choice((self.population_size), (self.sample_size), replace=False)
                        sample = [population[i] for i in indexes]
                        parent = self.select_parent(sample)
                        child = self.copy_mutate_arch(parent)
                        children_batch.append(child)

                    if len(new_results) > 0:
                        self.evaluator.add_eval_batch(children_batch)
                else:
                    self.evaluator.add_eval_batch(self.gen_random_batch(size=(len(new_results))))

    def select_parent(self, sample: list) -> list:
        cfg, _ = max(sample, key=(lambda x: x[1]))
        return cfg['arch_seq']

    def gen_random_batch(self, size: int) -> list:
        batch = []
        for _ in range(size):
            cfg = self.pb_dict.copy()
            cfg['arch_seq'] = self.random_search_space()
            batch.append(cfg)

        return batch

    def random_search_space(self) -> list:
        return [np.random.choice(b + 1) for _, b in self.space_list]

    def copy_mutate_arch(self, parent_arch: list) -> dict:
        """
        # ! Time performance is critical because called sequentialy

        Args:
            parent_arch (list(int)): [description]

        Returns:
            dict: [description]

        """
        i = np.random.choice(len(parent_arch))
        child_arch = parent_arch[:]
        range_upper_bound = self.space_list[i][1]
        elements = [j for j in range(range_upper_bound + 1) if j != child_arch[i]]
        sample = np.random.choice(elements, 1)[0]
        child_arch[i] = sample
        cfg = self.pb_dict.copy()
        cfg['arch_seq'] = child_arch
        return cfg


if __name__ == '__main__':
    args = RegularizedEvolution.parse_args()
    search = RegularizedEvolution(**vars(args))
    search.main()