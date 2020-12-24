# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/story_parser/specs/parsing_invalid_stories.py
# Compiled at: 2009-09-25 12:02:34
from story_parser import parse_text, InvalidHeaderException, InvalidScenarioException
from should_dsl import should_be
import unittest

class StoryParserWithInvalidStoryHeaders(unittest.TestCase):

    def test_should_raise_InvalidHeaderException_with_invalid_story_title(self):
        InvalidHeaderException | should_be.thrown_by | (parse_text,
         '\n                                                      Story title is invalid\n                                                      As a <role>\n                                                      I want to <feature>\n                                                      So that <business value>')

    def test_should_raise_InvalidHeaderException_with_invalid_story_header(self):
        InvalidHeaderException | should_be.thrown_by | (parse_text,
         '\n                                                      Story: Title is OK')

    def test_should_raise_InvalidHeaderException_with_invalid_story_role(self):
        InvalidHeaderException | should_be.thrown_by | (parse_text,
         '\n                                                      Story: <Title>\n                                                      As a_invalid\n                                                      I want to <feature>\n                                                      So that <business value>')

    def test_should_raise_InvalidHeaderException_with_invalid_story_feature(self):
        InvalidHeaderException | should_be.thrown_by | (parse_text,
         '\n                                                      Story: <Title>\n                                                      As a <role>\n                                                      I want to_be invalid\n                                                      So that <business value>')

    def test_should_raise_InvalidHeaderException_with_invalid_story_business_value(self):
        InvalidHeaderException | should_be.thrown_by | (parse_text,
         '\n                                                      Story: <Title>\n                                                      As a <role>\n                                                      I want to <feature>\n                                                      So that_business value_invalid')


class StoryParserWithInvalidScenarios(unittest.TestCase):

    def test_should_raise_InvalidScenarioException_if_scenario_title_is_wrong(self):
        InvalidScenarioException | should_be.thrown_by | (parse_text,
         'Story: <Title>\n                                                           As a <role>\n                                                           I want to <feature>\n                                                           So that <business value>\n\n                                                           Scenario Getting Money')

    def test_should_raise_InvalidScenarioException_if_step_line_is_not_valid(self):
        InvalidScenarioException | should_be.thrown_by | (parse_text,
         'Story: <Title>\n                                                           As a <role>\n                                                           I want to <feature>\n                                                           So that <business value>\n\n                                                           Scenario 1: <scenario_title>\n                                                           Foo Step\n                                                        ')


class ScenarioWithInvalidAndStep(unittest.TestCase):

    def test_and_without_context(self):
        InvalidScenarioException | should_be.thrown_by | (parse_text,
         'Story: 1\n                                                        As a 2\n                                                        I want to 3\n                                                        So that 4\n\n                                                        Scenario 1: 5\n                                                        And aff')


if __name__ == '__main__':
    unittest.main()