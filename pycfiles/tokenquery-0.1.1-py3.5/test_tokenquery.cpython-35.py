# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/tokenquery/tests/test_tokenquery.py
# Compiled at: 2017-01-28 20:28:20
# Size of source mod 2**32: 9220 bytes
import unittest
from tokenquery.nlp.tokenizer import Tokenizer
from tokenquery.nlp.pos_tagger import POSTagger
from tokenquery.tokenquery import TokenQuery

class TestTokenQueryClass(unittest.TestCase):

    def show_results(self, result):
        for group in result:
            print('=========')
            for chunk_name in group:
                print('---' + chunk_name + '---')
                chunk = group[chunk_name]
                for token in chunk:
                    print(token.get_token_id())
                    print(token.get_text())

    def assert_result(self, result, desired_result):
        self.assertEqual(len(result), len(desired_result))
        for group, desired_group in zip(result, desired_result):
            for chunk_name in group:
                self.assertIn(chunk_name, desired_group)
                chunk = group[chunk_name]
                desired_chunk = desired_group[chunk_name]
                for token, desired_token in zip(chunk, desired_chunk):
                    self.assertEqual(token.get_token_id(), desired_token.get_token_id())

    def test_regex_match(self):
        t = Tokenizer()
        input_tokens = t.tokenize('David is a painter and Ramtin Muller is an artist.')
        input_tokens[0].add_a_label('ner', 'PERSON')
        input_tokens[1].add_a_label('pos', 'VBZ')
        input_tokens[2].add_a_label('pos', 'DT')
        input_tokens[5].add_a_label('ner', 'PERSON')
        input_tokens[6].add_a_label('ner', 'PERSON')
        input_tokens[7].add_a_label('pos', 'VBZ')
        test_cases = []
        desired_results = []
        test_cases += ['[ner:"PERSON"]+ [pos:"VBZ"] [/an?/] [/artist|painter/]']
        desired_results.append([{'chunk 1': input_tokens[:4]},
         {'chunk 1': input_tokens[5:10]},
         {'chunk 1': input_tokens[6:10]}])
        test_cases += ['([ner:"NUMBER"]+) [/km|kilometers?/]']
        desired_results.append([])
        test_cases += ['[ner:"PERSON"]? [pos:/V.*/]']
        desired_results.append([{'chunk 1': input_tokens[:2]},
         {'chunk 1': input_tokens[1:2]},
         {'chunk 1': input_tokens[6:8]},
         {'chunk 1': input_tokens[7:8]}])
        for test_case, desired_result in zip(test_cases, desired_results):
            unit = TokenQuery(test_case)
            result = unit.match_tokens(input_tokens)
            self.assert_result(result, desired_result)

    def test_repetition(self):
        t = Tokenizer()
        input_tokens = t.tokenize('David is a painter and Ramtin Muller is an artist. Sir Isaac Newton ...')
        input_tokens[0].add_a_label('ner', 'PERSON')
        input_tokens[1].add_a_label('pos', 'VBZ')
        input_tokens[2].add_a_label('pos', 'DT')
        input_tokens[5].add_a_label('ner', 'PERSON')
        input_tokens[6].add_a_label('ner', 'PERSON')
        input_tokens[7].add_a_label('pos', 'VBZ')
        input_tokens[11].add_a_label('ner', 'PERSON')
        input_tokens[12].add_a_label('ner', 'PERSON')
        input_tokens[13].add_a_label('ner', 'PERSON')
        test_cases = []
        desired_results = []
        test_cases += ['[ner:str_eq(PERSON)]*']
        desired_results.append([{'chunk 1': input_tokens[:1]},
         {'chunk 1': input_tokens[5:7]},
         {'chunk 1': input_tokens[6:7]},
         {'chunk 1': input_tokens[11:14]},
         {'chunk 1': input_tokens[12:14]},
         {'chunk 1': input_tokens[13:14]}])
        test_cases += ['[ner:str_eq(PERSON)]?']
        desired_results.append([{'chunk 1': input_tokens[:1]},
         {'chunk 1': input_tokens[5:6]},
         {'chunk 1': input_tokens[6:7]},
         {'chunk 1': input_tokens[11:12]},
         {'chunk 1': input_tokens[12:13]},
         {'chunk 1': input_tokens[13:14]}])
        test_cases += ['[ner:str_eq(PERSON)]+']
        desired_results.append([{'chunk 1': input_tokens[:1]},
         {'chunk 1': input_tokens[5:7]},
         {'chunk 1': input_tokens[6:7]},
         {'chunk 1': input_tokens[11:14]},
         {'chunk 1': input_tokens[12:14]},
         {'chunk 1': input_tokens[13:14]}])
        test_cases += ['[ner:str_eq(PERSON)]{2}']
        desired_results.append([{'chunk 1': input_tokens[5:7]},
         {'chunk 1': input_tokens[11:13]},
         {'chunk 1': input_tokens[12:14]}])
        test_cases += ['[ner:str_eq(PERSON)]{1,2}']
        desired_results.append([{'chunk 1': input_tokens[:1]},
         {'chunk 1': input_tokens[5:7]},
         {'chunk 1': input_tokens[6:7]},
         {'chunk 1': input_tokens[11:13]},
         {'chunk 1': input_tokens[12:14]},
         {'chunk 1': input_tokens[13:14]}])
        for test_case, desired_result in zip(test_cases, desired_results):
            unit = TokenQuery(test_case)
            result = unit.match_tokens(input_tokens)
            self.assert_result(result, desired_result)

    def test_logics(self):
        t = Tokenizer()
        input_tokens = t.tokenize('David is a painter and Ramtin Muller is an artist. Sir Isaac Newton ...')
        input_tokens[0].add_a_label('ner', 'PERSON')
        input_tokens[1].add_a_label('pos', 'VBZ')
        input_tokens[2].add_a_label('pos', 'DT')
        input_tokens[5].add_a_label('ner', 'PERSON')
        input_tokens[6].add_a_label('ner', 'PERSON')
        input_tokens[7].add_a_label('pos', 'VBZ')
        input_tokens[11].add_a_label('ner', 'PERSON')
        input_tokens[12].add_a_label('ner', 'PERSON')
        input_tokens[13].add_a_label('ner', 'PERSON')
        test_cases = []
        desired_results = []
        test_cases += ['[ner:str_eq(PERSON)]+ [pos:str_eq(VBZ)] [/an?/] [str_eq(painter)]']
        test_cases += ['[ner:str_eq(PERSON)]+ [pos:str_eq(VBZ)] [/an?/&"a"] [str_eq(painter)]']
        test_cases += ['[ner:str_eq(PERSON)]+ [pos:str_eq(VBZ)] [/an?/&pos:"DT"] [str_eq(painter)]']
        test_cases += ['[ner:str_eq(PERSON)]+ [pos:str_eq(VBZ)] [/an?/&pos:str_eq(DT)] [str_eq(painter)]']

    def test_capturing(self):
        test_cases = []
        desired_results = []
        test_cases += ['[ner:"PERSON"]+ [pos:"VBZ"] [/an?/] ["painter"]']
        test_cases += ['([ner:"PERSON"]+) [pos:"VBZ"] [/an?/] ["painter"]']
        test_cases += ['([ner:"PERSON"]+ [pos:"VBZ"]) [/an?/] ["painter"]']
        test_cases += ['([ner:"PERSON"]+ [pos:"VBZ"] )[/an?/] ["painter"]']
        test_cases += ['[ner:"PERSON"]+ ([pos:"VBZ"] [/an?/] ["painter"])']

    def test_by_pos_tag(self):
        tokenizer = Tokenizer('PTBTokenizer')
        pos_tagger = POSTagger()
        test_text = "\n                    I am a painter, you're also a painter!\n                    "
        tokens = tokenizer.tokenize(test_text)
        tokens = pos_tagger.tag(tokens)


if __name__ == '__main__':
    unittest.main()