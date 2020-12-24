# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/ambs.py
# Compiled at: 2019-07-11 14:24:06
# Size of source mod 2**32: 4950 bytes
import signal, json
from deephyper.search.nas.optimizer import Optimizer
from deephyper.search import Search
from deephyper.search import util
logger = util.conf_logger('deephyper.search.nas.ambs')
SERVICE_PERIOD = 2
CHECKPOINT_INTERVAL = 1
EXIT_FLAG = False

def on_exit(signum, stack):
    global EXIT_FLAG
    EXIT_FLAG = True


def key(d):
    return json.dumps(dict(arch_seq=(d['arch_seq'])))


class AMBNeuralArchitectureSearch(Search):
    __doc__ = 'Asynchronous Model-Based Search.\n\n    Arguments of AMBS:\n\n    * ``learner``\n\n        * ``RF`` : Random Forest (default)\n        * ``ET`` : Extra Trees\n        * ``GBRT`` : Gradient Boosting Regression Trees\n        * ``DUMMY`` :\n        * ``GP`` : Gaussian process\n\n    * ``liar-strategy``\n\n        * ``cl_max`` : (default)\n        * ``cl_min`` :\n        * ``cl_mean`` :\n\n    * ``acq-func`` : Acquisition function\n\n        * ``LCB`` :\n        * ``EI`` :\n        * ``PI`` :\n        * ``gp_hedge`` : (default)\n    '

    def __init__(self, problem, run, evaluator, cache_key=key, **kwargs):
        (super().__init__)(problem, run, evaluator, **kwargs)
        logger.info('Initializing AMBS')
        self.optimizer = Optimizer(self.problem, self.num_workers, self.args)

    @staticmethod
    def _extend_parser(parser):
        parser.add_argument('--problem', type=str,
          default='deephyper.benchmark.nas.linearReg.Problem',
          help='Module path to the Problem instance you want to use for the search (e.g. deephyper.benchmark.nas.linearReg.Problem).')
        parser.add_argument('--run', type=str,
          default='deephyper.search.nas.model.run.alpha.run',
          help='Module path to the run function you want to use for the search (e.g. deephyper.search.nas.model.run.alpha.run).')
        parser.add_argument('--max-evals', type=int,
          default=10000000000.0,
          help='maximum number of evaluations.')
        parser.add_argument('--learner', default='RF',
          choices=[
         'RF', 'ET', 'GBRT', 'DUMMY', 'GP'],
          help='type of learner (surrogate model)')
        parser.add_argument('--liar-strategy', default='cl_min',
          choices=[
         'cl_min', 'cl_mean', 'cl_max'],
          help='Constant liar strategy')
        parser.add_argument('--acq-func', default='gp_hedge',
          choices=[
         'LCB', 'EI', 'PI', 'gp_hedge'],
          help='Acquisition function type')
        return parser

    def main(self):
        timer = util.DelayTimer(max_minutes=None, period=SERVICE_PERIOD)
        chkpoint_counter = 0
        num_evals = 0
        logger.info(f"Generating {self.num_workers} initial points...")
        XX = self.optimizer.ask_initial(n_points=(self.num_workers))
        self.evaluator.add_eval_batch(XX)
        for elapsed_str in timer:
            logger.info(f"Elapsed time: {elapsed_str}")
            results = list(self.evaluator.get_finished_evals())
            num_evals += len(results)
            chkpoint_counter += len(results)
            if EXIT_FLAG or num_evals >= self.args.max_evals:
                break
            if results:
                logger.info(f"Refitting model with batch of {len(results)} evals")
                self.optimizer.tell(results)
                logger.info(f"Drawing {len(results)} points with strategy {self.optimizer.strategy}")
                for batch in self.optimizer.ask(n_points=(len(results))):
                    self.evaluator.add_eval_batch(batch)

            if chkpoint_counter >= CHECKPOINT_INTERVAL:
                self.evaluator.dump_evals(saved_key='arch_seq')
                chkpoint_counter = 0

        logger.info('Hyperopt driver finishing')
        self.evaluator.dump_evals(saved_key='arch_seq')


if __name__ == '__main__':
    args = AMBNeuralArchitectureSearch.parse_args()
    search = AMBNeuralArchitectureSearch(**vars(args))
    signal.signal(signal.SIGINT, on_exit)
    signal.signal(signal.SIGTERM, on_exit)
    search.main()