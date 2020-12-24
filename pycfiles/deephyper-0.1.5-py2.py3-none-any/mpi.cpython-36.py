# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/mpi.py
# Compiled at: 2019-07-11 14:24:06
# Size of source mod 2**32: 5293 bytes
import signal, logging, argparse
from mpi4py import MPI
from deephyper.search import util
from deephyper.evaluator.evaluate import Evaluator
from .search import Search
from .hps.ambs import AMBS, on_exit as ambs_on_exit
from .hps.ga import GA, on_exit as ga_on_exit
logger = logging.getLogger(__name__)

class MPIWorker:
    __doc__ = 'MPIWorker is a class instanciated on non-zero MPI rank to\n    execute evaluations. It internally uses one of the existing\n    evaluators (e.g. threadPool) to dispatch work sent to it.\n    \n    Attributes\n    ----------\n    comm : MPI communicator gathering all workers and the master\n    rank : rank of this process in the MPI communicator\n    problem : instance of the problem space\n    run_func : function to run\n    evaluator : Evaluator instance\n    '

    def __init__(self, comm, problem, run, evaluator, **kwargs):
        """Constructor."""
        self.comm = comm
        self.rank = comm.Get_rank()
        self.problem = util.generic_loader(problem, 'Problem')
        self.run_func = util.generic_loader(run, 'run')
        self.evaluator = Evaluator.create((self.run_func), method=evaluator)

    def _exec(self, x):
        """Adds the evaluation of a new point and return its uid."""
        uid = self.evaluator.add_eval(x)
        return uid

    def run(self):
        """Runs the main loop of the MPI worker."""
        pending_uids = dict()
        request = None
        while 1:
            if request is None:
                request = comm.irecv(source=0, tag=(MPI.ANY_TAG))
            else:
                if len(pending_uids) == 0:
                    status = MPI.Status()
                    completed, cmd_info = True, MPI.Request.wait(request, status=status)
                else:
                    completed, cmd_info = MPI.Request.test(request, status=status)
            if completed:
                tag = status.Get_tag()
                cmd = cmd_info['cmd']
                if cmd == 'exit':
                    break
                if cmd == 'exec':
                    args = cmd_info.get('args', [])
                    kwargs = cmd_info.get('kwargs', dict())
                    uid = (self._exec)(*args, **kwargs)
                    pending_uids[uid] = tag
                request = None
            else:
                if len(pending_uids) != 0:
                    for x, y in self.evaluator.get_finished_evals(timeout=0.1):
                        uid = self.evaluator.encode(x)
                        self.comm.send(y, dest=0, tag=(pending_uids.pop(uid)))


class MPIManager:
    __doc__ = 'The MPIManager class is instanciated in rank 0 of the provided MPI\n    communicator. It instanciates a search class and dispatches evaluations\n    to the MPIWorkers on other ranks.\n    \n    Attributes\n    ----------\n\n    comm : MPI communicator\n    kwargs : dictionary of keyword arguments from the command line\n    search : Search class\n    '

    def __init__(self, comm, **kwargs):
        """Constructor."""
        self.comm = comm
        self.args = kwargs
        self.args['evaluator'] = '__mpiPool'
        search_cls = (self._get_search_cls)(**self.args)
        self.search = search_cls(**self.args)

    @staticmethod
    def parse_args():
        """Parses command line arguments. This method is used to
        enable the --search option, allowing users to request a
        particular search method (since the search module is not
        provided in the command line when using the MPI mode)."""
        parser = argparse.ArgumentParser(conflict_handler='resolve')
        parser.add_argument('--search', choices=[
         'AMBS', 'GA'],
          help='type of HPS search method to use')
        args, remaining_cmd = parser.parse_known_args()
        search_cls = (MPIManager._get_search_cls)(**vars(args))
        remaining_args = search_cls.parse_args(remaining_cmd)
        setattr(remaining_args, 'search', args.search)
        return remaining_args

    def run(self):
        """Runs the MPIManager. We have to check whether search is
        AMBS or GA because AMBS uses main() while GA uses run()."""
        if isinstance(self.search, AMBS):
            signal.signal(signal.SIGINT, ambs_on_exit)
            signal.signal(signal.SIGTERM, ambs_on_exit)
            self.search.main()
        elif isinstance(self.search, GA):
            self.search.run()

    @staticmethod
    def _get_search_cls(**kwargs):
        """Helper method to get the search class."""
        search_cls = None
        if kwargs['search'] == 'AMBS':
            search_cls = AMBS
        else:
            if kwargs['search'] == 'GA':
                search_cls = GA
        return search_cls


if __name__ == '__main__':
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    kwargs = MPIManager.parse_args()
    if rank == 0:
        master = MPIManager(comm, **vars(kwargs))
        master.run()
    else:
        worker = MPIWorker(comm, **vars(kwargs))
        worker.run()