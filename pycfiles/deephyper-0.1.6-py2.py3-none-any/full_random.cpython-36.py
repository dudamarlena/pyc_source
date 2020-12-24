# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/full_random.py
# Compiled at: 2019-07-10 12:45:57
# Size of source mod 2**32: 3710 bytes
import os
from random import random
from deephyper.search import Search
try:
    from mpi4py import MPI
except ImportError:
    MPI = None

class Random(Search):
    __doc__ = "Search class to run a full random neural architecture search. The search is filling every available nodes as soon as they are detected. The master job is using only 1 MPI rank.\n\n    Args:\n        problem (str): Module path to the Problem instance you want to use for the search (e.g. deephyper.benchmark.nas.linearReg.Problem).\n        run (str): Module path to the run function you want to use for the search (e.g. deephyper.search.nas.model.run.quick).\n        evaluator (str): value in ['balsam', 'subprocess', 'processPool', 'threadPool'].\n    "

    def __init__(self, problem, run, evaluator, **kwargs):
        if MPI is None:
            self.free_workers = 1
        else:
            nranks = MPI.COMM_WORLD.Get_size()
            if evaluator == 'balsam':
                balsam_launcher_nodes = int(os.environ.get('BALSAM_LAUNCHER_NODES', 1))
                deephyper_workers_per_node = int(os.environ.get('DEEPHYPER_WORKERS_PER_NODE', 1))
                n_free_nodes = balsam_launcher_nodes - nranks
                self.free_workers = n_free_nodes * deephyper_workers_per_node
            else:
                self.free_workers = 1
        (super().__init__)(problem, run, evaluator, **kwargs)

    @staticmethod
    def _extend_parser(parser):
        parser.add_argument('--problem', default='deephyper.benchmark.nas.linearReg.Problem',
          help='Module path to the Problem instance you want to use for the search (e.g. deephyper.benchmark.nas.linearReg.Problem).')
        parser.add_argument('--run', default='deephyper.search.nas.model.run.quick',
          help='Module path to the run function you want to use for the search (e.g. deephyper.search.nas.model.run.quick).')
        parser.add_argument('--max-evals', type=int, default=10000000000.0, help='maximum number of evaluations.')
        return parser

    def main(self):
        space = self.problem.space
        cs_kwargs = space['create_structure'].get('kwargs')
        if cs_kwargs is None:
            structure = space['create_structure']['func']()
        else:
            structure = (space['create_structure']['func'])(**cs_kwargs)
        len_arch = structure.max_num_ops

        def gen_arch():
            return [random() for _ in range(len_arch)]

        num_evals_done = 0
        available_workers = self.free_workers

        def gen_batch(size):
            batch = []
            for _ in range(size):
                cfg = space.copy()
                cfg['arch_seq'] = gen_arch()
                batch.append(cfg)

            return batch

        self.evaluator.add_eval_batch(gen_batch(size=available_workers))
        while num_evals_done < self.args.max_evals:
            results = self.evaluator.get_finished_evals()
            num_received = num_evals_done
            for _ in results:
                num_evals_done += 1

            num_received = num_evals_done - num_received
            if num_received > 0:
                self.evaluator.add_eval_batch(gen_batch(size=num_received))


if __name__ == '__main__':
    args = Random.parse_args()
    search = Random(**vars(args))
    search.main()