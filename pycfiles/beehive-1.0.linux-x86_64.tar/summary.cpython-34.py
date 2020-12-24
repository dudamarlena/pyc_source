# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.4/site-packages/beehive/reporter/summary.py
# Compiled at: 2014-10-31 12:44:01
# Size of source mod 2**32: 3234 bytes
"""
Provides a summary after each test run.
"""
import sys
from beehive.model import ScenarioOutline
from beehive.reporter.base import Reporter
optional_steps = ('untested', )

def format_summary(statement_type, summary):
    parts = []
    for status in ('passed', 'failed', 'skipped', 'undefined', 'untested'):
        if status not in summary:
            continue
        counts = summary[status]
        if status in optional_steps:
            if counts == 0:
                continue
            if not parts:
                label = statement_type
                if counts != 1:
                    label += 's'
                part = '%d %s %s' % (counts, label, status)
            else:
                part = '%d %s' % (counts, status)
            parts.append(part)

    return ', '.join(parts) + '\n'


class SummaryReporter(Reporter):
    show_failed_scenarios = True
    output_stream_name = 'stdout'

    def __init__(self, config):
        super(SummaryReporter, self).__init__(config)
        self.stream = getattr(sys, self.output_stream_name, sys.stderr)
        self.feature_summary = {'passed': 0,  'failed': 0,  'skipped': 0,  'untested': 0}
        self.scenario_summary = {'passed': 0,  'failed': 0,  'skipped': 0,  'untested': 0}
        self.step_summary = {'passed': 0,  'failed': 0,  'skipped': 0,  'undefined': 0, 
         'untested': 0}
        self.duration = 0.0
        self.failed_scenarios = []

    def feature(self, feature):
        self.feature_summary[(feature.status or 'skipped')] += 1
        self.duration += feature.duration
        for scenario in feature:
            if isinstance(scenario, ScenarioOutline):
                self.process_scenario_outline(scenario)
            else:
                self.process_scenario(scenario)

    def end(self):
        if self.show_failed_scenarios:
            if self.failed_scenarios:
                self.stream.write('\nFailing scenarios:\n')
                for scenario in self.failed_scenarios:
                    self.stream.write('  %s  %s\n' % (
                     scenario.location, scenario.name))

                self.stream.write('\n')
        self.stream.write(format_summary('feature', self.feature_summary))
        self.stream.write(format_summary('scenario', self.scenario_summary))
        self.stream.write(format_summary('step', self.step_summary))
        timings = (int(self.duration / 60), self.duration % 60)
        self.stream.write('Took %dm%02.3fs\n' % timings)

    def process_scenario(self, scenario):
        if scenario.status == 'failed':
            self.failed_scenarios.append(scenario)
        self.scenario_summary[(scenario.status or 'skipped')] += 1
        for step in scenario:
            self.step_summary[(step.status or 'skipped')] += 1

    def process_scenario_outline(self, scenario_outline):
        for scenario in scenario_outline.scenarios:
            self.process_scenario(scenario)