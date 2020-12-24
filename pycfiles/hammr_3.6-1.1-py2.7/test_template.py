# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/unit/commands/template/test_template.py
# Compiled at: 2016-12-15 07:45:41
from unittest import TestCase
from uforge.objects.uforge import *
from hammr.commands.template import template
from mock import MagicMock

class TestTemplate(TestCase):

    def test_do_clone_should_split_parameters_even_with_spaces(self):
        t = template.Template()
        name = 'my new name wit spaces'
        args = "--id 42 --name '%s' --version 1.0" % name
        t.clone_appliance = MagicMock(return_value=appliance())
        t.do_clone(args)
        self.assertEqual(t.clone_appliance.call_count, 1)
        self.assertEqual(t.clone_appliance.call_args[0][1].name, name)