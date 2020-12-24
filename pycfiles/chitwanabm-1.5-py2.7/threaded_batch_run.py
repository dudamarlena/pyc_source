# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\chitwanabm\threaded_batch_run.py
# Compiled at: 2013-02-14 02:05:58
"""
Allows running a series of model runs (all of the same scenario) on a machine 
with more than one core.
"""
import sys, time, os, argparse, signal, threading, subprocess, logging, socket
from pkg_resources import resource_filename
logger = logging.getLogger(__name__)
active_threads = []

def sighandler(num, frame):
    global sigint
    signal.signal(signal.SIGINT, sighandler)
    sigint = True
    logger.critical('System interrupt captured')
    for thread in list(active_threads):
        thread.kill()

    sys.exit()


sigint = False
signal.signal(signal.SIGINT, sighandler)

class ProcessThread(threading.Thread):

    def __init__(self, thread_ID, script_path, process_args):
        pool_sema.acquire()
        threading.Thread.__init__(self)
        self.threadID = thread_ID
        self.name = thread_ID
        self._script_path = script_path
        self._process_args = process_args
        active_threads.append(self)

    def run(self):
        dev_null = open(os.devnull, 'w')
        command = rcParams['batchrun.python_path'] + ' ' + self._script_path + ' ' + self._process_args + ' --run-id %s' % self.threadID
        if '--log' not in command:
            command += ' --log=CRITICAL'
        self._modelrun = subprocess.Popen(command, cwd=sys.path[0], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        output, unused_err = self._modelrun.communicate()
        retcode = self._modelrun.poll()
        logger.info('Finished run %s (return code %s)' % (self.name, retcode))
        pool_sema.release()
        active_threads.remove(self)
        if retcode != 0:
            logger.exception('Problem while running run %s.\nOutput: %s\nstderr: %s\nReturn code %s\n' % (self.threadID, output, unused_err, retcode))
            return 1
        return 0

    def kill(self):
        logger.warning('Killed run %s' % self.name)
        self._modelrun.terminate()


def main(argv=None):
    global pool_sema
    global rcParams
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    log_console_formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s', datefmt='%I:%M:%S%p')
    ch.setFormatter(log_console_formatter)
    root_logger.addHandler(ch)
    if argv is None:
        argv = sys.argv
    if len(argv) > 1:
        argv = map(lambda x: '"' + x + '"', argv)
    process_args = (' ').join(argv[1:])
    parser = argparse.ArgumentParser(description='Run the chitwanabm agent-based model (ABM).')
    parser.add_argument('--rc', dest='rc_file', metavar='RC_FILE', type=str, default=None, help='Path to a rc file to initialize a model run with custom parameters')
    args = parser.parse_args()
    from chitwanabm import rc_params
    from pyabm.utility import email_logfile
    rc_params.load_default_params(__name__)
    if not args.rc_file == None and not os.path.exists(args.rc_file):
        logger.critical('Custom rc file %s does not exist' % args.rc_file)
        sys.exit()
    rc_params.initialize('chitwanabm', args.rc_file)
    rcParams = rc_params.get_params()
    scenario_path = os.path.join(str(rcParams['model.resultspath']), rcParams['scenario.name'])
    if not os.path.exists(scenario_path):
        try:
            os.mkdir(scenario_path)
        except OSError:
            logger.critical('Could not create scenario directory %s' % scenario_path)
            return 1

    batchrun_name = 'Batch_' + socket.gethostname() + time.strftime('_%Y%m%d-%H%M%S')
    logfile = os.path.join(scenario_path, 'chitwanabm_' + batchrun_name + '.log')
    logger.info('Logging to %s' % logfile)
    fh = logging.FileHandler(logfile)
    log_file_formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s', datefmt='%Y/%m/%d %H:%M:%S')
    fh.setFormatter(log_file_formatter)
    root_logger.addHandler(fh)
    pool_sema = threading.BoundedSemaphore(value=rcParams['batchrun.num_cores'] + 1)
    logger.info("Starting batch run %s, running '%s' scenario" % (batchrun_name, rcParams['scenario.name']))
    run_count = 1
    while run_count <= rcParams['batchrun.num_runs']:
        with pool_sema:
            script_path = resource_filename(__name__, 'runmodel.py')
            new_thread = ProcessThread(run_count, script_path, process_args)
            logger.info('Starting run %s' % new_thread.name)
            new_thread.start()
            run_count += 1

    for thread in list(active_threads):
        thread.join()

    if rcParams['email_log']:
        logger.info('Emailing log to %s' % rcParams['email_log.to'])
        subject = 'chitwanabm Log - %s - %s' % (rcParams['scenario.name'],
         batchrun_name)
        email_logfile(logfile, subject)
    logger.info('Finished batch run %s' % batchrun_name)
    return


if __name__ == '__main__':
    sys.exit(main())