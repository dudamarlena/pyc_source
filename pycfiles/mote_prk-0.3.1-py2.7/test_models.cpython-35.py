# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hedley/django/instances/mote/mote/tests/test_models.py
# Compiled at: 2016-12-01 10:32:24
# Size of source mod 2**32: 1174 bytes
from django.test import TestCase
from mote import models

class ModelsTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        super(ModelsTestCase, cls).setUpTestData()
        cls.project = models.Project('myproject')
        cls.aspect = models.Aspect('website', cls.project)
        cls.pattern = models.Pattern('atoms', cls.aspect)
        cls.element = models.Element('button', cls.pattern)

    def test_project(self):
        self.assertEqual(self.project.id, 'myproject')
        self.assertEqual(self.project.title, 'My Project')
        self.assertEqual(self.aspect.id, self.project.aspects[0].id)

    def test_aspect(self):
        self.assertEqual(self.aspect.id, 'website')
        self.assertEqual(self.aspect.title, 'Website')
        self.assertEqual(self.pattern.id, self.aspect.patterns[0].id)

    def test_pattern(self):
        self.assertEqual(self.pattern.id, 'atoms')
        self.assertEqual(self.pattern.title, 'Atoms')
        self.assertEqual(self.element.id, self.pattern.elements[0].id)

    def test_element(self):
        self.assertEqual(self.element.id, 'button')
        self.assertEqual(self.element.title, 'Button')