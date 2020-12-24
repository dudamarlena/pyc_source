# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jhunk/Downloads/pandokia/pandokia/run.py
# Compiled at: 2018-05-14 14:25:23
# Size of source mod 2**32: 8039 bytes
import sys, getopt, os, os.path, stat, errno, pandokia.common as common
helpstr = '\npdk run [ options ] [ files/directories ]\npdkrun  [ options ] [ files/directories ]\n\nRuns tests and generates a pandokia report file of the results.\n\nfilename\n    If you specify a file name, it runs the test in that file.\n\ndirectoryname\n    If you specify a file name, it searches for files in that\n    directory that look like tests.\n\n    If you do not specify any files/directories, the default\n    command is "pdkrun -r ."\n\n-r / --recursive\n    search subdirectories\n\n--log file\n    write the PDK report log into this file\n\n    Default is "PDK_DEFAULT.LOG."+test_run\n\n--parallel N\n    run up to N tests concurrently ( but it can run at most one\n    test at a time in any single directory )\n\n    Default is 1\n\n--project NAME\n    use NAME for the project name in reports\n\n    Default is "default"\n\n--test_run NAME\n    use NAME for the test_run in reports\n\n    Default is a generated string including the user name and the\n    time to the nearest minute\n\n--host HOST\n    HOST is the value of hostname by defalt, but this flag provides a way to\n    override the system\'s value of hostname.  Alternatively, set PDK_HOST.\n\nDefaults can also be set by environment variables.\n\n\n'

def run(args):
    import pandokia.envgetter
    recursive = False
    environment_already_set = False
    directory = False
    log = os.environ.get('PDK_LOG', None)
    project = os.environ.get('PDK_PROJECT', None)
    test_run = os.environ.get('PDK_TESTRUN', None)
    test_prefix = os.environ.get('PDK_TESTPREFIX', None)
    context = os.environ.get('PDK_CONTEXT', 'default')
    parallel = os.environ.get('PDK_PARALLEL', None)
    tmpdir = os.environ.get('PDK_TMP', None)
    host = os.environ.get('PDK_HOST', None)
    verbose = 0
    dry_run = 0
    if args == []:
        args = [
         '-r', '.']
    opts, args = getopt.gnu_getopt(args, 'rvpsw', [
     'recursive', 'environment_already_set', 'dir', 'log=',
     'project=', 'test_run=', 'test_prefix=',
     'show-command', 'verbose', 'parallel=', 'help', 'context='])
    for opt, optarg in opts:
        if opt == '-r' or opt == '--recursive':
            recursive = True
        elif opt == '--environment_already_set':
            environment_already_set = True
        else:
            if opt == '--dir':
                pass
            else:
                if opt == '--help':
                    print(helpstr)
                    return (0, {})
            if opt == '--log':
                log = optarg
            elif opt == '--test_run':
                test_run = optarg
            elif opt == '--test_prefix':
                test_prefix = optarg
            elif opt == '--project':
                project = optarg
            elif opt == '--context':
                context = optarg
            elif opt == '--verbose' or opt == '-v':
                verbose = 1
            else:
                if opt == '--dry-run':
                    dry_run = 1
                else:
                    if opt == '-' or opt == '--parallel':
                        parallel = str(int(optarg))
                    else:
                        if opt == '--host':
                            host = optarg

    if project is None:
        project = default_project()
    if test_run is None:
        test_run = default_test_run()
    if log is None:
        log = 'PDK_DEFAULT.LOG.' + test_run
    if host is None:
        host = common.gethostname()
    if parallel is not None:
        os.environ['PDK_PARALLEL'] = parallel
    log = os.path.abspath(log)
    os.environ['PDK_LOG'] = log
    os.environ['PDK_PROJECT'] = project
    os.environ['PDK_TESTRUN'] = test_run
    os.environ['PDK_CONTEXT'] = context
    os.environ['PDK_HOST'] = host
    initialized_status_file = 0
    if 'PDK_STATUSFILE' not in os.environ:
        status_file_name = os.getcwd() + '/pdk_statusfile'
        import pandokia.run_status
        if parallel is None:
            n_status_records = 1
        else:
            n_status_records = int(parallel)
        f = pandokia.run_status.init_status(filename=status_file_name,
          n_records=n_status_records)
        if f:
            os.environ['PDK_STATUSFILE'] = os.getcwd() + '/pdk_statusfile'
            initialized_status_file = 1
    if test_prefix is not None:
        os.environ['PDK_TESTPREFIX'] = test_prefix
    if tmpdir is None:
        tmpdir = os.getcwd()
    os.environ['PDK_TMP'] = tmpdir
    envgetter = pandokia.envgetter.EnvGetter(context=context)
    if recursive:
        import pandokia.run_recursive
        was_error, t_stat = pandokia.run_recursive.run(args, envgetter)
    else:
        t_stat = {}
        was_error = 0
        n_things_run = 0
        for x in args:
            try:
                file_stat = os.stat(x)
            except OSError as e:
                print('%s %s' % (x, e))
                continue

            lstat = {}
            if stat.S_ISDIR(file_stat.st_mode):
                import pandokia.run_dir
                n_things_run += 1
                err, lstat = pandokia.run_dir.run(x, envgetter)
            else:
                if stat.S_ISREG(file_stat.st_mode):
                    import pandokia.run_file
                    n_things_run += 1
                    basename = os.path.basename(x)
                    dirname = os.path.dirname(x)
                    if dirname == '':
                        dirname = '.'
                    runner = pandokia.run_file.select_runner(dirname, basename)
                    if runner is not None:
                        err, lstat = pandokia.run_file.run(dirname, basename, envgetter, runner)
                    else:
                        print('no runner for %s' % x)
                        err = 1
                else:
                    lstat = {}
                    err = 0
            was_error |= err
            for y in lstat:
                t_stat[y] = t_stat.get(y, 0) + lstat[y]

    if n_things_run > 1:
        print('')
        print('Summary:')
        common.print_stat_dict(t_stat)
    if initialized_status_file:
        for x in range(0, n_status_records):
            pandokia.run_status.pdkrun_status('', slot=x)

        os.unlink(os.environ['PDK_STATUSFILE'])
    return (was_error, t_stat)


def default_project():
    return 'default'


def default_test_run():
    import datetime
    d = datetime.datetime.now()
    if 'USER' in os.environ:
        user = os.environ['USER']
    else:
        if 'USERNAME' in os.environ:
            user = os.environ['USERNAME']
        else:
            import getpass
            user = getpass.getuser()
    fmt = 'user_' + user + '_%Y-%m-%d-%H-%M-%S'
    d = d.strftime(fmt)
    print('DEFAULT TEST RUN %s' % d)
    return d


def export_environment(args):
    import pandokia.envgetter
    out = sys.stdout
    context = None
    env = {}
    format = 'env'
    opts, args = getopt.getopt(args, 'o:c:f', [
     'output=', 'context=', 'full', 'csh', 'sh'])
    for opt, optarg in opts:
        if opt == '-o' or opt == '-output':
            out = open(optarg, 'w')
        else:
            if opt == '-c' or opt == '--context':
                context = optarg
            else:
                if opt == '-f' or opt == '--full':
                    env = os.environ
                else:
                    if opt == '--csh' or opt == '--sh':
                        format = opt[2:]

    if len(args) == 0:
        args = [
         '.']
    for x in args:
        envgetter = pandokia.envgetter.EnvGetter(context=context, defdict=env)
        x = os.path.abspath(x)
        envgetter.envdir(x)
        envgetter.export(x, format=format, fh=out)

    out.flush()