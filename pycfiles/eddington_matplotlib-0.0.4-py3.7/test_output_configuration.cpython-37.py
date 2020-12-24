# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/test/test_output_configuration.py
# Compiled at: 2020-04-02 13:21:11
# Size of source mod 2**32: 1825 bytes
from pathlib import Path
from unittest import TestCase
from eddington_matplotlib import OutputConfiguration

class OutputConfigurationBaseTestCase:
    func_name = 'func_name'
    data_output_path = None
    fitting_output_path = None
    residuals_output_path = None

    def setUp(self):
        self.output_configuration = OutputConfiguration.build(func_name=(self.func_name),
          output_dir=(self.output_dir))

    def test_data_output_path(self):
        self.assertEqual((self.data_output_path),
          (self.output_configuration.data_output_path),
          msg='Data output path is different than expected')

    def test_fitting_output_path(self):
        self.assertEqual((self.fitting_output_path),
          (self.output_configuration.fitting_output_path),
          msg='Fitting output path is different than expected')

    def test_residuals_output_path(self):
        self.assertEqual((self.residuals_output_path),
          (self.output_configuration.residuals_output_path),
          msg='Residuals output path is different than expected')


class TestOutputConfigurationWithoutOutputDir(TestCase, OutputConfigurationBaseTestCase):
    output_dir = None
    data_output_path = None
    fitting_output_path = None
    residuals_output_path = None

    def setUp(self):
        OutputConfigurationBaseTestCase.setUp(self)


class TestOutputConfigurationWithOutputDir(TestCase, OutputConfigurationBaseTestCase):
    output_dir = Path('directory')
    data_output_path = output_dir / 'func_name_data.png'
    fitting_output_path = output_dir / 'func_name_fitting.png'
    residuals_output_path = output_dir / 'func_name_fitting_residuals.png'

    def setUp(self):
        OutputConfigurationBaseTestCase.setUp(self)