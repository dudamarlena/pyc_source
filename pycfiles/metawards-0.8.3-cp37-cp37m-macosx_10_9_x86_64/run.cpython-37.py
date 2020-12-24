# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/chris/GitHub/MetaWards/build/lib.macosx-10.9-x86_64-3.7/metawards/app/run.py
# Compiled at: 2020-04-21 13:11:28
# Size of source mod 2**32: 35047 bytes
"""
The metawards command line program.

Usage:
    To get the help for this program and the list of all of the
    arguments (with defaults) use;

    metawards --help
"""
__all__ = [
 'get_parallel_scheme', 'parse_args', 'get_hostfile',
 'get_cores_per_node', 'get_threads_per_task',
 'scoop_supervisor', 'mpi_supervisor',
 'cli']

def get_parallel_scheme():
    """This function tries to work out which of the different parallel
       methods we should use to distribute work between multiple processes.

       Detected schemes are "mpi4py", "scoop", and if none of these
       are found, then "multiprocessing"
    """
    import sys
    if 'mpi4py' in sys.modules:
        return 'mpi4py'
    if 'scoop' in sys.modules:
        return 'scoop'
    return 'multiprocessing'


def parse_args():
    """Parse all of the command line arguments"""
    import argparse, sys
    parser = argparse.ArgumentParser(description='MetaWards epidemic modelling - see https://github.com/metawards/metawards for more information',
      prog='metawards')
    parser.add_argument('--version', action='store_true', default=None,
      help='Print the version information about metawards')
    parser.add_argument('-i', '--input', type=str, help='Input file for the simulation that specifies the adjustable parameters to change for each run of the model. You must supply some input to run a model!')
    parser.add_argument('-l', '--line', type=str, default=None, nargs='*', help="Line number (or line numbers) containing the values of adjustable parameters to run for this run (or runs) of the model If this isn't specified then model runs will be performed for adjustable parameters given on all lines from the input file. You can specify many numbers, and ranges are also accepted, e.g. '-l 5 6-10 12,13,14' etc. Note that the line numbers are 0-indexed, e.g. the first line of the file is line 0. Ranges are inclusive, so 3-5 is the same as 3 4 5")
    parser.add_argument('-r', '--repeats', type=int, default=None, help='The number of repeat runs of the model to perform for each value of the adjustable parameters. By default only a single run will be performed for each set of adjustable parameters')
    parser.add_argument('-s', '--seed', type=int, default=None, help='Random number seed for this run (default is to use a random seed)')
    parser.add_argument('-a', '--additional', type=str, default=None, nargs='*',
      help='File (or files) containing additional seed of outbreak for the model. These are used to seed additional infections on specific days at different locations during a model run')
    parser.add_argument('-o', '--output', type=str, default='output', help="Path to the directory in which to place all output files (default 'output'). This directory will be subdivided if multiple adjustable parameter sets or repeats are used.")
    parser.add_argument('-d', '--disease', type=str, default=None, help="Name of the disease to model (default is 'ncov')")
    parser.add_argument('-I', '--input-data', type=str, default='2011Data', help="Name of the input data set for the network (default is '2011Data')")
    parser.add_argument('--start-date', type=str, default=None, help="Date of the start of the model outbreak. This accepts dates either is iso-format, or fuzzy dates such as 'monday', 'tomorrow' etc. This is used to work out which days are weekends, or to make it easier to specify time-based events.")
    parser.add_argument('--start-day', type=int, default=0, help="The start day of the model outbreak. By default the model outbreak starts on day zero (0), with each step of the model representing an additional day. Use this to start from a later day, which may be useful if you want to more quickly reach time based events. Note that the passed '--start-date' is always day 0, so day 10 has a date which is 10 days after start-date")
    parser.add_argument('-p', '--parameters', type=str, default='march29', help="Name of the input parameter set used to control the simulation (default 'march29')")
    parser.add_argument('-R', '--repository', type=str, default=None, help="Path to the MetaWardsData repository. If unspecified this defaults to the value in the environment variable METAWARDSDATA or, if that isn't specified, to $HOME/GitHub/MetaWardsData")
    parser.add_argument('-P', '--population', type=int, default=57104043, help='Initial population (default 57104043)')
    parser.add_argument('-n', '--nsteps', type=int, default=730, help='Maximum number of steps (days) to run for the simulation. Each step represents one day in the outbreak (default is to run for a maximum of two years - 730 days)')
    parser.add_argument('-u', '--user-variables', type=str, default=None, help='Name of the file containing user-defined custom variables. These provide extra information that can be read by the custom integrators or custom extractors.')
    parser.add_argument('--iterator', type=str, default=None, help='Name of the iterator to use to advance the outbreak at each step (day). For a full explanation see the tutorial at https://metawards.github.io')
    parser.add_argument('--extractor', type=str, default=None, help='Name of the extractor to use to extract information during a model run. For a full explanation see the tutorial at https://metawards.github.io')
    parser.add_argument('--UV', type=float, default=0.0, help='Value for the UV parameter for the model (default is 0.0)')
    parser.add_argument('--nthreads', type=int, default=None, help='Number of threads over which parallelise an individual model run. The total number of cores used by metawards will be nprocesses x nthreads')
    parser.add_argument('--nprocs', type=int, default=None, help='The number of processes over which to parallelise the different model runs for different adjustable parameter sets and repeats. By default this will automatically work out the number of processes based on the way metawards is launched. Use this option if you want to specify the number of processes manually.')
    parser.add_argument('--hostfile', type=str, default=None, help='The hostfile containing the names of the compute nodes over which to run a parallel job. If this is not set, the program will attempt to automatically get this information from the cluster queueing system. Use this if the auto-detection fails')
    parser.add_argument('--cores-per-node', type=int, default=None, help='Set the number of processor cores available on each of the compute nodes in the cluster that will be used to run the models (if a cluster is used). If this is not set then the program will attempt to get this information from the cluster queueing system. Use this option if the auto-detection fails.')
    parser.add_argument('--auto-bzip', action='store_true', default=None,
      help='Automatically bz2 compress all output files as they are written.')
    parser.add_argument('--no-auto-bzip', action='store_true', default=None,
      help='Do not automatically bz2 compress all output files as they are written.')
    parser.add_argument('--force-overwrite-output', action='store_true', default=False,
      help="Whether or not to force overwriting of any existing output. Using this option will tell metawards that it is safe to delete the contents of the output directory specified in by '--output' if it already exists. Dangerous as this can remove existing output files")
    parser.add_argument('--profile', action='store_true', default=None,
      help='Enable profiling of the code')
    parser.add_argument('--no-profile', action='store_true', default=None,
      help='Disable profiling of the code')
    parser.add_argument('--mpi', action='store_true', default=None, help='Force use of MPI to parallelise across runs')
    parser.add_argument('--scoop', action='store_true', default=None, help='Force use of scoop to parallelise across runs')
    parser.add_argument('--already-supervised', action='store_true', default=None,
      help=(argparse.SUPPRESS))
    args = parser.parse_args()
    if args.version:
        from metawards import get_version_string
        print(get_version_string())
        sys.exit(0)
    return (args, parser)


def get_hostfile(args):
    """Attempt to find the name of the hostfile used to specify the hosts
       to use in a cluster
    """
    if args.hostfile:
        return args.hostfile
    import os
    hostfile = os.getenv('PBS_NODEFILE')
    if hostfile:
        return hostfile
    hostfile = os.getenv('SLURM_HOSTFILE')
    if hostfile:
        return hostfile


def get_cores_per_node(args):
    """Return the number of cores per node in the cluster"""
    if args.cores_per_node:
        return args.cores_per_node
    import os
    try:
        cores_per_node = int(os.getenv('METAWARDS_CORES_PER_NODE'))
        if cores_per_node > 0:
            return cores_per_node
    except Exception:
        pass

    raise ValueError('You must specify the number of cores per node using --cores-per-node or by setting the environment variable METAWARDS_CORES_PER_NODE')


def get_threads_per_task(args):
    if args.nthreads:
        return args.nthreads
    import os
    try:
        nthreads = int(os.getenv('METAWARDS_THREADS_PER_TASK'))
        if nthreads > 0:
            return nthreads
        nthreads = int(os.getenv('OMP_NUM_THREADS'))
        if nthreads > 0:
            return nthreads
    except Exception:
        pass

    raise ValueError('You must specify the number of threads per task using --nthreads or by setting the environment variables METAWARDS_THREADS_PER_TASK or OMP_NUM_THREADS')


def scoop_supervisor(hostfile, args):
    """Function used by the scoop supervisor to get the information needed to
       form the scoop call to run a scoop version of the program
    """
    import os, sys
    print('RUNNING A SCOOP PROGRAM')
    outdir = args.output
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    cores_per_node = get_cores_per_node(args)
    print(f"Will run jobs assuming {cores_per_node} cores per compute node")
    nthreads = get_threads_per_task(args)
    print(f"Will use {nthreads} OpenMP threads per model run...")
    tasks_per_node = int(cores_per_node / nthreads)
    print(f"...meaning that the number of model runs per node will be {tasks_per_node}")
    hostnames = {}
    with open(hostfile, 'r') as (FILE):
        line = FILE.readline()
        while line:
            hostname = line.strip()
            hostnames[hostname] = 1
            line = FILE.readline()

    hostnames = list(hostnames.keys())
    hostnames.sort()
    print(f"Number of compute nodes equals {len(hostnames)}")
    print(', '.join(hostnames))
    nprocs = tasks_per_node * len(hostnames)
    if args.nprocs:
        if nprocs != args.nprocs:
            print(f"WARNING: You are using a not-recommended number of processes {args.nprocs} for the cluster {nprocs}.")
        nprocs = args.nprocs
    print(f"Total number of parallel processes to run will be {nprocs}")
    print(f"Total number of cores in use will be {nprocs * nthreads}")
    hostfile = os.path.join(outdir, 'hostfile')
    print(f"Writing hostfile to {hostfile}")
    with open(hostfile, 'w') as (FILE):
        i = 0
        while i < nprocs:
            for hostname in hostnames:
                FILE.write(hostname + '\n')
                i += 1
                if i == nprocs:
                    break

    import subprocess, shlex
    pyexe = sys.executable
    script = os.path.abspath(sys.argv[0])
    args = ' '.join(sys.argv[1:])
    cmd = f"{pyexe} -m scoop --hostfile {hostfile} -n {nprocs} {script} --already-supervised {args} --nprocs {nprocs}"
    print(f"Executing scoop job using '{cmd}'")
    try:
        args = shlex.split(cmd)
        subprocess.run(args).check_returncode()
    except Exception as e:
        try:
            print('ERROR: Something went wrong!')
            print(f"{e.__class__}: {e}")
            sys.exit(-1)
        finally:
            e = None
            del e

    print('Scoop processes completed successfully')


def mpi_supervisor(hostfile, args):
    """Function used by the MPI supervisor to get the information needed to
       form the mpiexec call to run an MPI version of the program
    """
    import os, sys
    print('RUNNING AN MPI PROGRAM')
    outdir = args.output
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    cores_per_node = get_cores_per_node(args)
    print(f"Will run jobs assuming {cores_per_node} cores per compute node")
    nthreads = get_threads_per_task(args)
    print(f"Will use {nthreads} OpenMP threads per model run...")
    tasks_per_node = int(cores_per_node / nthreads)
    print(f"...meaning that the number of model runs per node will be {tasks_per_node}")
    hostnames = {}
    with open(hostfile, 'r') as (FILE):
        line = FILE.readline()
        while line:
            hostname = line.strip()
            hostnames[hostname] = 1
            line = FILE.readline()

    hostnames = list(hostnames.keys())
    hostnames.sort()
    print(f"Number of compute nodes equals {len(hostnames)}")
    print(', '.join(hostnames))
    nprocs = tasks_per_node * len(hostnames)
    if args.nprocs:
        if nprocs != args.nprocs:
            print(f"WARNING: You are using an unrecommended number of processes {args.nprocs} for the cluster {nprocs}.")
        nprocs = args.nprocs
    print(f"Total number of parallel processes to run will be {nprocs}")
    print(f"Total number of cores in use will be {nprocs * nthreads}")
    hostfile = os.path.join(outdir, 'hostfile')
    print(f"Writing hostfile to {hostfile}")
    with open(hostfile, 'w') as (FILE):
        i = 0
        while i < nprocs:
            for hostname in hostnames:
                FILE.write(hostname + '\n')
                i += 1
                if i == nprocs:
                    break

    mpiexec = os.getenv('MPIEXEC')
    if mpiexec is None:
        mpiexec = 'mpiexec'
    import subprocess, shlex
    try:
        args = shlex.split(f"{mpiexec} -v")
        p = subprocess.run(args, stdout=(subprocess.PIPE), stderr=(subprocess.STDOUT))
        v = p.stdout.decode('utf-8').strip()
        print(f"{mpiexec} -v => {v}")
        if v.find('HPE HMPT') != -1:
            raise ValueError("metawards needs a more modern MPI library than HPE's, so please compile to another MPI and use that.")
    except Exception as e:
        try:
            print(f"[ERROR] {e.__class__} {e}")
        finally:
            e = None
            del e

    pyexe = sys.executable
    script = os.path.abspath(sys.argv[0])
    args = ' '.join(sys.argv[1:])
    cmd = f"{mpiexec} -np {nprocs} -hostfile {hostfile} {pyexe} -m mpi4py {script} --already-supervised {args}"
    print(f"Executing MPI job using '{cmd}'")
    try:
        args = shlex.split(cmd)
        subprocess.run(args).check_returncode()
    except Exception as e:
        try:
            print('ERROR: Something went wrong!')
            print(f"{e.__class__}: {e}")
            sys.exit(-1)
        finally:
            e = None
            del e

    print('MPI processes completed successfully')


def cli():
    """Main function for the command line interface. This does one of three
       things:

       1. If this is the main process, then it parses the arguments and
          runs and manages the jobs

       2. If this is a worker process, then it starts up and waits for work

       3. If this is a supervisor process, then it query the job scheduling
          system for information about the compute nodes to use, and will then
          set up and run a manager (main) process that will use those
          nodes to run the jobs
    """
    parallel_scheme = get_parallel_scheme()
    if parallel_scheme == 'mpi4py':
        from mpi4py import MPI
        comm = MPI.COMM_WORLD
        nprocs = comm.Get_size()
        rank = comm.Get_rank()
        if rank != 0:
            print(f"Starting worker process {rank + 1} of {nprocs - 1}...")
            return
        print('Starting main process...')
    else:
        if parallel_scheme == 'scoop':
            print('STARTING SCOOP PROCESS')
        else:
            import sys
            args, parser = parse_args()
            if not args.already_supervised:
                hostfile = get_hostfile(args)
                if hostfile:
                    if args.mpi:
                        mpi_supervisor(hostfile, args)
                        return
                        if args.scoop:
                            scoop_supervisor(hostfile, args)
                            return
                        try:
                            import scoop
                            have_scoop = True
                        except Exception:
                            have_scoop = False

                        if have_scoop:
                            scoop_supervisor(hostfile, args)
                            return
                    else:
                        try:
                            import mpi4py
                            have_mpi4py = True
                        except Exception:
                            have_mpi4py = False

                    if have_mpi4py:
                        mpi_supervisor(hostfile, args)
                        return
            should_run = False
            for arg in [args.input, args.repeats, args.disease, args.additional]:
                if arg is not None:
                    should_run = True
                    break

            if not should_run:
                parser.print_help(sys.stdout)
                sys.exit(0)
            if args.repeats is None:
                args.repeats = 1
            else:
                from metawards import Parameters, Network, Population, get_version_string
                print(get_version_string())
                print(f"Command used to run this job:\n{' '.join(sys.argv)}\n")
                if args.input:
                    if args.line is None or len(args.line) == 0:
                        linenums = None
                        print(f"Using parameters from all lines of {args.input}")
                    else:
                        from metawards.utils import string_to_ints
                        linenums = string_to_ints(args.line)
                        if len(linenums) == 0:
                            print(f"You cannot read no lines from {args.input}?")
                            sys.exit(-1)
                        else:
                            if len(linenums) == 1:
                                print(f"Using parameters from line {linenums[0]} of {args.input}")
                            else:
                                print(f"Using parameters from lines {linenums} of {args.input}")
                    from metawards import VariableSets, VariableSet
                    variables = VariableSets.read(filename=(args.input), line_numbers=linenums)
                else:
                    from metawards import VariableSets, VariableSet
                    variables = VariableSets()
                    variables.append(VariableSet())
                nrepeats = args.repeats
                if not nrepeats is None:
                    if nrepeats < 1:
                        nrepeats = 1
                    if nrepeats == 1:
                        print('Performing a single run of each set of parameters')
                else:
                    print(f"Performing {nrepeats} runs of each set of parameters")
            variables = variables.repeat(nrepeats)
            from metawards.utils import guess_num_threads_and_procs
            nthreads, nprocs = guess_num_threads_and_procs(njobs=(len(variables)),
              nthreads=(args.nthreads),
              nprocs=(args.nprocs),
              parallel_scheme=parallel_scheme)
            print(f"\nNumber of threads to use for each model run is {nthreads}")
            if nprocs > 1:
                print(f"Number of processes used to parallelise model runs is {nprocs}")
                print(f"Parallelisation will be achieved using {parallel_scheme}")
            seed = args.seed
            if seed is None:
                import random
                seed = random.randint(10000, 99999999)
            print(f"\nUsing random number seed {seed}")
            start_day = args.start_day
            if start_day < 0:
                raise ValueError(f"You cannot use a start day {start_day} that is less than zero!")
            else:
                start_date = None
                if args.start_date:
                    try:
                        from dateparser import parse
                        start_date = parse(args.start_date).date()
                    except Exception:
                        pass

                    if start_date is None:
                        from datetime import date
                        try:
                            start_date = date.fromisoformat(args.start_date)
                        except Exception as e:
                            try:
                                raise ValueError(f"Cannot interpret a valid date from '{args.start_date}'. Error is {e.__class__} {e}")
                            finally:
                                e = None
                                del e

                    if start_date is None:
                        from datetime import date
                        start_date = date.today()
                    print(f"\nDay zero is {start_date.strftime('%A %B %d %Y')}")
                    if start_day != 0:
                        from datetime import timedelta
                        start_day_date = start_date + timedelta(days=start_day)
                        print(f"Starting on day {start_day}, which is {start_day_date.strftime('%A %B %d %Y')}")
                else:
                    start_day_date = start_date
            repository, repository_version = Parameters.get_repository(args.repository)
            print(f"\nUsing MetaWardsData at {repository}")
            print(f"This is cloned from {repository_version['repository']}")
            print(f"branch {repository_version['branch']}, version {repository_version['version']}")
            if repository_version['is_dirty']:
                print('##\xa0WARNING - this repository is dirty, meaning that the data')
                print('## WARNING - has not been committed to git. This may make ')
                print('## WARNING - this calculation very difficult to reproduce')
            args.seed = seed
            args.nprocs = nprocs
            args.nthreads = nthreads
            args.start_date = start_date.isoformat()
            args.repository = repository
            repeat_cmd = 'metawards'
            for key, value in vars(args).items():
                if value is not None:
                    k = key.replace('_', '-')
                    if isinstance(value, bool):
                        if value:
                            repeat_cmd += f" --{k}"
                    else:
                        if isinstance(value, list):
                            repeat_cmd += f" --{k}"
                            for val in value:
                                v = str(val)
                                if ' ' in v:
                                    repeat_cmd += f" '{v}''"
                                else:
                                    repeat_cmd += f" {v}"

                v = str(value)
                if ' ' in v:
                    repeat_cmd += f" --{k} '{v}''"
                else:
                    repeat_cmd += f" --{k} {v}"

            t = '*** To repeat this job use the command ***'
            print('\n' + '*' * len(t))
            print(t)
            print('*' * len(t) + '\n')
            print(repeat_cmd + '\n')
            try:
                params = Parameters.load(parameters=(args.parameters))
            except Exception as e:
                try:
                    print('Unable to load parameter files. Make sure that you have cloned the MetaWardsData repository and have set the environment variable METAWARDSDATA to point to the local directory containing the repository, e.g. the default is $HOME/GitHub/MetaWardsData')
                    raise e
                finally:
                    e = None
                    del e

        profile = False
    if args.no_profile:
        profile = False
    else:
        if args.profile:
            profile = True
        else:
            if args.disease:
                params.set_disease(args.disease)
            else:
                params.set_disease('ncov')
            params.set_input_files(args.input_data)
            if args.user_variables:
                custom = VariableSet.read(args.user_variables)
                print(f"Adjusting variables to {custom}")
                custom.adjust(params)
            elif args.additional is None or len(args.additional) == 0:
                print('Not using any additional seeds...')
            else:
                for additional in args.additional:
                    print(f"Loading additional seeds from {additional}")
                    params.add_seeds(additional)

            params.UV = args.UV
            params.static_play_at_home = 0
            params.play_to_work = 0
            params.work_to_play = 0
            params.daily_imports = 0.0
            population = Population(initial=(args.population), date=start_day_date,
              day=start_day)
            print('\nBuilding the network...')
            network = Network.build(params=params, calculate_distances=True, profile=profile)
            print('\nRun the model...')
            from metawards import OutputFiles
            from metawards.utils import run_models
            outdir = args.output
            if outdir is None:
                outdir = 'output'
            if args.force_overwrite_output:
                prompt = None
            else:
                prompt = input
        auto_bzip = True
    if args.auto_bzip:
        auto_bzip = True
    else:
        if args.no_auto_bzip:
            auto_bzip = False
        else:
            if args.iterator:
                iterator = args.iterator
            else:
                iterator = None
            if args.extractor:
                extractor = args.extractor
            else:
                extractor = None
        with OutputFiles(outdir, force_empty=(args.force_overwrite_output), auto_bzip=auto_bzip,
          prompt=prompt) as (output_dir):
            result = run_models(network=network, variables=variables, population=population,
              nprocs=nprocs,
              nthreads=nthreads,
              seed=seed,
              nsteps=(args.nsteps),
              output_dir=output_dir,
              iterator=iterator,
              extractor=extractor,
              profile=profile,
              parallel_scheme=parallel_scheme)
            if result is None or len(result) == 0:
                print('No output - end of run')
                return 0
            else:
                RESULTS = output_dir.open('results.csv', auto_bzip=auto_bzip)
                print(f"\nWriting a summary of all results into the\ncsv file {output_dir.get_filename('results.csv')}.\nYou can use this to quickly look at statistics across\nall runs using e.g. R or pandas")
                varnames = result[0][0].variable_names()
                if varnames is None or len(varnames) == 0:
                    varnames = ''
                else:
                    varnames = ','.join(varnames) + ','
                has_date = result[0][1][0].date
                if has_date:
                    datestring = 'date,'
                else:
                    datestring = ''
            RESULTS.write(f"fingerprint,repeat,{varnames}day,{datestring}S,E,I,R,IW\n")
            for varset, trajectory in result:
                varvals = varset.variable_values()
                if varvals is None or len(varvals) == 0:
                    varvals = ''
                else:
                    varvals = ','.join(map(str, varvals)) + ','
                start = f"{varset.fingerprint()},{varset.repeat_index()},{varvals}"
                for i, pop in enumerate(trajectory):
                    if pop.date:
                        d = pop.date.isoformat() + ','
                    else:
                        d = ''
                    RESULTS.write(f"{start}{pop.day},{d}{pop.susceptibles},{pop.latent},{pop.total},{pop.recovereds},{pop.n_inf_wards}\n")

        print('End of the run')
        return 0


if __name__ == '__main__':
    cli()
else:
    from metawards.utils import run_worker