# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.4/site-packages/beehive/formatter/rerun.py
# Compiled at: 2014-10-30 09:03:06
# Size of source mod 2**32: 3983 bytes
"""
Provides a formatter that simplifies to rerun the failing scenarios
of the last test run. It writes a text file with the file locations of
the failing scenarios, like:

    # -- file:rerun.features
    # RERUN: Failing scenarios during last test run.
    features/alice.feature:10
    features/alice.feature:42
    features/bob.feature:67

To rerun the failing scenarios, use:

    beehive @rerun_failing.features

Normally, you put the RerunFormatter into the beehive configuration file:

    # -- file:beehive.ini
    [beehive]
    format   = rerun
    outfiles = rerun_failing.features
"""
from beehive.formatter.base import Formatter
from datetime import datetime
import os

class RerunFormatter(Formatter):
    __doc__ = '\n    Provides formatter class that emits a summary which scenarios failed\n    during the last test run. This output can be used to rerun the tests\n    with the failed scenarios.\n    '
    name = 'rerun'
    description = 'Emits scenario file locations of failing scenarios'
    show_timestamp = False
    show_failed_scenarios_descriptions = False

    def __init__(self, stream_opener, config):
        super(RerunFormatter, self).__init__(stream_opener, config)
        self.failed_scenarios = []
        self.current_feature = None

    def reset(self):
        self.failed_scenarios = []
        self.current_feature = None

    def feature(self, feature):
        self.current_feature = feature

    def eof(self):
        """Called at end of a feature."""
        if self.current_feature:
            if self.current_feature.status == 'failed':
                for scenario in self.current_feature.walk_scenarios():
                    if scenario.status == 'failed':
                        self.failed_scenarios.append(scenario)
                        continue

        self.current_feature = None
        assert self.current_feature is None

    def close(self):
        """Called at end of test run."""
        stream_name = self.stream_opener.name
        if self.failed_scenarios:
            self.stream = self.open()
            self.report_scenario_failures()
        elif stream_name:
            if os.path.exists(stream_name):
                os.remove(self.stream_opener.name)
        self.close_stream()

    def report_scenario_failures(self):
        assert self.failed_scenarios
        message = '# -- RERUN: %d failing scenarios during last test run.\n'
        self.stream.write(message % len(self.failed_scenarios))
        if self.show_timestamp:
            now = datetime.now().replace(microsecond=0)
            self.stream.write('# NOW: %s\n' % now.isoformat(' '))
        if self.show_failed_scenarios_descriptions:
            current_feature = None
            for index, scenario in enumerate(self.failed_scenarios):
                if current_feature != scenario.filename:
                    if current_feature is not None:
                        self.stream.write('#\n')
                    current_feature = scenario.filename
                    short_filename = os.path.relpath(scenario.filename, os.getcwd())
                    self.stream.write('# %s\n' % short_filename)
                self.stream.write('#  %4d:  %s\n' % (
                 scenario.line, scenario.name))

            self.stream.write('\n')
        for scenario in self.failed_scenarios:
            self.stream.write('%s\n' % scenario.location)

        self.stream.write('\n')