# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\tests\unit\substitutions\test_misc.py
# Compiled at: 2016-09-30 14:50:44
# Size of source mod 2**32: 4122 bytes
from unittest import main
from tests.commons import FlapTest
from tests.latex_project import a_project

class TestEndinputRemover(FlapTest):
    __doc__ = '\n    Specify the behaviour of the \\endinput remover\n    '

    def test_endinput_mask_subsequent_content(self):
        self._assume = a_project().with_main_file('aaa\n\\endinput\nccc')
        self._expect = a_project().with_merged_file('aaa\n')
        self._do_test_and_verify()

    def test_endinput_in_a_separate_tex_file(self):
        self._assume = a_project().with_main_file('aaa\n\\input{foo}\nccc').with_file('foo.tex', 'bbb\n\\endinput\nzzz')
        self._expect = a_project().with_merged_file('aaa\nbbb\n\nccc')
        self._do_test_and_verify()


class MiscellaneousTests(FlapTest):

    def test_indentation_is_preserved(self):
        self._assume = a_project().with_main_file('\t\\input{part}').with_file('part.tex', '\n\\begin{center}\n\t\\includegraphics[width=4cm]{img/foo}\n  \\includegraphics[width=5cm]{img/foo}\n\\end{center}').with_image('img/foo.pdf')
        self._expect = a_project().with_merged_file('\t\n\\begin{center}\n\t\\includegraphics[width=4cm]{img_foo}\n  \\includegraphics[width=5cm]{img_foo}\n\\end{center}').with_image('img_foo.pdf')
        self._do_test_and_verify()

    def test_conflicting_images_names(self):
        self._assume = a_project().with_main_file('\\includegraphics[width=\\textwidth]{partA/result}\\n\\includegraphics[width=\\textwidth]{partB/result}\\n').with_image('partA/result.pdf').with_image('partB/result.pdf')
        self._expect = a_project().with_merged_file('\\includegraphics[width=\\textwidth]{partA_result}\\n\\includegraphics[width=\\textwidth]{partB_result}\\n').with_image('partA_result.pdf').with_image('partB_result.pdf')
        self._do_test_and_verify()

    def test_flattening_in_a_file(self):
        self._assume = a_project().with_main_file('blablabla')
        self._expect = a_project().with_merged_file('blablabla')
        self._runner._destination = lambda name: self._runner._output_path(name) / 'merged.tex'
        self._do_test_and_verify()

    def test_resources_are_copied(self):
        self._assume = a_project().with_main_file('blablabla').with_file('style.cls', 'class content')
        self._expect = a_project().with_merged_file('blablabla').with_file('style.cls', 'class content')
        self._do_test_and_verify()


if __name__ == '__main__':
    main()