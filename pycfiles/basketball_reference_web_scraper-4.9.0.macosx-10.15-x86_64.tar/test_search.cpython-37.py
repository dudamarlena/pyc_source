# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jaebradley/.virtualenvs/basketball_reference_web_scraper/lib/python3.7/site-packages/tests/integration/client/test_search.py
# Compiled at: 2020-03-05 11:58:34
# Size of source mod 2**32: 4969 bytes
import json, os
from unittest import TestCase
from basketball_reference_web_scraper import client
from basketball_reference_web_scraper.data import League, OutputType, OutputWriteOption

class TestSearchInMemory(TestCase):

    def test_search_ja(self):
        results = client.search(term='ja')
        self.assertGreaterEqual(498, len(results['players']))

    def test_search_jaebaebae(self):
        results = client.search(term='jaebaebae')
        self.assertListEqual([], results['players'])

    def test_search_results_key(self):
        results = client.search(term='jaebaebae')
        self.assertListEqual(list(results), ['players'])

    def test_length_of_kobe_search_results(self):
        results = client.search(term='kobe')
        self.assertEqual(4, len(results['players']))

    def test_players_in_kobe_search_results(self):
        results = client.search(term='kobe')
        self.assertListEqual([
         {'name':'Kobe Bryant', 
          'identifier':'bryanko01', 
          'leagues':{
           League.NATIONAL_BASKETBALL_ASSOCIATION}},
         {'name':'Ruben Patterson', 
          'identifier':'patteru01', 
          'leagues':{
           League.NATIONAL_BASKETBALL_ASSOCIATION}},
         {'name':'Dion Waiters', 
          'identifier':'waitedi01', 
          'leagues':{
           League.NATIONAL_BASKETBALL_ASSOCIATION}},
         {'name':'Oleksandr Kobets', 
          'identifier':'kobetol01', 
          'leagues':set()}], results['players'])

    def test_exact_search_result(self):
        results = client.search(term='kobe bryant')
        self.assertEqual([
         {'name':'Kobe Bryant', 
          'identifier':'bryanko01', 
          'leagues':{
           League.NATIONAL_BASKETBALL_ASSOCIATION}}], results['players'])

    def test_large_search_pagination(self):
        results = client.search(term='a')
        self.assertGreaterEqual(len(results['players']), 960)


class TestSearchJSONOutput(TestCase):

    def setUp(self):
        self.output_file_path = os.path.join(os.path.dirname(__file__), '../output/ko_search.json')
        self.expected_output_file_path = os.path.join(os.path.dirname(__file__), '../output/expected/ko_search.json')

    def tearDown(self):
        os.remove(self.output_file_path)

    def test_ko_search_json_output_includes_expected_json_output(self):
        client.search(term='ko',
          output_type=(OutputType.JSON),
          output_file_path=(self.output_file_path),
          output_write_option=(OutputWriteOption.WRITE))
        with open(self.output_file_path, 'r') as (output_file):
            with open(self.expected_output_file_path, 'r') as (expected_output_file):
                output_data = json.load(output_file)
                expected_output_data = json.load(expected_output_file)
                for expected_data_row in expected_output_data:
                    self.assertTrue(expected_data_row in output_data)


class TestSearchCSVOutput(TestCase):

    def setUp(self):
        self.output_file_path = os.path.join(os.path.dirname(__file__), '../output/ko_search.csv')
        self.expected_output_file_path = os.path.join(os.path.dirname(__file__), '../output/expected/ko_search.csv')

    def tearDown(self):
        os.remove(self.output_file_path)

    def test_ko_csv_output_search_includes_expected_csv_output(self):
        client.search(term='ko',
          output_type=(OutputType.CSV),
          output_file_path=(self.output_file_path),
          output_write_option=(OutputWriteOption.WRITE))
        with open(self.output_file_path, 'r') as (output_file):
            with open(self.expected_output_file_path, 'r') as (expected_output_file):
                output_data = output_file.readlines()
                expected_output_data = expected_output_file.readlines()
                for expected_data_row in expected_output_data:
                    if '-' not in expected_data_row:
                        self.assertTrue(expected_data_row in output_data)