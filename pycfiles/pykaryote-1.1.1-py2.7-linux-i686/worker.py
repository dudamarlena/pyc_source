# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pykaryote/petri/worker.py
# Compiled at: 2013-08-30 10:09:51
"""Code to be run by worker processors.

Worker processors execute jobs and report status back to the master processor.
"""
from mpi4py import MPI
import multiprocessing, os.path, os, sys, shutil, time, tempfile, tags, numpy as np, traceback, matplotlib as mpl
mpl.use('Agg')
from pykaryote.utils.comparison import Grapher, get_config
from pykaryote.sim.simulation import Simulation
from pykaryote.utils.analysis import aggregate_batch
from pykaryote.utils.comparison import AnalyzerAggregator
comm = MPI.COMM_WORLD

class Worker(object):
    """Runs jobs on worker processors and reports status back to the master.

    Jobs are received from the master thread. Typical jobs include running
    simulations and graphing comparison batches.
    """

    def __init__(self, data_dir, status_interval=10):
        """
        Args:
            status_interval (int): The minimum number of seconds to wait before
            sending status data to the master thread.
        """
        self._status_interval = status_interval
        self._last_status = time.time()
        self._thread = None
        self._job = None
        self._wait_for_orders = True
        self._dest_dir = data_dir
        return

    def run(self):
        """Runs the current job.
        """
        while self._wait_for_orders:
            status = MPI.Status()
            message = comm.recv(source=tags.MASTER_ID, tag=MPI.ANY_TAG, status=status)
            if status.tag == tags.JOB_TAG:
                if self._job is None:
                    self._run_job(message)
                else:
                    comm.send(message, tags.MASTER_ID, tag=tags.FAILED_TAG)
            elif status.tag == tags.SHUTDOWN_TAG:
                self._wait_for_orders = False

        return

    def _status_update(self, current_gen, target_gen, eta):
        """Receives status from a running simulation.

        This is a callback function to be passed to simulation.run()
        Reports status to master in intervals of at least self._status_interval
        seconds.
        """
        if time.time() - self._last_status > self._status_interval:
            status = np.array([current_gen, target_gen, int(eta)], dtype=int)
            comm.send(status, tags.MASTER_ID, tag=tags.STATUS_TAG)
            self._last_status = time.time()

    def _run_job(self, job):
        """Runs a job.

        Jobs can be either comparison jobs, or graphing jobs. A comparison
        job runs a single simulation as part of a comparison. A graphing job
        graphs a completed comparison.

        Simulations are run in a temporary directory and then copied back
        to the destination directory if they finish successfully.
        """
        self._job = job
        if job.get('type') == 'comparison_graph':
            self._run_comparison_graph_job(job)
        elif job.get('type') == 'comparison':
            self._run_comparison_job(job)
        else:
            self._job = None
            print ('unrecognized job type: {}').format(job.get('type'))
            comm.send(job, tags.MASTER_ID, tag=tags.FAILED_TAG)
        return

    def _run_comparison_job(self, job):
        """Runs a simulation which is part of a larger comparison.

        If exceptions occur, they are caught and the job is reported as failed.
        Timed out jobs are also treated as failed.
        """
        dest_data_dir = os.path.join(self._dest_dir, job['comparison_name'], ('sim-{}').format(job['sim_num']))
        temp_data_dir = tempfile.mkdtemp(prefix='simulation_data')
        sim_name = ('run-{}').format(job['run_num'])
        self._sim = Simulation(job['config_filename'], data=temp_data_dir, name=sim_name, clear=True, comparison=True, status_callback=self._status_update)
        sim_dir = os.path.join(temp_data_dir, sim_name)
        try:
            self._sim.run(log=False, verbose=False)
            if self._sim.timed_out:
                raise RuntimeError('Simulation timed out.')
            shutil.move(sim_dir, os.path.join(dest_data_dir, sim_name))
            self._sim = None
            self._job = None
            comm.send(job, tags.MASTER_ID, tag=tags.SUCCESS_TAG)
        except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            if e.args[0] != 'Simulation timed out.':
                traceback.print_exception(exc_type, exc_value, exc_traceback)
            with open(os.path.join(sim_dir, 'error.log'), 'w') as (f):
                traceback.print_exception(exc_type, exc_value, exc_traceback, file=f)
            self._sim = None
            self._job = None
            failed_dir = os.path.join(self._dest_dir, job['comparison_name'], 'failed', ('sim-{}').format(job['sim_num']), ('run-{}').format(job['run_num']))
            shutil.move(sim_dir, failed_dir)
            comm.send(job, tags.MASTER_ID, tag=tags.FAILED_TAG)

        shutil.rmtree(temp_data_dir)
        return

    def _run_comparison_graph_job(self, job):
        """Wraps a comparison graphing job in a try/catch clause, reporting
        errors if they occur.
        """
        try:
            self.graph_comparison(job['comparison_name'], values=job['values'], clean=job['clean'])
            self._job = None
            comm.send(job, tags.MASTER_ID, tag=tags.SUCCESS_TAG)
        except Exception as e:
            print e
            traceback.print_exc()
            self._job = None
            comm.send(job, tags.MASTER_ID, tag=tags.FAILED_TAG)

        return

    def graph_comparison(self, cmp_name, values=None, clean=True):
        """Aggregate and graph a completed comparison.
        """
        comparison_dir = os.path.join(self._dest_dir, cmp_name)
        if os.path.isfile(os.path.join(self._dest_dir, cmp_name, 'comparative-analyzer')):
            try:
                self._graph_comparison
            except Exception:
                self._aggregate_comparison(comparison_dir, cmp_name, values)
                self._graph_comparison(comparison_dir)

        else:
            self._aggregate_comparison(comparison_dir, cmp_name, values)
            self._graph_comparison(comparison_dir)
        if clean:
            for batch_dir in os.listdir(comparison_dir):
                if batch_dir[:4] == 'sim-':
                    shutil.rmtree(os.path.join(comparison_dir, batch_dir), ignore_errors=True)

    def _aggregate_comparison(self, comparison_dir, cmp_name, values=None):
        """Aggregate a completed comparison.

        Args:
            values: A list of values used for varied options from the
            comparison.
        """
        sim_config = os.path.join(comparison_dir, 'sim_configs', 'sim-0.cfg')
        batch_sim_dirs = []
        for batch_sim_dir in os.listdir(comparison_dir):
            if batch_sim_dir[:4] == 'sim-':
                batch_sim_dirs.append(batch_sim_dir)
                analyzer_dirs = []
                for run_dir in os.listdir(os.path.join(comparison_dir, batch_sim_dir)):
                    if run_dir[:4] == 'run-':
                        analyzer_dirs.append(os.path.join(comparison_dir, batch_sim_dir, run_dir, 'analyzer'))

                output_analyzer_dir = os.path.join(comparison_dir, batch_sim_dir, 'analyzer')
                aggregate_batch(analyzer_dirs, output_analyzer_dir)

        if values is None:
            cmp_filename = os.path.join(comparison_dir, 'cmp.cfg')
            options, values = get_config(cmp_filename)
        agg = AnalyzerAggregator(self._dest_dir, cmp_name, values, sim_config)
        agg.compile_all()
        return

    def _graph_comparison(self, comparison_dir):
        sim_config = os.path.join(comparison_dir, 'sim_configs', 'sim-0.cfg')
        g = Grapher(comparison_dir, sim_config, verbose=False)
        g.save_all()