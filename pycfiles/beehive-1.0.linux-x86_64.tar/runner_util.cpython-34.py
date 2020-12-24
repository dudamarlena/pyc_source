# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.4/site-packages/beehive/runner_util.py
# Compiled at: 2014-11-03 05:47:13
# Size of source mod 2**32: 14242 bytes
"""
Contains utility functions and classes for Runners.
"""
from beehive import parser
from beehive.compat import basestring
from beehive.model import FileLocation
from bisect import bisect
import glob, os.path, re, sys

class FileNotFoundError(LookupError):
    pass


class InvalidFileLocationError(LookupError):
    pass


class InvalidFilenameError(ValueError):
    pass


class FileLocationParser:
    pattern = re.compile('^\\s*(?P<filename>.*):(?P<line>\\d+)\\s*$', re.UNICODE)

    @classmethod
    def parse(cls, text):
        match = cls.pattern.match(text)
        if match:
            filename = match.group('filename').strip()
            line = int(match.group('line'))
            return FileLocation(filename, line)
        else:
            filename = text.strip()
            return FileLocation(filename)


class FeatureScenarioLocationCollector(object):
    __doc__ = '\n    Collects FileLocation objects for a feature.\n    This is used to select a subset of scenarios in a feature that should run.\n\n    USE CASE:\n        beehive feature/foo.feature:10\n        beehive @selected_features.txt\n        beehive @rerun_failed_scenarios.txt\n\n    With features configuration files, like:\n\n        # -- file:rerun_failed_scenarios.txt\n        feature/foo.feature:10\n        feature/foo.feature:25\n        feature/bar.feature\n        # -- EOF\n\n    '

    def __init__(self, feature=None, location=None, filename=None):
        if not filename:
            if location:
                filename = location.filename
        self.feature = feature
        self.filename = filename
        self.use_all_scenarios = False
        self.scenario_lines = set()
        self.all_scenarios = set()
        self.selected_scenarios = set()
        if location:
            self.add_location(location)

    def clear(self):
        self.feature = None
        self.filename = None
        self.use_all_scenarios = False
        self.scenario_lines = set()
        self.all_scenarios = set()
        self.selected_scenarios = set()

    def add_location(self, location):
        if not self.filename:
            self.filename = location.filename
        assert self.filename == location.filename, '%s <=> %s' % (self.filename, location.filename)
        if location.line:
            self.scenario_lines.add(location.line)
        else:
            self.use_all_scenarios = True

    @staticmethod
    def select_scenario_line_for(line, scenario_lines):
        """
        Select scenario line for any given line.

        ALGORITHM: scenario.line <= line < next_scenario.line

        :param line:  A line number in the file (as number).
        :param scenario_lines: Sorted list of scenario lines.
        :return: Scenario.line (first line) for the given line.
        """
        if not scenario_lines:
            return 0
        pos = bisect(scenario_lines, line) - 1
        if pos < 0:
            pos = 0
        return scenario_lines[pos]

    def discover_selected_scenarios(self, strict=False):
        """
        Discovers selected scenarios based on the provided file locations.
        In addition:
          * discover all scenarios
          * auto-correct BAD LINE-NUMBERS

        :param strict:  If true, raises exception if file location is invalid.
        :return: List of selected scenarios of this feature (as set).
        :raises InvalidFileLocationError:
            If file location is no exactly correct and strict is true.
        """
        assert self.feature
        if not self.all_scenarios:
            self.all_scenarios = self.feature.walk_scenarios()
        existing_lines = [scenario.line for scenario in self.all_scenarios]
        selected_lines = list(self.scenario_lines)
        for line in selected_lines:
            new_line = self.select_scenario_line_for(line, existing_lines)
            if new_line != line:
                self.scenario_lines.remove(line)
                self.scenario_lines.add(new_line)
                if strict:
                    msg = "Scenario location '...:%d' should be: '%s:%d'" % (
                     line, self.filename, new_line)
                    raise InvalidFileLocationError(msg)
                else:
                    continue

        scenario_lines = set(self.scenario_lines)
        selected_scenarios = set()
        for scenario in self.all_scenarios:
            if scenario.line in scenario_lines:
                selected_scenarios.add(scenario)
                scenario_lines.remove(scenario.line)
                continue

        assert not scenario_lines
        return selected_scenarios

    def build_feature(self):
        """
        Determines which scenarios in the feature are selected and marks the
        remaining scenarios as skipped. Scenarios with the following tags
        are excluded from skipped-marking:

          * @setup
          * @teardown

        If no file locations are stored, the unmodified feature is returned.

        :return: Feature object to use.
        """
        use_all_scenarios = not self.scenario_lines or self.use_all_scenarios
        if not self.feature or use_all_scenarios:
            return self.feature
        self.all_scenarios = self.feature.walk_scenarios()
        self.selected_scenarios = self.discover_selected_scenarios()
        unselected_scenarios = set(self.all_scenarios) - self.selected_scenarios
        for scenario in unselected_scenarios:
            if not 'setup' in scenario.tags:
                if 'teardown' in scenario.tags:
                    continue
                scenario.mark_skipped()

        return self.feature


class FeatureListParser(object):
    __doc__ = "\n    Read textual file, ala '@features.txt'. This file contains:\n\n      * a feature filename or FileLocation on each line\n      * empty lines (skipped)\n      * comment lines (skipped)\n      * wildcards are expanded to select 0..N filenames or directories\n\n    Relative path names are evaluated relative to the listfile directory.\n    A leading '@' (AT) character is removed from the listfile name.\n    "

    @staticmethod
    def parse(text, here=None):
        """
        Parse contents of a features list file as text.

        :param text: Contents of a features list(file).
        :param here: Current working directory to use (optional).
        :return: List of FileLocation objects
        """
        locations = []
        for line in text.splitlines():
            filename = line.strip()
            if not filename:
                continue
            else:
                if filename.startswith('#'):
                    continue
                if here:
                    if not os.path.isabs(filename):
                        filename = os.path.join(here, line)
            filename = os.path.normpath(filename)
            if glob.has_magic(filename):
                for filename2 in glob.iglob(filename):
                    location = FileLocationParser.parse(filename2)
                    locations.append(location)

            else:
                location = FileLocationParser.parse(filename)
                locations.append(location)

        return locations

    @classmethod
    def parse_file(cls, filename):
        """
        Read textual file, ala '@features.txt'.

        :param filename:  Name of feature list file.
        :return: List of feature file locations.
        """
        if filename.startswith('@'):
            filename = filename[1:]
        if not os.path.isfile(filename):
            raise FileNotFoundError(filename)
        here = os.path.dirname(filename) or '.'
        contents = open(filename).read()
        return cls.parse(contents, here)


def parse_features(feature_files, language=None):
    """
    Parse feature files and return list of Feature model objects.
    Handles:

      * feature file names, ala "alice.feature"
      * feature file locations, ala: "alice.feature:10"

    :param feature_files: List of feature file names to parse.
    :param language:      Default language to use.
    :return: List of feature objects.
    """
    scenario_collector = FeatureScenarioLocationCollector()
    features = []
    for location in feature_files:
        if not isinstance(location, FileLocation):
            assert isinstance(location, basestring)
            location = FileLocation(os.path.normpath(location))
        if location.filename == scenario_collector.filename:
            scenario_collector.add_location(location)
            continue
        else:
            if scenario_collector.feature:
                current_feature = scenario_collector.build_feature()
                features.append(current_feature)
                scenario_collector.clear()
            if not isinstance(location, FileLocation):
                raise AssertionError
        filename = os.path.abspath(location.filename)
        feature = parser.parse_file(filename, language=language)
        if feature:
            scenario_collector.feature = feature
            scenario_collector.add_location(location)
            continue

    if scenario_collector.feature:
        current_feature = scenario_collector.build_feature()
        features.append(current_feature)
    return features


def collect_feature_locations(paths, strict=True):
    """
    Collect feature file names by processing list of paths (from command line).
    A path can be a:

      * filename (ending with ".feature")
      * location, ala "{filename}:{line_number}"
      * features configuration filename, ala "@features.txt"
      * directory, to discover and collect all "*.feature" files below.

    :param paths:  Paths to process.
    :return: Feature file locations to use (as list of FileLocations).
    """
    locations = []
    for path in paths:
        if os.path.isdir(path):
            for dirpath, dirnames, filenames in os.walk(path):
                dirnames.sort()
                for filename in sorted(filenames):
                    if filename.endswith('.feature'):
                        location = FileLocation(os.path.join(dirpath, filename))
                        locations.append(location)
                        continue

        elif path.startswith('@'):
            locations.extend(FeatureListParser.parse_file(path[1:]))
        else:
            location = FileLocationParser.parse(path)
            if not location.filename.endswith('.feature'):
                raise InvalidFilenameError(location.filename)
            elif location.exists():
                locations.append(location)
            elif strict:
                raise FileNotFoundError(path)
                continue

    return locations


def make_undefined_step_snippet(step, language=None):
    """
    Helper function to create an undefined-step snippet for a step.

    :param step: Step to use (as Step object or step text).
    :param language: i18n language, optionally needed for step text parsing.
    :return: Undefined-step snippet (as string).
    """
    if isinstance(step, basestring):
        step_text = step
        steps = parser.parse_steps(step_text, language=language)
        step = steps[0]
        assert step, 'ParseError: %s' % step_text
    prefix = 'u'
    single_quote = "'"
    if single_quote in step.name:
        step.name = step.name.replace(single_quote, "\\'")
    schema = "@%s(%s'%s')\ndef step_impl(context):\n    assert False\n\n"
    snippet = schema % (step.step_type, prefix, step.name)
    return snippet


def print_undefined_step_snippets(undefined_steps, stream=None, colored=True):
    """
    Print snippets for the undefined steps that were discovered.

    :param undefined_steps:  List of undefined steps (as list<string>).
    :param stream:      Output stream to use (default: sys.stderr).
    :param colored:     Indicates if coloring should be used (default: True)
    """
    if not undefined_steps:
        return
    if not stream:
        stream = sys.stderr
    msg = '\nYou can implement step definitions for undefined steps with '
    msg += 'these snippets:\n\n'
    printed = set()
    for step in undefined_steps:
        if step in printed:
            continue
        printed.add(step)
        msg += make_undefined_step_snippet(step)

    if colored:
        from beehive.formatter.ansi_escapes import escapes
        msg = escapes['undefined'] + msg + escapes['reset']
    stream.write(msg)
    stream.flush()