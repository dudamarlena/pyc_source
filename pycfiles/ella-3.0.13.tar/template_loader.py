# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/xaralis/Workspace/elladev/ella/test_ella/template_loader.py
# Compiled at: 2013-07-03 05:00:55
from unittest import TestCase
from django.template import TemplateDoesNotExist
from nose import tools
templates = {}

def load_template_source(template_name, dirs=None):
    """Dummy template loader that returns templates from local templates dictionary."""
    global templates
    try:
        return (templates[template_name], template_name)
    except KeyError as e:
        raise TemplateDoesNotExist(e)


load_template_source.is_usable = True

class TestDummyTemplateLoader(TestCase):

    def tearDown(self):
        global templates
        templates = {}

    def test_simple(self):
        templates['anything.html'] = 'Something'
        source, name = load_template_source('anything.html')
        tools.assert_equals('anything.html', name)
        tools.assert_equals('Something', source)

    def test_empty(self):
        tools.assert_raises(TemplateDoesNotExist, load_template_source, 'anything.html')