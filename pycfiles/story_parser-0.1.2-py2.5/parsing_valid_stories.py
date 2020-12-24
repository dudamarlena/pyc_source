# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/story_parser/specs/parsing_valid_stories.py
# Compiled at: 2009-10-27 16:42:59
from story_parser import parse_text, InvalidHeaderException
from should_dsl import should_be
import unittest

class StoryParserWithValidStorysHeaders(unittest.TestCase):

    def test_story_title_should_be_Title1(self):
        text_parsed = parse_text('Story: Title1\n        As a <role>\n        I want to <feature>\n        So that <business value>')
        story = text_parsed.get_stories()[0]
        story.title | should_be.equal_to | 'Title1'

    def test_story_role_should_be_business_analyst(self):
        text_parsed = parse_text('\n        Story: <Title>\n        As a business analyst\n        I want to <feature>\n        So that <business value>')
        story = text_parsed.get_stories()[0]
        story.role | should_be.equal_to | 'business analyst'

    def test_story_feature_should_be_be_rich(self):
        text_parsed = parse_text('\n        Story: <Title>\n        As a <role>\n        I want to be rich\n        So that <business value>')
        story = text_parsed.get_stories()[0]
        story.feature | should_be.equal_to | 'be rich'

    def test_story_business_value_should_be_i_rest_in_peace(self):
        text_parsed = parse_text('\n        Story: <Title>\n        As a <role>\n        I want to <feature>\n        So that I rest in peace')
        story = text_parsed.get_stories()[0]
        story.business_value | should_be.equal_to | 'I rest in peace'

    def test_story_business_value_should_be_have_an_automated_build(self):
        text_parsed = parse_text('\n        Story: <Title>\n        In order to have an automated build\n        As a <role>\n        I want to <feature>')
        story = text_parsed.get_stories()[0]
        story.business_value | should_be.equal_to | 'have an automated build'

    def test_story_header_should_be_get_easily(self):
        text_parsed = parse_text('\n        Story: <Title>\n        In order to <business value>\n        As a <role>\n        I want to <feature>\n\n        Scenario 1: Nothing\n        Given FOO\n        When BAR\n        Then FOOBAR')
        story = text_parsed.get_stories()[0]
        story.header | should_be.equal_to | 'Story: <Title>\n' + 'In order to <business value>\n' + 'As a <role>\n' + 'I want to <feature>'


class StoryParserWithValidScenarios(unittest.TestCase):

    def test_scenario_title_should_be_getting_money(self):
        text_parsed = parse_text('Story: <Title>\n                                      As a <role>\n                                      I want to <feature>\n                                      So that <business value>\n\n                                      Scenario 1: Getting Money')
        story = text_parsed.get_stories()[0]
        story.scenarios | should_be.equal_to | [('Getting Money', {'given': [], 'when': [], 'then': []})]

    def test_steps_should_contain_just_a_given_with_it_works_text(self):
        text_parsed = parse_text('Story: <Title>\n                                      As a <role>\n                                      I want to <feature>\n                                      So that <business value>\n\n                                      Scenario 1: Getting Money\n                                      Given it works')
        story = text_parsed.get_stories()[0]
        story.scenarios | should_be.equal_to | [('Getting Money', {'given': ['it works'], 'when': [], 'then': []})]

    def test_steps_should_contain_a_given_a_when_and_a_then_step(self):
        text_parsed = parse_text('Story: <Title>\n                                      As a <role>\n                                      I want to <feature>\n                                      So that <business value>\n\n                                      Scenario 1: Searching for pyhistorian at Google\n                                        Given I go to http://www.google.com\n                                        When I search for pyhistorian\n                                        Then I see a github.com page')
        story = text_parsed.get_stories()[0]
        story.scenarios | should_be.equal_to | [
         ('Searching for pyhistorian at Google',
          {'given': ['I go to http://www.google.com'], 'when': [
                    'I search for pyhistorian'], 
             'then': [
                    'I see a github.com page']})]

    def test_story_with_two_scenarios_each_one_with_three_steps(self):
        text_parsed = parse_text('Story: <Title>\n                                      As a <role>\n                                      I want to <feature>\n                                      So that <business value>\n                                      Scenario 1: Searching for pyhistorian at Google\n                                        Given I go to http://www.google.com\n                                        When I search for pyhistorian\n                                        Then I see a github.com page\n\n                                      Scenario 2: Searching for pyhistorian at Yahoo\n                                        Given I go to http://www.yahoo.com\n                                        When I search for pyhistorian\n                                        Then I see the old code.google.com page')
        story = text_parsed.get_stories()[0]
        story.scenarios | should_be.equal_to | [
         ('Searching for pyhistorian at Google',
          {'given': ['I go to http://www.google.com'], 'when': [
                    'I search for pyhistorian'], 
             'then': [
                    'I see a github.com page']}),
         (
          'Searching for pyhistorian at Yahoo',
          {'given': ['I go to http://www.yahoo.com'], 'when': [
                    'I search for pyhistorian'], 
             'then': [
                    'I see the old code.google.com page']})]

    def test_scenario_numbering_should_be_optional(self):
        text_parsed = parse_text('Story: <Title>\n                                      As a <role>\n                                      I want to <feature>\n                                      So that <business value>\n                                      Scenario: <title>\n                                        Then <nothing>\n                                        ')
        story = text_parsed.get_stories()[0]
        story.scenarios | should_be.equal_to | [
         ('<title>',
          {'given': [], 'when': [], 'then': [
                    '<nothing>']})]


class ParsingScenariosWithAnds(unittest.TestCase):

    def test_and_from_when_step(self):
        text_parsed = parse_text('Story: <Title>\n                                      As a <role>\n                                      I want to <feature>\n                                      So that <business value>\n                                      Scenario 1: Searching for pyhistorian at Google\n                                        Given I go to http://www.google.com\n                                        When I fill the searchbox with pyhistorian\n                                        And I click at "Search"\n                                        Then I see a github.com page')
        story = text_parsed.get_stories()[0]
        (title, steps) = story.scenarios[0]
        steps['when'] | should_be.equal_to | ['I fill the searchbox with pyhistorian', 'I click at "Search"']


class ParsingMultipleValidStories(unittest.TestCase):
    text_parsed = parse_text('Story: First Story\n                                  As a role1\n                                  I want to feature1\n                                  So that benefit1\n\n                                  Scenario 1: First Scenario of First Story\n\n\n                                  Story: Second Story\n                                  As a rol2\n                                  I want to feature2\n                                  So that benefit2\n\n                                  Scenario 1: First Scenario of Second Story')
    (first_story, second_story) = text_parsed.get_stories()
    first_story.title | should_be.equal_to | 'First Story'
    second_story.title | should_be.equal_to | 'Second Story'


if __name__ == '__main__':
    unittest.main()