# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.4/site-packages/beehive/formatter/steps.py
# Compiled at: 2014-11-03 05:47:13
# Size of source mod 2**32: 16071 bytes
"""
Provides a formatter that provides an overview of available step definitions
(step implementations).
"""
from beehive.formatter.base import Formatter
from beehive.step_registry import StepRegistry, registry
from beehive.textutil import compute_words_maxsize, indent, make_indentation
from beehive import i18n
import inspect

class AbstractStepsFormatter(Formatter):
    __doc__ = '\n    Provides a formatter base class that provides the common functionality\n    for formatter classes that operate on step definitions (implementations).\n\n    .. note::\n        Supports beehive dry-run mode.\n    '
    step_types = ('given', 'when', 'then', 'step')

    def __init__(self, stream_opener, config):
        super(AbstractStepsFormatter, self).__init__(stream_opener, config)
        self.step_registry = None
        self.current_feature = None

    def reset(self):
        self.step_registry = None
        self.current_feature = None

    def discover_step_definitions(self):
        if self.step_registry is None:
            self.step_registry = StepRegistry()
        for step_type in registry.steps.keys():
            step_definitions = tuple(registry.steps[step_type])
            for step_definition in step_definitions:
                step_definition.step_type = step_type

            self.step_registry.steps[step_type] = step_definitions

    def feature(self, feature):
        self.current_feature = feature
        if not self.step_registry:
            self.discover_step_definitions()

    def eof(self):
        """Called at end of a feature."""
        self.current_feature = None

    def close(self):
        """Called at end of test run."""
        if not self.step_registry:
            self.discover_step_definitions()
        if self.step_registry:
            self.stream = self.open()
            self.report()
        self.close_stream()

    def report(self):
        raise NotImplementedError()

    @staticmethod
    def describe_step_definition(step_definition, step_type=None):
        if not step_type:
            step_type = step_definition.step_type
        assert step_type
        return "@%s('%s')" % (step_type, step_definition.string)


class StepsFormatter(AbstractStepsFormatter):
    __doc__ = '\n    Provides formatter class that provides an overview\n    which step definitions are available.\n\n    EXAMPLE:\n        $ beehive --dry-run -f steps features/\n        GIVEN STEP DEFINITIONS[21]:\n          Given a new working directory\n          Given I use the current directory as working directory\n          Given a file named "{filename}" with\n          ...\n          Given a step passes\n          Given a step fails\n\n        WHEN STEP DEFINITIONS[14]:\n          When I run "{command}"\n          ...\n          When a step passes\n          When a step fails\n\n        THEN STEP DEFINITIONS[45]:\n          Then the command should fail with returncode="{result:int}"\n          Then it should pass with\n          Then it should fail with\n          Then the command output should contain "{text}"\n          ...\n          Then a step passes\n          Then a step fails\n\n        GENERIC STEP DEFINITIONS[13]:\n          * I remove the directory "{directory}"\n          * a file named "{filename}" exists\n          * a file named "{filename}" does not exist\n          ...\n          * a step passes\n          * a step fails\n\n    .. note::\n        Supports beehive dry-run mode.\n    '
    name = 'steps'
    description = 'Shows step definitions (step implementations).'
    shows_location = True
    min_location_column = 40

    def report(self):
        self.report_steps_by_type()

    def report_steps_by_type(self):
        """
        Show an overview of the existing step implementations per step type.
        """
        assert set(self.step_types) == set(self.step_registry.steps.keys())
        language = self.config.lang or 'en'
        language_keywords = i18n.languages[language]
        for step_type in self.step_types:
            steps = list(self.step_registry.steps[step_type])
            if step_type != 'step':
                steps.extend(self.step_registry.steps['step'])
            if not steps:
                continue
            step_type_name = step_type.upper()
            if step_type == 'step':
                step_keyword = '*'
                step_type_name = 'GENERIC'
            else:
                keywords = language_keywords[step_type]
                if keywords[0] == '*':
                    assert len(keywords) > 1
                    step_keyword = keywords[1]
                else:
                    step_keyword = keywords[0]
                steps_text = ['%s %s' % (step_keyword, step.string) for step in steps]
                if self.shows_location:
                    max_size = compute_words_maxsize(steps_text)
                    if max_size < self.min_location_column:
                        max_size = self.min_location_column
                    schema = '  %-' + str(max_size) + 's  # %s\n'
                else:
                    schema = '  %s\n'
            message = '%s STEP DEFINITIONS[%s]:\n'
            self.stream.write(message % (step_type_name, len(steps)))
            for step, step_text in zip(steps, steps_text):
                if self.shows_location:
                    self.stream.write(schema % (step_text, step.location))
                else:
                    self.stream.write(schema % step_text)

            self.stream.write('\n')


class StepsDocFormatter(AbstractStepsFormatter):
    __doc__ = '\n    Provides formatter class that shows the documentation of all registered\n    step definitions. The primary purpose is to provide help for a test writer.\n\n    EXAMPLE:\n        $ beehive --dry-run -f steps.doc features/\n        @given(\'a file named "{filename}" with\')\n          Function: step_a_file_named_filename_with()\n          Location: beehive4cmd0/command_steps.py:50\n            Creates a textual file with the content provided as docstring.\n\n        @when(\'I run "{command}"\')\n          Function: step_i_run_command()\n          Location: beehive4cmd0/command_steps.py:80\n            Run a command as subprocess, collect its output and returncode.\n\n        @step(\'a file named "{filename}" exists\')\n          Function: step_file_named_filename_exists()\n          Location: beehive4cmd0/command_steps.py:305\n            Verifies that a file with this filename exists.\n\n            .. code-block:: gherkin\n\n                Given a file named "abc.txt" exists\n                 When a file named "abc.txt" exists\n        ...\n\n    .. note::\n        Supports beehive dry-run mode.\n    '
    name = 'steps.doc'
    description = 'Shows documentation for step definitions.'
    shows_location = True
    shows_function_name = True
    ordered_by_location = True
    doc_prefix = make_indentation(4)

    def report(self):
        self.report_step_definition_docs()
        self.stream.write('\n')

    def report_step_definition_docs(self):
        step_definitions = []
        for step_type in self.step_types:
            for step_definition in self.step_registry.steps[step_type]:
                assert step_definition.step_type is not None
                step_definitions.append(step_definition)

        if self.ordered_by_location:
            step_definitions = sorted(step_definitions, key=lambda x: x.location)
        for step_definition in step_definitions:
            self.write_step_definition(step_definition)

    def write_step_definition(self, step_definition):
        step_definition_text = self.describe_step_definition(step_definition)
        self.stream.write('%s\n' % step_definition_text)
        doc = inspect.getdoc(step_definition.func)
        func_name = step_definition.func.__name__
        if self.shows_function_name:
            if func_name not in ('step', 'impl'):
                self.stream.write('  Function: %s()\n' % func_name)
        if self.shows_location:
            self.stream.write('  Location: %s\n' % step_definition.location)
        if doc:
            doc = doc.strip()
            self.stream.write(indent(doc, self.doc_prefix))
            self.stream.write('\n')
        self.stream.write('\n')


class StepsUsageFormatter(AbstractStepsFormatter):
    __doc__ = '\n    Provides formatter class that shows how step definitions are used by steps.\n\n    EXAMPLE:\n        $ beehive --dry-run -f steps.usage features/\n        ...\n\n    .. note::\n        Supports beehive dry-run mode.\n    '
    name = 'steps.usage'
    description = 'Shows how step definitions are used by steps.'
    doc_prefix = make_indentation(4)
    min_location_column = 40

    def __init__(self, stream_opener, config):
        super(StepsUsageFormatter, self).__init__(stream_opener, config)
        self.step_usage_database = {}
        self.undefined_steps = []

    def reset(self):
        super(StepsUsageFormatter, self).reset()
        self.step_usage_database = {}
        self.undefined_steps = []

    def get_step_type_for_step_definition(self, step_definition):
        step_type = step_definition.step_type
        if not step_type:
            assert self.step_registry
            for step_type, values in self.step_registry.steps.items():
                if step_definition in values:
                    return step_type

            step_type = 'step'
        return step_type

    def select_unused_step_definitions(self):
        step_definitions = set()
        for step_type, values in self.step_registry.steps.items():
            step_definitions.update(values)

        used_step_definitions = set(self.step_usage_database.keys())
        unused_step_definitions = step_definitions - used_step_definitions
        return unused_step_definitions

    def update_usage_database(self, step_definition, step):
        matching_steps = self.step_usage_database.get(step_definition, None)
        if matching_steps is None:
            assert step_definition.step_type is not None
            matching_steps = self.step_usage_database[step_definition] = []
        if not steps_contain(matching_steps, step):
            matching_steps.append(step)

    def update_usage_database_for_step(self, step):
        step_definition = self.step_registry.find_step_definition(step)
        if step_definition:
            self.update_usage_database(step_definition, step)
        elif not steps_contain(self.undefined_steps, step):
            self.undefined_steps.append(step)

    def update_usage_database_for_feature(self, feature):
        if feature.background:
            for step in feature.background.steps:
                self.update_usage_database_for_step(step)

        for scenario in feature.walk_scenarios():
            for step in scenario.steps:
                self.update_usage_database_for_step(step)

    def feature(self, feature):
        super(StepsUsageFormatter, self).feature(feature)
        self.update_usage_database_for_feature(feature)

    def report(self):
        self.report_used_step_definitions()
        self.report_unused_step_definitions()
        self.report_undefined_steps()
        self.stream.write('\n')

    def report_used_step_definitions(self):
        step_definition_items = self.step_usage_database.items()
        step_definition_items = sorted(step_definition_items, key=lambda x: x[0].location)
        for step_definition, steps in step_definition_items:
            stepdef_text = self.describe_step_definition(step_definition)
            steps_text = ['  %s %s' % (step.keyword, step.name) for step in steps]
            steps_text.append(stepdef_text)
            max_size = compute_words_maxsize(steps_text)
            if max_size < self.min_location_column:
                max_size = self.min_location_column
            schema = '%-' + str(max_size) + 's  # %s\n'
            self.stream.write(schema % (stepdef_text, step_definition.location))
            schema = '%-' + str(max_size) + 's  # %s\n'
            for step, step_text in zip(steps, steps_text):
                self.stream.write(schema % (step_text, step.location))

            self.stream.write('\n')

    def report_unused_step_definitions(self):
        unused_step_definitions = self.select_unused_step_definitions()
        if not unused_step_definitions:
            return
        step_definitions = sorted(unused_step_definitions, key=lambda x: x.location)
        step_texts = [self.describe_step_definition(step_definition) for step_definition in step_definitions]
        max_size = compute_words_maxsize(step_texts)
        if max_size < self.min_location_column - 2:
            max_size = self.min_location_column - 2
        schema = '  %-' + str(max_size) + 's  # %s\n'
        self.stream.write('UNUSED STEP DEFINITIONS[%d]:\n' % len(step_texts))
        for step_definition, text in zip(step_definitions, step_texts):
            self.stream.write(schema % (text, step_definition.location))

    def report_undefined_steps(self):
        if not self.undefined_steps:
            return
        undefined_steps = sorted(self.undefined_steps, key=lambda x: x.location)
        steps_text = ['  %s %s' % (step.keyword, step.name) for step in undefined_steps]
        max_size = compute_words_maxsize(steps_text)
        if max_size < self.min_location_column:
            max_size = self.min_location_column
        self.stream.write('\nUNDEFINED STEPS[%d]:\n' % len(steps_text))
        schema = '%-' + str(max_size) + 's  # %s\n'
        for step, step_text in zip(undefined_steps, steps_text):
            self.stream.write(schema % (step_text, step.location))


def steps_contain(steps, step):
    for other_step in steps:
        if step == other_step and step.location == other_step.location:
            return True

    return False