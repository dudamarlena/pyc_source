# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/antoine/work/python_dev/batchOpenMPI_source/examples/batchOpenMPI.py
# Compiled at: 2013-11-08 00:05:19
"""
Module written for batch Jobs calculation using OpenMPI. Load balancing is implemented.
"""
import sys, os, numpy, shutil, time, copy, traceback, atexit
from mpi4py import MPI
MasterProcess = 0
JOB_REQUEST = 1
JOB_FINISHED = 2
PROCESS_INFO = 3
STOP_Signal = -2
comm = MPI.COMM_WORLD
nprocs = comm.Get_size()
time_process_lauched = time.time()
_batchOpenMPI_copy_warning_message_displayed = False

def _display_copy_warning_message():
    global _batchOpenMPI_copy_warning_message_displayed
    if not _batchOpenMPI_copy_warning_message_displayed:
        _batchOpenMPI_copy_warning_message_displayed = True
        sys.stderr.write('WARNING - batchOpenMPI.batchFunction __copy__ and __deepcopy__ methods bypassed as not to break batchOpenMPI; consider creating new batchFunction instance instead.\n')


_batchOpenMPI_one_process_warning_message_displayed = False
drop_previous_batch_results = False
function_list = []

class batchFunction:
    """used as a wrapper for test function, allows for batch processing as well as normal use."""

    def __init__(self, func, multiRef=False, eq_func=None, permissible_exceptions=[]):
        """
        intialise batch function, needs to be done on each process before the begin_MPI_loop call
        
        each input passed to add_to_batch, will be stored and 
        processed when batchOpenMPI.processBatch() is called.
        The result from these input are then calculated on the workers when processBatch is called,
        
        when the function is called, the batch function will first check if
        the input has already be preprocessed, if it has, it will return the 
        stored result, else it will process it locally(on the master). In a well setup upcode,
        their should be no calculations done on the master.

        Once a results has been recalled, it is remove from list of processed inputs.
        Unless multi-reference is enabled.
        
        option aurguements :
          multiRef - use the result from one input is required multiple times, this is off by default as it can get expensive due the batch functions no longer emptying there cache
          eq_func - used inplace of function_input_1 == function_input_cache, when looking up results processed on workers.
          permissible_exceptions - if any of these execeptions occur, the exception is stored and then raise when the batch function is called with the input that created that exception. If an exception occurs which is not in this list, the processBatch function is stoped, the workers are released and the expection is raised on the master.
        """
        self.f = func
        self.multiRef = multiRef
        self.eq_func = eq_func
        if eq_func != None:
            raise NotImplemented, 'the  eq_func keyword for batchFunction is not supported yet.'
        self.permissible_exceptions = permissible_exceptions
        self.job_que = []
        self.jobs_completed = []
        self.evals_by_master = 0
        self.evals_by_workers = 0
        self.dropped_jobs = 0
        self.id = len(function_list)
        function_list.append(self)
        return

    def addtoBatch(self, x, calls_expected=1, multiDep=False):
        """
        adds the setting to the bacth / job que, to be processed with batchOpenMPI.processBatch().
        
        if type(x) is batchFunction_job (create from f.addtobatch()) the associated dependency will be 
        created. for example

        this is end result, which need to be pre-processed.
        > y = f(g(x)) + h(g(x)) # where both f,g,h are to be out sourced to workers.

        the pre-processing , add to batch/que code would be
        > f.addtoBatch(g.addtoBatch(x))
        > h.addtoBatch(g.addtoBatch(x))
        ** NB when you create g, be sure to make it multi-ref : < g = batchFunction(g_org,True)

        alternative pre-processing code 
        > gb = g.addtoBatch(x,2) #making use of calls_expected variable
        > f.addtoBatch(gb)
        > h.addtoBatch(gb)
        ** the advantage of this is that g does not need to support multi-ref. it should be a quicker ...

        now when processBatch() is called, g(x) will first be done, and then the result will be passed to f&h

        optional args :
           multiDep - multiple depedency's is True, x will be assumed to be list with one or more of the items of the list being be batchFunction job. Example of use
                       > f([g(x), h(y)]) # where f,g,h are expensive functions to be processed on workers.
                      preprocessing
                       > f.addtoBatch([g.addtoBatch(x) ,h.addtoBatch(y)], multiDep=True)
                       > batchOpenMPI.processBatch()

        """
        if not isinstance(x, batchFunction_job) and not multiDep:
            new_item = True
            if self.multiRef and not multiDep:
                loc = job_lookup(self.job_que, x)
                new_item = loc == -1
            if new_item:
                self.job_que.append(batchFunction_job(copy.copy(x), None, self.id, calls_expected))
                return self.job_que[(-1)]
            self.job_que[loc].calls_expected = self.job_que[loc].calls_expected + calls_expected
            return self.job_que[loc]
        else:
            self.job_que.append(batchFunction_job(None, x, self.id, calls_expected))
            return self.job_que[(-1)]
        return

    def addtoBatch_multiple(self, x_list):
        """add all the setting to the bacth, then call batchOpenMPI.processBatch(). to process the results"""
        for x in x_list:
            self.addtoBatch(x)

    def clear_results(self):
        """empty the function 'completed_jobs' variable containing input results. 
        Used by process batch if drop_previous_batch_results flag is on."""
        self.dropped_jobs = self.dropped_jobs + len(self.jobs_completed)
        del self.jobs_completed
        self.jobs_completed = []

    def __call__(self, x):
        """if the input(x), has been added to the batch[self.add_to_batch(x)],
        and sometime before this call the batch was processed [batchOpenMPI.processBatch()]. 
        That result will be returned, else the function will be processed here"""
        res_id = job_lookup(self.jobs_completed, x)
        if res_id >= 0:
            job = self.jobs_completed[res_id]
            result = job.result
            if job.calls_made == 0:
                self.evals_by_workers += 1
            job.calls_made = job.calls_made + 1
            if job.calls_expected == job.calls_made:
                del self.jobs_completed[res_id]
            if result[0]:
                return result[1]
            execption = result[1]
            raise execption[0], execption[1]
        else:
            self.evals_by_master += 1
            return self.f(x)

    def __copy__(self):
        """override copying, because copy breaks batchOpenMPI; consider creating new instance instead"""
        _display_copy_warning_message()
        return self

    def __deepcopy__(self, memo):
        """override copying, because copy is no longer in the function_list, and therefore deepcopy breaks batchOpenMPI"""
        _display_copy_warning_message()
        memo[id(self)] = self
        return self

    def __repr__(self):
        return '<batchFunction instance for function ' + str(self.f) + '>'


def job_lookup(job_list, x):
    """job list is a list of batchFunction_job"""
    job_inputs = [ j.input for j in job_list ]
    try:
        if type(x) != numpy.ndarray:
            res_id = job_inputs.index(x)
        else:
            va = [ (x == xv).all() for xv in job_inputs ]
            res_id = va.index(True)
    except ValueError as msg:
        if ' not in list' in str(msg):
            res_id = -1
        else:
            raise ValueError, msg

    return res_id


class counter:
    i = 0

    def __call__(self):
        self.i += 1
        return self.i


batchFunction_job_counter = counter()

class batchFunction_job:
    """stores information about jobs qued for batchFunction,"""

    def __init__(self, job_input, job_dep, bf_id, calls_expected):
        self.input = job_input
        self.dep = job_dep
        self.bf_id = bf_id
        self.calls_expected = calls_expected
        self.calls_made = 0
        self.id = batchFunction_job_counter()

    def dependencys_statisfied(self):
        """
        returns 3 possiblitys
          0 - False, wait for them to be process 
          1 - True, depency's met
          2 - Error will be raised when function called, as one of the depency prerequisites throws an error
              In this case the job will be deleted (as the function cannot be called, as an input will return ERROR!!!)
        """
        if self.dep == None:
            return 1
        else:
            if isinstance(self.dep, batchFunction_job):
                if hasattr(self.dep, 'result'):
                    if self.dep.result[0]:
                        self.input = self.dep.result[1]
                        return 1
                    else:
                        return 2

                else:
                    return 0
            else:
                input_temp = []
                for dep in self.dep:
                    if isinstance(dep, batchFunction_job):
                        if hasattr(dep, 'result'):
                            if dep.result[0]:
                                input_temp.append(dep.result[1])
                            else:
                                return 2
                        else:
                            return 0
                    else:
                        input_temp.append(dep)

                self.input = input_temp
                return 1
            return

    def __str__(self):
        if hasattr(self, 'result'):
            result_txt = str(self.result)
        else:
            result_txt = '<pending>'
        return 'batchFunction_job (id=%i, input=%s, dep=%s, batchFun_id=%i, calls_expected=%i, result=%s)' % (
         self.id, str(self.input), str(self.dep), self.bf_id, self.calls_expected, result_txt)

    def __repr__(self):
        return str(self)


class timer:
    """low class timer, used for performance assements."""
    time = 0

    def tic(self):
        self.t0 = time.time()

    def toc(self):
        self.time += time.time() - self.t0


pB_timeComm = timer()

def processBatch(lastProcessBatch=False):
    """function for master processes,
    the worker processed are contacted and the batch/que is processed.

    If lastProcessBatch is True, then the workers will be released when the job que is finished. This can always be left as False, provided that the end_MPI_loop function is called at the end of the script."""
    global _batchOpenMPI_one_process_warning_message_displayed
    job_que = []
    for bf in function_list:
        job_que = job_que + bf.job_que
        bf.job_que = []
        if drop_previous_batch_results:
            bf.clear_results()

    workers_available = range(1, nprocs)
    if nprocs > 1:
        req_worker = []
        req_input = []

        def SubmitJob(WorkerID):
            cf = False
            if len(job_que) > 0:
                i = -1
                while not cf:
                    i = i + 1
                    if i >= len(job_que):
                        break
                    dep_status = job_que[i].dependencys_statisfied()
                    if dep_status == 1:
                        cf = True
                        job = job_que.pop(i)
                    if dep_status == 2:
                        del job_que[i]
                        i = i - 1

            if cf:
                job_data = [
                 job.bf_id, job.input]
                pB_timeComm.tic()
                comm.send(job_data, WorkerID, JOB_REQUEST)
                pB_timeComm.toc()
                req_worker.append(WorkerID)
                req_input.append(job)
            else:
                if len(req_input) == 0 and len(job_que) > 0:
                    raise RuntimeError, 'processBatch - could not process depency for jobs still in que!!! ' + str(job_que)
                if lastProcessBatch and len(job_que) == 0:
                    releaseWorker(WorkerID)
                else:
                    workers_available.append(WorkerID)

        workers_available = range(1, nprocs)

        def free_Worker_And_Submit_NewJobs(freed_Worker=-1):
            if freed_Worker != -1:
                workers_available.append(freed_Worker)
            workers_to_send_jobs_to = copy.copy(workers_available)
            del workers_available[:]
            for worker_id in workers_to_send_jobs_to:
                SubmitJob(worker_id)

        free_Worker_And_Submit_NewJobs()
        while len(req_worker) > 0:
            pB_timeComm.tic()
            status = MPI.Status()
            comm.Probe(MPI.ANY_SOURCE, JOB_FINISHED, status)
            Process_Finished = status.Get_source()
            result = comm.recv(None, Process_Finished, JOB_FINISHED)
            pB_timeComm.toc()
            request_ind = req_worker.index(Process_Finished)
            job_finished = req_input[request_ind]
            del req_input[request_ind]
            del req_worker[request_ind]
            job_finished.result = result
            function_list[job_finished.bf_id].jobs_completed.append(job_finished)
            if result[0] == False:
                exception, exception_msg, traceback_info = result[1]
                if exception not in function_list[job_finished.bf_id].permissible_exceptions:
                    end_MPI_loop()
                    print traceback_info
                    exit(2)
            free_Worker_And_Submit_NewJobs(Process_Finished)

        if not lastProcessBatch and len(workers_available) != len(range(1, nprocs)):
            raise RuntimeError, 'processBatch - check free_Worker_And_Submit_NewJobs. workers_available' + str(workers_available)
    elif not _batchOpenMPI_one_process_warning_message_displayed:
        sys.stderr.write('WARNING!!: cannot process batch, as only one process active. Was the program lauched using mpirun?\n')
        _batchOpenMPI_one_process_warning_message_displayed = True
    return


WorkingDir_base = ()
WorkingDir_files = []

def worker_only_procedure(rank):
    pass


def begin_MPI_loop(print_launch_messages=True):
    """
    ammend_sys_excepthook , adds code to so that when an unhandled exception is raised on the master, the workers process are closed so the mpirun does not hang.
    """
    myrank = comm.Get_rank()
    procnm = MPI.Get_processor_name()
    if print_launch_messages:
        print 'Process (%d of %d) launched on %s. pid:%d ' % (myrank, nprocs, procnm, os.getpid())
    set_workingDirectory = WorkingDir_base != ()
    if myrank == MasterProcess:
        atexit.register(end_MPI_loop)
    else:
        worker_only_procedure(myrank)
        if set_workingDirectory:
            if not ('%(pid)' in WorkingDir_base or '%(rank)' in WorkingDir_base):
                raise AssertionError
                wdir = WorkingDir_base % {'pid': os.getpid(), 'rank': myrank}
                os.path.exists(wdir) or os.makedirs(wdir)
            for f in WorkingDir_files:
                fname = os.path.basename(f)
                shutil.copy(f, wdir + '/' + fname)

            launch_dir = os.getcwd()
            os.chdir(wdir)
        time_useful_work = timer()
        time_recieving_instructions = timer()
        time_sending_results = timer()
        jobs_completed = 0

        def Wait_for_New_instruction():
            """ Recieve a message from the master process.
            Instruction in the form of [function_id,function_input]"""
            return comm.recv(None, MasterProcess, JOB_REQUEST)

        instructions = Wait_for_New_instruction()
        while instructions != STOP_Signal:
            time_useful_work.tic()
            try:
                func_id, func_input = instructions
                result = [True, function_list[func_id].f(func_input)]
            except:
                exceptionInfo = sys.exc_info()[0:2]
                result = [False, [exceptionInfo[0], exceptionInfo[1], traceback.format_exc()]]

            time_useful_work.toc()
            jobs_completed = jobs_completed + 1
            time_sending_results.tic()
            comm.send(result, MasterProcess, JOB_FINISHED)
            time_sending_results.toc()
            time_recieving_instructions.tic()
            instructions = Wait_for_New_instruction()
            time_recieving_instructions.toc()

        comm.send([myrank, jobs_completed, time.time() - time_process_lauched, time_useful_work.time,
         time_recieving_instructions.time, time_sending_results.time], MasterProcess, PROCESS_INFO)
        if set_workingDirectory:
            os.chdir(launch_dir)
            for f in os.listdir(wdir):
                os.remove(wdir + '/' + f)

            os.rmdir(wdir)
        sys.exit()


process_information = []
processes_stoped = []

def releaseWorker(i):
    assert i not in processes_stoped
    comm.send(STOP_Signal, i, JOB_REQUEST)
    process_information.append(comm.recv(None, i, PROCESS_INFO))
    processes_stoped.append(i)
    return


def end_MPI_loop(print_stats=False):
    """sends stop signal to all workers"""
    for i in range(1, nprocs):
        if i not in processes_stoped:
            releaseWorker(i)

    if print_stats:
        showStats()


def showStats():
    if not all(i in processes_stoped for i in range(1, nprocs)):
        sys.stderr.write('batchOpenMPI.showStats call ignored as end_MPI_loop has not been called.\n')
        return
    print '            --------- batchOpenMPI Stats ---------'
    print 'process    jobs completed      time: uW/ sR/ wI* (s)    utilisation(%)'
    for pi in process_information:
        print ' %3i          %5i        %8.2f/%8.2f/%8.2f       %5.2f' % (pi[0], pi[1], pi[3], pi[5], pi[4],
         pi[3] / pi[2] * 100)

    tM = time.time() - time_process_lauched
    tUW = sum([ pi[3] for pi in process_information ]) + tM - pB_timeComm.time
    tAlive = sum([ pi[2] for pi in process_information ]) + tM
    print '   * time doing; uW - useful work, sR - sending results, wI - waiting for instructions, Total\n  time running master (s) :          %8.3f \n  total CPU time (s) :               %8.3f \n  total CPU time actually used (s) : %8.3f\n  overall utilization : %2.2f %%' % (tM, tAlive, tUW, tUW / tAlive * 100)
    print 'function stats :\n- solved on master  %s\n- solved on workers %s\n- jobs uncollected  %s\n- jobs dropped      %s' % (str([ bf.evals_by_master for bf in function_list ]),
     str([ bf.evals_by_workers for bf in function_list ]),
     str([ len(bf.jobs_completed) for bf in function_list ]),
     str([ bf.dropped_jobs for bf in function_list ]))