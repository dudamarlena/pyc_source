# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\tests\commons.py
# Compiled at: 2016-12-21 07:19:52
# Size of source mod 2**32: 3218 bytes
from io import StringIO
from flap import __version__
from flap.util import truncate
from flap.util.path import Path
from flap.ui import Display, Controller
from tests.latex_project import LatexProject
from flap.util.path import TEMP

class EndToEndRunner:

    def __init__(self, file_system):
        self._file_system = file_system

    def test(self, test_case):
        self._tear_down(test_case)
        self._setup(test_case)
        self._execute(test_case)
        self._verify(test_case)

    def _tear_down(self, test_case):
        self._output = StringIO()
        self._display = Display(self._output, verbose=True)
        self._controller = Controller(self._file_system, self._display)
        self._file_system.deleteDirectory(self._path_for(test_case))

    def _setup(self, test_case):
        test_case._project.setup(self._file_system, self._path_for(test_case) / 'project')

    def _path_for(self, test_case):
        return TEMP / 'flap' / 'acceptance' / test_case.escaped_name

    def _execute(self, test_case):
        self._file_system.move_to_directory(self._path_for(test_case))
        self._controller.run(tex_file='./project/main.tex', output='output')

    def _verify(self, test_case):
        self._verify_generated_files(test_case)
        self._verify_console_output(test_case)

    def _verify_generated_files(self, test_case):
        location = self._file_system.open(Path.fromText('output'))
        actual = LatexProject.extract_from_directory(location)
        actual.assert_is_equivalent_to(test_case._expected)

    def _verify_console_output(self, test_case):
        self._verify_shown(__version__)
        self._verify_shown(self._display.HEADER)
        self._verify_shown(self._display._horizontal_line())
        entries = [each.as_dictionary for each in test_case._output]
        for each_entry in entries:
            each_entry['code'] = truncate(each_entry['code'], self._display.WIDTHS[3])
            self._verify_shown(self._display.ENTRY.format(**each_entry))

        self._verify_shown(self._display.SUMMARY.format(count=len(test_case._output)))

    def _verify_shown(self, text):
        message = 'Could not find the following text:\n  "{pattern}"\n\nThe output was:\n{output}\n'
        if text not in self._output.getvalue():
            raise AssertionError(message.format(pattern=text, output=self._output.getvalue()))