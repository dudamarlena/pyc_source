# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: templateaddons/../templateaddons/tests.py
# Compiled at: 2016-10-21 19:41:55
from django.template import Template, Context
from django.test import TestCase
from django.utils.html import strip_spaces_between_tags

class TemplateTagTestCase(TestCase):
    """
    Base class to test template tags.
    """

    def validate_template_code_result(self, fixtures):
        """
        Validates that the template code in given fixtures match the
        corresponding expected output.

        The given 'fixtures' argument is an iterable of 2-items lists matching
        the following scheme::

          (
            (template_code_1, expected_output_1),
            (template_code_2, expected_output_2),
            ...
          )
        """
        for template_code, valid_output in fixtures:
            t = Template(template_code)
            c = Context()
            output = t.render(c)
            self.assertEquals(output, valid_output)


class AssignTemplateTagTestCase(TemplateTagTestCase):
    """Tests the {% assign %} template tag"""

    def test_output(self):
        fixtures = [
         ('{% assign %}1234{% endassign %}', ''),
         ('{% assign name="sample" %}1234{% endassign %}5678{{ sample }}', '56781234'),
         ('{% assign name="sample" %}1234{% endassign %}{% assign name="sample" %}5678{% endassign %}{{ sample }}',
 '5678'),
         ('{% assign silent=1 %}1234{% endassign %}', ''),
         ('{% assign silent=0 %}1234{% endassign %}', '1234')]
        fixtures = [ ('{% load assign %}' + template_code, valid_output) for template_code, valid_output in fixtures ]
        self.validate_template_code_result(fixtures)


class CounterTemplateTagTestCase(TemplateTagTestCase):
    """Tests the {% counter %} template tag"""

    def test_output(self):
        fixtures = [
         ('{% counter %}', '0'),
         ('{% counter %}{% counter %}', '01'),
         ('{% counter %}{% counter %}{% counter %}', '012'),
         ('{% counter %}{% counter name="c2" %}{% counter %}{% counter %}', '0012'),
         ('{% counter name="c2" %}{% counter %}{% counter name="c2" %}{% counter name="c2" %}',
 '0012'),
         ('{% counter name="c1" %}{% counter name="c2" %}{% counter name="c1" %}{% counter name="c1" %}{% counter name="c2" %}',
 '00121'),
         ('{% counter start=1 %}{% counter %}', '12'),
         ('{% counter step=4 %}{% counter %}{% counter %}', '048'),
         ('{% counter step=-4 %}{% counter %}{% counter %}', '0-4-8'),
         ('{% counter ascending=1 %}{% counter %}{% counter %}', '012'),
         ('{% counter ascending=0 %}{% counter %}{% counter %}', '0-1-2'),
         ('{% counter ascending=0 step=-1 %}{% counter %}{% counter %}', '012'),
         ('{% counter silent=1 %}{% counter %}{% counter %}', '12'),
         ('{% counter %}{% counter silent=1 %}{% counter %}', '02'),
         ('{% counter silent=1 %}{% counter silent=1 %}{% counter %}', '2'),
         ('{% counter assign="c1" %}{{ c1 }}{% counter %}{% counter assign="c1" %}{{ c1 }}{% counter %}{% counter assign="c2" %}{% counter %}{{ c1 }}{{ c2 }}',
 '0012234524'),
         ('{% counter start=4 step=4 ascending=0 %}{% counter start=8 step=23 ascending=1 %}{% counter %}',
 '40-4')]
        fixtures = [ ('{% load counter %}' + template_code, valid_output) for template_code, valid_output in fixtures ]
        self.validate_template_code_result(fixtures)


class HeadingContextTemplateTagTestCase(TemplateTagTestCase):
    """Tests the {% headingcontext %} template tag"""

    def test_output(self):
        fixtures = [
         ('{% headingcontext %}<h1>Test</h1>{% endheadingcontext %}', '<h2>Test</h2>'),
         ('{% headingcontext %}<H1>Test</H1>{% endheadingcontext %}', '<h2>Test</h2>'),
         ('{% headingcontext %}<h1 class="test">Test</h1>{% endheadingcontext %}', '<h2 class="test">Test</h2>'),
         ('{% headingcontext %}<h1>Test</h1>{% endheadingcontext %}', '<h2>Test</h2>'),
         ('{% headingcontext %}<h2>Test</h2>{% endheadingcontext %}', '<h3>Test</h3>'),
         ('{% headingcontext source_level=2 %}<h2>Test</h2>{% endheadingcontext %}', '<h2>Test</h2>'),
         ('{% headingcontext source_level=5 %}<h5>Test</h5>{% endheadingcontext %}', '<h2>Test</h2>'),
         ('{% headingcontext source_level=2 target_level=4 %}<h2>Test</h2>{% endheadingcontext %}',
 '<h4>Test</h4>'),
         ('{% headingcontext source_level=5 target_level=4 %}<h5>Test</h5>{% endheadingcontext %}',
 '<h4>Test</h4>')]
        fixtures = [ ('{% load heading %}' + template_code, valid_output) for template_code, valid_output in fixtures ]
        self.validate_template_code_result(fixtures)


class JavascriptTemplateTagTestCase(TemplateTagTestCase):
    """Tests the {% counter %} template tag"""

    def test_output(self):
        fixtures = [
         ('{% javascript_render %}', '')]
        fixtures = [ ('{% load javascript %}' + template_code, valid_output) for template_code, valid_output in fixtures ]
        self.validate_template_code_result(fixtures)


class ReplaceTemplateTagTestCase(TemplateTagTestCase):
    """Tests the {% replace %} template tag"""

    def test_output(self):
        fixtures = [
         ('{% replace %}{% endreplace %}', ''),
         ('{% replace search="" replacement="" %}{% endreplace %}', ''),
         ('{% replace search="" replacement="" %}toto{% endreplace %}', 'toto'),
         ('{% replace search="" replacement="aa" %}toto{% endreplace %}', 'toto'),
         ('{% replace search="t" replacement="m" %}toto{% endreplace %}', 'momo'),
         ('{% replace search="t" replacement="" %}toto{% endreplace %}', 'oo'),
         ('{% replace search="to" replacement="ma" %}toto{% endreplace %}', 'mama'),
         ('{% replace search="toto" replacement="a" %}toto{% endreplace %}', 'a'),
         ('{% replace search=" " replacement="-" %}t o t o{% endreplace %}', 't-o-t-o'),
         ('{% replace search="\\n" replacement="" %}t\noto{% endreplace %}', 'toto'),
         ('{% replace search="[a-z]+" replacement="" %}Toto{% endreplace %}', 'T'),
         ('{% replace search="^." replacement="A" %}toto{% endreplace %}', 'Aoto'),
         ('{% replace search="to$" replacement="Z" %}toto{% endreplace %}', 'toZ'),
         ('{% replace search="\\s+" replacement="-" %}to\t \n\n   \tto{% endreplace %}', 'to-to'),
         ('{% replace search="(to)" replacement="\\1a" %}toto{% endreplace %}', 'toatoa'),
         ('{% replace search="([a-z]+)" replacement="*\\1*" %}123abc456def{% endreplace %}',
 '123*abc*456*def*'),
         ('{% replace search="(to)" replacement="au" %}(to)to{% endreplace %}', '(au)au'),
         ('{% replace search="(to)" replacement="au" use_regexp=0 %}(to)to{% endreplace %}',
 'auto'),
         ('{% filter escape_regexp %}(to){% endfilter %}', '\\(to\\)')]
        fixtures = [ ('{% load replace %}' + template_code, valid_output) for template_code, valid_output in fixtures ]
        self.validate_template_code_result(fixtures)