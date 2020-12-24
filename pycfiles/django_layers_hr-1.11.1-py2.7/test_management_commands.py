# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/layers/tests/test_management_commands.py
# Compiled at: 2018-03-27 03:51:51
from django.test import TestCase
from django.core.management import call_command
from layers import reset_layer_stacks, build_layer_stacks
from layers.models import Layer

class ManagementCommandsTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        super(ManagementCommandsTestCase, cls).setUpTestData()
        reset_layer_stacks()
        build_layer_stacks()
        call_command('load_layers')

    def test_layer_objects(self):
        layers = [ o.name for o in Layer.objects.all().order_by('name') ]
        self.assertEqual(layers, ['basic'])