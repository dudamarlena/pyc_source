# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/idapload/main.py
# Compiled at: 2020-04-15 05:34:04
# Size of source mod 2**32: 10831 bytes
import inspect, logging, os, importlib, signal, socket, sys, time, gevent, idapload
from .event import Events
from .argument_parser import parse_idaploadfile_option, parse_options
from .core import HttpLocust, Locust
from .env import Environment
from .inspectidapload import get_task_ratio_dict, print_task_ratio
from .log import console_logger, setup_logging
from .runners import LocalLocustRunner, MasterLocustRunner, SlaveLocustRunner
from .stats import print_error_report, print_percentile_stats, print_stats, stats_printer, stats_writer, write_stat_csvs
from util.timespan import parse_timespan
from .web import WebUI
_internals = [
 Locust, HttpLocust]
version = idapload.__version__

def is_idapload(tup):
    """
    Takes (name, object) tuple, returns True if it's a public Locust subclass.
    """
    name, item = tup
    return bool(inspect.isclass(item) and issubclass(item, Locust) and hasattr(item, 'task_set') and getattr(item, 'task_set') and not name.startswith('_'))


def load_idaploadfile(path):
    """
    Import given idaploadfile path and return (docstring, callables).

    Specifically, the idaploadfile's ``__doc__`` attribute (a string) and a
    dictionary of ``{'name': callable}`` containing all callables which pass
    the "is a Locust" test.
    """

    def __import_idaploadfile__(filename, path):
        source = importlib.machinery.SourceFileLoader(os.path.splitext(idaploadfile)[0], path)
        return source.load_module()

    sys.path.insert(0, os.getcwd())
    directory, idaploadfile = os.path.split(path)
    added_to_path = False
    index = None
    if directory not in sys.path:
        sys.path.insert(0, directory)
        added_to_path = True
    else:
        i = sys.path.index(directory)
        if i != 0:
            index = i
            sys.path.insert(0, directory)
            del sys.path[i + 1]
    imported = __import_idaploadfile__(idaploadfile, path)
    if added_to_path:
        del sys.path[0]
    if index is not None:
        sys.path.insert(index + 1, directory)
        del sys.path[0]
    idaploads = dict(filter(is_idapload, vars(imported).items()))
    return (imported.__doc__, idaploads)


def create_environment(options, events=None):
    """
    Create an Environment instance from options
    """
    return Environment(events=events,
      host=(options.host),
      options=options,
      reset_stats=(options.reset_stats),
      step_load=(options.step_load),
      stop_timeout=(options.stop_timeout))


def main():
    idaploadfile = parse_idaploadfile_option()
    docstring, idaploads = load_idaploadfile(idaploadfile)
    options = parse_options()
    if not options.skip_log_setup:
        setup_logging(options.loglevel, options.logfile)
    logger = logging.getLogger(__name__)
    if options.list_commands:
        console_logger.info('Available Locusts:')
        for name in idaploads:
            console_logger.info('    ' + name)

        sys.exit(0)
    else:
        if not idaploads:
            logger.error('No Locust class found!')
            sys.exit(1)
        if options.idapload_classes:
            missing = set(options.idapload_classes) - set(idaploads.keys())
            if missing:
                logger.error('Unknown Locust(s): %s\n' % ', '.join(missing))
                sys.exit(1)
            else:
                names = set(options.idapload_classes) & set(idaploads.keys())
                idapload_classes = [idaploads[n] for n in names]
        else:
            idapload_classes = list(idaploads.values())
    environment = create_environment(options, events=(idapload.events))
    if options.show_task_ratio:
        console_logger.info('\n Task ratio per idapload class')
        console_logger.info('--------------------------------------------------------------------------------')
        print_task_ratio(idapload_classes)
        console_logger.info('\n Total task ratio')
        console_logger.info('--------------------------------------------------------------------------------')
        print_task_ratio(idapload_classes, total=True)
        sys.exit(0)
    if options.show_task_ratio_json:
        from json import dumps
        task_data = {'per_class':get_task_ratio_dict(idapload_classes),  'total':get_task_ratio_dict(idapload_classes, total=True)}
        console_logger.info(dumps(task_data))
        sys.exit(0)
    elif options.step_time:
        if not options.step_load:
            logger.error('The --step-time argument can only be used together with --step-load')
            sys.exit(1)
        if options.slave:
            logger.error('--step-time should be specified on the master node, and not on slave nodes')
            sys.exit(1)
        try:
            options.step_time = parse_timespan(options.step_time)
        except ValueError:
            logger.error('Valid --step-time formats are: 20, 20s, 3m, 2h, 1h20m, 3h30m10s, etc.')
            sys.exit(1)

        if options.master:
            runner = MasterLocustRunner(environment,
              idapload_classes,
              master_bind_host=(options.master_bind_host),
              master_bind_port=(options.master_bind_port))
    elif options.slave:
        try:
            runner = SlaveLocustRunner(environment,
              idapload_classes,
              master_host=(options.master_host),
              master_port=(options.master_port))
        except socket.error as e:
            try:
                logger.error('Failed to connect to the Locust master: %s', e)
                sys.exit(-1)
            finally:
                e = None
                del e

    else:
        runner = LocalLocustRunner(environment, idapload_classes)
    main_greenlet = runner.greenlet
    if options.run_time:
        if not options.no_web:
            logger.error('The --run-time argument can only be used together with --no-web')
            sys.exit(1)
        else:
            if options.slave:
                logger.error('--run-time should be specified on the master node, and not on slave nodes')
                sys.exit(1)
            try:
                options.run_time = parse_timespan(options.run_time)
            except ValueError:
                logger.error('Valid --run-time formats are: 20, 20s, 3m, 2h, 1h20m, 3h30m10s, etc.')
                sys.exit(1)

        def spawn_run_time_limit_greenlet():
            logger.info('Run time limit set to %s seconds' % options.run_time)

            def timelimit_stop():
                logger.info('Time limit reached. Stopping Locust.')
                runner.quit()

            gevent.spawn_later(options.run_time, timelimit_stop)

    elif not options.no_web:
        if not options.slave:
            logger.info('Starting web monitor at http://%s:%s' % (options.web_host or '*', options.web_port))
            web_ui = WebUI(environment=environment)
            main_greenlet = gevent.spawn((web_ui.start), host=(options.web_host), port=(options.web_port))
        else:
            web_ui = None
        environment.events.init.fire(environment=environment, runner=runner, web_ui=web_ui)
        if options.no_web:
            if options.master:
                while len(runner.clients.ready) < options.expect_slaves:
                    logging.info('Waiting for slaves to be ready, %s of %s connected', len(runner.clients.ready), options.expect_slaves)
                    time.sleep(1)

            if not options.slave:
                if options.step_time:
                    runner.start_stepload(options.num_clients, options.hatch_rate, options.step_clients, options.step_time)
    else:
        runner.start(options.num_clients, options.hatch_rate)
    if options.run_time:
        spawn_run_time_limit_greenlet()
    stats_printer_greenlet = None
    if not options.only_summary:
        if not options.print_stats:
            if options.no_web:
                if not options.slave:
                    stats_printer_greenlet = gevent.spawn(stats_printer(runner.stats))
    if options.csvfilebase:
        gevent.spawn(stats_writer, runner.stats, options.csvfilebase, options.stats_history_enabled)

    def shutdown(code=0):
        """
        Shut down idapload by firing quitting event, printing/writing stats and exiting
        """
        logger.info('Shutting down (exit code %s), bye.' % code)
        if stats_printer_greenlet is not None:
            stats_printer_greenlet.kill(block=False)
        logger.info('Cleaning up runner...')
        if runner is not None:
            runner.quit()
        logger.info('Running teardowns...')
        environment.events.quitting.fire(reverse=True)
        print_stats((runner.stats), current=False)
        print_percentile_stats(runner.stats)
        if options.csvfilebase:
            write_stat_csvs(runner.stats, options.csvfilebase, options.stats_history_enabled)
        print_error_report(runner.stats)
        sys.exit(code)

    def sig_term_handler():
        logger.info('Got SIGTERM signal')
        shutdown(0)

    gevent.signal(signal.SIGTERM, sig_term_handler)
    try:
        logger.info('Starting Locust %s' % version)
        main_greenlet.join()
        code = 0
        if len(runner.errors) or len(runner.exceptions):
            code = options.exit_code_on_error
        shutdown(code=code)
    except KeyboardInterrupt as e:
        try:
            shutdown(0)
        finally:
            e = None
            del e