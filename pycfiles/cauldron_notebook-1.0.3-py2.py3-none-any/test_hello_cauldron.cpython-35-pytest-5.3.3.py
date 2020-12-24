# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /cauldron/cauldron/resources/examples/hello_cauldron/step_tests/test_hello_cauldron.py
# Compiled at: 2019-12-10 19:41:35
# Size of source mod 2**32: 355 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from cauldron.steptest import StepTestCase

class TestNotebook(StepTestCase):

    def test_first_attempt(self):
        """Should run the step without error."""
        self.run_step('S01-create-data.py')

    def test_second_attempt(self):
        """Should run the same step a second time without error."""
        self.run_step('S01-create-data.py')