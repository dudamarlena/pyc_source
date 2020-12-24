# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\tests\unit\latex\test_parser.py
# Compiled at: 2017-01-10 07:31:11
# Size of source mod 2**32: 13137 bytes
from unittest import TestCase, main
from unittest.mock import MagicMock, ANY
from flap.latex.symbols import SymbolTable
from flap.latex.tokens import TokenFactory
from flap.latex.macros import MacroFactory
from flap.latex.parser import Parser, Context, Factory

class ContextTest(TestCase):

    def setUp(self):
        self._data = {'Z': 1}
        self._environment = Context()
        for key, value in self._data.items():
            self._environment[key] = value

    def test_look_up_a_key_that_was_never_defined(self):
        self.assertIsNone(self._environment['never defined'])
        self.assertNotIn('never defined', self._environment)

    def test_definition(self):
        key, value = ('X', 234)
        self.assertNotIn('X', self._environment)
        self._environment[key] = value
        self.assertEqual(value, self._environment[key])

    def test_containment(self):
        for key, value in self._data.items():
            self.assertTrue(key in self._environment)
            self.assertEqual(value, self._environment[key])


class ParserTests(TestCase):

    def setUp(self):
        self._engine = MagicMock()
        self._macros = MacroFactory(self._engine)
        self._symbols = SymbolTable.default()
        self._tokens = TokenFactory(self._symbols)
        self._factory = Factory(self._symbols)
        self._environment = Context(definitions=self._macros.all())
        self._lexer = None
        self._parser = None

    def test_parsing_a_regular_word(self):
        self._do_test_with('hello', 'hello')

    def _do_test_with(self, input, output):
        parser = Parser(self._factory.as_tokens(input, 'Unknown'), self._factory, self._environment)
        tokens = parser.rewrite()
        self._verify_output_is(output, tokens)

    def _verify_output_is(self, expected_text, actual_tokens):
        output = ''.join(str(t) for t in actual_tokens)
        self.assertEqual(expected_text, output)

    def test_rewriting_a_group(self):
        self._do_test_with('{bonjour}', '{bonjour}')

    def test_rewriting_a_command_that_shall_not_be_rewritten(self):
        self._do_test_with('\\macro[option=23cm]{some text}', '\\macro[option=23cm]{some text}')

    def test_rewriting_a_command_within_a_group(self):
        self._do_test_with('{\\macro[option=23cm]{some text} more text}', '{\\macro[option=23cm]{some text} more text}')

    def test_rewriting_a_command_in_a_verbatim_environment(self):
        self._do_test_with('\\begin{verbatim}\\foo{bar}\\end{verbatim}', '\\begin{verbatim}\\foo{bar}\\end{verbatim}')

    def test_rewriting_a_input_in_a_verbatim_environment(self):
        self._engine.content_of.return_value = 'blabla'
        self._do_test_with('\\begin{verbatim}\\input{bar}\\end{verbatim}', '\\begin{verbatim}\\input{bar}\\end{verbatim}')
        self._engine.content_of.assert_not_called()

    def test_rewriting_a_unknown_environment(self):
        self._do_test_with('\\begin{center}blabla\\end{center}', '\\begin{center}blabla\\end{center}')

    def test_parsing_a_macro_definition(self):
        self._do_test_with('\\def\\myMacro#1{my #1}', '')

    def test_parsing_commented_out_input(self):
        self._do_test_with('% \\input my-file', '% \\input my-file')
        self._engine.content_of.assert_not_called()

    def test_invoking_a_macro_with_one_parameter(self):
        self._define_macro('\\foo', '(#1)', '{bar #1}')
        self._do_test_with('\\foo(1)', 'bar 1')

    def _define_macro(self, name, parameters, body):
        macro = self._macro(name, parameters, body)
        self._environment[name] = macro

    def _macro(self, name, parameters, body):
        return self._macros.create(name, self._factory.as_list(parameters), self._factory.as_list(body))

    def test_invoking_a_macro_where_one_argument_is_a_group(self):
        self._define_macro('\\foo', '(#1)', '{Text: #1}')
        self._do_test_with('\\foo({bar!})', 'Text: bar!')

    def test_invoking_a_macro_with_two_parameters(self):
        self._define_macro('\\point', '(#1,#2)', '{X=#1 and Y=#2}')
        self._do_test_with('\\point(12,{3 point 5})', 'X=12 and Y=3 point 5')

    def test_defining_a_macro_without_parameter(self):
        self._do_test_with('\\def\\foo{X}', '')
        self.assertEqual(self._macro('\\foo', '', '{X}'), self._environment['\\foo'])

    def test_defining_internal_macro(self):
        self._symbols.CHARACTER += '@'
        self._do_test_with('\\def\\internal@foo{\\internal@bar} \\internal@foo', ' \\internal@bar')
        self.assertEqual(self._macro('\\internal@foo', '', '{\\internal@bar}'), self._environment['\\internal@foo'])

    def test_defining_a_macro_with_one_parameter(self):
        self._do_test_with('\\def\\foo#1{X}', '')
        self.assertEqual(self._macro('\\foo', '#1', '{X}'), self._environment['\\foo'])

    def test_defining_a_macro_with_multiple_parameters(self):
        self._do_test_with('\\def\\point(#1,#2,#3){X}', '')
        self.assertEqual(self._macro('\\point', '(#1,#2,#3)', '{X}'), self._environment['\\point'])

    def test_macro(self):
        self._do_test_with('\\def\\foo{X}\\foo', 'X')

    def test_macro_with_one_parameter(self):
        self._do_test_with('\\def\\foo#1{x=#1}\\foo{2}', 'x=2')

    def test_macro_with_inner_macro(self):
        self._do_test_with('\\def\\foo#1{\\def\\bar#1{X #1} \\bar{#1}} \\foo{Y}', '  X Y')

    def test_macro_with_parameter_scope(self):
        self._do_test_with('\\def\\foo(#1,#2){\\def\\bar#1{Bar=#1}\\bar{#2} ; #1}\\foo(2,3)', 'Bar=3 ; 2')

    def test_parsing_input(self):
        self._engine.content_of.return_value = 'File content'
        self._do_test_with('\\input{my-file}', 'File content')
        self._engine.content_of.assert_called_once_with('my-file', ANY)

    def test_macro_with_inner_redefinition_of_input(self):
        self._engine.content_of.return_value = 'File content'
        self._do_test_with('\\def\\foo#1{\\def\\input#1{File: #1} \\input{#1}} \\foo{test.tex}', '  File: test.tex')

    def test_macro_with_inner_use_of_input(self):
        self._engine.content_of.return_value = 'blabla'
        self._do_test_with('\\def\\foo#1{File: \\input{#1}} \\foo{test.tex}', ' File: blabla')

    def test_rewriting_multiline_commands(self):
        self._engine.update_link.return_value = 'img_result'
        self._do_test_with('\\includegraphics % \n' + '[witdh=\\textwidth] % Blabla\n' + '{img/result.pdf}', '\\includegraphics % \n' + '[witdh=\\textwidth] % Blabla\n' + '{img_result}')
        self._engine.update_link.assert_called_once_with('img/result.pdf', ANY)

    def test_rewriting_includegraphics(self):
        self._engine.update_link.return_value = 'img_result'
        self._do_test_with('\\includegraphics{img/result.pdf}', '\\includegraphics{img_result}')
        self._engine.update_link.assert_called_once_with('img/result.pdf', ANY)

    def test_rewriting_includegraphics_with_parameters(self):
        self._engine.update_link.return_value = 'img_result'
        self._do_test_with('\\includegraphics[width=\\linewidth]{img/result.pdf}', '\\includegraphics[width=\\linewidth]{img_result}')
        self._engine.update_link.assert_called_once_with('img/result.pdf', ANY)

    def test_rewriting_graphicspath(self):
        self._do_test_with('\\graphicspath{{img}}', '\\graphicspath{{img}}')
        self._engine.record_graphic_path.assert_called_once_with(['img'], ANY)

    def test_rewriting_include(self):
        self._engine.shall_include.return_value = True
        self._engine.content_of.return_value = 'File content'
        self._do_test_with('\\include{my-file}', 'File content\\clearpage')
        self._engine.shall_include.assert_called_once_with('my-file')
        self._engine.content_of.assert_called_once_with('my-file', ANY)

    def test_rewriting_include_when_the_file_shall_not_be_included(self):
        self._engine.shall_include.return_value = False
        self._engine.content_of.return_value = 'File content'
        self._do_test_with('\\include{my-file}', '')
        self._engine.shall_include.assert_called_once_with('my-file')
        self._engine.content_of.assert_not_called()

    def test_rewriting_includeonly(self):
        self._engine.shall_include.return_value = True
        self._do_test_with('\\includeonly{my-file.tex}', '')
        self._engine.include_only.assert_called_once_with(['my-file.tex'], ANY)

    def test_rewriting_subfile(self):
        self._engine.content_of.return_value = '\\documentclass[../main.tex]{subfiles}\\begin{document}File content\\end{document}'
        self._do_test_with('\\subfile{my-file}', 'File content')
        self._engine.content_of.assert_called_once_with('my-file', ANY)

    def test_rewriting_document_class(self):
        self._do_test_with('\\documentclass{article}\\begin{document}Not much!\\end{document}', '\\documentclass{article}\\begin{document}Not much!\\end{document}')
        self._engine.relocate_dependency.assert_called_once_with('article', ANY)

    def test_rewriting_usepackage(self):
        self._do_test_with('\\usepackage{my-package}', '\\usepackage{my-package}')
        self._engine.relocate_dependency.assert_called_once_with('my-package', ANY)

    def test_rewriting_usepackage_with_options(self):
        self._do_test_with('\\usepackage[length=3cm,width=2cm]{my-package}', '\\usepackage[length=3cm,width=2cm]{my-package}')
        self._engine.relocate_dependency.assert_called_once_with('my-package', ANY)

    def test_rewriting_bibliography_style(self):
        self._engine.update_link_to_bibliography_style.return_value = 'my-style'
        self._do_test_with('\\bibliographystyle{my-style}', '\\bibliographystyle{my-style}')
        self._engine.update_link_to_bibliography_style.assert_called_once_with('my-style', ANY)

    def test_rewriting_make_index(self):
        self._engine.update_link_to_index_style.return_value = 'my-style.ist'
        self._do_test_with('\\makeindex[columns=3, title=Alphabetical Index,\n options= -s my-style.ist]', '\\makeindex[columns=3, title=Alphabetical Index,\n options= -s my-style.ist]')
        self._engine.update_link_to_index_style.assert_called_once_with('my-style.ist', ANY)

    def test_rewriting_endinput(self):
        self._do_test_with('foo \\endinput bar', 'foo ')
        self._engine.end_of_input.assert_called_once_with('Unknown', ANY)

    def test_rewriting_overpic(self):
        self._engine.update_link.return_value = 'img_result'
        self._do_test_with('\\begin{overpic}{img/result}blabla\\end{overpic}', '\\begin{overpic}{img_result}blabla\\end{overpic}')
        self._engine.update_link.assert_called_once_with('img/result', ANY)


if __name__ == '__main__':
    main()