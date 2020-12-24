# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/scipysim/core/test_core.py
# Compiled at: 2010-04-22 06:03:43
import unittest
from actor import Actor
from errors import NoProcessFunctionDefined

class TestActor(unittest.TestCase):

    def setUp(self):
        self.block = Actor()

    def test_actor_is_abstract(self):
        self.assertRaises(NoProcessFunctionDefined, self.block.run)

    def test_input_queue_made(self):
        self.block.input_channel.put('Something')
        self.assertEquals('Something', self.block.input_channel.get())

    def test_actor_has_default_port_nums(self):
        """Test by loading a siso actor from a hardcoded path"""
        my_actor = Actor()
        self.assertEqual(my_actor.num_inputs, None)
        self.assertEqual(my_actor.num_outputs, None)
        return


if __name__ == '__main__':
    unittest.main()