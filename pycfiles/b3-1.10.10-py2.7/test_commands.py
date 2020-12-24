# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tests\plugins\welcome\test_commands.py
# Compiled at: 2016-03-08 18:42:10
from tests.plugins.welcome import Welcome_functional_test

class Test_cmd_greeting(Welcome_functional_test):

    def setUp(self):
        Welcome_functional_test.setUp(self)
        self.load_config()
        self.p.onEvent = lambda *args, **kwargs: None
        self.superadmin.connects('0')
        self.superadmin._connections = 3

    def test_no_parameter(self):
        self.superadmin.greeting = ''
        self.superadmin.clearMessageHistory()
        self.superadmin.says('!greeting')
        self.assertListEqual(['You have no greeting set'], self.superadmin.message_history)
        self.superadmin.greeting = 'hi f00'
        self.superadmin.clearMessageHistory()
        self.superadmin.says('!greeting')
        self.assertListEqual(['Your greeting is hi f00'], self.superadmin.message_history)

    def test_set_new_greeting_none(self):
        self.superadmin.greeting = 'f00'
        self.superadmin.says('!greeting none')
        self.assertListEqual(['Greeting cleared'], self.superadmin.message_history)
        self.assertEqual('', self.superadmin.greeting)

    def test_set_new_greeting_nominal(self):
        self.superadmin.greeting = ''
        self.superadmin.says('!greeting f00')
        self.assertListEqual(['Greeting Test: f00', 'Greeting changed to: f00'], self.superadmin.message_history)
        self.assertEqual('f00', self.superadmin.greeting)

    def test_set_new_greeting_too_long(self):
        self.superadmin.greeting = 'f00'
        self.superadmin.says('!greeting %s' % ('x' * 256))
        self.assertListEqual(['Your greeting is too long'], self.superadmin.message_history)
        self.assertEqual('f00', self.superadmin.greeting)

    def test_set_new_greeting_with_placeholder_name(self):
        self.superadmin.greeting = 'f00'
        self.superadmin.says('!greeting |$name|')
        self.assertListEqual(['Greeting Test: |SuperAdmin|', 'Greeting changed to: |$name|'], self.superadmin.message_history)
        self.assertEqual('|%(name)s|', self.superadmin.greeting)

    def test_set_new_greeting_with_placeholder_greeting(self):
        """
        make sure that '$greeting' cannot be taken as a placeholder or we would allow recursive greeting.
        """
        self.superadmin.greeting = 'f00'
        self.superadmin.says('!greeting |$greeting|')
        self.assertListEqual(['Greeting Test: |$greeting|', 'Greeting changed to: |$greeting|'], self.superadmin.message_history)
        self.assertEqual('|$greeting|', self.superadmin.greeting)

    def test_set_new_greeting_with_placeholder_maxLevel(self):
        self.superadmin.greeting = 'f00'
        self.superadmin.says('!greeting |$maxLevel|')
        self.assertListEqual(['Greeting Test: |100|', 'Greeting changed to: |$maxLevel|'], self.superadmin.message_history)
        self.assertEqual('|%(maxLevel)s|', self.superadmin.greeting)

    def test_set_new_greeting_with_placeholder_group(self):
        self.superadmin.greeting = 'f00'
        self.superadmin.says('!greeting |$group|')
        self.assertListEqual(['Greeting Test: |Super Admin|', 'Greeting changed to: |$group|'], self.superadmin.message_history)
        self.assertEqual('|%(group)s|', self.superadmin.greeting)

    def test_set_new_greeting_with_placeholder_connections(self):
        self.superadmin.greeting = 'f00'
        self.superadmin.says('!greeting |$connections|')
        self.assertListEqual(['Greeting Test: |3|', 'Greeting changed to: |$connections|'], self.superadmin.message_history)
        self.assertEqual('|%(connections)s|', self.superadmin.greeting)