# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-x0nyl_ya/flake8/flake8/main/application.py
# Compiled at: 2019-07-30 18:47:04
# Size of source mod 2**32: 15840 bytes
"""Module containing the application logic for Flake8."""
from __future__ import print_function
import logging, optparse, sys, time
from typing import Dict, List, Optional, Set
import flake8
from flake8 import checker
from flake8 import defaults
from flake8 import exceptions
from flake8 import style_guide
from flake8 import utils
from flake8.main import options
from flake8.options import aggregator, config
from flake8.options import manager
from flake8.plugins import manager as plugin_manager
LOG = logging.getLogger(__name__)

class Application(object):
    __doc__ = 'Abstract our application into a class.'

    def __init__(self, program='flake8', version=flake8.__version__):
        """Initialize our application.

        :param str program:
            The name of the program/application that we're executing.
        :param str version:
            The version of the program/application we're executing.
        """
        self.start_time = time.time()
        self.end_time = None
        self.program = program
        self.version = version
        self.option_manager = manager.OptionManager(prog='flake8',
          version=(flake8.__version__))
        options.register_default_options(self.option_manager)
        self.prelim_opts = None
        self.prelim_args = None
        self.config_finder = None
        self.local_plugins = None
        self.check_plugins = None
        self.formatting_plugins = None
        self.formatter = None
        self.guide = None
        self.file_checker_manager = None
        self.options = None
        self.args = None
        self.result_count = 0
        self.total_result_count = 0
        self.catastrophic_failure = False
        self.running_against_diff = False
        self.parsed_diff = {}

    def parse_preliminary_options_and_args(self, argv=None):
        """Get preliminary options and args from CLI, pre-plugin-loading.

        We need to know the values of a few standard options and args now, so
        that we can find config files and configure logging.

        Since plugins aren't loaded yet, there may be some as-yet-unknown
        options; we ignore those for now, they'll be parsed later when we do
        real option parsing.

        Sets self.prelim_opts and self.prelim_args.

        :param list argv:
            Command-line arguments passed in directly.
        """
        args = (argv if argv is not None else sys.argv)[:]
        try:
            args.remove('--version')
        except ValueError:
            pass

        try:
            args.remove('--help')
        except ValueError:
            pass

        try:
            args.remove('-h')
        except ValueError:
            pass

        opts, args = self.option_manager.parse_known_args(args)
        args = [a for a in args[1:] if not a.startswith('-')]
        self.prelim_opts, self.prelim_args = opts, args

    def exit(self):
        """Handle finalization and exiting the program.

        This should be the last thing called on the application instance. It
        will check certain options and exit appropriately.
        """
        if self.options.count:
            print(self.result_count)
        if not self.options.exit_zero:
            raise SystemExit(self.result_count > 0 or self.catastrophic_failure)

    def make_config_finder(self):
        """Make our ConfigFileFinder based on preliminary opts and args."""
        if self.config_finder is None:
            extra_config_files = utils.normalize_paths(self.prelim_opts.append_config)
            self.config_finder = config.ConfigFileFinder(self.option_manager.program_name, self.prelim_args, extra_config_files)

    def find_plugins(self):
        """Find and load the plugins for this application.

        If :attr:`check_plugins`, or :attr:`formatting_plugins` are ``None``
        then this method will update them with the appropriate plugin manager
        instance. Given the expense of finding plugins (via :mod:`entrypoints`)
        we want this to be idempotent and so only update those attributes if
        they are ``None``.
        """
        if self.local_plugins is None:
            self.local_plugins = config.get_local_plugins(self.config_finder, self.prelim_opts.config, self.prelim_opts.isolated)
        else:
            sys.path.extend(self.local_plugins.paths)
            if self.check_plugins is None:
                self.check_plugins = plugin_manager.Checkers(self.local_plugins.extension)
            if self.formatting_plugins is None:
                self.formatting_plugins = plugin_manager.ReportFormatters(self.local_plugins.report)
        self.check_plugins.load_plugins()
        self.formatting_plugins.load_plugins()

    def register_plugin_options(self):
        """Register options provided by plugins to our option manager."""
        self.check_plugins.register_options(self.option_manager)
        self.check_plugins.register_plugin_versions(self.option_manager)
        self.formatting_plugins.register_options(self.option_manager)

    def parse_configuration_and_cli(self, argv=None):
        """Parse configuration files and the CLI options.

        :param list argv:
            Command-line arguments passed in directly.
        """
        if self.options is None:
            if self.args is None:
                self.options, self.args = aggregator.aggregate_options(self.option_manager, self.config_finder, argv)
        self.running_against_diff = self.options.diff
        if self.running_against_diff:
            self.parsed_diff = utils.parse_unified_diff()
            if not self.parsed_diff:
                self.exit()
        self.options._running_from_vcs = False
        self.check_plugins.provide_options(self.option_manager, self.options, self.args)
        self.formatting_plugins.provide_options(self.option_manager, self.options, self.args)

    def formatter_for(self, formatter_plugin_name):
        """Retrieve the formatter class by plugin name."""
        default_formatter = self.formatting_plugins['default']
        formatter_plugin = self.formatting_plugins.get(formatter_plugin_name)
        if formatter_plugin is None:
            LOG.warning('"%s" is an unknown formatter. Falling back to default.', formatter_plugin_name)
            formatter_plugin = default_formatter
        return formatter_plugin.execute

    def make_formatter(self, formatter_class=None):
        """Initialize a formatter based on the parsed options."""
        if self.formatter is None:
            format_plugin = self.options.format
            if 1 <= self.options.quiet < 2:
                format_plugin = 'quiet-filename'
            else:
                if 2 <= self.options.quiet:
                    format_plugin = 'quiet-nothing'
            if formatter_class is None:
                formatter_class = self.formatter_for(format_plugin)
            self.formatter = formatter_class(self.options)

    def make_guide(self):
        """Initialize our StyleGuide."""
        if self.guide is None:
            self.guide = style_guide.StyleGuideManager(self.options, self.formatter)
        if self.running_against_diff:
            self.guide.add_diff_ranges(self.parsed_diff)

    def make_file_checker_manager(self):
        """Initialize our FileChecker Manager."""
        if self.file_checker_manager is None:
            self.file_checker_manager = checker.Manager(style_guide=(self.guide),
              arguments=(self.args),
              checker_plugins=(self.check_plugins))

    def run_checks(self, files=None):
        """Run the actual checks with the FileChecker Manager.

        This method encapsulates the logic to make a
        :class:`~flake8.checker.Manger` instance run the checks it is
        managing.

        :param list files:
            List of filenames to process
        """
        if self.running_against_diff:
            files = sorted(self.parsed_diff)
        self.file_checker_manager.start(files)
        try:
            self.file_checker_manager.run()
        except exceptions.PluginExecutionFailed as plugin_failed:
            print(str(plugin_failed))
            print('Run flake8 with greater verbosity to see more details')
            self.catastrophic_failure = True

        LOG.info('Finished running')
        self.file_checker_manager.stop()
        self.end_time = time.time()

    def report_benchmarks(self):
        """Aggregate, calculate, and report benchmarks for this run."""
        if not self.options.benchmark:
            return
        time_elapsed = self.end_time - self.start_time
        statistics = [('seconds elapsed', time_elapsed)]
        add_statistic = statistics.append
        for statistic in defaults.STATISTIC_NAMES + ('files', ):
            value = self.file_checker_manager.statistics[statistic]
            total_description = 'total ' + statistic + ' processed'
            add_statistic((total_description, value))
            per_second_description = statistic + ' processed per second'
            add_statistic((per_second_description, int(value / time_elapsed)))

        self.formatter.show_benchmarks(statistics)

    def report_errors(self):
        """Report all the errors found by flake8 3.0.

        This also updates the :attr:`result_count` attribute with the total
        number of errors, warnings, and other messages found.
        """
        LOG.info('Reporting errors')
        results = self.file_checker_manager.report()
        self.total_result_count, self.result_count = results
        LOG.info('Found a total of %d violations and reported %d', self.total_result_count, self.result_count)

    def report_statistics(self):
        """Aggregate and report statistics from this run."""
        if not self.options.statistics:
            return
        self.formatter.show_statistics(self.guide.stats)

    def initialize(self, argv):
        """Initialize the application to be run.

        This finds the plugins, registers their options, and parses the
        command-line arguments.
        """
        self.parse_preliminary_options_and_args(argv)
        flake8.configure_logging(self.prelim_opts.verbose, self.prelim_opts.output_file)
        self.make_config_finder()
        self.find_plugins()
        self.register_plugin_options()
        self.parse_configuration_and_cli(argv)
        self.make_formatter()
        self.make_guide()
        self.make_file_checker_manager()

    def report(self):
        """Report errors, statistics, and benchmarks."""
        self.formatter.start()
        self.report_errors()
        self.report_statistics()
        self.report_benchmarks()
        self.formatter.stop()

    def _run(self, argv):
        self.initialize(argv)
        self.run_checks()
        self.report()

    def run(self, argv=None):
        """Run our application.

        This method will also handle KeyboardInterrupt exceptions for the
        entirety of the flake8 application. If it sees a KeyboardInterrupt it
        will forcibly clean up the :class:`~flake8.checker.Manager`.
        """
        try:
            self._run(argv)
        except KeyboardInterrupt as exc:
            print('... stopped')
            LOG.critical('Caught keyboard interrupt from user')
            LOG.exception(exc)
            self.catastrophic_failure = True
        except exceptions.ExecutionError as exc:
            print('There was a critical error during execution of Flake8:')
            print(exc)
            LOG.exception(exc)
            self.catastrophic_failure = True
        except exceptions.EarlyQuit:
            self.catastrophic_failure = True
            print('... stopped while processing files')