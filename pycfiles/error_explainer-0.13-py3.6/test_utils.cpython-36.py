# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/test/test_utils.py
# Compiled at: 2020-04-06 02:33:21
# Size of source mod 2**32: 1674 bytes
from unittest import TestCase
from typing import NoReturn, List, Union
from error_explainer.check_runner import run_checks
from error_explainer.messages import get_formatted_message

def run_sanity_test(test_case: TestCase, path: str) -> NoReturn:
    """
    Run test case for sanity test that uses a broken print("foo" line in the otherwise correct sample to get past the
    compilation test. Expected outcome is is one missing_brackets.normal.closing message on line 1
    :param test_case: self of TestCase
    :param path: path to file
    """
    expected_message = get_formatted_message('missing_brackets.normal.closing',
      count=1, line_start=1, line_end=1)
    run_test_scenario(test_case, path, 1, expected_message)


def run_test_scenario(test_case: TestCase, path: str, expected_messages_count: int, expected_messages: Union[(List[str], str, None)]) -> NoReturn:
    """
    Default test scenario for checking errors in a python file.
    :param test_case: self of TestCase
    :param path: path to file
    :param expected_messages_count: number of expected messages
    :param expected_messages: 1 or more expected messages can be string or list
    """
    messages = run_checks(path)
    print(f"expected {expected_messages}")
    print(f"actual {messages}")
    test_case.assertEqual(expected_messages_count, len(messages))
    if expected_messages is not None:
        if type(expected_messages) == str:
            expected_messages = [
             expected_messages]
        test_case.assertTrue(set(expected_messages) == set(messages))