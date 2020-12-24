# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.4/site-packages/beehive/model.py
# Compiled at: 2014-11-03 07:16:44
# Size of source mod 2**32: 61272 bytes
from __future__ import with_statement
import copy, difflib, itertools, os.path, sys, time, traceback
from beehive.compat import unicode, basestring
from beehive import step_registry

class Argument(object):
    __doc__ = 'An argument found in a *feature file* step name and extracted using\n    step decorator `parameters`_.\n\n    The attributes are:\n\n    .. attribute:: original\n\n       The actual text matched in the step name.\n\n    .. attribute:: value\n\n       The potentially type-converted value of the argument.\n\n    .. attribute:: name\n\n       The name of the argument. This will be None if the parameter is\n       anonymous.\n\n    .. attribute:: start\n\n       The start index in the step name of the argument. Used for display.\n\n    .. attribute:: end\n\n       The end index in the step name of the argument. Used for display.\n    '

    def __init__(self, start, end, original, value, name=None):
        self.start = start
        self.end = end
        self.original = original
        self.value = value
        self.name = name


class FileLocation(object):
    __doc__ = '\n    Provides a value object for file location objects.\n    A file location consists of:\n\n      * filename\n      * line (number), optional\n\n    LOCATION SCHEMA:\n      * "{filename}:{line}" or\n      * "{filename}" (if line number is not present)\n    '
    __pychecker__ = 'missingattrs=line'

    def __init__(self, filename, line=None):
        self.filename = filename
        self.line = line

    def get(self):
        return self.filename

    def abspath(self):
        return os.path.abspath(self.filename)

    def basename(self):
        return os.path.basename(self.filename)

    def dirname(self):
        return os.path.dirname(self.filename)

    def relpath(self, start=os.curdir):
        """
        Compute relative path for start to filename.

        :param start: Base path or start directory (default=current dir).
        :return: Relative path from start to filename
        """
        return os.path.relpath(self.filename, start)

    def exists(self):
        return os.path.exists(self.filename)

    def __eq__(self, other):
        if isinstance(other, FileLocation):
            return self.filename == other.filename and self.line == other.line
        if isinstance(other, basestring):
            return self.filename == other
        raise AttributeError('Cannot compare FileLocation with %s:%s' % (
         type(other), other))

    def __ne__(self, other):
        return not self == other

    def __lt__(self, other):
        if isinstance(other, FileLocation):
            if self.filename < other.filename:
                return True
            else:
                if self.filename > other.filename:
                    return False
                assert self.filename == other.filename
                if self.line is None:
                    self.line = -float('inf')
                if other.line is None:
                    other.line = -float('inf')
                return self.line < other.line
        else:
            if isinstance(other, basestring):
                return self.filename < other
            raise AttributeError('Cannot compare FileLocation with %s:%s' % (
             type(other), other))

    def __le__(self, other):
        return not other < self

    def __gt__(self, other):
        if isinstance(other, FileLocation):
            return other < self
        else:
            return self.filename > other

    def __ge__(self, other):
        return not self < other

    def __repr__(self):
        return '<FileLocation: filename="%s", line=%s>' % (
         self.filename, self.line)

    def __str__(self):
        if self.line is None:
            return self.filename
        return '%s:%s' % (self.filename, self.line)


class BasicStatement(object):

    def __init__(self, filename, line, keyword, name):
        filename = filename or '<string>'
        filename = os.path.relpath(filename, os.getcwd())
        self.location = FileLocation(filename, line)
        assert isinstance(keyword, unicode)
        assert isinstance(name, unicode)
        self.keyword = keyword
        self.name = name

    @property
    def filename(self):
        return self.location.filename

    @property
    def line(self):
        return self.location.line

    def __cmp__(self, other):
        if sys.version_info[0] == '3':

            def cmp(a, b):
                return (a > b) - (a < b)

        return cmp((self.keyword, self.name), (other.keyword, other.name))


class TagStatement(BasicStatement):

    def __init__(self, filename, line, keyword, name, tags):
        super(TagStatement, self).__init__(filename, line, keyword, name)
        self.tags = tags


class TagAndStatusStatement(BasicStatement):
    final_status = ('passed', 'failed', 'skipped')

    def __init__(self, filename, line, keyword, name, tags):
        super(TagAndStatusStatement, self).__init__(filename, line, keyword, name)
        self.tags = tags
        self.should_skip = False
        self._cached_status = None

    @property
    def status(self):
        if self._cached_status not in self.final_status:
            self._cached_status = self.compute_status()
        return self._cached_status

    def reset(self):
        self.should_skip = False
        self._cached_status = None

    def compute_status(self):
        raise NotImplementedError


class Replayable(object):
    type = None

    def replay(self, formatter):
        getattr(formatter, self.type)(self)


class Feature(TagAndStatusStatement, Replayable):
    __doc__ = 'A `feature`_ parsed from a *feature file*.\n\n    The attributes are:\n\n    .. attribute:: keyword\n\n       This is the keyword as seen in the *feature file*. In English this will\n       be "Feature".\n\n    .. attribute:: name\n\n       The name of the feature (the text after "Feature".)\n\n    .. attribute:: description\n\n       The description of the feature as seen in the *feature file*. This is\n       stored as a list of text lines.\n\n    .. attribute:: background\n\n       The :class:`~beehive.model.Background` for this feature, if any.\n\n    .. attribute:: scenarios\n\n       A list of :class:`~beehive.model.Scenario` making up this feature.\n\n    .. attribute:: tags\n\n       A list of @tags (as :class:`~beehive.model.Tag` which are basically\n       glorified strings) attached to the feature.\n       See :ref:`controlling things with tags`.\n\n    .. attribute:: status\n\n       Read-Only. A summary status of the feature\'s run. If read before the\n       feature is fully tested it will return "untested" otherwise it will\n       return one of:\n\n       "untested"\n         The feature was has not been completely tested yet.\n       "skipped"\n         One or more steps of this feature was passed over during testing.\n       "passed"\n         The feature was tested successfully.\n       "failed"\n         One or more steps of this feature failed.\n\n    .. attribute:: duration\n\n       The time, in seconds, that it took to test this feature. If read before\n       the feature is tested it will return 0.0.\n\n    .. attribute:: filename\n\n       The file name (or "<string>") of the *feature file* where the feature\n       was found.\n\n    .. attribute:: line\n\n       The line number of the *feature file* where the feature was found.\n\n    .. _`feature`: gherkin.html#features\n    '
    type = 'feature'

    def __init__(self, filename, line, keyword, name, tags=None, description=None, scenarios=None, background=None):
        tags = tags or []
        super(Feature, self).__init__(filename, line, keyword, name, tags)
        self.description = description or []
        self.scenarios = []
        self.background = background
        self.parser = None
        if scenarios:
            for scenario in scenarios:
                self.add_scenario(scenario)

    def reset(self):
        """
        Reset to clean state before a test run.
        """
        super(Feature, self).reset()
        for scenario in self.scenarios:
            scenario.reset()

    def __repr__(self):
        return '<Feature "%s": %d scenario(s)>' % (
         self.name, len(self.scenarios))

    def __iter__(self):
        return iter(self.scenarios)

    def add_scenario(self, scenario):
        scenario.feature = self
        scenario.background = self.background
        self.scenarios.append(scenario)

    def compute_status(self):
        """
        Compute the status of this feature based on its:
           * scenarios
           * scenario outlines

        :return: Computed status (as string-enum).
        """
        skipped = True
        passed_count = 0
        for scenario in self.scenarios:
            scenario_status = scenario.status
            if scenario_status == 'failed':
                return 'failed'
            if scenario_status == 'untested':
                if passed_count > 0:
                    return 'failed'
                return 'untested'
            if scenario_status != 'skipped':
                skipped = False
            if scenario_status == 'passed':
                passed_count += 1
                continue

        return skipped and 'skipped' or 'passed'

    @property
    def duration(self):
        feature_duration = 0.0
        for scenario in self.scenarios:
            feature_duration += scenario.duration

        return feature_duration

    def walk_scenarios(self, with_outlines=False):
        """
        Provides a flat list of all scenarios of this feature.
        A ScenarioOutline element adds its scenarios to this list.
        But the ScenarioOutline element itself is only added when specified.

        A flat scenario list is useful when all scenarios of a features
        should be processed.

        :param with_outlines: If ScenarioOutline items should be added, too.
        :return: List of all scenarios of this feature.
        """
        all_scenarios = []
        for scenario in self.scenarios:
            if isinstance(scenario, ScenarioOutline):
                scenario_outline = scenario
                if with_outlines:
                    all_scenarios.append(scenario_outline)
                all_scenarios.extend(scenario_outline.scenarios)
            else:
                all_scenarios.append(scenario)

        return all_scenarios

    def should_run(self, config=None):
        """
        Determines if this Feature (and its scenarios) should run.
        Implements the run decision logic for a feature.
        The decision depends on:

          * if the Feature is marked as skipped
          * if the config.tags (tag expression) enable/disable this feature

        :param config:  Runner configuration to use (optional).
        :return: True, if scenario should run. False, otherwise.
        """
        answer = not self.should_skip
        if answer:
            if config:
                answer = self.should_run_with_tags(config.tags)
        return answer

    def should_run_with_tags(self, tag_expression):
        """
        Determines if this feature should run when the tag expression is used.
        A feature should run if:
          * it should run according to its tags
          * any of its scenarios should run according to its tags

        :param tag_expression:  Runner/config environment tags to use.
        :return: True, if feature should run. False, otherwise (skip it).
        """
        run_feature = tag_expression.check(self.tags)
        if not run_feature:
            for scenario in self:
                if scenario.should_run_with_tags(tag_expression):
                    run_feature = True
                    break

        return run_feature

    def mark_skipped(self):
        """
        Marks this feature (and all its scenarios and steps) as skipped.
        """
        self._cached_status = None
        self.should_skip = True
        for scenario in self.scenarios:
            scenario.mark_skipped()
        else:
            self._cached_status = 'skipped'

        assert self.status == 'skipped'

    def run(self, runner):
        self._cached_status = None
        runner.context._push()
        runner.context.feature = self
        run_feature = self.should_run(runner.config)
        if run_feature or runner.config.show_skipped:
            for formatter in runner.formatters:
                formatter.feature(self)

        runner.context.tags = set(self.tags)
        hooks_called = False
        if not runner.config.dry_run:
            if run_feature:
                hooks_called = True
                for tag in self.tags:
                    runner.run_hook('before_tag', runner.context, tag)

                runner.run_hook('before_feature', runner.context, self)
                run_feature = self.should_run()
        if self.background:
            if run_feature or runner.config.show_skipped:
                for formatter in runner.formatters:
                    formatter.background(self.background)

        failed_count = 0
        for scenario in self.scenarios:
            if runner.config.name:
                if not scenario.should_run_with_name_select(runner.config):
                    scenario.mark_skipped()
                    continue
            failed = scenario.run(runner)
            if failed:
                failed_count += 1
                if runner.config.stop or runner.aborted:
                    break
                else:
                    continue
        else:
            if not run_feature:
                self._cached_status = 'skipped'

        if hooks_called:
            runner.run_hook('after_feature', runner.context, self)
            if self._cached_status == 'failed':
                if failed_count == 0:
                    failed_count = 1
            for tag in self.tags:
                runner.run_hook('after_tag', runner.context, tag)

        runner.context._pop()
        if run_feature or runner.config.show_skipped:
            for formatter in runner.formatters:
                formatter.eof()

        failed = failed_count > 0
        return failed


class Background(BasicStatement, Replayable):
    __doc__ = 'A `background`_ parsed from a *feature file*.\n\n    The attributes are:\n\n    .. attribute:: keyword\n\n       This is the keyword as seen in the *feature file*. In English this will\n       typically be "Background".\n\n    .. attribute:: name\n\n       The name of the background (the text after "Background:".)\n\n    .. attribute:: steps\n\n       A list of :class:`~beehive.model.Step` making up this background.\n\n    .. attribute:: duration\n\n       The time, in seconds, that it took to run this background. If read\n       before the background is run it will return 0.0.\n\n    .. attribute:: filename\n\n       The file name (or "<string>") of the *feature file* where the scenario\n       was found.\n\n    .. attribute:: line\n\n       The line number of the *feature file* where the scenario was found.\n\n    .. _`background`: gherkin.html#backgrounds\n    '
    type = 'background'

    def __init__(self, filename, line, keyword, name, steps=None):
        super(Background, self).__init__(filename, line, keyword, name)
        self.steps = steps or []

    def __repr__(self):
        return '<Background "%s">' % self.name

    def __iter__(self):
        return iter(self.steps)

    @property
    def duration(self):
        duration = 0
        for step in self.steps:
            duration += step.duration

        return duration


class Scenario(TagAndStatusStatement, Replayable):
    __doc__ = 'A `scenario`_ parsed from a *feature file*.\n\n    The attributes are:\n\n    .. attribute:: keyword\n\n       This is the keyword as seen in the *feature file*. In English this will\n       typically be "Scenario".\n\n    .. attribute:: name\n\n       The name of the scenario (the text after "Scenario:".)\n\n    .. attribute:: description\n\n       The description of the scenario as seen in the *feature file*.\n       This is stored as a list of text lines.\n\n    .. attribute:: feature\n\n       The :class:`~beehive.model.Feature` this scenario belongs to.\n\n    .. attribute:: steps\n\n       A list of :class:`~beehive.model.Step` making up this scenario.\n\n    .. attribute:: tags\n\n       A list of @tags (as :class:`~beehive.model.Tag` which are basically\n       glorified strings) attached to the scenario.\n       See :ref:`controlling things with tags`.\n\n    .. attribute:: status\n\n       Read-Only. A summary status of the scenario\'s run. If read before the\n       scenario is fully tested it will return "untested" otherwise it will\n       return one of:\n\n       "untested"\n         The scenario was has not been completely tested yet.\n       "skipped"\n         One or more steps of this scenario was passed over during testing.\n       "passed"\n         The scenario was tested successfully.\n       "failed"\n         One or more steps of this scenario failed.\n\n    .. attribute:: duration\n\n       The time, in seconds, that it took to test this scenario. If read before\n       the scenario is tested it will return 0.0.\n\n    .. attribute:: filename\n\n       The file name (or "<string>") of the *feature file* where the scenario\n       was found.\n\n    .. attribute:: line\n\n       The line number of the *feature file* where the scenario was found.\n\n    .. _`scenario`: gherkin.html#scenarios\n    '
    type = 'scenario'

    def __init__(self, filename, line, keyword, name, tags=None, steps=None, description=None):
        tags = tags or []
        super(Scenario, self).__init__(filename, line, keyword, name, tags)
        self.description = description or []
        self.steps = steps or []
        self.background = None
        self.feature = None
        self._background_steps = None
        self._row = None
        self.was_dry_run = False
        self.stderr = None
        self.stdout = None

    def reset(self):
        """
        Reset the internal data to reintroduce new-born state just after the
        ctor was called.
        """
        super(Scenario, self).reset()
        self._row = None
        self.was_dry_run = False
        self.stderr = None
        self.stdout = None
        for step in self.all_steps:
            step.reset()

    @property
    def background_steps(self):
        """
        Provide background steps if feature has a background.
        Lazy init that copies the background steps.

        Note that a copy of the background steps is needed to ensure
        that the background step status is specific to the scenario.

        :return:  List of background steps or empty list
        """
        if self._background_steps is None:
            steps = []
            if self.background:
                steps = [copy.copy(step) for step in self.background.steps]
            self._background_steps = steps
        return self._background_steps

    @property
    def all_steps(self):
        """Returns iterator to all steps, including background steps if any."""
        if self.background is not None:
            return itertools.chain(self.background_steps, self.steps)
        else:
            return iter(self.steps)

    def __repr__(self):
        return '<Scenario "%s">' % self.name

    def __iter__(self):
        return self.all_steps

    def compute_status(self):
        """Compute the status of the scenario from its steps.
        :return: Computed status (as string).
        """
        for step in self.all_steps:
            if step.status == 'undefined':
                if self.was_dry_run:
                    return 'untested'
                else:
                    return 'failed'
            elif step.status != 'passed':
                assert step.status in ('failed', 'skipped', 'untested')
                return step.status

        return 'passed'

    @property
    def duration(self):
        scenario_duration = 0
        for step in self.all_steps:
            scenario_duration += step.duration

        return scenario_duration

    @property
    def effective_tags(self):
        """
        Effective tags for this scenario:
          * own tags
          * tags inherited from its feature
        """
        tags = self.tags
        if self.feature:
            tags = self.feature.tags + self.tags
        return tags

    def should_run(self, config=None):
        """
        Determines if this Scenario (or ScenarioOutline) should run.
        Implements the run decision logic for a scenario.
        The decision depends on:

          * if the Scenario is marked as skipped
          * if the config.tags (tag expression) enable/disable this scenario
          * if the scenario is selected by name

        :param config:  Runner configuration to use (optional).
        :return: True, if scenario should run. False, otherwise.
        """
        answer = not self.should_skip
        if answer:
            if config:
                answer = self.should_run_with_tags(config.tags) and self.should_run_with_name_select(config)
        return answer

    def should_run_with_tags(self, tag_expression):
        """
        Determines if this scenario should run when the tag expression is used.

        :param tag_expression:  Runner/config environment tags to use.
        :return: True, if scenario should run. False, otherwise (skip it).
        """
        return tag_expression.check(self.effective_tags)

    def should_run_with_name_select(self, config):
        """Determines if this scenario should run when it is selected by name.

        :param config:  Runner/config environment name regexp (if any).
        :return: True, if scenario should run. False, otherwise (skip it).
        """
        return not config.name or config.name_re.search(self.name)

    def mark_skipped(self):
        """
        Marks this scenario (and all its steps) as skipped.
        """
        self._cached_status = None
        self.should_skip = True
        for step in self.all_steps:
            if not step.status == 'untested':
                assert step.status == 'skipped'
                step.status = 'skipped'
        else:
            self._cached_status = 'skipped'

        assert self.status == 'skipped', 'OOPS: scenario.status=%s' % self.status

    def run(self, runner):
        self._cached_status = None
        failed = False
        run_scenario = self.should_run(runner.config)
        run_steps = run_scenario and not runner.config.dry_run
        dry_run_scenario = run_scenario and runner.config.dry_run
        self.was_dry_run = dry_run_scenario
        if run_scenario or runner.config.show_skipped:
            for formatter in runner.formatters:
                formatter.scenario(self)

        runner.context._push()
        runner.context.scenario = self
        runner.context.tags = set(self.effective_tags)
        hooks_called = False
        if not runner.config.dry_run:
            if run_scenario:
                hooks_called = True
                for tag in self.tags:
                    runner.run_hook('before_tag', runner.context, tag)

                runner.run_hook('before_scenario', runner.context, self)
                run_scenario = run_steps = self.should_run()
        runner.setup_capture()
        if run_scenario or runner.config.show_skipped:
            for step in self:
                for formatter in runner.formatters:
                    formatter.step(step)

        for step in self.all_steps:
            if run_steps and not self.should_skip:
                if not step.run(runner):
                    run_steps = False
                    failed = True
                    runner.context._set_root_attribute('failed', True)
                    self._cached_status = 'failed'
            elif failed or dry_run_scenario:
                step.status = 'skipped'
                if dry_run_scenario:
                    step.status = 'untested'
                found_step = step_registry.registry.find_match(step)
                if not found_step:
                    step.status = 'undefined'
                    runner.undefined_steps.append(step)
            else:
                step.status = 'skipped'
        else:
            if not run_scenario:
                self._cached_status = 'skipped'

        if runner.config.junit:
            self.stdout = runner.context.stdout_capture.getvalue()
            self.stderr = runner.context.stderr_capture.getvalue()
        runner.teardown_capture()
        if hooks_called:
            runner.run_hook('after_scenario', runner.context, self)
            if self._cached_status == 'failed':
                failed = True
            for tag in self.tags:
                runner.run_hook('after_tag', runner.context, tag)

        runner.context._pop()
        return failed


class ScenarioOutline(Scenario):
    __doc__ = 'A `scenario outline`_ parsed from a *feature file*.\n\n    A scenario outline extends the existing :class:`~beehive.model.Scenario`\n    class with the addition of the :class:`~beehive.model.Examples` tables of\n    data from the *feature file*.\n\n    The attributes are:\n\n    .. attribute:: keyword\n\n       This is the keyword as seen in the *feature file*. In English this will\n       typically be "Scenario Outline".\n\n    .. attribute:: name\n\n       The name of the scenario (the text after "Scenario Outline:".)\n\n    .. attribute:: description\n\n       The description of the `scenario outline`_ as seen in the *feature file*.\n       This is stored as a list of text lines.\n\n    .. attribute:: feature\n\n       The :class:`~beehive.model.Feature` this scenario outline belongs to.\n\n    .. attribute:: steps\n\n       A list of :class:`~beehive.model.Step` making up this scenario outline.\n\n    .. attribute:: examples\n\n       A list of :class:`~beehive.model.Examples` used by this scenario outline.\n\n    .. attribute:: tags\n\n       A list of @tags (as :class:`~beehive.model.Tag` which are basically\n       glorified strings) attached to the scenario.\n       See :ref:`controlling things with tags`.\n\n    .. attribute:: status\n\n       Read-Only. A summary status of the scenario outlines\'s run. If read\n       before the scenario is fully tested it will return "untested" otherwise\n       it will return one of:\n\n       "untested"\n         The scenario was has not been completely tested yet.\n       "skipped"\n         One or more scenarios of this outline was passed over during testing.\n       "passed"\n         The scenario was tested successfully.\n       "failed"\n         One or more scenarios of this outline failed.\n\n    .. attribute:: duration\n\n       The time, in seconds, that it took to test the scenarios of this\n       outline. If read before the scenarios are tested it will return 0.0.\n\n    .. attribute:: filename\n\n       The file name (or "<string>") of the *feature file* where the scenario\n       was found.\n\n    .. attribute:: line\n\n       The line number of the *feature file* where the scenario was found.\n\n    .. _`scenario outline`: gherkin.html#scenario-outlines\n    '
    type = 'scenario_outline'
    annotation_schema = '{name} -- @{row.id} {examples.name}'

    def __init__(self, filename, line, keyword, name, tags=None, steps=None, examples=None, description=None):
        super(ScenarioOutline, self).__init__(filename, line, keyword, name, tags, steps, description)
        self.examples = examples or []
        self._scenarios = []

    def reset(self):
        """Reset runtime temporary data like before a test run."""
        super(ScenarioOutline, self).reset()
        for scenario in self.scenarios:
            scenario.reset()

    @staticmethod
    def render_template(text, row=None, params=None):
        """Render a text template with placeholders, ala "Hello <name>".

        :param row:     As placeholder provider (dict-like).
        :param params:  As additional placeholder provider (as dict).
        :return: Rendered text, known placeholders are substituted w/ values.
        """
        if not ('<' in text and '>' in text):
            return text
        safe_values = False
        for placeholders in (row, params):
            if not placeholders:
                continue
            for name, value in placeholders.items():
                if safe_values:
                    if '<' in value and '>' in value:
                        continue
                    text = text.replace('<%s>' % name, value)

        return text

    def make_scenario_name(self, example, row, params=None):
        """Build a scenario name for an example row of this scenario outline.
        Placeholders for row data are replaced by values.

        SCHEMA: "{scenario_outline.name} -*- {examples.name}@{row.id}"

        :param example:  Examples object.
        :param row:      Row of this example.
        :param params:   Additional placeholders for example/row.
        :return: Computed name for the scenario representing example/row.
        """
        if params is None:
            params = {}
        params['examples.name'] = example.name or ''
        params.setdefault('examples.index', example.index)
        params.setdefault('row.index', row.index)
        params.setdefault('row.id', row.id)
        examples_name = self.render_template(example.name, row, params)
        params['examples.name'] = examples_name
        scenario_name = self.render_template(self.name, row, params)

        class Data(object):

            def __init__(self, name, index):
                self.name = name
                self.index = index
                self.id = name

        example_data = Data(examples_name, example.index)
        row_data = Data(row.id, row.index)
        return self.annotation_schema.format(name=scenario_name, examples=example_data, row=row_data)

    def make_row_tags(self, row, params=None):
        if not self.tags:
            return
        tags = []
        for tag in self.tags:
            if '<' in tag:
                if '>' in tag:
                    tag = self.render_template(tag, row, params)
            if not '<' in tag:
                if '>' in tag:
                    continue
                new_tag = Tag.make_name(tag, unescape=True)
                tags.append(new_tag)

        return tags

    @classmethod
    def make_step_for_row(cls, outline_step, row, params=None):
        new_step = copy.deepcopy(outline_step)
        new_step.name = cls.render_template(new_step.name, row, params)
        if new_step.text:
            new_step.text = cls.render_template(new_step.text, row)
        if new_step.table:
            for name, value in row.items():
                for row in new_step.table:
                    for i, cell in enumerate(row.cells):
                        row.cells[i] = cell.replace('<%s>' % name, value)

        return new_step

    @property
    def scenarios(self):
        """Return the scenarios with the steps altered to take the values from
        the examples.
        """
        if self._scenarios:
            return self._scenarios
        params = {'examples.name': None, 
         'examples.index': None, 
         'row.index': None, 
         'row.id': None}
        for example_index, example in enumerate(self.examples):
            example.index = example_index + 1
            params['examples.name'] = example.name
            params['examples.index'] = str(example.index)
            for row_index, row in enumerate(example.table):
                row.index = row_index + 1
                row.id = '%d.%d' % (example.index, row.index)
                params['row.id'] = row.id
                params['row.index'] = str(row.index)
                scenario_name = self.make_scenario_name(example, row, params)
                row_tags = self.make_row_tags(row, params)
                new_steps = []
                for outline_step in self.steps:
                    new_step = self.make_step_for_row(outline_step, row, params)
                    new_steps.append(new_step)

                scenario_line = row.line
                scenario = Scenario(self.filename, scenario_line, self.keyword, scenario_name, row_tags, new_steps)
                scenario.feature = self.feature
                scenario.background = self.background
                scenario._row = row
                self._scenarios.append(scenario)

        return self._scenarios

    def __repr__(self):
        return '<ScenarioOutline "%s">' % self.name

    def __iter__(self):
        return iter(self.scenarios)

    def compute_status(self):
        if not self.scenarios:
            return 'passed'
        skipped = 0
        for scenario in self.scenarios:
            scenario_status = scenario.status
            if scenario_status == 'failed':
                return 'failed'
            if scenario_status == 'skipped':
                skipped += 1
            else:
                if scenario_status == 'untested':
                    return 'untested'
                if not scenario_status == 'passed':
                    raise AssertionError

        if skipped == len(self.scenarios):
            return 'skipped'
        return 'passed'

    @property
    def duration(self):
        outline_duration = 0
        for scenario in self.scenarios:
            outline_duration += scenario.duration

        return outline_duration

    def should_run_with_tags(self, tag_expression):
        """
        Determines if this scenario outline (or one of its scenarios)
        should run when the tag expression is used.

        :param tag_expression:  Runner/config environment tags to use.
        :return: True, if scenario should run. False, otherwise (skip it).
        """
        if tag_expression.check(self.effective_tags):
            return True
        for scenario in self.scenarios:
            if scenario.should_run_with_tags(tag_expression):
                return True

        return False

    def should_run_with_name_select(self, config):
        """Determines if this scenario should run when it is selected by name.

        :param config:  Runner/config environment name regexp (if any).
        :return: True, if scenario should run. False, otherwise (skip it).
        """
        if not config.name:
            return True
        for scenario in self.scenarios:
            if scenario.should_run_with_name_select(config):
                return True

        return False

    def mark_skipped(self):
        """
        Marks this scenario outline (and all its scenarios/steps) as skipped.
        """
        self._cached_status = None
        self.should_skip = True
        for scenario in self.scenarios:
            scenario.mark_skipped()
        else:
            self._cached_status = 'skipped'

        assert self.status == 'skipped'

    def run(self, runner):
        self._cached_status = None
        failed_count = 0
        for scenario in self.scenarios:
            runner.context._set_root_attribute('active_outline', scenario._row)
            failed = scenario.run(runner)
            if failed:
                failed_count += 1
                if runner.config.stop or runner.aborted:
                    break
                else:
                    continue

        runner.context._set_root_attribute('active_outline', None)
        return failed_count > 0


class Examples(BasicStatement, Replayable):
    __doc__ = 'A table parsed from a `scenario outline`_ in a *feature file*.\n\n    The attributes are:\n\n    .. attribute:: keyword\n\n       This is the keyword as seen in the *feature file*. In English this will\n       typically be "Example".\n\n    .. attribute:: name\n\n       The name of the example (the text after "Example:".)\n\n    .. attribute:: table\n\n       An instance  of :class:`~beehive.model.Table` that came with the example\n       in the *feature file*.\n\n    .. attribute:: filename\n\n       The file name (or "<string>") of the *feature file* where the scenario\n       was found.\n\n    .. attribute:: line\n\n       The line number of the *feature file* where the scenario was found.\n\n    .. _`examples`: gherkin.html#examples\n    '
    type = 'examples'

    def __init__(self, filename, line, keyword, name, table=None):
        super(Examples, self).__init__(filename, line, keyword, name)
        self.table = table
        self.index = None


class Step(BasicStatement, Replayable):
    __doc__ = 'A single `step`_ parsed from a *feature file*.\n\n    The attributes are:\n\n    .. attribute:: keyword\n\n       This is the keyword as seen in the *feature file*. In English this will\n       typically be "Given", "When", "Then" or a number of other words.\n\n    .. attribute:: name\n\n       The name of the step (the text after "Given" etc.)\n\n    .. attribute:: step_type\n\n       The type of step as determined by the keyword. If the keyword is "and"\n       then the previous keyword in the *feature file* will determine this\n       step\'s step_type.\n\n    .. attribute:: text\n\n       An instance of :class:`~beehive.model.Text` that came with the step\n       in the *feature file*.\n\n    .. attribute:: table\n\n       An instance of :class:`~beehive.model.Table` that came with the step\n       in the *feature file*.\n\n    .. attribute:: status\n\n       Read-Only. A summary status of the step\'s run. If read before the\n       step is tested it will return "untested" otherwise it will\n       return one of:\n\n       "skipped"\n         This step was passed over during testing.\n       "passed"\n         The step was tested successfully.\n       "failed"\n         The step failed.\n\n    .. attribute:: duration\n\n       The time, in seconds, that it took to test this step. If read before the\n       step is tested it will return 0.0.\n\n    .. attribute:: error_message\n\n       If the step failed then this will hold any error information, as a\n       single string. It will otherwise be None.\n\n    .. attribute:: filename\n\n       The file name (or "<string>") of the *feature file* where the step was\n       found.\n\n    .. attribute:: line\n\n       The line number of the *feature file* where the step was found.\n\n    .. _`step`: gherkin.html#steps\n    '
    type = 'step'

    def __init__(self, filename, line, keyword, step_type, name, text=None, table=None):
        super(Step, self).__init__(filename, line, keyword, name)
        self.step_type = step_type
        self.text = text
        self.table = table
        self.status = 'untested'
        self.duration = 0
        self.exception = None
        self.exc_traceback = None
        self.error_message = None

    def reset(self):
        """Reset temporary runtime data to reach clean state again."""
        self.status = 'untested'
        self.duration = 0
        self.exception = None
        self.exc_traceback = None
        self.error_message = None

    def store_exception_context(self, exception):
        self.exception = exception
        self.exc_traceback = sys.exc_info()[2]

    def __repr__(self):
        return '<%s "%s">' % (self.step_type, self.name)

    def __eq__(self, other):
        return (
         self.step_type, self.name) == (other.step_type, other.name)

    def __hash__(self):
        return hash(self.step_type) + hash(self.name)

    def set_values(self, table_row):
        """Clone a new step from this one, used for ScenarioOutline.
        Replace ScenarioOutline placeholders w/ values.

        :param table_row:  Placeholder data for example row.
        :return: Cloned, adapted step object.

        .. note:: Deprecating
            Use 'ScenarioOutline.make_step_for_row()' instead.
        """
        import warnings
        warnings.warn("Use 'ScenarioOutline.make_step_for_row()' instead", PendingDeprecationWarning, stacklevel=2)
        outline_step = self
        return ScenarioOutline.make_step_for_row(outline_step, table_row)

    def run(self, runner, quiet=False, capture=True):
        self.exception = self.exc_traceback = self.error_message = None
        match = step_registry.registry.find_match(self)
        if match is None:
            runner.undefined_steps.append(self)
            if not quiet:
                for formatter in runner.formatters:
                    formatter.match(NoMatch())

            self.status = 'undefined'
            if not quiet:
                for formatter in runner.formatters:
                    formatter.result(self)

            return False
        keep_going = True
        if not quiet:
            for formatter in runner.formatters:
                formatter.match(match)

        runner.run_hook('before_step', runner.context, self)
        if capture:
            runner.start_capture()
        error = ''
        if self.status != 'failed':
            try:
                start = time.time()
                runner.context.text = self.text
                runner.context.table = self.table
                match.run(runner.context)
                self.status = 'passed'
            except KeyboardInterrupt as e:
                runner.aborted = True
                error = 'ABORTED: By user (KeyboardInterrupt).'
                self.status = 'failed'
                self.store_exception_context(e)
            except AssertionError as e:
                self.status = 'failed'
                self.store_exception_context(e)
                if e.args:
                    error = 'Assertion Failed: %s' % e
                else:
                    error = traceback.format_exc()
            except Exception as e:
                self.status = 'failed'
                error = traceback.format_exc()
                self.store_exception_context(e)

            self.duration = time.time() - start
        if capture:
            runner.stop_capture()
        runner.run_hook('after_step', runner.context, self)
        if self.status == 'failed':
            if capture:
                if runner.config.stdout_capture:
                    output = runner.stdout_capture.getvalue()
                    if hasattr(output, 'decode'):
                        output = output.decode('utf-8')
                    if output:
                        error += '\nCaptured stdout:\n%s' % output
                if runner.config.stderr_capture:
                    output = runner.stderr_capture.getvalue()
                    if hasattr(output, 'decode'):
                        output = output.decode('utf-8')
                    if output:
                        error += '\nCaptured stderr:\n%s' % output
                    if runner.config.log_capture:
                        output = runner.log_capture.getvalue()
                        if hasattr(output, 'decode'):
                            output = output.decode('utf-8')
                        if output:
                            error += '\nCaptured logging:\n%s' % output
                    self.error_message = error
                    keep_going = False
        if not quiet:
            for formatter in runner.formatters:
                formatter.result(self)

        return keep_going


class Table(Replayable):
    __doc__ = "A `table`_ extracted from a *feature file*.\n\n    Table instance data is accessible using a number of methods:\n\n    **iteration**\n      Iterating over the Table will yield the :class:`~beehive.model.Row`\n      instances from the .rows attribute.\n\n    **indexed access**\n      Individual rows may be accessed directly by index on the Table instance;\n      table[0] gives the first non-heading row and table[-1] gives the last\n      row.\n\n    The attributes are:\n\n    .. attribute:: headings\n\n       The headings of the table as a list of strings.\n\n    .. attribute:: rows\n\n       An list of instances of :class:`~beehive.model.Row` that make up the body\n       of the table in the *feature file*.\n\n    Tables are also comparable, for what that's worth. Headings and row data\n    are compared.\n\n    .. _`table`: gherkin.html#table\n    "
    type = 'table'

    def __init__(self, headings, line=None, rows=None):
        Replayable.__init__(self)
        self.headings = headings
        self.line = line
        self.rows = []
        if rows:
            for row in rows:
                self.add_row(row, line)

    def add_row(self, row, line=None):
        self.rows.append(Row(self.headings, row, line))

    def add_column(self, column_name, values=None, default_value=''):
        """
        Adds a new column to this table.
        Uses :param:`default_value` for new cells (if :param:`values` are
        not provided). param:`values` are extended with :param:`default_value`
        if values list is smaller than the number of table rows.

        :param column_name: Name of new column (as string).
        :param values: Optional list of cell values in new column.
        :param default_value: Default value for cell (if values not provided).
        :returns: Index of new column (as number).
        """
        assert not self.has_column(column_name)
        if values is None:
            values = [
             default_value] * len(self.rows)
        elif not isinstance(values, list):
            values = list(values)
        if len(values) < len(self.rows):
            more_size = len(self.rows) - len(values)
            more_values = [default_value] * more_size
            values.extend(more_values)
        new_column_index = len(self.headings)
        self.headings.append(column_name)
        for row, value in zip(self.rows, values):
            assert len(row.cells) == new_column_index
            row.cells.append(value)

        return new_column_index

    def remove_column(self, column_name):
        if not isinstance(column_name, int):
            try:
                column_index = self.get_column_index(column_name)
            except ValueError:
                raise KeyError('column=%s is unknown' % column_name)

        assert isinstance(column_index, int)
        assert column_index < len(self.headings)
        del self.headings[column_index]
        for row in self.rows:
            assert column_index < len(row.cells)
            del row.cells[column_index]

    def remove_columns(self, column_names):
        for column_name in column_names:
            self.remove_column(column_name)

    def has_column(self, column_name):
        return column_name in self.headings

    def get_column_index(self, column_name):
        return self.headings.index(column_name)

    def require_column(self, column_name):
        """
        Require that a column exists in the table.
        Raise an AssertionError if the column does not exist.

        :param column_name: Name of new column (as string).
        :return: Index of column (as number) if it exists.
        """
        if not self.has_column(column_name):
            columns = ', '.join(self.headings)
            msg = 'REQUIRE COLUMN: %s (columns: %s)' % (column_name, columns)
            raise AssertionError(msg)
        return self.get_column_index(column_name)

    def require_columns(self, column_names):
        for column_name in column_names:
            self.require_column(column_name)

    def ensure_column_exists(self, column_name):
        """
        Ensures that a column with the given name exists.
        If the column does not exist, the column is added.

        :param column_name: Name of column (as string).
        :return: Index of column (as number).
        """
        if self.has_column(column_name):
            return self.get_column_index(column_name)
        else:
            return self.add_column(column_name)

    def __repr__(self):
        return '<Table: %dx%d>' % (len(self.headings), len(self.rows))

    def __eq__(self, other):
        if isinstance(other, Table):
            if self.headings != other.headings:
                return False
            for my_row, their_row in zip(self.rows, other.rows):
                if my_row != their_row:
                    return False

        else:
            other_rows = other
            for my_row, their_row in zip(self.rows, other_rows):
                if my_row != their_row:
                    return False

        return True

    def __ne__(self, other):
        return not self == other

    def __iter__(self):
        return iter(self.rows)

    def __getitem__(self, index):
        return self.rows[index]

    def assert_equals(self, data):
        """Assert that this table's cells are the same as the supplied "data".

        The data passed in must be a list of lists giving:

            [
                [row 1],
                [row 2],
                [row 3],
            ]

        If the cells do not match then a useful AssertionError will be raised.
        """
        assert self == data
        raise NotImplementedError


class Row(object):
    __doc__ = 'One row of a `table`_ parsed from a *feature file*.\n\n    Row data is accessible using a number of methods:\n\n    **iteration**\n      Iterating over the Row will yield the individual cells as strings.\n\n    **named access**\n      Individual cells may be accessed by heading name; row[\'name\'] would give\n      the cell value for the column with heading "name".\n\n    **indexed access**\n      Individual cells may be accessed directly by index on the Row instance;\n      row[0] gives the first cell and row[-1] gives the last cell.\n\n    The attributes are:\n\n    .. attribute:: cells\n\n       The list of strings that form the cells of this row.\n\n    .. attribute:: headings\n\n       The headings of the table as a list of strings.\n\n    Rows are also comparable, for what that\'s worth. Only the cells are\n    compared.\n\n    .. _`table`: gherkin.html#table\n    '

    def __init__(self, headings, cells, line=None, comments=None):
        self.headings = headings
        self.comments = comments
        for c in cells:
            if not isinstance(c, unicode):
                raise AssertionError

        self.cells = cells
        self.line = line

    def __getitem__(self, name):
        try:
            index = self.headings.index(name)
        except ValueError:
            if isinstance(name, int):
                index = name
            else:
                raise KeyError('"%s" is not a row heading' % name)

        return self.cells[index]

    def __repr__(self):
        return '<Row %r>' % (self.cells,)

    def __eq__(self, other):
        return self.cells == other.cells

    def __ne__(self, other):
        return not self == other

    def __len__(self):
        return len(self.cells)

    def __iter__(self):
        return iter(self.cells)

    def items(self):
        return zip(self.headings, self.cells)

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default

    def as_dict(self):
        """
        Converts the row and its cell data into a dictionary.
        :return: Row data as dictionary (without comments, line info).
        """
        from beehive.compat.collections import OrderedDict
        return OrderedDict(self.items())


class Tag(unicode):
    __doc__ = "Tags appear may be associated with Features or Scenarios.\n\n    They're a subclass of regular strings (unicode pre-Python 3) with an\n    additional ``line`` number attribute (where the tag was seen in the source\n    feature file.\n\n    See :ref:`controlling things with tags`.\n    "

    def __new__(cls, name, line):
        o = unicode.__new__(cls, name)
        o.line = line
        return o

    @staticmethod
    def make_name(text, unescape=False):
        """Translate text into a "valid tag" without whitespace, etc.
        Translation rules are:
          * alnum chars => same, kept
          * space chars => '_'
          * other chars => deleted

        :param text: Unicode text as input for name.
        :return: Unicode name that can be used as tag.
        """
        assert isinstance(text, unicode)
        if unescape:
            text = text.replace('\\t', '\t').replace('\\n', '\n')
        allowed_chars = '._-'
        chars = []
        for char in text:
            if char.isalnum() or char in allowed_chars:
                chars.append(char)
            elif char.isspace():
                chars.append('_')
                continue

        return ''.join(chars)


class Text(unicode):
    __doc__ = "Store multiline text from a Step definition.\n\n    The attributes are:\n\n    .. attribute:: value\n\n       The actual text parsed from the *feature file*.\n\n    .. attribute:: content_type\n\n       Currently only 'text/plain'.\n    "

    def __new__(cls, value, content_type='text/plain', line=0):
        assert isinstance(value, unicode)
        assert isinstance(content_type, unicode)
        o = unicode.__new__(cls, value)
        o.content_type = content_type
        o.line = line
        return o

    def line_range(self):
        line_count = len(self.splitlines())
        return (self.line, self.line + line_count + 1)

    def replace(self, old, new):
        return Text(super(Text, self).replace(old, new), self.content_type, self.line)

    def assert_equals(self, expected):
        """Assert that my text is identical to the "expected" text.

        A nice context diff will be displayed if they do not match.'
        """
        if self == expected:
            return True
        diff = []
        for line in difflib.unified_diff(self.splitlines(), expected.splitlines()):
            diff.append(line)

        diff = ['Text does not match:'] + diff[3:]
        raise AssertionError('\n'.join(diff))


class Match(Replayable):
    __doc__ = 'An parameter-matched *feature file* step name extracted using\n    step decorator `parameters`_.\n\n    .. attribute:: func\n\n       The step function that this match will be applied to.\n\n    .. attribute:: arguments\n\n       A list of :class:`beehive.model.Argument` instances containing the\n       matched parameters from the step name.\n    '
    type = 'match'

    def __init__(self, func, arguments=None):
        super(Match, self).__init__()
        self.func = func
        self.arguments = arguments
        self.location = None
        if func:
            self.location = self.make_location(func)

    def __repr__(self):
        if self.func:
            func_name = self.func.__name__
        else:
            func_name = '<no function>'
        return '<Match %s, %s>' % (func_name, self.location)

    def __eq__(self, other):
        if not isinstance(other, Match):
            return False
        return (
         self.func, self.location) == (other.func, other.location)

    def with_arguments(self, arguments):
        match = copy.copy(self)
        match.arguments = arguments
        return match

    def run(self, context):
        args = []
        kwargs = {}
        for arg in self.arguments:
            if arg.name is not None:
                kwargs[arg.name] = arg.value
            else:
                args.append(arg.value)

        with context.user_mode():
            self.func(context, *args, **kwargs)

    @staticmethod
    def make_location(step_function):
        """
        Extracts the location information from the step function and builds
        the location string (schema: "{source_filename}:{line_number}").

        :param step_function: Function whose location should be determined.
        :return: Step function location as string.
        """
        filename = os.path.relpath(step_function.__code__.co_filename, os.getcwd())
        line_number = step_function.__code__.co_firstlineno
        return FileLocation(filename, line_number)


class NoMatch(Match):
    __doc__ = '\n    Used for an "undefined step" when it can not be matched with a\n    step definition.\n    '

    def __init__(self):
        Match.__init__(self, func=None)
        self.func = None
        self.arguments = []
        self.location = None


def reset_model(model_elements):
    """
    Reset the test run information stored in model elements.

    :param model_elements:  List of model elements (Feature, Scenario, ...)
    """
    for model_element in model_elements:
        model_element.reset()