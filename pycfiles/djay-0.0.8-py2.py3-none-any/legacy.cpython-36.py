# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-x0nyl_ya/flake8/flake8/api/legacy.py
# Compiled at: 2019-07-30 18:47:04
# Size of source mod 2**32: 6395 bytes
"""Module containing shims around Flake8 2.x behaviour.

Previously, users would import :func:`get_style_guide` from ``flake8.engine``.
In 3.0 we no longer have an "engine" module but we maintain the API from it.
"""
import logging, os.path, flake8
from flake8.formatting import base as formatter
from flake8.main import application as app
LOG = logging.getLogger(__name__)
__all__ = ('get_style_guide', )

def get_style_guide(**kwargs):
    r"""Provision a StyleGuide for use.

    :param \*\*kwargs:
        Keyword arguments that provide some options for the StyleGuide.
    :returns:
        An initialized StyleGuide
    :rtype:
        :class:`StyleGuide`
    """
    application = app.Application()
    application.parse_preliminary_options_and_args([])
    flake8.configure_logging(application.prelim_opts.verbose, application.prelim_opts.output_file)
    application.make_config_finder()
    application.find_plugins()
    application.register_plugin_options()
    application.parse_configuration_and_cli([])
    options = application.options
    for key, value in kwargs.items():
        try:
            getattr(options, key)
            setattr(options, key, value)
        except AttributeError:
            LOG.error('Could not update option "%s"', key)

    application.make_formatter()
    application.make_guide()
    application.make_file_checker_manager()
    return StyleGuide(application)


class StyleGuide(object):
    __doc__ = "Public facing object that mimic's Flake8 2.0's StyleGuide.\n\n    .. note::\n\n        There are important changes in how this object behaves compared to\n        the StyleGuide object provided in Flake8 2.x.\n\n    .. warning::\n\n        This object should not be instantiated directly by users.\n\n    .. versionchanged:: 3.0.0\n    "

    def __init__(self, application):
        """Initialize our StyleGuide."""
        self._application = application
        self._file_checker_manager = application.file_checker_manager

    @property
    def options(self):
        """Return application's options.

        An instance of :class:`optparse.Values` containing parsed options.
        """
        return self._application.options

    @property
    def paths(self):
        """Return the extra arguments passed as paths."""
        return self._application.paths

    def check_files(self, paths=None):
        """Run collected checks on the files provided.

        This will check the files passed in and return a :class:`Report`
        instance.

        :param list paths:
            List of filenames (or paths) to check.
        :returns:
            Object that mimic's Flake8 2.0's Reporter class.
        :rtype:
            flake8.api.legacy.Report
        """
        self._application.run_checks(paths)
        self._application.report_errors()
        return Report(self._application)

    def excluded(self, filename, parent=None):
        """Determine if a file is excluded.

        :param str filename:
            Path to the file to check if it is excluded.
        :param str parent:
            Name of the parent directory containing the file.
        :returns:
            True if the filename is excluded, False otherwise.
        :rtype:
            bool
        """
        return self._file_checker_manager.is_path_excluded(filename) or parent and self._file_checker_manager.is_path_excluded(os.path.join(parent, filename))

    def init_report(self, reporter=None):
        """Set up a formatter for this run of Flake8."""
        if reporter is None:
            return
        if not issubclass(reporter, formatter.BaseFormatter):
            raise ValueError('Report should be subclass of flake8.formatter.BaseFormatter.')
        self._application.formatter = None
        self._application.make_formatter(reporter)
        self._application.guide = None
        self._application.make_guide()
        self._application.file_checker_manager = None
        self._application.make_file_checker_manager()

    def input_file(self, filename, lines=None, expected=None, line_offset=0):
        """Run collected checks on a single file.

        This will check the file passed in and return a :class:`Report`
        instance.

        :param str filename:
            The path to the file to check.
        :param list lines:
            Ignored since Flake8 3.0.
        :param expected:
            Ignored since Flake8 3.0.
        :param int line_offset:
            Ignored since Flake8 3.0.
        :returns:
            Object that mimic's Flake8 2.0's Reporter class.
        :rtype:
            flake8.api.legacy.Report
        """
        return self.check_files([filename])


class Report(object):
    __doc__ = "Public facing object that mimic's Flake8 2.0's API.\n\n    .. note::\n\n        There are important changes in how this object behaves compared to\n        the object provided in Flake8 2.x.\n\n    .. warning::\n\n        This should not be instantiated by users.\n\n    .. versionchanged:: 3.0.0\n    "

    def __init__(self, application):
        """Initialize the Report for the user.

        .. warning:: This should not be instantiated by users.
        """
        self._application = application
        self._style_guide = application.guide
        self._stats = self._style_guide.stats

    @property
    def total_errors(self):
        """Return the total number of errors."""
        return self._application.result_count

    def get_statistics(self, violation):
        """Get the list of occurrences of a violation.

        :returns:
            List of occurrences of a violation formatted as:
            {Count} {Error Code} {Message}, e.g.,
            ``8 E531 Some error message about the error``
        :rtype:
            list
        """
        return ['{} {} {}'.format(s.count, s.error_code, s.message) for s in self._stats.statistics_for(violation)]