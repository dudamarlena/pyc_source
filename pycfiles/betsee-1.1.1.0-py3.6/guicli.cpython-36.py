# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/betsee/cli/guicli.py
# Compiled at: 2019-08-01 01:03:54
# Size of source mod 2**32: 9856 bytes
"""
Concrete subclasses defining this application's command line interface (CLI).
"""
from betse.util.app.meta import appmetaone
from betse.util.cli.cliabc import CLIABC
from betse.util.cli.cliopt import CLIOptionArgEnum, CLIOptionArgStr
from betse.util.io.log import logs
from betse.util.type.types import type_check, SequenceTypes
from betsee.lib.pyside2.cache.guipsdcache import CachePolicy

class BetseeCLI(CLIABC):
    __doc__ = "\n    Command line interface (CLI) for this application.\n\n    Attributes\n    ----------\n    _cache_policy : CachePolicy\n        Type of :mod:`PySide2`-based submodule caching to be performed.\n    _sim_conf_filename : StrOrNoneTypes\n        Absolute or relative filename of the initial YAML-formatted simulation\n        configuration file to be initially opened by this application's GUI if\n        any *or* ``None`` otherwise. This filename is parsed from command-line\n        options passed by the current user.\n    "

    def __init__(self):
        super().__init__()
        self._cache_policy = None
        self._sim_conf_filename = None

    @property
    def _help_epilog(self) -> str:
        return '\nTo simulate any simulation produced by this GUI at the command line, consider\nrunning the "betse" command underlying this GUI instead. For example, to\nseed, initialize, and then simulate such a simulation in the current directory:\n\n;    betse seed sim_config.yaml\n;    betse init sim_config.yaml\n;    betse  sim sim_config.yaml\n'

    @property
    def _options_top(self):
        options_top = super()._options_top
        return options_top + [
         CLIOptionArgEnum(long_name='--cache-policy',
           synopsis='type of caching to perform (defaults to "{default}"):\n;* "auto", deferring to "dev" or "user" as needed\n;* "dev", caching developer- and user-specific files\n;* "user", caching only user-specific files',
           enum_type=CachePolicy,
           enum_default=(CachePolicy.AUTO)),
         CLIOptionArgStr(long_name='--sim-conf-file',
           synopsis='simulation configuration file to initially open',
           var_name='sim_conf_filename',
           default_value=None)]

    def _parse_options_top(self):
        super()._parse_options_top()
        self._cache_policy = CachePolicy[self._args.cache_policy.upper()]
        self._sim_conf_filename = self._args.sim_conf_filename

    @property
    def _matplotlib_backend_name_forced(self) -> bool:
        """
        Name of the headless Qt-based matplotlib backend, preventing this CLI
        from exposing the ``--matplotlib-backend`` option and hence permitting
        users to externally specify an arbitrary matplotlib backend at the
        command line.

        Of necessity, this Qt-based application strictly requires a single
        Qt-based matplotlib backend (e.g., ``Qt5Agg``).
        """
        return 'Qt5Agg'

    def _init_app_libs(self) -> None:
        appmetaone.get_app_meta().init_libs(cache_policy=(self._cache_policy))

    def _do(self) -> object:
        """
        Implement this command-line interface (CLI) by unconditionally running
        this application's graphical user interface (GUI), returning this
        interface to be memory profiled when the ``--profile-type=size`` CLI
        option is passed.
        """
        from betsee.gui.guimain import BetseeGUI
        app_gui = BetseeGUI(sim_conf_filename=(self._sim_conf_filename))
        self._exit_status = app_gui.run()
        return app_gui

    @type_check
    def _handle_exception(self, exception):
        super()._handle_exception(exception)
        try:
            from betsee.util.io import guierror
            guierror.show_exception(exception)
        except ImportError as import_error:
            logs.log_error(str(import_error))