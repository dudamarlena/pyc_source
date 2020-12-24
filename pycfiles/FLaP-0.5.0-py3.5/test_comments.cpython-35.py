# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\tests\unit\substitutions\test_comments.py
# Compiled at: 2016-09-30 14:50:44
# Size of source mod 2**32: 2627 bytes
from unittest import main
from tests.commons import FlapTest
from tests.latex_project import a_project

class CommentRemoverTest(FlapTest):

    def test_remove_commented_lines(self):
        self._assume = a_project().with_main_file('\nfoo\n% this is a comment\nbar')
        self._expect = a_project().with_merged_file('\nfoo\nbar')
        self._do_test_and_verify()

    def test_remove_end_line_comments(self):
        self._assume = a_project().with_main_file('A\\includegraphics% This is a comment \n[width=8cm]{%\nfoo%\n}\nB').with_image('foo.pdf')
        self._expect = a_project().with_merged_file('A\\includegraphics[width=8cm]{foo}\nB').with_image('foo.pdf')
        self._do_test_and_verify()

    def test_does_not_takes_percent_as_comments(self):
        self._assume = a_project().with_main_file('25 \\% of that \n% this is a comment \nblah bla')
        self._expect = a_project().with_merged_file('25 \\% of that \nblah bla')
        self._do_test_and_verify()

    def test_does_not_takes_verbatim_comments_as_comments(self):
        self._assume = a_project().with_main_file('25 \\verb|%| of that \n% this is a comment \nblah bla')
        self._expect = a_project().with_merged_file('25 \\verb|%| of that \nblah bla')
        self._do_test_and_verify()


if __name__ == '__main__':
    main()