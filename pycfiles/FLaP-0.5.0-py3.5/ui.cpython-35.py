# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\tests\unit\ui.py
# Compiled at: 2016-09-30 09:41:22
# Size of source mod 2**32: 5173 bytes
from unittest import TestCase, main
import flap, re
from flap.engine import Fragment, Flap, GraphicNotFound, TexFileNotFound
from flap.ui import UI, Controller, Factory
from flap.util.oofs import File
from flap.util.path import ROOT, Path
from io import StringIO
from mock import patch, MagicMock

class UiTest(TestCase):

    def makeUI(self, mock):
        ui = UI(mock, True)
        return ui

    @patch('sys.stdout', new_callable=StringIO)
    def test_ui_displays_version_number(self, mock):
        ui = self.makeUI(mock)
        ui.show_opening_message()
        self.verify_output_contains(mock, flap.__version__)

    @patch('sys.stdout', new_callable=StringIO)
    def test_ui_reports_fragment(self, mock):
        ui = self.makeUI(mock)
        self.run_test(ui.on_fragment, mock, ['main.tex', '3', 'foo'])

    @patch('sys.stdout', new_callable=StringIO)
    def test_ui_reports_missing_image(self, mock):
        ui = self.makeUI(mock)
        self.run_test(ui.report_missing_graphic, mock, ['main.tex', '3', 'foo'])

    @patch('sys.stdout', new_callable=StringIO)
    def test_ui_reports_missing_tex_file(self, mock):
        ui = self.makeUI(mock)
        self.run_test(ui.report_missing_tex_file, mock, ['main.tex', '3', 'foo'])

    @patch('sys.stdout', new_callable=StringIO)
    def test_ui_reports_unexpected_error(self, mock):
        ui = self.makeUI(mock)
        ui.report_unexpected_error('foo')
        self.verify_output_contains(mock, 'foo')

    @patch('sys.stdout', new_callable=StringIO)
    def test_ui_reports_completion(self, mock):
        ui = self.makeUI(mock)
        ui.show_closing_message()
        self.verify_output_contains(mock, 'complete')

    def run_test(self, operation, mock, expected_outputs):
        operation(Fragment(File(None, ROOT / 'main.tex', None), 3, 'foo'))
        for each_output in expected_outputs:
            self.verify_output_contains(mock, each_output)

    @patch('sys.stdout', new_callable=StringIO)
    def test_disabling_reporting(self, mock):
        ui = self.makeUI(mock)
        ui.set_verbose(False)
        ui.on_fragment(Fragment(File(None, ROOT / 'main.tex', None), 3, 'foo'))
        self.assertFalse(mock.getvalue())

    def verify_output_contains(self, mock, pattern):
        output = mock.getvalue()
        self.assertIsNotNone(re.search(pattern, output), output)


class ControllerTest(TestCase):

    def setUp(self):
        self.flap_mock = MagicMock(Flap)
        self.ui_mock = MagicMock(UI)
        factory = MagicMock(Factory)
        factory.ui.return_value = self.ui_mock
        factory.flap.return_value = self.flap_mock
        self.controller = Controller(factory)

    def set_flap_behaviour(self, exception):
        self.flap_mock.flatten.side_effect = exception

    def test_missing_images_are_reported_to_the_ui(self):
        fragment = MagicMock(Fragment)
        self.set_flap_behaviour(GraphicNotFound(fragment))
        self._run_flap(['__main__.py', 'foo', 'bar'])
        self.ui_mock.report_missing_graphic.assert_called_once_with(fragment)

    def test_missing_tex_file_are_reported_to_the_ui(self):
        fragment = MagicMock(Fragment)
        self.set_flap_behaviour(TexFileNotFound(fragment))
        self._run_flap(['__main__.py', 'foo', 'bar'])
        self.ui_mock.report_missing_tex_file.assert_called_once_with(fragment)

    def test_unexpected_error_are_reported_to_the_ui(self):
        self.set_flap_behaviour(ValueError('foo'))
        self._run_flap(['__main__.py', 'foo', 'bar'])
        self.ui_mock.report_unexpected_error.assert_called_once_with('foo')

    def test_completion_is_reported(self):
        self._run_flap(['__main__.py', 'foo', 'bar'])
        self.ui_mock.show_closing_message.assert_called_with()

    def test_running_flap_with_a_specific_output_dir(self):
        self._run_flap(['__main__.py', 'foo.tex', 'output'])
        self.flap_mock.flatten.assert_called_once_with(Path.fromText('foo.tex'), Path.fromText('output'))

    def test_running_flap_with_a_specific_output_file(self):
        self._run_flap(['__main__.py', 'foo.tex', 'output/root.tex'])
        self.flap_mock.flatten.assert_called_once_with(Path.fromText('foo.tex'), Path.fromText('output/root.tex'))

    def _run_flap(self, parameters):
        self.controller.run(parameters)


if __name__ == '__main__':
    main()