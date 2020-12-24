# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/ambs.py
# Compiled at: 2019-09-05 10:20:47
# Size of source mod 2**32: 5829 bytes
import json, os, signal
import deephyper.core.logs.logging as jm
from deephyper.evaluator.evaluate import Encoder
from deephyper.search import util
from deephyper.search.nas import NeuralArchitectureSearch
from deephyper.search.nas.optimizer import Optimizer
dhlogger = util.conf_logger('deephyper.search.nas.ambs')
SERVICE_PERIOD = 2
CHECKPOINT_INTERVAL = 1
EXIT_FLAG = False

def on_exit(signum, stack):
    global EXIT_FLAG
    EXIT_FLAG = True


class AMBNeuralArchitectureSearch(NeuralArchitectureSearch):
    __doc__ = 'Asynchronous Model-Based Search.\n\n    Args:\n        problem (str): python attribute import of the ``NaProblem`` instance (e.g. ``mypackage.mymodule.myproblem``).\n        run (str): python attribute import of the run function (e.g. ``mypackage.mymodule.myrunfunction``).\n        evaluator (str): the name of the evaluator to use.\n        learner (str, optional): Choices are ["RF", "ET", "GBRT", "DUMMY", "GP"]. ``RF`` is Random Forest, ``ET`` is Extra Trees, ``GBRT`` is Gradient Boosting Regression Trees, ``DUMMY`` is random, ``GP`` is Gaussian process. Defaults to "RF".\n        liar_strategy (str, optional): ["cl_max", "cl_min", "cl_mean"]. Defaults to "cl_max".\n        acq_func (str, optional): Acquisition function, choices are ["gp_hedge", "LCB", "EI", "PI"]. Defaults to "gp_hedge".\n        n_jobs (int, optional): Number of parallel jobs to distribute the learner. Defaults to -1, means as many as the number of logical cores.\n    '

    def __init__(self, problem, run, evaluator, learner='RF', liar_strategy='cl_max', acq_func='gp_hedge', n_jobs=-1, **kwargs):
        (super().__init__)(problem=problem, run=run, evaluator=evaluator, **kwargs)
        if evaluator == 'balsam':
            balsam_launcher_nodes = int(os.environ.get('BALSAM_LAUNCHER_NODES', 1))
            deephyper_workers_per_node = int(os.environ.get('DEEPHYPER_WORKERS_PER_NODE', 1))
            n_free_nodes = balsam_launcher_nodes - 1
            self.free_workers = n_free_nodes * deephyper_workers_per_node
        else:
            self.free_workers = 1
        dhlogger.info(jm(type='start_infos',
          alg='ambs-nas',
          nworkers=(self.free_workers),
          encoded_space=json.dumps((self.problem.space), cls=Encoder)))
        dhlogger.info('Initializing AMBS')
        self.optimizer = Optimizer(self.problem, self.num_workers, learner=learner, liar_strategy=liar_strategy, acq_func=acq_func, n_jobs=n_jobs, **kwargs)

    @staticmethod
    def _extend_parser(parser):
        NeuralArchitectureSearch._extend_parser(parser)
        parser.add_argument('--learner', default='RF',
          choices=[
         'RF', 'ET', 'GBRT', 'DUMMY', 'GP'],
          help='type of learner (surrogate model)')
        parser.add_argument('--liar-strategy', default='cl_max',
          choices=[
         'cl_min', 'cl_mean', 'cl_max'],
          help='Constant liar strategy')
        parser.add_argument('--acq-func', default='gp_hedge',
          choices=[
         'LCB', 'EI', 'PI', 'gp_hedge'],
          help='Acquisition function type')
        parser.add_argument('--n-jobs', default=(-1),
          type=int,
          help='Number of processes to use for learner.')
        return parser

    def main(self):
        timer = util.DelayTimer(max_minutes=None, period=SERVICE_PERIOD)
        chkpoint_counter = 0
        num_evals = 0
        dhlogger.info(f"Generating {self.num_workers} initial points...")
        XX = self.optimizer.ask_initial(n_points=(self.num_workers))
        self.evaluator.add_eval_batch(XX)
        for elapsed_str in timer:
            dhlogger.info(f"Elapsed time: {elapsed_str}")
            results = list(self.evaluator.get_finished_evals())
            num_evals += len(results)
            chkpoint_counter += len(results)
            if not EXIT_FLAG:
                if num_evals >= self.max_evals:
                    break
                if results:
                    dhlogger.info(f"Refitting model with batch of {len(results)} evals")
                    self.optimizer.tell(results)
                    dhlogger.info(f"Drawing {len(results)} points with strategy {self.optimizer.strategy}")
                    for batch in self.optimizer.ask(n_points=(len(results))):
                        self.evaluator.add_eval_batch(batch)

                if chkpoint_counter >= CHECKPOINT_INTERVAL:
                    self.evaluator.dump_evals(saved_key='arch_seq')
                    chkpoint_counter = 0

        dhlogger.info('Hyperopt driver finishing')
        self.evaluator.dump_evals(saved_key='arch_seq')


if __name__ == '__main__':
    args = AMBNeuralArchitectureSearch.parse_args()
    search = AMBNeuralArchitectureSearch(**vars(args))
    signal.signal(signal.SIGINT, on_exit)
    signal.signal(signal.SIGTERM, on_exit)
    search.main()