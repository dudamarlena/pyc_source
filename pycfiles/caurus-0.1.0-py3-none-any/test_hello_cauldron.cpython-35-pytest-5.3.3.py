# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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