# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/test/test_arguments_parse_and_validate.py
# Compiled at: 2020-04-04 13:10:47
# Size of source mod 2**32: 6420 bytes
from unittest import TestCase
from mock import patch
from eddington.arguments.parser import LabUtilParser

class ArgumentsParseAndValidateBaseTestCase(TestCase):
    default_args = dict(a0=None,
      costumed=None,
      actual_a=None,
      csv_data=None,
      excel_data=None,
      func=[],
      max_coeff=10.0,
      measurements=20,
      min_coeff=(-10.0),
      output_dir=None,
      plot=True,
      random_data=False,
      title=None,
      residuals_title=None,
      x_column=1,
      xerr_column=None,
      xlabel=None,
      xmax=20.0,
      xmin=(-20.0),
      xsigma=0.5,
      y_column=None,
      yerr_column=None,
      ylabel=None,
      ysigma=0.5,
      plot_data=False,
      grid=False)

    def setUp(self):
        self.args = dict(self.default_args)
        self.error_message = None

    def check(self):
        if self.error_message is None:
            actual_args = LabUtilParser.parse_and_validate(self.argv)
            self.assertEqual((self.args),
              (vars(actual_args)), msg='Args are different than expected')
        else:
            self.assertRaisesRegex(ValueError, self.error_message, LabUtilParser.parse_and_validate, self.argv)


class TestBasicArgumentParseAndValidateFunctionalities(ArgumentsParseAndValidateBaseTestCase):

    def test_empty_args(self):
        self.argv = []
        self.check()

    @patch.object(LabUtilParser, 'parser')
    def test_print_help(self, parser_func):
        LabUtilParser.print_help()
        parser_func.return_value.print_help.assert_called()


class TestArgumentsOutputDirParseAndValidate(ArgumentsParseAndValidateBaseTestCase):
    output_dir_path_string = '/path/to/output/dir'

    def setUp(self):
        LabUtilParser.clear_parser()
        ArgumentsParseAndValidateBaseTestCase.setUp(self)
        self.argv = ['--output-dir', self.output_dir_path_string]
        path_patcher = patch('eddington.arguments.parser.Path')
        self.path_class = path_patcher.start()
        self.output_dir = self.path_class.return_value
        self.output_dir.__repr__ = lambda a: self.output_dir_path_string
        self.addCleanup(path_patcher.stop)

    def test_output_dir_doesnt_exist(self):
        self.output_dir.exists.return_value = False
        self.args['output_dir'] = self.output_dir
        self.check()
        self.output_dir.mkdir.assert_called()

    def test_output_is_not_a_directory(self):
        self.output_dir.exists.return_value = True
        self.output_dir.is_dir.return_value = False
        self.error_message = '/path/to/output/dir is not a directory!'
        self.check()

    def test_output_is_not_empty(self):
        self.output_dir.exists.return_value = True
        self.output_dir.is_dir.return_value = True
        self.output_dir.glob.return_value = ['a', 'b', 'c']
        self.error_message = '/path/to/output/dir must be empty!'
        self.check()
        self.output_dir.glob.assert_called_with('*')

    def test_output_exists_and_empty(self):
        self.output_dir.exists.return_value = True
        self.output_dir.is_dir.return_value = True
        self.output_dir.glob.return_value = []
        self.args['output_dir'] = self.output_dir
        self.check()
        self.output_dir.glob.assert_called_with('*')


class TestPlotArgumentsValidation(ArgumentsParseAndValidateBaseTestCase):
    title = 'title1'
    residuals_title = 'residuals_title1'
    xlabel = 'xlabel1'
    ylabel = 'ylabel1'

    def setUp(self):
        ArgumentsParseAndValidateBaseTestCase.setUp(self)

    def test_validation_success_with_no_plot_argument(self):
        self.argv = [
         '--no-plot']
        self.args['plot'] = False
        self.check()

    def test_validation_success_without_no_plot_argument_and_title_argument(self):
        self.argv = [
         '--title', self.title]
        self.args['title'] = self.title
        self.check()

    def test_validation_success_without_no_plot_argument_and_residuals_title_argument(self):
        self.argv = [
         '--residuals-title', self.residuals_title]
        self.args['residuals_title'] = self.residuals_title
        self.check()

    def test_validation_success_without_no_plot_argument_and_xlabel_argument(self):
        self.argv = [
         '--xlabel', self.xlabel]
        self.args['xlabel'] = self.xlabel
        self.check()

    def test_validation_success_without_no_plot_argument_and_ylabel_argument(self):
        self.argv = [
         '--ylabel', self.ylabel]
        self.args['ylabel'] = self.ylabel
        self.check()

    def test_validation_success_without_no_plot_argument_and_two_arguments(self):
        self.argv = [
         '--xlabel', self.xlabel, '--ylabel', self.ylabel]
        self.args['xlabel'] = self.xlabel
        self.args['ylabel'] = self.ylabel
        self.check()

    def test_validation_failure_with_no_plot_argument_and_title_argument(self):
        self.argv = [
         '--no-plot', '--title', self.title]
        self.error_message = 'The arguments --title cannot be set when --no-plot is set.'
        self.check()

    def test_validation_failure_with_no_plot_argument_and_residuals_title_argument(self):
        self.argv = [
         '--no-plot', '--residuals-title', self.residuals_title]
        self.error_message = 'The arguments --residuals-title cannot be set when --no-plot is set.'
        self.check()

    def test_validation_failure_with_no_plot_argument_and_xlabel_argument(self):
        self.argv = [
         '--no-plot', '--xlabel', self.xlabel]
        self.error_message = 'The arguments --xlabel cannot be set when --no-plot is set.'
        self.check()

    def test_validation_failure_with_no_plot_argument_and_ylabel_argument(self):
        self.argv = [
         '--no-plot', '--ylabel', self.ylabel]
        self.error_message = 'The arguments --ylabel cannot be set when --no-plot is set.'
        self.check()

    def test_validation_failure_with_no_plot_argument_and_two_more_arguments(self):
        self.argv = [
         '--no-plot', '--xlabel', self.xlabel, '--ylabel', self.ylabel]
        self.error_message = 'The arguments --xlabel, --ylabel cannot be set when --no-plot is set.'
        self.check()